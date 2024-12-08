from typing import Any
from json   import load, dump
from os     import path, mkdir


class FileManager:
    @classmethod
    def write_json(cls, path_: str, data: list[Any]) -> None:
        """Writes data to JSON"""
        with open(path_, "w", encoding="UTF-8") as file:
            dump(data, file, indent=4, ensure_ascii=False)

    @classmethod
    def load_cars(cls, path_: str) -> dict[Any, Any] | list[Any]:
        """Loading car list data from JSON"""
        with open(path_, "r", encoding="UTF-8") as file:
            return load(file)

    @classmethod
    def dir_exist(cls, path_: str) -> None:
        """Creates an output folder if it does not exist"""
        if not path.exists(path_):
            mkdir(path_)
