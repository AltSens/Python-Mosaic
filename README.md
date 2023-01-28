# python_mosaic #
Digital mosaics are artworks that are created using digital technology, rather than traditional materials like glass or stone. They can be made using a variety of software programs, such as photo editing software, graphic design software, or specialized mosaic software.

One of the main advantages of digital mosaics is that they can be created and manipulated using a computer, which allows for greater precision and control than traditional mosaic techniques. Digital mosaics can be created using a single image, or by compositing multiple images together. They can also be easily adjusted, scaled, or color corrected.

Another advantage of digital mosaics is that they can be created and shared online, which makes them more accessible to a wider audience. They can be printed on various materials or even displayed on digital screens.

Digital mosaics can be used in a variety of ways, such as in advertising, graphic design, game design, and digital art. Some artists use digital mosaics as a way to create a new interpretation of a traditional artwork, while others use them to create entirely new and original pieces.

# Mean Square Error Algorithm #

There are several algorithms that can be used to create digital mosaics, but one of the most common is the "mean-squared-error" (MSE) algorithm. This algorithm is used to compare the color and brightness of each pixel in the source image (the image that will be used to create the mosaic) to the corresponding pixel in the target image (the image that will be used as the individual tiles in the mosaic).

The MSE algorithm works by calculating the difference between the color and brightness of each pixel in the source image and the corresponding pixel in the target image. This difference is then squared and added up for all the pixels in the image. The result is a single number that represents the overall difference between the two images.
![image](https://user-images.githubusercontent.com/83893249/215243004-c0ded7a8-9ba6-43ef-bf13-6b9046fb4363.png)


The MSE algorithm can be used to compare the source image to all the images in a library of potential tile images, and the image with the lowest MSE score is chosen as the best match.

Once the best match is found the target image is then replaced with the matching tile. This process is repeated for each pixel in the source image, until the entire image has been replaced with a mosaic of tile images.

One drawback is that it is sensitive to color variations and it does not take into account the texture and shape of the tile images. This can result in a mosaic that looks unnatural, as the tile images may not match the colors or patterns in the source image.

Another drawback is that the MSE algorithm tends to produce mosaic images that are lower in resolution than the original image. The more tiles used, the more the resolution will decrease, This can be a problem when creating large mosaics or when the source image has a lot of fine details.

Additionally, MSE algorithm can be computationally expensive, especially when working with high-resolution images or large libraries of tile images, as the algorithm needs to compare each pixel in the source image to each pixel in each tile image. This can be a problem when working with low-powered computers or when a large number of images need to be processed.

# Fast Color Transfer Algorithm #

Fast color transfer is an algorithm that aims to overcome some of the drawbacks of the Mean Squared Error (MSE) algorithm by transferring the color palette of the source image to the tile images before creating the mosaic.

The algorithm first converts the source image and tile images to a color space that is more perceptually uniform, such as the LAB color space. Then, it calculates the mean and standard deviation of the color channels in the source image. These values are then used to adjust the color channels of the tile images so that they match the color palette of the source image.
![image](https://user-images.githubusercontent.com/83893249/215278168-27c5e62f-d446-4208-9902-fc8cb7999f8a.png)

By matching the color palette of the tile images to the source image, fast color transfer can produce a mosaic that looks more natural and visually pleasing than one created using the MSE algorithm alone.
![image](https://user-images.githubusercontent.com/83893249/215278314-f315b110-502b-4c70-8aa1-5c5240743656.png)

In addition, fast color transfer algorithm can also be used to improve the resolution of the mosaic by transferring the texture of the source image to the tile images. This can be achieved by extracting the texture from the source image and then transferring it to the tile images.

Moreover, fast color transfer algorithm doesn't have the same computational burden as the MSE algorithm, it's faster and requires less computational power.

Overall, fast color transfer algorithm is a powerful tool for creating digital mosaics that can overcome some of the limitations of the MSE algorithm, by producing more natural and visually pleasing results with improved resolution and lower computational cost.

# Usage #

Entry point: altmosaic.py
Possible arguments:
  --orientation: horizontal or vertical
  --tile_size: Tiles are square. Both sides have equal length.
  --enable_mask: A mask is an overlay image that is used to add borders on the tile. With this project, masks are found in /Img/Masks/ forler.
  --mask_type: Let you choose from the types defined in /Config/masks.py. 
  --bgweight: The alpha channel weight of the background (tiled mosaic) 
  --fgweight: The alpha channel weight of the foreground (main image)

Ex: python3 altmosaic.py --orientation horizontal --tile_size 64 --enable_mask True --mask_type swoosh --bgweight 0.5 --fgweight 0.5
  
* The raw images you wish to use for your mosaic need to be found in /Img/Raw/.
* The main image need to be found in /Img/Main
* Your custom masks will reside in /Img/Masks. Because the tiles are resized to 512x512 in the processing stage, masks need to have these dimensions as   well.

## Algorithm ##
1. From the quantity of images available in the raw folder, we compute the maximum number of tiles for the rows and columns upon an aspect ration of 2:3.
2. Each raw tiles are preprocessed and cropped to a centered square. 
3. Each squarified tiles are processed and receives the color from an associated region of the main image.
4. A mask border might be overlayed on the tiles at this stage.
5. All the tiles are assembled into a mosaic.
6. The mosaic and the main image are blended together with the specified alpha level.
7. The result is outputed to /Img/Result/

