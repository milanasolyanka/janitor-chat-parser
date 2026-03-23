import os
from datetime import datetime

from json_processing import process_file
from graph_utils import plot_sorted_bar_chart


JSON_DIR = "./jsons"

# папка с текущей датой
GRAPH_DIR = datetime.today().strftime("%Y.%m.%d")

TOP_N = 10

def format_character_label(name: str, file_id: str, max_len: int = 15) -> str:
    """
    Обрезает имя персонажа и добавляет id.

    Parameters
    ----------
    name : str
        Имя персонажа (character.name)
    file_id : str
        ID (например имя файла без .json)
    max_len : int
        Максимальная длина имени

    Returns
    -------
    str
        Отформатированная строка
    """

    if len(name) > max_len:
        name = name[:max_len] + "...\n"

    return f"{name} ({file_id})"

def remove_json_extension(filename: str) -> str:
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

    character_names = []
    all_words_stats = []
    not_bot_words_stats = []

    for filename in os.listdir(JSON_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(JSON_DIR, filename)

        try:
            file_id = remove_json_extension(filename)

            character_name, all_count, not_bot_count = process_file(filepath)

            label = format_character_label(character_name, file_id)

            character_names.append(label)
            all_words_stats.append(all_count)
            not_bot_words_stats.append(not_bot_count)

            print(f"{label}")
            print(f"  all_words: {all_count}")
            print(f"  not_bot_words: {not_bot_count}\n")

        except Exception as e:
            print(f"[ERROR] {filename}: {e}")

    # берём топ-10
    top_all_names, top_all_values = get_top_n(
        character_names,
        all_words_stats,
        TOP_N
    )

    top_notbot_names, top_notbot_values = get_top_n(
        character_names,
        not_bot_words_stats,
        TOP_N
    )

    # график all_words
    plot_sorted_bar_chart(
        top_all_names,
        top_all_values,
        "Количество слов (all_words)",
        os.path.join(GRAPH_DIR, "all_words.png")
    )

    plot_sorted_bar_chart(
        top_notbot_names,
        top_notbot_values,
        "Количество слов (not_bot_words)",
        os.path.join(GRAPH_DIR, "not_bot_words.png")
    )

    print(f"Графики сохранены в папке {GRAPH_DIR}/")


if __name__ == "__main__":
    main()