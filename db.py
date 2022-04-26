import psycopg2

from config import HOST, USER, PASSWORD, BASE_NAME
from pars import parse

def save_data_in_db():
    """Сохраняем данные в бд"""

    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=BASE_NAME
        )

        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE product(
                    id serial PRIMARY KEY,
                    name varchar(250),
                    price varchar(50),
                    link varchar(100));"""
            )

        data = parse()
        for d in data:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""INSERT INTO product(name, price, link)
                    VALUES ('{d[1]}', '{d[0]}', '{d[2]}');"""
                )
        print('[INFO] Поля добавленны в базу данных')

    except Exception as ex:
        print(f'[ERROR] - {ex}')

    finally:
        if connection:
            connection.close()
            print('[INFO] Соединение закрыто')


if __name__ == '__main__':
    save_data_in_db()
