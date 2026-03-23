import requests
import json
import os
import time
import random

from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("BASE_URL")
TOKEN = os.getenv("JANITOR_TOKEN")


USER_AGENT = os.getenv("USER_AGENT")
APP_VERSION = os.getenv("APP_VERSION")

DATA_DIR = os.getenv("DATA_DIR")

MESSAGES_FILE = os.path.join(DATA_DIR, os.getenv("MESSAGES_FILE"))
DOWNLOADED_CHATS_FILE = os.path.join(DATA_DIR, os.getenv("DOWNLOADED_CHATS_FILE"))

COOKIE = os.getenv("COOKIE")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/plain, */*",
    "Referer": BASE_URL,
    "x-app-version": APP_VERSION,
    "Cookie": COOKIE,
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

if not TOKEN:
    raise Exception("JANITOR_TOKEN not found in .env")


os.makedirs(DATA_DIR, exist_ok=True)


def sleep_random():
    time.sleep(random.uniform(0.8, 3.0))


def load_downloaded_chats():
    if not os.path.exists(DOWNLOADED_CHATS_FILE):
        return {}

    with open(DOWNLOADED_CHATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_downloaded_chats(data):
    with open(DOWNLOADED_CHATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def append_messages(messages):
    with open(MESSAGES_FILE, "a", encoding="utf-8") as f:
        for m in messages:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")


def get_json(url):
    r = requests.get(url, headers=HEADERS)

    if r.status_code == 401:
        raise Exception("Authorization failed. Token probably expired.")

    r.raise_for_status()

    return r.json()


def fetch_characters():
    print("[INFO] Fetching characters")

    page = 1
    characters = []

    while True:
        print(f"[INFO] Loading character page {page}")

        url = f"{BASE_URL}/hampter/chats/character-chats?page={page}&sortBy=latest"

        data = get_json(url)

        characters.extend(data["characters"])

        if not data["hasMore"]:
            break

        page += 1
        sleep_random()

    print(f"[INFO] Total characters found: {len(characters)}")

    return characters


def fetch_character_chats(character_id):
    url = f"{BASE_URL}/hampter/chats/character/{character_id}/chats"

    data = get_json(url)

    return data["chats"]


def fetch_chat(chat_id):
    url = f"{BASE_URL}/hampter/chats/{chat_id}"

    return get_json(url)


def process_chat(chat_data):
    character = chat_data["character"]
    character_id = character["id"]
    character_name = character["name"]

    messages = []

    for msg in reversed(chat_data["chatMessages"]):
        sender = "bot" if msg["is_bot"] else "user"

        messages.append({
            "chat_id": chat_data["chat"]["id"],
            "character_id": character_id,
            "character_name": character_name,
            "sender": sender,
            "text": msg["message"]
        })

    return messages


def main():
    print("[INFO] Starting export")

    downloaded_chats = load_downloaded_chats()

    print(f"[INFO] Already downloaded chats: {len(downloaded_chats)}")

    characters = fetch_characters()

    total_characters = len(characters)

    for i, character in enumerate(characters, start=1):

        character_id = character["character_id"]
        character_name = character["name"]

        print(f"[INFO] Processing character {i}/{total_characters}: {character_name}")

        try:
            chats = fetch_character_chats(character_id)
        except Exception as e:
            print(f"[ERROR] Failed to fetch chats for {character_name}: {e}")
            continue

        print(f"[INFO] Chats found: {len(chats)}")

        sleep_random()

        for chat in chats:

            chat_id = str(chat["id"])

            if chat_id in downloaded_chats:
                print(f"[INFO] Chat {chat_id} already downloaded")
                continue

            print(f"[INFO] Downloading chat {chat_id}")

            try:
                chat_data = fetch_chat(chat_id)
            except Exception as e:
                print(f"[ERROR] Failed to fetch chat {chat_id}: {e}")
                continue

            messages = process_chat(chat_data)

            append_messages(messages)

            downloaded_chats[chat_id] = True

            print(f"[INFO] Saved messages: {len(messages)}")

            sleep_random()

    save_downloaded_chats(downloaded_chats)

    print("[INFO] Export finished")


if __name__ == "__main__":
    main()