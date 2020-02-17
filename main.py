import datetime
import time

import telebot
from telebot import types

import inline_calendar
from inline_calendar import get_callback_next_month, get_callback_prev_month, set_down_all_markers

import tokens
import config
import dbworker
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep


from sqlite_db_worker import init_db
from sqlite_db_worker import add_message
from sqlite_db_worker import count_messages
from sqlite_db_worker import list_messages
from sqlite_db_worker import user_id_in_base
from sqlite_db_worker import list_of_user_ids

import datetime
import calendar

# Объявление переменных
bot = telebot.TeleBot(token=tokens.telegram)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

AUTHOR_ID = 186928299

login_mystat = ''
pass_mystat = ''

CLICKED_BY = []

now = datetime.datetime.now()

#Объявление смайлов для работы бота
Hihi = u'\U0001F601'

@bot.message_handler(commands=["start"])
def mystat_login(message):
    if user_id_in_base(user_id=message.chat.id) == False:
        add_message(user_id=message.chat.id, text=str(message.text))
    bot.send_message(
        message.chat.id, "Классно, что ты решил поработать со Стёпой! Воспользуйся командой /login , чтобы получить "
                         "больше нужных функций!")


#Старт работы с ботом. Функция /login работы с ботом. Отправка сообщения с просьбой ввести логин.
@bot.message_handler(commands=["login"])
def mystat_login(message):
    if user_id_in_base(user_id=message.chat.id) == False:
        add_message(user_id=message.chat.id, text=str(message.text))

    bot.send_message(
        message.chat.id, "Для входа в Mystat вы должны указать Ваш логин и пароль. Введите сначала логин.")
    dbworker.set_state(
        message.chat.id, config.Mystat_logins_steps.S_ENTER_LOGIN_MYSTAT.value)

#Запоминание логина и занесение его в переменную для дальнейшей авторизации. Отправка сообщения введите пароль.
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.Mystat_logins_steps.S_ENTER_LOGIN_MYSTAT.value)
def user_entering_name(message):
    global login_mystat
    login_mystat = message.text
    bot.send_message(
        message.chat.id, "Логин принят. Напишите теперь Ваш пароль.")
    dbworker.set_state(
        message.chat.id, config.Mystat_logins_steps.S_ENTER_PASS_MYSTAT.value)

#Заход в систему майстат. Авторизация пользователя. Вывод меню со статистикой, расписанием ( и т.д. ).
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.Mystat_logins_steps.S_ENTER_PASS_MYSTAT.value)
def user_entering_age(message):
    global pass_mystat
    pass_mystat = message.text
    bot.send_message(
        message.chat.id, "Пароль принят, выполняем вход в систему Mystat.")
    bot.send_message(message.chat.id, "Заходим в систему Mystat с логином: " +
                     str(login_mystat)+" и паролем: "+str(pass_mystat)+".")
    dbworker.set_state(message.chat.id, config.Mystat_logins_steps.S_ENTER_SYSTEM_MYSTAT.value)

    driver = webdriver.Chrome()
    driver.get("https://mystat.itstep.org/")

    login_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'username')))
    login_element.send_keys(str(login_mystat))
    sleep(1)
    pass_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'password')))
    pass_element.send_keys(str(pass_mystat))
    pass_element.submit()
    student_group_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[@class='user-full-name']/span[@class='select-univercity']/span[2]")))
    student_fio_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[@class='user-full-name']/span[@class='profile-link']/a[@class='fio-stud']")))

    bot.send_message(message.chat.id, "Вы авторизованы в Mystat под ФИО: " +
                     str(student_fio_element.text) + ". Учебная группа: " + str(student_group_element.text) + ".")
    sleep(10)
    driver.quit()
    driver = webdriver.Chrome()
    driver.get("https://mystat.itstep.org/ru/main/settings/page/index")
    login_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'username')))
    login_element.send_keys("Kova_pu05")
    sleep(1)
    pass_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'password')))
    pass_element.send_keys("51gB58ZF")
    pass_element.submit()
    percent_profile = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='profile-section']/div[@class='row']/div[@class='col-md-8 item progress-block']/div[@class='conteiner-profile']/div[@class='sum-profile']/div[@class='count-holder']/p[@class='all-count']/span")))
    if str(percent_profile.text) != "100%":
        bot.send_message(message.chat.id, "Эй парень, профиль в Mystat заполнен не полностью!", parse_mode="HTML")
    sleep(5)
    driver.quit()
    markup = types.ReplyKeyboardMarkup()
    markup.row('Расписание', 'Статистика аккаунта')
    markup.row('Отправить жалобу / предложение', 'Контакты', 'Настройки')
    bot.send_message(message.chat.id, "Выберите пункт из доступного меню:", reply_markup=markup)

