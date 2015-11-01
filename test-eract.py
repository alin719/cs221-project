import sys
import os
import cv2
import pytesseract
# from sklearn.externals import joblib
from skimage.feature import hog
try:
	import Image
except ImportError:
	from PIL import Image

img_folder = os.path.dirname(os.path.realpath(__file__)) + "/img/"


def test1():
	print("### test1: EUROTEXT ###")
	print("################")
	print(pytesseract.image_to_string(Image.open(img_folder + 'eurotext_clean.png')))
	print("################\n")

def test2():
	print("### test2: 5 + 2 = 9 ###")
	print("#################")
	print(pytesseract.image_to_string(Image.open(img_folder + '5+2=9_clean_10pct.png')))
	print("#################\n")

def test3a():
	print("### test3a: 5 + 2 = 9 ###")
	print("#################")
	image = Image.open(img_folder + '5+2=9_clean2_10pct.png')
	print(pytesseract.image_to_string(image))
	print("#################\n")

def test3aa():
	print("### test3aa: 5 + 2 = 9 ###")
	print("#################")
	image = Image.open(img_folder + '5+2=9_clean2_10pct.png')
	print(pytesseract.image_to_string(image, None))
	print("#################\n")

def test3b():
	print("### test3b: 5 + 2 = 9 ###")
	print("#################")
	#image = Image.open('5+2=9_clean2.png')
	cvimage = cv2.imread(img_folder + '5+2=9_clean2.png')
	half = cv2.resize(cvimage, (0,0), fx=0.5, fy=0.5) 
	cv2.imwrite(img_folder + "5+2=9_clean2_50.png", half)
	image = Image.open(img_folder + '5+2=9_clean2_50.png')
	print(pytesseract.image_to_string(image))

def test3c():
	print("### test3c: 5 + 2 = 9 ###")
	print("#################")
	img = Image.open(img_folder + '5+2=9_rect.png')
	img = img.resize((194, 42))
	print(pytesseract.image_to_string(img))
	print("#################\n")

def test4():
	print("### test4: 5 + 2 = 9 ###")
	print("#################")
	print(pytesseract.image_to_string(Image.open(img_folder + '5+2=9_clean3.png')))
	print("#################\n")

def test5():
	# Read the input image 
	im = cv2.imread(img_folder + "5+2=9.png")

	# Convert to grayscale and apply Gaussian filtering
	im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

	cv2.imwrite(img_folder + "5+2=9_cv.png", im_gray)

	# Threshold the image
	ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)

	# Find contours in the image
	ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# Get rectangles contains each contour
	rects = [cv2.boundingRect(ctr) for ctr in ctrs]

	# For each rectangular region, calculate HOG features and predict
	# the digit using Linear SVM.
	for rect in rects:
	    # Resize the image
	    roi = cv2.resize(im_th, (28, 28), interpolation=cv2.INTER_AREA)
	    roi = cv2.dilate(roi, (3, 3))
	    # Calculate the HOG features
	    roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
	    #cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

	im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
	cv2.imwrite(img_folder + "5+2=9_rect.png", im)

	cv2.imshow("Resulting Image with Rectangular ROIs", im)

def test6():
	print("### test1: hello world! ###")
	print("################")
	print(pytesseract.image_to_string(Image.open(img_folder + 'helloworld_10pct.png')))
	print("################\n")

# test1()
#test2()
#test3a()
#test3aa()
#test3b()
#test3c()
#test4()
#test5()
test6()