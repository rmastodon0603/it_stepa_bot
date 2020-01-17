# -*- coding: utf-8 -*-

#from vedis import Vedis
import shelve
import config


# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id):
    with shelve.open(config.db_file) as db:
        if str(user_id) in db:
            return db[str(user_id)] 
        return config.Mystat_logins_steps.S_START.value  # значение по умолчанию - начало диалога


# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    with shelve.open(config.db_file) as db:
        try:
            db[str(user_id)] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False
        
        
# Записываем в базу данных новый месседж фром юзер айди , чтобы потом по нему отправлять сообщение

