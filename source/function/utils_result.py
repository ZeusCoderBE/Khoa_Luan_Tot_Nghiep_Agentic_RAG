from source.rerank.utils_rerank import Rerank_Utils
from source.search.utils_search import Qdrant_Utils
from source.extract.utils_extract import Extract_Information
from source.generate.generate import Gemini_Generate
from source.core.config import Settings
from source.function.utils_shared import load_information_from_json,search_from_json,clean_code_fence_safe,fix_json_string
import json
from source.model.embedding_model import Sentences_Transformer_Embedding
class RAG():
    def __init__(self,gemini_utils:Gemini_Generate,bert_utils: Extract_Information,qdrant_utils:Qdrant_Utils,rerank_utils:Rerank_Utils,setting:Settings,model_embedding:Sentences_Transformer_Embedding):
         self.qdrant_utils=qdrant_utils
         self.rerank_utils=rerank_utils
         self.extract_utils=bert_utils
         self.generate=gemini_utils
         self.model_embedding=model_embedding
         self.corpus,self.corpus_embedding=load_information_from_json(setting,self.model_embedding)
    def get_Article_Content_Results(self,user_Query):
        check=self.generate.classify_query(user_Query)
        if  check==0:
                context=search_from_json(self.corpus_embedding,self.corpus,user_Query,self.model_embedding)
                return self.generate.generate_information(user_Query,context),""
        elif check==2:
                return self.generate.invalid_query(user_Query),""
        elif check==1:
            article_documents = self.qdrant_utils.search_With_Similarity_Queries(user_Query)
            print("Đã thực hiện xong retrival")
            print(f"Số document retrival được {len(article_documents)}")
            rrf_result_docs=self.rerank_utils.reciprocal_rank_fusion(article_documents)
            print(f"Số document khi xoá trùng {len(rrf_result_docs)}")
            rerank_article_documents = self.rerank_utils.rerank_documents(user_Query,rrf_result_docs) # .rerank_documents_finetune nếu dùng model 5tune
            print(f"Số document sau khi qua rerank: {len(rerank_article_documents)}")
            lst_Article_Quote = []
            article_Content_Resuls=[]
            try :
                for doc, _ in rerank_article_documents:
                    article_Content_Resuls.append(doc.replace("_"," "))
                document_reduce=self.extract_utils.predict(article_Content_Resuls,user_Query)
                result_gemini=self.generate.generate_response(user_Query,document_reduce)
                answer_result= clean_code_fence_safe(result_gemini)
                answer_result= fix_json_string(answer_result)
                answer_result= json.loads(answer_result)
                selected_keys = answer_result["key"]
                answer_result = answer_result['answer']
                if selected_keys :
                    selected_documents = [rerank_article_documents[i] for i in selected_keys]
                    lst_Article_Quote = [
                        f"""\
                        Tài liệu tham khảo: {i+1}
                        Loại văn bản: {infor['doc_metadata'].get("LoaiVanBan", "")}
                        Nơi ban hành: {infor['doc_metadata'].get("NoiBanHanh", "")}
                        Số hiệu: {infor['doc_metadata'].get("SoHieu", "")}
                        Lĩnh vực - ngành: {infor['doc_metadata'].get("LinhVucNganh", "")}
                        Ngày ban hành: {infor['doc_metadata'].get("NgayBanHanh", "")}
                        Chủ đề: {infor['doc_metadata'].get("ChuDe", "")}
                        Chương: {infor['doc_metadata'].get("Chapter", "")}
                        Mục: {infor['doc_metadata'].get("Section", "")}
                        Tiểu mục: {infor['doc_metadata'].get("MiniSection", "")}
                        Điều: {infor['doc_metadata'].get("Article", "")}
                        <=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>
                        {doc.replace("_", " ").replace(' .', '.').replace(' ,', ',').replace(' !', '!').replace(' ?', '?').replace(' :', ':').replace(' ;', ';')}
                        """ 
                            for i, ((doc, infor), key) in enumerate(zip(selected_documents,selected_keys))
                        ]
                else  :
                     lst_Article_Quote=""
                return answer_result, lst_Article_Quote
            except Exception as e :
                print(e)
                return "", []