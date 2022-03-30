from numpy import *
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
import ctypes
import cv2
import matplotlib.pyplot as plt
import os

mask = "Mask/"
piece = "Pieces/"
original = "Image/original.PNG"
image_original = cv2.imread(original)
detector = cv2.xfeatures2d.SIFT_create()
keypoints_2, descriptors_2 = detector.detectAndCompute(image_original, None)

for file in os.listdir(piece):
    fullfilename = os.path.join(piece, file)
    image = cv2.imread(fullfilename)
    #img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ret,BW = cv2.threshold(img_grey, 0, 255, cv2.THRESH_BINARY)
    keypoints, descriptors = detector.detectAndCompute(image, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors, descriptors_2, k=2)
    good=[]
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    x_good = []
    y_good = []
    for i in range(0, len(good) - 1):
        x_good.append(keypoints_2[good[i][0].trainIdx].pt[0])
        y_good.append(keypoints_2[good[i][0].trainIdx].pt[1])

    xc = np.mean(x_good)
    yc = np.mean(y_good)

    cv2.circle(image_original, (int(xc), int(yc)), 20, (0, 0, 255), 4)

    images = cv2.drawMatchesKnn(image, keypoints, image_original, keypoints_2, good, None)
    cv2.imshow('frame',images[::2,::2,:])
    cv2.waitKey()
    cv2.destroyAllWindows()

    """image = cv2.imread(fullfilename)
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,BW = cv2.threshold(img_grey, 0, 255, cv2.THRESH_BINARY)

    img_contours = np.zeros(image.shape)
    contours, hierarchy = cv2.findContours(BW, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img_contours, contours, -1, (1,1,1), 1)

    plt.imshow(img_contours)
    plt.show()"""

cv2.imshow('frame',image_original)
cv2.waitKey()
cv2.destroyAllWindows()
