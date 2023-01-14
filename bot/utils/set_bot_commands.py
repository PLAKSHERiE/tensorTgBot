from aiogram import types


COMMANDS = [
    '/start',
    '/help',
]


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand(COMMANDS[0], "Запустить бота"),
            # types.BotCommand(COMMANDS[1], "Вывести справку"),
        ]
    )
