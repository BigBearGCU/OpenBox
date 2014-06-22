#!/usr/bin/env python

## @namespace cbutton
#
# Holds extension of the standard button used in the iDore system
import os, sys

import pygame
from pygame.locals import *

from xsprite import XSprite
from xbutton import XButton
from xxml import *

xbuttonStart = 0
xbuttonIdle = 1
xbuttonCharge = 2
xbuttonFire = 3
xbuttonFired = 4

## CButton class<br>
# A button that is fired when charged.
# @deprecated Use XButton instead
class CButton(XButton):
    
    ## CButton constructor<br>
    # @param self The object pointer
    # @param element The XElement that describes this button
    def __init__(self, element=None):
        XButton.__init__(self, element)
	
    ## Updates the state of the button
    # This function updates the state of button which also advance the button
    # animation
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
        elif self.state == xbuttonFire and self.ximage.frame == self.ximage.frames -1:
            print "Button fired!!!", self.id
            self.set_state(xbuttonFired)

        else:
            self.ximage.update(elapsedTime)

        ## Need to make sure image attribute is set correctly for pygame.sprite drawing
        self.image = self.ximage.image
        self.tickled = False

#--------------------------------------------------------------------