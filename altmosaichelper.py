""" Complex logic or reusable piece of code for altmosaic.py """
import cv2
from Utils.utils import getFileList, color_transfer, overlay_transparent
from Utils import progressbar
from Config import directories
from Config.masks import get_mask_filename
from Config.orientation import Orientation
import numpy as np


def computeMosaicShape(orientation):
    """
    From the number of pictures in the raw folder, the maximum columns and rows are computed
    orientation : Horizontal ratio : 2x3
    orientation : Vertical ratio : 3x2
    @param orientation:
    @return: Height, Width
    """

    w = 0
    h = 0

    nbs_pictures = len(getFileList(directories.raw_picture_folder))
    if nbs_pictures < 6:
        return 0, 0

    if orientation == Orientation('horizontal'):
        h = int(np.sqrt(nbs_pictures * 2 / 3))
        w = int(np.sqrt(nbs_pictures * 3 / 2))
    elif orientation == Orientation('vertical'):
        h = int(np.sqrt(nbs_pictures * 3 / 2))
        w = int(np.sqrt(nbs_pictures * 2 / 3))

    # If we return 0, 0, there's an error
    # Should manage to throw an error!!
    return h, w


def resize_main_img(width, height):
    """
    Resizes the main image with the specified width and height
    @param width: Desired width
    @param height: Desired height
    @return: The modified image
    """
    main_picture_list = getFileList(directories.main_picture_folder)
    img = cv2.imread(directories.main_picture_folder + main_picture_list[0], cv2.IMREAD_UNCHANGED)
    dsize = (height, width)
    img = cv2.resize(img, dsize)
    cv2.imwrite(directories.main_picture_folder + 'main.jpeg', img)


def squarify(tile_size=512):
    """
    From the dimension of the image's smallest side, the image is cropped along the longest side in a way
    where both the square's and the image's center overlap.
    @param tile_size: Size of the square's side (Default is 512)
    @return: The squared image
    """
    raw_picture_list = getFileList(directories.raw_picture_folder)

    # for picture_filename in raw_picture_list:
    for picture_filename in progressbar.progressBar(raw_picture_list, prefix='Progress:', suffix='Complete', length=50):
        tile = cv2.imread('Img/Raw/'+picture_filename)
        (height, width, channel) = tile.shape

        if height > width:
            offset = int((height - width)/2)
            tile = tile[offset:offset+width, :]

        elif width > height:
            offset = int((width - width) / 2)
            tile = tile[:, offset:offset + height]

        tile = cv2.resize(tile, (tile_size, tile_size))

        tile = cv2.cvtColor(tile, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(directories.squared_picture_folder + '{0}.png'.format(picture_filename.split('.')[0]), tile)


def process_squared_tiles(mosaic_width, mosaic_height, args):
    """
    Each square tile is associated with a region on the main image. This region's color scheme is transferred
    on the tile. If a mask was previously requested, it will be overlaid on the tile. The resulting tile is
    persisted in the /Img/Processed/ folder
    @param mosaic_width: How many columns are there in the mosaic
    @param mosaic_height: How many rows are there in the mosaic
    @param args: Arguments from the program's entrypoint
    @return:
    """
    col = mosaic_width
    row = mosaic_height
    counter = 0

    # List of raw pictures
    img_list = getFileList(directories.squared_picture_folder)

    # Instantiate required pictures
    main_img = cv2.imread(directories.main_picture_folder + 'main.jpeg')
    mask_img = cv2.imread(directories.mask_picture_folder + get_mask_filename(args.mask_type),
                          cv2.IMREAD_UNCHANGED)
    mask_img = cv2.resize(mask_img, (args.tile_size, args.tile_size))

    # for i in range(row):
    for i in progressbar.progressBar(range(row), prefix='Progress:', suffix='Complete', length=50):
        for j in range(col):
            # print(str(i) + "  " + str(j) + "    " + img_list[counter])
            sub_img = main_img[args.tile_size*i:args.tile_size*(i+1), args.tile_size*j:args.tile_size*(j+1)]

            img = cv2.imread(directories.squared_picture_folder + img_list[counter])
            img = cv2.resize(img, (args.tile_size, args.tile_size))

            transferred = color_transfer(sub_img, img)

            finished_img = overlay_transparent(transferred,
                                               mask_img, 0, 0)
            cv2.imwrite(directories.processed_picture_folder + str(counter) + '.jpeg',
                        finished_img)
            counter = counter + 1


# Assembling the tiles in the order they were generated.
# The result is an image resulting from the tile's matrix.
#
def mosaify(col, row):
    """
    Assembles the processed tiles into a mosaic with a size matching the main image.
    @param col: The number of columns in the mosaic
    @param row: The number of rows in the mosaic
    @return:
    """
    nbs_tiles = col*row
    initial_loop = 0
    new_loop_beginning = 0

    im_v = None
    im_h = None

    initialised_vertical = False
    for i in range(nbs_tiles):
        # Todo - Should validate if the image exists first
        tile = cv2.imread(directories.processed_picture_folder + str(i) + '.jpeg')

        # Todo - Rework to have less ifs
        if i % col == new_loop_beginning:
            if i != initial_loop:
                if initialised_vertical is False:
                    im_v = im_h
                    initialised_vertical = True
                else:
                    im_v = cv2.vconcat([im_v, im_h])

                im_h = tile
            else:
                im_h = tile
        else:
            im_h = cv2.hconcat([im_h, tile])

    # Add the last horizontal concatenation
    im_v = cv2.vconcat([im_v, im_h])

    return im_v


def blend_tiles_with_main_image(img1, args):
    """
    Merges img1 and img2 based on their alpha channel values defined in the application entrypoint
    arguments. The main image is automatically provided from /Img/Main/main.jpg
    @param img1: The tiled mosaic
    @param args: Entrypoint arguments
    @return: Merged image
    """
    main_img = cv2.imread(directories.main_picture_folder + 'main.jpeg')
    return cv2.addWeighted(img1, args.bgweight, main_img, args.fgweight, 0)
