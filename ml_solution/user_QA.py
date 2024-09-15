from models import AnswerModel, RerankerModel
from typing import List

# Загружаем модель для получения ответов
answer_model = AnswerModel()

# Загружаем модель для ранжировки вариантов ответов (наиболее подходящий - ближе к началу)
reranker_model = RerankerModel()


# Заливаем все возможные ответы в спискок
answers = []
with open('answers.txt') as file:
    for answer in file.readlines():
        answers.append(answer)


# Хитрая штука для получения 10 ответов на вопрос пользователя
def get_answer(question: str, documents: List[str]):
    text_ranks = reranker_model.predict(query=question, documents=documents)
    variants = list(set([answer_model.predict(question=question, context=tr) for tr in list(text_ranks.keys())[:10]]))
    text_ranks = reranker_model.predict(query=question, documents=variants)
    return list(text_ranks.keys())[0]


# Вопрос и ответ на него
print(get_answer(question="О чем ФЗ-44?", documents=answers))

