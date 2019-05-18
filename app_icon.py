#!/usr/bin/env python
#-*- coding: utf-8 -*-

import inkex
from simplestyle import *
from lxml import etree
import os
#from pathlib import Path
import traceback
import sys

class GenerateIconsEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('-i', '--ios_icons', action = 'store',
          type = 'string', dest = 'ios', default = 'false',
          help = 'Will you create ios icons?')
        self.OptionParser.add_option('-a', '--android_icons', action = 'store',
          type = 'string', dest = 'android', default = 'false',
          help = 'Will you create android icons')
    # TODO: add support for custom path to save file
    # TODO: add android support
    def effect(self):
        # make sure the doc meets the requirements
        passing = self.runTests()

        if passing == False:
            inkex.errormsg(_("Errors encountered. Please fix them and try again."))
            exit()
        else:
            ios = self.options.ios
            android = self.options.android
            svg = self.document.getroot()
            currentFileName = self.args[-1]
            #saveDir = os.path.expanduser("~") #saves icons to the home directory
            if ios == "true":
                path = "~/appicon_output" + currentFileName + "/ios/"
                self.makePath(path)
                # inkex.errormsg(_("calling inkscape -e " + path + "Icon-app-1024.png -h 1024 -f " + currentFileName))
                os.system("inkscape -e " + path + "Icon-App-1024x1024@1x.png -h 1024 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-83.5x83.5@2x.png -h 167 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-76x76@2x.png -h 152 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-76x76@1x.png -h 76 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-60x60@3x.png -h 180 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-60x60@2x.png -h 120 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-40x40@3x.png -h 120 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-40x40@2x.png -h 80 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-40x40@1x.png -h 40 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-29x29@3x.png -h 87 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-29x29@2x.png -h 58 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-29x29@1x.png -h 29 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-20x20@3x.png -h 60 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-20x20@2x.png -h 40 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-App-20x20@1x.png -h 20 -f " + currentFileName)
                inkex.errormsg(_("saving to: " + path))
            if android == "true":
                path = "~/appicon_output" + currentFileName + "/android/"
                self.makePath(path)
                # inkex.errormsg(_("calling inkscape -e " + path + "Icon-app-1024.png -h 1024 -f " + currentFileName))
                os.system("inkscape -e " + path + "Icon-xxxhdpi.png -h 192 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-xxhdpi.png -h 144 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-xhdpi.png -h 96 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-hdpi.png -h 72 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-mdpi.png -h 48 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-ldpi.png -h 36 -f " + currentFileName)
                os.system("inkscape -e " + path + "Icon-512.png -h 512 -f " + currentFileName)
                inkex.errormsg(_("saving to: " + path))


    def runTests(self):
        ios = self.options.ios
        android = self.options.android

        # make sure at least one option is selected
        if ios == 'false' and android == 'false':
            inkex.errormsg(_("No icon groups selected"))
            return False

        #get document and make sure it is a square
        svg = self.document.getroot()
        width  = self.unittouu(svg.get('width'))
        height = self.unittouu(svg.attrib['height'])

        if width != height:
            inkex.errormsg(_("Canvas is not square"))
            return False
        # TODO: add a test for to make sure there is no alpha in the iOS application
        return True

    def makePath(self, path):
        os.system("mkdir -p " + path)

# Create effect instance and apply it.
effect = GenerateIconsEffect()
effect.affect()
