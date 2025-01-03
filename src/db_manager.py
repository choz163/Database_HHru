import psycopg2
from psycopg2 import sql
from typing import List, Tuple, Optional, Dict, Any


class DBManager:
    def __init__(self, db_config: Dict[str, str]):
        """Инициализирует соединение с базой данных."""
        self.db_config = db_config
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def create_database(self, db_name: str) -> None:
        """
        Создает базу данных, если она не существует.

        Args:
            db_name (str): Имя базы данных для создания.
        """
        try:
            # Создаем временное соединение с PostgreSQL
            conn = psycopg2.connect(
                dbname="postgres",  # Подключаемся к стандартной базе данных
                user=self.db_config["user"],
                password=self.db_config["password"],
                host=self.db_config["host"],
                port=self.db_config["port"],
            )
            conn.autocommit = True  # Включаем автокоммит
            cursor = conn.cursor()

            # Проверяем, существует ли база данных
            cursor.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"), [db_name]
            )
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                )
                print(f"Database {db_name} created successfully.")
            else:
                print(f"Database {db_name} already exists.")

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error creating database: {e}")

    def create_tables(self) -> None:
        """Создает таблицы для компаний и вакансий в базе данных."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                hh_id BIGINT UNIQUE NOT NULL,
                name VARCHAR NOT NULL
            );
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                company_id INT REFERENCES companies(id),
                title VARCHAR NOT NULL,
                salary_min INT,
                salary_max INT,
                url VARCHAR NOT NULL
            );
        """
        )
        self.connection.commit()

    def insert_company(self, company: Dict[str, Any]) -> Optional[int]:
        """Вставляет информацию о компании в базу данных, избегая дубликатов."""
        try:
            self.cursor.execute(
                """
                INSERT INTO companies (hh_id, name) 
                VALUES (%s, %s) 
                ON CONFLICT (hh_id) DO NOTHING 
                RETURNING id;
            """,
                (company["id"], company["name"]),
            )

            result = self.cursor.fetchone()
            if result:
                return result[0]  # Возвращаем id вставленной компании
            else:
                # Если запись уже существует, можно вернуть None или id существующей записи
                print(f"Company with hh_id {company['id']} already exists.")
                return None
        except Exception as e:
            print(f"Error inserting company: {e}")
            return None

    def insert_vacancy(self, vacancy: Dict[str, Any], company_id: int) -> None:
        """Вставляет информацию о вакансии в базу данных."""
        self.cursor.execute(
            """
            INSERT INTO vacancies (company_id, title, salary_min, salary_max, url) VALUES (%s, %s, %s, %s, %s);
        """,
            (
                company_id,
                vacancy["name"],
                vacancy.get("salary", {}).get("from"),
                vacancy.get("salary", {}).get("to"),
                vacancy["alternate_url"],
            ),
        )
        self.connection.commit()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.cursor.execute(
            """
            SELECT c.name, COUNT(v.id) 
            FROM companies c LEFT JOIN vacancies v ON c.id = v.company_id 
            GROUP BY c.id;
        """
        )
        return self.cursor.fetchall()

    def get_all_vacancies(
        self,
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        self.cursor.execute(
            """
            SELECT c.name, v.title, v.salary_min, v.salary_max, v.url 
            FROM vacancies v JOIN companies c ON v.company_id = c.id;
        """
        )
        return self.cursor.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """Получает среднюю зарплату по вакансиям."""
        self.cursor.execute(
            """
            SELECT AVG(salary_min) FROM vacancies WHERE salary_min IS NOT NULL;
        """
        )
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[int, int, str]]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            """
            SELECT * FROM vacancies WHERE salary_min > %s;
        """,
            (avg_salary,),
        )
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[int, int, str]]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        self.cursor.execute(
            """
            SELECT * FROM vacancies WHERE title ILIKE %s;
        """,
            (f"%{keyword}%",),
        )
        return self.cursor.fetchall()

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        self.cursor.close()
        self.connection.close()
