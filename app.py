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
from .filters.point_filters import PolarizeFilter, WhitenFilter

class App:
    def __init__(self, window, window_title):
        """
        Initialize app window and start main loop
        """
        #TODO: put into config
        root_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(root_path, "resources", "image")
        
        # Initialize app window
        self.window = window
        self.window.title(window_title)
        self.window.geometry("600x350")
        self.window.wm_iconbitmap(os.path.join(img_path, "zz.ico"))
        
        # Title object
        title = tk.Label(text="Filter Project", font=config.TITLE_FONT)
        title.grid(row=0, column=0, columnspan=3)

        # Load original image
        #TODO: add load functionality
        self.orig_img = cv2.imread(os.path.join(img_path, "orig", "pku.jpg"),
                              cv2.IMREAD_GRAYSCALE)
        self.out_img = self.orig_img
        print(self.orig_img)
        
        # Show original image
        height, width = self.orig_img.shape
        self.orig_canvas = tk.Canvas(window, width=width, height=height)
        self.orig_canvas.grid(row=1, column=0)
        self.orig_photo = ImageTk.PhotoImage(master=self.orig_canvas,
                                             image=Image.fromarray(self.orig_img))
        self.orig_canvas.create_image(0, 0, 
                                      image=self.orig_photo,
                                      anchor=tk.NW)
        
        # Show output image, initialized as a copy of original image
        self.out_canvas = tk.Canvas(window, width=width, height=height)
        self.out_canvas.grid(row=1, column=2)
        self.out_photo = ImageTk.PhotoImage(master=self.out_canvas,
                                            image=Image.fromarray(self.out_img))
        self.out_img_on_canvas = self.out_canvas.create_image(0, 0, 
                                          image=self.out_photo,
                                          anchor=tk.NW)
        
        # Button to apply filter and update output image
        f = PolarizeFilter()
        apply_filter_button = tk.Button(text="Apply", bg="white",
                                        command=lambda:self.apply(self.filter_dict[self.filter_in_use.get()]))
        apply_filter_button.grid(row=1, column=1)
        
        # Drop down for filter selection
        self.filter_dict = {"polar": PolarizeFilter(),
                            "whiten": WhitenFilter()}
        self.filter_name_list = sorted(list(self.filter_dict.keys()))
        self.filter_in_use = tk.StringVar(self.window)
        self.filter_in_use.set(self.filter_name_list[0]) # default value
        dd = tk.OptionMenu(self.window, self.filter_in_use,
                           *(self.filter_name_list))
        dd.grid(row=2, column=0, columnspan=3)
        
        # Saving
        save_button = tk.Button(text="Save", bg="white",
                                command=lambda:self.save(self.out_img))
        save_button.grid(row=3, column=0, columnspan=3)
        
        # Start main loop
        self.window.mainloop()
        
        
    def apply(self, img_filter):
        """
        Apply filter to self.orig_img, set and display self.out_img
        img_filter: the filter to be applied, an instance of filters.ImageFilter
        """
        #TODO: ensure value between 0 and 255
        self.out_img = img_filter.apply(self.orig_img)
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
        save_display.grid(row=4, column=0, columnspan=3)
        save_display.insert(tk.END, save_message)
        
        
def run():
    """
    Create a window and pass it to the Application object
    """
    App(tk.Tk(), "ZZ Image Filter")
        