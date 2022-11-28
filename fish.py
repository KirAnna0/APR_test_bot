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
study = InlineKeyboardButton('🧑‍⚕️ Обучение медиков', callback_data='study_med')
problems = InlineKeyboardButton('📃 Проблемы с документами', callback_data='problems_dok')
category = InlineKeyboardButton('🎓 Квалификационные категории', callback_data='category_dok')
seminar = InlineKeyboardButton('📚 Семинары', callback_data='seminar')
question = InlineKeyboardButton('❓ Задайте свой вопрос', callback_data='your_quest')
menu = InlineKeyboardMarkup(row_width=1).add(study,problems,category,seminar, question)

#обратные кнопки
back_blok_1 = InlineKeyboardButton('🔙 Назад', callback_data='back_blok_1') #обучение медиков
back_blok_pk = InlineKeyboardButton('🔙 Назад', callback_data='back_blok_pk')#обучение пк

#back_blok_2 = #проблемы с доками

#back_block_3 = #категогия

#БЛОК 1: Обучение медиков  #готов
pk_btn = InlineKeyboardButton('Повышение квалификации', callback_data='pk_med')
pp_btn = InlineKeyboardButton('Профессиональная переподготовка', callback_data='pp_med')
nmo_btn = InlineKeyboardButton('Баллы НМО', callback_data='nmo_med')
accre_btn = InlineKeyboardButton('Аккредитация', callback_data='accred_med')
study_main_m = InlineKeyboardMarkup(row_width=1).add(pk_btn, pp_btn, nmo_btn, accre_btn, back_blok_1)
#ПК. подраздел. Для чего проходят ПК
for_accred = InlineKeyboardButton('Для прохождения аккредитации', callback_data='for_acc')
for_prodlen = InlineKeyboardButton('Продлить сертификат', callback_data='for_prod')
for_prosroch = InlineKeyboardButton('У меня просрочен сертификат', callback_data='for_pros')
for_menu = InlineKeyboardMarkup(row_width=1).add(for_accred, for_prodlen, for_prosroch, back_blok_pk)
#ПП. подраздел. Для чего проходят ПП
pp_smp = InlineKeyboardButton('Среднее профессиональное образование', callback_data='pp_smp_med')
pp_vmp = InlineKeyboardButton('Высшее образование', callback_data='pp_vmp_med')
pp_for_menu = InlineKeyboardMarkup(row_width=1).add(pp_smp, pp_vmp)
#Аккредитация. подразделы
accred_btn_first = InlineKeyboardButton('Первичная аккредитация', callback_data='first_accred')
accred_btn_reply = InlineKeyboardButton('Периодическая аккредитация', callback_data='reply_accred')
accred_btn_spec_first = InlineKeyboardButton('Первичная специализированная', callback_data='spec_accred')
accred_menu = InlineKeyboardMarkup(row_width=1).add(accred_btn_first, accred_btn_reply,accred_btn_spec_first, back_blok_pk)

#БЛОК 2: Проблемы с документами
delay = InlineKeyboardButton('У меня просрочен сертификат', callback_data='delay_sert')
foreign_dok = InlineKeyboardButton('У меня иностранные документы', callback_data='foreign')
pause_work = InlineKeyboardButton('У меня перерыв в стаже', callback_data='pause')
not_end = InlineKeyboardButton('У меня неоконченное образование', callback_data='not_edu')
problem_menu = InlineKeyboardMarkup(row_width=1).add(delay, foreign_dok, pause_work, not_end, back_blok_1)
#Подраздел неоконченное образование
no_ed_y_n = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Да, получил(а)', callback_data='yes_sert'), 
InlineKeyboardButton('Нет, не получал(а)', callback_data='no_sert'))
ordinature = InlineKeyboardButton('Высшее - интернатура/ординатура', callback_data='ordinat')
specialitet = InlineKeyboardButton('Высшее - специалитет', callback_data='specialit')
srednee = InlineKeyboardButton('Среднее профессиональное', callback_data='sred')
level_edu = InlineKeyboardMarkup(row_width=1).add(ordinature, specialitet, srednee)

