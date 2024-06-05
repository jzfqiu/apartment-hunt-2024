from dataclasses import dataclass
from typing import Literal


@dataclass
class Apartment:
    apt_name: str
    apt_num: str
    layout: Literal["Studio", "1 Bed", "2 Bed", ">2 Bed"]
    price: int
    available: str

    def __repr__(self) -> str:
        return (
            f"Property: {self.apt_name}\n"
            f"Apt #: {self.apt_num}\n"
            f"Layout: {self.layout}\n"
            f"Price: ${self.price}\n"
            f"Availale after: {self.available}"
        )

    def meets_condition(self) -> bool:
        return (
            self.price < 3200
            and self.available > "2024-08-15"
            and self.available < "2024-09-25"
        )
