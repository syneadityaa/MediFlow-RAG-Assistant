"""Step 1-2: load documents from the knowledge_base folder and extract their text."""
from pathlib import Path

from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}


def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n\n".join((page.extract_text() or "") for page in reader.pages)


def load_documents(folder) -> list[dict]:
    """Return [{'source': 'file.md', 'text': '...'}]. Missing folder or empty files are skipped."""
    folder = Path(folder)
    if not folder.is_dir():
        return []

    documents = []
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            if path.suffix.lower() == ".pdf":
                text = _read_pdf(path)
            else:
                text = path.read_text(encoding="utf-8")
        except Exception as exc:  # unreadable file should not crash the app
            print(f"[document_loader] Skipped {path.name}: {exc}")
            continue

        text = text.strip()
        if text:
            documents.append({"source": path.name, "text": text})
    return documents