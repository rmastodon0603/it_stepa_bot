# Вывод активных дней в расписании
"""
element = WebDriverWait(driver, 30).until(
    ec.presence_of_all_elements_located((By.XPATH, "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='day-holder']//div[@class='active-day']")))
for date in element:
    print(date.text)
    """

# Вывод полного списка названий пар ( сегодня )
"""
today_day_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='day-holder']/div[@class='day has-day is-today']//div[@class='active-day']")))
today_day_mystat.click()
sleep(5)
element_all_lessons = WebDriverWait(driver, 30).until(
    ec.presence_of_all_elements_located((By.XPATH, "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='less-name']")))
element_all_time = WebDriverWait(driver, 30).until(
    ec.presence_of_all_elements_located((By.XPATH, "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='time']")))
element_all_places = WebDriverWait(driver, 30).until(
    ec.presence_of_all_elements_located((By.XPATH,"/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='time-place']/span[@class='place']/span[@class='num']")))
element_all_teachers = WebDriverWait(driver, 30).until(
    ec.presence_of_all_elements_located((By.XPATH,"/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons']/span[@class='name-teacher']")))
for number in range(len(element_all_lessons)):
    print (number)
    print(element_all_lessons[number].text)
    print(element_all_time[number].text)
    print(element_all_places[number].text)
    print(element_all_teachers[number].text)
sleep(10)
driver.quit()
    """

# Вывод "Во сколько первая пара сегодня?"
"""        today_lection_name_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons'][1]/span[@class='less-name']")))
        today_lection_time_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons'][1]/span[@class='time-place']/span[@class='time']")))
        today_lection_auditore_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons'][1]/span[@class='time-place']/span[@class='place']/span[@class='num']")))
        today_lection_teacher_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='on-hover']/div[@class='lessons'][1]/span[@class='name-teacher']")))
        """

# Код для авторизации ( со своим логином и паролем ) в майстат ( ссылка )
"""driver = webdriver.Chrome()
driver.get("https://mystat.itstep.org/ru/main/schedule/page/index")

login_element = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.ID, 'username')))
login_element.send_keys("Kova_pu05")
sleep(1)
pass_element = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.ID, 'password')))
pass_element.send_keys("51gB58ZF")
pass_element.submit()"""

#Пути xpath для наград на главной странице ( выводит пустую строку, кроме даты )
"""last_nagrada_date_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-12 main-flex-block']/div[@id='block-item-gaming']/div[@class='inner']/div[@class='part part-history']/div[@class='part-container']/div[@class='history-content']/ul/div[@class='history-item']/div[1]/li/p[@class='history-date']")))
last_nagrada_name_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-12 main-flex-block']/div[@id='block-item-gaming']/div[@class='inner']/div[@class='part part-history']/div[@class='part-container']/div[@class='history-content']/ul/div[@class='history-item']/div[1]/li/p[@class='name-achive your-awords']/span[1]")))
last_nagrada_qual_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-12 main-flex-block']/div[@id='block-item-gaming']/div[@class='inner']/div[@class='part part-history']/div[@class='part-container']/div[@class='history-content']/ul/div[@class='history-item']/div[1]/li/p[@class='name-achive your-awords']/span[@class='float-right point']")))
last_nagrada_qualandname_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-12 main-flex-block']/div[@id='block-item-gaming']/div[@class='inner']/div[@class='part part-history']/div[@class='part-container']/div[@class='history-content']/ul/div[@class='history-item']/div[1]/li/p[@class='name-achive your-awords']/span")))
last_nagrada_allli_mystat = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-12 main-flex-block']/div[@id='block-item-gaming']/div[@class='inner']/div[@class='part part-history']/div[@class='part-container']/div[@class='history-content']/ul/div[@class='history-item']/div[1]/li/p[@class='name-achive your-awords']")))
print(str(last_nagrada_allli_mystat.text))
print(str(last_nagrada_qualandname_mystat.text))
print(str(last_nagrada_date_mystat.text))
print(str(last_nagrada_name_mystat.text))
print(str(last_nagrada_qual_mystat.text))
sleep(10)
driver.quit()"""

