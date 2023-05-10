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
    
   # получение продукта
    def get_product(self, id_product):
        text_SQL = f"""
            SELECT * FROM product
            WHERE id = '{id_product}'
        """
        return self.request_db(text_SQL)


    # получение списка всех маркеров
    def get_list_marker(self):
        text_SQL = f"""
            SELECT * FROM marker;
        """
        result = self.request_db(text_SQL)
        return result
    
    
    
    # получение маркеров с ошибкой
    def get_error_prod_marker(self, id_product):
        text_SQL = f"""
            SELECT * FROM marker
            WHERE id_product = '{id_product}' and status = 'error'
        """
        result = self.request_db(text_SQL)
        return result

    
    # получение маркеров для печати
    def get_wait_prod_marker(self, id_product):
        text_SQL = f"""
            SELECT * FROM marker
            WHERE id_product = '{id_product}' and status = 'wait' 
        """
        result = self.request_db(text_SQL)
        return result
    

    #изменение статуса
    def update_status_marker(self, id_marker, status):
        text_SQL = f"""
            UPDATE marker
            SET status = '{status}' 
            WHERE id = '{id_marker}'
        """
        result = self.request_db(text_SQL)
  

        
    # получение кол-ва маркеров для определенного продукта 
    def get_count_all_prod_marker(self):
        text_SQL = f"""
            SELECT id_product, COUNT(*) FROM marker
            GROUP BY id_product;
        """
        result = self.request_db(text_SQL)
        array={}
        if "Response" in result:
            for row in result["Response"]:
                array.update({f"{row[0]}":row[1]})
        return array
    

    # получение кол-ва ожидающих печати маркеров для определенного продукта 
    def get_count_wait_prod_marker(self):
        text_SQL = f"""
            SELECT id_product, COUNT(*) FROM marker
            WHERE status = 'wait'
            GROUP BY id_product;
        """
        result = self.request_db(text_SQL)
        array={}
        if "Response" in result:
            for row in result["Response"]:
                array.update({f"{row[0]}":row[1]})
        return array
    

    # получение списка всех продуктов и кол-ва маркеров
    def get_list_product(self):
        text_SQL = f"""
            SELECT * FROM product;
        """
        result = self.request_db(text_SQL)
        
        arr_count_all = self.get_count_all_prod_marker()
        arr_count_wait =  self.get_count_wait_prod_marker()
        print(arr_count_all)
        print(arr_count_wait)
        array = []
        if "Response" in result:
            for row in result["Response"]:
                if f"{row[0]}" in arr_count_all:
                    count_all = arr_count_all[f"{row[0]}"]
                else: count_all = 0
                if f"{row[0]}" in arr_count_wait:
                    count_wait = arr_count_wait[f"{row[0]}"]
                else: count_wait = 0
                array.append({"id": row[0], "name":  row[1],"gtin":  row[2],"count_all":  count_all, "count_wait": count_wait})
        return array
            
    


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

    
  

