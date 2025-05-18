from typing import List,Tuple
from source.model.rerank_model import Cohere
from cohere import ClientV2
class Rerank_Utils():
    def __init__(self,model_rerank:Cohere):
         self.model_rerank=model_rerank
    def reciprocal_rank_fusion(self,documents_nested, k=60):
        document_scores = {}  
        try:
            for query_idx, result_list in enumerate(documents_nested):
                for rank, (doc, _) in enumerate(result_list):
                    doc_key = doc.page_content
                    doc_metadata=doc.metadata
                    rrf_score = 1 / (k + rank + 1)
                    if doc_key not in document_scores:
                        document_scores[doc_key] = {
                            "score": 0,
                            "doc_metadata":doc_metadata,
                            "count": 0  
                        }
                    document_scores[doc_key]["score"] += rrf_score
                    document_scores[doc_key]["count"] += 1
            reranked_docs = sorted(document_scores.items(), key=lambda x: x[1]["score"], reverse=True)
            return reranked_docs[:50]  
        except Exception as e:
            print(f"Lỗi khi tính RRF: {e}")
            return []
    def rerank_documents(self,query,documents) -> List[Tuple[str, float]]:
            doc_contents = [(doc).replace("_"," ") for doc,_ in documents]
            try:
                co = ClientV2(self.model_rerank.key_manager.get_next_key())
                response = co.rerank(
                    model=self.model_rerank.model_cohere,
                    query=query,
                    documents=doc_contents,
                    top_n=5,
                )
                reranked_results = response.results
                print(reranked_results)
                ranked_documents = [documents[res.index] for res in reranked_results]
            except Exception as e:
                print(f"An error occurred: {e}")
            return ranked_documents  