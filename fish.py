from datetime import datetime
import logging

from aiogram import Bot, Dispatcher, executor, types
import asyncio
import time

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
back_blok_nmo = InlineKeyboardButton('🔙 Назад', callback_data='back_blok_nmo')#блок НМО

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
differ_accred=InlineKeyboardButton('Чем отличаются виды аккредитации?',callback_data='what_diff')
accred_menu = InlineKeyboardMarkup(row_width=1).add(accred_btn_first, accred_btn_reply,accred_btn_spec_first,differ_accred, back_blok_pk)

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
categ_y_n = InlineKeyboardMarkup(row_width=3).add(cat_yes, cat_no , back_blok_1)
level_cat = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Первая категория', callback_data='1_cat'), 
InlineKeyboardButton('Вторая категория', callback_data='2_cat'), 
InlineKeyboardButton('Высшая категория', callback_data='3_cat'))
ex_work = InlineKeyboardMarkup(row_width=4).add(InlineKeyboardButton('До 3 лет', callback_data='less_3'), 
InlineKeyboardButton('3-5 лет', callback_data='3_5'), InlineKeyboardButton('5-7 лет',callback_data='5_7'),
InlineKeyboardButton('От 7 лет',callback_data='more_7'))
ex_work_2 = InlineKeyboardMarkup(row_width=4).add(InlineKeyboardButton('До 2 лет', callback_data='less_2'), 
InlineKeyboardButton('2-5 лет', callback_data='2_5'), InlineKeyboardButton('5-8 лет',callback_data='5_8'),
InlineKeyboardButton('От 8 лет',callback_data='more_8'))
lev_ed = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Высшее образование',callback_data='cat_vp'), InlineKeyboardButton('Среднее образование',callback_data='cat_sp'))

#Другие кнопки

back = InlineKeyboardButton('🔙 Вернуться в меню', callback_data='go_back')
go_accred = InlineKeyboardButton('🔜 Перейти в блок Аккредитации', callback_data='go_accred')
else_question = InlineKeyboardButton('Получить консультацию', callback_data='else_question')
request_bnt_2 = InlineKeyboardButton('Оставить заявку', callback_data='send_text')
period_akkred = InlineKeyboardButton('Периодическая аккредитация',callback_data='per_acc')

end_btn = InlineKeyboardMarkup(row_width=2).add(back, else_question)
end_btn_2 = InlineKeyboardMarkup(row_width=1).add(back, go_accred, else_question)
end_btn_3 = InlineKeyboardMarkup(row_width=2).add(back, request_bnt_2)
end_btn_4 = InlineKeyboardMarkup(row_width=2).add(back)
request_bnt_3 = InlineKeyboardMarkup(row_width=2).add(request_bnt_2)
end_btn_5 = InlineKeyboardMarkup(row_width=2).add(back, delay)
end_btn_6= InlineKeyboardMarkup(row_width=1).add(back, delay, else_question)
end_btn_7 = InlineKeyboardMarkup(row_width=1).add(back, period_akkred, else_question)
#кнопки-ссылки
semin_url = InlineKeyboardMarkup(row_width=1).add(back, InlineKeyboardButton('Посмотреть расписание семинаров', url='https://apr.center/seminars'))

port_url = InlineKeyboardButton('Портал НФМО',url='https://edu.rosminzdrav.ru/')

kvalik_vmp = InlineKeyboardMarkup(row_width=2).add(back_blok_pk, InlineKeyboardButton('Перейти в приказ', url='http://ivo.garant.ru/#/document/71231064/paragraph/13:0'), else_question)
kvalik_smp = InlineKeyboardMarkup(row_width=2).add(back_blok_pk, InlineKeyboardButton('Перейти в приказ', url='https://docs.cntd.ru/document/420339191'), else_question)

