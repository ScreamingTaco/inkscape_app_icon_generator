#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# https://developer.android.com/training/multiscreen/screendensities#java

#          Carlos Vazquez initial version
# 20200408 Ron AF Greve Splitted android dirs in mipmap and drawables and added windows icon and ICO file. Added path variables.

import inkex
from inkex import command
from simplestyle import *
from lxml import etree
import os
#from pathlib import Path
import traceback
import sys

DEBUG = False
WINDOWS_ICON_RESOLUTIONS = [256, 128, 64, 48, 32, 24, 16, 12, 8]
IOS_ICON_RESOLUTIONS = [1024, 1024, 167, 152, 76, 180, 120, 120, 80, 40, 87, 58, 29, 60, 40, 20]


def debug(msg):
    if DEBUG:
        inkex.utils.debug(msg)


def export_image(source, output, resolution=None):
    args = [source, "-o", output]
    if resolution:
        args += ["-h", str(resolution)]
    debug("Calling Inkscape with args %s" % args)
    command.inkscape(*args)


class WindowsIconInfo():
    # Note the windows icon file can either be a ICO or CUR file 
    # (the latter needs to have the coordinates of the the pixel that acts as the pointer i.e. that pixel decides if the cursor is above another object)
    ICO = 1
    CUR = 2

    # -- Specify CurX and CurY only if it is a CUR file, otherwise it will be ignored
    def __init__( self, ImagePath, Height, CurX = 0, CurY = 0 ):
        self.ImagePath = ImagePath
        self.Height    = Height
        self.CurX      = CurX
        self.CurY      = CurY
  
    def GetHeight( self ):
        return self.Height 
	  
    def GetImagePath( self ):
        return self.ImagePath 

    def GetCurX( self ):
        return self.CurX 
	  
    def GetCurY( self ):
        return self.CurY



