from source.core.config import Settings
from source.model.embedding_model import Sentences_Transformer_Embedding
from langchain_qdrant import Qdrant
class Qdrant_Vector():
    def __init__(self,setting:Settings,embedding:Sentences_Transformer_Embedding):
        self.setting=setting
        self.embedding=embedding
    def Open_Qdrant(self):
        open_collection = Qdrant.from_existing_collection(
            embedding = self.embedding.embeddings_bkai,
            url =self.setting.URL_QDRANT_LOCAL,
            collection_name =self.setting.EXIST_COLLECTION_NAME,
            metadata_payload_key=self.setting.metadata_payload_key
        )
        return open_collection


