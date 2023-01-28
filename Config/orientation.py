from enum import Enum

class Orientation(Enum):
    """
    To help integration with argparser
    """
    vertical = 'vertical'
    horizontal = 'horizontal'

    def __str__(self):
        return self.value
