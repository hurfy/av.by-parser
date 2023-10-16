# AV.BY ASYNC PARSER
This is an async parser that searches for auto information on a website [av.by](https://cars.av.by).

*The [API](https://api.av.by/_doc) was used to compile the list of cars.

## Feature:
- Choosing a car brand
- Selecting a car model
- Displaying search results
- Saving information to .json and .csv file

## Quickstart:
Clone the repository:
```cmd
  git clone git@github.com:hurfy/av.by-parser.git
```
Install requirements:
```cmd
  pip install -r requirements.txt
```
Done, now just run the main.py file.

## Libraries:
- [PyInquirer](https://github.com/CITGuru/PyInquirer/) (Menu)
- [Bs4](https://www.crummy.com/software/BeautifulSoup/) (Parsing)
- [aiohttp](https://docs.aiohttp.org/en/stable/) (Async requests)
- [requests](https://requests.readthedocs.io/en/latest/) (Requests)

## Authors:
- [@hurfy](https://github.com/hurfy)