class GenerateIconsEffect(inkex.Effect):
    WindowsIconCurList = []

    def __init__(self):
        inkex.Effect.__init__(self)

        # Arguments for generating ios icons
        self.arg_parser.add_argument('-k', '--ios_icons', dest='ios_icons', default='false',
                                     help='Create ios icons?')
        self.arg_parser.add_argument('-i', '--ios_path', dest='ios_path', help='Path where the ios icons are stored')

        # Arguments for generating Android icons
        self.arg_parser.add_argument('-m', '--android_mipmap', dest='android_mipmap', default='false',
                                     help='Create android mipmap dirs and icons?')
        self.arg_parser.add_argument('-d', '--android_drawable', dest='android_drawable', default='false',
                                     help='Create android drawable dirs and icons?')
        self.arg_parser.add_argument('-a', '--android_path', dest='android_path', default='false',
                                     help='Path to and including the android res directory')
        self.arg_parser.add_argument('-t', '--android_tvdpi', dest='android_tvdpi', default='false',
                                     help='Add android TV resolution')
        self.arg_parser.add_argument('-b', '--android_basepx', dest='android_basepx', default='false',
                                     help='Add android TV resolution')

        # Arguments for generating Windows icons
        self.arg_parser.add_argument('-x', '--windows_icons', dest='windows_icons', default='false',
                                     help='Create windows icons?')
        self.arg_parser.add_argument('-c', '--windows_one_ico_file', dest='windows_one_ico_file', default='false',
                                     help='Create one windows ico file?')
        self.arg_parser.add_argument('-w', '--windows_path', dest='windows_path',
                                     help='Path where the windows icons are stored')
        self.arg_parser.add_argument('-n', '--name', dest='name', default='false',
                                     help='Name of image file without extension or path')

    def effect(self):
        # make sure the doc meets the requirements
        passing = self.runTests()

        if not passing:
            inkex.errormsg(_("Errors encountered. Please fix them and try again."))
            exit()
        else:
            ios_icons               = self.options.ios_icons
            ios_path                = self.options.ios_path

            android_mipmap          = self.options.android_mipmap
            android_drawable        = self.options.android_drawable
            android_path            = self.options.android_path
            android_tvdpi           = self.options.android_tvdpi
            try:
                android_basepx          = int( self.options.android_basepx )
            except:
                android_basepx = 48

            windows_icons           = self.options.windows_icons
            windows_one_ico_file    = self.options.windows_one_ico_file
            windows_path            = self.options.windows_path
            
            icon_base_name                    = self.options.name

            svg = self.document.getroot()
            currentFileName = self.options.input_file
            
            #saveDir = os.path.expanduser("~") #saves icons to the home directory

            if ios_icons == "true":
                self.makePath(ios_path)
                for resolution in IOS_ICON_RESOLUTIONS:
                    ios_icon_name = "Icon-App-{res}x{res}@1x.png".format(res=resolution)
                    debug('Exporting ios image %s' % ios_icon_name)
                    export_image(
                        currentFileName,
                        os.path.join(ios_path, ios_icon_name),
                        resolution
                    )

                # inkex.errormsg(_("saving to: " + ios_path))

            if android_mipmap == "true" or android_drawable == "true":
                android_icon_name = "%s.png" % icon_base_name

                DirectoryPrefixes = []

                if android_mipmap == "true":
                    DirectoryPrefixes.append( "mipmap" )

                if android_drawable == "true":
                    DirectoryPrefixes.append( "drawable" )
                
                self.makePath( android_path )
                #os.system("inkscape -e " + path + "Icon-xxxhdpi.png -h 192 -f " + currentFileName)

                # Densities calculated of baseline in ratios 3:4:6:8:12:16
                # Where 4 corresponds to mdpi the baseline dpi (for instance 48 so the divisor = 12)
                if android_basepx == 0:
                    android_basepx = 48
                DensityMap = { "ldpi" : 3, "mdpi" : 4, "hdpi" : 6, "xhdpi" : 8, "xxhdpi" : 12, "xxxhdpi" : 16 }
                if android_tvdpi == "true":
                    DensityMap.update( { "tvdpi" : 4 * 1.33 } )

                for Density, Ratio in DensityMap.items():
                    DensityInPx = ( Ratio * android_basepx ) / 4
                    for DirectoryPrefix in DirectoryPrefixes:
                        FullPath = os.path.join(android_path, "%s-%s" % ( DirectoryPrefix, Density ))
                        self.makePath( FullPath )
                        targetFile = os.path.join(FullPath, android_icon_name)
                        export_image(
                            currentFileName,
                            targetFile,
                            int(DensityInPx)
                        )

            if windows_icons == "true" or windows_one_ico_file == "true":
                self.makePath( windows_path )

                for resolution in WINDOWS_ICON_RESOLUTIONS:
                    windows_icon_name = "%s-%s.png" % (icon_base_name, resolution)
                    icon_dest_path = os.path.join(windows_path, windows_icon_name)
                    export_image(
                        currentFileName,
                        icon_dest_path,
                        resolution)
                    self.WindowsIconCurList.append( WindowsIconInfo( icon_dest_path, resolution ) )
                if windows_one_ico_file == "true":
                    ico_file_path = os.path.join(windows_path, "%s.ico" % icon_base_name)
                    self.CreateIconFile(ico_file_path, 1)

    # Write int (defined in this program as 2 bytes ) 
    def WriteInt2ToByteArray( self, ByteArray, Value ):
        ByteArray.append( Value & 0xFF ) 
        ByteArray.append( Value >> 8  ) 

    # Write int (defined in this program as 2 bytes ) 
    def WriteInt4ToByteArray( self, ByteArray, Value ):
        ByteArray.append( Value & 0xFF ) 
        ByteArray.append( ( Value >> 8 ) &0xFF ) 
        ByteArray.append( ( Value >> 16 ) &0xFF ) 
        ByteArray.append( ( Value >> 24 ) &0xFF ) 

    def WriteIconDirEntry( self, ByteArray, WindowsIconInfo, Type ):
        # 256 should be written as 0 everything else just as it is (it can't be larger than 256 pixels)
        # Since we only allow squares, write the height twice
        ByteArray.append( WindowsIconInfo.GetHeight() if WindowsIconInfo.GetHeight() < 256 else 0 ) 
        ByteArray.append( WindowsIconInfo.GetHeight() if WindowsIconInfo.GetHeight() < 256 else 0 ) 
        # -- No palette
        ByteArray.append( 0 ) 
        # -- Reserved 
        ByteArray.append( 0 ) 

        # -- Number of color planes  or the hotspot position for the cursor
        if Type == WindowsIconInfo.ICO:
            # -- Number of color planes ( not sure this matters for png's) 
            self.WriteInt2ToByteArray( ByteArray, 1  )  
            # -- Number of bits per pixel ( I hope this is always true color) 
            self.WriteInt2ToByteArray( ByteArray, 32 )  
        else:
            # -- Hotspot position for the cursor
            self.WriteInt2ToByteArray( ByteArray, WindowsIconInfo.GetCurX() )  
            self.WriteInt2ToByteArray( ByteArray, WindowsIconInfo.GetCurY() )  

        # -- Write the file size
        Filesize = os.stat( WindowsIconInfo.GetImagePath() ).st_size
        self.WriteInt4ToByteArray( ByteArray, Filesize )

        # -- Offset from beginning of file 
        self.WriteInt4ToByteArray( ByteArray, self.CurrentOffset )
        self.CurrentOffset = self.CurrentOffset + Filesize

    def WriteFile( self, ByteArray, WindowsIconInfo ):
        with open( WindowsIconInfo.GetImagePath(), "rb" ) as File:
            ByteArrayFile = bytearray( File.read() )
            ByteArray.extend( ByteArrayFile )
        
        
    def CreateIconFile( self, Filename, Type ):
        self.CurrentOffset = 0
        ByteArray = bytearray()
        # ---- Write windows icon format. Note that the format is in little endian i.e. MSB goes last
        # -- Header Reserved. Must always be 0
        self.WriteInt2ToByteArray( ByteArray, 0 )

        # -- Specifies image type icon of cursor
        self.WriteInt2ToByteArray( ByteArray, Type )
        
        # -- Write number of images in the file  
        Size = len( self.WindowsIconCurList )
        self.WriteInt2ToByteArray( ByteArray, Size )

        self.CurrentOffset = len( ByteArray ) + len( self.WindowsIconCurList ) * 16

        # ---- Write the icon dir entrie(s)
        for WindowsIconInfo in self.WindowsIconCurList:
            self.WriteIconDirEntry( ByteArray, WindowsIconInfo, Type )      

        # ---- Write the icon image file(s). Note that only PNG is supported (since the BitmapFileHeader structure would have to 
        # be stripped of in case of BMP (which isn't difficult but I am to lazy to do right now)
        for WindowsIconInfo in self.WindowsIconCurList:
            self.WriteFile( ByteArray, WindowsIconInfo )      

        # -- Output to a file
        with open( Filename, "wb" ) as File:
            File.write( ByteArray )






    def runTests(self):
        ios_icons = self.options.ios_icons
        android_mipmap = self.options.android_mipmap
        android_drawable = self.options.android_drawable
        windows_icons = self.options.windows_icons

        # make sure at least one option is selected
        if ios_icons == 'false' and android_drawable == 'false' and android_mipmap == 'false' and windows_icons =='false':
            inkex.errormsg(_("No icon groups selected"))
            return False

        #get document and make sure it is a square
        svg = self.document.getroot()
        width  = self.svg.unittouu(svg.get('width'))
        height = self.svg.unittouu(svg.attrib['height'])

        if width != height:
            inkex.errormsg(_("Canvas is not square"))
            return False
        # TODO: add a test for to make sure there is no alpha in the iOS application
        return True

    def makePath(self, path):
        if not os.path.exists( path ):
            os.makedirs( path )

# Create effect instance and apply it.
effect = GenerateIconsEffect()
effect.run()
