from numpy import *
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import ctypes
import imageio
import cv2
import matplotlib.pyplot as plt
import bris
import os

widthUser = ctypes.windll.user32.GetSystemMetrics(0)
heightUser = ctypes.windll.user32.GetSystemMetrics(1)
filename = ""

def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir="/Users/louis/Perso/Polytech/4A/Projet/Image",  #mettre le dossier par défault
                                          title="Select a File",
                                          filetypes=(("all files","*.*"),   #formats de l'image autorisés
                                                    ("PNG image","*.png*"),
                                                     ("JPG image","*.jpg*")))

    test1 = Image.open(filename)

    width = int(ws / 2.5)           #Calcul des nouvelles dimentions de l'image
    height = int(test1.width * width / test1.height)
    if height > hs / 1.5:
        height = int(hs / 1.5)
        width = int(test1.height * height / test1.width)
    newSize = (height, width)

    test1 = test1.resize(newSize)   #Redéfinition de la taille de l'image

    test = ImageTk.PhotoImage(test1)    #Creation d'une image compatible pour le canevas à partir de l'image redimensionnée

    picture_label.configure(image=test)     #Affichage de l'image redimensionnée dans le canevas
    picture_label.photo = test
    picture_label.place(x=60, y=hs/2 - width/2)     #Replacement de l'image

def brisure():

    nb_pieces = bris.brisure(filename)
    piece_directory = "Pieces/"

    for file in os.listdir(piece_directory):
        fullfilename = os.path.join(piece_directory, file)
        img_temp = Image.open(fullfilename)
        img_temp.show()
fenetre = Tk(className='Puzzle resolver')

bg = '#FA8072'

ws = int(widthUser*0.75)
hs = int(heightUser*0.75)
fenetre.geometry(str(ws)+"x"+str(hs))

#image = PhotoImage(file="Pieces/piece__0.png")
canvas = Canvas(fenetre, width=ws, height=hs,bg= bg)

Menu = PhotoImage(file="Image/piece1.gif")
image_original = canvas.create_image(100,100,image="")

picture_label = Label(bg=bg)
picture_label.place(x=10,y=100)

button_explore = Button(fenetre,
                        text = "Browse Files",
                        command = browseFiles)
button_exit = Button(fenetre,
                     text = "Exit",
                     command = exit)
button_brisure = Button(fenetre,
                        text = "Break",
                        command = brisure)
button_explore.place(x=0,y=0)
button_exit.place(x=ws-30,y=0)
button_brisure.pack()

#canvas.bind("<Button-1>", Clic_Gauche)
canvas.pack()

fenetre.mainloop()