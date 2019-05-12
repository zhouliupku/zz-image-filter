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
        """
        Initialize app window and start main loop
        """
        self.window = window
        self.window.title(window_title)
        self.window.geometry("600x350")
        
        title = tk.Label(text="Filter Project", font=config.TITLE_FONT)
        title.grid(row=0, column=0, columnspan=3)

        apply_filter_button = tk.Button(text="Apply", bg="white")
        apply_filter_button.grid(row=1, column=1)
        
        #TODO: put into config
        root_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(root_path, "resources", "image", "orig")
        orig_img = cv2.imread(os.path.join(img_path, "pku.jpg"))
        height, width, no_channels = orig_img.shape
        
        #TODO: modularize
        orig_img_canvas = tk.Canvas(window, width=width, height=height)
        orig_img_canvas.grid(row=1, column=0)
        orig_img_photo = ImageTk.PhotoImage(master=orig_img_canvas,
                                            image=Image.fromarray(orig_img))
        orig_img_canvas.create_image(0, 0, image=orig_img_photo, anchor=tk.NW)
        
        #TODO: apply filter
        out_img = orig_img
        out_img_canvas = tk.Canvas(window, width=width, height=height)
        out_img_canvas.grid(row=1, column=2)
        out_img_photo = ImageTk.PhotoImage(master=out_img_canvas,
                                            image=Image.fromarray(out_img))
        out_img_canvas.create_image(0, 0, image=out_img_photo, anchor=tk.NW)
        
        save_button = tk.Button(text="Save", bg="white",
                                command=lambda:self.save(out_img))
        save_button.grid(row=2, column=0, columnspan=3)
        
        self.window.mainloop()
        
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
        