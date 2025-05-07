from fastapi import APIRouter,HTTPException
from source.function.utils_result import RAG
from source.search.utils_search import Qdrant_Utils
from source.rerank.utils_rerank import Rerank_Utils  
from source.model.embedding_model import Sentences_Transformer_Embedding
from source.model.extract_model import Bert_Extract
from source.model.generate_model import Gemini
from source.model.rerank_model import Cohere
from source.data.vectordb.qdrant import Qdrant_Vector
from source.core.config import Settings
from source.generate.generate import Gemini_Generate
from source.extract.utils_extract import Extract_Information
from source.schema.chatbot_querry import ChatbotQuery
setting=Settings()
gemini=Gemini(setting)
cohere=Cohere(setting)
bert=Bert_Extract(setting)
sentences_transformer_embedding=Sentences_Transformer_Embedding(setting)
qdrant=Qdrant_Vector(setting,sentences_transformer_embedding)
router = APIRouter()
rerank_Utils=Rerank_Utils(cohere)
extract_Utils= Extract_Information(bert)
generate_Utils=Gemini_Generate(gemini,setting)
qdrant_Utils=Qdrant_Utils(qdrant, generate_Utils)
rag=RAG(generate_Utils,extract_Utils,qdrant_Utils,rerank_Utils,setting,sentences_transformer_embedding)
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
