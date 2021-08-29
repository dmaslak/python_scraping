import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import re


# Скрапер для headhunter

# Создаём необходимые переменные
my_headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0'}
hh_url = 'https://chelyabinsk.hh.ru/search/vacancy ? clusters=true & enable_snippets=true & salary= & st=searchVacancy & text=data+analyst'
hh_main_url = 'https://chelyabinsk.hh.ru'

# Создаём базу, куда будем записывать результат
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
hh_vacancies = db.hh_vacancies


# Сам цикл. Параметры запроса включены в него, так как мы передаём номер страницы
for i in range(40):
    hh_params = {'clusters' : 'true',         
             'enable_snippets' : 'true', 
             'salary' : '', 
             'st' : 'searchVacancy', 
             'text' : 'data analyst', 
             'page' : i 
            }
    
    response = requests.get(hh_main_url + '/search/vacancy', params = hh_params, headers = my_headers)
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.find_all('div', {'class' : 'vacancy-serp-item'})

    def get_salary_numbers(salary_string):
        min_salary = None
        max_salary = None
        salary_list = salary_string.replace('\u202f', '').split()
        clean_lst = [int(item) for item in salary_list if item.isnumeric()]

        if '–' in salary_list:
            min_salary = clean_lst[0]
            max_salary = clean_lst[1]
        elif 'от' in salary_list:
            min_salary = clean_lst[0]
            max_salary = None
        elif 'до' in salary_list:
            min_salary = None
            max_salary = clean_lst[0]
        
        result_list = [min_salary, max_salary]            
        return result_list

    for vacancy in vacancy_list:
        
        link = vacancy.find('a')
        vacancy_href = link.get('href')
        vacancy_id = int(re.search('([0-9]{5,})', vacancy_href).group())
        vacancy_name = link.getText()
        salary_data = vacancy.find('span', {'data-qa' : 'vacancy-serp__vacancy-compensation'})
        
        if salary_data is not None:
            vacancy_salary = salary_data.getText()
            min_max_list = get_salary_numbers(vacancy_salary)
            salary_min = min_max_list[0]
            salary_max = min_max_list[1]
        else:
            vacancy_salary = None
            salary_min = None
            salary_max = None
            
        # Наполняем нашу базу
        new_vacancy = {'_id': vacancy_id, 
                        'name': vacancy_name,
                        'link': vacancy_href,
                        'salary_string': vacancy_salary,
                        'min_salary': salary_min,
                        'max_salary': salary_max
                        }
        # Проверка, которая добавляет только новые документы
        if hh_vacancies.count_documents({'_id': vacancy_id}):
            continue
        else:
            hh_vacancies.insert_one(new_vacancy)

# Функция, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
def get_vacancies_with_salary(min, max):
    for item in hh_vacancies.find({'$and': [{'max_salary': {'$gt': min}}, {'min_salary': {'$gt': max}}]}):
        print(item)
