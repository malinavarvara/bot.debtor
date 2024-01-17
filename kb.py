from aiogram import types

#import keyboards.kb_text as kb_text

def get_kb_menu():
    kb = [
        [
            types.KeyboardButton(text="Создать долг"),
            types.KeyboardButton(text="Создать свой долг"),
        ],
        [
            types.KeyboardButton(text="Посмотреть должников"),
            types.KeyboardButton(text="Посмотреть свои долги")
        ],
        [
            types.KeyboardButton(text="Изменить статус долга"),
            types.KeyboardButton(text="Инструкция")
        ]
    ]

    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
