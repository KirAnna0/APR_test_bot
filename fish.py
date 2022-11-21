from datetime import datetime
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
admin_id = 394221139

#--HEROKU---------------------------------------------------------------------------------------------------
#https://newtechaudit.ru/asinhronnyj-telegram-bot-s-vebhukami-na-heroku/

HEROKU_APP_NAME = os.getenv('apr-test-bot') #переименовать

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT',default=5000)

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(dispatcher):
    await bot.delete_webhook()

#<<<<<<<<<  КНОПКИ  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
start = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('🏠 Главное меню', callback_data='start'))

#стартовое меню
study = InlineKeyboardButton('🧑‍⚕️ Блок: Обучение медиков', callback_data='study_med')
problems = InlineKeyboardButton('📃 Блок: Проблемы с документами', callback_data='problems_dok')
category = InlineKeyboardButton('🎓 Блок: Категория', callback_data='category_dok')
question = InlineKeyboardButton('❓ Блок: Напишите свой вопрос', callback_data='your_quest')
menu = InlineKeyboardMarkup(row_width=1).add(study,problems,category,question)

#БЛОК 1: Обучение медиков  #готов
pk_btn = InlineKeyboardButton('Блок: ПК', callback_data='pk_med')
pp_btn = InlineKeyboardButton('Блок: ПП', callback_data='pp_med')
nmo_btn = InlineKeyboardButton('Блок: НМО', callback_data='nmo_med')
accre_btn = InlineKeyboardButton('Блок: Аккредитация', callback_data='accred_med')
study_main_m = InlineKeyboardMarkup(row_width=1).add(pk_btn, pp_btn, nmo_btn, accre_btn)
#ПК. подраздел. Для чего проходят ПК
for_accred = InlineKeyboardButton('Для прохождения аккредитации', callback_data='for_acc')
for_prodlen = InlineKeyboardButton('С целью продлить сертификат', callback_data='for_prod')
for_prosroch = InlineKeyboardButton('У меня просрочен сертификат', callback_data='for_pros')
for_menu = InlineKeyboardMarkup(row_width=1).add(for_accred, for_prodlen, for_prosroch)
#ПП. подраздел. Для чего проходят ПП
pp_smp = InlineKeyboardButton('Среднее профессиональное образование', callback_data='pp_smp_med')
pp_vmp = InlineKeyboardButton('Высшее образование', callback_data='pp_vmp_med')
pp_for_menu = InlineKeyboardMarkup(row_width=1).add(pp_smp, pp_vmp)
#Аккредитация. подразделы
accred_btn_first = InlineKeyboardButton('Первичная аккредитация', callback_data='first_accred')
accred_btn_reply = InlineKeyboardButton('Периодическая аккредитация', callback_data='reply_accred')
accred_btn_spec_first = InlineKeyboardButton('Первичная специализированная', callback_data='spec_accred')
accred_menu = InlineKeyboardMarkup(row_width=1).add(accred_btn_first, accred_btn_reply,accred_btn_spec_first)

#БЛОК 2: Проблемы с документами
delay = InlineKeyboardButton('Просрочен сертификат. Что делать?', callback_data='delay_sert')
foreign_dok = InlineKeyboardButton('У меня иностранные документы об образовании. Что делать?', callback_data='foreign')
pause_work = InlineKeyboardButton('У меня перерыв в стаже. Не работал. Что делать?', callback_data='pause')
not_end = InlineKeyboardButton('Неоконченное образование. Что делать?', callback_data='not_edu')
problem_menu = InlineKeyboardMarkup(row_width=1).add(delay, foreign_dok, pause_work, not_end)
#Подраздел неоконченное образование
no_ed_y_n = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Да, я получил(а) серт', callback_data='yes_sert'), 
InlineKeyboardButton('Нет, не получал(а)', callback_data='no_sert'))
ordinature = InlineKeyboardButton('Высшее - интернатура/ординатура', callback_data='ordinat')
specialitet = InlineKeyboardButton('Высшее - специалитет', callback_data='specialit')
srednee = InlineKeyboardButton('Среднее профессиональное', callback_data='sred')
level_edu = InlineKeyboardMarkup(row_width=1).add(ordinature, specialitet, srednee)

