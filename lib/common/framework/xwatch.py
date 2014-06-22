#!/usr/bin/env python

##@file
##@namespace
# This module contains all classes and functions to deal
# with the interaction of user with the webcam interface
import os, sys

import pygame
from pygame.locals import *

from xglobals import *
from xvec2d import XVec2d

## Class XScreenRegion<br>
# Defines a region of the screen, used to optimise webcam interaction
class XScreenRegion:
	##XScreenRegion Constructor<br>
	# @param self The object pointer
	# @param rect The size of the region
	# @param pos The position of the region on the screen
	# @param colour The colour of the region
    def __init__(self, rect, pos, colour):
        self.rect = rect
        self.pos = pos
        self.colour = colour


## Class XBlobSprite<br>
# A sprite-like object that contains an XBlob
# This is persistent between frames if a matching blob is found
# Used for collision detection with XSprites
class XBlobSprite(pygame.sprite.Sprite):
	## XBlobSprite Constructor<br>
	# @param self The object pointer
	# @param blob The blob that this Blob Sprite will hold
	# @param screenRegions a list of all screen regions
	# @param elapsedTime The elapsed Time since the last game update
    def __init__(self, blob, screenRegions, elapsedTime):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

        self.blob = blob
        self.rect = blob.rect
        self.rects = blob.rects
        self.velocity = XVec2d(0,0)

        ## Initialise its velocity based on the position of the blobs
        ## likely entry point on the screen
        for region in screenRegions:
            if region.rect.collidepoint(blob.rect.center):
                v = XVec2d(blob.rect.centerx - region.pos[0], blob.rect.centery - region.pos[1])
                self.velocity = v / elapsedTime
				
	##Set blob<br>
	# Sets the blob that this XBlobSprite holds
	# @param self The object pointer
	# @param blob The blob that this will hold
	# @param elapsedTime The elapsed time since the last game update
    def set_blob(self, blob, elapsedTime):
        prevBlob = self.blob
        self.blob = blob
        self.rect = blob.rect
        self.rects = blob.rects

        ## Calculate its velocity based on the position of the
        ## previous blob
        v = XVec2d(blob.rect.centerx - prevBlob.rect.centerx, blob.rect.centery - prevBlob.rect.centery)
        self.velocity = v / elapsedTime
	
	##Draw<br>
	# This draws the blob on the screen, this will be used for
	# debugging purposes
	# @param self The object pointer
	# @param surface The surface object to draw the blob to, usually the screen
    def draw(self, surface):
        colour = gBlobColours[self.blob.id]
        for rect in self.blob.rects:
           surface.fill(colour, rect)
        colour = gBlobColours[(self.blob.id + 1) % len(gBlobColours)]
        rect = Rect(self.rect.center, (10, 10))
        surface.fill((0, 0, 0), rect)
        endPos = self.rect.center + (self.velocity * 20)
        pygame.draw.line(surface, colour, self.rect.center, endPos, 5)

##class XBlob<br>
#
# A collection of rectangles that have changed indicating motion
class XBlob:
	##XBlob Constructor
	#@param self The object pointer
	#@param id The id of the blob
    def __init__(self, id):
        self.id = id
        self.rects = []
        self.rect = None
		
	##Calculate geometry<br>
	#Calcultes the size and position of the blob
	#@param self The object pointer
    def calc_geometry(self):
        self.rect = None
        for rect in self.rects:
            if self.rect:
                self.rect.union_ip(rect)
            else:
                self.rect = Rect(rect)
        self.center = XVec2d(rect.center)
		
	##Compare<br>
	# Sorts blob list into decending order
	#@param blob1 the first blob to compare
	#@param blob2 the second blob to compare 
    def compare(blob1, blob2):
        
        if len(blob1.rects) > len(blob2.rects):
            return -1
        elif len(blob1.rects) == len(blob2.rects):
            return 0
        else:
            return 1
            
