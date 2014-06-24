#!/usr/bin/env python

##@file
##@namespace xtest
# This module contains the common operations for 
# drawing text to the screen
import os, sys,platform

import pygame
from pygame.locals import *

from xutils import parse_colour
     
##class XFontManager<br>
# Handles the creation and the retrieval of fonts to enable
# the drawing of text
class XFontManager:
	
	##XFont Manager Constructor<br>
	#@param self The object pointer
    def __init__(self):

        self.defaultFont = None
        if pygame.font:
            self.defaultFont = pygame.font.Font(None, 36)
        else:
            print "XText.__init__: Fonts disabled"
    
        self.fonts = {}
		
	## Get the specfied font<br>
	# This retrieves the specfied font, if none is passed in
	# then the default font is returned
	# @param self The object pointer
	# @param name The name of font required
	# @returns The specfied font, or default if sepecfied font is not
	# avaible
    def get_font(self, name=None):
        font = self.defaultFont
        if name:
            try:
                font = self.fonts[name]
            except:
                font = self.defaultFont
        return font
    
	## Create Font from file<br>
	# Creates a font from a true type font file, this will add it to
	# the loaded font dictonary for later retrieval
	# @param self The object pointer
	# @param name The name of the font to be loaded
	# @param filename The filename where the font is stored
	# @param size The font size of the loaded font
	# @returns font The loaded font 
    def create_font_from_file(self, name, filename, size):
        font = pygame.font.Font(filename, size)
        self.fonts[name] = font
        return font
    
	## Create font from a system font<br>
	# This creates a font that is stored in the operting system, this will
	# add the font to the dictonary
	# @param self The object pointer
	# @param name The name of the font
	# @param size The size of the font to be loaded
	# @param bold Boolean to specfiy if the font is to be bold
	# @param italic Italic to specfiy if the font is to be italic
	# @returns font The loaded font
    def create_font_from_sys(self, name, sys, size, bold, italic):
        font = pygame.font.SysFont(sys, size, bold, italic)
        self.fonts[name] = font
        return font
    
	## Creates a font from an XElement<br>
	# This retrieves all necessary values from an XElement(loaded from XML)
	# to create a font
	# @param self The object pointer
	# @param element The XElement that descibes the font
	# @returns font The loaded font
    def create_font_from_element(self, element):
        filename = element.get_attr_string("filename")
        if filename:
            return self.create_font_from_file(element.get_attr_string("name"), element.get_attr_string("filename"),
                element.get_attr_int("size"))
        else:
            return self.create_font_from_sys(element.get_attr_string("name"), element.get_attr_string("sys"), element.get_attr_int("size"),
                element.get_attr_bool("bold"), element.get_attr_bool("italic"))


## Class XText<br>
# This class handles the most common task of display test on the screen to the user
class XText(pygame.sprite.Sprite):
	## XText Constructor<br>
	# @param self The object pointer
	# @param manager The font manager used to retrieve and load fonts
	# @param element The XElement that describes the XText we are going to display
    def __init__(self, manager, element):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        
        self.id = element.get_attr_string('id', 'id')
        self.font = manager.get_font(element.get_attr_string("font"))
        value = element.get_attr_string("value", "")
        fg = element.get_attr_string("fgcolor", "")
        bg = element.get_attr_string("bgcolor", "")

        if fg:
            self.fg = parse_colour(fg)
        else:
            self.fg = (0,0,0)
        
        if bg:
            self.bg = parse_colour(bg)
        else:
            self.bg = None
            
        #print "Colour", self.fg, self.bg
            
        x = element.get_attr_int('x')
        y = element.get_attr_int('y')
        self.pos = (x, y)
        align = element.get_attr_string("align")
        self.set_value(value, align)
    
	##Set Position<br>
	# Set the position of the Text on the screen. Please note that the position of 
	# the text is the top left of the sprite
	# @param self The object pointer
	# @param pos The x and y position of the text
    def set_pos(self, pos):
        self.rect.topleft = pos
    
	## Set Foreground colour<br>
	# Set the foreground colour of the Text, this will be the colour of the
	# actual text displayed to the user
	# @param self The object pointer
	# @param fg The r,g,b colour of the text
    def set_fg(self, fg):
        self.fg = fg
        self.set_value(self.value)
    
	## Set background colour<br>
	# Set the background colour of the Text, this will be the colour of the
	# background of the text
	# @param self The object pointer
	# @param bg The r,g,b colour of the background
    def set_bg(self, bg):
        self.bg = bg
        self.set_value(self.value)
    
	## Set Value<br>
	# Sets the string of the text to be displayed on the screen
	# @param self The object pointer
	# @param value The string to displayed
	# @param align The alignement of the text can be 
	# c- centre
	# l - left
	# r - right
    def set_value(self, value, align="c"):
        self.value = value
        size = self.font.size(self.value)
        if self.bg:
            self.image = self.font.render(self.value, True, self.fg, self.bg)
        else:
            self.image = self.font.render(self.value, True, self.fg)
        
        if align == "l":    ## Left
            self.rect = Rect(self.pos, size)
        elif align == "r":  ## Right
            pos = (self.pos[0] - size[0], self.pos[1])
            self.rect = Rect(pos, size)
        else:               ## Center
            pos = (self.pos[0] - size[0]/2, self.pos[1])
            self.rect = Rect(pos, size)
            
    
#--------------------------------------------------------------------
