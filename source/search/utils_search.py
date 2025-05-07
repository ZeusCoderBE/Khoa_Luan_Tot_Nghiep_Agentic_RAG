from qdrant_client.models import Filter, FieldCondition, MatchValue
from pyvi import ViTokenizer
from source.generate.generate import Gemini_Generate
from source.data.vectordb.qdrant import Qdrant_Vector
class Qdrant_Utils():
    def __init__(self,qdrant:Qdrant_Vector,gemini_util:Gemini_Generate):
        self.qdrant=qdrant
        self.gemini=gemini_util
    # def create_should_filter(self,user_keywords, metadata_fields = metadata_Fields_To_Filter):
    #     should_conditions = []
        
    #     for keyword in user_keywords:
    #         for field in metadata_fields:
    #             should_conditions.append(FieldCondition(
    #                 key=field, 
    #                 match=MatchValue(value=keyword)
    #             ))
        
    #     return Filter(
    #         should=should_conditions
    #     )

    def search_documents(self,query,top_k = 10):
        connection=self.qdrant.Open_Qdrant()
        search_results = connection.similarity_search_with_score(
            query=query,
            k=top_k,
            timeout = 300
        )
        
        return search_results

    def search_With_Similarity_Queries(self,user_query: str):
        queries_processed=[]
        queries = self.gemini.generate_query(user_query)
        for query in queries:
            queries_processed.append(ViTokenizer.tokenize(query))
        query_results = []
        for query in queries_processed:
            search_results =self.search_documents(query)
            query_results.extend(search_results)  

        unique_results = {}
        for doc, score in query_results:
            if doc.page_content in unique_results:
                if score > unique_results[doc.page_content][1]:
                    unique_results[doc.page_content] = (doc, score)
            else:
                unique_results[doc.page_content] = (doc, score)
        
        return list(unique_results.values())

    # def extract_Unique_Metadata(self,top_results):
    #     metadata_list = []
    #     metadata_dict_set = set() 

    #     for result in top_results:
    #         doc = result[0]  
    #         metadata = {
    #             "stt": doc.metadata.get('stt'),
    #             "loai_van_ban": doc.metadata.get('loai_van_ban'),
    #             "noi_ban_hanh": doc.metadata.get('noi_ban_hanh'),
    #             "so_hieu": doc.metadata.get('so_hieu'),
    #             "linhvuc_nganh": doc.metadata.get('linhvuc_nganh'),
    #             "ngay_ban_hanh": doc.metadata.get('ngay_ban_hanh'),
    #             "ngay_hieu_luc": doc.metadata.get('ngay_hieu_luc'),
    #             "chu_de": doc.metadata.get('chu_de'),
    #             "Chapter": doc.metadata.get('Chapter'),
    #             "Section": doc.metadata.get('Section'),
    #             "Mini-Section": doc.metadata.get('Mini-Section'),
    #             "Article": doc.metadata.get('Article'),
    #         }

    #         filtered_metadata = {key: value for key, value in metadata.items() if value is not None}
    #         metadata_tuple = tuple(filtered_metadata.items())
    #         metadata_dict_set.add(metadata_tuple)

    #     for metadata_tuple in metadata_dict_set:
    #         metadata_dict = dict(metadata_tuple)
    #         metadata_list.append(metadata_dict)

    #     return metadata_list