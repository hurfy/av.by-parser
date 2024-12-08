from functools   import wraps
from asyncio     import run
from typing      import Any, AnyStr, Callable, Coroutine, Optional, Annotated
from typer       import Argument, run as typer_run
from os          import path
from datetime    import datetime

from controllers import Fm, Mm, Config, Brand, Model
from parser      import CarParser, Car

ROOTDIR: AnyStr = path.dirname(path.dirname(path.abspath(__file__)))


def async_typer(func: Callable) -> Callable:
    """Wrapper for async typer run"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Coroutine:
        return run(func(*args, **kwargs))

    return wrapper


@async_typer
async def main(
        brand: Annotated[Optional[int], Argument(help="Brand ID")] = None,
        model: Annotated[Optional[int], Argument(help="Model ID")] = None,
) -> None:
    """main ..."""
    if brand is None or model is None:
        config: Config = await Mm(
            Fm.load_cars(r"{}\public\cars.json".format(ROOTDIR))
        ).execute()

    else:
        config: Config = Config(
            brand=Brand(name=None, id=brand),
            model=Model(name=None, id=model),
        )

    # Parse public
    async with CarParser(config) as parser:
        car_list: list[Car] = await parser.parse()

    # Validate and serialize public
    dumped_list: list[dict[str, Any]] = [
        each.model_dump(mode="json") for each in car_list
    ]

    # Save finished public
    Fm.dir_exist(r"{}/output/".format(ROOTDIR))
    Fm.write_json(r"{}/output/{}.json".format(
        ROOTDIR,
        datetime.now().strftime("%d-%m-%Y-%H-%M-%S")),
        dumped_list
    )


if __name__ == "__main__":
    typer_run(main)
