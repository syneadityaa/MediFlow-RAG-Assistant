# MediFlow AI Assistant 🤖

### An AI-powered RAG chatbot for the MediFlow healthcare appointment platform

MediFlow AI Assistant is an intelligent chatbot designed to help users understand the features and workflows of the MediFlow application.

Built using **Python, Streamlit, Google Gemini, and Retrieval-Augmented Generation (RAG)**, it retrieves relevant information from a dedicated knowledge base before generating answers.

The goal is to make MediFlow's documentation easier to access through a conversational AI interface.

## ✨ Features

- **Context-aware Q&A:** Answers questions using MediFlow-specific documentation.
- **Retrieval-Augmented Generation:** Retrieves relevant knowledge before generating responses.
- **Semantic Search:** Finds relevant content based on the meaning of a question.
- **Gemini-powered Responses:** Generates natural-language answers using Google's Gemini API.
- **Document Processing:** Supports PDF text extraction.
- **Dedicated Knowledge Base:** Organizes information about registration, authentication, doctors, appointments, queues, and dashboards.
- **Interactive Chat Interface:** Provides a simple interface using Streamlit.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Chat interface |
| Google Gemini API | Response generation |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| NumPy | Numerical operations |
| PyPDF | PDF text extraction |

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation pipeline.

```text
MediFlow Documentation
         |
         v
   Document Loading
         |
         v
    Text Chunking
         |
         v
  Embedding Generation
         |
         v
    FAISS Vector Store
         |
         |
 User Question
         |
         v
  Query Embedding
         |
         v
  Semantic Retrieval
         |
         v
 Relevant Context
         |
         v
    Gemini API
         |
         v
   AI-generated Answer
```

### RAG Pipeline

1. **Document Loading:** Loads information from the MediFlow knowledge base and supported PDF documents.
2. **Text Chunking:** Divides documents into smaller sections.
3. **Embedding Generation:** Converts text into numerical vector representations.
4. **Vector Storage:** Stores embeddings for similarity-based retrieval.
5. **Semantic Retrieval:** Finds relevant information for the user's question.
6. **Response Generation:** Uses the retrieved context to generate an answer through Gemini.

## 📁 Project Structure

```text
MediFlow-RAG-Assistant/
│
├── assets/
├── knowledge_base/
├── src/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/syneadityaa/MediFlow-RAG-Assistant.git
cd MediFlow-RAG-Assistant
```

### 2. Create a virtual environment

Python 3.11 is recommended.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root using `.env.example` as a reference.

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get your API key from [Google AI Studio](https://aistudio.google.com/).

**Security:** Never upload your actual `.env` file or API key to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## 💬 Example Questions

- How do I register on MediFlow?
- How can I search for doctors?
- How do I book an appointment?
- How does the appointment queue work?
- Can patients cancel appointments?
- What features are available in the doctor dashboard?

## 🔒 Scope and Limitations

MediFlow AI Assistant is intended to provide information about the MediFlow application.

- It is not a medical diagnosis or treatment assistant.
- It does not prescribe medicines or recommend treatments.
- Its answers depend on the available knowledge base.
- It does not independently access live patient records or hospital databases.

## 🚀 Future Enhancements

- Integration with the main MediFlow application.
- Improved retrieval accuracy.
- Source references for generated answers.
- Conversation history and context retention.
- Authentication-aware access to application information.

## 🎯 Objective

This project explores how Large Language Models and Retrieval-Augmented Generation can be used to build application-specific AI assistants.

It demonstrates how semantic retrieval and generative AI can work together to provide contextual answers from a controlled knowledge base.

## 👨‍💻 Author

**Aditya Raj**

B.Tech – Computer Science and Engineering (AI & ML)

GitHub: [@syneadityaa](https://github.com/syneadityaa)

---

*An AI extension to the MediFlow Smart Medical Appointment and Queue Optimization project.*