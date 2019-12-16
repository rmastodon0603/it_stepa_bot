# -*- coding: utf-8 -*-

from enum import Enum

db_file = "database.db"


class Mystat_logins_steps(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_LOGIN_MYSTAT = "1"
    S_ENTER_PASS_MYSTAT = "2"
    S_ENTER_SYSTEM_MYSTAT = "3"