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
    if salary_from and salary_to:
        return ((int(salary_from) + int(salary_to))) / 2
    elif not salary_from and salary_to:
        return int(salary_to) * 0.8
    elif salary_from and not salary_to:
        return int(salary_from) * 1.2
    else:
        return


def predict_rub_salary_hh(vacancy):
    if not vacancy["salary"]:
        return
    elif vacancy["salary"]["currency"] != 'RUR':
        return
    else:
        return predict_salary(vacancy["salary"]["from"],
                              vacancy["salary"]["to"])


def predict_rub_salary_sj(vacancy):
    if vacancy["currency"] != 'rub' or not vacancy["currency"]:
        return
    else:
        return predict_salary(vacancy['payment_from'],
                              vacancy['payment_to'])


def transformation_for_table(statistic):
    for_table = [['Язык программирования', 'Вакансий найдено',
                  'Вакансий обработано', 'Средняя зарплата'], ]
    for language in statistic:
        language_solar = [language, statistic[language]['vacancies_found'],
                          statistic[language]['vacancies_processed'],
                          statistic[language]['average_salary']]
        for_table.append(language_solar)
    return for_table