#Вызов декоратора, если человек нажал в меню кнопку "Расписание". Подключение к расписанию. Вывод инлайн клавиатуры работы с расписанием.
@bot.message_handler(regexp="Расписание")
def shedule_global(message):
    bot.send_message(message.chat.id, "Подключаюсь к Mystat для просмотра расписания..")
    driver = webdriver.Chrome()
    driver.get("https://mystat.itstep.org/ru/main/schedule/page/index")

    login_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'username')))
    login_element.send_keys("Kova_pu05")
    sleep(1)
    pass_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'password')))
    pass_element.send_keys("51gB58ZF")
    pass_element.submit()
    shedule_month = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='mount-cont']/span[@class='mount']")))
    bot.send_message(message.chat.id, "Расписание доступно на: " + str(shedule_month.text))
    cid = message.chat.id
    mid = message.message_id
    uid = message.from_user.id
    shedule_kb = types.InlineKeyboardMarkup()
    click_shedule_button = types.InlineKeyboardButton("Получить расписание на сегодня", callback_data='click_shedule_button')
    shedule_kb.row(click_shedule_button)
    click_month_shedule_button = types.InlineKeyboardButton("Получить расписание в другой день",
                                                      callback_data='click_shedule_month_button')
    shedule_kb.row(click_month_shedule_button)
    bot.send_message(cid, "<b>Что ты хочешь конкретно посмотреть в расписании?</b>", parse_mode="HTML",
                     reply_markup=shedule_kb, disable_web_page_preview=True)
    sleep(10)
    driver.quit()
    
# Вывод декоратора, если человек нажал на кнопку "Получить расписание сегодня." Выводит несколькими сообщениями расписание на сегодня.
@bot.callback_query_handler(func=lambda call: call.data == 'click_shedule_button')
def command_click_inline(call):
    cid = call.message.chat.id
    uid = call.from_user.id
    mid = call.message.message_id

    if uid not in CLICKED_BY:
        CLICKED_BY.append(uid)
        click_kb_edited = types.InlineKeyboardMarkup()
        click_edited = types.InlineKeyboardButton("Расписание на сегодня..", callback_data='clicked')
        click_kb_edited.row(click_edited)
        bot.edit_message_text("<b>Элемент выбран..</b>", cid, mid, reply_markup=click_kb_edited, parse_mode="HTML")
        bot.answer_callback_query(call.id, text="Расписание будет выведено в следующем сообщении,  {}.".format(call.from_user.first_name))

        #Запускаем драйвер, который проверяет сегодня расписание
        driver = webdriver.Chrome()
        driver.get("https://mystat.itstep.org/ru/main/schedule/page/index")

        login_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, 'username')))
        login_element.send_keys("Kova_pu05")
        #sleep(1)
        pass_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, 'password')))
        pass_element.send_keys("51gB58ZF")
        pass_element.submit()

        today_day_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div["
                                            "@class='content']/div[@class='wrapper']/ng-component/ng-component/div["
                                            "@class='schedule-section']/div[@class='row']/div[@class='col-md-12 "
                                            "item']/div[@class='content-schedule']/div[@class='day-holder']/div["
                                            "@class='day has-day is-today']//div[@class='active-day']")))
        today_day_mystat.click()
        #sleep(5)
        element_all_lessons = WebDriverWait(driver, 30).until(
            ec.presence_of_all_elements_located((By.XPATH,
                                                 "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='less-name']")))
        element_all_time = WebDriverWait(driver, 30).until(
            ec.presence_of_all_elements_located((By.XPATH,
                                                 "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='time']")))
        element_all_places = WebDriverWait(driver, 30).until(
            ec.presence_of_all_elements_located((By.XPATH,
                                                 "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='place']/span[@class='num']")))
        element_all_teachers = WebDriverWait(driver, 30).until(
            ec.presence_of_all_elements_located((By.XPATH,
                                                 "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='name-teacher']")))
        for number in range(len(element_all_lessons)):
            bot.send_message(cid, "Лекция: " + element_all_lessons[number].text + ". \nВремя: " + element_all_time[number].text + ". \nАудитория: " + element_all_places[number].text + ". \nПреподователь: " + element_all_teachers[number].text + ".")
        #sleep(5)
        driver.quit()
    else:
        bot.answer_callback_query(call.id, text="Расписание уже выведено!")


