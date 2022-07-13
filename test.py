"""
The Bot for applications - это сохранка работающего бота 2, который пишет в табличку
"""
import logging
from aiogram import Bot, Dispatcher, executor, types
import os
from sys import exit
import json

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from app.creds.constants import SHEET_ID

TOKEN2 = 'test'
bot = Bot(TOKEN2)
dp = Dispatcher(bot)

channel_id = os.environ.get('CHANNEL_ID')

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def get_service_sacc():
    """
    Могу читать и (возможно) писать в таблицы кот. выдан доступ
    для сервисного аккаунта приложения
    sacc-1@privet-yotube-azzrael-code.iam.gserviceaccount.com
    :return:
    """
    creds_json = os.path.dirname(__file__) + "/creds/creds.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


sheet = get_service_sacc().spreadsheets()


# Handlers
@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.reply('Привет!\nМеня зовут Аплик, и я переадресую твою заявку, куда следует ;)'
                        '\nТебе нужно просто написать в ответном сообщении свою заявку :) ')



'''@dp.message_handler()
async def all_msg_handler(message: types.Message):
    user = message.from_user.username
    button_text = f'Нам пишет: @{user}\nЕго заявка: \n{message.text}'
    log.debug('The answer is %r', button_text)

    reply_text = 'Спасибо за твою заявку! Я всё передал!'

    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(channel_id, button_text)'''

@dp.message_handler()
async def echo(message: types.Message):
    user = message.from_user.username
    button_text = f'Нам пишет: @{user}\nЕго сообщение: \n{message.text}'
    log.debug('The answer is %r', button_text)
    values = [[f'@{user}', message.text]]

    resp = sheet.values().append(
        spreadsheetId=SHEET_ID,
        range="Лист1!A1",
        valueInputOption="RAW",
        body={'values': values}).execute()

    reply_text = 'Спасибо за твою заявку! Я всё передал!'

    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(channel_id, button_text)
    '''await message.answer(message.text)'''


# Functions for Yandex.Cloud
#@dp.message_handler()
async def register_handlers(dp: Dispatcher):
    """Registration all handlers before processing update."""

    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(echo)

    log.debug('Handlers are registered.')


#@dp.message_handler()
async def process_event(event, dp: Dispatcher):
    """
    Converting an Yandex.Cloud functions event to an update and
    handling tha update.
    """

    update = json.loads(event['body'])
    log.debug('Update: ' + str(update))

    Bot.set_current(dp.bot)
    update = types.Update.to_object(update)
    await dp.process_update(update)


#@dp.message_handler()
async def handler(event, context):
    """Yandex.Cloud functions handler."""

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
