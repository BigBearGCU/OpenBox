#!/usr/bin/env python

##@file
##@namespace xsprite
# This module contains the common sprite operations
import os, sys

import pygame
from pygame.locals import *

from xutils import *
from xvec2d import XVec2d
from ximage import XImage

updateTime = 50  # Number of millisenconds per frame

## class XSprite<br>
# This handles the drawing, copying and other operations that are common to a
# a sprite
# <br>
# <br>
# <b>Note: An XButton x,y coordinates start at it's top left corner</b>
class XSprite(XImage):
	
	##XSprite Constructor<br>
	# @param self The object pointer
	# @param element The XElement that descibes the XSprite
	def __init__(self, element=None):
		XImage.__init__(self, element) #call Sprite initializer
		self.velocity = XVec2d(0,0)
	
	##Do Copy<br>
	# Carry out a copy opertion on an XSprite
	# @param self The object pointer
	# @param to_cpy The XSprite to copy
	def do_copy(self, to_cpy):
		XImage.do_copy(self, to_cpy)
		self.hitmask = get_colorkey_and_alpha_hitmask(self.image, self.rect)

	## Copy<br>
	# Copies this XSprite to a new one
	# @param self The object pointer
	# @returns a XSprite which is a copy of this one(the calling object)
	def copy(self):
		cpy = XSprite()
		cpy.do_copy(self)
		return cpy
	
	## Set Image<br>
	# Sets the current Image of the the XSprite, is can be a whole image or part
	# of an image for sprite animation
	# @param self The object pointer
	# @param frames The number of animation frames
	# @param size The size of the image to be displayed, if None it will be calculated
	# @param loop Is the animation of image to be looped
	# @param duration The duration of the animation
	# @param anim Specfies if the image is to be animated
	def set_image(self, img, frames=1, size=None, loop=True, duration=None, anim=True):
		XImage.set_image(self, img, frames, size, loop, duration, anim)
		self.hitmask = get_colorkey_and_alpha_hitmask(self.image, self.rect)
		
	##Set Velocity<br>
	# Sets the current velocity of the sprite
	# @param x The x velocity
	# @param y The y velocity
	def set_velocity(self, x, y):
		self.velocity.set(x, y)
		
	def move(self,change):
		self.rect.topleft=(self.rect.topleft[0]+change[0],self.rect.topleft[1]+change[1])

        
#--------------------------------------------------------------------
