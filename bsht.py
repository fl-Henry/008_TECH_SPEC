import random
import requests

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from time import sleep


def random_dd_mm_yyy(start_date, end_date: tuple[int, int, int] = None):
    if end_date is None:
        end_date = datetime.today()
    else:
        if len(end_date) == 3:
            end_date = datetime(year=end_date[2], month=end_date[1], day=end_date[0])
        else:
            raise ValueError
    start_date = datetime(year=start_date[2], month=start_date[1], day=start_date[0])
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    dd = int(str(random_date.strftime("%d")))
    mm = int(str(random_date.strftime("%m")))
    yyyy = int(str(random_date.strftime("%Y")))
    return dd, mm, yyyy


def url_generator(dd, mm, yyyy, der):
    """

    :param dd: int              | day
    :param mm: int              | month
    :param yyyy: int            | year
    :param der: str             | str from list values_for_url[...]
    :return:
    """
    base_url = "http://tsjdgo.gob.mx/Recursos"
    if (dd <= 31) and (mm <= 12) and (yyyy >= 2017):
        if (mm <= 9) and (yyyy == 2017):
            if (mm == 9) and (dd > 26):
                url = f"{base_url}/images/flash/ListasAcuerdos/{dd}{mm}{yyyy}/{der}pdf"
            else:
                url = f"{base_url}/images/flash/ListasAcuerdos/{dd}{mm}{yyyy}/{der}swf"
        else:
            url = f"{base_url}/images/flash/ListasAcuerdos/{dd}{mm}{yyyy}/{der}pdf"
    else:
        url = f"{base_url}/images/flash/ListasAcuerdos/{dd}{mm}{yyyy}/{der}swf"
    return url

def main():

    urls = [
        "http://tsjdgo.gob.mx/Recursos/ListasDeAcuerdos.html#",
        "",
    ]
    url = "http://tsjdgo.gob.mx/Recursos/ListasDeAcuerdos.html#"
    css_selectors = {
        1: "#contenedor1",                   # button with text De la capital
        2: "#contenedor2",                   # button with text Gómez Palacio y Lerdo
        3: "#contenedor3",                   # button with text Juzgados foraneos
        4: "#panel-oculto",                  # block after clicking button with text De la capital
        5: "#panel-oculto2",                 # block after clicking button with text Gómez Palacio y Lerdo
        6: "#panel-oculto1",                 # block after clicking button with text Juzgados foraneos
        7: "input.der",                      # radio_buttons
        8: "#panel-oculto input.der",        # radio_buttons for De la capital
        9: "#panel-oculto2 input.der",       # radio_buttons for Gómez Palacio y Lerdo
        10: "#panel-oculto1 input.der",       # radio_buttons for Juzgados foraneos
    }
    response = requests.get(urls[0])
    soup = BeautifulSoup(response.text, "lxml")
    list_capital = soup.select(css_selectors[8])
    list_lerdo = soup.select(css_selectors[9])
    list_foraneos = soup.select(css_selectors[10])
    values_for_url = {
        "capital": [x['value'] for x in list_capital],
        "lerdo": [x['value'] for x in list_lerdo],
        "foraneos": [x['value'] for x in list_foraneos],
    }

    # tests url_generator
    print(f"\n======= TIMESTAMP UTC ======= {datetime.utcnow()} =======\n")
    counter = 0
    test_amount = 120
    for _ in range(test_amount):
        dd, mm, yyyy = random_dd_mm_yyy((1, 1, 2017))
        key_index = random.randint(0, 2)
        key = [*values_for_url.keys()][key_index]
        value_index = random.randint(0, len([*values_for_url.keys()][0]) - 1)
        value = values_for_url[key][value_index]
        print("day:", dd, ", mm: ", mm, ", yyyy: ", yyyy, ", key: ", key, ", value: ", value)
        url = url_generator(dd, mm, yyyy, value)
        print(url)
        response_ = requests.get(url)
        if response_.text == "Not Found [CFN #0005]":
            print(response_.text)
        else:
            print("File Exists")
            counter += 1
        sleep(0.2)
        print()
    print(f"Test completed: {counter}/{test_amount} files exist")

if __name__ == '__main__':
    main()

