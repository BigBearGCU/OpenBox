#--------------------------------------------------------------------
# System

import platform
gSystem = platform.system()
gLinux = (gSystem == 'Linux')
gWindows=(gSystem=='Windows')
gMac=(gSystem=='Darwin')

#--------------------------------------------------------------------
if gLinux:
    gFps = 40
    gImageFps = 20
elif gWindows: # Windows
    gFps = 60
    gImageFps = 10
elif gMac:
    gFps=40
    gImageFps=40

gWebcamFps = 40
gSaveFps = 3
gImageFps = 10

#--------------------------------------------------------------------
# Webcam

gVideo4Linux = False        # On Linux whether to use v4l (True) or v4l2 (False) libraries
gVideo4Linux2 = not gVideo4Linux

gDetectStart = 250         # Give camera a chance to start up before detecting motion
gMinBlobSize = 4           # Weed out small blobs due to screen flicker
gMaxBlobSize = 80          # Weed out webcam blitz
gThreshold   = 15          # Max background color fluctuation before detected as motion

gResolutions = {'tiny': (160, 120), 'small': (176, 144), 'low': (320, 240), 'med': (352, 288), 'high': (640, 480)}

gWatchCols = 25
gWatchRows = 25

gNumBlobs = 2  # Number of blobs - can be overridden in XML

# For debug, need at least as many as gNumBlobs or as set in XML
gBlobColours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 128), (255, 255, 0), (0, 255, 255)]

# For determining if same blob from one frame to next
gMaxBlobDistance = 200   # maximum distance same blob could have moved

gShowBlobs=False
gShowCells=False

gFullScreen=False
gShowFPS=False
gEeePC=False
