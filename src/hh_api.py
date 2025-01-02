import requests
from typing import List, Dict, Any


class HHAPI:
    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_companies() -> List[Dict[str, Any]]:
        """Получает список всех компаний с сайта hh.ru."""
        response = requests.get(f"{HHAPI.BASE_URL}/employers")
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Error fetching companies: {response.status_code}")
            return []

    @staticmethod
    def get_vacancies(company_id: int) -> List[Dict[str, Any]]:
        """
        Получает список вакансий для заданного идентификатора компании."""
        response = requests.get(f"{HHAPI.BASE_URL}/vacancies?employer_id={company_id}")
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(
                f"Error fetching vacancies for company {company_id}: {response.status_code}"
            )
            return []