#БЛОК 3: КАТЕГОРИИ
cat_yes = InlineKeyboardButton('Да', callback_data='cat_yes')
cat_no = InlineKeyboardButton('Нет', callback_data='cat_no')
categ_y_n = InlineKeyboardMarkup(row_width=2).add(cat_yes, cat_no , back_blok_1)
level_cat = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Первая категория', callback_data='1_cat'), 
InlineKeyboardButton('Вторая категория', callback_data='2_cat'), 
InlineKeyboardButton('Высшая категория', callback_data='3_cat'))
ex_work = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('До 3-ех лет', callback_data='less_3'), 
InlineKeyboardButton('Более 3-ех лет', callback_data='more_3'))

#Другие кнопки

back = InlineKeyboardButton('🔙 Вернуться в меню', callback_data='go_back')
go_accred = InlineKeyboardButton('🔜 Перейти в блок Аккредитации', callback_data='go_accred')
else_question = InlineKeyboardButton('Получить консультацию', callback_data='else_question')
request_bnt_2 = InlineKeyboardButton('Оставить заявку', callback_data='send_text')
period_akkred = InlineKeyboardButton('Периодическая аккредитация',callback_data='per_acc')

end_btn = InlineKeyboardMarkup(row_width=2).add(back, else_question)
end_btn_2 = InlineKeyboardMarkup(row_width=2).add(back, go_accred, else_question)
end_btn_3 = InlineKeyboardMarkup(row_width=2).add(back, request_bnt_2)
end_btn_4 = InlineKeyboardMarkup(row_width=2).add(back)
request_bnt_3 = InlineKeyboardMarkup(row_width=2).add(request_bnt_2)
end_btn_5 = InlineKeyboardMarkup(row_width=2).add(back, delay)
end_btn_6= InlineKeyboardMarkup(row_width=2).add(back, delay, else_question)
end_btn_7 = InlineKeyboardMarkup().add(back, period_akkred, else_question)

#кнопки-ссылки
semin_url = InlineKeyboardMarkup(row_width=1).add(back, InlineKeyboardButton('Посмотреть расписание семинаров', url='https://apr.center/seminars'))

rmapo_url = InlineKeyboardButton('Расписание на сайте РМАПО для высшего', url='https://rmapo.ru/akkreditacija/pervichnaya-specializirovannaya-akkreditaciya/9551-pervichnaja-specializirovannaja-akkreditacija.html')
mcud_url = InlineKeyboardButton('Расписание на сайте МК для среднего', url='https://mcud.ru/%D0%B0%D0%BA%D0%BA%D1%80%D0%B5%D0%B4%D0%B8%D1%82%D0%B0%D1%86%D0%B8%D1%8F-%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82%D0%B0-%D1%81%D0%BF%D0%BE/%D0%BF%D0%B5%D1%80%D0%B2%D0%B8%D1%87%D0%BD%D0%B0%D1%8F-%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F-%D0%B0%D0%BA%D0%BA%D1%80%D0%B5%D0%B4/')
accred_url = InlineKeyboardMarkup(row_width=1).add(rmapo_url, mcud_url,back_blok_pk, else_question)

kvalik_vmp = InlineKeyboardMarkup(row_width=2).add(back_blok_pk, InlineKeyboardButton('Перейти в приказ', url='https://docs.cntd.ru/document/420339191'), else_question)
kvalik_smp = InlineKeyboardMarkup(row_width=2).add(back_blok_pk, InlineKeyboardButton('Перейти в приказ', url='http://ivo.garant.ru/#/document/71231064/paragraph/13:0'), else_question)

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
    test=State()
#<<<<<<<<<  АЛГОРИТМ  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Первый запуск бота, приветственное слово
HI = '''Добрый день! Это бот «Академии профессионального развития»    
Здесь вы можете найти всю полезную информацию по обучению медицинских специалистов, подготовиться к аккредитации и рассчитать баллы НМО. 
 
Для того, чтобы приступить к работе нажмите «Главное меню»!'''

@dp.message_handler(commands=['start'], state=None)
async def button_start_key(message: types.Message):
    await message.reply(text=HI, reply_markup=start)

#Реакция на кнопку Начать, всплытие меню основных разделов
MAIN_STAGES_TEXT = '''<b>Какой раздел вас интересует?</b> 
<b>Обучение медиков:</b> информации о повышении квалификации, баллах НМО и профессиональной переподготовке.
<b>Проблемы с документами:</b> что делать если у Вас просрочены документы, документы иностранного государства, или был перерыв в стаже
<b>Квалификационные категории:</b> если Вам необходимо продлить или получить категорию с нуля.
<b>Семинары:</b> наши мероприятия с баллами НМО, с возможностью обучения очно и онлайн.
'''

