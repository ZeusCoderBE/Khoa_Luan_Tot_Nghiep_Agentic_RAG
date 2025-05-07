from source.rerank.utils_rerank import Rerank_Utils
from source.search.utils_search import Qdrant_Utils
from source.extract.utils_extract import Extract_Information
from source.generate.generate import Gemini_Generate
from source.core.config import Settings
from source.function.utils_shared import load_information_from_json,search_from_json
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
        if self.generate.classify_query(user_Query)==0:
                return self.generate.greeting_query(user_Query),""
        elif self.generate.classify_query(user_Query)==1:
                context=search_from_json(self.corpus_embedding,self.corpus,user_Query,self.model_embedding)
                return self.generate.generate_information(user_Query,context),""
        elif self.generate.classify_query(user_Query)==3:
                return self.generate.invalid_query(user_Query),""
        elif self.generate.classify_query(user_Query)==2:
            article_documents = self.qdrant_utils.search_With_Similarity_Queries(user_Query)
            print(f"Số document retrival được {len(article_documents)}")
            rerank_article_documents = self.rerank_utils.rerank_documents(user_Query,article_documents)
            article_Content_Resuls = []
            lst_Article_Quote = []
            print(len(rerank_article_documents))
            for doc, _ in rerank_article_documents:
                article_Content_Resuls.append((doc.page_content).replace("_"," "))
                loai_van_ban = doc.metadata.get("Loai-Van-Ban", "N/A")
                noi_ban_hanh = doc.metadata.get("Noi-Ban-Hanh", "N/A")
                so_hieu = doc.metadata.get("So-Hieu", "N/A")
                linhvuc_nganh = doc.metadata.get("LinhVuc-Nganh", "N/A")
                ngay_ban_hanh = doc.metadata.get("Ngay-Ban-Hanh", "N/A")
                chu_de = doc.metadata.get("Chu-De", "N/A")
                chapter = doc.metadata.get("Chapter", "N/A")
                section = doc.metadata.get("Section", "N/A")
                mini_section = doc.metadata.get("Mini-Section", "N/A")
                article = doc.metadata.get("Article","N/A")
                formatted_quote = f"""\
                                Loại văn bản: {loai_van_ban}
                                Nơi ban hành: {noi_ban_hanh}
                                Số hiệu: {so_hieu}
                                Lĩnh vực - ngành: {linhvuc_nganh}
                                Ngày ban hành: {ngay_ban_hanh}
                                Chủ đề: {chu_de}
                                Chương: {chapter}
                                Mục: {section}
                                Tiểu mục: {mini_section}
                                Điều: {article}
                                <=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>
                                {
                                    
                                    doc.page_content.replace("_"," ")
                                }
                                """
                lst_Article_Quote.append(formatted_quote)
            document_reduce=self.extract_utils.predict(article_Content_Resuls,user_Query)
            result_gemini=self.generate.generate_response(user_Query,document_reduce)
            return result_gemini, lst_Article_Quote