#Хендлер вывода статистики ( Осталось: доделать дизайн иконок в выведенном сообщении. Добавить ИИ анализа статистики и выводить правильный разговор Стёпы )
@bot.message_handler(regexp="Статистика аккаунта")
def function_statistics_mystat(message):
    driver = webdriver.Chrome()
    driver.get("https://mystat.itstep.org/ru/main/dashboard/page/index")

    login_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'username')))
    login_element.send_keys("Kova_pu05")
    pass_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'password')))
    pass_element.send_keys("51gB58ZF")
    pass_element.submit()
    sleep(10)
    student_place_in_group = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-12 main-flex-block']/leader-component/div[@class='leader-flex']/div[@class='row']/div[@class='col-md-6 rating-blocks block-item']/div[@class='ratings']/div[@class='inner with-bg']/div[@class='part part-rating']/div[@class='part-container']/div[@class='rating-content']/div[@class='rating rating-group']/div[@class='rating-position']")))
    student_place_in_flow = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-12 main-flex-block']/leader-component/div[@class='leader-flex']/div[@class='row']/div[@class='col-md-6 rating-blocks block-item']/div[@class='ratings']/div[@class='inner with-bg']/div[@class='part part-rating']/div[@class='part-container']/div[@class='rating-content']/div[@class='rating rating-stream']/div[@class='rating-position']")))
    student_academic_in_month = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/progress-component[@class='col-md-6']/div[@class='block-item']/div[@class='inner']/div[@class='part part-progress']/div[@class='part-container']/div[@class='progress-content']/div[@class='progress-part progress-info']/div[@class='row']/div[@class='col-md-4 progress-info-count']/span[@class='middle-count']")))
    student_academic_attendance = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/attendance-component[@class='col-md-6']/div[@class='block-item']/div[@class='inner']/div[@class='part part-attendance']/div[@class='part-container']/div[@class='attendance-part']/div[@class='attendance-content progress-info']/div[@class='row']/div[@class='col-md-4 progress-info-count']/span[@class='middle-count']")))
    mystat_current_homeworks = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-4 block-item end-line-block'][1]/div[@class='inner']/div[@class='part part-homeworks']/div[@class='part-container']/div[@class='homeworks-content']/div[@class='count-holder items']/div[@class='item'][1]/div[@class='item-self'][1]/span[@class='open']")))
    mystat_allready_homeworks = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-4 block-item end-line-block'][1]/div[@class='inner']/div[@class='part part-homeworks']/div[@class='part-container']/div[@class='homeworks-content']/div[@class='count-holder items']/div[@class='item'][1]/div[@class='item-self'][2]/span[@class='done']")))
    mystat_check_homeworks = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-4 block-item end-line-block'][1]/div[@class='inner']/div[@class='part part-homeworks']/div[@class='part-container']/div[@class='homeworks-content']/div[@class='count-holder items']/div[@class='item'][2]/div[@class='item-self'][1]/span[@class='inspection']")))
    mystat_dead_homeworks = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-4 block-item end-line-block'][1]/div[@class='inner']/div[@class='part part-homeworks']/div[@class='part-container']/div[@class='homeworks-content']/div[@class='count-holder items']/div[@class='item'][2]/div[@class='item-self'][2]/span[@class='lose']")))
    mystat_stepcoins = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[3]/span[@id='all-pricess']/span[@class='count-item']")))
    mystat_crystalls = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[3]/span[@class='wrap-counts']/span[@id='all-christal']/span[@class='count-item']")))
    mystat_coins = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[3]/span[@class='wrap-counts']/span[@id='all-coin']/span[@class='count-item']")))
    mystat_badges = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[3]/span[@class='wrap-counts']/span[@id='all-badges']")))
    bot.send_message(
        message.chat.id, "Место в группе: " + str(student_place_in_group.text) +
                         "\nМесто на потоке: " + str(student_place_in_flow.text) +
                         "\nУспеваемость в этом месяце: " + str(student_academic_in_month.text) +
                         "\nПосещаемость в этом месяце: " + str(student_academic_attendance.text) +
                         "\nСтепкоины: " + str(mystat_stepcoins.text) +
                         "\nКристаллы: " + str(mystat_crystalls.text) +
                         "\nКоины: " + str(mystat_coins.text) +
                         "\nБэйджи: " + str(mystat_badges.text) +
                         "\nПросроченные домашние задания: " + str(mystat_dead_homeworks.text), parse_mode="HTML")
    driver.quit()

