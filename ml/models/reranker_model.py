from typing import List, Dict
from sentence_transformers import CrossEncoder


class RerankerModel:
    def __init__(self, device: str ='cpu'):
        self._model = CrossEncoder('DiTy/cross-encoder-russian-msmarco', max_length=512, device=device)
        print('reranker model is ready!')

    def predict(self, query: str, documents: List[str]) -> Dict[str, float]:
        return {documents[r['corpus_id']]: r['score'] for r in self._model.rank(query, documents)}


