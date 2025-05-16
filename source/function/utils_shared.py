import yaml
from langchain_core.prompts import ChatPromptTemplate
from source.core.config import Settings
import os
import json
import re
from sentence_transformers import util
from source.model.embedding_model import Sentences_Transformer_Embedding
def load_prompt_from_yaml(settings: Settings, section: str) -> ChatPromptTemplate:
    # Tạo đường dẫn tuyệt đối đến file YAML
    current_dir = os.path.dirname(__file__)
    yaml_path = os.path.join(current_dir, '..', 'core', settings.YAML_PATH)
    yaml_path = os.path.abspath(yaml_path)
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)

    messages = yaml_data['prompts'][section]['messages']
    return ChatPromptTemplate.from_messages(
        [(msg['role'], msg['content']) for msg in messages]
    )
def load_information_from_json(settings:Settings,model_embedding:Sentences_Transformer_Embedding):
    current_dir=os.path.dirname(__file__)
    json_path=os.path.join(current_dir,'..','core',settings.PATH_INFOR)
    json_path=os.path.abspath(json_path)
    with open(json_path,'r',encoding='utf-8') as f:
        data=json.load(f)
    corpus=[item['content'] for item in data]
    corpus_embedding=model_embedding.embeddings_bkai.embed_documents(corpus)
    return corpus,corpus_embedding
def search_from_json(corpus_embedding,corpus,query,model_embedding:Sentences_Transformer_Embedding):
    query_embedding=model_embedding.embeddings_bkai.embed_query(query)
    cos_scores = util.cos_sim(query_embedding, corpus_embedding)[0]
    top_results = cos_scores.argsort(descending=True)[:5]
    results=[]
    for idx in top_results:
        results.append(corpus[idx])
    return "\n".join(results)

def clean_generated_queries(queries):
        cleaned_queries = []
        for query in queries:
            if '```' in query:
                continue
            if len(query.split()) < 5:
                continue
            cleaned_queries.append(query)
        return cleaned_queries
def extract_json_dict(text):
    # Dùng regex để trích nội dung bên trong ```json ... ```
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    else:
        raise ValueError("Không tìm thấy nội dung JSON hợp lệ.")