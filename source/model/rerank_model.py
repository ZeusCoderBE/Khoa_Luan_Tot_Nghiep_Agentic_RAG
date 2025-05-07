from source.model.reset_apikey import APIKeyManager
from source.core.config import Settings
class Cohere():
    def __init__(self,setting:Settings) :
        self.key_manager=APIKeyManager(setting.API_RERANKER)
        self.model_cohere=setting.MODEL_RERANK