#По слову "Контакты" ( кнопка в главном меню ) выводит из майстата контакты учебной части, приёмной и авторов бота
@bot.message_handler(regexp="Контакты")
def shedule_global(message):
    driver = webdriver.Chrome()
    driver.get("https://mystat.itstep.org/ru/main/contacts/page/index")
    login_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'username')))
    login_element.send_keys("Kova_pu05")
    sleep(1)
    pass_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'password')))
    pass_element.send_keys("51gB58ZF")
    pass_element.submit()
    study_mystat_telephone = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='contacts-section']/div[@class='row']/div[@class='col-md-4 item'][2]/div[@class='contacts-block']/div[@class='left-contact-block']/div[@class='contacts phone']")))
    study_mystat_url = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='contacts-section']/div[@class='row']/div[@class='col-md-4 item'][2]/div[@class='contacts-block']/div[@class='left-contact-block']/div[@class='contacts address']/div[@class='name training-name-address']/div[@class='contacts-content street']/span[1]/a")))
    reception_mystat_adress = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='contacts-section']/div[@class='row']/div[@class='col-md-4 item'][1]/div[@class='contacts-block']/div[@class='contacts address']/div[@class='name name-address']/div[@class='contacts-content street']/span[1]")))
    reception_mystat_adress_2 = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='contacts-section']/div[@class='row']/div[@class='col-md-4 item'][1]/div[@class='contacts-block']/div[@class='contacts address']/div[@class='name name-address']/div[@class='contacts-content street']/span[2]")))
    reception_mystat_contact_1 = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='contacts-section']/div[@class='row']/div[@class='col-md-4 item'][1]/div[@class='contacts-block']/div[@class='contacts phone']/div[@class='name name-phone']/div[@class='contacts-content number']/span[1]")))
    reception_mystat_contact_2 = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='contacts-section']/div[@class='row']/div[@class='col-md-4 item'][1]/div[@class='contacts-block']/div[@class='contacts phone']/div[@class='name name-phone']/div[@class='contacts-content number']/span[2]")))
    reception_mystat_contact_3 = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='contacts-section']/div[@class='row']/div[@class='col-md-4 item'][1]/div[@class='contacts-block']/div[@class='contacts phone']/div[@class='name name-phone']/div[@class='contacts-content number']/span[3]")))
    bot.send_message(message.chat.id,
                     "Учёбная часть: "
                     "\nСайт: " + str(study_mystat_url.text) +
                     "\nТелефон: " + str(study_mystat_telephone.text) +
                     "\n\nПриёмная: "
                     "\nАдрес: " + str(reception_mystat_adress.text) +
                     "\nАдрес 2: " + str(reception_mystat_adress_2.text) +
                     "\nТелефон 1: " + str(reception_mystat_contact_1.text) +
                     "\nТелефон 2: " + str(reception_mystat_contact_2.text) +
                     "\nТелефон 3: " + str(reception_mystat_contact_3.text) +
                     "\n\nСоздатели бота ( написать свои предложения ) :" +
                     "\nВова Ковальчук: @kovalchuk_vova" +
                     "\nБорис Пономаренко: @PanamBoor" +
                     "\n\nBoris - IT company Group 2019")
    sleep(10)
    driver.quit()


