import cv2
from altmosaichelper import squarify, \
                            resize_main_img, \
                            process_squared_tiles, \
                            mosaify, \
                            blend_tiles_with_main_image, \
                            computeMosaicShape

from Parser import args_parser as ap
from Config import directories
from Utils.utils import clear_working_directories


def main():
    """
    .Uses the images in Img/Raw to create the tiled background for the mosaic.
    .Uses the main.jpeg image from Img/Main for the foreground image.
    .Each raw images are prepared by squaring the image with equal width and height. The square is centered
     in the raw image before the latter is cropped.
    .Colors from the receiving section of the main image are transferred on the tile with the fast color transfer
     algorythm.
    .A frame (or border) can be overlaid on the tile **Optional
    .The tiles are assembled.
    .The main image is overlaid on the assembled tiles. The weight from the alpha channel can be adjusted
     for both the background and foreground image.

    @return:
    """

    # Extracting args
    args = ap.parse_args()

    print('Starting to build the mosaic')

    print('Cleaning working directories...')
    clear_working_directories()

    # Computing how many columns and rows are available from the number of raw pictures
    (mosaic_height, mosaic_width) = computeMosaicShape(args.orientation)
    mosaic_height = int(mosaic_height)
    mosaic_width = int(mosaic_width)
    print("Parameters:\n\nHeight: {0}\nWidth: {1}\nTile Size: {2}\nTile Width: {3}\nTile Height: {4}\nResult Size: {5}"
          .format(mosaic_height, mosaic_width, args.tile_size, mosaic_width, mosaic_height,
                  str(args.tile_size*mosaic_width)+'x'+str(args.tile_size*mosaic_height)))

    # Extracting a centered square image from the raw images
    print('Squarifying tile pictures')
    squarify(args.tile_size)

    resize_main_img(mosaic_height*args.tile_size, mosaic_width*args.tile_size)
    print('Main image resized')

    print('Processing Squarified Tiles')
    process_squared_tiles(mosaic_width, mosaic_height, args)

    print('Assembling the mosaic')
    result = mosaify(mosaic_width, mosaic_height)

    print('Blending mosaic with main image')
    result = blend_tiles_with_main_image(result, args)

    print('Storing file')
    cv2.imwrite(directories.result_picture_folder + 'result.jpeg', result)

    print('Process Completed')


# Launch AltMosaic
if __name__ == '__main__':
    main()
