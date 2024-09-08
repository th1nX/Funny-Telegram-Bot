import ast
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon import events
from features import db
from dotenv import load_dotenv
from os import getenv

load_dotenv()

api_id = getenv('API_ID') #string
api_hash = getenv('API_HASH') #string
phone = getenv('PHONE_NUMBER') #string
allowed_tgids = ast.literal_eval(getenv('ALLOWED_TGIDS')) #list


async def main():
    async with TelegramClient(phone, api_id, api_hash) as client:
        async def reload_chats():
            chats = []
            result = await client(GetDialogsRequest(  # -- Getting all chats and channels from TG account
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                hash=0,
                limit=1000
            ))
            chats.extend(result.chats)
            for chat in chats:
                if chat.title != 'Unsupported Chat':
                    id = chat.id
                    name = chat.title
                    status = True
                    count = chat.participants_count
                    db.insert_canal(id, id, name, status, count)
            print('All chats was reloaded!')

        @client.on(events.NewMessage(pattern='/start'))
        async def start(event):
            user_id = event.sender_id
            if user_id in allowed_tgids:
                print(user_id + " used /start command")
                await event.reply(
                """
Бот: 
- Для создания базы данных нужно прописать /create

- Для добавления чатов нужно зайти на аккаунт и присоединиться к чату самостоятельно.

- Для перезагрузки списка чатов нужно использовать /reload

- Для обновления текста рассылки нужно использовать /update (Ваш текст) (Можно с абзацами)

- Для начала рассылки по каналам нужно использовать /mailing

- Для обновления текста спама нужно использовать /supd (Ваш текст) (Можно с абзацами)

- Для начала спама по TelegramId (Именно цифрового) нужно использовать /spam (Telegram Id) (Количество сообщений)
!Цифровой Telegram ID можно получить здесь -> @username_to_id_bot !
                """)
            else:
                print(user_id)
                await event.reply('Ты тупой? Я тебе не бот.')

        @client.on(events.NewMessage(pattern='/reload'))
        async def reloading(event):
            user_id = event.sender_id
            if user_id in allowed_tgids:
                await reload_chats()
                await event.reply('Бот: Чаты перезагружены!')
                print('\nChats were reloaded.')

        @client.on(events.NewMessage(pattern='/mailing'))
        async def mailing(event):
            user_id = event.sender_id
            print('\nStart mailing...')
            if user_id in allowed_tgids:
                for id in db.get_all_id():
                    await client.send_message(id, db.get_text(0))
                await event.reply('Бот: Рассылка завершена!')
                print('\nMailing was completed!')

        @client.on(events.NewMessage(pattern='/update'))
        async def update(event):
            user_id = event.sender_id
            if user_id in allowed_tgids:
                text = event.raw_text.replace('/update', '').replace(' ', '', 1)
                db.update_text(0, text)
                await  event.reply(
            f"""
Бот: Текст обновлён!
Ваш текущий текст для рассылки:
{text}            
            """)
                print('\nText for mailing was updated!')

        @client.on(events.NewMessage(pattern='/supd'))
        async def update(event):
            user_id = event.sender_id
            if user_id in allowed_tgids:
                spam_text = event.raw_text.replace('/supd', '').replace(' ', '', 1)
                db.update_text(1, spam_text)
                await  event.reply(
                f"""
Бот: Текст обновлён!
Ваш текущий текст для спама:
{spam_text}            
                """)
                print('\nText for spamming was updated!')

        @client.on(events.NewMessage(pattern='/spam'))
        async def spam(event):
            user_id = event.sender_id
            if user_id in allowed_tgids:
                victim_id = int(event.raw_text.split()[1])
                counter = int(event.raw_text.split()[2])
                print(f'\nStart spamming [{counter}] times to {victim_id} ...')
                for i in range(counter):
                    await client.send_message(victim_id, db.get_text(1))
                await client.send_message(user_id, f"Бот: Спам пользователю {victim_id} закончен.")
                print('\nSpamming was completed!')

        @client.on(events.NewMessage(pattern='/create'))
        async def create(event):
            user_id = event.sender_id
            if user_id in allowed_tgids:
                print('\nDatabase was created!')
                await db.create_db()

        print(f"{'-'*40}\nBot was started!\n{'-'*40}")
        await client.run_until_disconnected()


asyncio.run(main())

