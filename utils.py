import requests


def get_vacancies_hh(job_name, number_of_pages, par):
    url = 'https://api.hh.ru/vacancies'
    vacancies = list()
    for i in range(number_of_pages):
        par['page'] = i
        par['text'] = job_name
        try:
            response = requests.get(url, params=par)
            response.raise_for_status()
            vacancies.append(response.json())
        except requests.exceptions.HTTPError:
            return vacancies
    return vacancies


def predict_salary(salary_from, salary_to):
    if (salary_from is not None and salary_to is not None and
            salary_from != 0 and salary_to != 0):
        return ((int(salary_from) + int(salary_to))) / 2
    elif (salary_from is None or salary_from == 0) and (salary_to is not None
                                                        and salary_to != 0):
        return int(salary_to) * 0.8
    elif (salary_from is not None and salary_from != 0) and (salary_to is None or
                                                             salary_to != 0):
        return int(salary_from) * 1.2
    else:
        return


def predict_rub_salary_hh(vacancy):
    if vacancy["salary"] is None:
        return
    elif vacancy["salary"]["currency"] != 'RUR':
        return
    else:
        return predict_salary(vacancy["salary"]["from"], vacancy["salary"]["to"])


def predict_rub_salary_sj(vacancy):
    if vacancy["currency"] != 'rub' or vacancy["currency"] is None:
        return
    else:
        return predict_salary(vacancy['payment_from'], vacancy['payment_to'])


def transformation_for_table(statistic):
    for_table = [['Язык программирования', 'Вакансий найдено',
                   'Вакансий обработано', 'Средняя зарплата'], ]
    for language in statistic:
        language_solar = [language, statistic[language]['vacancies_found'],
                          statistic[language]['vacancies_processed'],
                          statistic[language]['average_salary']]
        for_table.append(language_solar)
    return for_table
