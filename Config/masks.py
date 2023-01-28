""" Mask enumeration and factory provider """

from enum import Enum

class Masks(Enum):
    """
    Help integration with argparser
    """
    swoosh = 'swoosh'
    square = 'square'
    square_thick = 'square-thick'
    circular = 'circular'
    none = 'none'

    def __str__(self):
        return self.value


def get_mask_filename(mask_type):
    """
    Factory where a filename associated with the mask type is returned.
    @param mask_type: Mask type enumerated in Masks' enums
    @return: The filename associated with the mask type
    """
    if mask_type == Masks('swoosh'):
        mask_filename = 'swooshmask_512x512.png'
    elif mask_type == Masks('square'):
        mask_filename = 'squaremask_512x512.png'
    elif mask_type == Masks('square-thick'):
        mask_filename = 'square_thickmask_512x512.png'
    elif mask_type == Masks('circular'):
        mask_filename = 'circlemask_512x512.png'
    else:
        mask_filename = 'none_512x512.png'    # default

    return mask_filename
