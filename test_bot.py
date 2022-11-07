import time
import logging

from aiogram import Bot, Dispatcher, executor, types

#библиотеки для всплывающих кнопок
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import FSMContext #FSM
from aiogram.dispatcher.filters import Command #FSM
from aiogram.contrib.fsm_storage.memory import MemoryStorage   #FSM
from aiogram.dispatcher.filters.state import StatesGroup, State #FSM

from aiogram.utils.executor import start_webhook
import os

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage() #FSM


TOKEN = '5705218954:AAGhWEtoNR6oLeZoYiXczF_NHydP91-zhzk'

bot= Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=storage)

#--HEROKU---------------------------------------------------------------------------------------------------
#https://newtechaudit.ru/asinhronnyj-telegram-bot-s-vebhukami-na-heroku/

HEROKU_APP_NAME = os.getenv('apr-test-bot') #переименовать
# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(dispatcher):
    await bot.delete_webhook()


#--------КНОПКИ-----------------------------------------------------------------------------------------
#постоянная кнопка запуска
button_start = KeyboardButton('Начать')
zayavka = KeyboardButton('Оставить заявку')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start, zayavka)

#кнопка телефона
markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свой контакт ☎️', request_contact=True))

#инлайн клавиатура
#вернуться назад
back1 = InlineKeyboardButton('Назад', callback_data='back')
back2 = InlineKeyboardButton('Вернуться в раздел задач', callback_data='back_task')
back3 = InlineKeyboardButton('Вернуться в основной каталог', callback_data='back_catal')
total_back = InlineKeyboardMarkup(row_width=2).add(back2)
total_back_catal = InlineKeyboardMarkup(row_width=2).add(back3)

#Главное меню
tasks = InlineKeyboardButton('Задачи',callback_data='menu1')
lids = InlineKeyboardButton('Лиды',callback_data='menu2')
cards = InlineKeyboardButton('Карточки',callback_data='menu3')
deals = InlineKeyboardButton('Сделки',callback_data='menu4')
offers = InlineKeyboardButton('Предложения',callback_data='menu5')
main_menu = InlineKeyboardMarkup(row_width=2).add(tasks,lids,cards,deals,offers,back1)

#Разделы Задач
inline_btn_1 = InlineKeyboardButton('Открытие портала', callback_data='btn1')
open1 = InlineKeyboardButton('Баллы НМО под ключ', callback_data='op1')
open2 = InlineKeyboardButton('Баллы НМО самозапись', callback_data='op2')
open3 = InlineKeyboardButton('Док.сопровождение', callback_data='op3')
open4 = InlineKeyboardButton('ПК или ПП', callback_data='op4')
open_all = InlineKeyboardMarkup(row_width=2).add(open1,open2,open3,open4, back2)

inline_btn_2=InlineKeyboardButton('Выпуск документов', callback_data='btn2')
vipusk1 = InlineKeyboardButton('ПП2019', callback_data='vp1')
vipusk2 = InlineKeyboardButton('ПК2022', callback_data='vp2')
vipusk_all = InlineKeyboardMarkup(row_width=2).add(vipusk1,vipusk2, back2)

inline_btn_3=InlineKeyboardButton('Отправка документов', callback_data='btn3')

inline_btn_4=InlineKeyboardButton('Шаблон заявок', callback_data='btn4')
shablon1=InlineKeyboardButton('НМО под ключ', callback_data='shb1')
shablon2=InlineKeyboardButton('Заявка на выпуск', callback_data='shb2')
shablon3=InlineKeyboardButton('Заявка на рабочку', callback_data='shb3')
shablon_all=InlineKeyboardMarkup(row_width=2).add(shablon1, shablon2, shablon3, back2)

start_all = InlineKeyboardMarkup(row_width=2).add(inline_btn_1,inline_btn_2, \
    inline_btn_3, inline_btn_4, back1)

#длинные ответы бота----------------------------------------------------------------------------------------------------------
HI = "Привет! Это тестовый бот для Академии. \
    Здесь можно будет найти всю информацию касаемо работы в Битриксе, \
        полезных ссылок в новостной ленте, а так же многое другое.\
            Для работы с ботом нажми кнопку 'Начать'. Если хочешь протестировать работу заявки и скорость ее обработки \
                нажми 'Оставить заявку'. Приятного изучения!"

OTPRAVKA = "Для того, чтобы отправить документы необходимо перейди в сделку в раздел 'Реестр отправок' и \
    и создать новую заявку. Подробная инструкция опубликованна в новостной ленте Битрикса \
        Но вот на всякий случай полезная ссылка на пост: https://apr77.bitrix24.ru/company/personal/user/37/blog/433/"

start_text = "Привет! Давай начнем"

ERROR = "Упс! Здесь идут ремонтные работы"

#--ЗАПРОСЫ----------------------------------------------------------------------------------------#
@dp.message_handler(commands=['start'], state=None)
async def buttuon_start_key(message: types.Message):
#    joinedFile = open("user.txt","a") #запись ID при обращении
#    joinedFile.write(str(message.chat.id)+"\n")
#    joinedUsers=set().add(message.chat.id)
    await message.reply(text=HI, reply_markup=greet_kb, parse_mode='Markdown')

