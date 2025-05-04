# 🧠 Resume Parser & Candidate Ranker

This project uses **Natural Language Processing (NLP)** to automate resume parsing and rank candidates based on job relevance. It enables recruiters to efficiently shortlist the best candidates by extracting structured information from resumes and matching them against job descriptions.

## 🚀 Features

- 📄 **Resume Parsing** (PDF/DOCX): Extracts name, contact info, education, experience, skills, and certifications
- 🧠 **NLP-powered Entity Recognition**: Uses spaCy and custom logic to identify structured fields
- 🔍 **Skill Matching**: Compares extracted skills with job descriptions
- ⚖️ **Candidate Scoring**: Ranks resumes using customizable weight-based or ML-based scoring
- 📊 **REST API**: Built with FastAPI for easy integration
- 🔒 Optional bias detection (gender, age, etc.)

## 🛠 Tech Stack

- Python, spaCy, scikit-learn
- FastAPI (for REST endpoints)
- PyMuPDF / python-docx (for document parsing)
- Sentence Transformers (for semantic similarity)

## 📁 Project Structure

```
resume-parser/
├── parser/           # Resume text extraction & NLP logic
├── api/              # FastAPI endpoints
├── models/           # ML models and embeddings
├── data/             # Sample resumes & job descriptions
└── main.py           # Entry point
```

## ▶️ Getting Started

```bash
# Clone repo & setup
git clone https://github.com/your-username/resume-parser.git
cd resume-parser
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run the app
uvicorn api.main:app --reload
```

## 📬 API Endpoints

- `POST /parse`: Upload a resume, get structured JSON
- `POST /rank`: Submit multiple resumes + job description → get ranked results

## 📌 Todo

- [ ] Add frontend dashboard
- [ ] Train custom NER model on resumes
- [ ] Add export-to-CSV option

---