@dp.callback_query_handler(text = "start")
async def main_stage(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=MAIN_STAGES_TEXT, reply_markup=menu)

#реакция на закрытие раздела
YES_QUESTION = 'Если у вас все еще остались вопросы, можете оставить заявку и наш менеджер вам перезвонит'
@dp.callback_query_handler(text = ("else_question", 'your_quest'))
async def ent_answer(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)    
    await bot.send_message(callback_query.from_user.id, text=YES_QUESTION, reply_markup=end_btn_3)

#БЛОК 1. ОБУЧЕНИЕ МЕДИКОВ----------------------------------------------------------------------------------------------------------
#Реакция на кнопку 'Блок: Обучение медиков', всплытие подразделов
@dp.callback_query_handler(text="study_med")
async def study_menu(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Какой вид обучения Вас интересует?', reply_markup=study_main_m)
#go back
@dp.callback_query_handler(text="back_blok_1")
async def back_1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=MAIN_STAGES_TEXT, reply_markup=menu)  
#Реакция на кнопку подраздел 'ПК', всплытие подразделов
@dp.callback_query_handler(text="pk_med")
async def pk_menu(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='С какой целью Вы хотите пройти повышение квалификации?', reply_markup=for_menu)     # скрываем предыдущий текст + кнопки
#реакции на подразделы меню ПК
@dp.callback_query_handler(text="for_acc")
async def for_accreditation(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Вам нужно перейти в раздел аккред. Переход в аккред', reply_markup=end_btn_2)   
INFO_TEXT_6 = '''Медицинские сертификаты перестали выдаваться учебными центрами 31.12.2020. На смену сертификатам пришло свидетельство об аккредитации.
Пройти процедуру НЕСЛОЖНО: достаточно курса повышения квалификации 144 часа и портфолио с информацией о профессиональной деятельности.
'''
@dp.callback_query_handler(text=("for_prod"))
async def for_prodlenie(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_6, reply_markup=end_btn_7)
INFO_TEXT_9='''НЕ ПИСАТЬ. Укажите год выдачи Вашего посленего сертификата? <em>(напишите в ответном сообщении год цифрами)</em>
'''
@dp.callback_query_handler(text="for_pros")
async def for_prosrochki(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_9, reply_markup=end_btn_5)   
#go_back
@dp.callback_query_handler(text="back_blok_pk")
async def back_3(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Какой вид обучения Вас интересует?', reply_markup=study_main_m)  
#Реакция на кнопку подраздел 'ПП', всплытие подразделов
@dp.callback_query_handler(text="pp_med")
async def pp_menu(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Укажите Ваш уровень образования', reply_markup=pp_for_menu)

#реакции на подразделы меню ПП
INFO_TEXT_1 = f'''Откройте приказ доступный по ссылке и найдите интересующую Вас специальность.
https://docs.cntd.ru/document/420339191
<b>Как читать приказ?<b>
В пункте «Дополнительное профессиональное образование» указаны требования к вашему диплому.
В пункте «Должности» - возможные должности, которые занимает специалист с выбранной специальностью.
Для успешного прохождения переподготовки, у Вас должен быть соответствующий диплом. В ином случае Вы не можете претендовать на переподготовку по выбранной специальности.'''

INFO_TEXT_2 = f'''Откройте приказ доступный по ссылке и найдите интересующую Вас специальность.
http://ivo.garant.ru/#/document/71231064/paragraph/13:0
<b>Как читать приказ?<b>
В пункте «Уровень профессионального образования» - требования к Вашему диплому
В пункте «Дополнительное профессиональное образование» - требования к интернатуре/ординатуре
В пункте «Должности» - возможные должности, которые занимает специалист с выбранной специальностью.
Для успешного прохождения переподготовки, у Вас должен быть соответствующий диплом и интернатура/ординатура. В ином случае Вы не можете претендовать на переподготовку по выбранной специальности.'''

@dp.callback_query_handler(text="pp_smp_med")
async def otv_smp(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_1, reply_markup=kvalik_smp)
@dp.callback_query_handler(text="pp_vmp_med")
async def otv_vmp(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_2, reply_markup=kvalik_vmp)

#реакция на Блок: Аккредитация, всплытие подразделов
INFO_TEXT_3 = 'Описание что такое аккредитация. В каких случаях какую надо проходить. И конечный вопрос: Какая аккредитация вас интересует?'
INFO_TEXT_5 = 'какой-то там инфо текст про расписание. Про то, что нужно готовится к экзаменам, самостоятельно проходить обучение и все такое'
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
@dp.callback_query_handler(text=("reply_accred",'per_acc'))
async def otv_rep_acc(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Какой-то инфо текст про то, что нужны баллы', reply_markup=calculate_nmo)  

@dp.callback_query_handler(text="spec_accred")
async def otv_first_spec_ac(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_5, reply_markup=accred_url)
#реакция на Семинар
INFO_TEXT_14='''Наш учебный центр «Академия профессионального развития» проводит не только обучение ДПО, но и семинары/вебинары для медицинских работников.
В мероприятиях участвуют ведущие лекторы по своим направлениям, и дают слушателям актуальную информацию и знания по соответствующим темам: УЗИ, гинекология, неврология и многое другое.
Мероприятия доступны в очном формате в Москве и в дистанционном по всей России.

К тому же Вы можете получить баллы НМО за каждый семинар: 36 или 50 баллов.

Присоединяйтесь!
'''
@dp.callback_query_handler(text="seminar")
async def seminar_apr(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_14, reply_markup=semin_url)

#БЛОК. Калькулятор баллов НМО----------------------------------------------------------------------------------------------------
#кнопки
calk_nmo = InlineKeyboardButton('🧮 Калькулятор баллов', callback_data='calculate_nmo')
calculate_nmo = InlineKeyboardMarkup(row_width=2).add(calk_nmo, back_blok_pk)
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
INFO_TEXT_7 = '''
<b>НМО</b> - это непрерывное медицинское образование. Данная система включает в себя аккредитацию и пришла на смену привычным сертификатам. Главное отличие в процессе обучения. 
Если раньше специалист учился 1 раз в 5 лет, и объем обучения составлял 144/288 часов. То теперь специалист учится каждый год в объеме 50 часов. То есть 250 часов за 5 лет.
1 балл НМО = 1 часу обучения. Система является обязательной и для высшего и для среднего медицинского образования.

Ниже Вы найдете калькулятор баллов НМО, который позволит Вам узнать, сколько Вам нужно накопить баллов НМО, чтобы успешно пройти периодическую аккредитацию и получить документ для работы.
'''
@dp.callback_query_handler(text="nmo_med")
async def nmo(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text=INFO_TEXT_7, reply_markup=calculate_nmo) #ЗАМЕНА КНОПОК
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
INFO_TEXT_8='''
Опишите, какая у Вас проблема?
Если вы не нашли свой вариант, то нажмите «Назад» и нажмите кнопку «Получить консультацию»'''
@dp.callback_query_handler(text='problems_dok')
async def problem_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_8, reply_markup=problem_menu) 
#реакция на просрочку сертификата
@dp.callback_query_handler(text='delay_sert')
async def delay_sert_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='ОБНОВЛЕНИЕ АЛГОРИТМА', reply_markup=end_btn_2) #ПЕРЕХОД НА АККРЕДИТАЦИЮ
INFO_TEXT_10 = '''Для прохождения обучения на территории РФ Вам необходимо подтвердить иностранные документы в соответствующих ведомствах.
Диплом об образовании подтверждается в Рособрнадзоре(https://obrnadzor.gov.ru/) (за исключением взаимопризнанных документов - посмотреть список государств: https://nic.glavex.ru//ru/docs/foreign/confirmation)
Медицинский сертификат подтверждается в Росздравнадзоре (https://roszdravnadzor.gov.ru/).
После обращения в данные ведомства Вам будет прислана инструкция о дальнейших действиях для подтверждения документов.
'''
#реакция на иностранные документы
@dp.callback_query_handler(text='foreign')
async def foreign_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_10, reply_markup=end_btn)
#реакция на неоконченное образование
@dp.callback_query_handler(text='not_edu')
async def not_edu_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Получали ли Вы сертификат или свидительство об аккредитации?', reply_markup=no_ed_y_n) 
#реакция на подраздел после да
INFO_TEXT_11 = '''Вы можете обучаться по любым программам дополнительного профессионального образования.
Перейдите в главное меню, в раздел «Обучение медиков», чтобы посмотреть доступные варианты обучения
'''
@dp.callback_query_handler(text='yes_sert')
async def not_btn2(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_11, reply_markup=end_btn)     
#реакция на подраздел после нет
INFO_TEXT_12 = '''Если Вы не получали документов, то Вы не сможете без них обучаться по программам дополнительного профессионального образования.
Для получения документов у Вас есть два варианта:
1. Обратиться в учебное заведение и завершить свое обучение, пройти первичную аккредитацию.
2. При наличии диплома на руках Вы можете обратиться в свой территориальный аккредитационный центр и пройти первичную аккредитацию.
'''
@dp.callback_query_handler(text='no_sert')
async def not_btn3(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_12, reply_markup=end_btn)  

#реакция на перерыв в стаже КАЛЬКУЛЯТОР ПЕРЕРЫВА-------------------------------------------------------------------------------------------------------------------
#кнопки
#ОБНОВЛЕНИЕ КАЛЬКУЛЯТОРА ПЕРЕРЫВА В СТАЖЕ + ПРОСРОЧКА СЕРТИФИКАТА
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
    text='Присвоена ли Вам в данный момент квалификационная категория?', reply_markup=categ_y_n)
