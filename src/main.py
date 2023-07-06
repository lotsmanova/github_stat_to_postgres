from src.functions import get_repos_stats
from postgres_db import PostgresDB

def main():
    # запрашиваем имя пользователя
    user_name = input('Введите имя пользователя на GitHub: ')

    # получаем статистику с ГХ
    data_github = get_repos_stats(user_name)

    # создаем экземпляр класса
    posgresdb = PostgresDB('test_database')
    # создаем БД
    posgresdb.create_database()
    # создаем таблицу
    posgresdb.create_table()
    # добавляем данные с ГХ в БД
    posgresdb.add_data_to_table(data_github)
    # сохраняем данные в файл
    posgresdb.save_data_to_json()

    # вывод статистику в консоль
    res = posgresdb.get_data()
    print(res)

if __name__ == '__main__':
    main()