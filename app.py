# -*- coding: utf-8 -*-
"""
Created on Sun May 12 15:19:11 2019

@author: Zhen
"""

import tkinter as tk
import cv2
import os
from PIL import Image, ImageTk

from .common import config

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("600x400")
        
        title = tk.Label(text="Filter Project", font=config.TITLE_FONT)
        title.grid(row=0)

        apply_filter_button = tk.Button(text="Apply")
        apply_filter_button.grid(row=1)
        
        root_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(root_path, "resources", "image", "orig")
        img = cv2.imread(os.path.join(img_path, "sample_img.jpeg"))
#        print(img)
        height, width, no_channels = img.shape
        
        canvas = tk.Canvas(window, width=width, height=height)
#        canvas.pack()
        canvas.grid(row=2)
        photo = ImageTk.PhotoImage(image=Image.fromarray(img), master=canvas)
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        
        self.window.mainloop()
        
def run():
    # Create a window and pass it to the Application object
    App(tk.Tk(), "ZZ Image Filter")
        