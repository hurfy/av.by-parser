from asyncio  import create_task, gather
from aiohttp  import ClientSession
from requests import get
from math     import ceil
from bs4      import BeautifulSoup
from re       import sub


class Car:
    def __init__(self, model: str, url: str, price: list, parameters: str) -> None:
        """
        Initial method
        :param model:      str: Auto model
        :param url:        str: Auto url
        :param price:     list: Auto price [BYN, USD]
        :param parameters: str: Auto parameters "Engine type, Engine displacement, Mileage, Year of manufacture"
        """
        self._model = model
        self._url   = url
        self._price = price
        self._parameters = parameters

    def get_info(self) -> dict:
        """
        The method returns information about auto in the form of a dictionary
        :return: dict: About auto
        """
        return {'model' : self._model,
                'price' : self._price,
                'params': self._parameters,
                'url'   : self._url}

    def __str__(self) -> str:
        """
        String method
        :return: str: About auto
        """
        return f'Model:      {self._model}\n' \
               f'Price:      {self._price[0]} BYN / {self._price[1]} USD\n' \
               f'Parameters: {self._parameters}\n' \
               f'URL:        {self._url}'

    def __lt__(self, other) -> bool:
        """
        Operator '<'
        :param other: object: Other Car object
        :return:        bool: True / False
        """
        return self._price[1] < other

    def __gt__(self, other) -> bool:
        """
        Operator '>'
        :param other: object: Other Car object
        :return:        bool: True / False
        """
        return self._price[1] > other


# Remove HTML chars
def rhc(text: str) -> str:
    """
    The function removes garbage characters, and replaces special HTML characters with normal characters
    :param text: str: The text in which the replacement will take place
    :return:     str: The text in which the substitution took place
    """
    return text.replace(' ·', '').replace('\xa0', ' ').replace('\u2009', ' ')


async def cars_count(brand: int, model: int) -> int:
    """
    This async function parse the page with the selected car, finding the number of ads
    :param brand: int: Auto brand ID
    :param model: int: Auto model ID
    :return:      int: Pages count
    """
    async with ClientSession() as session:
        url    = fr'https://cars.av.by/filter'
        params = {'brands[0][brand]': brand, 'brands[0][model]': model}

        async with session.get(url, params=params) as response:
            soup  = BeautifulSoup(await response.text(), 'html.parser')
            count = soup.find('h3', class_='listing__title')

    # There are 25 ads on each page
    return 0 if count is None else ceil(int(sub(r'\D', '', count.text)) / 25)


async def fetch_cars(session: object, url: str, params: dict) -> list:
    """
    The function sends an async request and collects all the information about the machines on the page
    :param session: object: Async session
    :param url:        str: Page URLD
    :param params:    dict: Response parameters
    :return:          list: The list of cars from the page
    """
    async with session.get(url, params=params) as response:
        soup       = BeautifulSoup(await response.text(), 'html.parser')
        result     = []
        car_blocks = soup.find_all(class_='listing-item')

        for car in car_blocks:
            link      = fr'https://cars.av.by{car.find(class_="listing-item__link").get("href")}'
            name      = rhc(car.find('span', class_='link-text').text)
            price_byn = int(rhc(sub(r'[^0-9]', '', car.find(class_='listing-item__price').text)))
            price_usd = int(rhc(sub(r'[^0-9]', '', car.find(class_='listing-item__priceusd').text)))
            params    = ', '.join([rhc(div.text.strip()) for div in
                                   car.find(class_='listing-item__params').find_all('div')])

            result.append(Car(name, link, [price_byn, price_usd], params))

    return result


async def gather_cars_data(brand: int, model: int, count: int) -> list:
    """
    The function creates n-tasks for async collection of auto information
    :param brand: int: Auto brand ID
    :param model: int: Auto model ID
    :param count: int: Pages count
    :return:     list: Car list
    """
    async with ClientSession() as session:
        url   = fr'https://cars.av.by/filter'
        tasks = []

        for page in range(1, count + 1):
            params = {'brands[0][brand]': brand, 'brands[0][model]': model, 'page': page}
            tasks.append(create_task(fetch_cars(session, url, params)))

        return sorted(cars for car_list in await gather(*tasks) for cars in car_list)
