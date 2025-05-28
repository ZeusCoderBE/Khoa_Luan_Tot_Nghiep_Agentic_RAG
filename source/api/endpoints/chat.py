from fastapi import APIRouter,HTTPException
from source.function.utils_result import RAG
from source.search.utils_search import Qdrant_Utils
from source.rerank.utils_rerank import Rerank_Utils  
from source.model.embedding_model import Sentences_Transformer_Embedding
from source.model.extract_model import Bert_Extract
from source.model.generate_model import Gemini
from source.model.rerank_model import Cohere
from source.model.rerank_model_finetune import RerankModelFinetune
from source.data.vectordb.qdrant import Qdrant_Vector
from source.core.config import Settings
from source.generate.generate import Gemini_Generate
from source.extract.utils_extract import Extract_Information
from source.schema.chatbot_querry import ChatbotQuery
from source.tool.utils_search import Utils_Search_Tools
from source.tool.google_search import GoogleSearchTool

setting=Settings()
gemini=Gemini(setting)
cohere=Cohere(setting)
bert=Bert_Extract(setting)
sentences_transformer_embedding=Sentences_Transformer_Embedding(setting)
qdrant=Qdrant_Vector(setting,sentences_transformer_embedding)
router = APIRouter()
model_finetune = RerankModelFinetune()
rerank_Utils=Rerank_Utils(cohere, model_finetune)
extract_Utils= Extract_Information(bert)
generate_Utils=Gemini_Generate(gemini,setting)
qdrant_Utils=Qdrant_Utils(qdrant, generate_Utils)
rag=RAG(generate_Utils,extract_Utils,qdrant_Utils,rerank_Utils,setting,sentences_transformer_embedding)

# Khởi tạo các tools cần thiết cho web search
google_search_tools = GoogleSearchTool(setting)
search_tools = Utils_Search_Tools(setting, generate_Utils, extract_Utils, google_search_tools)

@router.post("/chatbot-with-search-web")
def chatbot_with_search_web(query: ChatbotQuery):
    try:
        user_input = query.query
        answer, relevant_links = search_tools.Search_Docs_From_Tools(user_input)
        return {
            "answer": answer,
            "lst_Relevant_Documents": relevant_links
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.post("/chatbot-with-gemini")
def chatbot_with_gemini(query: ChatbotQuery):
    try:
        user_input = query.query
        article_Document_Results, lst_Article_Quote = rag.get_Article_Content_Results(user_input)
        print(user_input)
        return {
            "answer": article_Document_Results,
            "lst_Relevant_Documents": lst_Article_Quote
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
