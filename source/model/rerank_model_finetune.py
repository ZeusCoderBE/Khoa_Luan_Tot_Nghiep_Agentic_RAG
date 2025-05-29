from sentence_transformers import CrossEncoder
import torch
from source.core.config import Settings
class RerankModelFinetune:
    def __init__(self,setting:Settings ):
        self.model = CrossEncoder(setting.RERANK, trust_remote_code=True, device='cuda' if torch.cuda.is_available() else 'cpu')