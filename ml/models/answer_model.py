from transformers import pipeline


class AnswerModel:
    def __init__(self, device: str = 'cpu'):
        self._model = pipeline(task='question-answering', model='timpal0l/mdeberta-v3-base-squad2', device=device)
        print('answer model is ready!')

    def predict(self, question: str, context: str):
        return self._model(question=question, context=context)['answer']