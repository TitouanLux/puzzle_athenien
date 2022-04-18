from numpy import *
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
import ctypes
import cv2
import matplotlib.pyplot as plt
import os

def Detection(filename):

    piece = "Pieces/"
    original = filename
    image_original = cv2.imread(original)
    detector = cv2.xfeatures2d.SIFT_create()
    keypoints_2, descriptors_2 = detector.detectAndCompute(image_original, None)
    coords = []

    for file in os.listdir(piece):
        fullfilename = os.path.join(piece, file)
        image = cv2.imread(fullfilename)
        # img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # ret,BW = cv2.threshold(img_grey, 0, 255, cv2.THRESH_BINARY)
        keypoints, descriptors = detector.detectAndCompute(image, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors, descriptors_2, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.5 * n.distance:
                good.append([m])
        x_good = []
        y_good = []
        for i in range(0, len(good) - 1):
            x_good.append(keypoints_2[good[i][0].trainIdx].pt[0])
            y_good.append(keypoints_2[good[i][0].trainIdx].pt[1])

        xc = np.mean(x_good)
        yc = np.mean(y_good)

        coords.append([xc, yc])

        image_cpy = image_original.copy()
        cv2.circle(image_cpy, (int(xc), int(yc)), 20, (255, 255, 255), 4)

        images = cv2.drawMatchesKnn(image, keypoints, image_original, keypoints_2, good, None)

        img_concate_Hori=np.concatenate((image_cpy,image),axis=1)
        #cv2.imshow('frame', images[::2, ::2, :])
        cv2.imshow('frame', img_concate_Hori[::2, ::2, :])
        cv2.waitKey()
        cv2.destroyAllWindows()