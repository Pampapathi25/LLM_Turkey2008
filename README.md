# Local LLM Pipeline 

## Overview

This project implements a complete **Local Large Language Model (LLM) pipeline** to analyse a **United Nations Human Development Report (HDR)** for an assigned country. The system extracts structured development indicators, summarises report chapters, evaluates LLM outputs using a second local model, and presents the extracted information through an interactive dashboard.

The project was developed as part of the MSc Data Science module on Natural Language Processing and Large Language Models.

---

## Objectives

* Extract text from a UN Human Development Report (PDF)
* Clean and segment the document into meaningful chunks
* Generate an overall report summary
* Produce chapter-wise summaries
* Extract thematic information from the report
* Identify key strengths and development challenges
* Extract numerical development indicators in JSON format
* Compare outputs from multiple local LLMs
* Evaluate extraction quality using a second LLM
* Visualise the extracted information in an interactive dashboard

---

## Technologies Used

* Python 3.x
* Ollama
* Llama 3
* Phi-3
* Gemma 2 (optional model comparison)
* PyMuPDF
* Pandas
* Plotly
* Matplotlib
* Streamlit

---

## Project Structure

```text
LLM-UN-HDR/
│
├── data/
│   └── report.pdf
│
├── outputs/
│   ├── summaries/
│   ├── json/
│   ├── csv/
│   └── plots/
│
├── src/
│   ├── extract_text.py
│   ├── chunk_text.py
│   ├── summarise.py
│   ├── thematic_extraction.py
│   ├── indicator_extraction.py
│   ├── evaluation.py
│   └── dashboard.py
│
├── requirements.txt
├── README.md
└── main.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/your-repository.git
```

Move into the project directory:

```bash
cd your-repository
```

Create a virtual environment (recommended):

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download and install Ollama from:

https://ollama.com

Download the required local models:

```bash
ollama pull llama3
ollama pull phi3
ollama pull gemma2
```

Verify installation:

```bash
ollama list
```

---

## Running the Project

Run the main pipeline:

```bash
python main.py
```

Launch the dashboard:

```bash
streamlit run src/dashboard.py
```

---

## Pipeline Workflow

1. Load the UN Human Development Report PDF.
2. Extract raw text using PyMuPDF.
3. Clean and segment the extracted text.
4. Generate an overall summary.
5. Produce summaries for each chapter.
6. Extract themes:

   * Education
   * Health
   * Economy
   * Gender
   * Climate
   * Employment
   * Inequality
7. Extract:

   * Key strengths
   * Key challenges
   * Numerical development indicators
8. Evaluate extraction quality using a second local LLM.
9. Generate interactive visualisations.
10. Display results in a Streamlit dashboard.

---

## Dashboard Features

The dashboard includes:

* Overall report summary
* Chapter summaries
* Theme distribution
* Development indicators
* Strengths and challenges
* Time-series trends (where available)
* LLM comparison results
* Evaluation scores

---

## Local LLM Models

| Model   | Purpose                                                 |
| ------- | ------------------------------------------------------- |
| Llama 3 | Information extraction and summarisation                |
| Phi-3   | Evaluation of summaries and extracted data              |
| Gemma 2 | Optional comparison for stability and thematic richness |

---

## Output Files

The pipeline generates:

* Overall summary
* Chapter summaries
* Theme counts
* Strengths
* Challenges
* Structured JSON indicators
* Evaluation scores
* Dashboard visualisations

---

## Future Improvements

* Retrieval-Augmented Generation (RAG)
* Vector database integration
* Automatic table extraction from PDFs
* OCR support for scanned reports
* Comparison across multiple country reports
* Additional dashboard visualisations

---

## References

* United Nations Development Programme (UNDP) Human Development Reports
* Ollama Documentation
* PyMuPDF Documentation
* Plotly Documentation
* Streamlit Documentation

---

