from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import os
import json
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.settings import dp, Bot
import logging


channel_id = os.environ.get('CHANNEL_ID')
sheet_id = '1LE10RehEQPon2bcAvr3CnYmyZM3Np2EP8P5KF9ZcuPM'
logger = logging.getLogger(__name__)


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Привет!\nЯ автоматический обработчик заявлений в Республику.'
                         '\nЕсли хотите подать заявку, используйте команду: /start_application ',
                         reply_markup=types.ReplyKeyboardRemove()
                         )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


async def process_event(event, dp: Dispatcher):
    """
    Converting an Yandex.Cloud functions event to an update and
    handling tha update.
    """

    update = json.loads(event['body'])
    logger.debug('Update: ' + str(update))

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
        await register_handlers_common(dp)
        await process_event(event, dp)

        return {'statusCode': 200, 'body': 'ok'}
    return {'statusCode': 405}


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")

