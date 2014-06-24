#!/usr/bin/env python

##@file
##@namespace webcam
# This module contains all the functionality to obtain an image from a
# webcam

import os, sys, Image

import pygame
from pygame.locals import *

from threading import Thread
import thread

from xglobals import *
from xutils import image_load
from xwatch import XWatchArray
#from opencv import cv
#from opencv import highgui

#--------------------------------------------------------------------
#
# Platform setup
#

if gLinux:
    if gVideo4Linux:
        from fg import Device
    else:
        from pyvideograb import directvideo
        from pyvideograb import v4l2_consts
else:
    import cv2

#--------------------------------------------------------------------
#
# Some important notes for webcam and motion detection:
#
# - "camera" variables relate to the resolution of the webcam
# - "screen" variables relate to the dimensions of final display device
# - "window" variables relate to the dimensions of the displayed webcam image
# - "view"   variables relate to the viewport onto the displayed webcam image
#
# Points from the webcam image ("camera") must be:
# - mapped to "screen" for the purposes of collision detectiontwo
# - mapped to "window" for the purposes of displaying blobs (for debuging)
#


##Class XSaveThread<br>
# A Camera thread that allows us to save the webcam image 
class XSaveThread(Thread):
	
	## XSaveThread Constructor<br>
	# @param self - The object pointer
    def __init__ (self):
        Thread.__init__(self)
        self.lock = thread.allocate_lock()
        self.sleepTime = 1000 / gSaveFps
        self.rec = None
        self.dir = None
        self.frame = 0
        self.image = None

    def __del__(self):
        if self.go: self.stop()
		
		
	## Run function<br>
	# This function is invoked when the thread is running, this will
	# actual save the webcam image every update
	# @param self The object pointer
    def run(self):
        #print "XSaveThread: dir=", self.dir
        self.go=True
        print "XSaveThread starting..." 
        while self.go:
            pygame.time.wait(self.sleepTime)
            
            if self.rec and self.image:
                filename = "frame" + repr(self.frame) + ".tga"
                fullname = os.path.join(self.dir, filename)
                pygame.image.save(self.image, fullname)
                self.frame += 1
                del self.image
                self.image = None
                
        print "XSaveThread stopped"
	
	## Stop<br>
	# This function stops the thread execution
	# @param self The object pointer
    def stop(self):
        print "XSaveThread stopping..."
        self.lock.acquire()
        self.go = False
        self.lock.release()
	
	## save images<br>
	# This sets the save image we retrieve from the web cam
	# @self The object pointer
	# @image The image we want to save
    def save_image(self, image):
        if self.lock.acquire(False):
            #self.image = image.convert(16)
			self.image=image.convert(16)
			self.lock.release()
	
    
    def set_recording(self, bool, dir=None):
  
        print "XSaveThread recording =", bool
        self.lock.acquire()
        self.rec = bool
        if bool:
            if dir and dir != self.dir:
                self.frame = 0
                self.dir = dir
            if not self.dir or not os.path.exists(self.dir):
                print "XSaveThread error: directory does not exist", self.dir
                self.rec = False
            
        self.lock.release()

