import configparser
from src.db_manager import DBManager
from src.hh_api import HHAPI


def main():
    # Загрузка конфигурации из файла
    config = configparser.ConfigParser()
    config.read("database.ini")

    try:
        # Проверяем, что секция 'database' существует
        if not config.has_section("database"):
            raise ValueError("Раздел [database] в файле конфигурации.")

        db_config = {
            "dbname": config["database"]["dbname"],
            "user": config["database"]["user"],
            "password": config["database"]["password"],
            "host": config["database"]["host"],
            "port": config["database"]["port"],
        }
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return

    db_manager = DBManager(db_config)

    # Создание базы данных, если она не существует
    db_manager.create_database(db_config["dbname"])

    # Создание таблиц
    db_manager.create_tables()

    # Получение данных о компаниях и вакансиях
    companies = HHAPI.get_companies()
    for company in companies:
        company_id = db_manager.insert_company(company)
        vacancies = HHAPI.get_vacancies(company["id"])
        for vacancy in vacancies:
            db_manager.insert_vacancy(vacancy, company_id)

    # Примеры использования методов
    print(db_manager.get_companies_and_vacancies_count())
    print(db_manager.get_all_vacancies())
    print(db_manager.get_avg_salary())
    print(db_manager.get_vacancies_with_higher_salary())
    print(db_manager.get_vacancies_with_keyword("python"))

    db_manager.close()


if __name__ == "__main__":
    main()