#Гайды
gid = InlineKeyboardButton('Гайд по оформлению документов',callback_data='gid')
gid_2 = InlineKeyboardButton('Гайд по оформлению документов',callback_data='gid_2')
end_gid = InlineKeyboardMarkup(row_width=1).add(back, else_question,gid)
end_gid_2 = InlineKeyboardMarkup(row_width=1).add(back, else_question,gid_2)

#Подсказки
promp_1 = InlineKeyboardButton('Где посмотреть баллы НМО?', callback_data='promp_1')
promp_2 = InlineKeyboardButton('Посмотреть список документов', callback_data='promp_2')
promp_3_cat = InlineKeyboardButton('Посмотреть список документов', callback_data='promp_3')
promp_4_cat = InlineKeyboardButton('Как проходит аттестация на категорию', callback_data='promp_4')
promp_5_nmo = InlineKeyboardButton('Что такое периодическая аккредитация?', callback_data='promp_5')

#Концовка с подсказкой
end_btn_8=InlineKeyboardMarkup(row_width=1).add(back, else_question, promp_2)
end_btn_9=InlineKeyboardMarkup(row_width=1).add(back, else_question, promp_3_cat, promp_4_cat)
end_btn_10=InlineKeyboardMarkup(row_width=1).add(back, else_question, promp_3_cat)
end_btn_11=InlineKeyboardMarkup(row_width=1).add(back, else_question, promp_5_nmo, gid)
end_btn_12 = InlineKeyboardMarkup(row_width=1).add(back_blok_nmo, port_url)
end_btn_13 = InlineKeyboardMarkup(row_width=1).add(back, else_question, gid_2)
end_btn_14 = InlineKeyboardMarkup(row_width=1).add(back, else_question, promp_3_cat)
end_btn_15 = InlineKeyboardMarkup(row_width=1).add(back, else_question, gid)

#Оставить свою заявку
request_bnt = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Оставить заявку'))

#<<<<<<<<<  ПЕРЕМЕННЫЕ СОСТОЯНИЯ  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class ProfilestatesGroup(StatesGroup):
    zapros = State()
    telefon = State()
    name = State()
    year = State()
    ball_144= State()
    pros=State() 
    test=State()

# post-state
class Post(StatesGroup):
    text = State()
    confirm = State()

#<<<<<<<<<  РАССЫЛКА  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
joinedFile = open('mailing.txt','r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

#Первый запуск бота, приветственное слово
HI = '''Добрый день! Это бот «Академии профессионального развития»    
Здесь вы можете найти всю полезную информацию по обучению медицинских специалистов, подготовиться к аккредитации и рассчитать баллы НМО. 
 
Для того, чтобы приступить к работе нажмите «Главное меню»!'''

@dp.message_handler(commands=['start'], state=None)
async def button_start_key(message: types.Message):
    if not str(message.chat.id) in joinedUsers:     #запись пользователя
        joinedFile=open('mailing.txt','a')
        joinedFile.write(str(message.chat.id)+"\n")
        joinedUsers.add(message.chat.id)
    await message.reply(text=HI, reply_markup=start)

#начало рассылки
@dp.message_handler(commands=['send'])
async def send_public_post(message: types.Message):
    text_to_admin = 'Чтобы сделать рассылку, отправьте текст.'
    not_allowed = 'Вам это делать нельзя! ;)'
#    if str(message.chat.id) in ADMIN_ID:
    await Post.text.set()
    await message.answer(text_to_admin)
#    else:
#        await message.answer(not_allowed, reply_markup=menu)
#Предпросмотр текста
@dp.message_handler(state=Post.text)
async def got_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)

    text_before_confirmation = f'Предпросмотр текста рассылки:\n\n{message.text}\n\n' \
                               f'Для начала рассылки отправьте ' \
                               f'<b>ДА</b>, для отмены - <b>НЕТ</b>.'
    await Post.confirm.set()
    await message.answer(text_before_confirmation)

