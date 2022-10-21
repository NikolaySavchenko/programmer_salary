from utils import get_vacancies_hh
from utils import predict_rub_salary_hh
from utils import predict_rub_salary_sj
from utils import transformation_for_table
from dotenv import load_dotenv
from terminaltables import AsciiTable
import requests
import os


def get_from_hh(languages):
    number_of_pages = 100
    par = {'area': '1', 'per_page': '50', 'period': '30'}
    average_salary = dict()
    for language in languages:
        average_salary[language] = dict()
        vacancies = get_vacancies_hh(language, number_of_pages, par)
        average_salary[language]['vacancies_found'] = vacancies[0]['found']
        vacancies_processed = 0
        sum_salary = 0
        for page in range(number_of_pages):
            try:
                for vacancy in vacancies[page]["items"]:
                    if predict_rub_salary_hh(vacancy):
                        vacancies_processed += 1
                        sum_salary += predict_rub_salary_hh(vacancy)
            except IndexError:
                break
        average_salary[language]['vacancies_processed'] = vacancies_processed
        average_salary[language]['average_salary'] = int(sum_salary / vacancies_processed)
    return average_salary


def get_from_superjob(languages):
    load_dotenv()
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': os.environ['SUPERJOB_TOKEN']}
    average_salary = dict()
    for language in languages:
        average_salary[language] = dict()
        vacancies = list()
        for page in range(5):
            payload = {'keyword': language, 'page': page, 'count': 100,
                       't': 4, 'catalogues': 'Разработка, программирование'}
            response = requests.get(url, params=payload, headers=headers)
            response.raise_for_status()
            vacancies.append(response.json())
        average_salary[language]['vacancies_found'] = vacancies[0]['total']
        vacancies_processed = 0
        sum_salary = 0
        for page in range(5):
            for vacancy in vacancies[page]['objects']:
                if predict_rub_salary_sj(vacancy):
                    vacancies_processed += 1
                    sum_salary += predict_rub_salary_sj(vacancy)
        average_salary[language]['vacancies_processed'] = vacancies_processed
        average_salary[language]['average_salary'] = int(sum_salary / vacancies_processed)
    return average_salary


def main():
    languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++',
                 'CSS', 'C#', 'Shell', 'Go']
    statistics_sj = transformation_for_table(get_from_superjob(languages))
    statistics_hh = transformation_for_table(get_from_hh(languages))
    table_sj = AsciiTable(statistics_sj, 'SuperJob, Moscow')
    table_hh = AsciiTable(statistics_hh, 'HeadHunter, Moscow')
    print(table_sj.table)
    print(table_hh.table)


if __name__ == '__main__':
    main()