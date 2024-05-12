"""
Module для парсинга и классификации сообщений из скриншотов диалогов.

Этот модуль содержит функции для авторизации на Yandex Cloud, отправки изображений
на OCR обработку, а также классификации полученных текстовых блоков в сообщениях.
Основная функциональность включает в себя определение отправителя сообщения и
исключение системных сообщений, основываясь на их положении на изображении.

Основной скрипт (main) обрабатывает аргументы командной строки для настройки
параметров запроса и выводит результаты классификации сообщений.

Пример использования:
python text_recognition.py --folder-id "123" --oauth-token "token" --image-path "path/to/image.png"
"""
import re
import json
import argparse
import base64
from requests import post

def get_iam_token(iam_url, oauth_token):
    """
    Получает IAM-токен для авторизации запросов на Yandex Cloud.

    Args:
        iam_url (str): URL для запроса IAM-токена.
        oauth_token (str): OAuth токен пользователя Яндекса.

    Returns:
        str: IAM-токен или None, если запрос не успешен.
    """
    response = post(iam_url, json={"yandexPassportOauthToken": oauth_token}, timeout=20)
    json_data = json.loads(response.text)
    if json_data is not None and 'iamToken' in json_data:
        return json_data['iamToken']
    return None

def request_analyze(ocr_url, iam_token, folder_id, image_data):
    """
    Отправляет изображение на сервер Yandex Cloud для распознавания текста.

    Args:
        vision_url (str): URL OCR сервиса Yandex Cloud.
        iam_token (str): IAM-токен для авторизации запроса.
        folder_id (str): Идентификатор папки на Yandex Cloud.
        image_data (str): Изображение в формате base64.

    Returns:
        str: Ответ сервера в формате JSON.
    """
    response = post(ocr_url,
        headers={'Authorization': 'Bearer ' + iam_token, 'x-folder-id': folder_id},
        json=
    {
        "mimeType": "*",
        "languageCodes": ["*"],
        "model": "page",
        "content": image_data
    },
      timeout=20)
    return response.text

def main():
    """
    Главная функция, обрабатывающая аргументы командной строки,
    выполняющая запрос к OCR сервису и классифицирующая сообщения из скриншота.
    Обрабатывает аргументы командной строки, запрашивает IAM-токен, 
    отправляет изображение на обработку и выводит классифицированные сообщения.
    """
    # Создаем парсер аргументов командной строки и задаем необходимые аргументы
    parser = argparse.ArgumentParser()

    parser.add_argument('--folder-id', required=True)
    parser.add_argument('--oauth-token', required=True)
    parser.add_argument('--image-path', required=True)
    args = parser.parse_args()

    # Указываем URL для IAM токена и OCR сервиса
    iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    ocr_url = 'https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText'

    # Получаем IAM токен с помощью функции get_iam_token
    iam_token = get_iam_token(iam_url, args.oauth_token)
    # Читаем изображение, кодируем в base64 и отправляем на анализ
    with open(args.image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    response_text = request_analyze(ocr_url, iam_token, args.folder_id, image_data)

    # Парсим ответ от сервера
    response_data = json.loads(response_text)

    # Определяем ширину изображения и вычисляем середину
    image_width = int(response_data["result"]["textAnnotation"]["width"])
    midpoint = image_width / 2

    # Устанавливаем порог для определения системных сообщений
    threshold = 0.05  # 8% от ширины изображения считается центральной зоной
    system_msg_min_x = midpoint - (image_width * threshold / 2)
    system_msg_max_x = midpoint + (image_width * threshold / 2)

    # Компилируем регулярные выражения для времени и специальных символов
    time_pattern = re.compile(r'\b\d{1,2}:\d{2}\b')
    symbols_pattern = re.compile(r'[//]+')

    classified_messages = []

    # Цикл обработки каждого блока текста в ответе сервера OCR.
    for block in response_data["result"]["textAnnotation"]["blocks"]:
        # Обходим каждую линию в блоке
        for line in block["lines"]:
            text = line["text"]
            vertices = line["boundingBox"]["vertices"]
            # Вычисляем среднюю X координату для классификации сообщения
            x_coords = [int(vertex["x"]) for vertex in vertices]
            current_x = sum(x_coords) / len(x_coords)

            # Исключаем системные сообщения, попадающие в центральную зону
            if system_msg_min_x <= current_x <= system_msg_max_x:
                continue  # Пропускаем системные сообщения

            # Определяем отправителя сообщения
            sender = "Partner" if current_x < midpoint else "You"

            # Удаляем время и специальные символы из текста сообщения
            text = time_pattern.sub("", text)
            text = symbols_pattern.sub("", text)

            # Добавляем очищенное сообщение в список, если оно не пустое
            if text.strip():
                classified_messages.append((sender, text.strip()))

    # Выводим классифицированные сообщения
    for sender, text in classified_messages:
        print(f"{sender}: {text}")

if __name__ == '__main__':
    main()