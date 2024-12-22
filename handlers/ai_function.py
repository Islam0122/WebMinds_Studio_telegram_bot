import base64
import json
import os
import uuid
from io import BytesIO

import requests
from aiogram import Bot, types
from dotenv import load_dotenv, find_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv(find_dotenv())

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('SECRET')


def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),  # уникальный идентификатор запроса
    }
    payload = {"scope": "GIGACHAT_API_PERS"}

    try:
        res = requests.post(
            url=url,
            headers=headers,
            auth=HTTPBasicAuth(CLIENT_ID, SECRET),
            data=payload,
            verify=False,  # Убедитесь, что использование verify=False безопасно для вашей среды
        )
        res.raise_for_status()  # проверка на наличие ошибок
        access_token = res.json().get("access_token")
        if not access_token:
            raise ValueError("Токен доступа не был получен.")
        return access_token
    except requests.RequestException as e:
        print("Ошибка при получении access token:", e)
        return None



def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": msg,
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        response.raise_for_status()  # проверка на наличие ошибок
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        print("Ошибка при отправке запроса к GigaChat API:", e)
        return "Ошибка при получении ответа от GigaChat."


def sent_prompt_and_get_response(msg: str):
    access_token = get_access_token()

    message = (
        f"✨🌈 Придумай необычную и уникальную сказку о {msg} 🧚‍♀️🦄! "
        f"Пусть это будет история, в которой царства превращаются в нечто удивительное, а герои сталкиваются с необычными событиями и открытиями 🌟🌌. "
        f"Наполни её чудесами, смайликами и волшебными элементами, чтобы она была яркой и запоминающейся! 😍🎭. "
        f"Убедись, что текст не превышает 3000 символов, включая пробелы и смайлики. Постарайся сохранить логичность сюжета и увлекательность."
    )

    if access_token:
        response = send_prompt(message, access_token)
        decorated_response = f'✨🌟 {response} 🌈🧚‍♂️'
        return decorated_response
    else:
        return "Не удалось получить access token."


def sent_prompt_and_get_response_2(msg: str):
    access_token = get_access_token()

    # Формируем сообщение для ИИ с учётом вопроса пользователя о студии
    message = (
        f"Пользователь задал вопрос: '{msg}'\n\n"
        "Ответьте на этот вопрос, используя информацию о нашей студии WebMinds Studio. "
        "У нас есть следующие услуги:\n"
        "1. 🌐 Разработка сайтов — создание современных и функциональных сайтов для бизнеса.\n"
        "2. 🤖 Создание Telegram-ботов — разработка удобных и эффективных ботов.\n"
        "3. 🔍 SEO-оптимизация — повышение видимости сайта в поисковых системах.\n"
        "4. ⚙️ Индивидуальные решения — разработка решений для специфических задач.\n"
        "5. 📈 Внедрение CRM-систем — интеграция CRM для улучшения бизнес-процессов.\n\n"
        "Пожалуйста, ответьте на вопрос, используя эти данные и добавьте дополнительную информацию, если это необходимо."
    )

    if access_token:
        response = send_prompt(message, access_token)  # Отправляем запрос в ИИ
        decorated_response = f'✨🌟 {response} 🌈🧚‍♂️'  # Украшаем ответ
        return decorated_response
    else:
        return "Не удалось получить access token."
