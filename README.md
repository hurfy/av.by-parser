# AV.BY ASYNC PARSER
This is an async parser that searches for information about a car on the [av.by](https://cars.av.by) website.

*The [API](https://api.av.by/_doc) was used to compile the list of cars.<br>
*In the startup configuration setting, you must enable the "Emulate Terminal in output console" option.
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


## Authors:
- [@hurfy](https://github.com/hurfy)
