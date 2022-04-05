from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json
base_url = 'https://www.hh.ru'
vacancy_name = input("Введите вакансию")
page = input("Введите страницу")
params = {'text': vacancy_name, 'page': page}
url = base_url + '/search/vacancy?search_field=name&search_field=company_name&search_field=description&clusters=true&ored_clusters=true&enable_snippets=true'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
response = requests.get(url, params=params, headers=headers)
dom = bs(response.text, 'html.parser')
vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
vacancies_list = []
for vacancy in vacancies:
    response = requests.get(url, params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancy_data = {}
    vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
    vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).getText()
    vacancy_salary = vacancy.find('span', {'class': 'bloko-header-section-3'})
    if not vacancy_salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        vacancy_salary = vacancy_salary.getText().split()
        if vacancy_salary[0] == 'до':
            salary_min = None
            salary_max_1 = str(vacancy_salary[1]) + str(vacancy_salary[2])
            salary_max = int(salary_max_1)
            salary_currency = vacancy_salary[-1]
        elif vacancy_salary[0] == 'от':
            salary_min_1 = str(vacancy_salary[1]) + str(vacancy_salary[2])
            salary_min = int(salary_min_1)
            salary_max = None
            salary_currency = vacancy_salary[-1]
        else:
            salary_min_1 = str(vacancy_salary[0]) + str(vacancy_salary[1])
            salary_min = int(salary_min_1)
            salary_max_1 = str(vacancy_salary[3]) + str(vacancy_salary[4])
            salary_max = int(salary_max_1)
            salary_currency = vacancy_salary[-1]

    vacancy_data['salary_min'] = salary_min
    vacancy_data['salary_max'] = salary_max
    vacancy_data['salary_currency'] = salary_currency
    vacancy_data['name'] = vacancy_name
    vacancy_data['link'] = vacancy_link
    vacancy_data['site'] = base_url
    vacancies_list.append(vacancy_data)
with open('vacancies_list.json', 'w') as outfile:
    json.dump(vacancies_list, outfile)
pprint(vacancies_list)