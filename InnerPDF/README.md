# Adobe GenAI Hackathon Round 1B - PDF Document Understanding Pipeline

## Project Overview

This repository contains a modular Python pipeline to process, extract, and rank relevant textual information from PDF documents, targeting the requirements of the Adobe GenAI Hackathon Round 1B.

The pipeline includes:

- PDF Section Chunking based on Table of Contents (TOC)
- Semantic Section Ranking using SentenceTransformers (MiniLM model)
- Persona and Job Contextual Refinement of extracted text
- Generation of structured JSON outputs containing key sections and refined snippets
- Support for sequential processing of a batch of PDFs

---


## 🗂️ Project Structure
```bash
├── input/ 
├── output/ 
├── main.py
├── chunker.py 
├── ranker.py 
├── refiner.py 
├──download_model.py 
├── requirements.txt 
├── Dockerfile 
├── .dockerignore
├── README.md 