@bot.message_handler(regexp="Отправить жалобу / предложение")
def mystat_report(message):
    bot.send_message(message.chat.id, "Раздел отправки жалоб и предложений в учебную часть ШАГа")


    cid = message.chat.id
    mid = message.message_id
    uid = message.from_user.id
    click_kb = types.InlineKeyboardMarkup()
    mystat_report_button = types.InlineKeyboardButton("Хочу отправить жалобу", callback_data='mystat_report_button_clicked')
    mystat_prepose_button = types.InlineKeyboardButton("Хочу отправить предложение", callback_data='mystat_prepose_button_clicked')
    click_kb.row(mystat_report_button)
    click_kb.row(mystat_prepose_button)
    bot.send_message(cid, "<b>И что ты решил отправлять в учёбную часть?</b>", parse_mode="HTML",
                     reply_markup=click_kb, disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data == 'mystat_report_button_clicked')
def command_click_inline(call):
    cid = call.message.chat.id
    uid = call.from_user.id
    mid = call.message.message_id
    #Редактируем кнопки
    if uid not in CLICKED_BY:
        CLICKED_BY.append(uid)
        click_kb_edited = types.InlineKeyboardMarkup()
        click_edited = types.InlineKeyboardButton("Напишите в следующем сообщении полный текст Вашей жалобы..", callback_data='mystat_report_button_clicked')
        click_kb_edited.row(click_edited)
        bot.edit_message_text("<b>Выбран элемент отправки жалобы..</b>", cid, mid, reply_markup=click_kb_edited, parse_mode="HTML")
        bot.answer_callback_query(call.id, text="Расписание будет выведено в следующем сообщении,  {}.".format(call.from_user.first_name))
        #основная функция работы с жалобой


        driver = webdriver.Chrome()
        driver.get("https://mystat.itstep.org/ru/main/signal/page/index")

        login_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, 'username')))
        login_element.send_keys("Kova_pu05")
        sleep(1)
        pass_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, 'password')))
        pass_element.send_keys("51gB58ZF")
        pass_element.submit()
        mystat_text_report = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='signal-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='signal-form-container']/div[@class='body-form']/form[@class='ng-invalid ng-dirty ng-touched']/div[@class='form-group'][3]/textarea[@class='form-control ng-pristine ng-invalid ng-touched']")))
        sleep(10)
        driver.quit()
    else:
        bot.answer_callback_query(call.id, text="Напишите текст жалобы в следующем сообщении и отправьте его мне!")


@bot.message_handler(regexp="Настройки")
def settings_stepa(message):
    bot.send_message(message.chat.id, "Вы в настройках..")
    cid = message.chat.id
    mid = message.message_id
    uid = message.from_user.id
    click_kb = types.InlineKeyboardMarkup()
    exit_mystat = types.InlineKeyboardButton("Выйти из учётной записи майстат", callback_data='exit_mystat_clicked')
    click_kb.row(exit_mystat)
    bot.send_message(cid, "<b>Вы находитесь в меню раздела настроек: </b>", parse_mode="HTML",
                     reply_markup=click_kb, disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data == 'exit_mystat_clicked')
