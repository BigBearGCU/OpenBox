#!/usr/bin/env python

##@file

## @namespace xxml
#
#Handles the parsing and the creation of an xml document

import os, sys

import xml.parsers.expat
import xml.dom.minidom

## XElement class<br>
#Defines an xml element, this element can have many children
#or none 	 
class XElement :
	
    ## XElement constructor<br>
    # @param self The objects pointer
    # @param parent The parent XElement
    # @param attrs The attributes of the XElement, held in a dictonary
    def __init__(self, parent, type, attrs=None):
        self.type = type
        self.parent = parent
        if attrs:
            self.attrs = attrs
        else:
            self.attrs = {}
        self.elements = []
        self.filename = None

    ## Adds an XElement to the current XElement object<br>
    # @param self The object pointer
    # @param element The element we are going to this XElement object
    def add_element(self,element):

        element.parent = self
        self.elements.append(element)
	
    ## Prints out to the screen the current XElement<br>
    #  This functions prints the current XElement to the screen, including all
    #  attached elements and all atributes with the correct indentation.
    #  @param self The object pointer
    #  @param indent What character we use for indenting, by default we use
    #  whitespace
    def debug(self, indent=""):

        s = self.type
        for a in self.attrs.keys():
            s += " " + a + "=\"" + self.attrs[a] + "\""
        if len(self.elements) > 0:
            print indent + "<" + s + ">"
            for e in self.elements: e.debug(indent + "  ")
            print indent + "</" + self.type + ">"
        else:
            print indent + "<" + s + "/>"
	
    ## Writes the current XElement to file<br>
    # This function writes the current XElement to a file, 
    # including all child elements and attributes with the 
    # correct indentation.
    # @param self The object pointer
    # @param file The file object that the XElement will be written to
    # @param indent The character used for indentation, by default whitespace
    def write(self, file, indent=""):
        s = self.type
        for a in self.attrs.keys():
            if self.attrs[a]:
                s += " " + a + "=\"" + self.attrs[a] + "\""
        if len(self.elements) > 0:
            w = indent + "<" + s + ">\n"
            file.write(w)
            for e in self.elements: e.write(file, indent + "  ")
            w = indent + "</" + self.type + ">\n"
            file.write(w)
        else:
            w = indent + "<" + s + "/>\n"
            file.write(w)
	
    ## Saves the current XElement to file<br>
    # This functions saves the current XElement to the specfied file
    # @param self The object pointer
    # @param filename The file object that will be written to
    def save(self, filename=None):
        if filename == None:
            filename = self.filename
        file = open(filename, 'w')
        file.write("<?xml version=\"1.0\"?>\n")
        self.write(file)
        file.close()
	
    ## Returns the specfied attribute value as an Integer<br>
    # This function retrieves the attributes value from the XElement
    # and casts it to an integer. If the attribute dosen't exist or
    # can not be cast as an integer then a default value is returned
    # @param self The object pointer
    # @param attr The name of the attribute we want to retrieve
    # @param default The value that is return if the attribute
    # dosen't exist
    # @return The attribute value or default value
    def get_attr_int(self, attr, default=0):
        try:
            return int(self.attrs[attr])
        except:
            return default
    
    ## Set the specfied attribute value as an integer<br>
    # This function sets the attribute value of XElement, this will also
    # add the attribute to XElement
    # @param self The object pointer
    # @param attr The name of the attribute that we want to set
    # @param value The value of the attribute
    def set_attr_int(self, attr, value):
        self.attrs[attr] = str(value)
	
    ## Returns the specfied attribute value as a floating point value<br>
    # This function retrieves the specfied value of XElement and casts
    # it to a floating point value. If it dosen't exist or can not be cast
    # then the default value is returned
    # @param self The object pointer
    # @param atter The name of the attribute that we want to retrieve
    # @param default The value that will be retuirn if this function fails
    # @return The attribute value cast as a floating point number
    def get_attr_float(self, attr, default=0.0):
        try:
            return float(self.attrs[attr])
        except:
            return default
	
    def set_attr_float(self, attr, value):
        self.attrs[attr] = str(value)

    def get_attr_string(self, attr, default=None):
        try:
            return self.attrs[attr]
        except:
            return default

    def set_attr_string(self, attr, value):
        self.attrs[attr] = value

    def get_attr_bool(self, attr, default=False):
        try:
            return (self.attrs[attr] == 'true')
        except:
            return default

    def set_attr_bool(self, attr, value):
        if value:
            self.attrs[attr] = "true"
        else:
            self.attrs[attr] = "false"

##
# XML Parser handler functions<br>
# Note that can not make it recursive as the xml library requires
# handler functions to be set and therefore object mthods would not work

rootElement = None
currentElement = None

def start_element(type, attrs):
    #print 'Element type=%s attrs=%s' % (type, attrs)
    global currentElement, rootElement 
    element = XElement(currentElement, type, attrs)
    if currentElement == None: 
        rootElement = element
    else:
        currentElement.elements.append(element)

    currentElement = element

def end_element(type):
    #print 'End element:', type
    global currentElement
    currentElement = currentElement.parent

def char_data(data):
    #print 'Character data:', repr(data)
    pass

## Loads an XElement from an XML file<br>
# This function opens up an XML file and creates an
# XElement which is the root element of the XML file. 
# You can then use this XElement to retrieve any Element
# or attribute that was contained in the XML.
# @param filename The string that represents the path and the filename
# of the XML file you want to load
# @return rootElement The root XElement contained in the XML 
def xml_load(filename):
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data

    f = open(filename, 'r')
    p.ParseFile(f)
    f.close()

    if rootElement:
        rootElement.filename = filename
    return rootElement

## Saves the XElement to a file<br>
# This function saves an XElement to file, including all child XElements
# and all attached attributes
# @param element The XElement we want to save
# @param filename The filename where we want to the save the XElement to
def xml_save(element, filename=None):
    element.save(filename)

#--------------------------------------------------------------------

#this calls the 'main' function when this script is executed

if __name__ == '__main__':
    element = xml_load('game.xml')
    element.debug()

