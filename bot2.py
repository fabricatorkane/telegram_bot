"""
The Bot for applications
"""
import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit
from app.creds.constants import CHANNEL_ID

bot_token = getenv("TOKEN2")
if not bot_token:
    exit("Error: no token provided")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# инициализируем бота
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    '/start' or '/help'
    """
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)    # кнопки, resize_keyboard - чтоб кнопка была компактной
    '''btns_text = ('Да!', 'Нет!')    # это те кнопки, которые будет показывать бот
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))'''    # row - наши кнопки в ряд, мы их перебираем
    user = message.from_user.username

    await message.reply('Привет!\nМеня зовут Аплик, и я переадресую твою заявку, куда следует ;)'
                        '\nТебе нужно просто написать в ответном сообщении свою заявку :) ')
    '''await message.answer('Это твой ник? @' + f'{user}', reply_markup=keyboard_markup)'''    # reply_markup - привязываем клавиатуру


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    user = message.from_user.username
    button_text = f'Нам пишет: @{user}\nЕго заявка: \n{message.text}'
    logger.debug('The answer is %r', button_text)

    '''if button_text == 'Да!':
        reply_text = 'Крутяк!'

    elif button_text == 'Нет!':
        reply_text = 'Ну и оки'

    else:
        reply_text = 'Я вас не понял'''
    reply_text = 'Спасибо за твою заявку! Я всё передал!'

    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(CHANNEL_ID, button_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
