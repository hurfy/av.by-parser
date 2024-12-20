from operator       import attrgetter
from asyncio        import create_task, gather, Task
from aiohttp        import ClientSession
from inspect        import Traceback
from math           import ceil
from bs4            import BeautifulSoup
from re             import sub

from parser.helpers import remove_html_chars as rhc
from parser.schemas import Car, CarPrice
from controllers    import Config


class CarParser:
    headers: dict[str, str] = {
    "Content-Type": "application/text",
    "User-Agent"  : "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, jak Gecko) "
                    "Chrome/77.0.3865.90 Safari/537.36"
    }

    def __init__(self, config: Config) -> None:
        """__init__ ..."""
        self.config: Config = config


    async def __aenter__(self) -> "CarParser":
        """__enter__ ..."""
        self.session: ClientSession = ClientSession(
            headers=self.headers,
        )

        return self

    async def __aexit__(self, exc_type: BaseException, exc_val: BaseException, exc_tb: Traceback) -> None:
        """__exit__ ..."""
        if exc_type is not None:
            print(f"An exception occurred: {exc_val}")

        await self.session.close()

    async def _get_pages_count(self) -> int:
        """Fetching and calculating the number of pages. Number of ads/per page"""
        params: dict[str, int] = {
            "brands[0][brand]": self.config.brand.id,
            "brands[0][model]": self.config.model.id
        }

        # Get the total number of ads
        async with self.session.get(url=r"https://cars.av.by/filter", params=params) as response:
            soup    = BeautifulSoup(await response.text(), "html.parser")
            counter = soup.find("h3", class_="listing__title")

        # Number of pages per calculation: 25 ads per page
        if counter is not None:
            return ceil(int(sub(r'\D', '', counter.text)) / 25)

        return 0

    async def _parse_on_page(self, page: int) -> list[Car]:
        """Fetching and parsing ads on each page"""
        result: list[Car]      = []
        params: dict[str, int] = {
            "brands[0][brand]": self.config.brand.id,
            "brands[0][model]": self.config.model.id,
            "page"            : page
        }

        # Get raw HTML
        async with self.session.get(url=r"https://cars.av.by/filter", params=params) as response:
            soup      = BeautifulSoup(await response.text(), "html.parser")
            car_items = soup.find_all(class_="listing-item")

            # For each car in car list block
            for car in car_items:
                car_price = CarPrice(
                    usd=int(rhc(sub(r'[^0-9]', '', car.find(class_='listing-item__price').text))),
                    byn=int(rhc(sub(r'[^0-9]', '', car.find(class_='listing-item__priceusd').text))),
                )

                # Appending Car object
                result.append(
                    Car(
                        model=rhc(car.find('span', class_='link-text').text),
                        params=", ".join(
                            [
                                # ...
                                rhc(div.text.strip()) for div
                                in car.find(class_="listing-item__params").find_all("div")
                            ]
                        ),
                        url=r"https://cars.av.by{}".format(car.find(class_='listing-item__link').get('href')),
                        price=car_price,
                    )
                )

            return result

    async def parse(self) -> list[Car]:
        """'Main' method for starting public processing and parsing"""
        tasks: list[Task] = []

        # Creating a task for each page
        for page in range(await self._get_pages_count()):
            tasks.append(
                create_task(self._parse_on_page(page + 1))
            )

        # Tasks execution
        result: list[Car] = [
            cars for car_list in await gather(*tasks) for cars in car_list
        ]

        return sorted(result, key=attrgetter("price.usd"))
