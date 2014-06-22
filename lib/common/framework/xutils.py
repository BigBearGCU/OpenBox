#!/usr/bin/env python
##@file
##@namespace xutils
# Holds utility functions used by othe classes in the idore system
import os, sys

import pygame
from pygame.locals import *
from string import atoi
from datetime import *
point_cache = {}

EXERCISE_MOVIES_DIRECTORY = "ex_movies"

#load points<br>
#loads a lists of points from a file and returns that list of points C{(x, y)}.
#@param filename: Name of file to load data from.
#        Data should be formatted as C{(x, y)} with
#        one point per line.
def load_points(filename):
    
    print "load_points(filename):", filename

    global point_cache

    if point_cache.has_key(filename):
        points = point_cache[filename]
        return points

    else:
#        dirs = get_dirs('paths')

#        full_path = get_full_path(filename, dirs)
#        full_path = os.path.join('../images', name)
        
        full_path = filename  
        try:
            f = file(full_path)
        except IOError:
            f = None

        if f is None:
            raise pygame.error, 'Could not load %s' % filename

        points = []
        for line in f.readlines():
            line = line.strip()
            xRaw, yRaw = line.split(',')
            x = int(xRaw[1:])
            y = int(yRaw[:-1])
            points.append((x, y))

        point_cache[filename] = points
        print "Successfully loaded point file: ", filename
        #print "Path ponts = ", points
        return points

#def load_points(filename):
#    global point_cache                
#    full_path = os.path.join('../path', filename)
#    try:
#        f = file(full_path)
#    except IOError:
#        f = None
# 
#        if f is None:
#            raise pygame.error, 'Could not load %s' % filename
# 
#        points = []
#        for line in f.readlines():
#            line = line.strip()
#            xRaw, yRaw = line.split(',')
#        x = int(xRaw[1:])
#        y = int(yRaw[:-1])
#        points.append((x, y))
#        print "points from xutils: ", points
#
#    return points  

#--------------------------------------------------------------------
# Image loading

gMissingImage = None

## Set missing image<br>
# Sets the image that will be displayed if asset is missing or
# can not be loaded
# @param fullname The filename of the error image
def set_missing_image(fullname):
    try:
        global gMissingImage
        gMissingImage = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load missing assets image:', fullname

## Load Image<br>
# Loads an image from a filename
# @param name The filename of the image
# @param colorKey The colour key of the image, this colour will
# transparent when the image is display
# @returns The image loaded and the image dimensions
def image_load(name, colorkey=None):
    
    #print "image_load(name):", name
    
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name, repr(gMissingImage)
        if gMissingImage:
            image = gMissingImage
        else:
            raise
#    if colorkey is not None:
#        if colorkey is -1:
#            colorkey = image.get_at((0,0))
#        image.set_colorkey(colorkey, RLEACCEL)
    image = image.convert_alpha()
    return image, image.get_rect()

## Load Movie<br>
# Loads an image from file
# @param name The filename of the movie to load
# @returns movie The loaded movie
def movie_load(name):
    fullname = os.path.join(EXERCISE_MOVIES_DIRECTORY, name)
    
    if not os.path.exists(fullname):
            fullname = os.path.join('assets', name)
            
    try:
        movie = pygame.movie.Movie(fullname)
    except pygame.error, message:
            print 'Cannot load movie:', name
            raise SystemExit, message
    return movie

## returns a hitmask using an image's colorkey<br>
#@param image  a pygame Surface,
#@param rect pygame Rect that fits image,
#@param key an over-ride color, if not None will be used instead of the image's colorkey
#@returns Hitmask
def get_colorkey_hitmask(image, rect, key=None):

    if key==None:colorkey=image.get_colorkey()
    else:colorkey=key
    mask=[]
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not image.get_at((x,y)) == colorkey)
    return mask

##returns a hitmask using an image's alpha<br>
#@param image pygame Surface
#@param rect pygame Rect that fits image
#@param alpha the alpha amount that is invisible in collisions
#@returns Hitmask
def get_alpha_hitmask(image, rect, alpha=0):

    mask=[]
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not image.get_at((x,y))[3]==alpha)
    return mask

##returns a hitmask using an image's alpha and colour key<br>
#@param image pygame Surface
#@param rect pygame Rect that fits image
#@param key an over-ride color, if not None will be used instead of the image's colorkey
#@param alpha the alpha amount that is invisible in collisions
#@returns Hitmask
def get_colorkey_and_alpha_hitmask(image, rect, key=None, alpha=0):
    if key==None:colorkey=image.get_colorkey()
    else:colorkey=key
    mask=[]
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not (image.get_at((x,y))[3]==alpha or\
                                image.get_at((x,y))==colorkey))
    return mask
		
##Get full hitmask<br>
#returns a completely full hitmask that fits the image, without referencing the images #colorkey or alpha
#@param image pygame Surface
#@param rect pygame Rect that fits image
#@returns Hitmask
def get_full_hitmask(image, rect):

    mask=[]
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(True)
    return mask

## Colour parsing<br>
# Parse colour defined in HTML format "#rrggbb" (hex values)
# @param string The colour as a string in hex value format
# @return The r,g,b colour
def parse_colour(string):
    try:
        r = atoi(string[1:3], 16)
        g = atoi(string[3:5], 16)
        b = atoi(string[5:7], 16)
        return (r, g, b)
    except:
        return (0,0,0)

## Format Date<br>
# Formats a date into a specfied format
# @param date The date to be formated
# @param format The format of the date
def format_date(date,format):
	dateStr,ms=str(date).split(".",1)
	return datetime.strptime(str(dateStr), format)

## Format Date from string<br>
# @param dateStr The date in string date
# @param format The format of the date
def format_date_string(dateStr,format):
	return datetime.strptime(dateStr, format)
