# 📄 Document Change Detector

A Streamlit-based application that compares two versions of a PDF and detects **added, removed, modified, and unchanged sections** using semantic similarity, text comparison, and an LLM.

## 🚀 Project Overview

The Document Change Detector allows users to upload an **OLD PDF** and a **NEW PDF**.

The system:

1. Extracts text from both PDFs.
2. Splits the documents into sections.
3. Converts sections into embeddings.
4. Uses FAISS to find semantically similar sections.
5. Classifies sections as:
   - Added
   - Removed
   - Modified
   - Unchanged
6. Uses `difflib` to identify textual differences.
7. Uses a Groq-powered LLM to generate a clear explanation of modifications.
8. Displays the complete comparison through a Streamlit interface.

## ✨ Features

- 📕 Upload OLD PDF
- 📗 Upload NEW PDF
- 🔍 Semantic section matching
- 🟢 Unchanged section detection
- 🟡 Modified section detection
- 🔵 Added section detection
- 🔴 Removed section detection
- ❌ Word-level difference detection
- 🤖 AI-generated change explanations
- 📊 Comparison summary
- 📄 Page-level information
- 📈 Semantic similarity scores

## 🧠 How It Works

```text
OLD PDF
   │
   ▼
Text Extraction
   │
   ▼
Section Chunking
   │
   ▼
Embeddings
   │
   ▼
FAISS


NEW PDF
   │
   ▼
Text Extraction
   │
   ▼
Section Chunking
   │
   ▼
Embeddings
   │
   ▼
FAISS

        OLD ↔ NEW
           │
           ▼
    Semantic Matching
           │
           ▼
 ┌─────────────────────┐
 │ Change Classification│
 └─────────────────────┘
           │
     ┌─────┼─────┬─────────┐
     ▼     ▼     ▼         ▼
  Added Removed Modified Unchanged
                    │
                    ▼
                 difflib
                    │
                    ▼
                Groq LLM
                    │
                    ▼
             AI Explanation