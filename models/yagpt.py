import requests
import json


class YaGPT:
    def __init__(self, catalog_id: str, api_key: str):
        if not isinstance(catalog_id, str) or not catalog_id:
            raise ValueError("catalog_id должен быть непустой строкой.")
        if not isinstance(api_key, str) or not api_key:
            raise ValueError("api_key должен быть непустой строкой.")

        self._catalog_id = catalog_id
        self._api_key = api_key
        self._url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self._api_key}"
        }
        self._context = 'Привет!'

    def set_context(self, context: str) -> None:
        if not isinstance(context, str) or not context:
            raise ValueError("context должен быть непустой строкой.")
        self._context = context

    def get_GPT_answer(self, query: str) -> str:
        if not isinstance(query, str) or not query:
            raise ValueError("query должен быть непустой строкой.")

        prompt = {
            "modelUri": f"gpt://{self._catalog_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 2000  # исправлено на число
            },
            "messages": [
                {
                    "role": "system",
                    "text": self._context
                },
                {
                    "role": "user",
                    "text": query
                },
            ]
        }

        response = requests.post(self._url, headers=self._headers, json=prompt)
        if response.status_code != 200:
            raise Exception(f"Ошибка API: {response.status_code} - {response.text}")

        result = response.json()  # Лучше использовать json() для получения данных
        role = result['result']['alternatives'][0]['message']['role']
        text = result['result']['alternatives'][0]['message']['text']

        return text


# yagpt = YaGPT(catalog_id='b1gaa0i749eqe9ogone8', api_key='AQVN2yvuhm5p2BeZDjf-wj-k0qC1sHRVoZUYM_r3')
# yagpt.set_context(context='Ты инвестор c многолетним стажем')
# answer = yagpt.get_GPT_answer(query="Ответь только да или нет, без дополнительного текста, инвестирует ли этот инвестор в it проекты на основе этого описания: Приоритетными являются уже созданные компании, существующие на рынке более года с потребностью привлечения средств для дальнейшего роста и развития. Также интересуют проекты, создаваемые руководителями компаний, желающих перейти из категории наемных сотрудников в собственный бизнес с долевым участием. Рассматриваем проекты с объемом привлечения средств от 1 500 000 до 30 000 000 рублей.")
#
# print(answer)
# print(role, text)