#отмена рассылки
@dp.message_handler(lambda message: message.text.upper() == 'НЕТ', state=Post.confirm)
async def cancel_publication(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено.')

#запуск рассылки
@dp.message_handler(lambda message: message.text.upper() == 'ДА', state=Post.confirm)
async def publish(message: types.Message, state: FSMContext):
    counter = 0
    async with state.proxy() as data:
        for user in joinedUsers:
            if counter % 10 == 0:
                time.sleep(0.5)
            try:
                await bot.send_message(user, text=data['text'])
            except:
                counter += 1
    all_users = len(joinedUsers)
    await state.finish()
    publication_ended_text = f'Рассылка закончена.\n\n' \
                             f'Ваше сообщение отправлено <b>{all_users - counter}</b> пользователям.'
    await message.answer(publication_ended_text)

#<<<<<<<<<  СТАТИСТИКА  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


#<<<<<<<<<  АЛГОРИТМ  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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
INFO_TEXT_1 = '''Откройте приказ доступный по ссылке и найдите интересующую Вас специальность.
https://docs.cntd.ru/document/420339191

<b>Как читать приказ?</b>
В пункте «Дополнительное профессиональное образование» указаны требования к вашему диплому.
В пункте «Должности» - возможные должности, которые занимает специалист с выбранной специальностью.
Для успешного прохождения переподготовки, у Вас должен быть соответствующий диплом. В ином случае Вы не можете претендовать на переподготовку по выбранной специальности.'''

INFO_TEXT_2 = '''Откройте приказ доступный по ссылке и найдите интересующую Вас специальность.
http://ivo.garant.ru/#/document/71231064/paragraph/13:0

<b>Как читать приказ?</b>
В пункте «Уровень профессионального образования» - требования к Вашему диплому
В пункте «Дополнительное профессиональное образование» - требования к интернатуре/ординатуре
В пункте «Должности» - возможные должности, которые занимает специалист с выбранной специальностью.
Для успешного прохождения переподготовки, у Вас должен быть соответствующий диплом и интернатура/ординатура. В ином случае Вы не можете претендовать на переподготовку по выбранной специальности.'''

@dp.callback_query_handler(text="pp_smp_med")
async def otv_smp(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id = callback_query.message.chat.id, text=INFO_TEXT_1, reply_markup=kvalik_smp, disable_web_page_preview=True)

@dp.callback_query_handler(text="pp_vmp_med")
async def otv_vmp(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id = callback_query.message.chat.id, text=INFO_TEXT_2, reply_markup=kvalik_vmp, disable_web_page_preview=True)

#реакция на Блок: Аккредитация, всплытие подразделов
@dp.callback_query_handler(text='accred_med')
async def accreditation(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Какой вид аккредитации Вас интересует?', reply_markup=accred_menu) 
#реакции на подразделы меню Аккредитации
#Первичная аккред
INFO_TEXT_4='''Первичная аккредитация проводится для выпускников медицинских ВУЗов, колледжей (за исключением тех, кто учился за рубежом или проходил ординатуру).
Первичная аккредитация включает в себя 2 этапа: тестирование за компьютером, оценка навыков в симулированных условиях.
Для успешного прохождения необходимо правильно решить не менее 70% заданий на каждом из этапов аккредитации.
Проводится очно в соответствующем территориальном аккредитационном центре (обычно на базе места обучения).
'''
@dp.callback_query_handler(text="first_accred")
async def otv_first_ac(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_4, reply_markup=end_btn) 

INFO_TEXT_25='''Периодическая аккредитация - это обязательная процедура подтверждения права на осуществление медицинской деятельности. Она проводится для всех медицинских работников: и врачей, и медсестер. Период прохождения - 1 раз в 5 лет.
Процедура проводится дистанционно в формате зачет/незачет. Аккредитационная комиссия проверяет поданные работником сведения о пройденных образовательных курсах, и сведения о профессиональной деятельности в виде отчета.
Для прохождения периодической аккредитации работнику необходимо пройти обучение объемом 144 часа:
а) Программы повышения квалификации (144 часа), не входящие в перечень портала НМО;
б) Альтернативный способ набора 144 часов: программы повышения квалификации (не менее 72 часов на портале НМО) + образовательные неформальные активности (ИОМ) на портале НМО (оставшиеся 72 часа и менее).
'''
#Периодическая аккред
@dp.callback_query_handler(text=("reply_accred",'per_acc'))
async def otv_rep_acc(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_25, reply_markup=end_btn_15)   

INFO_TEXT_5 = '''Первичная специализированная аккредитация (ПСА) проводится для медицинских работников, которые получали высшее образование заграницей, выпускников ординатуры или программ профессиональной переподготовки.
ПСА включает в себя 3 этапа: тестирование за компьютером, оценка навыков в симулированных условиях, решение ситуационных задач.
Для успешного прохождения необходимо правильно решить не менее 70% заданий на каждом из этапов аккредитации.
Проводится очно в соответствующем территориальном аккредитационном центре.
'''
#Первичная специализированная
@dp.callback_query_handler(text="spec_accred")
async def otv_first_spec_ac(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_5, reply_markup=end_btn)

INFO_TEXT_26='''Мы подготовили для Вас специальный гайд по видам аккредитации, где Вы можете узнать обо всех различиях.
Вы можете скачать его по кнопке ниже.
'''
@dp.callback_query_handler(text="what_diff")
async def dif_a(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_26, reply_markup=end_gid_2)

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
calculate_nmo = InlineKeyboardMarkup(row_width=2).add(calk_nmo, back_blok_pk, else_question)
one_more= InlineKeyboardMarkup(row_width=2).add(calk_nmo, back)

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
INFO_TEXT_15 = '''Укажите год выдачи Вашего последнего сертификата? 
<em>(напишите в ответном сообщении год цифрами)</em>
'''
@dp.callback_query_handler(text="nmo_med")
async def nmo(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text=INFO_TEXT_7, reply_markup=calculate_nmo)
@dp.callback_query_handler(text="calculate_nmo")
async def nmo1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=INFO_TEXT_15) #тут запрос не год выдачи
    await ProfilestatesGroup.year.set()

    #таймер на ожидание
    await asyncio.sleep(10) #секунды
    if await state.get_state() == "ProfilestatesGroup:year":
        await bot.send_message(callback_query.from_user.id, text='Пожалуйста, укажите год выдачи Вашего последнего сертификата')
    
#сохраняем год выпуска, проверка на просрочку
@dp.message_handler(state=ProfilestatesGroup.year)
async def spec(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['year']=int(message.text)
    start_year = datetime.now().year - 5 #год начала перед просрочкой
    if data['year'] < start_year:
        await message.answer('Ваш сертификат уже просрочился. Вам необходимо его продлить', reply_markup=end_btn_6)
    else:
        await message.answer('Накапливали ли Вы баллы НМО?', reply_markup=yes_no_2) #+подсказка
    await state.finish()

#Да, копили баллы про 144ч
@dp.callback_query_handler(text="yes_2")
async def nmo3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text='Сколько баллов у Вас набрано? <em>(напишите число в ответном сообщении)</em>')
    await ProfilestatesGroup.ball_144.set()

     #таймер на ожидание
    await asyncio.sleep(10) #секунды
    if await state.get_state() == "ProfilestatesGroup:ball_144":
        await bot.send_message(callback_query.from_user.id, text='Пожалуйста, укажите количество набранных баллов')

#считаем баллы
@dp.message_handler(state=ProfilestatesGroup.ball_144)
async def nmo4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ball_144']=int(message.text) 
    if data['ball_144'] >= 144:
        INFO_TEXT_22='''Вы набрали достаточное кол-во баллов для прохождения аккредитации.
В соответствии с текущими рекомендациями Минздрава РФ, вам достаточно в сумме набрать 144 часа обучения.
После этого Вам будет необходимо составить портфолио, прикрепить туда документы об образовании и пройти периодическую аккредитацию.
Для прохождения аккредитации Вы можете обратиться в наш учебный центр.
'''
        await message.answer(INFO_TEXT_22, reply_markup=end_btn_11)
    else:
        num4= 144 - data['ball_144']
        INFO_TEXT_21=f'''Для прохождения аккредитации вам необходимо набрать {num4} балла(ов) НМО.
В соответствии с текущими рекомендациями Минздрава РФ, вам достаточно в сумме набрать 144 часа обучения.
После этого Вам будет необходимо составить портфолио, прикрепить туда документы об образовании и пройти периодическую аккредитацию.
Для набора баллов НМО и прохождения аккредитации Вы можете обратиться в наш учебный центр.
'''
        await message.answer(INFO_TEXT_21, reply_markup=end_btn_11)
    await state.finish()

INFO_TEXT_22 = '''Процедура периодической аккредитации включает в себя дистанционную проверку портфолио за 5 лет в формате зачет/незачет. В портфолио входят следующие сведения:
- Документы о прохождении всех курсов повышения квалификации;
- Данные об основном образовании, стаже и месте работы;
- Отчет о профессиональной деятельности, включающий в себя статистические данные.
'''
@dp.callback_query_handler(text='promp_5')
async def pr_5(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_22, reply_markup=end_btn_13)


INFO_TEXT_23='''
В соответствии с текущими рекомендациями Минздрава РФ, вам необходимо для прохождения аккредитации пройти курс повышения квалификации объемом 144 часа. Вы можете это сделать, как в рамках НМО, так и пройти обычный курс.
После этого Вам будет необходимо составить портфолио, прикрепить туда документы об образовании и пройти периодическую аккредитацию.
Для набора баллов НМО и прохождения аккредитации Вы можете обратиться в наш учебный центр.
'''
#Нет, не копили
@dp.callback_query_handler(text="no_2")
async def nmo5(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=INFO_TEXT_23, reply_markup=end_btn_11)

#доп.инфа по НМО
INFO_TEXT_20 = '''Баллы НМО бывают двух типов:
- Формальное обучение (курсы повышения квалификации)
- Неформальное обучение (интерактивные образовательные модули)
Количество баллов, Вы можете узнать в личном кабинете на портале НМФО
Если у Вас нет личного кабинета, то оставьте заявку в нашем учебном центре, и мы Вам поможем!
'''
@dp.callback_query_handler(text='promp_1')
async def pr_1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_20, reply_markup=end_btn_12)

