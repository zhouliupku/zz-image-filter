# -*- coding: utf-8 -*-
"""
Created on Sun May 12 15:19:11 2019

@author: Zhen
"""

import tkinter as tk
from tkinter import filedialog as FD
from tkinter import messagebox as MSG
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
        self.img_path = os.path.join(root_path, "resources", "image")
        
        # Initialize app window
        self.window = window
        self.window.title(window_title)
        self.window.geometry(AGC.WINDOW_SIZE)
        for col in [AGC.COL_ORIG_CONTENT, AGC.COL_OUT_CONTENT]:
            self.window.grid_columnconfigure(col, minsize=AGC.DROPDOWN_WIDTH)
        for col in [AGC.COL_ORIG_BUTTON, AGC.COL_OUT_BUTTON]:
            self.window.grid_columnconfigure(col, minsize=AGC.BUTTON_WIDTH)
        self.window.wm_iconbitmap(os.path.join(self.img_path, "zz.ico"))
        
        # Title and subtitle
        title = tk.Label(text="Filter Project", font=AFC.TITLE_FONT)
        title.grid(row=AGC.ROW_TITLE,
                   column=AGC.COL_LEFTMOST,
                   columnspan=AGC.ALL_COLUMNS)
        subtitle = tk.Label(text="Designed by zz", font=AFC.SUBTITLE_FONT)
        subtitle.grid(row=AGC.ROW_SUBTITLE,
                      column=AGC.COL_LEFTMOST,
                      columnspan=AGC.ALL_COLUMNS)

        # Load default original image to start with
        default_image = os.path.join(self.img_path, "orig", "pku.jpg")
        self.input_filename = default_image
        self.orig_img = cv2.imread(self.input_filename, cv2.IMREAD_GRAYSCALE)
        self.out_img = self.orig_img
        print(self.orig_img)
        
        # Show original image
        self.orig_canvas = tk.Canvas(window,
                                     width=AGC.IMAGE_WIDTH,
                                     height=AGC.IMAGE_HEIGHT)
        self.orig_canvas.grid(row=AGC.ROW_IMAGE,
                              column=AGC.COL_ORIG_CONTENT,
                              columnspan=AGC.HALF_COLUMNS)
        self.orig_photo = ImageTk.PhotoImage(master=self.orig_canvas,
                                             image=Image.fromarray(self.orig_img).resize((AGC.IMAGE_WIDTH,
                                                                 AGC.IMAGE_HEIGHT)))
        self.orig_img_on_canvas = self.orig_canvas.create_image(0, 0, 
                                      image=self.orig_photo,
                                      anchor=tk.NW)
        
        # Show output image, initialized as a copy of original image
        self.out_canvas = tk.Canvas(window,
                                    width=AGC.IMAGE_WIDTH,
                                    height=AGC.IMAGE_HEIGHT)
        self.out_canvas.grid(row=AGC.ROW_IMAGE,
                             column=AGC.COL_OUT_CONTENT,
                             columnspan=AGC.HALF_COLUMNS)
        self.out_photo = ImageTk.PhotoImage(master=self.out_canvas,
                                            image=Image.fromarray(self.out_img).resize((AGC.IMAGE_WIDTH,
                                                                 AGC.IMAGE_HEIGHT)))
        self.out_img_on_canvas = self.out_canvas.create_image(0, 0, 
                                          image=self.out_photo,
                                          anchor=tk.NW)
        
        # Loading and saving
        self.load_label = tk.Label(text=self.input_filename, font=AFC.TEXT_FONT)
        self.load_label.grid(row=AGC.ROW_MENU_1,
                             column=AGC.COL_LEFTMOST)
        load_button = tk.Button(text="Load", bg="white",
                                command=lambda:self.load())
        load_button.grid(row=AGC.ROW_MENU_1,
                         column=AGC.COL_ORIG_BUTTON)
        self.save_label = tk.Label(text="", font=AFC.TEXT_FONT)
        self.save_label.grid(row=AGC.ROW_MENU_2,
                             column=AGC.COL_LEFTMOST)
        save_button = tk.Button(text="Save", bg="white",
                                command=lambda:self.save(self.out_img))
        save_button.grid(row=AGC.ROW_MENU_2,
                         column=AGC.COL_ORIG_BUTTON)
        
        # Filter selection and apply
        self.filter_name_list = sorted(list(filters.filter_dict.keys()))
        self.filter_in_use = tk.StringVar(self.window)
        self.filter_in_use.set(self.filter_name_list[0]) # default value
        dropdown_filter = tk.OptionMenu(self.window, self.filter_in_use,
                                        *(self.filter_name_list))
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
        self.update_all_image()
        self.save_label.config(text="Changes are not saved yet!")
        
        
    def load(self):
        """
        Load from customized path and set self.input_filename
        """
        filename = FD.askopenfilename(initialdir=os.path.join(self.img_path, "orig"),
                                     title="Load",
                                     filetypes=(("jpeg files","*.jpg"),
                                                  ("png files","*.png"),
                                                  ("all files","*.*")))
        if filename == "":      # on cancel
            return
        self.input_filename = filename
        self.load_label.config(text=self.input_filename)
        self.orig_img = cv2.imread(self.input_filename, cv2.IMREAD_GRAYSCALE)
        self.out_img = self.orig_img
        self.update_all_image()
        
    
    def save(self, image):
        """
        img: image to be saved, represented as numpy array
        Save image to specific path 
        """
        filename =  FD.asksaveasfilename(initialdir=os.path.join(self.img_path, "out"),
                                         title="Save",
                                         defaultextension=".png",
                                         filetypes=(("jpeg files","*.jpg"),
                                                      ("png files","*.png"),
                                                      ("all files","*.*")))
        if filename == "":      # on cancel
            return
        try:
            cv2.imwrite(filename, image)
            self.save_label.config(text=filename)
        except:
            MSG.showwarning("Save", "Failed to save changes to {}".format(filename))
            
            
    def update_all_image(self):
        """
        Update image for both input and output canvas
        """
        self.orig_photo = ImageTk.PhotoImage(master=self.orig_canvas,
                                            image=Image.fromarray(self.orig_img).resize((AGC.IMAGE_WIDTH,
                                                                 AGC.IMAGE_HEIGHT)))
        self.orig_canvas.itemconfig(self.orig_img_on_canvas, image = self.orig_photo)
        self.out_photo = ImageTk.PhotoImage(master=self.out_canvas,
                                            image=Image.fromarray(self.out_img).resize((AGC.IMAGE_WIDTH,
                                                                 AGC.IMAGE_HEIGHT)))
        self.out_canvas.itemconfig(self.out_img_on_canvas, image = self.out_photo)
        
        
def run():
    """
    Create a window and pass it to the Application object
    """
    App(tk.Tk(), "ZZ Image Filter")
        