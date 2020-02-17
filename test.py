import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import time


# Открытие веб - драйвера в расписании текущего месяца. 
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

# Отработка взаимодействия нажатий на стрелочки в цикле влево
#arrow_left_element_xpath_code = "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='mount-cont']/span[@class='arrow-left']"
#arrow_left_element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, arrow_left_element_xpath_code)))
#arrow_left_element.click()

# Отработка взаимодейсвтий нажатий на стрелочку в цикле вправо
arrow_right_element_xpath_code = "/html/body/mystat/ng-component/ng-component/div[@class='wrap']/div[@class='content']/div[@class='wrapper']/ng-component/ng-component/div[@class='schedule-section']/div[@class='row']/div[@class='col-md-12 item']/div[@class='content-schedule']/div[@class='mount-cont']/span[@class='arrow-right']"

# Отработка цикла нажатий стрелочек
for i in range(2):
    arrow_right_element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, arrow_right_element_xpath_code)))
    arrow_right_element.click()
    sleep(5)

sleep(15)
driver.quit()