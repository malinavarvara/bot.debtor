import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram import F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import html
from aiogram.filters import Command, CommandObject
from aiogram.utils.markdown import hide_link
from datetime import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder
import kb
import config
import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client[config.db_name]
mongo_item = mongo_db['item']


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6774574734:AAHrGYBuHs42l9wi2ABjR8ljLodLKTCEYvM")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")
    await message.answer(
        "Выберите команду:",
        reply_markup=kb.get_kb_menu()
    )

#описание бота
@dp.message(F.text.lower() == "инструкция")
async def with_puree(message: types.Message):
    await message.answer("Всё гениальное просто, и всё простое гениально.\nУ тебя есть 5 функций.\n\
Первые две (создать долг и создать свой долг) предназначены для записи долгов. Ты можешь записывать как чужой долг,\
 так и свой (ничего не мешает тебе создать долг самому себе). При нажатии на кнопки есть указания, как правильно вводить данные.\
\nТакже есть команды для просмотра долгов. Там указаны должник (или тот, кому ты должен), вещь, которую должны и статус долга.\
\nПоследняя функция для того, чтобы обозначить, что долг вернули. Ясное дело, что ты можешь обозначить возвращение только чужих \
долгов. Иначе слишком просто))\
\nПользуйся и не копи долги")
    await message.answer(
        "Выберите команду:",
        reply_markup=kb.get_kb_menu()
    )

#Чей-то долг
@dp.message(F.text.lower() == "создать долг")
async def extract_data(message: Message):
    await message.answer("Введи...\nДолг: \n <tg должника> \n <опиисание долга> \n <дата возвращения долга>")
    await message.answer("Пример:\nДолг: \n@Саня \nсотку \nзавтра")

@dp.message(F.text.startswith('Долг:'))
async def cmd_settimer(
        msg: types.Message, bot: Bot
):
    print('added new debt\n')
    print(msg)
    values = msg.text.split("\n")
    print(values)
    id_recipient = msg.chat.username
    id_debtor = values[1]
    description = values[2]
    time_now = datetime.today() .strftime('%d/%m/%y %H:%M')
    date_start = time_now
    date_end = values[3]
    if id_debtor is None:
        id_debtor = None

    mongo_item.insert_one({"id_recipient": id_recipient, \
                           "id_debtor": id_debtor[1:],\
                           "description": description, \
                           "date_start": date_start, \
                           "date_end": date_end, "status": 'active'})

    await msg.answer(
        f"Кому должны: @{id_recipient}\n"
        f"Должник: {id_debtor}\n"
        f"Что должен: {description}\n"
        f"Остчет от {date_start} до {date_end}"
    )
    await msg.answer(
        "Выберите команду:",
        reply_markup=kb.get_kb_menu()
    )
#Мой долг
@dp.message(F.text.lower() == "создать свой долг")
async def extract_data(message: Message):
    await message.answer("Введи...\nДолжен: \n <tg кому должен> \n <опиисание долга> \n <дата возвращения долга>")
    await message.answer("Пример:\nДолжен: \n@Саня \nподзатыльник \nзавтра")

@dp.message(F.text.startswith('Должен:'))
async def cmd_settimer(
        msg: types.Message, bot: Bot
):
    print('added new debt\n')
    print(msg)
    values = msg.text.split("\n")
    print(values)
    id_recipient = values[1]
    id_debtor = msg.chat.username
    description = values[2]
    time_now = datetime.today() .strftime('%d/%m/%y %H:%M')
    date_start = time_now
    date_end = values[3]
    if id_debtor is None:
        id_debtor = None

    mongo_item.insert_one({"id_recipient": id_recipient[1:], \
                           "id_debtor": id_debtor, \
                           "description": description, \
                           "date_start": date_start, \
                           "date_end": date_end, "status": 'active'})

    await msg.answer(
        f"Кому должны: {id_recipient}\n"
        f"Должник: @{id_debtor}\n"
        f"Что должен: {description}\n"
        f"Остчет от {date_start} до {date_end}"
    )
    await msg.answer(
        "Выберите команду:",
        reply_markup=kb.get_kb_menu()
    )

@dp.message(F.text.lower() == "посмотреть должников")
async def extract_data(message: Message):
    query = {"id_recipient": message.chat.username, "status": "active"}
    for value in mongo_item.find(query, {"_id":0,"id_debtor": 1, "description":1, "status":1 }):
        await message.answer(f"@{value['id_debtor']} "
                             f"должен тебе {value['description']}\n"
                             f"Статус долга: {value['status']}")
    await message.answer(
        "Выберите команду:",
        reply_markup=kb.get_kb_menu()
    )


@dp.message(F.text.lower() == "посмотреть свои долги")
async def extract_data(message: Message):
    query = {"id_debtor": message.chat.username, "status": "active"}
    for value in mongo_item.find(query,{"_id":0,"id_recipient": 1, "description":1 }):
        await message.answer(f"Ты должен @{value['id_recipient']} "
                             f"{value['description']}")
    await message.answer(
        "Выберите команду:",
        reply_markup=kb.get_kb_menu()
    )

@dp.message(F.text.lower() == "изменить статус долга")
async def extract_data(message: Message):
    query = {"id_recipient": message.chat.username, "status": "active"}
    id=1
    for value in mongo_item.find(query,{"id_debtor": 1, "description":1 }):
        await message.answer(f"{id}."
                             f" @{value['id_debtor']} "
                             f"должен тебе {value['description']}")
        id+=1
    if id==1: await message.answer("Тебе вернули все долги)))")
    else:
        await message.answer("Введи /changestatus и номер долга, статус которого хочешь изменить")

@dp.message(Command("changestatus"))
async def cmd_settimer(
        message: Message,
        command: CommandObject
):
    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    # Пробуем разделить аргументы на две части по первому встречному пробелу
    try:
        status_id = command.args
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/changestatus <номер долга>"
        )
        return
    query = {"id_recipient": message.chat.username, "status": "active"}
    list = []
    for value in mongo_item.find(query, {"id_debtor": 1, "description": 1}):
        list.append(value['_id'])
    current ={"_id": list[int(status_id)-1]}
    new_data = {"$set": {"status": "done"}}
    mongo_item.update_one(current, new_data)
    await message.answer("Статус изменен")
    await message.answer(
        "Выберите команду:",
        reply_markup=kb.get_kb_menu()
    )


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())