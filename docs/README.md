-- Document Extractor --

This service will extract data from uploaded documents from fileType like Pdf or scanned images

- Language: Python, FastAPI
- Main Packages: 
- OCR Layer: PaddleOCR / Tesseract
- Monitoring: Prometheus + Grafana
- LLm Inference: OpenAI / Ollama
- DB: PostgreSQL
- Job Queue: BullMQ / Celery

# OCR + Layout Parsing Layer
Extract visual and text data with layout info (bounding boxes, font size, tables).

Two branches:
If PDF is scanned/image-based → use OCR

If PDF is native/text-based → use direct extraction

OCR Tools:
🧠 PaddleOCR (accurate + supports layout)

🧠 Tesseract (lightweight, customizable)

🧠 DocTR (deep learning based)

Optional: LayoutParser or Adobe Extract API for document structure

# LLM-based Field Extraction
Extract semantic fields using LLMs.

Two Approaches:
Few-shot prompts: Provide examples of what to extract

Schema-based extraction: Provide a field schema (e.g., "invoice_number", "due_date")

Models:
Hosted: OpenAI (GPT-4), Claude, Gemini

Local: Mistral-7B, LLaMA3, Zephyr, Mixtral via Ollama, vLLM, or llama.cpp

# Data Structuring and Validation Layer
Ensure the output is usable, structured, and correct.

Tasks:
Validate types: dates, numbers, etc.

Apply fuzzy matching or regex fallback if LLM fails

Normalize currency, dates, addresses


# Visual Roadmap

[Document Upload] 
      ↓
[OCR + Layout Parsing]
      ↓
[LLM-based Field Extraction]
      ↓
[Validation + Normalization]
      ↓
[Structured JSON Output]
      ↓
[Feedback / Audit / Retraining]
