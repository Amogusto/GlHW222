import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = 'https://kazan.hh.ru/search/vacancy?text=&area=88'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.4.837 Yowser/2.5 Safari/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

vacancys = soup.find_all('div', {'class': 'vacancy-serp-item__layout'})

vacancys_list = []
for vacancy in vacancys:
    vacancy_info = {}
    print()
    info = vacancy.find('a', {'class': 'serp-item__title'})
    name = info.text
    link = info.get('href')
    salary = vacancy.find('span', {'class': 'bloko-header-section-2'})
    try:
        salary = salary.text.split()


        if salary[0] == 'до':
            s_min = None
            s_max = int(salary[1] + salary[2])
            currency = salary[3]
        elif salary[0] == 'от':
            s_min = int(salary[1] + salary[2])
            s_max = None
            currency = salary[3]
        else:
            s_min = int(salary[0] + salary[1])
            s_max = int(salary[3] + salary[4])
            currency = salary[5]
    except:
        vacancy_info['name'] = name
        vacancy_info['link'] = link
        vacancy_info['source'] = 'hh.ru'
        vacancy_info['max_salary'] = None
        vacancy_info['min_salary'] = None
        vacancy_info['currency'] = None
    #s_min = salary[0]
    #s_min = int(s_min)
    #s_max = salary[3]
    #s_max = int(s_max)
    #currency = salary[5]

    vacancy_info['name'] = name
    vacancy_info['link'] = link
    vacancy_info['source'] = 'hh.ru'
    vacancy_info['max_salary'] = s_max
    vacancy_info['min_salary'] = s_min
    vacancy_info['currency'] = currency
    vacancys_list.append(vacancy_info)
pprint(vacancys_list)
