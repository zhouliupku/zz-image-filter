# -*- coding: utf-8 -*-
"""
Created on Sun May 12 18:29:21 2019

@author: Zhen
"""

import math
import numpy as np

from .image_filter import ImageFilter

#TODO: move to config
MID = 127.5
NORM_STD = 50


def safe_pow(x, y):
    return np.sign(x) * (abs(x) ** y)


class PointFilter(ImageFilter):
    """
    Point-wise filters
    """
    def __init__(self):
        self.discription = "Pointwise filter base class"
        
        
    def apply(self, image):
        """
        Call apply_pointwise for each pixel of image and clip the value
        within 0 and 255
        """
        self.extract_feature(image)
        return np.clip(np.vectorize(self.apply_pointwise)(image), 0, 255)
        
    
    def apply_pointwise(self, x):
        """
        Given x, the value for a certain pixel, apply some filtering logic
        """
        raise NotImplementedError
        
    def extract_feature(self, image):
        """
        Place holder for feature extraction before apply
        """
        
        
class PolarizeFilter(PointFilter):
    def __init__(self):
        self.discription = "Polarize image to enhance contraction"
        
        
    def apply_pointwise(self, x):
        return int(round(MID * (1 + safe_pow(x / MID - 1, 0.5)), 0))
    
    
class WhitenFilter(PointFilter):
    def __init__(self):
        self.discription = "Increase brightness of image"
        
        
    def apply_pointwise(self, x):
        return x + 77
    
    
class NormalizeFilter(PointFilter):
    """
    An example of previously-called global filter
    """
    def __init__(self):
        self.discription = "Normalize image brightness"
        
        
    def apply_pointwise(self, x):
        return MID + NORM_STD * (x - self.mean) / self.std
        
        
    def extract_feature(self, image):
        self.mean = image.mean()
        self.std = image.std()