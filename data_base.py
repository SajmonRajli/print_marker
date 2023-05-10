# -*- coding: utf-8 -*-
import configparser
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")
# config database
user=config['database']['user']
password=config['database']['password']
host=config['database']['host']
port=config['database']['port']

class Database:
    def __init__(self, database):
        self.connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
									database=database)
        # Курсор для выполнения операций с базой данных
        self.cursor = self.connection.cursor()
        print(f'Connected to the database {database}')

    # отправка запроса
    def request_db(self, text_SQL):
        try:
            self.cursor.execute(text_SQL)
            self.connection.commit()
            return {"Response": self.cursor.fetchall()}
        except Exception as e:
            return {"Exception": e}
		
   # добавление продукта
    def add_product(self, id, name, gtin):
        text_SQL = f"""
        INSERT INTO product (id, name, gtin) VALUES
        ({id}, '{name}', '{gtin}')
        """
        print(text_SQL)
        return self.request_db(text_SQL)



# создает базу и две таблицы (Нужно запустить один раз!!!!)
if __name__ == '__main__':
    name_db = 'tcpbd'
    connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # запрос на создание базы данных
    sql_create_database = f'Create database {name_db}'
    cursor.execute(sql_create_database)
    print(f'Successfully created db "{name_db}')
    cursor.close()
    connection.close()

    

    DB = Database(name_db)


    text_sql = """
        CREATE TABLE product
        (
            id int PRIMARY KEY NOT NULL,
            name text NOT NULL,
            gtin CHAR(14) NOT NULL, 
            CONSTRAINT products UNIQUE (gtin) 
        ); 
    """   
    print(DB.request_db(text_sql))
    text_sql = """
        CREATE TYPE mood AS ENUM ('wait','print','error','done');
        CREATE TABLE marker
        (
            id int PRIMARY KEY NOT NULL,
            serial CHAR(6) NOT NULL,  
            id_product int REFERENCES product (id),
            status mood,
            CONSTRAINT markers UNIQUE (serial)
        ); 
    """
    print(DB.request_db(text_sql))



