import sys
sys.path.append('../')
from PIL import Image 
import imutils




def get_dimensions(file_name):
    '''
    get a geotiff file name and return its dimensions
    :param file_name: geotiff file name (string)
    :return: width, heigt, channel
    '''
    ds = Image.Open(file_name)
    width, height = ds.size 
    return width, height



def pyramid(image, scale=1, minSize=(3, 3)):
    # yield the original image
    yield image

    # keep looping over the pyramid
    while True:
        # compute the new dimensions of the image and resize it
        w = int(image.shape[1] / scale)
        image = imutils.resize(image, width=w)

        # if the resized image does not meet the supplied minimum
        # size, then stop constructing the pyramid
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break

        # yield the next image in the pyramid
        yield image

def sliding_window(image, stepSize, windowSize, progress=(0,0)):
    # slide a window across the image
    startPoint = progress[0]
    for y in range(progress[1], int(image.shape[0]), int(stepSize)):
        for x in range(startPoint, int(image.shape[1]), int(stepSize)):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
        startPoint = 0
