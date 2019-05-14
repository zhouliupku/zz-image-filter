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
        return np.clip(np.vectorize(self.apply_pointwise)(image), 0, 255)
        
    
    def apply_pointwise(self, x):
        """
        Given x, the value for a certain pixel, apply some filtering logic
        """
        raise NotImplementedError
        
        
class PolarizeFilter(PointFilter):
    def apply_pointwise(self, x):
        return int(round(MID * (1 + safe_pow(x / MID - 1, 0.5)), 0))
    
    
class WhitenFilter(PointFilter):
    def apply_pointwise(self, x):
        return x + 77
    