#Категория - ДА
#@dp.callback_query_handler(text="cat_yes")
#async def cat1(callback_query: types.CallbackQuery):
#    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
#    text='Какая у Вас категория?', reply_markup=level_cat)
#Подразделы уровня категорий
INFO_TEXT_13='''Для повышения или для сохранения текущей категории, Вам необходимо собрать пакет документов, написать отчет о своей профессиональной деятельности и подготовиться к тестированию и собеседованию. В ходе тестирования специалист отвечает на теоретические и практические вопросы по своей специальности с вариантами ответов. В ходе собеседования комиссия обсуждает с претендентом отчет о его профессиональной деятельности и задает дополнительные вопросы по специальности.
Аттестация проходит в Вашей территориальной комиссии, у каждой комиссии могут быть свои варианты тестирования и дополнительные вопросы.
'''
@dp.callback_query_handler(text='cat_yes')
async def cat5(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_13, reply_markup=end_btn)
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
@dp.callback_query_handler(text = ("send_text"))
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
    answer = '''Пожалуйста укажите свой номер телефона, чтобы мы могли связаться с вами
    Вы можете прописать его вручную в формате 1112223344 или нажать на кнопку внизу.'''
    await bot.send_message(message.from_user.id, answer, reply_markup=contact)
    await ProfilestatesGroup.telefon.set()

