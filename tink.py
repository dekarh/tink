# -*- coding: utf-8 -*-
# Робот переносящий из Сатурна в Tinkoff


import sys, subprocess
import datetime
from mysql.connector import MySQLConnection, Error
from random import random

from lib import read_config, lenl, s_minus, s, l, filter_rus_sp, filter_rus_minus
from lib_scan import wj, p, chk
from tink_env import clicktity, inputtity, inputtity_first, selectity, select_selectity, gluk_w_point

import time

# DRIVER_PATH = 'drivers/chromedriver.exe'
#DRIVER_PATH = 'drivers/chromedriver'

change_errors = {
    'Выберите модель из списка' : 'Укажите марку и модель машины так, как они записаны в техпаспорте или ПТС',
    'Выберите марку из списка' : 'Укажите марку и модель машины так, как они записаны в техпаспорте или ПТС',
}
change2errors = {
    'Укажите регион' : 'Укажите адрес регистрации и проживания',
    'Укажите номер дома' : 'Укажите номер дома в адресе регистрации и проживания',
}
change3errors = {
    'Укажите регион' : 'Укажите рабочий адрес',
    'Укажите номер дома': 'Укажите номер дома в рабочем адресе',
}

not_errors = [
#    'Укажите серию и номер паспорта',
#    'Укажите название организации в которой работаете',
#    'Укажите Ваш персональный доход',
    ]


now = datetime.datetime.now()
if now.timetuple().tm_hour < 10 or now.timetuple().tm_hour > 21:
#    print(datetime.datetime.now().strftime("%H:%M:%S") + ' Не рабочее время. Работа скрипта окончена')
    sys.exit()

dbconfig = read_config(filename='tink.ini', section='mysql')

## Формируем SQL
main_sql = 'SELECT a.client_id '
main_sql += 'FROM clients AS a INNER JOIN contracts AS b ON a.client_id=b.client_id ' \
                'WHERE b.status_code=0 OR ' \
                '(b.status_code=1 AND b.transaction_date<DATE_SUB(NOW(),INTERVAL 10 MINUTE))'

conn = MySQLConnection(**dbconfig) # Открываем БД из конфиг-файла
cursor = conn.cursor()
cursor.execute(main_sql)
rows = cursor.fetchall()
conn.close()

# print(datetime.datetime.now().strftime("%H:%M:%S") +' Скрипт выгрузки. Начинаем \n')

if len(rows) < 1:
#    print(datetime.datetime.now().strftime("%H:%M:%S") + ' Нет новых договоров. Работа скрипта окончена')
    sys.exit()

# authorize(driver, **webconfig)  # Авторизация

error = ''
while len(rows) > 0:                    # Цикл по строкам таблицы (основной)
    conn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
    cursor = conn.cursor()
    sql = 'UPDATE contracts SET status_code=100, transaction_date=NOW(), error_message=NULL WHERE client_id=%s AND id>-1'
    cursor.execute(sql, (rows[0][0],))
    conn.commit()
    cursor = conn.cursor()
    cursor.execute(main_sql)
    rows = cursor.fetchall()
    conn.close()
    time.sleep(int(random() * 10))



