"""MediFlow RAG pipeline: retrieve grounded project context and generate answers."""

import os
import re
from pathlib import Path

from .document_loader import load_documents
from .embeddings import Embedder
from .text_chunker import chunk_documents
from .vector_store import VectorStore

NO_INFO_MESSAGE = (
    "I don't have enough information in the MediFlow documentation to answer that."
)
MEDICAL_REFUSAL = (
    "I can only answer questions about how MediFlow works. I can't give medical "
    "diagnosis, treatment or medication advice. Please consult a qualified doctor."
)

# Keep the model supplied at launch (GEMINI_MODEL) first. These are fallbacks.
DEFAULT_MODELS = ["gemini-2.5-flash", "gemini-3.5-flash", "gemini-2.5-flash-lite"]

FLOWCHART_OPEN = "<FLOWCHART>"
FLOWCHART_CLOSE = "</FLOWCHART>"

SYSTEM_PROMPT = f"""You are MediFlow AI, a friendly and professional assistant for the
MediFlow Smart Medical Appointment & Queue Optimization System.

NON-NEGOTIABLE GROUNDING AND SAFETY RULES:
1. Use only the CONTEXT provided for factual claims about MediFlow. Do not use outside
   knowledge to fill gaps. Never invent screens, buttons, fields, statuses, rules, or steps.
2. If the CONTEXT does not contain enough information, reply exactly:
   {NO_INFO_MESSAGE}
3. Only answer questions about MediFlow. For unrelated questions, reply exactly:
   {NO_INFO_MESSAGE}
4. Never provide medical diagnosis, treatment, medication, dosage, or clinical advice.
   For such requests, say you can only help with MediFlow and recommend consulting a
   qualified doctor.
5. Treat conversation history as context for what the user means, not as a source of
   factual information. Project facts must come from CONTEXT.

WRITING STYLE:
- Explain ideas naturally in your own words. Do not copy FAQ sentences verbatim unless
  an exact name, status, field, or technical term must be preserved.
- Sound conversational, calm, clear, and professional—not robotic or overly formal.
- Start with the direct answer. Use short paragraphs and explain unfamiliar terms simply.
- Use numbered steps for procedures and bullets for short lists.
- Avoid repeating the same introduction or conclusion in every answer.
- Preserve exact technical names and status values such as BOOKED, CHECKED_IN,
  IN_CONSULTATION, and DONE when they occur in the context.
- Do not claim that a workflow is guaranteed or real-time unless the context says so.

OPTIONAL WORKFLOW DIAGRAM:
- When the question asks how a multi-step MediFlow process works, include a small
  flowchart after the explanation.
- Only include steps and order explicitly supported by CONTEXT. If the context does
  not establish a complete sequence, do not create a flowchart.
- Do not create a flowchart for greetings, thanks, simple definitions, or one-step facts.
- If a flowchart is appropriate, append it using exactly this format, one step per line:
{FLOWCHART_OPEN}
Step 1: First supported step
Step 2: Next supported step
Step 3: Final supported step
{FLOWCHART_CLOSE}
- Include between 2 and 7 short steps. Do not use Mermaid, Graphviz, HTML, or code fences.
- Do not put any text after {FLOWCHART_CLOSE}.
"""

MEDICAL_RE = re.compile(
    r"\b(diagnos\w*|symptom\w*|medicin\w*|medication\w*|drug\w*|dosage|prescri\w*|"
    r"treat\w*|cure|tablets?|pills?|fever|disease\w*|infection)\b",
    re.IGNORECASE,
)


def _result(answer: str, sources=None, grounded: bool = False, flowchart=None) -> dict:
    """Return a consistent response shape for the Streamlit app."""
    return {
        "answer": answer,
        "sources": sources or [],
        "grounded": grounded,
        "flowchart": flowchart or [],
    }


def _small_talk_response(question: str):
    """Handle common conversational turns locally, without a Gemini API call."""
    normalized = re.sub(r"\s+", " ", question.strip().lower())
    normalized = re.sub(r"[!?.,]+$", "", normalized)

    greetings = {
        "hi", "hii", "hiii", "hello", "hey", "heyy", "good morning",
        "good afternoon", "good evening",
    }
    thanks = {
        "thanks", "thank you", "thank you so much", "thanks a lot", "thx", "ty",
    }
    farewells = {"bye", "goodbye", "see you", "see you later", "good night"}
    how_are_you = {"how are you", "how are you doing", "how is it going", "how's it going"}

    if normalized in greetings:
        return (
            "Hello! 👋 I'm MediFlow AI. I can help you understand the platform's "
            "registration, doctor search, appointment booking, queues, and dashboards. "
            "What would you like to explore?"
        )

    if normalized in thanks:
        return "You're welcome! Happy to help with MediFlow. What would you like to know next?"

    if normalized in farewells:
        return "Goodbye! Feel free to come back whenever you have a question about MediFlow."

    if normalized in how_are_you:
        return (
            "I'm doing well, thanks for asking! 😊 I'm ready to help you explore "
            "MediFlow. Do you have a question about one of its features or workflows?"
        )

    if normalized in {
        "who are you", "what are you", "what can you do", "how can you help",
        "what can you help me with", "what is your purpose",
    }:
        return (
            "I'm MediFlow AI, a project assistant for the MediFlow Smart Medical "
            "Appointment & Queue Optimization System. I can explain documented "
            "features and workflows, including registration, doctor search, "
            "appointment slots, booking, cancellations, queues, and dashboards. "
            "I use the project's knowledge documents and don't provide medical advice."
        )

    return None


