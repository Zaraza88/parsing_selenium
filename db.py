import psycopg2

from config import HOST, USER, PASSWORD, BASE_NAME
from pars import main

class SaveDataInDB(object):

    def __init__(self, data, connection):
        self.data = data
        self.connection = connection

    def save(self):
        try:
            self.create_a_database()
            self.populate_the_database()   
        except Exception as ex:
            print(f'-[ERROR]-{ex}-[ERROR]-') 
        finally:
            if self.connection:
                self.connection.close()
                print('[INFO] Соединение закрыто')

    #создаем базу данных
    def create_a_database(self):
        self.connection.autocommit = True

        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE product(
                    id serial PRIMARY KEY,
                    name varchar(250),
                    price varchar(50),
                    link varchar(100));"""
            )

    #заполняем бд данными парсинга
    def populate_the_database(self):
        for d in self.data:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"""INSERT INTO product(name, price, link)
                    VALUES ('{d[1]}', '{d[0]}', '{d[2]}');"""
                )
        print('[INFO] Поля добавленны в базу данных')


if __name__ == '__main__':
    connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=BASE_NAME
    )
    data = main()
    savedata = SaveDataInDB(data, connection)
    savedata.save()
