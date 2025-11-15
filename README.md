# 📚 Ed-Guide
### Curriculum-Aligned Lesson Plan Generator using LLM + RAG

---

## 📑 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture Overview](#-architecture-overview)
  - [1️⃣ rag.ipynb – Curriculum Preprocessing & Vector Store Creation](#1️⃣-ragipynb--curriculum-preprocessing--vector-store-creation)
  - [2️⃣ ui.py – Streamlit App for Lesson Plan Generation](#2️⃣-uipy--streamlit-app-for-lesson-plan-generation)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Set Your OpenAI API Key](#-set-your-openai-api-key)
- [Building the Vector Stores (RAG Setup)](#-building-the-vector-stores-rag-setup)
- [Running the App](#-running-the-app)
- [Future Enhancements](#-future-enhancements)

---

## 🔍 Overview

Ed-Guide is an AI-powered teaching assistant that generates **curriculum-aligned lesson plans** using:

- 📄 Official curriculum PDFs (per country)
- 🧠 RAG over Chroma vector stores
- 💬 GPT-4 for structured, personalized lesson planning

This tool is designed for tutors, teachers, and students who want **accurate, local-curriculum–aligned lesson plans** with follow-up explanation support.

---

## 🧩 Key Features

- 🌍 **Multi-country curriculum support** (Australia, India, USA, UK, Europe)
- 🧠 **RAG-powered retrieval** from country curriculum PDFs
- 🎯 **Personalized lesson plan generation** based on:
  - Grade level  
  - Subject  
  - Duration  
  - Focus area (Theory / Practice / Balanced)
  - Special needs support
- 🔁 **Follow-up conversational Q&A** with context retention
- 🎮 **Gamified activities**, **practice questions**, and **model answers**
- 📝 **Full lesson plan structure** including:
  - Learning objectives  
  - Warm-up  
  - Theory  
  - Activities  
  - Differentiation  
  - Reflection prompts  

---

## 🏗 Architecture Overview

### 1️⃣ `rag.ipynb` – Curriculum Preprocessing & Vector Store Creation

This notebook:

- Loads and extracts text from curriculum PDFs  
- Splits text into chunks using `CharacterTextSplitter`
- Embeds using **OpenAIEmbeddings**
- Creates Chroma vector stores per country:
  ```
  chroma_dbs/
    ├── chroma_Australia/
    ├── chroma_Europe/
    ├── chroma_India/
    ├── chroma_UK/
    └── chroma_USA/
  ```

Used **once**, unless you update or add new PDFs.

---

### 2️⃣ `ui.py` – Streamlit App for Lesson Plan Generation

The UI provides:

- Sidebar configuration for:
  - Country  
  - Subject  
  - Grade level  
  - Focus topic  
  - Special needs  
  - Lesson duration  
  - Focus area  
- Loads relevant vector store  
- Retrieves curriculum context  
- Passes context + user parameters to GPT-4 via structured prompts  
- Generates:
  - A full curriculum-aligned lesson plan  
  - Follow-up answers using **conversation state**  
- Uses **Lottie animations** for polished UI

---

## 📁 Project Structure

```
Ed-Guide/
│
├── ui.py                 # Streamlit application
├── rag.ipynb             # Vector store creation pipeline
├── animation.json        # Lottie animation for UI loader
└── README.md             # Documentation (this file)
```

You must supply your own curriculum PDFs in folders:

```
Australia/
Europe/
India/
UK/
USA/
```

Then generate vector stores using `rag.ipynb`.

---

## 🛠 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Varshith-Y/Ed-Guide.git
cd Ed-Guide
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

Create a `requirements.txt` with these (or ask me to generate one):

```
streamlit
openai
python-dotenv
langchain
langchain-openai
langchain-community
langchain-chroma
chromadb
PyPDF2
nltk
evaluate
rouge-score
tiktoken
numpy
pandas
Pillow
streamlit-lottie
```

Install:

```bash
pip install -r requirements.txt
```

---

## 🔑 Set Your OpenAI API Key

```bash
export OPENAI_API_KEY="yourapikey"    # macOS/Linux
setx OPENAI_API_KEY "yourapikey"      # Windows
```

Avoid hardcoding API keys in scripts.

---

## 🧮 Building the Vector Stores (RAG Setup)

Before using the app:

1. Put curriculum PDFs inside folders:  
   `Australia/`, `Europe/`, `India/`, `USA/`, `UK/`

2. Run **rag.ipynb**  
   It will:
   - Extract text  
   - Chunk  
   - Embed  
   - Save into `chroma_dbs/chroma_{country}`

3. Ensure `chroma_dbs/` contains all required directories.

---

## ▶ Running the App

After vector stores are ready:

```bash
streamlit run ui.py
```

Then:

- Select curriculum country
- Choose student age + subject
- (Optional) Add special needs
- Choose lesson duration and focus area
- Click **Generate Lesson Plan**
- Scroll down to ask follow-up questions

---

## 🚀 Future Enhancements

- Export lesson plans as PDF/DOCX  
- Add International Baccalaureate (IB) curriculum  
- Add student interactive mode  
- Add multi-language support  
- Advanced analytics for tutors  

---

Feel free to adapt with a standard license (MIT, Apache 2.0, etc.).