def command_click_inline(call):
    cid = call.message.chat.id
    uid = call.from_user.id
    mid = call.message.message_id
    #Редактируем кнопки
    if uid not in CLICKED_BY:
        CLICKED_BY.append(uid)
        click_kb_edited = types.InlineKeyboardMarkup()
        click_edited = types.InlineKeyboardButton("Проивзодится выход из системы Mystat..", callback_data='exit_mystat_clicked')
        click_kb_edited.row(click_edited)
        bot.edit_message_text("<b>Вы выбрали выйти из майстат</b>", cid, mid, reply_markup=click_kb_edited, parse_mode="HTML")
        bot.answer_callback_query(call.id, text="Выходим из майстата,  {}.".format(call.from_user.first_name))

        #основная функция работы с жалобой
        global login_mystat
        global pass_mystat
        login_mystat = ""
        pass_mystat = ""
        bot.send_message(cid, "Выход из майстат проведён успешно.. Зайти обратно можно за счёт команды /login ")
    else:
        bot.answer_callback_query(call.id, text="Я уже вышел из учётной записи майстат!")

        
@bot.message_handler(commands=["author"])
def author_function(message):
    if message.from_user.id == AUTHOR_ID:
        bot.send_message(message.chat.id, "Это сообщение от автора! Ответь следующим сообщением, что ты хочешь"
                                          "разослать всем пользователям")
        dbworker.set_state(
            message.chat.id, config.Mystat_logins_steps.S_AUTHOR_START.value)
    else:
        bot.send_message(message.chat.id, "Хей, у тебя нет прав автора!")


@bot.callback_query_handler(func=lambda call: call.data == 'click_shedule_month_button')
def command_click_inline_shedule_month_button(call):
    cid = call.message.chat.id
    uid = call.from_user.id
    mid = call.message.message_id
    inline_calendar.init(uid,
                         datetime.date.today(),
                         datetime.date(year=2018, month=11, day=1),
                         datetime.date(year=2020, month=12, day=31))
    bot.send_message(uid, text='Введите нужную Вам дату: ', reply_markup=inline_calendar.get_keyboard(uid))

