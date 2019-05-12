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
from .filters.point_filters import polarize_filter

class App:
    def __init__(self, window, window_title):
        """
        Initialize app window and start main loop
        """
        self.window = window
        self.window.title(window_title)
        self.window.geometry("600x350")
        
        title = tk.Label(text="Filter Project", font=config.TITLE_FONT)
        title.grid(row=0, column=0, columnspan=3)

        #TODO: put into config
        root_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(root_path, "resources", "image", "orig")
        self.orig_img = cv2.imread(os.path.join(img_path, "pku.jpg"),
                              cv2.IMREAD_GRAYSCALE)
        self.out_img = self.orig_img
        print(self.orig_img)
        
        height, width = self.orig_img.shape
        self.orig_canvas = tk.Canvas(window, width=width, height=height)
        self.orig_canvas.grid(row=1, column=0)
        self.orig_photo = ImageTk.PhotoImage(master=self.orig_canvas,
                                             image=Image.fromarray(self.orig_img))
        self.orig_canvas.create_image(0, 0, 
                                      image=self.orig_photo,
                                      anchor=tk.NW)
        
        self.out_canvas = tk.Canvas(window, width=width, height=height)
        self.out_canvas.grid(row=1, column=2)
        self.out_photo = ImageTk.PhotoImage(master=self.out_canvas,
                                            image=Image.fromarray(self.out_img))
        self.out_img_on_canvas = self.out_canvas.create_image(0, 0, 
                                          image=self.out_photo,
                                          anchor=tk.NW)
        
        apply_filter_button = tk.Button(text="Apply", bg="white",
                                        command=lambda:self.apply(polarize_filter))
        apply_filter_button.grid(row=1, column=1)
        
        # Saving
        save_button = tk.Button(text="Save", bg="white",
                                command=lambda:self.save(self.out_img))
        save_button.grid(row=2, column=0, columnspan=3)
        
        # Start main loop
        self.window.mainloop()
        
    def apply(self, point_filter):
        """
        Apply filter pointwise to self.orig_img, set and display self.out_img
        point_filter: the filter to be applied
        """
        #TODO: ensure value between 0 and 255
        self.out_img = point_filter(self.orig_img)
        print(self.out_img)
        self.out_photo = ImageTk.PhotoImage(master=self.out_canvas,
                                            image=Image.fromarray(self.out_img))
        self.out_canvas.itemconfig(self.out_img_on_canvas, image = self.out_photo)
        
    def save(self, img):
        """
        img: image to be saved, represented as numpy array
        Save image to specific path (currently static defined)
        """
        #TODO: generalize filename generation
        filename = "test.png"
        root_path = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(root_path, "resources", "image", "out")
        cv2.imwrite(os.path.join(save_path, filename), img)
        self.after_save(os.path.join(save_path, filename))
        
    def after_save(self, filename):
        """
        filename: path + filename
        Display message after saving image
        """
        save_message = "Image has been saved to {}".format(filename)
        save_display = tk.Text(master=self.window, height=3, width=50)
        save_display.grid(row=3, column=0, columnspan=3)
        save_display.insert(tk.END, save_message)
        
        
def run():
    """
    Create a window and pass it to the Application object
    """
    App(tk.Tk(), "ZZ Image Filter")
        