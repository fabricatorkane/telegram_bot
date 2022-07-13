"""
The Bot for applications - это сохранка работающего бота 2, который пишет в табличку
"""
import asyncio
import logging

from aiogram import Bot, executor
from aiogram.types import BotCommand

from app.handlers.apply import register_handlers_application
from app.handlers.common import register_handlers_common
from app.settings import dp, bot


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Написать в галактическую республику"),
        BotCommand(command="/start_application", description="Подать заявку"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_application(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()
    #await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())










"""

def get_service_sacc():
    '''
    Могу читать и (возможно) писать в таблицы кот. выдан доступ
    для сервисного аккаунта приложения
    sacc-1@privet-yotube-azzrael-code.iam.gserviceaccount.com
    '''
    creds_json = os.path.dirname(__file__) + "/creds/creds.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    '''return build('sheets', 'v4', http=creds_service)''' - раскомментить!! чо-то пайчарм гурался


sheet = get_service_sacc().spreadsheets()


# Handlers
@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.reply('Привет!\nМеня зовут Аплик, и я переадресую твою заявку, куда следует ;)'
                        '\nТебе нужно просто написать в ответном сообщении свою заявку :) ')


@dp.message_handler(commands='stop')
async def stop(message: types.Message):

    resp = sheet.values().append(
        spreadsheetId=sheet_id,
        range="Лист1!A1",
        valueInputOption="RAW",
        body={'values': [values]}).execute()
    await bot.send_message(channel_id, values)


@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(random.randint(1, 10)))


@dp.message_handler()
async def echo(message: types.Message):
    user = '@' + message.from_user.username
    user_text = message.text
    values.append(user)
    values.append(user_text)
    button_text = values #f'Нам пишет: @{user}\nЕго сообщение: \n{message.text}'
    log.debug('The answer is %r', button_text)

    reply_text = 'Спасибо за информацию, если хочешь закончить формирование заявки, выбири команду /stop'

    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())
    '''await message.answer(message.text)'''



# Functions for Yandex.Cloud
#@dp.message_handler()
async def register_handlers(dp: Dispatcher):
    '''Registration all handlers before processing update.'''

    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(echo)

    log.debug('Handlers are registered.')


#@dp.message_handler()
async def process_event(event, dp: Dispatcher):
    '''
    Converting an Yandex.Cloud functions event to an update and
    handling tha update.
    '''

    update = json.loads(event['body'])
    log.debug('Update: ' + str(update))

    Bot.set_current(dp.bot)
    update = types.Update.to_object(update)
    await dp.process_update(update)


#@dp.message_handler()
async def handler(event, context):
    '''Yandex.Cloud functions handler.'''

    if event['httpMethod'] == 'POST':
        # Bot and dispatcher initialization
        '''bot = Bot(os.environ.get('TOKEN2'))
        dp = Dispatcher(bot)'''
        await register_handlers(dp)
        await process_event(event, dp)

        return {'statusCode': 200, 'body': 'ok'}
    return {'statusCode': 405}


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
"""