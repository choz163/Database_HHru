# HH.ru Job Scraper

Этот проект представляет собой приложение для извлечения данных о компаниях и их вакансиях с сайта hh.ru с использованием публичного API. Данные сохраняются в базе данных PostgreSQL, и предоставляется интерфейс для работы с этими данными.

## Описание

Проект включает в себя следующие основные функции:
- Получение данных о работодателях и их вакансиях с сайта hh.ru.
- Сохранение полученных данных в базе данных PostgreSQL.
- Предоставление методов для извлечения информации о компаниях и вакансиях.


### Требования

- Python = "3.12" или выше
- PostgreSQL
- Установленные библиотеки:
  - requests
  - psycopg2
  - (дополнительно) poetry для управления зависимостями

### Установка зависимостей

1. Клонируйте репозиторий:

   ```bash
   https://github.com/choz163/Database_HHru.git
   
Копировать

Если вы используете poetry:


poetry install
Копировать

Либо используйте pip:

pip install requests psycopg2
Копировать



### Настройка базы данных

Создайте базу данных в PostgreSQL:


CREATE DATABASE CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    hh_id BIGINT UNIQUE NOT NULL,
    name VARCHAR NOT NULL
);

CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id),
    title VARCHAR NOT NULL,
    salary_min INT,
    salary_max INT,
    url VARCHAR NOT NULL
);;
Копировать



Обновите параметры подключения в main.py:


db_config = {
    'dbname': 'postgres',
    'user': 'postgresr',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}
Копировать



Использование

Запустите скрипт main.py для извлечения данных и их сохранения в базе данных:

python main.py
Копировать

После завершения выполнения скрипта вы можете использовать методы класса DBManager для извлечения информации о компаниях и вакансиях.

Методы

DBManager


get_companies_and_vacancies_count(): Получает список всех компаний и количество вакансий у каждой компании.

get_all_vacancies(): Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.

get_avg_salary(): Получает среднюю зарплату по вакансиям.

get_vacancies_with_higher_salary(): Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

get_vacancies_with_keyword(keyword): Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