@dp.callback_query_handler(text='back_blok_nmo')
async def back_nmo(callback_query:types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Накапливали ли Вы баллы НМО?', reply_markup=yes_no_2)

#БЛОК 2. ПРОБЛЕМЫ С ДОКУМЕНТАМИ---------------------------------------------------------------------------------------------------
yes_no_pr = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Да', callback_data='yes_pro'),
InlineKeyboardButton('Нет', callback_data='no_pro'))

#реакция на блок
INFO_TEXT_8='''
Опишите, какая у Вас проблема?
Если вы не нашли свой вариант, то нажмите «Назад» и нажмите кнопку «Получить консультацию»'''
@dp.callback_query_handler(text='problems_dok')
async def problem_btn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_8, reply_markup=problem_menu) 
#реакция на просрочку сертификата
INFO_TEXT_16='''Вам необходимо пройти профессиональную переподготовку по Вашей специальности и после этого пройти первичную специализированную аккредитацию. Это необходимо сделать, так как Ваш перерыв, составляет более 5 лет.
'''
INFO_TEXT_17 = '''Вам достаточно пройти периодическую аккредитацию. Для этого необходимо пройти обучение объемом 144 часа и подготовить портфолио. В портфолио входит:
- Сведения об образовательных программах;
- Отчет о профессиональной деятельности, заверенный руководителем.
'''
@dp.callback_query_handler(text=('delay_sert','for_pros', 'pause'))
async def delay_sert_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_15)
    await ProfilestatesGroup.pros.set()

    #таймер на ожидание
    await asyncio.sleep(10) #секунды
    if await state.get_state() == "ProfilestatesGroup:pros":
        await bot.send_message(callback_query.from_user.id, text='Пожалуйста, укажите год выдачи Вашего последнего сертификата')

