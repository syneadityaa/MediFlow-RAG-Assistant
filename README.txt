MediFlow AI conversation upgrade

Files in this archive (stored at the correct project-relative paths):
- app.py
- src/rag_pipeline.py

Install from the root of your existing MediFlow-RAG-Assistant project:

1. Make a backup of your current app.py and src/rag_pipeline.py.
2. Extract this ZIP directly into the MediFlow-RAG-Assistant folder.
   Allow the two files to be replaced. Other files are not included or changed.
3. Launch with your working Intel Mac settings:

   GEMINI_MODEL=gemini-3.5-flash-lite OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 streamlit run app.py

Changes:
- Common greetings, thanks, farewells, identity and capability prompts are handled locally.
- Gemini is instructed to explain project facts naturally rather than copy FAQ wording.
- For documented multi-step workflows, Gemini may return 2-7 grounded flowchart steps.
- Streamlit renders those steps as a compact vertical diagram.
- Existing document loading, chunking, Sentence Transformers, FAISS retrieval and Gemini call remain in place.

No knowledge-base files or dependency files are changed.
