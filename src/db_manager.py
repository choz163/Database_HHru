import psycopg2


class DBManager:
    def __init__(self, db_config):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def create_tables(self):
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

    def insert_company(self, company):
        try:
            self.cursor.execute("""
                INSERT INTO companies (hh_id, name) VALUES (%s, %s) RETURNING id;
            """, (company['id'], company['name']))
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Error inserting company: {e}")
            return None

    def insert_vacancy(self, vacancy, company_id):
        try:
            self.cursor.execute("""
                INSERT INTO vacancies (company_id, title, salary_min, salary_max, url) VALUES (%s, %s, %s, %s, %s);
            """, (
            company_id, vacancy['name'], vacancy.get('salary', {}).get('from'), vacancy.get('salary', {}).get('to'),
            vacancy['alternate_url']))
            self.connection.commit()
        except Exception as e:
            print(f"Error inserting vacancy: {e}")

    def get_companies_and_vacancies_count(self):
        self.cursor.execute(
            """
            SELECT c.name, COUNT(v.id) FROM companies c LEFT JOIN vacancies v ON c.id = v.company_id 
            GROUP BY c.id;
        """
        )
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute(
            """
            SELECT c.name, v.title, v.salary_min, v.salary_max, v.url 
            FROM vacancies v JOIN companies c ON v.company_id = c.id;
        """
        )
        return self.cursor.fetchall()

    def get_avg_salary(self):
        self.cursor.execute(
            """
            SELECT AVG(salary_min) FROM vacancies WHERE salary_min IS NOT NULL;
        """
        )
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            """
            SELECT * FROM vacancies WHERE salary_min > %s;
        """,
            (avg_salary,),
        )
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute(
            """
            SELECT * FROM vacancies WHERE title ILIKE %s;
        """,
            (f"%{keyword}%",),
        )
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()

