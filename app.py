# -*- coding: utf-8 -*-
"""
Created on Sun May 12 15:19:11 2019

@author: Zhen
"""

import tkinter
import cv2
import os
from PIL import Image, ImageTk

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        root_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(root_path, "resources", "image", "orig")
        img = cv2.imread(os.path.join(img_path, "sample_img.jpeg"))
#        print(img)
        height, width, no_channels = img.shape
        
        canvas = tkinter.Canvas(window, width = width, height = height)
        canvas.pack()
        photo = ImageTk.PhotoImage(image = Image.fromarray(img), master=canvas)
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

        self.window.mainloop()
        
def run():
    # Create a window and pass it to the Application object
    App(tkinter.Tk(), "ZZ Image Filter")
        