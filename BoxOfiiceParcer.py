from bs4 import BeautifulSoup
from requests import get
from BoxOfficeParserInsideHrefs import get_budget
from BoxOfficeParserCheckingNumbers import Check
import json

dictionary_film = {}
box_office_mojo = 'https://www.boxofficemojo.com'

for page in range(1, 2):
    site_html = get(box_office_mojo + f"/alltime/world/?pagenum={page}&p=.htm").text
    soup = BeautifulSoup(site_html, 'html.parser')
    # print(type(soup.find_all('table')), '/n')
    # print(soup.find_all('table')[2].find_all('tr')[1].find_all('td')[1].get_text())
    # print(soup)
    infoTable = soup.find_all('table')[2]  # table with all movies

    for x in infoTable.find_all('tr'):
        try:
            film_id = int(x.find_all('td')[0].get_text())

            title = x.find_all('td')[1].get_text()
            studio = x.find_all('td')[2].get_text()

            worldwide = x.find_all('td')[3].get_text()
            worldwide = worldwide.replace(',', '')

            domestic = x.find_all('td')[4].get_text()
            domestic = domestic.replace(',', '')
            # if domestic box office is less than million
            if domestic[-1] == 'k':
                domestic = '$' + str(round(float(domestic[1:-1]) / 1000, 4))

            overseas = x.find_all('td')[6].get_text()
            overseas = overseas.replace(',', '')

            year = x.find_all('td')[8].get_text()
            # if year ends with not necessary symbol '^'
            if year[-1] == '^':
                year = year.replace('^', '')

            href_link = x.find_all('a')[0].get('href')
            budget = get_budget(href_link)

            worldwide, domestic, overseas, budget = Check(worldwide, domestic, overseas, budget)

            film_dict = {film_id: {'name': title, 'studio': studio, 'budget': float(budget),
                                   'worldwide': float(worldwide), 'domestic': float(domestic),
                                   'overseas': float(overseas), 'year': int(year)}}
            dictionary_film.update(film_dict)
            print(film_dict)

        except ValueError as e:
            # for first element
            continue

# for x in dictionary_film:
#     # TODO domestic /a, do something with this
#     try:
#         print(dictionary_film[x]['domestic'][1:])
#     except ValueError:
#         print('a')
print(dictionary_film)

with open('movies_list.txt', 'w') as json_file:
    json.dump(dictionary_film, json_file)
