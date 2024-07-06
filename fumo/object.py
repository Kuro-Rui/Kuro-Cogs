from dataclasses import dataclass
from typing import List

import discord


@dataclass
class Fumos:
    friday: List[str]
    gif: List[str]
    image: List[str]
    video: List[str]

    @property
    def all(self) -> List[str]:
        all_fumos = self.gif + self.image + self.video
        if discord.utils.utcnow().weekday() == 4:
            all_fumos += self.friday
        return all_fumos