## Class XWebcamThread<br>
#A Camera thread that allows us to update the state of the camera
class XWebcamThread(Thread):
    
	## XWebcamThread Constructor<br>
	#@param self The object pointer
	#@param device The webcam device object
	#@param camSize The size of the image captured from the webcam
	#@param windowSize The size of the window that the webcam image will
	# be displayed on
	#@param flip A boolean that specfies if we have to flip the webcam image
    def __init__ (self, device, camSize, windowSize, flip):
        Thread.__init__(self)

        self.device = device
        self.camWidth, self.camHeight = camSize
        self.windowSize = windowSize
        self.flip = flip
        self.lock = thread.allocate_lock()
        self.surface = None
        self.sleepTime = 1000 / gWebcamFps
        
    def __del__(self):
        if self.go: self.stop()
		
	##Run<br>
	# This function is invoked when the thread is running, this will
	# retrieve an image from a webcam device
	#@param self The object pointer
    def run(self):
        camImage1=None
        camImage2=None
        camImage3=None
        camImage4=None
        image=None
        img=None
        
        
        print "XWebcamThread starting..."
        self.go = True
        
        if gLinux and gVideo4Linux2: self.device.startcapture()

        while self.go:
            pygame.time.wait(self.sleepTime)
            if gLinux:
                if gVideo4Linux:
                    camBuffer, camWidth, camHeight = self.device.getBuffer()
                else: # Video4Linus2
                    camBuffer = self.device.getimage()
		    #do we need this? some further test will be needed
                    camBuffer = self.device.yuyv_to_rgb(camBuffer)
                    img = Image.fromstring('RGB',(camWidth,camHeight),camBuffer)
            else: # Windows + Mac
                ret,image=self.device.read()

            ## Convert buffer to a Pygame Image object
	    #very slow need some further optimisations I guess we would not need to scale the image if 
	    #match the res with the window size         
            if (image.any):
                img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                camImage1 = pygame.image.frombuffer(img,(self.camWidth,self.camHeight), 'RGB')
                if gLinux:
                    if camBuffer:
                        del camBuffer
                if img.any:
                    del img
                                                 
                ## Prepare the Image for display

                #camImage2 = camImage1.convert()
                if gLinux:
                    camImage3 = pygame.transform.flip(camImage2, True, self.flip)
                    camImage4 = pygame.transform.scale(camImage3, self.windowSize)
                else:
                    camImage2=pygame.transform.flip(camImage1,True,False)
                    camImage4=pygame.transform.scale(camImage2, self.windowSize)
                if camImage1:    
                    del camImage1
                if camImage2:
                    del camImage2
                if camImage3:
                    del camImage3

            ## Make it available for returning
                self.lock.acquire()            
                self.surface = camImage4
                self.lock.release()
            
        if gLinux and gVideo4Linux2: self.device.stopcapture()

        print "XWebcamThread stopped"
		
	##Stop<br>
	#Stops the thread running
	#@param self The object pointer
    def stop(self):
        print "XWebcamThread stopping..."
        self.lock.acquire()
        self.go = False
        self.lock.release()
		
	##Get Image<br>
	#Retrieves the image from the webcam thread
	#@param self The object pointer
	#@returns surface A pygame surface which will contain the image
	#captured from the webcam
    def get_image(self):
        surface = None
        self.lock.acquire()
        if self.surface:
            surface = self.surface
            self.surface = None
        else:
            ## Pause main thread to give a bit of time to webcam thread
            pygame.time.wait(10) 
        self.lock.release()
        return surface            

