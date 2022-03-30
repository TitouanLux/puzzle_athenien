import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import random, randrange
import skimage as sk
from skimage import measure, filters, color
import scipy as sp
from scipy import ndimage
import os

def brisure(filename):

    input_directory = "Image/"
    output_directory = "Pieces/"
    mask_directory = "Mask/"
    if not os.path.exists(input_directory): os.mkdir(input_directory)
    if not os.path.exists(output_directory): os.mkdir(output_directory)
    if not os.path.exists(mask_directory): os.mkdir(mask_directory)
    image = cv2.imread(filename)  # ouverture de l'image
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    height, width, col = image.shape  # Recuperation des dimention de l'image

    crackSize = 20  # Gestion de la taille des brisures

    # gestion de la brisure horizontale
    startPoint = (
        0,
        int(height / 2) + randrange(int(height / 10)) - int(height / (crackSize * 2)))  # mise en place du point de départ
    endPoint = startPoint  # declaration du point d'arret

    while (endPoint[0] < width):
        startPoint = endPoint  # heritage du point d'arret
        endPoint = (startPoint[0] + randrange(int(width / crackSize)) + 50,
                    startPoint[1] + randrange(int(height / crackSize)) - int(
                        height / (crackSize * 2)))  # mise en place du prochain point d'arret
        image = cv2.line(image, startPoint, endPoint, (255, 255, 255), 1)  # on dessine la ligne sur l'image

    # meme chose pour la brisure verticale
    startPoint = (int(width / 2) + randrange(int(width / 10)) - int(width / (crackSize * 2)), 0)
    endPoint = startPoint

    while (endPoint[1] < height):
        startPoint = endPoint
        endPoint = (startPoint[0] + randrange(int(width / crackSize)) - int(width / (crackSize * 2)),
                    startPoint[1] + randrange(int(height / crackSize)) + 50)
        image = cv2.line(image, startPoint, endPoint, (255, 255, 255), 1)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    BW = np.where(gray == 255, 0, 1)

    connectivity = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    label, nb_labels = sp.ndimage.measurements.label(BW, connectivity)
    histo, bins = sk.exposure.histogram(label)

    for i in range(nb_labels):
        img_mask = np.where(label == i+1, 1,0)

        output_filename = "Piece_" + str(i) + ".png"
        fullPathName = os.path.join(output_directory, output_filename)
        output_filename = "MaskPiece_" + str(i) + ".png"
        fullPathNameMask = os.path.join(mask_directory, output_filename)
        img_piece = image.copy()
        img_piece[:, :, 0] = image[:, :, 0] * img_mask
        img_piece[:, :, 1] = image[:, :, 1] * img_mask
        img_piece[:, :, 2] = image[:, :, 2] * img_mask
        alpha = np.sum(img_piece, axis=-1) > 0
        alpha = np.uint8(alpha * 255)
        res = np.dstack((img_piece, alpha))

        cv2.imwrite(fullPathName, res)
        img_mask = img_mask * 255
        cv2.imwrite(fullPathNameMask, img_mask)
        plt.imshow(res)

    return nb_labels