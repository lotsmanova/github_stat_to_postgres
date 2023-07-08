import os
from dotenv import load_dotenv
from src.functions import get_repos_stats
from postgres_db import PostgresDB

load_dotenv()

# переменные окружения с параметрами для подключения к БД из файла .env
db_config = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB')
}

def main():
    # запрашиваем имя пользователя
    user_name = input('Введите имя пользователя на GitHub: ')

    # получаем статистику с ГХ
    data_github = get_repos_stats(user_name)

    # создаем экземпляр класса
    posgresdb = PostgresDB(**db_config)
    # добавляем данные с ГХ в БД
    posgresdb.add_data_to_table(data_github)
    # сохраняем данные в файл
    posgresdb.save_data_to_json()

    # вывод статистику в консоль
    res = posgresdb.get_data(5, 'name_repos')
    print(res)

if __name__ == '__main__':
    main()