## Class XWebcam
# This class has responsibilty for the creation and update of the webcam
# resource, this will allow us to capture images from the webcam and use
# that image for user interaction
class XWebcam(pygame.sprite.Sprite):
	##XWebcam Constructor
	#@param self The object pointer
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

        #--------------------------------
        # Setup the Camera
        # use the first video-device which is found
        # devnum=1 uses the second one and so on

        try:
            if gLinux:
                if gVideo4Linux:
                    self.device = Device(0)
                    self.device.setFormat() # This Linux library needs initialise hack
                else: # Video4Linus2
                    self.device = directvideo.VideoSource()
                self.flip = False
            else: # Windows
                self.device=cv2.VideoCapture(0)
                self.flip = True
                        
        except:
            print "XWebcam: No webcam connected or webcam failure"
            raise
            exit()

        if gLinux and gVideo4Linux: 
            res = "tiny" 
        else: # Windows and video4Linux2
            res = "high"            
        camWidth, camHeight = self.camSize = gResolutions[res]
        print "Camera Width "+str(camWidth)+" Camera Height"+str(camHeight)
        if gLinux and gVideo4Linux2:
            #we need to check if this fails
	    #if this does then we should try outher pixel formats
	    if (os.path.exists("/dev/video0")):
	    	self.device.open(
                    device="/dev/video0",
                    width=camWidth,
                    height=camHeight,
                    method="m",
                    input=0,
                    pixelformat=v4l2_consts.V4L2_PIX_FMT_YUYV
                )
        else:
            #windows and mac
            #highgui.cvSetCaptureProperty(self.device,highgui.CV_CAP_PROP_FRAME_WIDTH,camWidth)
            #highgui.cvSetCaptureProperty(self.device,highgui.CV_CAP_PROP_FRAME_HEIGHT,camHeight)
            self.device=cv2.VideoCapture(0)
            self.device.set(3,camWidth)
            self.device.set(4,camHeight)
            
        self.watch = XWatchArray()
        self.windowRect = None
        self.maskImage = None
        self.camImage = None
        self.image = None ## The one that gets rendered (XWebcam is a subclass of Sprite)
        self.cam = None
        self.saver = None
        self.recording = False
        self.detectStart = gDetectStart
            
    def __del__(self):
        if gLinux and gVideo4Linux2: self.device.close()
        del self.device
		
	##Set Screen Size<br>
	#Sets the screen size that this webcam will operate on
	#@param self The object pointer
	#@param screenSize The x and y size of the screen
    def set_screen_size(self, screenSize):
        width, height = screenSize
        self.watch.set_screen_resolution(width, height)
    
	##Set Mask>br>
	#Set the webcam mask, this allows us to limit the region where user interaction
	# can occur. This allows us to optimise webcam interaction
	# @param self The object pointer
	# @param viewPos The position of the mask
	# @param viewSize The size of the mask
	# @param maskFilename The filename of the image that constains the mask
    def set_mask(self, viewPos, viewSize, maskFilename=None):
        if maskFilename:
            img, rect = image_load(maskFilename, None)
            self.maskImage = pygame.transform.scale(img, self.windowRect.size)
        else:
            self.maskImage = None
        self.viewRect = Rect(viewPos, viewSize)
        self.watch.set_mask(self.viewRect, self.maskImage)
        self.rect = self.viewRect.clip(self.windowRect)
		
	## Set Params<br>
	# Sets the various parameters of the webcam
	#@param windowPos The position of the window where the webcam will be displayed to
	#@param windowSize The size of the window
	#@param viewPos The position on the webcam image we will use
	#@param viewSize The size of the webcam image
	#@param maskFilename The filename of the webcam mask we are going to use
	#@param blobs The number of 'blobs' that we are going to generate, used for user interaction
	#@param blank Boolean to control whether we are going to capture from the webcam
	# or just display a blank image
    def set_params(self, windowPos, windowSize, viewPos, viewSize, maskFilename=None, blobs=gNumBlobs, blank=False):

        if self.windowRect and self.windowRect.size != windowSize:
            self.stop()
            
        self.windowRect = Rect(windowPos, windowSize)        
        self.watch.set_window_resolution(self.windowRect.width, self.windowRect.height)
        self.set_mask(viewPos, viewSize, maskFilename)
        self.watch.set_num_blobs(blobs)
                
        ## Make sure we have something for returning
        self.set_blank(blank)        
        if not self.cam:
            self.start()
	
    ##Set webcam blank<br>
	#Specfies if we should just retrieve a blank image from the webcam
	#@param self The object pointer
    def set_blank(self, bool):
        self.blank = bool
        self.image = pygame.Surface(self.windowRect.size)
        self.image.fill((0,0,0))
     
	##Set Element<br>
	#Sets the XElement that describes the webcam properties
	#@param self The object pointer
	#@param element The XElement that describes the webcam
    def set_element(self, element):        
        x = element.get_attr_int('x')
        y = element.get_attr_int('y')
        width = element.get_attr_int('width')
        height = element.get_attr_int('height')
        vx = element.get_attr_int('vx', x)
        vy = element.get_attr_int('vy', y)
        vwidth = element.get_attr_int('vwidth', width)
        vheight = element.get_attr_int('vheight', height)
        maskFilename = element.get_attr_string('mask', None)
        blobs = element.get_attr_int('blobs', gNumBlobs)
        blank = element.get_attr_bool('blank', False)
        self.set_params((x, y), (width, height), (vx, vy), (vwidth, vheight), maskFilename, blobs, blank)
		
	## Start<br>
	# Starts the webcam, this allows us to start to capture images from the webcam
	#@param self The object pointer
    def start(self):
       if self.cam == None:
            self.cam = XWebcamThread(self.device, self.camSize, self.windowRect.size, self.flip)
            self.cam.start()
       if self.saver == None:
            self.saver = XSaveThread()
            self.saver.start()
    
	##Is Active<br>
	#Specfies if we have actually started our webcam
	#@param self The object pointer
	#@returns active A boolean to specify if we have started our webcam
    def is_active(self):
        return self.cam != None
	
	##Stop<br>
	#Stops the webcam
	#@param self The object pointer
    def stop(self):
        if self.cam:
            self.cam.stop()
            self.cam.join()
            del(self.cam)
            self.cam = None
        if self.saver:
            self.saver.stop()
            self.saver.join()
            del(self.saver)
            self.saver = None
			
	##Get Mask Value<br>
	#Gets the value of the mask at the specfied position
	#@param self The object pointer
	#@param pos The position in the mask
	#@param returns colour The rgb value of the pixel
    def get_mask_val(self, pos):
        if self.maskImage:
            return self.maskImage.get_at(pos)
        else:
            return None
		
	##Get Image<br>
	#Gets the image retrieved from the webcam
	#@param self The object pointer
	#@param image The webcam image
    def get_image(self):
        image = self.cam.get_image()
        if image:
            del self.camImage
            self.camImage = image
            if not self.blank: 
                del self.image
                self.image = self.camImage.subsurface(self.viewRect)
            if self.saver: self.saver.save_image(self.camImage)
        return image
			
	##Reset Calibration<br>
	# Resets webcam calibration
	# @deprecated We no longer need to calibrate the webcam
	# @param self The object pointer
    def reset_calibration(self):
        ## deprecated
        pass
	
	##Is Calibrating<br>
	# Specfies if we are still calibrating the webcam
	# @deprecated We no longer need to calibrate the webcam
	# @param self The object pointer
	# @returns calbirating A boolean that specfies if we are still calibrarting
    def is_calibrating(self):
        ## deprecated
        return False
    
	##Is Calibrated<br>
	# Specfies if we have calibrated the webcam
	# @deprecated We no longer need to calibrate the webcam
	# @param self The object pointer
	# @returns calibrated A boolean that specfies if the webcam has been calibrated
    def is_calibrated(self):
        ## deprecated
        return True
    
	##Start Calibration<br>
	# Starts the calibration of the webcam
	# @deprecated We no longer need to calibrate the webcam
	# @param self The object pointer
    def start_calibration(self):
        ## deprecated
        pass
	
	##Stop Calibration<br>
	# Stops webcam calibration
	# @deprecated We no longer need to calibrate the webcam
	# @param self The object pointer
    def stop_calibration(self):
        ## deprecated
        pass
	
	##Detect motion<br>
	# Detects motion in the image retrieved from the webcam
	#@param self The object pointer
	#@param elapsedTime The elapsed time since the last game update
	#@param screenSize The Size of screen
	#@returns bolbSprites The list of sprites generate by user movement
    def detect_motion(self, elapsedTime, screenSize):
        blobSprites = []
        if self.detectStart > 0:
            self.detectStart -= elapsedTime
        else:
            blobSprites = self.watch.detect_motion(self.camImage, elapsedTime)
        return blobSprites
    
	##Set recording<br>
	# Sets the webcam to record, this allows us to retrieve images from the webcam 
	# and save them to a folder
	#@param self The object pointer
	#@param bool A boolean to specify if we should save images from the webcam
	#@param dir A path to directory where we are going to save the images
    def set_recording(self, bool, dir=None):
        if self.saver:
            self.saver.set_recording(bool, dir)
                
#--------------------------------------------------------------------
