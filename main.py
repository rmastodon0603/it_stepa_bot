import datetime

import telebot
from telebot import types

import tokens
import config
import dbworker
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep

# Объявление переменных
bot = telebot.TeleBot(token=tokens.telegram)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

login_mystat = ''
pass_mystat = ''

CLICKED_BY = []

now = datetime.datetime.now()

#Объявление смайлов для работы бота
Hihi = u'\U0001F601'

#Старт работы с ботом. Функция /login работы с ботом. Отправка сообщения с просьбой ввести логин.
@bot.message_handler(commands=["login"])
def mystat_login(message):
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
    markup.row('Отправить жалобу / предложение', 'Контакты', 'Настройки ( персонализировать бота )')
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
    click_kb = types.InlineKeyboardMarkup()
    click_button = types.InlineKeyboardButton("Получить расписание на сегодня", callback_data='clicked')
    click_kb.row(click_button)
    bot.send_message(cid, "<b>Что ты хочешь конкретно посмотреть в расписании?</b>", parse_mode="HTML",
                     reply_markup=click_kb, disable_web_page_preview=True)
    sleep(10)
    driver.quit()

# Вывод декоратора, если человек нажал на кнопку "Получить расписание сегодня." Выводит несколькими сообщениями расписание на сегодня.
@bot.callback_query_handler(func=lambda call: call.data == 'clicked')
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
        sleep(1)
        pass_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, 'password')))
        pass_element.send_keys("51gB58ZF")
        pass_element.submit()
        shedule_month = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            '//div[@class="mount-cont"]//span[text()="Декабрь 2019"]')))
        bot.send_message(cid, "Расписание доступно на: " + str(shedule_month.text))
        today_day_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='day-holder']/div[@class='day has-day is-today']//div[@class='active-day']")))
        today_day_mystat.click()
        sleep(5)
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
        sleep(5)
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
    sleep(1)
    pass_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'password')))
    pass_element.send_keys("51gB58ZF")
    pass_element.submit()

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
    sleep(5)
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

#Вызов test команды
@bot.message_handler(commands=["test"])
def test_function_name(message):
    driver = webdriver.Chrome()
    sleep(5)
    driver.quit()

"""
@bot.message_handler(regexp="Контакты")
def shedule_global(message):
"""

# Обновляем запросы по сообщениям
if __name__ == '__main__':
    bot.polling(none_stop=True)