#БЛОК 3: КАТЕГОРИИ
cat_yes = InlineKeyboardButton('Да, есть категория', callback_data='cat_yes')
cat_no = InlineKeyboardButton('Нет, категории не имею', callback_data='cat_no')
categ_y_n = InlineKeyboardMarkup(row_width=2).add(cat_yes, cat_no)
level_cat = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Первая категория', callback_data='1_cat'), 
InlineKeyboardButton('Вторая категория', callback_data='2_cat'), 
InlineKeyboardButton('Высшая категория', callback_data='3_cat'))
ex_work = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('До 3-ех лет', callback_data='less_3'), 
InlineKeyboardButton('Более 3-ех лет', callback_data='more_3'))

#Другие кнопки

back = InlineKeyboardButton('🔙 Вернуться в меню', callback_data='go_back')
go_accred = InlineKeyboardButton('🔜 Перейти в блок Аккредитации', callback_data='go_accred')
else_question = InlineKeyboardButton('❓ Все еще есть вопросы?', callback_data='else_question')
request_bnt_2 = InlineKeyboardButton('Оставить заявку', callback_data='send_text')

end_btn = InlineKeyboardMarkup(row_width=2).add(back, else_question)
end_btn_2 = InlineKeyboardMarkup(row_width=2).add(back, go_accred, else_question)
end_btn_3 = InlineKeyboardMarkup(row_width=2).add(back, request_bnt_2)
end_btn_4 = InlineKeyboardMarkup(row_width=2).add(back)
request_bnt_3 = InlineKeyboardMarkup(row_width=2).add(request_bnt_2)
end_btn_5 = InlineKeyboardMarkup(row_width=2).add(back, delay)
end_btn_6= InlineKeyboardMarkup(row_width=2).add(back, delay, else_question)

#кнопки-ссылки
rmapo_url = InlineKeyboardMarkup(row_width=1).add(back,InlineKeyboardButton('Расписание на сайте РМАПО', url='https://rmapo.ru/akkreditacija/pervichnaya-specializirovannaya-akkreditaciya/9551-pervichnaja-specializirovannaja-akkreditacija.html'))

#Подсказки
promp_1 = InlineKeyboardButton('Где посмотреть баллы НМО?', callback_data='promp_1')

#Оставить свою заявку
request_bnt = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Оставить заявку'))
contact = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('☎️ Отправить свой контакт', request_contact=True)) 

#<<<<<<<<<  ПЕРЕМЕННЫЕ СОСТОЯНИЯ  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class ProfilestatesGroup(StatesGroup):
    zapros = State()
    telefon = State()
    name = State()
    year = State()
    ball_250= State()
    ball_144= State()
    year_delay = State()
#<<<<<<<<<  АЛГОРИТМ  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Первый запуск бота, приветственное слово
HI = "Привет! Это бот от УЦ 'Академия профессионального развития'. \
    Здесь Вы можете найти всю полезную информацию по обучению медиков. От НМО до Аккредитации \
    Для того, чтобы приступить к работе нажмите 'Главное меню'"
@dp.message_handler(commands=['start'], state=None)
async def button_start_key(message: types.Message):
    await message.reply(text=HI, reply_markup=start)

#Реакция на кнопку Начать, всплытие меню основных разделов
MAIN_STAGES_TEXT = "Какой раздел вас интересует? Блок обучение медиков: ПК, ПП, НМО, аккредитация. \
    Блок проблем с документами: просрочка, иностранные доки, перерыв в стаже. \
    Блок Категория. Или напишите нам свой вопрос - мы вам ответим"
@dp.callback_query_handler(text = "start")
async def main_stage(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=MAIN_STAGES_TEXT, reply_markup=menu)

#реакция на закрытие раздела
YES_QUESTION = 'Если у вас все еще остались вопросы, можете оставить заявку и наш менеджер вам перезвонит'
@dp.callback_query_handler(text = "else_question")
async def ent_answer(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)    
    await bot.send_message(callback_query.from_user.id, text=YES_QUESTION, reply_markup=end_btn_3)

