from sentence_transformers import CrossEncoder

class RerankModelFinetune:
    def __init__(self, model_repo="hghaan/rerank_model", device="cuda"):
        self.model = CrossEncoder(model_repo, trust_remote_code=True, device=device)

    def predict(self, pairs):
        return self.model.predict(pairs) 