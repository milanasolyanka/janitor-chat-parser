import os
from datetime import datetime

from json_processing import process_file
from graph_utils import plot_sorted_bar_chart


SOURCE_JSON_LIST = [
    'anaxa_arranged_m_1.json',
    'anaxa_arranged_m_2.json',
    'anaxa_cuntboy.json',
    'anaxa_slowburn.json',
    'blade.json',
    'blade_tyrant.json',
    'feixiao.json',
    'jingyuan_prince.json',
    'jingyuan_teacher.json'
]

# папка с текущей датой
GRAPH_DIR = datetime.today().strftime("%Y.%m.%d")

TOP_N = 10

def remove_json_extension(filename: str) -> str:
    """
    Удаляет расширение .json из имени файла.

    Parameters
    ----------
    filename : str
        Имя файла с расширением.

    Returns
    -------
    str
        Имя файла без .json
    """
    return os.path.splitext(filename)[0]


def get_top_n(filenames, values, n):
    """
    Возвращает топ-N элементов по значению.

    Parameters
    ----------
    filenames : list[str]
        Список имен файлов.
    values : list[int]
        Соответствующие значения.
    n : int
        Количество элементов, которое нужно оставить.

    Returns
    -------
    tuple[list[str], list[int]]
        Отфильтрованные списки (filenames, values)
    """

    sorted_data = sorted(
        zip(filenames, values),
        key=lambda x: x[1],
        reverse=True
    )[:n]

    top_files, top_values = zip(*sorted_data)
    return list(top_files), list(top_values)

def main():
    os.makedirs(GRAPH_DIR, exist_ok=True)

    filenames = []
    all_words_stats = []
    not_bot_words_stats = []

    for filename in SOURCE_JSON_LIST:
        all_count, not_bot_count = process_file(filename)

        filenames.append(filename)
        all_words_stats.append(all_count)
        not_bot_words_stats.append(not_bot_count)

        print(f"{filename}")
        print(f"  all_words: {all_count}")
        print(f"  not_bot_words: {not_bot_count}\n")

    # убираем .json для подписей
    clean_filenames = [remove_json_extension(f) for f in filenames]

    # берём топ-10
    top_all_files, top_all_values = get_top_n(
        clean_filenames,
        all_words_stats,
        TOP_N
    )

    top_notbot_files, top_notbot_values = get_top_n(
        clean_filenames,
        not_bot_words_stats,
        TOP_N
    )

    # график all_words
    plot_sorted_bar_chart(
        top_all_files,
        top_all_values,
        "Количество слов (all_words)",
        os.path.join(GRAPH_DIR, "all_words.png")
    )

    # график not_bot_words
    plot_sorted_bar_chart(
        top_notbot_files,
        top_notbot_values,
        "Количество слов (not_bot_words)",
        os.path.join(GRAPH_DIR, "not_bot_words.png")
    )

    print(f"Графики сохранены в папке {GRAPH_DIR}/")


if __name__ == "__main__":
    main()