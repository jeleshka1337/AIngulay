from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
import xml.etree.ElementTree as El

#url для запроса
folderId = "b1gpngivlee1eh4et6e8"
apiKey = "AQVNwJP4ui_MQLkK0ztDhhS9PpaH3Q_aDG1DJMyY"
question = "К какому мегафакультету ИТМО принадлежит СУиР? 1. КТиУ 2. Ангуляй 3. ФТМИ 4. 17"
url = f"https://yandex.ru/search/xml?folderid={folderId}&apikey={apiKey}&query={question}"
params = {
    "text": question,
    "lang": "ru",
    "type": "web",
    "limit": 1
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0'
}

try:
    #отправка запроса, парсинг
    response = requests.get(url, params=params, timeout=1)
    response.raise_for_status()
    print("XML ответ:")
    print(response.text)
    print("-" * 50)
    root = El.fromstring(response.text)
    results = root.findall('.//doc')
    
    #
    if results:
        for i, doc in enumerate(results[:3]):
            title = doc.find('title').text if doc.find('title') is not None else 'Нет заголовка'
            url = doc.find('url').text if doc.find('url') is not None else 'Нет URL'
            
            # Ищем тег extended-text в properties
            extended_text = doc.find('.//extended-text')
            extended = extended_text.text if extended_text is not None and extended_text.text else 'Нет расширенного описания'
            
            print("XML ответ:")
            print(response.text)
            print("-" * 50)
            print(f"\nРезультат {i+1}:")
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Extended text: {extended}")
            print("-" * 50)

except requests.exceptions.RequestException as errorType:
    print(f"Ошибка при выполнении запроса: {errorType}")
except El.ParseError as errorType:
    print(f"Ошибка при парсинге XML: {errorType}")
except Exception as errorType:
    print(f"Неожиданная ошибка: {errorType}")