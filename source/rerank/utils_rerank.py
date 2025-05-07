from typing import List,Tuple
from source.model.rerank_model import Cohere
from cohere import ClientV2
class Rerank_Utils():
    def __init__(self,model_rerank:Cohere):
         self.model_rerank=model_rerank

    def rerank_documents(self,query,documents) -> List[Tuple[str, float]]:
            ranked_documents = []
            doc_contents = [(doc.page_content).replace("_"," ") for doc, _ in documents]
            try:
                co = ClientV2(self.model_rerank.key_manager.get_next_key())
                response = co.rerank(
                    model=self.model_rerank.model_cohere,
                    query=query.replace("_"," "),
                    documents=doc_contents,
                    top_n=5,
                )
                reranked_results = response.results
                ranked_documents = [documents[res.index] for res in reranked_results]
            except Exception as e:
                print(f"An error occurred: {e}")
            return ranked_documents  