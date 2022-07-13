from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.settings import dp, bot, channel_id
from app.write_out_to_googlesheet import write_out_to_googlesheet


sheet_id = '1LE10RehEQPon2bcAvr3CnYmyZM3Np2EP8P5KF9ZcuPM'
available_finish = ['Да', 'Нет']


class OrderFood(StatesGroup):
    waiting_for_name = State()
    waiting_for_application = State()
    waiting_for_finishing = State()


async def start_application(message: types.Message):
    await message.answer('Для начала напишите, пожалуйста, Ваше имя:')
    await OrderFood.waiting_for_name.set()


# Обратите внимание: есть второй аргумент
async def wrtiting_name(message: types.Message, state: FSMContext):
    '''if message.text.lower() not in available_food_names:
        await message.answer("Пожалуйста, выберите блюдо, используя клавиатуру ниже.")
        return'''
    await state.update_data(user_name=message.text)    # сохранить полученный текст в хранилище данных FSM, это словарь, поэтому воспользуемся функцией update_data() и сохраним текст сообщения под ключом chosen_food и со значением message.text.lower()

    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await OrderFood.next()    # тут переводим пользователя на следующий шаг
    await message.answer("Следующим шагом оставьте, пожалуйста, текст вашей заявки:")


async def wrtiting_application(message: types.Message, state: FSMContext):
    '''if message.text.lower() not in available_food_names:
        await message.answer("Пожалуйста, выберите блюдо, используя клавиатуру ниже.")
        return'''
    await state.update_data(user_application=message.text)    # сохранить полученный текст в хранилище данных FSM, это словарь, поэтому воспользуемся функцией update_data() и сохраним текст сообщения под ключом chosen_food и со значением message.text.lower()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_finish:
        keyboard.add(size)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await OrderFood.next()    # тут переводим пользователя на следующий шаг
    user_data = await state.get_data()
    await message.answer(f'Вы закончили формировать заявку, она выглядит так:'
                         f'\n<b><u>Ваше имя</u></b>: {user_data["user_name"]} \n<b><u>Ваша заявка</u></b>: {user_data["user_application"]}.'
                         f'\n\nЯ могу её отправить?', reply_markup=keyboard)


async def finish_application(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_data = await state.get_data()
    print(user_data)
    user = '@' + message.from_user.username
    values = f'<b>К нам обратился новый заявитель</b>:' \
             f'\n\n<u>Связь с заявителем</u>: {user} \n<u>Имя заявителя</u>: {user_data["user_name"]} ' \
             f'\n<u>Заявка заявителя</u>: {user_data["user_application"]}.'
    for size in available_finish:
        keyboard.add(size)
    if message.text.lower() == 'да':
        user_data = await state.get_data()
        await bot.send_message(channel_id, values)
        write_out_to_googlesheet(user_data, user)
        await message.answer(f"Заявка отправлена! Спасибо, с Вами свяжутся!", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer(f"Если хотите отменить, используйте команду /cancel",
                             reply_markup=types.ReplyKeyboardRemove())

    else:
        await message.answer('Вы закончили формировать заявку, я могу её отправить?', reply_markup=keyboard)
        return


def register_handlers_application(dp: Dispatcher):
    dp.register_message_handler(start_application, commands='start_application', state="*")
    dp.register_message_handler(wrtiting_name, state=OrderFood.waiting_for_name)
    dp.register_message_handler(wrtiting_application, state=OrderFood.waiting_for_application)
    dp.register_message_handler(finish_application, state=OrderFood.waiting_for_finishing)

