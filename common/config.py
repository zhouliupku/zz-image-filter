# -*- coding: utf-8 -*-
"""
Created on Sun May 12 16:47:24 2019

@author: Zhen
"""

class AppFontConfig(object):
    TITLE_FONT = ("Times New Roman", 20)
    SUBTITLE_FONT = ("Times New Roman", 12)
    TEXT_FONT = ("Times New Roman", 10)


class AppGridConfig(object):
    """
    For GUI grids only
    """
    WINDOW_SIZE = "1000x600"
    DROPDOWN_WIDTH = 420
    BUTTON_WIDTH = 80
    
    ROW_TITLE = 0
    ROW_SUBTITLE = 1
    ROW_IMAGE = 2
    ROW_MENU_1 = 3
    ROW_MENU_2 = 4
    ROW_MENU_3 = 5
    ROW_NOTICE = 6
    
    COL_ORIG_CONTENT = 0
    COL_ORIG_BUTTON = 1
    COL_OUT_CONTENT = 2
    COL_OUT_BUTTON = 3
    
    COL_LEFTMOST = 0
    ALL_COLUMNS = 4
    HALF_COLUMNS = 2