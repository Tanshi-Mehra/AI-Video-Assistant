# AI Video Assistant

An AI-powered Video & Meeting Assistant that automatically transcribes videos, generates concise summaries, extracts action items and key decisions, and allows users to chat with the video using Retrieval-Augmented Generation (RAG).

---

# Features

* Upload local video files
* Process YouTube videos
* Speech-to-Text Transcription
* Hindi/Hinglish to English Translation
* AI-powered Summarization
* Automatic Action Item Extraction
* Key Decision Extraction
* Open Question Identification
* Chat with Video using RAG
* Semantic Search over Transcript
* Complete Transcript Viewer

---

# Project Architecture

```text
Input Video / YouTube URL
          │
          ▼
 Audio Extraction (FFmpeg)
          │
          ▼
 Audio Chunking (Pydub)
          │
          ▼
 Speech-to-Text (Whisper / Sarvam AI)
          │
          ▼
 Transcript Generation
          │
          ▼
 LangChain + Mistral LLM
          │
          ├── Summary
          ├── Title
          ├── Action Items
          ├── Key Decisions
          ├── Questions
          │
          ▼
 ChromaDB Vector Store
          │
          ▼
 Retrieval-Augmented Generation (RAG)
          │
          ▼
 Interactive Chat
```

---

# Tech Stack

* Python
* Streamlit
* LangChain
* Mistral AI
* OpenAI Whisper
* Sarvam AI
* ChromaDB
* Hugging Face Embeddings
* FFmpeg
* Pydub
* yt-dlp
* Retrieval-Augmented Generation (RAG)

---

# Project Structure

```text
AI-Video-Assistant/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
│
├── utils/
│   ├── audio_processor.py
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── vector_store.py
│
├── temp/
├── chroma_db/
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd AI-Video-Assistant
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a file named `.env` in the project root.

Example:

```env
# Mistral AI API Key
MISTRAL_API_KEY=your_mistral_api_key

# Sarvam AI API Key (Hindi/Hinglish Translation)
SARVAM_API_KEY=your_sarvam_api_key

# Optional: OpenAI API Key (Only if using OpenAI APIs)
OPENAI_API_KEY=your_openai_api_key
```

> **Note**
>
> If you are using the **local OpenAI Whisper model (`openai-whisper`)**, no API key is required. Whisper runs locally on your machine.
>
> If you are using the **OpenAI Whisper API**, add your `OPENAI_API_KEY` to the `.env` file.

---

# Running the Project

```bash
streamlit run app.py
```

The application will start locally and open in your default web browser.

---

# How It Works

1. Upload a local video or provide a YouTube URL.
2. Audio is extracted from the video using FFmpeg.
3. The audio is split into smaller chunks using Pydub.
4. Whisper converts speech into text.
5. Sarvam AI translates Hindi/Hinglish speech into English when required.
6. LangChain processes the transcript with the Mistral Large Language Model.
7. The application generates:

   * Video Title
   * Summary
   * Action Items
   * Key Decisions
   * Open Questions
8. Transcript embeddings are stored in ChromaDB.
9. Users can ask natural-language questions, which are answered using a Retrieval-Augmented Generation (RAG) pipeline.

---

# Real-World Applications

* Corporate Meeting Assistant
* Lecture Summarization
* Podcast Analysis
* YouTube Video Summaries
* Interview Analysis
* Customer Support Call Analysis
* Medical Consultation Documentation
* Legal Meeting Documentation

---

# Future Improvements

* Speaker Diarization
* Timestamped Summaries
* Multi-language Support
* Live Meeting Transcription
* Cloud-based Vector Database
* PDF/DOCX Export
* Meeting Analytics Dashboard
* Multi-Agent AI Workflow

---

# License

This project is intended for educational and research purposes.