@dp.message_handler(state=ProfilestatesGroup.pros)
async def pros(message: types.Message, state: FSMContext):
    async with state.proxy() as pr: 
        pr['year']=int(message.text)
    num7 = pr['year'] + 10
  
    if num7 < datetime.now().year:
        await message.answer(INFO_TEXT_16, reply_markup=end_btn)
    else:
        await message.answer('Работали ли Вы по указанной в документе специальности последние 2 года?', reply_markup=yes_no_pr)
        
        @dp.callback_query_handler(text='yes_pro')
        async def yes_p(callback_query: types.CallbackQuery):
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
            text=INFO_TEXT_17, reply_markup=end_gid)

        @dp.callback_query_handler(text='no_pro')
        async def no_p(callback_query: types.CallbackQuery):
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
            text=INFO_TEXT_16, reply_markup=end_btn)

    await state.finish()

link='https://obrnadzor.gov.ru/'
link2='https://nic.glavex.ru//ru/docs/foreign/confirmation'
link3='https://roszdravnadzor.gov.ru/'
INFO_TEXT_10 = f'''Для прохождения обучения на территории РФ Вам необходимо подтвердить иностранные документы в соответствующих ведомствах.
Диплом об образовании подтверждается в <a href="{link}">Рособрнадзоре</a> (за исключением взаимопризнанных документов - <a href="{link2}">посмотреть список государств</a>)
Медицинский сертификат подтверждается в <a href="{link3}">Росздравнадзоре</a>.
После обращения в данные ведомства Вам будет прислана инструкция о дальнейших действиях для подтверждения документов.
'''
#реакция на иностранные документы
@dp.callback_query_handler(text='foreign')
async def foreign_btn(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id = callback_query.message.chat.id, text=INFO_TEXT_10, reply_markup=end_btn, disable_web_page_preview=True)

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

