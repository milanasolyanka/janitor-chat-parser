import json
from text_utils import extract_words


def process_file(filename: str) -> tuple[int, int]:
    """
    Обрабатывает JSON-файл с историей чата и подсчитывает количество слов.

    Функция извлекает все сообщения из поля `chatMessages`
    и считает:
    - общее количество слов во всех сообщениях
    - количество слов только в сообщениях пользователя
      (где is_bot == False)

    Parameters
    ----------
    filename : str
        Путь к JSON-файлу.

    Returns
    -------
    tuple[int, int]
        Кортеж из двух значений:
        (all_words_count, not_bot_words_count)
    """

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    character_name = data.get("character", {}).get("name", "Unknown")

    chat_messages = data.get("chatMessages", [])

    all_words_count = 0
    not_bot_words_count = 0

    for msg in chat_messages:
        message_text = msg.get("message")
        if not message_text:
            continue

        words = extract_words(message_text)
        all_words_count += len(words)

        if msg.get("is_bot") is False:
            not_bot_words_count += len(words)

    return character_name, all_words_count, not_bot_words_count