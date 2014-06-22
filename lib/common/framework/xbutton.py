#!/usr/bin/env python

## @file

## @namespace xbutton
#
# A standard button in the iDore system

import os, sys

import pygame
from pygame.locals import *

from xutils import image_load
from ximage import XImage

## State<br>
# The state of the XButton, it can be one of 5 values
# @code
# xbuttonStart = 0
# xbuttonIdle = 1
# xbuttonCharge = 2
# xbuttonFire = 3
# xbuttonFired = 4
# @endcode
xbuttonStart = 0
xbuttonIdle = 1
xbuttonCharge = 2
xbuttonFire = 3
xbuttonFired = 4

## class XButton<br>
# An XButton is the main user interface element of the iDore system, 
# it has several states which control how the button is animated.
# <br>
# <br>
# <b>Note: An XButton x,y coordinates start at it's top left corner</b>
class XButton(pygame.sprite.Sprite):
    
    ##
    # XButton Constructor<br>
    # @param self The object pointer
    # @param element The XElement that describes this buttons properties
    def __init__(self, element=None):
        pygame.sprite.Sprite.__init__(self)
        
        self.tickled = False
        self.handler = None        
        
        if element:
            self.set_element(element)
	    
    ## Sets the XElement of XButton<br>
    # This sets the XElement and then retrieves the various properties from
    # the XElement such as id, x and y position, width and height
    # @param self The object pointer
    # @param element The XElement that describes the XButton's properties 
    def set_element(self, element):

        self.id = element.get_attr_string('id', 'id')
        x = element.get_attr_int('x')
        y = element.get_attr_int('y')
        width = element.get_attr_int('width')
        height = element.get_attr_int('height')
        self.rect = Rect(0, 0, width, height)
        self.rect.topleft = (x, y)

        start = None
        idle = None
        charge = None
        fire = None
        for e in element.elements:
            if e.get_attr_string('id') == "start":
                start = self.load(e, False)
            elif e.get_attr_string('id') == "idle":
                idle = self.load(e, True)
            elif e.get_attr_string('id') == "charge":
                charge = self.load(e, False)
            elif e.get_attr_string('id') == "fire":
                fire = self.load(e, False)
                
        assert(start and idle and charge and fire)
        self.ximages = (start, idle, charge, fire)
        self.set_state(xbuttonStart)
        #fix by Brian McDonald, base class image is not set this causes a crash when
        #we try to move to a new screen using buttons.
        #This sets the base classes image to the start image of button
        self.image=start.image
	
    ## Carries out a copy operation on a XButton<br>
    # This copies a XButton to this XButton
    # @param self The object pointer
    # @param to_cpy The Button we are going to copy 
    def do_copy(self, to_cpy):
        self.id = to_cpy.id
        self.handler = to_cpy.handler
        self.rect = Rect(to_cpy.rect)
        self.ximages = []
        for image in to_cpy.ximages:
            self.ximages.append(image.copy())
        self.set_state(xbuttonStart)       
	 
    ## Copies a XButton<br>
    # This returns a copy of the current XButton
    # @param self The object pointer
    # @returns XButton which is a copy of the current button
    def copy(self):
        cpy = XButton()
        cpy.do_copy(self)
        return cpy
    
    ## Load the XButton properties from an XElement<br>
    # This loads a XButton from an XElement and the loads 
    # the image specfied in the XElement.
    # @param self The object pointer
    # @param element The XElement that holds the XButtons properties
    # @param loop Specfies if we are to loop the button animation
    # @returns XImage the image that describes the current state
    # of the XButton after loading
    def load(self, element, loop):
        img, rect = image_load(element.get_attr_string('src'), -1)
        frames = element.get_attr_int('frames', 1)
        if self.rect.width == 0 or self.rect.height == 0:
            self.rect.width = rect.width
            self.rect.height = rect.height / frames
        ximage = XImage()
        ximage.set_image(img, frames, self.rect.size, loop)
        ximage.set_pos(self.rect.topleft)
        return ximage
	
    ## Sets the position of the XButton<br>
    # This sets the x and y position of the XButton
    # @param self The object pointer
    # @param pos The new position of the button 
    def set_pos(self, pos):
        self.rect.topleft = pos
        for image in self.ximages:
            image.set_pos(pos)
    
    ## Sets the new state of the XButton<br>
    # Sets the new state of XButton
    # @param self The object pointer
    # @param state The new state of the button
    def set_state(self, state):
        assert(state >=0 and state <= xbuttonFired)
        self.state = state
        self.tickled = True
        if state < xbuttonFired:
            assert(self.ximages[state])
            self.ximage = self.ximages[state]
            self.ximage.set_frame(0)
        if self.handler:
            self.handler(self, self.state)
    
    ## Sets the function which will handle XButton messages<br>
    # This will set what function will be used to handle the user
    # interaction with the button. This handler function will be 
    # called when the state of the button changes
    # @param handler The function that will handle button interactions
    def set_handler(self, handler):
        self.handler = handler
    
    ## Called when the user interacts with a button
    # This function is called when movement is detected within a XButton,
    # it then sets the state of the XButton to charged and indicates that
    # the XButton has been selected.
    # @param elapsedTime The elapsed time since the last game update
    def apply_motion(self, elapsedTime):
        if self.state == xbuttonIdle:
            self.set_state(xbuttonCharge)
        self.tickled = True

    ## Updates the animation and the state of the XButton
    # This function will called every game update. It has the responsibilty to
    # update animation and update state of the XButton
    # @param self The object pointer
    # @param elapsedTime The elapsed time since the last game update
    def update(self, elapsedTime):
        if self.state == xbuttonStart and self.ximage.frame == self.ximage.frames -1:
            self.set_state(xbuttonIdle)
        elif self.state == xbuttonCharge:
            if self.tickled: 
                print "Button charging...", self.id
                if not self.ximage.forward_frame(elapsedTime):
                    print "Button charged!!!", self.id
                    self.set_state(xbuttonFire)
            else:
                #print "Button un-charging...", self.id
                if not self.ximage.backward_frame(elapsedTime):
                    #print "Button un-charged", self.id
                    self.set_state(xbuttonIdle)
        elif self.state == xbuttonFire and self.ximage.frame == self.ximage.frames -1:
            #print "Button fired!!!", self.id
            self.set_state(xbuttonFired)
        else:
            self.ximage.update(elapsedTime)
            
        #Need to make sure image attribute is set correctly for pygame.sprite drawing
        self.image = self.ximage.image
        self.tickled = False

#--------------------------------------------------------------------
