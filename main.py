from utils import get_vacancies_hh
from utils import predict_rub_salary_hh
from utils import predict_rub_salary_sj
from utils import convert_for_table
from dotenv import load_dotenv
from terminaltables import AsciiTable
import requests
import os


def get_salary_hh(languages):
    number_of_pages = 100
    vacancy_in_page = 50
    days = 30
    moscow_area = 1
    params = {'area': moscow_area, 'per_page': vacancy_in_page, 'period': days}
    average_salary = dict()
    for language in languages:
        average_salary[language] = dict()
        vacancies = get_vacancies_hh(language, number_of_pages, params)
        average_salary[language]['vacancies_found'] = vacancies[0]['found']
        vacancies_processed = 0
        sum_salary = 0
        for page in range(number_of_pages):
            try:
                for vacancy in vacancies[page]["items"]:
                    middle_salary = predict_rub_salary_hh(vacancy)
                    if middle_salary:
                        vacancies_processed += 1
                        sum_salary += middle_salary
            except IndexError:
                break
        average_salary[language]['vacancies_processed'] = vacancies_processed
        if vacancies_processed:
            average_salary[language]['average_salary'] = int(sum_salary /
                                                             vacancies_processed)
        else:
            average_salary[language]['average_salary'] = 0
    return average_salary


def get_salary_sj(languages, headers):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    average_salary = dict()
    moscow_id = 4
    max_page = 5
    vacancy_in_page = 100
    for language in languages:
        average_salary[language] = dict()
        vacancies = list()
        vacancies_processed = 0
        sum_salary = 0
        for page in range(max_page):
            payload = {'keyword': language, 'page': page, 'count': vacancy_in_page,
                       't': moscow_id, 'catalogues': 'Разработка, программирование'}
            response = requests.get(url, params=payload, headers=headers)
            response.raise_for_status()
            page_vacancies = response.json()
            vacancies.append(page_vacancies)
            for vacancie in page_vacancies['objects']:
                middle_salary = predict_rub_salary_sj(vacancie)
                if middle_salary:
                    vacancies_processed += 1
                    sum_salary += middle_salary
        average_salary[language]['vacancies_found'] = vacancies[0]['total']
        average_salary[language]['vacancies_processed'] = vacancies_processed
        if vacancies_processed:
            average_salary[language]['average_salary'] = int(sum_salary /
                                                             vacancies_processed)
        else:
            average_salary[language]['average_salary'] = 0
    return average_salary


def main():
    load_dotenv()
    headers_sj = {'X-Api-App-Id': os.environ['SUPERJOB_TOKEN']}
    languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++',
                 'CSS', 'C#', 'Shell', 'Go']
    statistics_sj = convert_for_table(get_salary_sj(languages, headers_sj))
    statistics_hh = convert_for_table(get_salary_hh(languages))
    table_sj = AsciiTable(statistics_sj, 'SuperJob, Moscow')
    table_hh = AsciiTable(statistics_hh, 'HeadHunter, Moscow')
    print(table_sj.table)
    print(table_hh.table)


if __name__ == '__main__':
    main()
