import re


def extract_words(text: str) -> list[str]:
    """
    Извлекает слова из текстовой строки.

    Функция ищет последовательности латинских букв и апострофов,
    приводя текст к нижнему регистру.

    Parameters
    ----------
    text : str
        Исходный текст сообщения.

    Returns
    -------
    list[str]
        Список найденных слов.
    """

    return re.findall(r"[A-Za-z']+", text.lower())