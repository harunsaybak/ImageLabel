# import the necessary packages
from helper import pyramid
from helper import sliding_window
import argparse
import time
import cv2
import os
import _pickle as cPickle
from shutil import copyfile
import keyboard 

#parameters
x = 30
(winW, winH) = (x,x)
stepSize = winW / 2
output_folder = 'images'
resolution = [1920, 1080]
accept_key = 121
exit_key = keyboard.is_pressed('n')


bound = 200
resolution[0] = resolution[0] - bound
resolution[1] = resolution[1] - bound

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    progress0 = [0,0,0]
else:
	progress0 = cPickle.load(open('images/progress.pik', 'rb'))


# just for quality control
#############################################################
positive_folder = output_folder + '/positive'
if not os.path.exists(positive_folder):
	os.makedirs(positive_folder)
negative_folder = output_folder + '/negative'
if not os.path.exists(negative_folder):
	os.makedirs(negative_folder)
#############################################################

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False, help="Path to the image")
args = vars(ap.parse_args())

# load the image and define the window width and height
image = cv2.imread("test1.jpg")


i = 0
labels = []
for (x, y, window) in sliding_window(image, stepSize=stepSize, windowSize=(winW, winH), progress = progress0):

	i = i + 1
	# if the window does not meet our desired window size, ignore it
	if window.shape[0] != winH or window.shape[1] != winW:
		continue

	# THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW, SUCH AS APPLYING A
	# MACHINE LEARNING CLASSIFIER TO CLASSIFY THE CONTENTS OF THE
	# WINDOW

	# since we do not have a classifier, we'll just draw the window
	if x + stepSize > resolution[0]:
		x1 = x - resolution[0] + stepSize + bound
	else:
		x1 = 0
	x2 = x1 + resolution[0] + bound
	if y + stepSize > resolution[1]:
		y1 = y - resolution[1] + stepSize + bound
	else:
		y1 = 0
	y2 = y1 + resolution[1] + bound
	clone = image.copy()[y1:, x1:]
	cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
	cv2.imshow("Window", clone)
	name = '{0}/{1}.jpg'.format(output_folder, str(i).zfill(5))
	#print(name)
	cv2.imwrite(name,window)



	key = cv2.waitKey(0)
	if key == exit_key:

		break
	labels.append(key)
	#print key
	time.sleep(0.025)
	progress = [x+stepSize, y, i]
	#print 'image: [{0}:{1}, {2}:{3}] \t window: [{4}:{5}, {6}:{7}]'.format(x1, clone.shape[1] + x1, y1, clone.shape[0] + y1, x,x + stepSize, y, y + stepSize)
	
	#############################################################################
	if key == accept_key:
		copyfile(name, '{0}/{1}.jpg'.format(positive_folder, str(i).zfill(5)))
	else:
		copyfile(name, '{0}/{1}.jpg'.format(negative_folder, str(i).zfill(5)))
	#############################################################################


#print labels
i = progress0[2]
with open('images/labels.txt', 'a') as f:
	for label in labels:
		i = i + 1
		if label == accept_key:
			f.write('{0}.jpg {1}\n'.format(str(i).zfill(5), str(1)))
		else:
			f.write('{0}.jpg {1}\n'.format(str(i).zfill(5), str(0)))

cPickle.dump(progress, open('images/progress.pik', 'wb')) 
