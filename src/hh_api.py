import requests


class HHAPI:
    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_companies():
        response = requests.get(f"{HHAPI.BASE_URL}/employers")
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            print(f"Error fetching companies: {response.status_code}")
            return []

    @staticmethod
    def get_vacancies(company_id):
        response = requests.get(f"{HHAPI.BASE_URL}/vacancies?employer_id={company_id}")
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(
                f"Error fetching vacancies for company {company_id}: {response.status_code}"
            )
            return []