@dp.message_handler(lambda message: not message.text.isdigit(), state=ProfilestatesGroup.telefon)
async def chek_num(message: types.Message):
    await message.answer('Пожалуйста, укажите номер телефона в формате 1112223344 без дополнительных символов и пробелов или нажмите на кнопку внизу', reply_markup=contact)
    await ProfilestatesGroup.telefon.set()

@dp.message_handler(state=ProfilestatesGroup.telefon)
async def tel_2(message: types.Message, state: FSMContext):
    async with state.proxy() as ZPR: #открываем локальное хранилище данных
        ZPR['tel']=message.text #сохранение текста
    await bot.send_message(admin_id, f'Никнейм пользователя: @{message.from_user.username} \n'
                                f'Как обращаться: {ZPR["name"]} \n'
                                f'Телефон: {ZPR["tel"]} \n'
                                f'Запрос: {ZPR["info"]} \n')
    await message.answer(text="✔ Спасибо за заявку. В скором времени менеджер с вами свяжется", reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Для продолжения работы вернитесь в главное меню", reply_markup=end_btn_4)  
    await state.finish()

@dp.message_handler(content_types=['contact'], state=ProfilestatesGroup.telefon)
async def tel(message: types.Message, state: FSMContext):    
    async with state.proxy() as ZPR: #открываем локальное хранилище данных
        ZPR['number']=message.text #сохранение текста   
    await bot.send_message(admin_id, f'Никнейм пользователя: @{message.from_user.username} \n'
                                f'Как обращаться: {ZPR["name"]} \n'
                                f'Телефон: {ZPR["number"]} \n'
                                f'Запрос: {ZPR["info"]} \n')
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