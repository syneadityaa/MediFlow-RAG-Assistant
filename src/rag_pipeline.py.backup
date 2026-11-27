"""The full RAG pipeline: load -> chunk -> embed -> index -> retrieve -> generate."""
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

# Tried in order; a model that is unavailable (404 / not found) is skipped.
DEFAULT_MODELS = ["gemini-2.5-flash", "gemini-3.5-flash", "gemini-2.5-flash-lite"]

SYSTEM_PROMPT = f"""You are the MediFlow AI Assistant. MediFlow is a medical appointment and queue management web application.

Rules:
1. Answer ONLY using the CONTEXT provided. Never use outside knowledge and never invent features, buttons, steps or statuses.
2. If the CONTEXT does not contain the answer, reply with exactly: {NO_INFO_MESSAGE}
3. Only answer questions about MediFlow. For anything else, reply with exactly: {NO_INFO_MESSAGE}
4. Never give medical diagnosis, treatment or medication advice. If asked, say you can only help with MediFlow and suggest consulting a doctor.
5. Be concise and friendly. Use short steps or bullet points when explaining a process.
"""

MEDICAL_RE = re.compile(
    r"\b(diagnos\w*|symptom\w*|medicin\w*|medication\w*|drug\w*|dosage|prescri\w*|"
    r"treat\w*|cure|tablets?|pills?|fever|disease\w*|infection)\b",
    re.IGNORECASE,
)


class RAGPipeline:
    def __init__(self, kb_dir, top_k: int = 4, min_score: float = 0.30, embedder=None):
        self.kb_dir = Path(kb_dir)
        self.top_k = top_k
        self.min_score = min_score  # below this, the question is treated as "not in the docs"
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
        # Very short follow-ups ("and can I cancel it?") borrow the previous user question for retrieval.
        if history and len(question.split()) < 6:
            previous = [m["content"] for m in history if m["role"] == "user"]
            if previous:
                query = f"{previous[-1]} {question}"
        return self.store.search(self.embedder.embed([query])[0], k=self.top_k)

    # ---------- generation ----------
    def _generate(self, prompt: str, api_key: str) -> str:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        models = ([os.getenv("GEMINI_MODEL")] if os.getenv("GEMINI_MODEL") else []) + DEFAULT_MODELS
        last_error = None
        for model in models:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT, temperature=0.2
                    ),
                )
                text = (response.text or "").strip()
                if text:
                    return text
                last_error = RuntimeError("Gemini returned an empty response.")
            except Exception as exc:
                last_error = exc
                message = str(exc).lower()
                if "404" in message or "not found" in message or "not supported" in message:
                    continue  # try the next model name
                raise
        raise RuntimeError(f"No Gemini model worked. Last error: {last_error}")

    def answer(self, question: str, history=None, api_key: str | None = None) -> dict:
        """Return {'answer': str, 'sources': [{'source','heading','score'}], 'grounded': bool}."""
        question = question.strip()
        if not question:
            return {"answer": "Please type a question.", "sources": [], "grounded": False}

        results = self.retrieve(question, history)
        best = results[0]["score"] if results else 0.0

        if MEDICAL_RE.search(question) and best < 0.5:
            return {"answer": MEDICAL_REFUSAL, "sources": [], "grounded": False}
        if not results or best < self.min_score:
            return {"answer": NO_INFO_MESSAGE, "sources": [], "grounded": False}
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env or Streamlit secrets.")

        context = "\n\n".join(
            f"[Source: {r['source']} | Section: {r['heading']}]\n{r['text']}" for r in results
        )
        recent = (history or [])[-6:]
        convo = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in recent)
        prompt = (
            f"CONTEXT:\n{context}\n\n"
            f"RECENT CONVERSATION:\n{convo or '(none)'}\n\n"
            f"QUESTION: {question}\n\nANSWER:"
        )
        text = self._generate(prompt, api_key)

        if NO_INFO_MESSAGE.lower() in text.lower() or text.strip() == MEDICAL_REFUSAL:
            return {"answer": text, "sources": [], "grounded": False}

        seen, sources = set(), []
        for r in results:
            key = (r["source"], r["heading"])
            if key not in seen:
                seen.add(key)
                sources.append({"source": r["source"], "heading": r["heading"], "score": r["score"]})
        return {"answer": text, "sources": sources, "grounded": True}