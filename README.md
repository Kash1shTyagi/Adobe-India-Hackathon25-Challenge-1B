# approach_explanation.md

## 🔍 Problem Overview

The task is to extract the most relevant answers from a given set of PDFs based on natural language questions provided in a structured input JSON file. This is a classic **information retrieval** problem where the solution must parse unstructured documents, understand context semantically, and retrieve the best-matching answers efficiently and accurately.

## 🧠 Methodology

Our solution is broken down into 4 key stages:

### 1. 📄 PDF Parsing using `pdfplumber`

We use `pdfplumber` for robust and accurate text extraction from PDFs. Unlike basic text extraction libraries, `pdfplumber` handles layout, whitespace, and line breaks effectively, allowing us to extract a coherent stream of text. We iterate through all pages, clean the text, and split it into semantically meaningful **paragraphs**.

Each paragraph is considered a potential answer candidate.

### 2. 🔗 Semantic Embedding using `sentence-transformers`

We leverage the `all-MiniLM-L6-v2` model from the [sentence-transformers](https://www.sbert.net/) library to encode both questions and paragraphs into high-dimensional semantic vectors. This model is lightweight and efficient while maintaining good accuracy for sentence-level similarity tasks.

- Each **paragraph** is embedded once and stored.
- Each **question** from the input JSON is also embedded.

By doing this, we move from raw text comparison to **semantic similarity**, which allows us to match based on meaning rather than keywords.

### 3. 📊 Ranking with Cosine Similarity

Once embeddings are available, we compute the **cosine similarity** between each question vector and every paragraph vector from the PDFs.

- The paragraph with the **highest similarity score** is selected as the most relevant answer for that question.
- We store the top result (and optionally top-k results for inspection or confidence analysis).

This process ensures that even if the paragraph doesn’t have the exact words from the question, it can still be chosen if it's semantically aligned.

### 4. 📦 Output JSON Generation

Finally, we structure the output into the required format:
- Each question ID is mapped to the **best-matching paragraph** and its similarity **confidence score**.
- The output is written to a new JSON file as specified by the command-line arguments.

## 🧪 Evaluation

This pipeline can be evaluated on:
- **Accuracy** of matched paragraphs (manual or labeled evaluation).
- **Confidence scores** to understand model certainty.
- **Latency** and efficiency, thanks to batching and fast transformer models.

## ✅ Why This Approach?

- **Simple & Scalable**: Easy to extend with new models or rerankers.
- **Modern NLP**: Utilizes SOTA sentence embeddings for semantic understanding.
- **Maintainable**: Clean module separation for PDF parsing, embedding, and ranking.