@bot.callback_query_handler(func=inline_calendar.is_inline_calendar_callbackquery)
def calendar_callback_handler(q: types.CallbackQuery):
    bot.answer_callback_query(q.id)
    
    arrow_right_element_xpath_code = "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='mount-cont']/span[@class='arrow-right']"
    arrow_left_element_xpath_code = "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='mount-cont']/span[@class='arrow-left']"


    try:
        return_data = inline_calendar.handler_callback(q.from_user.id, q.data)
        if return_data is None:
            print(return_data)
            print(get_callback_prev_month())
            print(get_callback_next_month())
            bot.edit_message_reply_markup(chat_id=q.from_user.id, message_id=q.message.message_id,
                                          reply_markup=inline_calendar.get_keyboard(q.from_user.id))
            # В браузере кликать на изменение месяца
            if get_callback_prev_month() == 1:
                print('Я нажал стрелочку влево')

            if get_callback_next_month() == 1:
                print('Я нажал стрелочку вправо')

        else:
            picked_data = return_data
            print(picked_data)
            print(picked_data.day)
            bot.edit_message_text(text='Выводим расписание лент на выбранную дату: {0}'.format(picked_data), chat_id=q.from_user.id, message_id=q.message.message_id)
            # Вывод пар на выбранную человеком дату.

            # Нахождение дня по выбранному дню месяца и открытие его
            find_date_day = "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='day-holder']/div[@class='day has-day'][{}]//div[@class='active-day']".format(picked_data.day)
            print(find_date_day)

            # Подсчёт изменения месяца у человека в работе с календарём
            current_month_counter = 0
            arrow_element_road = 0 # 0 - текущий месяц, 1 - месяца назад, 2 - месяца вперёд

            #Введение str(picked_data.day)>today_day_mystat.text переменных
            if get_callback_next_month()>get_callback_prev_month():
                # Подсчёт стрелок, если месяц следующий
                print("Стрелок вправо больше, чем стрелок влево")
                current_month_counter = get_callback_next_month()-get_callback_prev_month()
                print ("current_month_counter = " + str(current_month_counter))
                arrow_element_road = 1
                print ("arrow_element_road = " + str(arrow_element_road))


                                #Открываем драйвер и заходим в расписание
                # Открытие веб - драйвера в расписании текущего месяца. 
                driver = webdriver.Chrome()
                driver.get("https://mystat.itstep.org/ru/main/schedule/page/index")

                login_element = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, 'username')))
                login_element.send_keys("Kova_pu05")
                pass_element = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, 'password')))
                pass_element.send_keys("51gB58ZF")
                pass_element.submit()

                # Доходим до выбранного пользователя месяца

                for i in range(current_month_counter):
                    arrow_right_element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, arrow_right_element_xpath_code)))
                    arrow_right_element.click()
                    sleep(5)

                # Выводим пары по дню, который он выбрал 
                # Выгрузка из find_date информации о парах (default как мы достаём данные о парах)
                find_date_day_xpath = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH,str(find_date_day))))
                find_date_day_xpath.click()
                element_all_lessons = WebDriverWait(driver, 30).until(
                    ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='less-name']")))
                element_all_time = WebDriverWait(driver, 30).until(
                    ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='time']")))
                element_all_places = WebDriverWait(driver, 30).until(
                    ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='place']/span[@class='num']")))
                element_all_teachers = WebDriverWait(driver, 30).until(
                    ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='name-teacher']")))
                for number in range(len(element_all_lessons)):
                    bot.send_message(q.from_user.id, "Лекция: " + element_all_lessons[number].text + ". \nВремя: " + element_all_time[number].text + ". \nАудитория: " + element_all_places[number].text + ". \nПреподователь: " + element_all_teachers[number].text + ".")
            
                # Закрываем драйвер и снимаем все маркеры
                set_down_all_markers()
                driver.quit()


            elif get_callback_next_month()==get_callback_prev_month():
                # Подсчёт стрелок, если месяц текущий
                print("Человек остановился на текущем месте")
                current_month_counter = 0
                print ("current_month_counter = " + str(current_month_counter))
                arrow_element_road = 0
                print ("arrow_element_road = " + str(arrow_element_road))

                # Открытие веб - драйвера в расписании текущего месяца. 
                driver = webdriver.Chrome()
                driver.get("https://mystat.itstep.org/ru/main/schedule/page/index")

                login_element = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, 'username')))
                login_element.send_keys("Kova_pu05")
                pass_element = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, 'password')))
                pass_element.send_keys("51gB58ZF")
                pass_element.submit()

                # Проверка выбранный день совпадает с has-day is today?
                today_day_mystat = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH,
                                    "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='day-holder']/div[@class='day has-day is-today']//div[@class='active-day']")))


                print("Find has day is today = " + today_day_mystat.text)
                today_int_day_mystat = int(today_day_mystat.text)

                if picked_data.day==today_int_day_mystat:
                    print("Человек выбрал сегодняшний день!")
                    today_day_mystat.click()
                    element_all_lessons = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='less-name']")))
                    element_all_time = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='time']")))
                    element_all_places = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='place']/span[@class='num']")))
                    element_all_teachers = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='name-teacher']")))
                    for number in range(len(element_all_lessons)):
                        bot.send_message(q.from_user.id, "Лекция: " + element_all_lessons[number].text + ". \nВремя: " + element_all_time[number].text + ". \nАудитория: " + element_all_places[number].text + ". \nПреподователь: " + element_all_teachers[number].text + ".")
            
                    # Закрываем драйвер и снимаем все маркеры
                    set_down_all_markers()
                    driver.quit()

                elif picked_data.day>today_int_day_mystat:
                    print("Человек выбрал какой - то другой день в этом месяце, но не сегодняшний!")
                    # Проверка это день перед или после has-day is today?
                    print(str(picked_data.day) + " ? " + today_day_mystat.text)
                    print("Человек выбрал день, который идёт после текущего дня!")
                    find_date_day = "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='day-holder']/div[@class='day has-day'][{}]//div[@class='active-day']".format(picked_data.day-1)

                    print(find_date_day)
                    find_date_day_xpath = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.XPATH,str(find_date_day))))
                    find_date_day_xpath.click()
                    element_all_lessons = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='less-name']")))
                    element_all_time = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='time']")))
                    element_all_places = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='place']/span[@class='num']")))
                    element_all_teachers = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='name-teacher']")))
                    for number in range(len(element_all_lessons)):
                        bot.send_message(q.from_user.id, "Лекция: " + element_all_lessons[number].text + ". \nВремя: " + element_all_time[number].text + ". \nАудитория: " + element_all_places[number].text + ". \nПреподователь: " + element_all_teachers[number].text + ".")
            
                    # Закрываем драйвер и снимаем все маркеры
                    set_down_all_markers()
                    driver.quit()
                elif picked_data.day<today_int_day_mystat:
                    print("Человек выбрал день перед текущим в этом месяце!")
                    find_date_day_xpath = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.XPATH,str(find_date_day))))
                    find_date_day_xpath.click()
                    element_all_lessons = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='less-name']")))
                    element_all_time = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='time']")))
                    element_all_places = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='place']/span[@class='num']")))
                    element_all_teachers = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='name-teacher']")))
                    for number in range(len(element_all_lessons)):
                        bot.send_message(q.from_user.id, "Лекция: " + element_all_lessons[number].text + ". \nВремя: " + element_all_time[number].text + ". \nАудитория: " + element_all_places[number].text + ". \nПреподователь: " + element_all_teachers[number].text + ".")
            
                    # Закрываем драйвер и снимаем все маркеры
                    set_down_all_markers()
                    driver.quit()

            else:

                # Подсчёт стрелок, если месяц предыдущий
                print("Больше стрелок влево, чем вправо")
                current_month_counter = get_callback_prev_month()-get_callback_next_month()
                print(current_month_counter)
                print ("current_month_counter = " + str(current_month_counter))
                arrow_element_road = 2
                print ("arrow_element_road = " + str(arrow_element_road))

                #Открываем драйвер и заходим в расписание
                # Открытие веб - драйвера в расписании текущего месяца. 
                driver = webdriver.Chrome()
                driver.get("https://mystat.itstep.org/ru/main/schedule/page/index")

                login_element = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, 'username')))
                login_element.send_keys("Kova_pu05")
                pass_element = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.ID, 'password')))
                pass_element.send_keys("51gB58ZF")
                pass_element.submit()

                # Доходим до выбранного пользователя месяца

                for i in range(current_month_counter):
                    arrow_left_element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, arrow_left_element_xpath_code)))
                    arrow_left_element.click()
                    sleep(5)

                # Выводим пары по дню, который он выбрал 
                # Выгрузка из find_date информации о парах (default как мы достаём данные о парах)
                find_date_day_xpath = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH,str(find_date_day))))
                find_date_day_xpath.click()
                element_all_lessons = WebDriverWait(driver, 30).until(
                    ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='less-name']")))
                element_all_time = WebDriverWait(driver, 30).until(
                    ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='time']")))
                element_all_places = WebDriverWait(driver, 30).until(
                    ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='place']/span[@class='num']")))
                element_all_teachers = WebDriverWait(driver, 30).until(
                    ec.presence_of_all_elements_located((By.XPATH,
                                                     "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='name-teacher']")))
                for number in range(len(element_all_lessons)):
                    bot.send_message(q.from_user.id, "Лекция: " + element_all_lessons[number].text + ". \nВремя: " + element_all_time[number].text + ". \nАудитория: " + element_all_places[number].text + ". \nПреподователь: " + element_all_teachers[number].text + ".")
            
                # Закрываем драйвер и снимаем все маркеры
                set_down_all_markers()
                driver.quit()



    except inline_calendar.WrongChoiceCallbackException:
        bot.edit_message_text(text='Вы нажали что - то запрещённое..', chat_id=q.from_user.id, message_id=q.message.message_id,
                              reply_markup=inline_calendar.get_keyboard(q.from_user.id))

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.Mystat_logins_steps.S_AUTHOR_START.value)
def send_message_all_function(message):
    blog_text = message.text
    for id in list_of_user_ids():
        bot.send_message(id[0], str(blog_text))
        sleep(5)


#Вызов test команды
@bot.message_handler(commands=["test"])
def test_function_name(message):
    driver = webdriver.Chrome()
    sleep(5)
    driver.quit()

# Обновляем запросы по сообщениям
while True:
    try:
        bot.polling(none_stop=True, interval=2)
        break
    except Exception as ex:
        print(ex)
        bot.stop_polling()
        time.sleep(15)

