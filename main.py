from parser     import gather_cars_data, cars_count
from PyInquirer import prompt
from json       import load
from examples   import custom_style_2
from asyncio    import run
from os.path    import exists
from os         import makedirs
from json       import dump
from csv        import writer


def load_cars_list() -> dict:
    """
    The function returns the dictionary of cars from cars.json
    :return: dict: Auto dict
    """
    with open('cars.json', 'r', encoding='UTF-8') as file:
        return load(file)


def create_menu(text: str, choice: list) -> str:
    """
    The function creates a menu using the PyInquirer module
    :param text:    str: Question text
    :param choice: list: Choice
    :return:        str: Choice result
    """
    menu = [
        {
            'type': 'list',
            'name': 'result',
            'message': text,
            'choices': choice
        }
    ]

    return prompt(menu, style=custom_style_2)['result']


def write_to_json(name: str, path: str, text: list) -> None:
    """
    The function writes the results to a .json file
    :param name:  str: File name
    :param path:  str: File path
    :param text: list: Text to write
    :return:           None
    """
    with open(f'{path}/{name}.json', 'w', encoding='UTF-8', newline='') as file:
        dump([car.get_info() for car in text], file, ensure_ascii=False, indent=4)


def write_to_csv(name: str, path: str, text: list) -> None:
    """
    The function writes the results to a .csv file
    :param name:  str: File name
    :param path:  str: File path
    :param text: list: Text to write
    :return:           None
    """
    with open(f'{path}/{name}.csv', 'w', encoding='UTF-8', newline='') as file:
        csv_writer = writer(file, delimiter=';')

        for car in text:
            car = car.get_info()
            csv_writer.writerow([car['model'], car['price'], car['params'], car['url']])


def select_car() -> tuple:
    """
    The function creates a menu from a list of cars and their models,
    allowing the user to conveniently select makes and models of cars
    :return: tuple: (Brand, Brand ID, Model, Model ID)
    """
    cars_list = load_cars_list()

    selected_brand = create_menu('Choose a car brand:', [i for i in cars_list.keys()])
    selected_model = create_menu('Choose a model:', [i for i in cars_list[selected_brand]['models']])

    return selected_brand, cars_list[selected_brand]['id'],\
        selected_model, cars_list[selected_brand]['models'][selected_model]


async def main() -> None:
    """
    The function starts an infinite loop, which can be terminated only by user's decision.
    Creates a menu with auto and model selection, processes other inputs. Writes the results to files.
    :return: None
    """
    while True:
        brand, brand_id, model, model_id = select_car()

        # If the number of auto is 0, the search will not be performed
        if (count := await cars_count(brand_id, model_id)) == 0:
            if create_menu('0 cars found, want to continue?', ['Yes', 'No']) == 'Yes':
                continue
            break

        cars = await gather_cars_data(brand_id, model_id, count)
        name = f'{brand.lower().replace(" ", "_")}_{model.lower().replace(" ", "_").replace("-", "_")}'
        path = fr'output/{name}'

        # Print the list of found cars
        if create_menu(f'{len(cars)} cars found, show list?', ['Yes', 'No']) == 'Yes':
            [print(f'{car}\n') for car in cars]

        # Checking the folder
        if not exists(path):
            makedirs(path, exist_ok=True)

        # Writing to files
        write_to_json(name, path, cars)
        write_to_csv(name, path, cars)

        # Continue searching
        if create_menu(f'Want to continue?', ['Yes', 'No']) == 'No':
            break


if __name__ == '__main__':
    run(main())
