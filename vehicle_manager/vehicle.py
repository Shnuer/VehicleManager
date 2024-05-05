from typing import Optional

from .constants import ID_KEY
from .descriptors import FloatDesc, IDDesc, IntegerDesc, StringDesc, YearDesc


class Vehicle:
    id = IDDesc()
    name = StringDesc()
    model = StringDesc()
    year = YearDesc()
    color = StringDesc()
    price = IntegerDesc()
    latitude = FloatDesc()
    longitude = FloatDesc()

    def __init__(
        self,
        name: str,
        model: str,
        year: int,
        color: str,
        price: int,
        latitude: float,
        longitude: float,
        id: Optional[int] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__}: {self.name} {self.model} "
                f"{self.year} {self.color} {self.price}>")

    def get_dict_repr(self) -> dict:
        return {key[1:]: value for key, value in self.__dict__.items()}

    def get_dict_repr_except_id(self) -> dict:
        dict_data = self.get_dict_repr()
        del dict_data[ID_KEY]
        return dict_data
