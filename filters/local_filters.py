# -*- coding: utf-8 -*-
"""
Created on Sun May 12 18:37:02 2019

@author: Zhen
"""

import numpy as np
from scipy.signal import convolve2d as cvv
from .image_filter import ImageFilter


class LocalFilter(ImageFilter):
    """
    Convolutional filters that leverage local features
    """
    def __init__(self):
        self.discription = "Local filter base class"
        self.kernel = np.array([[1]])       # Identical kernel
        
        
    def apply(self, image):
        """
        Apply kernel on the image and clip the value within 0 and 255
        """
        return np.clip(cvv(image, self.kernel, mode="same"), 0, 255)
        
        
class AverageBlurFilter(LocalFilter):
    def __init__(self):
        self.discription = "Blur 5*5"
        self.kernel = np.array([[0.04] * 5] * 5)
    