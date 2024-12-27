from src.hh_api import HHAPI
from src.db_manager import DBManager


def main():
    db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
    }

    db_manager = DBManager(db_config)

    # Создание таблиц
    db_manager.create_tables()

    # Получение данных о компаниях
    companies = HHAPI.get_companies()
    for company in companies:
        print(f"Retrieved company: {company}")  # Логирование
        company_id = db_manager.insert_company(company)
        vacancies = HHAPI.get_vacancies(company['id'])
        for vacancy in vacancies:
            print(f"Retrieved vacancy: {vacancy}")  # Логирование
            db_manager.insert_vacancy(vacancy, company_id)

    # Примеры использования методов
    print(db_manager.get_companies_and_vacancies_count())
    print(db_manager.get_all_vacancies())
    print(db_manager.get_avg_salary())
    print(db_manager.get_vacancies_with_higher_salary())
    print(db_manager.get_vacancies_with_keyword('python'))

    db_manager.close()

if __name__ == "__main__":
    main()