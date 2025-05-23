from sentence_transformers import CrossEncoder

def rerank_model(query, documents):
    if len(documents) > 50:
        raise ValueError("Số lượng documents không được vượt quá 50.")

    model_repo = "hghaan/rerank_model"
    model = CrossEncoder(model_repo, trust_remote_code=True)

    pairs = [(query, doc) for doc in documents]
    scores = model.predict(pairs)
    ranked = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)

    return ranked[:5]