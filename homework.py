import os
import requests
import telegram
import time
import logging
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL_PRACT = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
BOT = telegram.Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework):
    if 'homework_name' and 'status' in homework.keys():
        logging.error('Сервачек не хочет работать:(')
    homework_name = homework['homework_name']
    if homework['status'] != 'approved':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    if current_timestamp is None:
        logging.error(f'Проверь значение {current_timestamp}')
    try:
        homework_statuses = requests.get(URL_PRACT, headers=headers, params=params)
        return homework_statuses.json()
    except:
        logging.error('Проверь что передаешь!')


def send_message(message):
    bot = BOT
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            logging.error(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
