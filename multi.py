import asyncio
import random
import json
from telethon import TelegramClient, functions, errors
import aiohttp
import os
import time
from datetime import datetime

COLORS = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "END": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}

ACCOUNTS_FILE = "accounts.json"
PROGRESS_FILE = "progress.json"


def show_watermark():
    print(COLORS["RED"] + "="*50 + COLORS["END"])
    print(COLORS["GREEN"] + r"""  
      ██ ███    ██ ██   ██ ██    ██ ███    ███  █████  ███    ██ ████████ ████████ 
      ██ ████   ██ ██   ██ ██    ██ ████  ████ ██   ██ ████   ██    ██       ██    
      ██ ██ ██  ██ ███████ ██    ██ ██ ████ ██ ███████ ██ ██  ██    ██       ██    
      ██ ██  ██ ██ ██   ██ ██    ██ ██  ██  ██ ██   ██ ██  ██ ██    ██       ██    
      ██ ██   ████ ██   ██  ██████  ██      ██ ██   ██ ██   ████    ██       ██                                                                                                                                                             
""" + COLORS["END"])
    print(COLORS["BLUE"] + " " * 15 + "INHUMANTT" + COLORS["END"])
    print(COLORS["RED"] + "="*50 + COLORS["END"] + "\n")


def install_requirements():
    try:
        import aiohttp
        import telethon
    except ImportError:
        import subprocess
        subprocess.check_call(["python", "-m", "pip", "install", "telethon", "aiohttp"])


def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=2)


async def get_user_input():
    while True:
        try:
            count = int(input(COLORS["YELLOW"] + "How many groups to create per account? " + COLORS["END"]))
            if count < 1:
                raise ValueError
            break
        except ValueError:
            print(COLORS["RED"] + "Enter a number greater than 0." + COLORS["END"])

    accounts = []
    while True:
        print(COLORS["CYAN"] + "Please enter the following details for the account:" + COLORS["END"])
        phone = input("Phone number (e.g., +18106834498): ").strip()
        api_id = input("API ID: ").strip()
        api_hash = input("API Hash: ").strip()
        accounts.append({'phone': phone, 'api_id': api_id, 'api_hash': api_hash})
        cont = input("Do you want to add another account? (y/n): ").lower()
        if cont != 'y':
            break

    save_accounts(accounts)
    return count


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f)


async def fetch_random_image(client):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://picsum.photos/500?random={random.randint(1, 9999)}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    return await client.upload_file(data, file_name='group_photo.jpg')
    except Exception as e:
        print(COLORS["RED"] + f"Image error: {e}" + COLORS["END"])
    return None


async def login_account(account):
    phone, api_id, api_hash = account.values()
    client = TelegramClient(f'{phone}.session', api_id, api_hash)

    try:
        await client.start(phone)
        print(COLORS["GREEN"] + f"Logged in: {phone}" + COLORS["END"])
        return client
    except errors.PhoneNumberBannedError:
        print(COLORS["RED"] + f"Account {phone} is banned. Skipping." + COLORS["END"])
    except Exception as e:
        print(COLORS["RED"] + f"Login failed for {phone}: {e}" + COLORS["END"])
    return None


async def login_all_accounts():
    accounts = load_accounts()
    clients = []
    for account in accounts:
        client = await login_account(account)
        if client:
            clients.append(client)
    return clients


async def create_groups_for_account(client, total_count):
    phone = client.session.filename.split('.')[0]
    progress = load_progress()
    done = progress.get(phone, 0)

    if done >= total_count:
        print(COLORS["YELLOW"] + f"Skipping {phone} — already created {done}/{total_count} groups." + COLORS["END"])
        return False

    prefixes = ['', 'The ', 'Global ', 'United ']
    adjectives = ['Emerald', 'Golden', 'Silver', 'Cosmic', 'Urban']
    nouns = ['Network', 'Collective', 'Hub', 'Circle', 'Alliance']
    suffixes = ['Chat', 'Group', 'Zone', 'Connect']
    emojis = ['🌟', '✨', '🔥', '🚀', '💬']
    bios = [
        "Welcome! Let's grow together.",
        "Connecting people worldwide.",
        "Join the conversation.",
        "Open space for ideas.",
        "Friendly community chat."
    ]
    messages = [
        ("Welcome! Please introduce yourself.", 1.2),
        ("Check the pinned message for rules.", 0.8),
        ("Weekly event starts soon!", 1.5),
        ("Invite friends to join!", 1.0),
        ("Poll live now. Vote!", 1.1)
    ]

    print(COLORS["GREEN"] + f"\n[{phone}.session] Resuming from {done}/{total_count}" + COLORS["END"])
    start_time = time.monotonic()

    for i in range(done + 1, total_count + 1):
        name = f"{random.choice(prefixes)}{random.choice(adjectives)}{random.choice(nouns)} {random.choice(suffixes)}"
        if random.random() > 0.3:
            name += f" {random.choice(emojis)}"
        name = name.replace("  ", " ").strip()
        about = random.choice(bios)

        await asyncio.sleep(random.uniform(1.5, 3.0))

        try:
            group = await client(functions.channels.CreateChannelRequest(
                title=name,
                about=about,
                megagroup=True
            ))
        except errors.FloodWaitError as e:
            print(COLORS["RED"] + f"[{phone}] FloodWaitError: {e.seconds}s. Saving progress & stopping." + COLORS["END"])
            progress[phone] = i - 1
            save_progress(progress)
            return True

        entity = group.chats[0]

        photo = await fetch_random_image(client)
        if photo:
            try:
                await client(functions.channels.EditPhotoRequest(
                    channel=entity,
                    photo=photo
                ))
                await asyncio.sleep(random.randint(25, 40))
            except errors.FloodWaitError as e:
                print(COLORS["RED"] + f"[{phone}] Flood wait on photo: {e.seconds}s. Saving & stopping." + COLORS["END"])
                progress[phone] = i - 1
                save_progress(progress)
                return True

        for msg, d in random.choices(messages, k=5):
            await client.send_message(entity=entity, message=msg)
            await asyncio.sleep(d + random.uniform(-0.3, 0.5))

        elapsed = int((time.monotonic() - start_time) / 60)
        now = datetime.now().strftime("%H:%M:%S")
        print(COLORS["CYAN"] + f"[{i}/{total_count}] | Elapsed: {elapsed}m | Time: {now}" + COLORS["END"])
        print(COLORS["GREEN"] + f"Created {name}" + COLORS["END"])
        print(COLORS["YELLOW"] + f"» Bio: {about}" + COLORS["END"])

        progress[phone] = i
        save_progress(progress)

        if i < total_count:
            wait = 270
            print(f"Next group in {wait} seconds")
            await asyncio.sleep(wait)

    return True


async def main():
    install_requirements()
    show_watermark()
    count = await get_user_input()

    while True:
        clients = await login_all_accounts()

        any_work_done = False
        for client in clients:
            result = await create_groups_for_account(client, count)
            if result:
                any_work_done = True

        if not any_work_done:
            print(COLORS["GREEN"] + "\nAll accounts have already created the required number of groups." + COLORS["END"])
        else:
            print(COLORS["CYAN"] + "\nGroup creation cycle completed." + COLORS["END"])

        print(COLORS["YELLOW"] + "Sleeping for 24 hours before restarting..." + COLORS["END"])
        await asyncio.sleep(86400)


if __name__ == '__main__':
    asyncio.run(main())
