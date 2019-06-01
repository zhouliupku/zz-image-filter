# -*- coding: utf-8 -*-
"""
Created on Sun May 12 18:29:06 2019

@author: Zhen
"""

from . import point_filters, local_filters

filter_dict = {"polar": point_filters.PolarizeFilter(),
               "whiten": point_filters.WhitenFilter(),
               "normalize": point_filters.NormalizeFilter(),
               "blur": local_filters.AverageBlurFilter()}