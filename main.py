from telethon import TelegramClient, events
from datetime import datetime, timedelta
import asyncio
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
target_channel = os.getenv("TARGET_CHANNEL")

source_channels = [
    'agent_pepki', 'agentadurovatg', 'allcombokod', 'andrew_portugalets',
    'auctions_stars', 'barontono', 'bears_nft', 'bestnewsnft',
    'buystarseasy', 'catlipseton', 'cryptobumss', 'cryptosharkg1',
    'cryptosiege', 'cryptotullon', 'cryptozavrek', 'darthmere_channel',
    'dhehhshop', 'durovson', 'easygiftnews', 'everygift', 'fekalist',
    'flugrandnft', 'freepodarkisnow', 'fuckbroton', 'gat_free',
    'gat_main', 'gemsmens', 'ggtonru', 'giftexplorercommunity',
    'giftgalaxychannel', 'gifthuber', 'giftinspector', 'giftmaloy',
    'gifts_nftishki', 'gimme_life', 'giveawaystracker', 'grinch_v_ton',
    'hzcrypto', 'lacostestars', 'lavkadurova', 'lowake', 'lusuidurov',
    'markushooo', 'muha_gadjjj', 'nemnogopodarkov', 'nft_ludka',
    'nftbulls_nft', 'otbivnaya_iz_krypti', 'otzivitik', 'papa_kupil_futures',
    'papa_kupil_nft', 'pepe_challenge', 'plantation', 'pluxury_rare',
    'podarokdurova', 'projectx2277', 'qwerdnft', 'ruleltgift',
    's_nyl9_do_pepe', 'silentiumnft', 'silswag', 'skeletonnftt',
    'tgnews_nft', 'toiletgift', 'tokenflippers', 'tonnel_en',
    'tonovskiykot', 'valutacry', 'vipfragment_gifts', 'vladlenton',
    'westik', 'worldnftintg'
]

keywords = [
    'розыгрыш', 'приз', 'условия', 'подпишись', 'бесплатно', 'подарок',
    'разыгрываем', 'участие', 'выиграй', 'получи', 'дарим',
    'airdrop', 'giveaway', 'условия просты', 'спонсор', 'отметь друга'
]

client = TelegramClient('session', api_id, api_hash)
saved_messages = []

async def auto_delete_old():
    while True:
        now = datetime.now()
        for msg in saved_messages[:]:
            if now - msg['time'] > timedelta(days=7):
                try:
                    await client.delete_messages(target_channel, msg['id'])
                    saved_messages.remove(msg)
                except: pass
        await asyncio.sleep(3600)

async def process_post(event):
    try:
        if not event.chat or not event.chat.username:
            return
        username = event.chat.username.lower()
        if username not in source_channels:
            return
        text = event.raw_text.lower()
        if any(word in text for word in keywords) and ('@' in text or 'подпиш' in text):
            fwd = await client.forward_messages(target_channel, event.message)
            saved_messages.append({'id': fwd.id, 'time': datetime.now()})
            print(f"[FORWARDED] @{username}")
    except Exception as e:
        print(f"[ERROR] {e}")

@client.on(events.NewMessage)
async def handler(event):
    await process_post(event)

async def main():
    print("Bot started and listening...")
    await asyncio.gather(client.run_until_disconnected(), auto_delete_old())

with client:
    client.loop.run_until_complete(main())