## Class XCell<br>
# A region of the screen that is used to track webcam movement
class XCell:
	
	##XCell Constructor<br>
	#@param self The object pointer
	#@param col The column number of the screen area
	#@param row The row number of the screen area 
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.notMasked = True

        self.prevColor = None
        self.nowColor = None
        self.threshold = 0
        
        self.highColor = None
        self.lowColor = None
        
        self.blobId = -1   ## -1 == not active, 0 == active, >0 == blob number
		
	##Set Neighbours<br>
	# Set the neighbouring cells of this XCell
	#@param self The object pointer
	#@param up The cell above
	#@param down The cell below
	#@param left The cell to the left
	#@param right The cell to the right
    def set_neighbours(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
		
	##Set Window resolution<br>
	#Sets the resolution of the current window
	#@param self The object pointer
	#@param x The x position of the window
	#@param y The y position of the window
	#@param width The width of the window
	#@param height The height of the window
    def set_window_resolution(self, x, y, width, height):
        self.windowPos = (x, y)
        self.windowRect = Rect(x, y, width, height)
		
	##Set screen resolution<br>
	#Sets the resolution of the screen
	#@param self The object pointer
	#@param x The x position of the screen
	#@param y The y position of the screen
	#@param width The width of the screen
	#@param height The height of the screen
    def set_screen_resolution(self, x, y, width, height):
        self.screenPos = (x, y)
        self.screenRect = Rect(x, y, width, height)
	
    def __repr__(self):
        return 'XCell(%s, %s, %s, %s)' % (self.col, self.row, self.screenPos, self.windowPos)

## Class XWatchArray<br>
# This class holds an array of cells, and is the class responsible for
# detecting motion in cells which are obtained by movement from the webcam
class XWatchArray:
	## XWatchArray Constructor<br>
	# @param self The Object pointer
    def __init__(self):

        self.font = None
        if pygame.font:
            self.font = pygame.font.Font(None, 12)
        else:
            print "XWatchArray.__init__: Fonts disabled"

        self.cols = gWatchCols
        self.rows = gWatchRows
        self.numBlobs = gNumBlobs
        self.detectMotion = False
        self.sprites = []

        ## create the array of cells
        self.cells = []
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells.append(XCell(col, row))

        ## set each cell neighbours
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row * self.rows + col]
                if col == 0:
                    left = None
                else:
                    left = self.cells[row * self.rows + col-1]
                if col+1 >= self.cols:
                    right = None
                else:
                    right = self.cells[row * self.rows + col+1]
                if row == 0:
                    up = None
                else:
                    up = self.cells[(row-1) * self.rows + col]
                if row+1 >= self.rows:
                    down = None
                else:
                    down = self.cells[(row+1) * self.rows + col]
                cell.set_neighbours(up, down, left, right)
    
	##Set Number of blobs<br>
	#@param self The object pointer
	#@param numBlobs The number of blobs to be head in the array
    def set_num_blobs(self, numBlobs):
        self.numBlobs = numBlobs
		
	##Set the Window resolution<br>
	#@param self The object pointer
	#@param width The width of the window
	#@param height The heigh of the window
    def set_window_resolution(self, width, height):

        self.windowWidth = width
        self.windowHeight = height
        self.windowHgap = width / self.cols
        self.windowVgap = height / self.rows
        self.windowRect = Rect(0, 0, width, height)

        ## set the resolution for each cell
        y = 0
        for row in range(self.rows):
            x = 0
            for col in range(self.cols):
                cell = self.cells[row * self.rows + col]
                cell.set_window_resolution(x, y, self.windowHgap, self.windowVgap)
                x += self.windowHgap
            y += self.windowVgap
	
	##Set screen resolution<br>
	#Sets the resolution of the screen
	#@param self The object pointer
	#@param height The height of the screen
    def set_screen_resolution(self, width, height):
        
        self.screenHgap = width / self.cols
        self.screenVgap = height / self.rows
        self.screenRect = Rect(0, 0, width, height)
        
        ## set the resolution for each cell
        y = 0
        for row in range(self.rows):
            x = 0
            for col in range(self.cols):
                cell = self.cells[row * self.rows + col]
                cell.set_screen_resolution(x, y, self.screenHgap, self.screenVgap)
                x += self.screenHgap
            y += self.screenVgap
            
        ## create screen region rectangles
        self.screenRegions = []
        topLeft = Rect(0, 0, width/4, height/4)
        midLeft = Rect(0, height/4, width/4, height/2)
        botLeft = Rect(0, 3*height/4, width/4, height/4)
        self.screenRegions.append(XScreenRegion(topLeft, topLeft.topleft, (50, 0, 0)))
        self.screenRegions.append(XScreenRegion(midLeft, midLeft.midleft, (100, 0, 0)))
        self.screenRegions.append(XScreenRegion(botLeft, botLeft.bottomleft, (200, 0, 0)))

        topRight = Rect(3*width/4, 0, width/4, height/4)
        midRight = Rect(3*width/4, height/4, width/4, height/2)
        botRight = Rect(3*width/4, 3*height/4, width/4, height/4)
        self.screenRegions.append(XScreenRegion(topRight, topRight.topright, (0, 50, 0)))
        self.screenRegions.append(XScreenRegion(midRight, midRight.midright, (0, 100, 0)))
        self.screenRegions.append(XScreenRegion(botRight, botRight.bottomright, (0, 200, 0)))

        topCenter = Rect(width/4, 0, width/2, height/4)
        midCenter = Rect(width/4, height/4, width/2, height/2)
        botCenter = Rect(width/4, 3*height/4, width/2, height/4)
        self.screenRegions.append(XScreenRegion(topCenter, topCenter.midtop, (0, 0, 50)))
        self.screenRegions.append(XScreenRegion(midCenter, midCenter.center, (0, 0, 100)))
        self.screenRegions.append(XScreenRegion(botCenter, botCenter.midbottom, (0, 0, 200)))

        self.screenRegionRects = []
        for region in self.screenRegions:
            self.screenRegionRects.append(region.rect)
    
	## Set Mask<br>
	# Set the mask for the screen
	# @param self The object pointer
	# @param rect The size of the area of the screen
	# @param mask The mask used
    def set_mask(self, rect, mask):
        for cell in self.cells:
            inside = rect.contains(cell.windowRect)
            if mask:
                ## If red channel is 0 then cell is masked
                cell.notMasked = inside and not (mask.get_at(cell.windowPos)[0] == 0)
            else:
                cell.notMasked = inside
    
	## Set the view rectangle<br>
	# Set the view rectangle of the cells, this is used to do optimise 
	# webcam process to reduce watch area
	# @param self The object pointer
	# @param viewRect The view dimensions
    def set_view_rect(self, viewRect):
        for cell in self.cells:
            if mask:
                ## If red channel is 0 then cell is masked
                cell.notMasked = not (mask.get_at(cell.windowPos)[0] == 0)
            else:
                cell.notMasked = True

	## Detect Motion<br>
	# Detection the webcam motion in array of cells
	# @param self The object pointer
	# @param surface The surface we are checking
	# @param elapsedTime The elapsed time since the last game update
    def detect_motion(self, surface, elapsedTime):
        activeCells = []
        
        for cell in self.cells:
            nowColor = surface.get_at(cell.windowPos)
            if not cell.nowColor:
                cell.nowColor = nowColor[0]
                    
            cell.blobId = -1   # reset its blob group
                
            if cell.notMasked:
                cell.prevColor = cell.nowColor
                cell.nowColor = nowColor[0]        
                if abs(cell.nowColor - cell.prevColor) > gThreshold:
                    cell.blobId = 0
                    activeCells.append(cell)                        

        #-----------------------------------------------------------------------
        #Build lists of connected cells using an flood fill type algorithm

        blobs = self.buildBlobs(activeCells)
                
        #-----------------------------------------------------------------------
        # Try and match new blobs to previous blobs in the sprites
        # If can not then create a new sprite for the blob

        for sprite in self.sprites:
            bestBlob = None
            bestDistance = gMaxBlobDistance
            for blob in blobs:
                distance = abs((sprite.blob.center - blob.center).length)
                if distance < bestDistance:
                    bestDistance = distance
                    bestBlob = blob
            if bestBlob:
                blobs.remove(bestBlob)
                sprite.set_blob(bestBlob, elapsedTime)
            else:
                self.sprites.remove(sprite)

        for blob in blobs:
            if len(self.sprites) < self.numBlobs:
                self.sprites.append(XBlobSprite(blob, self.screenRegions, elapsedTime))
                
        # Debug stuff
        if gShowBlobs==True:
            for sprite in self.sprites:
                sprite.draw(surface)
        if gShowCells:
            font = pygame.font.SysFont("times", 15, False, False)
            for cell in self.cells:
                value = repr(abs(gThreshold - cell.nowColor))
                image = font.render(value, True, (255, 255, 255))
                surface.blit(image, cell.screenPos)
                
        return self.sprites
	
	## Build Blob<br>
	# Build the screen blobs used to for interaction with the game world
	# @param self The object pointer
	# @param blobid The ID of the blob
	# @param cell The cell of the screen we are checking
    def buildBlob(self, blobId, cell):
        
        stack = []
        stack.append(cell)
        blob = XBlob(blobId)
     
        while len(stack):
            cell = stack.pop()
        
            while cell.up and cell.up.blobId == 0: 
                cell = cell.up
            
            spanLeft = spanRight = 0
            
            while cell and cell.blobId == 0:
                                
                cell.blobId = blobId
                blob.rects.append(cell.screenRect)
                
                if not spanLeft and cell.left and cell.left.blobId == 0:
                    stack.append(cell.left)
                    spanLeft = 1
                
                elif spanLeft and cell.left and cell.left.blobId <> 0:
                    spanLeft = 0
                
                if not spanRight and cell.right and cell.right.blobId == 0:
                    stack.append(cell.right)
                    spanRight = 1
                
                elif spanRight and cell.right and cell.right.blobId <> 0:
                    spanRight = 0

                cell = cell.down
                                                
        return blob
    
	##Build blobs<br>
	# Creates blobs for any cells that have movement detected
	# @param self The object pointer
	# @param cells The cless to check
	# @returns blobs The created blobs
    def buildBlobs(self, cells):
        blobId = 1
        blobs = []
        for cell in cells:
            if cell.blobId == 0:
                blob = self.buildBlob(blobId, cell)
                if len(blob.rects) >= gMinBlobSize and len(blob.rects) <= gMaxBlobSize: 
                    blobs.append(blob)
                blobId += 1
        blobs.sort(XBlob.compare)
        del blobs[self.numBlobs:]
        for id, blob in enumerate(blobs):
            blob.id = id
            blob.calc_geometry()
        return blobs

#--------------------------------------------------------------------
