'''Provide example to update variable.'''

from dataclasses import dataclass


@dataclass
class Settings:
    var1: str
    var2: str = 'default'
