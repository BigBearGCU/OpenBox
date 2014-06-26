#!/usr/bin/env python

##@file

##@namespace xframework
# All system wide resources are managed in this package 
import os, sys,platform
from datetime import datetime

import pygame
from pygame.locals import *

from xwebcam import XWebcam
from xtext import XFontManager
from xutils import set_missing_image

gFramework = None

## Retrieves the global XFramework object<br>
# This function can be used to retrieve the XFramework object 
# and all resources managed by that object
def get_framework():
    global gFramework
    if gFramework == None:
        gFramework = XFramework()
        log_message("Started execution")
    return gFramework

## Delete the global XFramework object<br>
# This function deletes the flobal XFramework object and all
# resources managed by it
# <br>
# <br>
# <b>NB. That if this function is called mid game or application then the 
# iDore application will crash
def del_framework():
    global gFramework
    if gFramework.webcam and gFramework.webcam.is_active():
        gFramework.webcam.stop()
        log_message("Stopped execution")
        del gFramework
    gFramework = None
    exit()
    

## Log messages to the screen and a log file<br>
# This functions logs the message passed in to a log file 
# and to the standard terminal output
# @param msg The message to log
def log_message(msg):
    gFramework.log_message(msg)    

## Displays an error message to the screen<br>
# This function passes information to the XFramework to 
# display a standard error screen to the user
# @param msg The Message to display
# @param exception The Exception that has been raised by the application
# @param detail The Detail error message present to be displayed
def error_message(msg, exception=None, detail=None):
    gFramework.error_message(msg, exception, detail)

## XFramework class<br>
# Class to own the common resources across instantiations of XGame
# Copes with display or webcam being instantiated in any order
class XFramework:
    
    ## XFramework Constructor<br>
    # Sets all neccessary paths, for saving and loading 
    def __init__(self):
		print "XFramework.__init__"
				
		self.gcalpath = os.getenv("GCALPYTHONPATH")
		self.savepath = os.path.join(self.gcalpath, "save")
		self.appspath = os.path.join(self.gcalpath, "apps")
		self.assetpath = os.path.join(self.gcalpath, "apps", "assets")
		
		logfileName = os.path.join(self.savepath, "log.txt")
		self.logfile = open(logfileName, 'a')
		
		pygame.init()
		pygame.mouse.set_visible(False)
		self.fontManager = XFontManager()
		self.webcam = None
		self.displaySurface = None
				
		set_missing_image(os.path.join(self.assetpath, "image-missing.png"))
		#self.gameList=GameList(os.path.join(self.savepath,"games.xml"))
    
    ## Logs a message to the log file and the terminal window<br>
    # Logs a meesage to a log file and also sends the message to 
    # the standard output stream
    # @param self The object pointer
    # @param msg The message to log
    def log_message(self, msg):
        now = datetime.now()
        self.logfile.write(now.strftime("%d-%m-%y %H:%M:%S") + ": " + msg + "\n")
        print now.strftime("%d-%m-%y %H:%M:%S") + ": " + msg
	
    ## Displays an Error Screen to the user<br>
    # This function creates a standard error screen and then displays it
    # to the user. It will also send the message to the log function
    # @param self The object pointer
    # @param msg The message to be display
    # @param exception The exception that has been raised by the
    # application
    # @param detail The detailed error message to be displayed
    def error_message(self, msg, exception=None, detail=None):
        white = (255, 255, 255)
        blue = (0, 0, 255)
        font = self.fontManager.get_font()
        msgImage = font.render(msg, True, blue, white)
        exceptionImage = font.render(repr(exception), True, blue, white)
        detailImage = font.render(repr(detail), True, blue, white)
        log_message("Error:" + msg)
        log_message("Exception:" + repr(exception))
        log_message("Detail:" + repr(detail))
        
        while 1:
            for event in pygame.event.get():                
                if event.type == QUIT:
                    return                
                elif event.type == KEYUP:
                    return
            self.displaySurface.fill(white)
            self.displaySurface.blit(msgImage, (50, 100))
            self.displaySurface.blit(exceptionImage, (50, 150))
            self.displaySurface.blit(detailImage, (50, 200))
            pygame.display.update()
    
    ## Retrieves the font manager from the XFramework object<br>
    # @param self The object pointer
    def get_font_manager(self):
        return self.fontManager
    
    ## Retrieves the webcam<br>
    # If the webcam has been initailised allow it to be retrieved, if not
    # then create the webcam and pass it back to the caller
    # @param self The object pointer
    def get_webcam(self):
        if self.webcam == None:
            self.webcam = XWebcam()
            if self.displaySurface:
                self.webcam.set_screen_size(self.displaySurface.get_size())
        return self.webcam
	    
    ## Set the screen<br>
    # This function creates a screen that we can draw on
    # @param self The object pointer
    # @param size The size of the screen to create
    # @param flags The creation flags of the screen
    # @returns displaySurface A surface that we can render to
    def set_display_surface(self, size, flags):
        assert self.displaySurface == None
        self.displaySurface = pygame.display.set_mode(size, flags)
        if self.webcam:
            self.webcam.set_screen_size(self.displaySurface.get_size())
        #pygame.mouse.set_visible(0)
        return self.displaySurface
	
	## Get the screen
	# Returns the surface that we are goign to draw on
	# @returns displaySurface A surface that we can draw on 
    def get_display_surface(self):
        return self.displaySurface
	 
	## Deletes the allocated memory for this class
	# This deletes all persistant resource attached to the 
	# XFramework object
	# @param self The object pointer
    def __del__(self):
        del self.webcam
        del self.fontManager
        self.logfile.close()
        print "XFramework.__del__"
        sys.exit(0)
