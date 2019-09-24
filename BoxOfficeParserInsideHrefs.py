from bs4 import BeautifulSoup
from requests import get

dictionary_film = {}
box_office_mojo = 'https://www.boxofficemojo.com'


def get_budget(href):
    site_html = get(box_office_mojo + href).text
    soup = BeautifulSoup(site_html, 'html.parser')
    # unique 611th problematic film
    try:
        budget_value = soup.find_all('table')[5].find_all('tr')[3].text.split()[-2]
    except IndexError:
        return None

    if budget_value[1:].isdigit():
        return budget_value
    else:
        return None


if __name__ == '__main__':
    print(123)
