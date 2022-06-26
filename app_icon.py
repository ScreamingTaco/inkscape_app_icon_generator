#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# https://developer.android.com/training/multiscreen/screendensities#java

#          Carlos Vazquez initial version
# 20200408 Ron AF Greve Splitted android dirs in mipmap and drawables and added windows icon and ICO file. Added path variables.


import inkex
from simplestyle import *
from lxml import etree
import os
#from pathlib import Path
import traceback
import sys

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
        self.arg_parser.add_argument('-k', '--ios_icons', action = 'store',
          type = str, dest = 'ios_icons', default = 'false',
          help = 'Create ios icons?')
        self.arg_parser.add_argument('-i', '--ios_path', action = 'store',
          type = str, dest = 'ios_path', default = 'false',
          help = 'Path where the ios icons are stored')
        self.arg_parser.add_argument('-m', '--android_mipmap', action = 'store',
          type = str, dest = 'android_mipmap', default = 'false',
          help = 'Create android mipmap dirs and icons?')
        self.arg_parser.add_argument('-d', '--android_drawable', action = 'store',
          type = str, dest = 'android_drawable', default = 'false',
          help = 'Create android drawable dirs and icons?')
        self.arg_parser.add_argument('-a', '--android_path', action = 'store',
          type = str, dest = 'android_path', default = 'false',
          help = 'Path to and including the android res directory')
        self.arg_parser.add_argument('-t', '--android_tvdpi', action = 'store',
          type = str, dest = 'android_tvdpi', default = 'false',
          help = 'Add android TV resolution')
        self.arg_parser.add_argument('-b', '--android_basepx', action = 'store',
          type = str, dest = 'android_basepx', default = 'false',
          help = 'Add android TV resolution')
        self.arg_parser.add_argument('-x', '--windows_icons', action = 'store',
          type = str, dest = 'windows_icons', default = 'false',
          help = 'Create windows icons?')
        self.arg_parser.add_argument('-c', '--windows_one_ico_file', action = 'store',
          type = str, dest = 'windows_one_ico_file', default = 'false',
          help = 'Create one windows ico file?')
        self.arg_parser.add_argument('-w', '--windows_path', action = 'store',
          type = str, dest = 'windows_path', default = 'false',
          help = 'Path where the windows icons are stored')

        self.arg_parser.add_argument('-n', '--name', action = 'store',
          type = str, dest = 'name', default = 'false',
          help = 'Name of image file without extension or path')
   
    def NormalizeDir( self, Directory ):
        if len( Directory ) == 0:
            return Directory
        if Directory.endswith( "/" ) or Directory.endswith( "\\" ):
            return Directory
        return Directory + "/"

    def effect(self):
        # make sure the doc meets the requirements
        passing = self.runTests()

        if passing == False:
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
            
            name                    = self.options.name

            ios_path        = self.NormalizeDir( ios_path     )
            android_path    = self.NormalizeDir( android_path )
            windows_path    = self.NormalizeDir( windows_path )
            

            svg = self.document.getroot()
            currentFileName = self.options.input_file
            
            #saveDir = os.path.expanduser("~") #saves icons to the home directory
            if ios_icons == "true":
                self.makePath(ios_path)

                os.system("inkscape -o " + ios_path + "Icon-App-1024x1024@1x.png -h 1024 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-1024x1024@1x.png -h 1024 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-83.5x83.5@2x.png -h 167 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-76x76@2x.png -h 152 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-76x76@1x.png -h 76 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-60x60@3x.png -h 180 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-60x60@2x.png -h 120 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-40x40@3x.png -h 120 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-40x40@2x.png -h 80 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-40x40@1x.png -h 40 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-29x29@3x.png -h 87 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-29x29@2x.png -h 58 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-29x29@1x.png -h 29 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-20x20@3x.png -h 60 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-20x20@2x.png -h 40 " + currentFileName)
                os.system("inkscape -o " + ios_path + "Icon-App-20x20@1x.png -h 20 " + currentFileName)
                # inkex.errormsg(_("saving to: " + ios_path))

            if android_mipmap == "true" or android_drawable == "true":
                DirectoryPrefixes = []

                if android_mipmap == "true":
                    DirectoryPrefixes.append( "mipmap" )

                if android_drawable == "true":
                    DirectoryPrefixes.append( "drawable" )
                
                self.makePath( android_path )
                #os.system("inkscape -o " + path + "Icon-xxxhdpi.png -h 192 " + currentFileName)

                # Densities calculated of baseline in ratios 3:4:6:8:12:16
                # Where 4 correspons to mdpi the baseline dpi (for instance 48 so the divisor = 12)
                if android_basepx == 0:
                    android_basepx = 48
                DensityMap = { "ldpi" : 3, "mdpi" : 4, "hdpi" : 6, "xhdpi" : 8, "xxhdpi" : 12, "xxxhdpi" : 16 }
                if android_tvdpi == "true":
                    DensityMap.update( { "tvdpi" : 4 * 1.33 } )

                for Density, Ratio in list(DensityMap.items()):
                    DensityInPx = ( Ratio * android_basepx ) / 4
                    for DirectoryPrefix in DirectoryPrefixes:
                        FullPath = android_path + DirectoryPrefix + "-" + Density + "/" 
                        self.makePath( FullPath )
                        os.system( "inkscape -o " + FullPath + name + ".png -h " + str( DensityInPx ) + " " + currentFileName )

            if windows_icons == "true" or windows_one_ico_file == "true":
                self.makePath( windows_path )
                Resolutions = [ 256, 128, 64, 48, 32, 24, 16, 12, 8 ]
                for Resolution in Resolutions:
                    ImagePath = windows_path + name + "-" + str( Resolution ) + ".png" 
                    os.system("inkscape -o " + ImagePath + " -h " + str( Resolution ) + " " + currentFileName)
                    self.WindowsIconCurList.append( WindowsIconInfo( ImagePath, Resolution ) )
                if windows_one_ico_file == "true":                
                    self.CreateIconFile( windows_path + name + ".ico", 1 )

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
        File = open( WindowsIconInfo.GetImagePath(), "rb" )
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
        File = open( Filename, "wb" )
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
        #os.system("mkdir -p " + path)

# Create effect instance and apply it.
effect = GenerateIconsEffect()
effect.run()
