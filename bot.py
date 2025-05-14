from telethon import TelegramClient, events
import asyncio
import random
import datetime
import re

api_id = 23155794
api_hash = '9de8c86f1c18583aab9765dd6360eb5a'
DEST_CHANNEL = 'Only_givee'

KEYWORDS = [
    'gift', 'giveaway!', 'prizes:',
    'розыгрыш', 'подарок', 'бесплатно', 'участвуй'
]

EXCLUDE_WORDS = [
    'рулетка',
    'на подарок',
    'на дорогой подарок',
    'приз выдан',
    'результаты розыгрыша',
    'получает нфт подарок',
    'один прокрут',
    'цена одной попытки',
    'подарок выдан'
]

used_links_sets = []

def extract_links(text):
    return set(re.findall(r'(https?://\S+|t\.me/\S+|@\w+|\S+\.gg|\S+\.me)', text.lower()))

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    try:
        if event.is_channel and not event.is_group:
            message_text = event.raw_text.lower().strip()
            links = extract_links(message_text)

            if any(kw in message_text for kw in KEYWORDS):
                if not any(ex in message_text for ex in EXCLUDE_WORDS):
                    if not links:
                        print("🔗 Нет ссылок — пропущено")
                        return

                    for used in used_links_sets:
                        if links == used:
                            print("🔁 Дубликат по ссылкам — пропущено")
                            return

                    await asyncio.sleep(random.uniform(2, 4))
                    fwd = await event.forward_to(DEST_CHANNEL)
                    print(f"✅ Переслано: {event.chat.title}")

                    used_links_sets.append(links)
                    if len(used_links_sets) > 100:
                        used_links_sets.pop(0)

                    await asyncio.sleep(604800)
                    await fwd.delete()
                    print("🗑 Удалено (7 дней)")
                else:
                    print("⛔ Пропущено (исключение)")
            else:
                print("🤏 Нет ключевых слов — пропущено")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")

print("🤖 Бот Railway готов к работе...")
with client:
    client.run_until_disconnected()

