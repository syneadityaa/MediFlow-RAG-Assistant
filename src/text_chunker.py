"""Step 3: split documents into chunks. Markdown is split by heading first,
then long sections are split by paragraph with a small overlap."""
import re

HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)")


def _split_sections(text: str) -> list[tuple[str, str]]:
    sections, heading, buffer = [], "Introduction", []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            body = "\n".join(buffer).strip()
            if body:
                sections.append((heading, body))
            heading, buffer = match.group(2).strip(), []
        else:
            buffer.append(line)
    body = "\n".join(buffer).strip()
    if body:
        sections.append((heading, body))
    return sections


def _split_long(body: str, max_chars: int, overlap: int) -> list[str]:
    if len(body) <= max_chars:
        return [body]

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    chunks, current = [], ""
    for para in paragraphs:
        if current and len(current) + len(para) + 2 > max_chars:
            chunks.append(current)
            current = (current[-overlap:] + "\n\n" + para) if overlap else para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current:
        chunks.append(current)

    final = []  # safety net for one huge paragraph
    for chunk in chunks:
        while len(chunk) > max_chars * 1.5:
            final.append(chunk[:max_chars])
            chunk = chunk[max_chars - overlap:]
        final.append(chunk)
    return final


def chunk_documents(documents: list[dict], max_chars: int = 800, overlap: int = 100) -> list[dict]:
    """Return [{'text', 'source', 'heading'}]. The heading is kept inside the text
    so each chunk stays understandable on its own."""
    chunks = []
    for doc in documents:
        for heading, body in _split_sections(doc["text"]):
            for piece in _split_long(body, max_chars, overlap):
                chunks.append(
                    {
                        "text": f"{heading}\n{piece}",
                        "source": doc["source"],
                        "heading": heading,
                    }
                )
    return chunks