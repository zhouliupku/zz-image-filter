# -*- coding: utf-8 -*-
"""
Created on Sun May 12 18:29:21 2019

@author: Zhen
"""

import math
import numpy as np

#TODO: move to config
MID = 127.5

def safe_pow(x, y):
    return np.sign(x) * (abs(x) ** y)

polarize_filter = np.vectorize(lambda x: int(round(MID*(1+safe_pow(x/MID-1, 0.5)), 0)))