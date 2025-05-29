import sys
project_path = r"D:/DaiHoc/machinelearning/TLCN/DoAnTotNghiep_chat_bot/"
sys.path.append(project_path)
import json 
from source.function.utils_shared import clean_code_fence_safe,fix_json_string
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
            answer_result=fix_json_string(answer_result)
            answer_result = json.loads(answer_result)
            relevant_links = [lst_links[i] for i in answer_result['key']]
            return answer_result['answer'], relevant_links
        except Exception as e :
            print("Đang bị lỗi"+e)
            return "", []