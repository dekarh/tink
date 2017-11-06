# -*- coding: utf-8 -*-
# Общая библиотека функций
# ver 1.07

import string
import re
from configparser import ConfigParser

def lenl(a):            # длинна белиберды переведнной в цифры или 0
    try:
        if a != None:
            a = str(a).strip()
            if  a != '':
                a = ''.join([char for char in a if char in string.digits])
                return len(a)
        return 0
    except TypeError:
        return 0

def l(a):               # белиберду в цифры или 0
    try:
        if a != None:
            a = str(a).strip()
            if  a != '':
                a = ''.join([char for char in a if char in string.digits])
                if len(a) > 0:
                    return int(a)
                else:
                    return 0
        return 0
    except TypeError:
        return 0

def s(a):                   # белиберду в строку
    try:
        if a != None:
            return str(a).strip().replace(u"\xa0", u" ")
        return ''
    except TypeError:
        return ''

def t(a):
    try:
        if a != None and str(type(a)) == "<class 'bool'>":
            return a
        return False
    except TypeError:
        return False

def s_minus(a):                   # белиберду в строку
    try:
        if a != None:
            if len(str(a).strip().replace(u"\xa0", u" ")) > 0:
                return str(a).strip().replace(u"\xa0", u" ")
            else:
                return '-'
    except TypeError:
        return '-'


def unique(lst):            # сделать список уникальным
    seen = set()
    j = 0
    while j < len(lst)-1:
        for i, x in enumerate(lst):
            j = i
            if x.lower() in seen:
                lst.pop(i)
                seen = set()
                break
            seen.add(x.lower())
    return

def filter_rus_sp(a):
    if not a:
        return ''
    else:
        b = re.sub(r'[^а-яА-ЯёЁ0-9\\\-\.\/\(\)\s]', '', a)
    return b.replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ')

def filter_rus_minus(a):
    if not a:
        return ''
    else:
        b = re.sub(r'[^а-яА-ЯёЁ0-9\-\s]', '', a)
    return b.replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ')

def get_path(full):
    if len(full.split('/')) > 1:
        return '/'.join(full.split('/')[:len(full.split('/')) - 1]) + '/'  # только путь без имени файла
    else:
        return ''

def get_filename(full):
    if len(full.split('/')) > 1:
        return full.split('/')[len(full.split('/'))-1]
    else:
        return full

def format_police_code(code):# форматирование любого числа в код подразделения 2 => '000-002'
    if lenl(code) < 7:
        return '{:=06d}'.format(l(code))[:3]+'-'+'{:=06d}'.format(l(code))[3:]
    else:
        return '111-111'

def format_phone(tel):
    tel = str(tel).strip()
    if tel == '' or tel == None:
        return None
    else:
        tel = ''.join([char for char in tel if char in string.digits])
        if len(tel) == 11:
            if tel[0] in ['8', '9']:
                return int('7' + tel[1:])
            elif tel[0] == '7':
                return int(tel)
            else:
                return None
        elif len(tel) == 10:
            return int('7' + tel)
        elif len(tel) == 6:
            return int('78512' + tel)
        else:
            return None

def read_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db
