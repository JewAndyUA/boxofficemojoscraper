from bs4 import BeautifulSoup
from requests import get
from BoxOfficeParserInsideHrefs import get_budget
import json

dictionary_film = {}
box_office_mojo = 'https://www.boxofficemojo.com'

for page in range(1, 9):
    site_html = get(box_office_mojo + f"/alltime/world/?pagenum={page}&p=.htm").text
    soup = BeautifulSoup(site_html, 'html.parser')
    infoTable = soup.find_all('table')[2]  # table with all movies

    for x in infoTable.find_all('tr'):
        try:
            film_id = int(x.find_all('td')[0].text.strip())

            title = x.find_all('td')[1].text.strip()
            studio = x.find_all('td')[2].text.strip()

            worldwide = x.find_all('td')[3].text.strip()
            worldwide = worldwide.replace(',', '')

            domestic = x.find_all('td')[4].text.strip()
            domestic = domestic.replace(',', '')
            # if domestic box office is less than million
            if domestic[-1] == 'k':
                domestic = '$' + str(round(float(domestic[1:-1])/1000, 4))

            overseas = x.find_all('td')[6].text.strip()
            overseas = overseas.replace(',', '')

            year = x.find_all('td')[8].text.strip()
            # if year ends with not necessary symbol '^'
            if year[-1] == '^':
                year = year.replace('^', '')

            href_link = x.find_all('a')[0].get('href')
            budget = get_budget(href_link)

            film_dict = {film_id: {'name': title, 'studio': studio, 'budget': budget,
                                   'worldwide': worldwide, 'domestic': domestic, 'overseas': overseas, 'year': year}}
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