@dp.message_handler(lambda message: message.text == "Начать")
async def pin(message: types.Message):
    await message.answer(text='Переходим в каталог',reply_markup=main_menu)

#вернуться в раздел задач
@dp.callback_query_handler(text="back")
async def back_ccat(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text=start_text, reply_markup=main_menu)

#вернуться в раздел каталога
@dp.callback_query_handler(text="back_catal")
async def back_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Основной каталог разделов', reply_markup=main_menu)

#перечень разделов
@dp.callback_query_handler(text="modle")#text=callback_data
async def modle(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text='По какому разделу вопрос?', reply_markup=main_menu)

#перечень Лиды
@dp.callback_query_handler(text="menu2")#text=callback_data
async def lids1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=total_back_catal)

#перечень Карточки
@dp.callback_query_handler(text="menu3")#text=callback_data
async def cards1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=total_back_catal)

#перечень Сделки
@dp.callback_query_handler(text="menu4")#text=callback_data
async def deals1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=total_back_catal)    

#перечень Предложения
@dp.callback_query_handler(text="menu5")#text=callback_data
async def offes1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=total_back_catal)  

#перечень Задачи
@dp.callback_query_handler(text="menu1")#text=callback_data
async def task1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text="Какая задача интересует?", reply_markup=start_all)

#открытие портала
@dp.callback_query_handler(text="btn1")#text=callback_data
async def btn1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text="По какому направлению проходит обучение?", reply_markup=open_all)
#открытие Баллы НМО под ключ
@dp.callback_query_handler(text="op1")#text=callback_data
async def opp1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=open_all)  
#открытие Баллы НМО самозапись
@dp.callback_query_handler(text="op2")#text=callback_data
async def opp2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=open_all)  
#открытие Док.сопровождение
@dp.callback_query_handler(text="op3")#text=callback_data
async def opp3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=open_all)  
#открытие ПК или ПП
@dp.callback_query_handler(text="op4")#text=callback_data
async def opp4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=open_all)  

#вернуться в разделы задач
@dp.callback_query_handler(text="back_task")
async def back_callback_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Разделы Задач', reply_markup=start_all)

#выпуск документов
@dp.callback_query_handler(text="btn2")#text=callback_data
async def btn2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text="Какие документы выпускаем?", reply_markup=vipusk_all)
#выпуск ПП2019
@dp.callback_query_handler(text="vp1")#text=callback_data
async def vpp1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=vipusk_all)  
#выпуск ПК2022
@dp.callback_query_handler(text="vp2")#text=callback_data
async def vpp2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=ERROR, reply_markup=vipusk_all)  

#отправка документов
@dp.callback_query_handler(text="btn3")#text=callback_data
async def btn3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=OTPRAVKA, reply_markup=total_back)

#шаблон заявок
@dp.callback_query_handler(text="btn4")#text=callback_data
async def btn4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text='Какой шаблон нужен? Будет ссылка', reply_markup=shablon_all)
#шаблон НМО под ключ
@dp.callback_query_handler(text="shb1")#text=callback_data
async def shbb1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text='Ссылка на шаблон заявки: в разработке', reply_markup=shablon_all)
#шаблон Заявка на выпуск
@dp.callback_query_handler(text="shb2")#text=callback_data
async def shbb2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text='Ссылка на шаблон заявки: в разработке', reply_markup=shablon_all)
#шаблон Заявка на рабочку
@dp.callback_query_handler(text="shb3")#text=callback_data
async def shbb3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text='Ссылка на шаблон заявки: в разработке', reply_markup=shablon_all)

#отправка уведомлений о связи с оператором---------------------------------------------------------------------------------
#Через кнопку
@dp.message_handler(lambda message: message.text == "Оставить заявку")
async def zvk(message: types.Message):
    await message.answer(text='Напишите ваш вопрос в чат',
    reply_markup=markup_request)

#Перессылка сообщения в другой чат
@dp.message_handler(content_types=["text"])
async def sand_message(message: types.Message):
    bot_chat_id = message.chat.id
    group_id = 394221139 # id группы в которую должны приходить сообщения
    await bot.forward_message(group_id, bot_chat_id, message.message_id)
    answer = 'Ваш запрос получен. Пожалуйста оставьте свой номер телефона, чтобы мы могли связаться с вами'
    await bot.send_message(message.from_user.id, answer, reply_markup=markup_request)

#Перессылка сообщения в другой чат
@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    if message.contact is not None: #Если присланный объект не равен нулю
        text = 'Новый запрос от: ' + message.contact.full_name + '. телефон: ' + message.contact.phone_number #+ вопрос от клиента
        await bot.send_message(394221139, text) #тут указать ID получателя заявки. Сейчас ID моего канала. Тестирую 
        await message.answer(text="Спасибо за заявку. В скором времени менеджер с вами свяжется", reply_markup=greet_kb)

#сохранение логов в базу данных---------------------------------------------------------------------------------------------------


#запуск работы
if __name__ == '__main__':
    executor.start_polling(dp) #для терминала

    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        )