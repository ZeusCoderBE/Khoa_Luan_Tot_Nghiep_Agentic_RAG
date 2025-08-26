![AGENTIC_RAG1-Detail_Workflow drawio](https://github.com/user-attachments/assets/92ad2bf4-9ce9-4cd0-87d6-6a3d3933f479)

Here is the Demo video: [Legal Retrieval System with Multi Agent System: Vietnamese Law QA powered by LLMs & Agentic RAG](https://youtu.be/v9iN9ebrfx8?si=0QFnMgT6_434TMRK)

| **Purpose**                      | **Dataset Link**                                                                                                                                                                                                                |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Embedding Training**           | [embedding-data-law (Kaggle)](https://www.kaggle.com/datasets/huymeme123/data-embd)|
| **Extractor Fine-Tuning**        | [extract-data-law (Kaggle)](https://www.kaggle.com/datasets/huymeme123/data-bert-extract)|
| **Supervised Legal QA (Zalo)**   | [vinli-zalo-supervised (Kaggle)](https://www.kaggle.com/datasets/huynhgiahan/vinli-zalo-supervised)|
|  **Data Qdrant**                 | [GOOGLE DRIVER](https://drive.google.com/drive/folders/1ujLaNsVjbbLXZx3VIWH_vuMF2IeZsWiI?usp=sharing)


# 📄 **Technical Report**

## Legal Retrieval System with Multi Agent System: Vietnamese Law QA powered by LLMs & Agentic RAG

**Author**: We would like to express our sincere gratitude to the team members who contributed their efforts and expertise to this project:

  1. Đặng Nguyễn Quang Huy - [ZeusCoderBE](https://github.com/ZeusCoderBE)
  2. Nguyễn Trọng Dũng - [NgTrDung](https://github.com/NgTrDung)

---

## 1. Executive Summary

This report presents the development and evaluation of a **Legal Retrieval System with Multi Agent System** aimed at providing accurate and context-aware responses to Vietnamese legal questions. The system leverages cutting-edge techniques including **LLMs**, **embedding-based vector retrieval**, **fine-tuned reranking**, and an **Agentic RAG pipeline**. The project represents a shift from traditional RAG architectures to more dynamic, modular, and agent-driven retrieval-generation frameworks, optimized for legal domain complexity.


![image](https://github.com/user-attachments/assets/05e843fe-0623-4085-b641-e4635fcea3c0)


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
* **Embedding Model**: Custom Sentence Transformers (`huyydangg/DEk21_hcmute_embedding`).
* **Reranker**: Cross-Encoder with Reciprocal Rank Fusion (RRF) strategy (`hghaan/rerank_model`).
* **RAG Architecture**: Agentic RAG integrating:

  * `Query Router`
  * `Query Rewriter`
  * `Entity Extractor`
  * `Search + Rerank`
  * `Search Tool`
  * `Gemini-powered LLM inference module`.

![AGENTIC_RAG1-Detail_Workflow](https://github.com/user-attachments/assets/69daefa3-937a-4f94-9b6f-9b888051c252)


### 3.2 Technical Stack


| Layer                | Technology / Tool                           | Description                                                                                                  |
| -------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Open Model**       | 🤗 HuggingFace Transformers                 | Foundation for models like BERT (extractor), Sentence-Transformers (embedding), and Cross-Encoder (reranker) |
| **Embedding** | 🧠 Sentence-BERT + Matryoshka Loss          | Generates semantic vector representations for queries and legal passages                                     |
| **Reranker**         | 🎯 Cross-Encoder BERT + RRF                 | Re-evaluates the relevance between the query and retrieved passages                                          |
| **LLM Reasoning**    | 🔮 Gemini API (or local LLM)                | Aggregates context and generates the final legal answer with citations                                       |
| **Agent Modules**    | 🤖 Query Router, Rewriter, Entity Extractor | Directs the question, rewrites queries, extracts entities (laws, dates, etc.)                                |
| **Search**    | 🔍 Qdrant + Optional External Tools         | Retrieves vectors and optionally searches external sources (Google, vbpl.gov.vn)                             |
| **Extractor**        | 🧾 Extract Information              |         Extract legal answer spans and helps reduce LLM context and API cost      |
| **Infrastructure**   | ⚙️ FastAPI + Docker + LangChain             | Lightweight backend API, fast deployment, and orchestration of the LLM/RAG pipeline                          |
| **Deployment**       | ☁️ Containerized microservices              | Easily scalable and deployable as independent services or clusters                                           |
| **Storage**          | 🧮 Qdrant vector database                   | Stores vectors and metadata, optimized for cosine similarity search                                          |                                    |
---

## 4. Methodology & Model Optimization

### 4.1 Embedding Optimization

* Trained using **MultipleNegativesRankingLoss**
* Applied **Matryoshka Representation Learning** for multi-resolution search.
* Evaluated via **Recall\@K**, **MAP**, **MRR**, and **NDCG** metrics.

### 4.2 Reranking

* Fine-tuned Cross-Encoder with labeled question-document pairs.
* Integrated **RRF** to balance multiple retrieval scores.

### 4.3. Extractor

* Fine-tuned BERT to extract legal answer spans
* Helps reduce LLM context and API cost

### 4.4 Agentic RAG Pipeline

* Dynamically routes queries to appropriate modules.
* Enables **multi-hop reasoning**, **context rewriting**, and **document grounding**.
* Achieves significant improvements over static RAG by incorporating feedback and tool usage capabilities.

---

## 5. Experimentation & Results

| Module         | Technique                     | Evaluation Score    |
| -------------- | ----------------------------- | ------------------- |
| BERT Extractor | Full & LoRA Fine-Tuning       | F1: 0.93, EM: 0.91  |
| Embedding      | SBERT + Matryoshka            | NDCG\@10: 0.92      |
| Reranker       | Cross-Encoder + RRF           | MRR\@10: 0.87       |
| Full System    | Agentic RAG (w/ Gemini Agent) | Query Accuracy: 90% |

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


