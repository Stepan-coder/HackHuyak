from transformers import pipeline
import torch

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


class SummarizeModel:
    def __init__(self, max_length:int=1000, num_beams:int=10, do_sample:bool=True, repetition_penalty:float=10.0):
        self._max_length = max_length
        self._num_beams = num_beams
        self._do_sample = do_sample
        self._repetition_penalty = repetition_penalty
        self._model = T5ForConditionalGeneration.from_pretrained('cointegrated/rut5-base-absum')
        self._tokenizer = T5Tokenizer.from_pretrained('cointegrated/rut5-base-absum')
        print("Ready")

    def summarize(self, context, n_words=None, compression=None, **kwargs):
        if n_words:
            context = '[{}] '.format(n_words) + context
        elif compression:
            context = '[{0:.1g}] '.format(compression) + context
        x = self._tokenizer(context, return_tensors='pt', padding=True).to(self._model.device)
        with torch.inference_mode():
            out = self._model.generate(
                **x,
                max_length=self._max_length, num_beams=self._num_beams,
                do_sample=self._do_sample, repetition_penalty=self._repetition_penalty,
                **kwargs
            )
        return self._tokenizer.decode(out[0], skip_special_tokens=True)


class AnswerModel:
    def __init__(self, device: str = 'cpu'):
        self._model = pipeline(task='question-answering', model='timpal0l/mdeberta-v3-base-squad2', device=device)
        print('answer model is ready!')

    def predict(self, question: str, context: str):
        return self._model(question=question, context=context)['answer']


<<<<<<< Updated upstream
context = """
Юридический адрес: 121087, г. Москва,
ул. Тучковская, д.9, корп. 2;
Телефон: +7 (499) 145-66-60; 
+7 (499) 148-98-24
Адрес электронной почты: upravafp@mos.ru;
ОГРН: 1027730012111
ИНН 7730161028
КПП 773001001
Название банка: ГУ Банка России по ЦФО//УФК по г. Москве г. Москва 
Плательщик: Департамент финансов города Москвы (управа района Филевский парк 
города Москвы л/с 0391112000680228) 
р/с 03221643450000007300
к/с 40102810545370000003
БИК 004525988
Реквизиты счета для перечисления денежных средств в качестве обеспечения исполнения контракта: ГУ Банка России по ЦФО//УФК по г. Москве г. Москва
БИК 004525988   
р/с 03222643450000007300  
к/с 40102810545370000003
"""

# summarize_model = SummarizeModel()
# new_context = summarize_model.summarize(context=context)
#


# print(context)
answer_model = AnswerModel()

answer = answer_model.predict(question='Юридический адрес',
                              context=context)
print(answer)
=======


>>>>>>> Stashed changes
