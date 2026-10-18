import requests
import json
import sys
sys.stdout.reconfigure(encoding="utf-8")

class MyAPIClient:
    def __init__(self,api_key):
        #Конструктор моего АПИ клиента, тут формируется сам клиент, его ключ, и адрес, по которому будем отправлять запрос
        self.api_key = api_key
        self.its_url = ("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent")
        
    def build_payload(self,prompt):
        #Формируем JSON запроса
        return {
            "contents": [
                {
                    "role": "user", 
                    "parts":[{"text": prompt}]
                }
            ],
            "generationConfig": {
                "thinkingConfig":{
                    "thinkingLevel": "low"
                    
                }
            }
        }
        
    def send_request(self, payload):
        response = requests.post(
            self.its_url,
            params={"key": self.api_key}, # у метода post два основных параметра - url и сам json, так как работает с ключом апи, добавляем и апи_ключ
            headers={"Content-Type": "application/json"}, # дает серверу понять что объект надо будет парсить именно как json
            json=payload,
            timeout=(10, 120)
        )
        response.raise_for_status()  # бросит HTTPError при ошибках 400 или 500 или все что начинается на 4/5
        return response

    def send_message(self,prompt):
        payload = self.build_payload(prompt)
        response = self.send_request(payload)
        data = response.json()
        try:
            model_response = data["candidates"][0]["content"]["parts"][0]["text"] # в словаре data берем текст из первого кандидата на ответ
        except (KeyError, IndexError):
            raise Exception(f"Не удалось распарсить ответ: {data}")
        
        return model_response
    
    
if __name__ == "__main__":
    import os

    API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6LtPelJloAubZncYsApsTLshwIv5FV02qpOnJEYbW0XJQ")

    client = MyAPIClient(
        api_key=API_KEY,
    )

    answer = client.send_message("Привет! Кто проживает на дне океана?")
    print("Александр:", answer)
    
# Все предложения рассматриваются здесь)
        