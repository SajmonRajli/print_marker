# -*- coding: utf-8 -*-
import configparser
from data_base import Database
from random import randint
# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")
# config database
user=config['database']['user']
password=config['database']['password']
host=config['database']['host']
port=config['database']['port']




# заполняем базу тестовыми значениями
if __name__ == '__main__':
    name_db = 'tcpbd'
    DB = Database(name_db)

    id_marker = 0
    for id_prod in [0,1]:
        print(DB.add_product(id_prod, f'prod{id_prod}', f'1234567890000{id_prod}'))
        text_SQL ='INSERT INTO marker (id, serial, id_product, status) VALUES\n'
        for i in range(0,randint(5,9)):
            id_marker +=1
            text_SQL = text_SQL + f"({id_marker},  'qwer{id_prod}{i}', '{id_prod}', 'wait'),\n"
        text_SQL = text_SQL[:-2]+';'

        print(DB.request_db(text_SQL))

    print(DB.request_db("SELECT * FROM product;"))
    print(DB.request_db("SELECT * FROM marker;"))
