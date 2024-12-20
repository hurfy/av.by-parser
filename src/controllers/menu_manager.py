from questionary         import select
from typing              import Any

from controllers.schemas import Brand, Model, Config


class MenuManager:
    def __init__(self, cars: dict[str, Any]) -> None:
        self.cars: dict[str, Any] = cars

    @staticmethod
    async def _create_menu(message: str, choices: list[Any]) -> Any:
        """Creates a selection menu and returns the user's selection"""
        return await select(
            message=message,
            choices=choices,
        ).ask_async()

    async def execute(self) -> Config:
        """Creates a menu with a selection of brand and model"""
        brand    = await self._create_menu("Choose a brand:", self.cars.keys())
        brand_id = self.cars[brand]["id"]

        model    = await self._create_menu("Choose a model:", self.cars[brand]["models"])
        model_id = self.cars[brand]["models"][model]

        return Config(
            brand=Brand(name=brand, id=brand_id),
            model=Model(name=model, id=model_id),
        )
