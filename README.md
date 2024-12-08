<div align="center">
    <a href="https://github.com/hurfy/av.by-parser"><img src="https://github.com/user-attachments/assets/1d99334f-d0a6-4000-82d5-4b2ebe1f5935" alt="av.by-parser" /></a>
</div>

<div align="center">
    <img src="https://img.shields.io/github/issues/hurfy/av.by-parser?style=for-the-badge" alt="open issues" />
    <img src="https://img.shields.io/badge/version-1.1.0-blue?style=for-the-badge" alt="version" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/github/license/hurfy/av.by-parser?style=for-the-badge" alt="license" /></a>
</div>

<br />

<div align="center">
  Simple async ad parser :)
</div>

<div align="center">
  <sub>
    Built with love 
    &bull; Brought to you by <a href="https://github.com/hurfy">@hurfy</a>
    and other <a href="https://github.com/hurfy/av.by-parser/graphs/contributors">contributors</a>
  </sub>
</div>

## Introduction
This is an async parser that searches for information about a car on the [av.by](https://cars.av.by) website.

## Quick Start
First of all, start the application using CMD, otherwise it is unlikely to start.<br>*You can use “Emulate Terminal in output console” if you use PyCharm.

Clone the repository:
```cmd
  git clone git@github.com:hurfy/av.by-parser.git
```
Install requirements:
```cmd
  pip install -r requirements.txt
```
Done, now just run the main.py file:
```cmd
  python src/main.py
```

There are two ways to start it:
1. Without specifying parameters. In this case, a menu will be created where the user will be prompted to select the make and model of the car.
    ```cmd
      python src/main.py
    ```
2. With parameters specified. In this case the application will parse the car with the specified id.
   `--brand --model`
    ```cmd
      python src/main.py 84 521
    ```
Python 3.11 was used in the development, so I do not guarantee its performance on other versions.

## JSON Example:
```json
{
     "model": "Aito M5",
     "params": "2022 г., автомат, 1,5 л, бензин (гибрид), внедорожник 5 дв., 4 591 км",
     "price": {
         "byn": 30500,
         "usd": 106125
     },
     "url": "https://cars.av.by/aito/m5/111030007"
}
```

## Libraries:
- [pydantic](https://docs.pydantic.dev/latest/) (validation)
- [typer](https://typer.tiangolo.com/) (CLI)
- [questionary](https://questionary.readthedocs.io/en/stable/) (menu)
- [Bs4](https://www.crummy.com/software/BeautifulSoup/) (parsing)
- [aiohttp](https://docs.aiohttp.org/en/stable/) (async requests)