#БЛОК 3. КАТЕГОРИЯ-----------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="category_dok")
async def cat(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Присвоена ли Вам в данный момент квалификационная категория?', reply_markup=categ_y_n)
#Категория - ДА
@dp.callback_query_handler(text="cat_yes")
async def cat1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Какая у Вас категория?', reply_markup=level_cat)
#Подразделы уровня категорий
INFO_TEXT_13='''Для повышения или для сохранения текущей категории, Вам необходимо собрать пакет документов, написать отчет о своей профессиональной деятельности и подготовиться к тестированию и собеседованию. В ходе тестирования специалист отвечает на теоретические и практические вопросы по своей специальности с вариантами ответов. В ходе собеседования комиссия обсуждает с претендентом отчет о его профессиональной деятельности и задает дополнительные вопросы по специальности.
Аттестация проходит в Вашей территориальной комиссии, у каждой комиссии могут быть свои варианты тестирования и дополнительные вопросы.
'''
@dp.callback_query_handler(text=('2_cat','1_cat','3_cat'))
async def cat5(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_13, reply_markup=end_btn_8)   
#Категория - НЕТ
@dp.callback_query_handler(text="cat_no")
async def cat2(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Укажите Ваш уровень образования', reply_markup=lev_ed)
#среднее обр
@dp.callback_query_handler(text="cat_sp")
async def cat_s(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Укажите свой стаж работы по специальности', reply_markup=ex_work_2)
#высшее обр
@dp.callback_query_handler(text="cat_vp")
async def cat_v(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text='Укажите свой стаж работы по специальности', reply_markup=ex_work)
#мало стажа
INFO_TEXT_18='''К сожалению Вы не можете претендовать на получение категории в этом году. Минимальный стаж необходимый для получения второй категории составляет:
2 года опыта для среднего медперсонала, и 3 года для высшего.
Вы можете посмотреть дополнительную информацию о категориях ниже.
'''
@dp.callback_query_handler(text=('less_3','less_2'))
async def no_enog(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_18, reply_markup=end_btn_9)

INFO_TEXT_24='''Аттестация на категорию проходит следующим образом. Вам необходимо собрать пакет документов, написать отчет о своей профессиональной деятельности и подготовиться к тестированию и собеседованию. В ходе тестирования специалист отвечает на теоретические и практические вопросы по своей специальности с вариантами ответов. В ходе собеседования комиссия обсуждает с претендентом отчет о его профессиональной деятельности и задает дополнительные вопросы по специальности.
Аттестация проходит в Вашей территориальной комиссии, у каждой комиссии могут быть свои варианты тестирования и дополнительные вопросы.
'''
@dp.callback_query_handler(text='promp_4')
async def pr_4(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_24, reply_markup=end_btn_14)

#норм стажа
INFO_TEXT_19 = '''Вы можете претендовать на получение категории. Категории выдаются последовательно, поэтому начать стоит со второй категории.
Вам необходимо собрать пакет документов, написать отчет о своей профессиональной деятельности и подготовиться к тестированию и собеседованию. В ходе тестирования специалист отвечает на теоретические и практические вопросы по своей специальности с вариантами ответов. В ходе собеседования комиссия обсуждает с претендентом отчет о его профессиональной деятельности и задает дополнительные вопросы по специальности.
Аттестация проходит в Вашей территориальной комиссии, у каждой комиссии могут быть свои варианты тестирования и дополнительные вопросы.
'''
@dp.callback_query_handler(text=('3_5','5_7','more_7','2_5','5_8','more_8'))
async def enog(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, 
    text=INFO_TEXT_19, reply_markup=end_btn_10)

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
    text='Какой вид аккредитации Вас интересует?', reply_markup=accred_menu)

#БЛОК - ОСТАВИТЬ ЗАЯВКУ - ДА ---------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text = "send_text")
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
    Вы можете прописать его вручную в формате 1112223344'''
    await bot.send_message(message.from_user.id, answer)
    await ProfilestatesGroup.telefon.set()

@dp.message_handler(lambda message: not message.text.isdigit(), state=ProfilestatesGroup.telefon)
async def chek_num(message: types.Message):
    await message.answer('Пожалуйста, укажите номер телефона в формате 1112223344 без дополнительных символов и пробелов')
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

#ПОДСКАЗКИ - были, стали просто кнопками
@dp.callback_query_handler(text='promp_2')
async def pr_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text='Список документов: 1. 2. 3. ', show_alert=True) #дополнить

@dp.callback_query_handler(text='promp_3')
async def pr_3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text='Список документов для категории: 1. 2. 3. ', show_alert=True) #дополнить

#ФАЙЛЫ
#файл через систему
@dp.callback_query_handler(text = 'gid') # файл должен лежать в той же папке, что и прога бота
async def send_file(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)    
    await bot.send_message(callback_query.from_user.id, text='Ожидайте, формирую файл для скачивания')
    with open('Гайд_по_периодической_аккредитации_и_портфолио_2022.pdf', 'rb') as file:
        await callback_query.message.answer_document(file)
        await bot.send_message(callback_query.from_user.id, text = 'Если остались вопросы: напишите нам или продолжайте работу с ботом', reply_markup=end_btn)

#файл 2 через систему
@dp.callback_query_handler(text = 'gid_2') # файл должен лежать в той же папке, что и прога бота
async def send_file_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)    
    await bot.send_message(callback_query.from_user.id, text='Ожидайте, формирую файл для скачивания')
    with open('Гайд по видам аккредитации.pdf', 'rb') as file:
        await callback_query.message.answer_document(file)
        await bot.send_message(callback_query.from_user.id, text = 'Если остались вопросы: напишите нам или продолжайте работу с ботом', reply_markup=end_btn)

#файл - через скачивание из яндекса
    
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