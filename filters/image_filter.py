# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:11:47 2019

@author: Zhen
"""

class ImageFilter(object):
    """
    Base class of image filters
    """
    def __init__(self):
        self.discription = "Image Filter Base Class"
        
    def apply(self, image):
        """
        Apply filter to a given image
        """
        raise NotImplementedError
        
    def __repr__(self):
        return self.discription
        
    def __str__(self):
        return self.discription