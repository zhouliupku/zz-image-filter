# -*- coding: utf-8 -*-
"""
Created on Sun May 12 15:19:11 2019

@author: Zhen
"""

import tkinter as tk
import cv2
import os
from PIL import Image, ImageTk

from .common.config import AppFontConfig as AFC
from .common.config import AppGridConfig as AGC
from . import filters

class App:
    def __init__(self, window, window_title):
        """
        Initialize app window and start main loop
        """
        root_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(root_path, "resources", "image")
        
        # Initialize app window
        self.window = window
        self.window.title(window_title)
        self.window.geometry(AGC.WINDOW_SIZE)
        for col in [AGC.COL_ORIG_CONTENT, AGC.COL_OUT_CONTENT]:
            self.window.grid_columnconfigure(col, minsize=AGC.DROPDOWN_WIDTH)
        for col in [AGC.COL_ORIG_BUTTON, AGC.COL_OUT_BUTTON]:
            self.window.grid_columnconfigure(col, minsize=AGC.BUTTON_WIDTH)
        self.window.wm_iconbitmap(os.path.join(img_path, "zz.ico"))
        
        # Title and subtitle
        title = tk.Label(text="Filter Project", font=AFC.TITLE_FONT)
        title.grid(row=AGC.ROW_TITLE,
                   column=AGC.COL_LEFTMOST,
                   columnspan=AGC.ALL_COLUMNS)
        subtitle = tk.Label(text="Designed by zz", font=AFC.SUBTITLE_FONT)
        subtitle.grid(row=AGC.ROW_SUBTITLE,
                      column=AGC.COL_LEFTMOST,
                      columnspan=AGC.ALL_COLUMNS)

        # Load original image
        #TODO: add load functionality
        filename = "pku.jpg"
        self.orig_img = cv2.imread(os.path.join(img_path, "orig", filename),
                                   cv2.IMREAD_GRAYSCALE)
        self.out_img = self.orig_img
        print(self.orig_img)
        
        # Show original image
        #TODO: support resizing
        height, width = self.orig_img.shape
        self.orig_canvas = tk.Canvas(window, width=width, height=height)
        self.orig_canvas.grid(row=AGC.ROW_IMAGE,
                              column=AGC.COL_ORIG_CONTENT,
                              columnspan=AGC.HALF_COLUMNS)
        self.orig_photo = ImageTk.PhotoImage(master=self.orig_canvas,
                                             image=Image.fromarray(self.orig_img))
        self.orig_canvas.create_image(0, 0, 
                                      image=self.orig_photo,
                                      anchor=tk.NW)
        
        # Show output image, initialized as a copy of original image
        self.out_canvas = tk.Canvas(window, width=width, height=height)
        self.out_canvas.grid(row=AGC.ROW_IMAGE,
                             column=AGC.COL_OUT_CONTENT,
                             columnspan=AGC.HALF_COLUMNS)
        self.out_photo = ImageTk.PhotoImage(master=self.out_canvas,
                                            image=Image.fromarray(self.out_img))
        self.out_img_on_canvas = self.out_canvas.create_image(0, 0, 
                                          image=self.out_photo,
                                          anchor=tk.NW)
        
        # Loading and saving
        load_button = tk.Button(text="Load", bg="white")
#                                command=lambda:self.save(self.out_img, filename))
        load_button.grid(row=AGC.ROW_MENU_1,
                         column=AGC.COL_ORIG_BUTTON)
        save_button = tk.Button(text="Save", bg="white",
                                command=lambda:self.save(self.out_img, filename))
        save_button.grid(row=AGC.ROW_MENU_2,
                         column=AGC.COL_ORIG_BUTTON)
        
        # Filter selection and apply
        self.filter_name_list = sorted(list(filters.filter_dict.keys()))
        self.filter_in_use = tk.StringVar(self.window)
        self.filter_in_use.set(self.filter_name_list[0]) # default value
        dropdown_filter = tk.OptionMenu(self.window, self.filter_in_use,
                                        *(self.filter_name_list))
#        dropdown_filter.config(width=20)
        dropdown_filter.grid(row=AGC.ROW_MENU_1,
                             column=AGC.COL_OUT_CONTENT,
                             sticky="ew")
        apply_filter_button = tk.Button(text="Apply", bg="white",
                                        command=lambda:self.apply(filters.filter_dict[self.filter_in_use.get()]))
        apply_filter_button.grid(row=AGC.ROW_MENU_1,
                                 column=AGC.COL_OUT_BUTTON)
        
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
        
        
    def save(self, img, orig_filename):
        """
        img: image to be saved, represented as numpy array
        orig_filename: iroginal filename
        Save image to specific path (currently static defined)
        """
        filename = "modified_" + orig_filename
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
        save_display.grid(row=AGC.ROW_NOTICE,
                          column=AGC.COL_LEFTMOST,
                          columnspan=AGC.ALL_COLUMNS)
        save_display.insert(tk.END, save_message)
        
        
def run():
    """
    Create a window and pass it to the Application object
    """
    App(tk.Tk(), "ZZ Image Filter")
        