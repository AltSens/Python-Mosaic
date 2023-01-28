import argparse
from Config.orientation import Orientation
from Config.masks import Masks

# Parses args and return a digested version
# orientation : Is the resulting image is horizontal or vertical
# tile_size : How big should be each tiles.
def parse_args():
    """
    Assembles the arguments passed to the app entrypoint and defines default values for the missing arguments.
    @return: Argument object containing all passed or default parameters.
    """
    parser = argparse.ArgumentParser(description='Mosaic Parameters')

    parser.add_argument('--orientation', dest='orientation', type=Orientation, choices=list(Orientation))
    parser.add_argument('--tile_size', dest='tile_size', type=int)
    parser.add_argument('--enable_mask', dest='enable_mask', type=bool)
    parser.add_argument('--mask_type', dest='mask_type', type=Masks, choices=list(Masks))
    parser.add_argument('--bgweight', dest='bgweight', type=float)  # Background weight (tiled image)
    parser.add_argument('--fgweight', dest='fgweight', type=float) # Main image

    args = parser.parse_args()

    if args.orientation is None:
        args.orientation = Orientation('horizontal')

    if args.tile_size is None:
        args.tile_size = 512

    if args.enable_mask is None:
        args.enable_mask = True

    if args.mask_type is None:
        args.mask_type = Masks('swoosh')

    # Alpha channel weight for the background
    if args.bgweight is None:
        args.bgweight = 0.5

    # Alpha channel weight for the main image (foreground)
    if args.fgweight is None:
        args.fgweight = 0.5

    return args