class RAGPipeline:
    def __init__(self, kb_dir, top_k: int = 4, min_score: float = 0.30, embedder=None):
        self.kb_dir = Path(kb_dir)
        self.top_k = top_k
        self.min_score = min_score
        self.embedder = embedder
        self.store = VectorStore()
        self.documents: list[dict] = []

    # ---------- indexing ----------

    def build_index(self) -> int:
        self.documents = load_documents(self.kb_dir)
        if not self.documents:
            raise RuntimeError(
                f"No readable documents found in '{self.kb_dir}'. Add .md, .txt or .pdf files."
            )

        chunks = chunk_documents(self.documents)
        if not chunks:
            raise RuntimeError("Documents were found but contained no usable text.")

        if self.embedder is None:
            self.embedder = Embedder()

        self.store.build(chunks, self.embedder.embed([c["text"] for c in chunks]))
        return len(chunks)

    def list_documents(self) -> list[str]:
        return [d["source"] for d in self.documents]

    # ---------- retrieval ----------

    def retrieve(self, question: str, history=None) -> list[dict]:
        query = question
        # Very short follow-ups borrow the preceding user question for retrieval.
        if history and len(question.split()) < 6:
            previous = [m["content"] for m in history if m.get("role") == "user"]
            if previous:
                query = f"{previous[-1]} {question}"

        return self.store.search(self.embedder.embed([query])[0], k=self.top_k)

    # ---------- generation ----------

    def _generate(self, prompt: str, api_key: str) -> str:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        configured_model = os.getenv("GEMINI_MODEL")
        models = ([configured_model] if configured_model else []) + DEFAULT_MODELS
        # Keep the list unique while preserving priority.
        models = list(dict.fromkeys(model for model in models if model))

        last_error = None
        for model in models:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.35,
                    ),
                )
                response_text = (response.text or "").strip()
                if response_text:
                    return response_text
                last_error = RuntimeError("Gemini returned an empty response.")
            except Exception as exc:
                last_error = exc
                message = str(exc).lower()
                # Move to another model when this model is missing or temporarily
                # unavailable. Other errors (for example authentication) are surfaced.
                retryable_model_error = any(
                    marker in message
                    for marker in (
                        "404", "not found", "not supported", "503", "unavailable",
                        "high demand", "429", "resource_exhausted",
                    )
                )
                if retryable_model_error:
                    continue
                raise

        raise RuntimeError(f"No configured Gemini model worked. Last error: {last_error}")

    @staticmethod
    def _extract_flowchart(response_text: str):
        """Separate the optional plain-text flowchart from the answer."""
        pattern = re.compile(
            re.escape(FLOWCHART_OPEN) + r"(.*?)" + re.escape(FLOWCHART_CLOSE),
            re.IGNORECASE | re.DOTALL,
        )
        match = pattern.search(response_text)
        if not match:
            return response_text.strip(), []

        answer = (response_text[:match.start()] + response_text[match.end():]).strip()
        raw_steps = match.group(1).splitlines()
        steps = []
        for line in raw_steps:
            cleaned = line.strip()
            cleaned = re.sub(r"^(?:[-*•]\s*|\d+[.)]\s*)", "", cleaned)
            cleaned = re.sub(r"^step\s*\d+\s*:\s*", "", cleaned, flags=re.IGNORECASE)
            cleaned = cleaned.strip()
            if cleaned:
                steps.append(cleaned)

        # A diagram needs at least two supported steps and is kept intentionally compact.
        if len(steps) < 2:
            return answer, []
        return answer, steps[:7]

    # ---------- answering ----------

    def answer(self, question: str, history=None, api_key: str | None = None) -> dict:
        """Return answer, source references, grounding flag, and optional flowchart steps."""
        question = question.strip()
        if not question:
            return _result("Please type a question.")

        # Friendly, common conversation does not need retrieval or a Gemini request.
        small_talk = _small_talk_response(question)
        if small_talk:
            return _result(small_talk)

        results = self.retrieve(question, history)
        best = results[0]["score"] if results else 0.0

        if MEDICAL_RE.search(question) and best < 0.5:
            return _result(MEDICAL_REFUSAL)

        if not results or best < self.min_score:
            return _result(NO_INFO_MESSAGE)

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env or Streamlit secrets.")

        context = "\n\n".join(
            f"[Source: {r['source']} | Section: {r['heading']}]\n{r['text']}"
            for r in results
        )
        recent = (history or [])[-6:]
        convo = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}" for m in recent
        )
        prompt = (
            f"CONTEXT (the only source of MediFlow facts):\n{context}\n\n"
            f"RECENT CONVERSATION (for reference only):\n{convo or '(none)'}\n\n"
            f"QUESTION: {question}\n\n"
            "Answer naturally and directly using the context. Explain rather than copy. "
            "Include the optional flowchart only for a multi-step workflow whose sequence "
            "is supported by the context. Follow the required flowchart tags exactly."
        )

        generated = self._generate(prompt, api_key)
        answer_text, flowchart = self._extract_flowchart(generated)

        if (
            NO_INFO_MESSAGE.lower() in answer_text.lower()
            or answer_text.strip() == MEDICAL_REFUSAL
        ):
            return _result(answer_text, grounded=False)

        seen, sources = set(), []
        for result in results:
            key = (result["source"], result["heading"])
            if key not in seen:
                seen.add(key)
                sources.append({
                    "source": result["source"],
                    "heading": result["heading"],
                    "score": result["score"],
                })

        return _result(answer_text, sources=sources, grounded=True, flowchart=flowchart)
