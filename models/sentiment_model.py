import enum
from transformers import pipeline


class Sentiment(enum.Enum):
    POSITIVE = 1
    NEUTRAL = 0
    NEGATIVE = -1
    DEFOULT = -2


class SentimentModel:
    def __init__(self):
        self._model = pipeline(model="r1char9/rubert-base-cased-russian-sentiment")
        print('sentiment model is ready!')

    def predict(self, text: str) -> Sentiment:
        answer = self._model(text)[0]
        if answer['label'] == 'positive':
            return Sentiment.POSITIVE
        elif answer['label'] == 'neutral':
            return Sentiment.NEUTRAL
        elif answer['label'] == 'negative':
            return Sentiment.NEGATIVE
        else:
            return Sentiment.DEFOULT