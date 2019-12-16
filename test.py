import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import time


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