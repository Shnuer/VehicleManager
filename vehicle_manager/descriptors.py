import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class AbstractDescriptor(ABC):

    @abstractmethod
    def validate_value(self, value: Any):
        ...

    @abstractmethod
    def __set_name__(self, owner: type, name: str) -> None:
        ...

    @abstractmethod
    def __get__(self, instance: object, owner: type) -> None:
        ...

    @abstractmethod
    def __set__(self, instance: object, value: Any) -> None:
        ...


class BaseDescriptor(AbstractDescriptor):

    def __set_name__(self, owner: type, name: str):
        self.name = "_" + name

    def __get__(self, instance: object, owner: type):
        return getattr(instance, self.name)

    def __set__(self, instance: object, value: Any):
        self.validate_value(value)
        setattr(instance, self.name, value)


class StringDesc(BaseDescriptor):

    def validate_value(self, string_value: Any):
        if not isinstance(string_value, str):
            raise TypeError(f"{self.name} must be a string")


class IntegerDesc(BaseDescriptor):

    def validate_value(self, integer_value: Any):
        if not isinstance(integer_value, int):
            raise TypeError(f"{self.name} must be a integer")
        if integer_value < 0:
            raise ValueError(f"{self.name} value cannot be less zero")


class FloatDesc(BaseDescriptor):
    def validate_value(self, float_value: Any):
        if not isinstance(float_value, float):
            raise TypeError(f"{self.name} must be a float")


class YearDesc(BaseDescriptor):

    MAX_YEAR = datetime.now().year
    MIN_YEAR = 1885

    def validate_value(self, year_value: Any):
        if not isinstance(year_value, int):
            raise TypeError(f"{self.name} must be a integer")
        if year_value < self.MIN_YEAR:
            raise ValueError(
                f"The year of manufacture is less than "
                f"the first documented car: {self.MIN_YEAR}"
            )
        if year_value > self.MAX_YEAR:
            raise ValueError(
                f"The year of manufacture is greater than the current year: "
                f"{self.MAX_YEAR}"
            )


class IDDesc(BaseDescriptor):

    def validate_value(self, value: Any):
        if not isinstance(value, (int, type(None))):
            raise TypeError(f"{self.name} must be a integer or empty")


class URLDesc(BaseDescriptor):
    REGEX = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE
    )

    def validate_value(self, value: Any):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a integer or empty")

        if re.match(self.REGEX, value) is None:
            raise ValueError(f"{self.name} is invalid URL")
