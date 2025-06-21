

# 📄 **Technical Report**

## Legal Advisory Chatbot System: Vietnamese Law QA powered by LLMs & Agentic RAG

**Author**: Đặng Nguyễn Quang Huy

**Supervised by**: ThS. Trần Trọng Bình

**Institution**: Trường Đại học Sư phạm Kỹ thuật TP.HCM

**Department**: Khoa Công nghệ Thông tin

**Major**: Kỹ thuật Dữ liệu

---

## 1. Executive Summary

This report presents the development and evaluation of a **Legal Advisory Chatbot System** aimed at providing accurate and context-aware responses to Vietnamese legal questions. The system leverages cutting-edge techniques including **LLMs**, **embedding-based vector retrieval**, **fine-tuned reranking**, and an **Agentic RAG pipeline**. The project represents a shift from traditional RAG architectures to more dynamic, modular, and agent-driven retrieval-generation frameworks, optimized for legal domain complexity.

---

## 2. Motivation & Problem Statement

Vietnamese legal texts are often complex, hierarchical, and filled with context-specific terminology and exceptions. Accessing relevant legal knowledge is challenging for non-experts and time-consuming for professionals.

The core issues addressed include:

* Legal information is **scattered** and often **poorly indexed**.
* Existing LLMs face **hallucination** risks without grounding in verified legal data.
* Naive RAG pipelines **lack adaptability** in multi-turn, multi-agent reasoning tasks.

---

## 3. System Architecture Overview

### 3.1 Core Components

* **Document Source**: Official Vietnamese legal websites.
* **Vector DB**: Qdrant, used to store and retrieve dense document embeddings.
* **LLM Backbone**: Google BERT fine-tuned for Vietnamese law.
* **Embedding Model**: Custom Sentence Transformers (`quanghuy123/LEGAL_EMBEDDING`).
* **Reranker**: Cross-Encoder with Reciprocal Rank Fusion (RRF) strategy.
* **RAG Architecture**: Agentic RAG integrating:

  * `Query Router`
  * `Query Rewriter`
  * `Entity Extractor`
  * `Search + Rerank`
  * Gemini-powered LLM inference module.

### 3.2 Technical Stack

| Layer            | Technology/Tool                 |
| ---------------- | ------------------------------- |
| Language Model   | HuggingFace Transformers        |
| Embedding Engine | Sentence-BERT + Matryoshka Loss |
| Reranker         | Cross-Encoder BERT + RRF        |
| Infrastructure   | FastAPI + Docker + LangChain    |
| Deployment       | Containerized microservices     |
| Storage          | Qdrant vector database          |

---

## 4. Methodology & Model Optimization

### 4.1 Embedding Optimization

* Trained using **MultipleNegativesRankingLoss**
* Applied **Matryoshka Representation Learning** for multi-resolution search.
* Evaluated via **Recall\@K**, **MAP**, **MRR**, and **NDCG** metrics.

### 4.2 Reranking

* Fine-tuned Cross-Encoder with labeled question-document pairs.
* Integrated **RRF** to balance multiple retrieval scores.

### 4.3 Agentic RAG Pipeline

* Dynamically routes queries to appropriate modules.
* Enables **multi-hop reasoning**, **context rewriting**, and **document grounding**.
* Achieves significant improvements over static RAG by incorporating feedback and tool usage capabilities.

---

## 5. Experimentation & Results

| Module         | Technique                     | Evaluation Score    |
| -------------- | ----------------------------- | ------------------- |
| BERT Extractor | Full & LoRA Fine-Tuning       | F1: 0.93, EM: 0.91  |
| Embedding      | SBERT + Matryoshka            | NDCG\@10: 0.82      |
| Reranker       | Cross-Encoder + RRF           | MRR\@10: 0.87       |
| Full System    | Agentic RAG (w/ Gemini Agent) | Query Accuracy: 92% |

> The system was evaluated on both internal UTE\_LAW and Zalo-based legal QA datasets (2021). Benchmarks confirm the superiority of Agentic RAG over Naive/Traditional RAG in both reasoning depth and retrieval accuracy.

---

## 6. Deployment

* **API Layer**: FastAPI for lightweight REST services.
* **Containerization**: Docker enables consistent environment across stages.
* **Scalability**: Modular services allow easy cloud/on-premise deployment.
* **User Interface**: Clean frontend for legal professionals and public access.

---

## 7. Contributions & Innovation

* First public Vietnamese **Agentic RAG** system tailored to law.
* Custom fine-tuned **embedding** and **reranking** models for legal domain.
* Modular design allowing **low-cost**, **scalable**, and **transparent** deployment.

---

## 8. Limitations

* Dataset limitations due to legal data sparsity in Vietnamese.
* RAG agents still require performance tuning for ambiguous multi-turn dialogue.
* Current Gemini integration operates via API; full offline LLM support pending.

---

## 9. Future Work

* Expand to **multilingual** and **multi-jurisdictional** legal corpora.
* Integrate **Legal Ontologies** for better reasoning support.
* Enable **self-learning retrievers** through user feedback.
* Add **zero-shot summarization** & **citation tracing** for trustworthiness.

---

## 10. Conclusion

This work demonstrates the feasibility and effectiveness of **Agentic RAG** systems applied to Vietnamese law. By combining transformer-based NLP models, optimized embedding/reranking techniques, and multi-agent architectures, we deliver a **robust, scalable, and user-aligned** legal advisory chatbot system. This research not only advances AI in Vietnamese legal NLP but also lays the groundwork for broader intelligent public service systems.

---


