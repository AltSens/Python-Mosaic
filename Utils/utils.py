import shutil
from os import listdir, makedirs
from os.path import isfile, join
import cv2
import numpy as np
from Config import directories


# Get the list of files in a specific folder
def getFileList(folderPath):
    """
    Get the list of files from the folder path
    @param folderPath: Folder containing the list of files
    @return: List of files from the folder's path
    """
    return [f for f in listdir(folderPath) if isfile(join(folderPath, f))]


def clear_working_directories():
    """
    Cleanup images folders except for the raw folder where the users pictures are.
    @return:
    """
    shutil.rmtree(directories.squared_picture_folder)
    shutil.rmtree(directories.result_picture_folder)
    shutil.rmtree(directories.processed_picture_folder)

    makedirs(directories.squared_picture_folder)
    makedirs(directories.result_picture_folder)
    makedirs(directories.processed_picture_folder)



def color_transfer(source, target):
    """
    Transfers the color style from the source image to the target images
    using LAB color space
    ref : https://pyimagesearch.com/2014/06/30/super-fast-color-transfer-images/
    @param source: Image with the colors we wish to transfer
    @param target: Image to which we wish to transfer the colors to
    @return: The resulting image
    """
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # compute color statistics for the source and target images
    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc,
     bMeanSrc, bStdSrc) = image_stats(source)

    (lMeanTar, lStdTar, aMeanTar, aStdTar,
     bMeanTar, bStdTar) = image_stats(target)

    # subtract the means from the target image
    (lu, a, b) = cv2.split(target)
    lu -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar

    # add in the source mean
    lu += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc

    # clip the pixel intensities to [0, 255] if they fall outside
    # this range
    lu = np.clip(lu, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    # merge the channels together and convert back to the RGB color
    # space, being sure to utilize the 8-bit unsigned integer data
    # type
    transfer = cv2.merge([lu, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    # return the color transferred image
    return transfer


def image_stats(image):
    """
    Compute the mean and standard deviation of each channel
    ref : https://pyimagesearch.com/2014/06/30/super-fast-color-transfer-images/
    @param image:
    @return:
    """
    (l, a, b) = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())

    # return the color statistics
    return lMean, lStd, aMean, aStd, bMean, bStd



def overlay_transparent(background_img,
                        img_to_overlay_t,
                        x, y, overlay_size=None):
    """
    @brief      Overlays a transparant PNG onto another image using CV2
    # ref : https://gist.github.com/clungzta/b4bbb3e2aa0490b0cfcbc042184b0b4e

    @param      background_img    The background image
    @param      img_to_overlay_t  The transparent image to overlay
                                  (has alpha channel)
    @param      x                 x location to place the top-left corner
                                  of our overlay
    @param      y                 y location to place the top-left corner
                                  of our overlay
    @param      overlay_size      The size to scale our overlay to (tuple),
                                  no scaling if None

    @return     Background image with overlay on top
    """

    bg_img = background_img.copy()
    if overlay_size is not None:
        img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

    # Extract the alpha mask of the RGBA image, convert to RGB
    b, g, r, a = cv2.split(img_to_overlay_t)
    overlay_color = cv2.merge((b, g, r))

    # Apply some simple filtering to remove edge noise
    mask = cv2.medianBlur(a, 5)

    h, w, _ = overlay_color.shape
    roi = bg_img[y:y+h, x:x+w]

    # Black-out the area behind the logo in our original ROI
    img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(),
                              mask=cv2.bitwise_not(mask))

    # Mask out the logo from the logo image.
    img2_fg = cv2.bitwise_and(overlay_color, overlay_color, mask=mask)

    # Update the original image with our new ROI
    bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

    return bg_img
