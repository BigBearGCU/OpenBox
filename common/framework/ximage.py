##@file

##@namespace ximage
# Contains classes and functions for image manipulation

#!/usr/bin/env python

import os, sys

import pygame
from pygame.locals import *

from xglobals import *
from xutils import image_load


#--------------------------------------------------------------------
# Globals
gUpdateTime = 1000 / gImageFps

## class XImage
# An XImage handles the drawing of an image to the screen, it is the
# base class for all visible objects to be drawn to the screen
# <br>
# <br>
# <b>Note: An XImage x,y coordinates start at it's top left corner</b>
class XImage(pygame.sprite.Sprite):
	
	## XImage constructor<br>
	# @param self The object pointer
	# @param element The XElement that describes our image
    def __init__(self, element=None):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.id = None
        self.rect = Rect(0,0,0,0)
        self.updateTime = gUpdateTime
        if element:
            self.set_element(element)
        self.pause = False
		
	## Set Image<br>
	# Sets the current image to be displayed to the screen
	# @param self The object pointer
	# @param frames The number of animation frames
	# @param size The size of the image to be displayed, if None it will be calculated
	# @param loop Is the animation of image to be looped
	# @param duration The duration of the animation
	# @param anim Specfies if the image is to be animated
    def set_image(self, img, frames=1, size=None, loop=True, duration=None, anim=True):
        self.theImage = img
        self.image = img
        self.loop = loop
        self.anim = anim
        self.duration = duration
        if frames <= 0:
            frames = 1
        self.frames = frames
        #set Animation functions
        #if number of animation is 1 we wil have no update function
        if self.frames == 1:
            self.updateFn = None
        #else me have animation frames then
        else:
            #if animation set to loop then set update function accordingly
            if loop:
                self.updateFn = self.update_loop
            else:
                self.updateFn = self.update_once
        #size of button is none
        if size == None:
            #then calculate with images
            self.rect.size = img.get_size()
            self.rect.width = self.rect.width
            self.rect.height = self.rect.height / frames
        #else 
        else:
            #if the number frames is only 1
            if self.frames == 1:
                self.rect.size = size
                self.theImage = pygame.transform.scale(img, size)
                self.image = self.theImage
            else:
                self.rect.size = size
                self.theImage = pygame.transform.scale(img, (self.rect.width , self.rect.height* frames))
        self.frameRect = Rect((0, 0), self.rect.size)
        if self.frames > 1:
            if self.duration:
               self.updateTime = self.duration / self.frames 
            self.frame = 0
            self.elapsedTime = 0
            self.image = self.theImage.subsurface(self.frameRect)
			
	## Set XElement of the XImage<br>
	# Sets the XElement XImage, this will also retrieve all the 
	# properties of the XImage such as filename, position, animation frames,
	# etc
	# @param self The object pointer
	# @param element The XElement that descibes this XImage
    def set_element(self, element):
        self.id = element.get_attr_string('id', 'id')
        img, rect = image_load(element.get_attr_string('src'), -1)
        x = element.get_attr_int('x')
        y = element.get_attr_int('y')
        frames = element.get_attr_int('frames', 1)
        loop = element.get_attr_bool('loop', True)
        anim = element.get_attr_bool('anim', True)
        duration = element.get_attr_int('duration', None)
        width = element.get_attr_int('width')
        height = element.get_attr_int('height')
        if width == 0:
            size = None
        else:
            size = (width, height)
        self.rect.topleft = (x, y)
        self.set_image(img, frames, size, loop, duration, anim)
		
    ## Carries out a copy operation on a XImage<br>
    # This copies a XImage to this XImage
    # @param self The object pointer
    # @param to_cpy The XImage we are going to copy 	
    def do_copy(self, to_cpy):
        self.id = to_cpy.id
        self.set_image(to_cpy.theImage, to_cpy.frames, to_cpy.rect.size, to_cpy.loop, to_cpy.duration, to_cpy.anim)
	
    ## Copies a XImage<br>
    # This returns a copy of the current XImage
    # @param self The object pointer
    # @returns XImage which is a copy of the current image	
    def copy(self):
        cpy = XImage()
        cpy.do_copy(self)
        return cpy
	
	## Set Position<br>
	# Sets the new x and y position of the XImage
	# @param self The object pointer
	# @param pos The new x,y position 
    def set_pos(self, pos):
        self.rect.topleft = pos
    
	## Set Centre Position<br>
	# Sets the new x and y centre position of the XImage
	# @param self The object pointer
	# @param pos The new x,y position
    def set_pos_center(self, pos):
        self.rect.center = pos
    
	## Get Centre Position<br>
	# Retreives the centre position of the XImage
	# @todo remove pos from function argument
	# @param self The object pointer
	# @returns center The centre of the XImage
    def get_pos_center(self, pos):
        return self.rect.center
    
	## Retrieves the Position<br>
	# Returns the top left position of the XImage
	# @returns topleft The top left position of the XImage
    def get_pos(self):
        return self.rect.topleft
	
	## Retrieves the Size<br>
	# Returns the size of the XImage
	# @returns size The size of the XImage
    def get_size(self):
        return self.rect.size
    
	## Set Duration<br>
	# Sets the duration of animation, this will also calculate the 
	# update time of any animation
	# @param self The object pointer
	# @param duration The duration of the animation
    def set_duration(self, duration):
        self.duration = duration
        self.updateTime = self.duration / self.frames 
    
	## Update<br>
	# Updates the state of the XImage
	# @param self The object pointer
	# @param elapsedTime The Elapsed Time since the last update
    def update(self, elapsedTime):
        #print "Update ",self.id
        if self.anim and self.pause==False:
            if self.updateFn: self.updateFn(elapsedTime)
	
    ## Set Animation frame<br>
	# Sets the animation frame of the XImage
	# @param self The Object pointer
	# @param frame The animation frame number
    def set_frame(self, frame):
        if frame >= 0 and frame < self.frames:
            self.frame = frame
            self.frameRect.top=self.frame*self.frameRect.height
            self.image = self.theImage.subsurface(self.frameRect)
            self.elapsedTime = 0
    
	## Get Animation frame<br>
	# Retrieves the current animation frame of XImage
	# @param self The object pointer
	# @returns frame
    def get_frame(self):
        return self.frame
    
	## Update Animation in a loop<br>
	# Updates the animation state of XImage, this will loop
	# back to the start if the we reach the of the animation 
	# @param self The object pointer
	# @param elapsedTime The elapsed time since the last game update	
    def update_loop(self, elapsedTime):
        self.elapsedTime += elapsedTime
        if self.elapsedTime > self.updateTime:
            self.set_frame((self.frame + 1) % self.frames)
			
    ## Update Animation once<br>
	# Updates the animation state of XImage, this will only run
	# through the animation sequence once and will stop
	# when we reach the last frame
	# @param self The object pointer
	# @param elapsedTime The elapsed time since the last game update
    def update_once(self, elapsedTime):
        if self.frame < self.frames - 1:
            self.elapsedTime += elapsedTime
            if self.elapsedTime > self.updateTime:
                self.set_frame(self.frame + 1)
    
	## Move animation forward one frame<br>
	# Moves the animation forward one frame, will not wrap back
	# to the first frame of animation once we get to the end of
	# the animation sequence
	# @param self The object pointer
	# @param elapsedTime The elapsed time since the last game update 
    def forward_frame(self, elapsedTime):
        if self.frame == self.frames - 1:
            return False
        self.elapsedTime += elapsedTime
        if self.elapsedTime > self.updateTime:
            self.set_frame(self.frame + 1)
        return True
		
	## Move animation backwards one frame<br>
	# Moves the animation backwards one frame, will not wrap back
	# to the last frame of animation once we get to the start of
	# the animation sequence
	# @param self The object pointer
	# @param elapsedTime The elapsed time since the last game update 
    def backward_frame(self, elapsedTime):
        if self.frame == 0:
            return False
        self.elapsedTime += elapsedTime
        if self.elapsedTime > self.updateTime:
            self.set_frame(self.frame - 1)
        return True