#БЛОК 1. ОБУЧЕНИЕ МЕДИКОВ----------------------------------------------------------------------------------------------------------
#Реакция на кнопку 'Блок: Обучение медиков', всплытие подразделов
@dp.callback_query_handler(text="study_med")
async def study_menu(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Что интересует: ПП, ПК, НМО, акрредитация?', reply_markup=study_main_m)

#Реакция на кнопку подраздел 'ПК', всплытие подразделов
@dp.callback_query_handler(text="pk_med")
async def pk_menu(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='С какой целью хотите пройти обучение?', reply_markup=for_menu)     # скрываем предыдущий текст + кнопки
#реакции на подразделы меню ПК
@dp.callback_query_handler(text="for_acc")
async def for_accreditation(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Вам нужно перейти в раздел аккред. Переход в аккред', reply_markup=end_btn_2)   
@dp.callback_query_handler(text="for_prod")
async def for_prodlenie(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Какой-то инфо текст про ПРОДЛЕНИЕ. Переход в аккред', reply_markup=end_btn_2) 
@dp.callback_query_handler(text="for_pros")
async def for_prosrochki(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Какой-то инфо текст для ПРОСРОЧКИ сертификатов ', reply_markup=end_btn_5)   

#Реакция на кнопку подраздел 'ПП', всплытие подразделов
@dp.callback_query_handler(text="pp_med")
async def pp_menu(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Ваш уровень образования?', reply_markup=pp_for_menu)  
#реакции на подразделы меню ПП
INFO_TEXT_1 = 'Инфо текст про то, как посмотреть на какую специальность можно переучится. Ссылка на приказ: https://docs.cntd.ru/document/420339191'
INFO_TEXT_2 = 'Инфо текст про то, как посмотреть на какую специальность можно переучится. Ссылка на приказ: http://ivo.garant.ru/#/document/71231064/paragraph/13:0'
@dp.callback_query_handler(text="pp_smp_med")
async def otv_smp(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_1, reply_markup=end_btn) 
@dp.callback_query_handler(text="pp_vmp_med")
async def otv_vmp(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_2, reply_markup=end_btn) 

#реакция на Блок: Аккредитация, всплытие подразделов
INFO_TEXT_3 = 'Описание что такое аккредитация. В каких случаях какую надо проходить. И конечный вопрос: Какая аккредитация вас интересует?'
INFO_TEXT_5 = 'какой-то там инфо текст про расписание. \
    Полезная ссылка на сайт РМАПО:https://rmapo.ru/akkreditacija/pervichnaya-specializirovannaya-akkreditaciya/9551-pervichnaja-specializirovannaja-akkreditacija.html'
@dp.callback_query_handler(text='accred_med')
async def accreditation(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_3, reply_markup=accred_menu) 
#реакции на подразделы меню Аккредитации
INFO_TEXT_4='Для получения первичной аккредитации обратитесь в то учебное учреждение, где было получено базовое образование (колледж / специалитет)'
@dp.callback_query_handler(text="first_accred")
async def otv_first_ac(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_4, reply_markup=end_btn) 
@dp.callback_query_handler(text="reply_accred")
async def otv_rep_acc(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Какой-то инфо текст про то, что нужны баллы', reply_markup=calculate_nmo)  

@dp.callback_query_handler(text="spec_accred")
async def otv_first_spec_ac(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_5, reply_markup=rmapo_url)
#БЛОК. Калькулятор баллов НМО----------------------------------------------------------------------------------------------------
#кнопки
calk_nmo = InlineKeyboardButton('🧮 Калькулятор баллов', callback_data='calculate_nmo')
calculate_nmo = InlineKeyboardMarkup(row_width=2).add(calk_nmo)
one_more= InlineKeyboardMarkup(row_width=2).add(calk_nmo, back)

before_mart = InlineKeyboardButton('Выдан до марта: январь, февраль', callback_data='b_mart')
after_mart = InlineKeyboardButton('Выдан после марта: март-декабрь', callback_data='a_mart')
mart = InlineKeyboardMarkup(row_width=1).add(before_mart, after_mart)
yes = InlineKeyboardButton('Да, копил(а)', callback_data='yes')
no = InlineKeyboardButton('Нет, не копил(а)', callback_data='no')
yes_no = InlineKeyboardMarkup(row_width=2).add(yes, no, promp_1)
yes_2 = InlineKeyboardButton('Да, копил(а)', callback_data='yes_2')
no_2 = InlineKeyboardButton('Нет, не копил(а)', callback_data='no_2')
yes_no_2 = InlineKeyboardMarkup(row_width=2).add(yes_2, no_2, promp_1)

#реакция на Блок: НМО
@dp.callback_query_handler(text="nmo_med")
async def nmo(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Что такое НМО и с чем его едят.Далее переход на калькулятор. Нажми кнопку', reply_markup=calculate_nmo)
@dp.callback_query_handler(text="calculate_nmo")
async def nmo1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text='Год выпуска сертификата?')
    await ProfilestatesGroup.year.set()
#сохраняем год выпуска и спрашиваем про март
@dp.message_handler(state=ProfilestatesGroup.year)
async def spec(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['year']=int(message.text)
    num_y = 5 + data['year'] #год, когда заканчивается серт у клиента
    start_year = datetime.now().year - 5 #год начала перед просрочкой
    if data['year'] < start_year:
        await message.answer('Ваш сертификат уже просрочился. Вам необходимо его продлить', reply_markup=end_btn_6)
    else:
        if num_y <= 2023:
            await message.answer('Месяц выдачи сертификата: до марта или после?', reply_markup=mart)
        else:
            await message.answer('Копили ли вы баллы НМО?', reply_markup=yes_no_2)
    await state.finish()

#ответы про март. ДО
@dp.callback_query_handler(text=("b_mart"))
async def nmo2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Копили ли вы баллы НМО?', reply_markup=yes_no)
#Да, копили баллы про 144ч
@dp.callback_query_handler(text="yes")
async def nmo3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Сколько баллов было набрано?')
    await ProfilestatesGroup.ball_144.set()
#считаем баллы
@dp.message_handler(state=ProfilestatesGroup.ball_144)
async def nmo4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ball_144']=int(message.text) 
    if data['ball_144'] >= 144:
        await message.answer('Вы набрали достаточное кол-во баллов для прохождения аккредитации', reply_markup=end_btn)
    else:
        num4= 144 - data['ball_144']
        await message.answer(f'Вам осталось набрать {num4} балл(а/ов) до 144ч')
    await state.finish()
    await message.answer('Повторно просчитать баллы?', reply_markup=one_more)
#Нет, не копили
@dp.callback_query_handler(text="no")
async def nmo5(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text='Тогда вам необходимо пройти пк на 144ч', reply_markup=end_btn)

#ответы про март. ПОСЛЕ
@dp.callback_query_handler(text=("a_mart"))
async def nmo2_1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Копили ли вы баллы НМО?', reply_markup=yes_no_2)
#Да, копили баллы про 250ч
@dp.callback_query_handler(text="yes_2")
async def nmo7(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Сколько баллов вы набрали?') #разные текстовки!
    await ProfilestatesGroup.ball_250.set()
#считаем баллы
@dp.message_handler(state=ProfilestatesGroup.ball_250)
async def nmo8(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ball_250']=int(message.text) 
    if data['ball_250'] >= 250:
        await message.answer ('Вы набрали достаточное кол-во баллов', reply_markup=end_btn)
    else:
        num5 = 250 - data['ball_250']
        await message.answer(f'Вам осталось набрать {num5} балл(а/ов) до 250ч')
    await state.finish()
    await message.answer('Повторно просчитать баллы?', reply_markup=one_more)
#Нет, не копили
@dp.callback_query_handler(text="no_2")
async def nmo9(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text='Нужно копить. Вот тебе инфо.... ', reply_markup=end_btn)

#БЛОК 2. ПРОБЛЕМЫ С ДОКУМЕНТАМИ---------------------------------------------------------------------------------------------------
#реакция на блок
@dp.callback_query_handler(text='problems_dok')
async def problem_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Какая у вас проблема?', reply_markup=problem_menu) 
#реакция на просрочку сертификата -- тоже самое, что и перерыв в стаже ???
@dp.callback_query_handler(text='delay_sert')
async def delay_sert_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Вот тут надо что-то прописать. У меня стоит алгоритм на просчет даты получения серта, но не понятно зачем он', reply_markup=end_btn_2) #ПЕРЕХОД НА АККРЕДИТАЦИЮ
#реакция на иностранные документы
@dp.callback_query_handler(text='foreign')
async def foreign_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Здесь короткое описание того, что надо делать в этом случае и ссылка на наш сайт. Не нашла ее на нашем сайте', reply_markup=end_btn)

#реакция на неоконченное образование
@dp.callback_query_handler(text='not_edu')
async def not_edu_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Есть ли сертификат или свидетельство на руках?', reply_markup=no_ed_y_n)
#реакция на подраздел. ДА
@dp.callback_query_handler(text='yes_sert')
async def not_btn1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Какой у вас уровень образования?', reply_markup=level_edu)      
#реакция на подраздел после да. высшее и среднее образование
@dp.callback_query_handler(text=('ordinat','sred'))
async def not_btn2(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='У вас на руках должны быть актуальные сертификаты или свидетельства. Вы можете проходить любое обучение', reply_markup=end_btn)     
#реакция на подраздел после да. специалитет высшее + ответ нет
@dp.callback_query_handler(text=('no_sert','specialit'))
async def not_btn3(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Вам необходимо обратиться в то учреждение, где вы заканчивали обучение', reply_markup=end_btn)  

#реакция на перерыв в стаже КАЛЬКУЛЯТОР ПЕРЕРЫВА-------------------------------------------------------------------------------------------------------------------
#кнопки
y_n_3= InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Да, работал(а)', callback_data='y_work'), 
InlineKeyboardButton('Нет, не работал(а)', callback_data='n_work'))

@dp.callback_query_handler(text=('pause','delay_sert'))
async def pause_bnt(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text='Укажите год получения последнего сертификата')
    await ProfilestatesGroup.year_delay.set()

#сохраняем год выпуска и спрашиваем про стаж
@dp.message_handler(state=ProfilestatesGroup.year_delay)
async def year_del(message: types.Message, state: FSMContext):
    async with state.proxy() as delay_sert_1:
        delay_sert_1['year_delay']=int(message.text)
    pause_year = delay_sert_1['year_delay'] + 10 
    if pause_year < datetime.now().year:
        await message.answer('Вам нужно пройти ПП и пойти на Первичную Специализированную аккредитацию', reply_markup=end_btn_2)
    else:
        await message.answer('Работали ли вы по специальности сертификата последние 5 лет?', reply_markup=y_n_3)
    await state.finish()
#далее про стаж YES
@dp.callback_query_handler(text="y_work")
async def stazh(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Вам нужно подавать документы на Периодическую аккредитацию', reply_markup=end_btn_2) 
#далее про стаж NO
@dp.callback_query_handler(text="n_work")
async def stazh2(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Вам нужно пройти ПП и пойти на Первичную Специализированную аккредитацию', reply_markup=end_btn_2) 

#БЛОК 3. КАТЕГОРИЯ-----------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="category_dok")
async def cat(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Есть ли у вас уже категория', reply_markup=categ_y_n)
#Категория - ДА
@dp.callback_query_handler(text="cat_yes")
async def cat1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Какая у вас категория?', reply_markup=level_cat)
#Подразделы уровня категорий
@dp.callback_query_handler(text=("1_cat", "2_cat"))
async def cat5(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Для того, чтобы получиь категорию выше нужно собрать пакет документов и иметь стаж более 3 лет по специальности', reply_markup=end_btn)
@dp.callback_query_handler(text="3_cat")
async def cat6(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Сейчас мораторий на продление/подтверждение категории. Можно только понизить на ступень', reply_markup=end_btn)
#Категория - НЕТ
@dp.callback_query_handler(text="cat_no")
async def cat2(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Сколько лет стажа?', reply_markup=ex_work)
#Подразделы стажа
@dp.callback_query_handler(text="less_3")
async def stazh_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Сейчас вы не можете получить категорию. Необходимо иметь стаж более 3-ех лет по специальности', reply_markup=end_btn)
@dp.callback_query_handler(text="more_3")
async def stazh_btn1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Для того, чтобы получить вторую категорию необходимо: ...', reply_markup=end_btn)

#БЛОК - ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ--------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="go_back")
async def Back(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=MAIN_STAGES_TEXT, reply_markup=menu)

@dp.message_handler(text="🔙 Вернуться в меню")
async def back_2(message: types.Message):
    await message.answer(text=MAIN_STAGES_TEXT, reply_markup=menu)

#БЛОК - ПЕРЕЙТИ К АККРЕДИТАЦИИ------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="go_accred")
async def accred_go(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_3, reply_markup=accred_menu)

#БЛОК - ОСТАВИТЬ ЗАЯВКУ - ДА ---------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text = ("send_text", "your_quest"))
async def zvk(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Введите Имя')
    await ProfilestatesGroup.name.set()

@dp.message_handler(state=ProfilestatesGroup.name)
async def name_test(message: types.Message, state: FSMContext):
    async with state.proxy() as ZPR: #открываем локальное хранилище данных
        ZPR['name']=message.text #сохранение текста
    answer = 'Ваш Запрос'
    await bot.send_message(message.from_user.id, answer)
    await ProfilestatesGroup.zapros.set()

@dp.message_handler(state=ProfilestatesGroup.zapros)
async def zapros_info(message: types.Message, state: FSMContext):
    async with state.proxy() as ZPR: #открываем локальное хранилище данных
        ZPR['info']=message.text #сохранение текста
    answer = 'Пожалуйста оставьте свой номер телефона, чтобы мы могли связаться с вами. Для этого достаточно нажать на кнопку внизу'
    await bot.send_message(message.from_user.id, answer, reply_markup=contact)
    await ProfilestatesGroup.telefon.set()
  

@dp.message_handler(content_types=['contact'], state=ProfilestatesGroup.telefon)
async def tel(message: types.Message, state: FSMContext):    
    async with state.proxy() as ZPR: #открываем локальное хранилище данных
        ZPR['number']=message.text #сохранение текста   
    await bot.send_message(admin_id, f'Пользователь: {message.from_user.full_name} \n \n'
                                f'Как обращаться: {ZPR["name"]} \n \n'
                                f'Телефон: {message.contact.phone_number} \n \n'
                                f'Запрос: {ZPR["info"]} \n \n')
    await message.answer(text="✔ Спасибо за заявку. В скором времени менеджер с вами свяжется", reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Для продолжения работы вернитесь в главное меню", reply_markup=end_btn_4)  
    await state.finish()

#<<<<<<<<<  ВСПОМОГАТЕЛЬНОЕ МЕНЮ   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Вспомогательное меню
@dp.message_handler(commands=['menu'])
async def my_commands_3(message: types.Message):
    await message.answer(text=MAIN_STAGES_TEXT, reply_markup=menu)
@dp.message_handler(commands=['call'])
async def my_commands(message: types.Message):
    await message.answer(text='Если вы не нашли ответа на свой вопрос в нашем боте, вы можете оставить заявку', reply_markup=request_bnt_3)
@dp.message_handler(commands=['info'])
async def my_commands_2(message: types.Message):
    await message.answer(text='Здесь будет инфо текст про УЦ АПР с контактными данными, номером лицензии и ссылкой на сайт', reply_markup=end_btn_4)

#ПОДСКАЗКИ
@dp.callback_query_handler(text='promp_1')
async def pr_1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text='Здесь инфо текст про то где именно смотреть кол-во баллов НМО', show_alert=True)
#<<<<<<<<<  КОНЕЦ   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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