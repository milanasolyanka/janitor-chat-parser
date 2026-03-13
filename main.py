import json
import re
import os

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

GRAPH_DIR = "graphs"


def extract_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z']+", text.lower())


def process_file(filename: str) -> tuple[int, int]:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

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

    return all_words_count, not_bot_words_count


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

    plot_sorted_bar_chart(
        filenames,
        all_words_stats,
        "Количество слов (all_words)",
        os.path.join(GRAPH_DIR, "all_words.png")
    )

    plot_sorted_bar_chart(
        filenames,
        not_bot_words_stats,
        "Количество слов (not_bot_words)",
        os.path.join(GRAPH_DIR, "not_bot_words.png")
    )

    print("Графики сохранены в папке graphs/")


if __name__ == "__main__":
    main()