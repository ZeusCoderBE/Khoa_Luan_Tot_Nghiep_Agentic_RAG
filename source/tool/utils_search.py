import json 
from source.function.utils_shared import clean_code_fence_safe,parse_raw_json
from source.extract.utils_extract import Extract_Information
from source.core.config import Settings
from source.generate.generate import Gemini_Generate
from source.tool.google_search import GoogleSearchTool
from source.core.config import Settings

class Utils_Search_Tools:
    def __init__(self,setting:Settings,gemini_func:Gemini_Generate,extract_func:Extract_Information,google_search_tools:GoogleSearchTool):
        self.setting=setting
        self.gemini_func=gemini_func
        self.extract_func=extract_func
        self.google_search_tools=google_search_tools
    
    def Search_Docs_From_Tools(self,query):
        try:
            lst_links=self.google_search_tools.search(query)
            lst_docs=self.google_search_tools.extract_texts_from_links(lst_links)
            lst_reduce_docs=self.extract_func.predict(lst_docs,query)
            result_final=self.gemini_func.generate_response(query,lst_reduce_docs)
            answer_result=clean_code_fence_safe(result_final)
            answer_result=parse_raw_json(answer_result)
            relevant_links = [lst_links[i] for i in answer_result['key']]
            
            # Kiểm tra nếu không có relevant links
            if not relevant_links or len(relevant_links) == 0:
                error_message = "Xin lỗi, tôi không thể đưa ra kết quả cuối cùng được. Tuy nhiên, bạn có thể tham khảo thông qua danh sách các tài liệu mà tôi đã tìm kiếm."
                return error_message, lst_links
            
            return answer_result['answer'], relevant_links
        except Exception as e:
            print("Đang bị lỗi"+e)
            error_message = "Xin lỗi, tôi không thể đưa ra kết quả cuối cùng được. Tuy nhiên, bạn có thể tham khảo thông qua danh sách các tài liệu mà tôi đã tìm kiếm."
            return error_message, lst_links