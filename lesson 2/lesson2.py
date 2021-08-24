import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

# Скрапер для headhunter

# Создаём необходимые переменные
my_headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0'}
hh_url = 'https://chelyabinsk.hh.ru/search/vacancy ? clusters=true & enable_snippets=true & salary= & st=searchVacancy & text=data+analyst'
hh_main_url = 'https://chelyabinsk.hh.ru'

# Создаём датафрем, куда будем записывать результат
hh_df = pd.DataFrame(columns = ['hh_id', 'name', 'link', 'salary'])

# Создаём переменные для цикла
df_row = 0

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

    for vacancy in vacancy_list:
        
        link = vacancy.find('a')
        vacancy_href = link.get('href')
        vacancy_name = link.getText()
        salary_data = vacancy.find('span', {'data-qa' : 'vacancy-serp__vacancy-compensation'})
        
        if salary_data is not None:
            vacancy_salary = salary_data.getText()
        else:
            vacancy_salary = np.NaN
            
        # Наполняем наш датафрейм, строчка за строчкой 
        hh_df.loc[df_row, 'name'] = vacancy_name
        hh_df.loc[df_row, 'link'] = vacancy_href
        hh_df.loc[df_row, 'salary'] = vacancy_salary
        
        df_row += 1
    # После прохождения по одной странице заполняем первую колонку фрейма уникальным id, взятым из ссылки
    # при помощи регулярного выражения    
    hh_df['hh_id'] = hh_df['link'].str.extract('([0-9]{5,})')

# Скрапер для superjob

# Создаём необходимые переменные
my_headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0'}
sj_url = 'https://www.superjob.ru/vakansii/analitik.html ? noGeo=1 & page=1'
sj_main_url = 'https://www.superjob.ru'


# Создаём датафрем, куда будем записывать результат
sj_df = pd.DataFrame(columns = ['sj_id', 'name', 'link', 'salary'])

# Создаём переменные для цикла
df_row = 0

# Сам цикл. Параметры запроса включены в него, так как мы передаём номер страницы
for i in range(12):
    sj_params = {'noGeo' : '1', 
                 'page' : i 
                }
    
    response = requests.get(sj_main_url + '/vakansii/analitik.html', params = sj_params, headers = my_headers)
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.find_all('div', {'class' : 'f-test-vacancy-item'})

    for vacancy in vacancy_list:
        
        link = vacancy.find('a')
        vacancy_href = link.get('href')
        vacancy_name = link.getText()
        salary_data = vacancy.find('span', {'class' : 'f-test-text-company-item-salary'})
        
        if salary_data is not None:
            vacancy_salary = salary_data.getText()
        else:
            vacancy_salary = np.NaN
            
        # Наполняем наш датафрейм, строчка за строчкой 
        sj_df.loc[df_row, 'name'] = vacancy_name
        sj_df.loc[df_row, 'link'] = sj_main_url + vacancy_href
        sj_df.loc[df_row, 'salary'] = vacancy_salary
        
        df_row += 1
    # После прохождения по одной странице заполняем первую колонку фрейма уникальным id, взятым из ссылки
    # при помощи регулярного выражения    
    sj_df['sj_id'] = sj_df['link'].str.extract('([0-9]{5,})')

hh_df.to_csv('hh_df.csv')
sj_df.to_csv('sj_df.csv')
