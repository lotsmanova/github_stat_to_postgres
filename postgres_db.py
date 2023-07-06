import psycopg2
import json
from config import config


class PostgresDB:
    """Класс для взаимодействия с Postgres"""
    def __init__(self, database_name: str) -> None:
        """Инициализация экземпляра класса"""
        self.params = config()
        self.database_name = database_name


    def create_database(self):
        """Создание базы данных"""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        cur.close()
        conn.close()


    def create_table(self):
        """Метод создания таблицы"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE repos (
                        repos_id SERIAL PRIMARY KEY,
                        name_repos VARCHAR(100) NOT NULL,
                        url TEXT,
                        stars INT,
                        forks INT,
                        watchers INT
                    )
                """)
        conn.commit()
        conn.close()


    def add_data_to_table(self, data_github: list[dict]) -> None:
        """Метод добавления данных в таблицу"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            for data in data_github:
                cur.execute(
                    """
                    INSERT INTO repos (name_repos, url, stars, forks, watchers)
                    VALUES (%s, %s, %s, %s, %s)
                    
                    """,
                    (data['name'], data['url'], data['stars'], data['forks'], data['watchers'])
                )
        conn.commit()
        conn.close()


    def save_data_to_json(self):
        """Сохранение данных в json и получение данных из таблицы"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM repos")
            data = cur.fetchall()
        conn.close()



        with open('./data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)


    def get_data(self):
        """Получение данных из таблицы"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM repos")
            data = cur.fetchall()
        return data