#Полный наход статистики аккаунта на майстат
"""import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import time


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
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-12 main-flex-block']/leader-component/div[@class='leader-flex']/div[@class='row']/div[@class='col-md-6 rating-blocks block-item']/div[@class='ratings']/div[@class='inner with-bg']/div[@class='part part-rating']/div[@class='part-container']/div[@class='rating-content']/div[@class='rating rating-group']/div[@class='rating-position']")))
student_place_in_flow = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-12 main-flex-block']/leader-component/div[@class='leader-flex']/div[@class='row']/div[@class='col-md-6 rating-blocks block-item']/div[@class='ratings']/div[@class='inner with-bg']/div[@class='part part-rating']/div[@class='part-container']/div[@class='rating-content']/div[@class='rating rating-stream']/div[@class='rating-position']")))
student_academic_in_month = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/progress-component[@class='col-md-6']/div[@class='block-item']/div[@class='inner']/div[@class='part part-progress']/div[@class='part-container']/div[@class='progress-content']/div[@class='progress-part progress-info']/div[@class='row']/div[@class='col-md-4 progress-info-count']/span[@class='middle-count']")))
student_academic_attendance = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/attendance-component[@class='col-md-6']/div[@class='block-item']/div[@class='inner']/div[@class='part part-attendance']/div[@class='part-container']/div[@class='attendance-part']/div[@class='attendance-content progress-info']/div[@class='row']/div[@class='col-md-4 progress-info-count']/span[@class='middle-count']")))
mystat_current_homeworks = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-4 block-item end-line-block'][1]/div[@class='inner']/div[@class='part part-homeworks']/div[@class='part-container']/div[@class='homeworks-content']/div[@class='count-holder items']/div[@class='item'][1]/div[@class='item-self'][1]/span[@class='open']")))
mystat_allready_homeworks = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-4 block-item end-line-block'][1]/div[@class='inner']/div[@class='part part-homeworks']/div[@class='part-container']/div[@class='homeworks-content']/div[@class='count-holder items']/div[@class='item'][1]/div[@class='item-self'][2]/span[@class='done']")))
mystat_check_homeworks = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-4 block-item end-line-block'][1]/div[@class='inner']/div[@class='part part-homeworks']/div[@class='part-container']/div[@class='homeworks-content']/div[@class='count-holder items']/div[@class='item'][2]/div[@class='item-self'][1]/span[@class='inspection']")))
mystat_dead_homeworks = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-4 block-item end-line-block'][1]/div[@class='inner']/div[@class='part part-homeworks']/div[@class='part-container']/div[@class='homeworks-content']/div[@class='count-holder items']/div[@class='item'][2]/div[@class='item-self'][2]/span[@class='lose']")))
mystat_stepcoins = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[3]/span[@id='all-pricess']/span[@class='count-item']")))
mystat_crystalls = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[3]/span[@class='wrap-counts']/span[@id='all-christal']/span[@class='count-item']")))
mystat_coins = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[3]/span[@class='wrap-counts']/span[@id='all-coin']/span[@class='count-item']")))
mystat_badges = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='pos-f-t']/top-pane/nav[@class='navbar navbar-expand-lg justify-content-between']/div[@class='left-block']/span[3]/span[@class='wrap-counts']/span[@id='all-badges']")))



print(str(student_place_in_group.text))
print(str(student_place_in_flow.text))
print(str(student_academic_in_month.text))
print(str(student_academic_attendance.text))
print(str(mystat_current_homeworks.text))
print(str(mystat_allready_homeworks.text))
print(str(mystat_check_homeworks.text))
print(str(mystat_dead_homeworks.text))
print(str(mystat_stepcoins.text))
print(str(mystat_crystalls.text))
print(str(mystat_coins.text))
print(str(mystat_badges.text))"""

#Пример проверки наличие нового домашнего задания
"""import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import time


old_mystat_current_homeworks = ""

while True:
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
    mystat_current_homeworks = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='container-fluid homepage-wrapper']/div[@class='row']/div[@class='col-md-4 block-item end-line-block'][1]/div[@class='inner']/div[@class='part part-homeworks']/div[@class='part-container']/div[@class='homeworks-content']/div[@class='count-holder items']/div[@class='item'][1]/div[@class='item-self'][1]/span[@class='open']")))

    if mystat_current_homeworks.text == old_mystat_current_homeworks:
        print("Ничего не изменилось")
    else:
        print("Появилась новая домашка")
        old_mystat_current_homeworks = mystat_current_homeworks.text
    driver.quit()
    time.sleep(20)



sleep(10)
driver.quit()"""

#Перенос текста на новую строку
"""bot.send_message(
        message.chat.id, "Для входа в Mystat вы должны указать Ваш логин и пароль. \nВведите сначала логин.\n", parse_mode="HTML")
        """

#Фукнция проверки новой новости и вывода подробной информации ( Недоделанная кнопка вывода "Подробнее" )
"""
old_mystat_news = ""

while True:
    driver = webdriver.Chrome()
    driver.get("https://mystat.itstep.org/ru/main/news/page/index")

    login_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'username')))
    login_element.send_keys("Kova_pu05")
    sleep(1)
    pass_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'password')))
    pass_element.send_keys("51gB58ZF")
    pass_element.submit()
    mystat_last_news = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH,"/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='news-section']/div[@class='row']/div[@class='col-md-4 item'][1]/div[@class='news-container']/div[@class='logo']")))
    if mystat_last_news.text == old_mystat_news:
        print("Новых новостей нету.")
    else:
        print("Новая новость: " + str(mystat_last_news.text) + " .")
        old_mystat_news = mystat_last_news.text

        #Вывод новости "Подробнее"
        mystat_news_more = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/div[@class='news-section']/div[@class='row']/div[@class='col-md-4 item'][1]/div[@class='news-container']")))
        mystat_news_more.click()
        mystat_news_description = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "/html/body[@class='modal-open']/modal-container[@class='modal fade show']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='big-news-container']")))
        print("Подробная информация о новости: " + str(mystat_news_description.text))
        driver.quit()
        time.sleep(20)
        """

#Объявление отдельных смайлов
"""
#Объявление смайлов для работы бота
Hihi = u'\U0001F601' 
"""