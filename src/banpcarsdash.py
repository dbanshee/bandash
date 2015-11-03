# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

#!/usr/bin/env python 

import Tkinter as tk
import ttk as ttk
import tkFont
#import threading
import time
#import requests
import pycurl
import json
from StringIO import StringIO
from PIL import Image, ImageTk

__author__ = "onamaya"
__date__ = "$30-oct-2015 17:11:18$"

class Win(tk.Tk):

    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)
        self.bind('<Button-2>',self.quit)
        self.bind('<Button-3>',self.quit)
        self.wm_attributes('-topmost', 1)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y
        
    def quit(self, event):
       self.destroy()


class Application(tk.Frame):
    def __init__(self, master=None, dataSource=None):
        tk.Frame.__init__(self, master)
        
        self.dataSource = dataSource
        self.widgets = []

        self.configure(background='#000')
        self.pack(fill=tk.BOTH, expand=1)
        #self.place(height=500, width=500)

        self.createWidgets()

    # Load screns from files
    def createWidgets(self):
        
        
        # Car Name
        carLabel = GenericLabel(    master=self, posX=400, posY=350, height=110, width=550, 
                                    dataSource=self.dataSource, dataFieldName="MCARNAME", defaultValue='-', labelFontName='Digital-7 Mono',
                                    labelFontSize=45, labelColor='#ffc90e', subLabelFontName='Digital-7 Mono')
        carLabel.place()
        self.addItem(carLabel)
        

        # Speed
        speedLabel = GenericLabel(  master=self, posX=550, posY=10, height=110, width=180, 
                                    #subLabelName="SPEED",  subLabelColor='#ffc90e', subLabelFontSize=12, 
                                    dataSource=self.dataSource, dataFieldName="MSPEED", defaultValue='0',  labelFontName='Digital-7 Mono',
                                    labelFontSize=50, labelColor='#ffc90e', subLabelFontName='Digital-7 Mono',
                                    transFunc=lambda x: int(x*3.6))
        speedLabel.place()
        self.addItem(speedLabel)
        
        #Rpms
        rpmLabel = GenericLabel(    master=self, posX=95, posY=20, height=50, width=280, 
                                    subLabelName="RPM ", subLabelFontSize=35, subLabelColor='#80FF00', subLabelSide=tk.LEFT, labelFontName='Digital-7 Mono',
                                    dataSource=self.dataSource, dataFieldName="MRPM", defaultValue='0',  subLabelFontName='Digital-7 Mono',
                                    labelFontSize=50, labelColor='#ffc90e',
                                    transFunc=lambda x: str(int(round(x))).rjust(5))
        rpmLabel.place()
        self.addItem(rpmLabel)
        
        # Gear
        gearLabel = GenericLabel(   master=self, posX=550, posY=100, height=250, width=180, 
                                    #subLabelName="GEAR", subLabelColor='#0f0', subLabelFontSize=20,  subLabelFontName='Digital-7 Mono'
                                    dataSource=self.dataSource, dataFieldName="MGEAR", defaultValue='N',  labelFontName='Digital-7 Mono',
                                    labelFontSize=200, labelColor='#ffc90e',
                                    transFunc=lambda x: 'N' if x == 0 else ('R' if x == -1 else str(x)))
        gearLabel.place()
        self.addItem(gearLabel)
                 
       
        # Fuel Bar
        fuelBar = BarLabel(     master=self, posX=85, posY=560, height=150, width=82, 
                                subLabelName="FUEL", dataSource=self.dataSource, dataFieldName="MFUELLEVEL",
                                subLabelFontSize=25, subLabelFontName = 'Digital-7 Mono',
                                barColor='#804040', subLabelColor='#80FF00',
                                transFunc=lambda x: x*100)   
                                
                                    
        fuelBar.place()
        self.addItem(fuelBar)
        
        
        # Session Info
        posLabel = GenericLabel(    master=self, posX=775, posY=20, height=80, width=250, 
                                    subLabelName="POS", subLabelFontSize=40, subLabelColor='#80FF00', subLabelSide=tk.LEFT, labelFontName='Digital-7 Mono',
                                    dataSource=self.dataSource, dataFieldName="EXT_MPOSITION", defaultValue='0',  subLabelFontName='Digital-7 Mono',
                                    labelFontSize=50, labelColor='#ffc90e',)
        posLabel.place()
        self.addItem(posLabel)
        
        
        
        #################
        # Times 
        #################
        
        # Lap Time
        timesFontSize       = 35
        timesLabelFontSize  = 15
        timeHeight          = 95
        timeWidth           = 210
        
        pX = 1050
        pY = 10
        
        lapTimeLabel = TimeLabel(   master=self, posX=pX, posY=pY, height=timeHeight, width=timeWidth, labelColor='#8ff',
                                    subLabelName="LAP TIME", dataSource=self.dataSource, dataFieldName="EXT_MCURRENTTIME", 
                                    labelFontSize=timesFontSize, subLabelFontSize=timesLabelFontSize,  labelFontName='Digital-7 Mono',
                                    subLabelColor='#8ff', condColor="#f00")
                                    
        lapTimeLabel.place()
        self.addItem(lapTimeLabel)
        
        pY = pY + timeHeight
        lastTimeLabel = TimeLabel(  master=self, posX=pX, posY=pY, height=timeHeight, width=timeWidth, 
                                    subLabelName="LAST LAP TIME", dataSource=self.dataSource, dataFieldName="EXT_MLASTLAPTIME",
                                    labelFontSize=timesFontSize, subLabelFontSize=timesLabelFontSize,  labelFontName='Digital-7 Mono',
                                    subLabelColor='#0f0', condColor="#0f0")
                                    
        lastTimeLabel.place()
        self.addItem(lastTimeLabel)
        
        pY = pY + timeHeight
        bestTimeLabel = TimeLabel(  master=self, posX=pX, posY=pY, height=timeHeight, width=timeWidth, 
                                    subLabelName="BEST LAP TIME", dataSource=self.dataSource, dataFieldName="MBESTLAPTIME", subLabelColor='#f8f',
                                    labelFontSize=timesFontSize, subLabelFontSize=timesLabelFontSize, labelFontName='Digital-7 Mono', labelColor='#f8f')
                                    
        bestTimeLabel.place()
        self.addItem(bestTimeLabel)
        
         # Delta Session Current
#        deltaSessionCLabel = DeltaTimeLabel(    master=self, posX=1150, posY=200, height=80, width=100, 
#                                                subLabelName="Delta Current", dataSource=self.dataSource,
#                                                labelFontSize=20, subLabelFontSize=10,
#                                                subLabelColor='#0f0',
#                                                timeRefFieldName="MBESTLAPTIME", timeFieldName="MCURRENTTIME")
#                                    
#        deltaSessionCLabel.place()
#        self.addItem(deltaSessionCLabel)



        batteryBar = BarLabel(  master=self, posX=10, posY=10, height=700, width=70, 
                                subLabelName="BAT", dataSource=self.dataSource, dataFieldName="MBOOSTAMOUNT",
                                subLabelFontSize=25, subLabelFontName = 'Digital-7 Mono',
                                barColor='#80FF80', subLabelColor='#80FF00')
                                    
        batteryBar.place()
        self.addItem(batteryBar)
        
        
        # Sector Gap 
        sectorGapTable = TableLabels(master=self, posX=90, posY=100, height=175, width=350, rows=1, columns=3, 
                                    dataSource=self.dataSource, dataFieldName="EXT_MSESSIONSECTORGAP", 
                                    labelColor='#8ff', labelFontSize=40,
                                    tableLabelName="SESSION GAP", tableLabelFontSize=30, tableLabelColor='#8ff',  tableLabelFontName='Digital-7 Mono',
                                    transFunc=lambda x: '--' if (x == -999999) else '{:.3f}'.format(x),
                                    colorTransFunc=lambda x: '#8ff' if (x == '--') else ('#f00' if (float(x) > 0.0) else '#0f0')
                                    )
        
        sectorGapTable.place()
        self.addItem(sectorGapTable)
        
        # Delta Lap
        deltaLapLabel = GenericLabel(   master=self, posX=90, posY=255, height=180, width=300, 
                                        subLabelName="DELTA SEC", subLabelFontSize=25, subLabelColor='#8ff', subLabelSide=tk.BOTTOM,
                                        dataSource=self.dataSource, dataFieldName="EXT_MSESSIONSECTORDELTA", defaultValue='0', labelFontName='Digital-7',
                                        labelFontSize=80, labelColor='#ffc90e', subLabelFontName='Digital-7',
                                        transFunc=lambda x: '-.---' if (x == -999999) else '{:.3f}'.format(x),
                                        colorTransFunc=lambda x: '#8ff' if (x == '-.---') else ('#f00' if (float(x) > 0.0) else '#0f0'))
        deltaLapLabel.place()
        self.addItem(deltaLapLabel)
        
        
        
        
        
        # Tyres Temp
        tyreTempTable = TableLabels(master=self, posX=475, posY=500, height=225, width=225, rows=2, columns=2, 
                                    dataSource=self.dataSource, dataFieldName="MTYRETREADTEMP", 
                                    labelColor='#8ff', labelFontSize=45,
                                    tableLabelName="TYRE TEMP", tableLabelFontSize=20, tableLabelColor='#8ff',  tableLabelFontName='Digital-7 Mono',
                                    transFunc=lambda x: str(int(x-273.15)).rjust(3) if (x > 0) else '--',
                                    colorTransFunc=lambda x: '#8ff' if (x == '--') else ('#8ff' if (float(x) < 130) else '#f00'))
        
        tyreTempTable.place()
        self.addItem(tyreTempTable)
        
        # Brakes Temp
        tyreTempTable = TableLabels(master=self, posX=700, posY=500, height=225, width=225, rows=2, columns=2, 
                                    dataSource=self.dataSource, dataFieldName="MBRAKETEMPCELSIUS", 
                                    labelColor='#ff80c0', labelFontSize=45,
                                    tableLabelName="BRAKE TEMP", tableLabelFontSize=20, tableLabelColor='#ff80c0', tableLabelFontName='Digital-7 Mono',
                                    transFunc=lambda x: str(int(x)).rjust(3) if (x > 0) else '--',
                                    colorTransFunc=lambda x: '#ff80c0' if (x == '--') else ('#ff80c0' if (float(x) < 350) else '#f00'))
        
        
        tyreTempTable.place()
        self.addItem(tyreTempTable)
        
        # Oil Temp
        oilTempLabel = GenericLabel(    master=self, posX=970, posY=580, height=75, width=260, 
                                        subLabelName="OIL TEMP   ",  subLabelColor='#FF8080', subLabelFontSize=25, subLabelSide=tk.LEFT, subLabelFontName='Digital-7 Mono',
                                        dataSource=self.dataSource, dataFieldName="MOILTEMPCELSIUS", defaultValue='0', 
                                        labelFontSize=45, labelColor='#ffc90e',  labelFontName='Digital-7 Mono',
                                        transFunc=lambda x: str(int(x)).rjust(3) if (x > 0) else '--')
        oilTempLabel.place()
        self.addItem(oilTempLabel)
        
        # Water Temp
        waterTempLabel = GenericLabel(  master=self, posX=970, posY=640, height=75, width=260, 
                                        subLabelName="WATER TEMP ",  subLabelColor='#FF8080', subLabelFontSize=25, subLabelSide=tk.LEFT, subLabelFontName='Digital-7 Mono',
                                        dataSource=self.dataSource, dataFieldName="MWATERTEMPCELSIUS", defaultValue='0', 
                                        labelFontSize=45, labelColor='#ffc90e',  labelFontName='Digital-7 Mono',
                                        transFunc=lambda x: str(int(x)).rjust(3) if (x > 0) else '--')
        waterTempLabel.place()
        self.addItem(waterTempLabel)
        
        
        # Pedals
        #pedalsFontSize       = 35
        pedalsLabelFontSize  = 25
        pedalsHeight          = 250
        pedalsWidth           = 30
        
        pX = 1200
        pY = 320
        
        # Throttle
        pedalBar = BarLabel(    master=self, posX=pX, posY=pY, height=pedalsHeight, width=pedalsWidth, 
                                subLabelName="T", dataSource=self.dataSource, dataFieldName="MTHROTTLE",
                                subLabelFontSize=pedalsLabelFontSize, subLabelFontName = 'Digital-7 Mono',
                                barColor='#80FF80', subLabelColor='#80FF80',
                                transFunc=lambda x: x*100)   
        pedalBar.place()
        self.addItem(pedalBar)
        
        # Brake
        pX = pX - pedalsWidth
        pedalBar = BarLabel(    master=self, posX=pX, posY=pY, height=pedalsHeight, width=pedalsWidth, 
                                subLabelName="B", dataSource=self.dataSource, dataFieldName="MBRAKE",
                                subLabelFontSize=pedalsLabelFontSize, subLabelFontName = 'Digital-7 Mono',
                                barColor='#FF8080', subLabelColor='#FF8080',
                                transFunc=lambda x: x*100)   
        pedalBar.place()
        self.addItem(pedalBar)
        
        # Clutch
        pX = pX - pedalsWidth
        pedalBar = BarLabel(    master=self, posX=pX, posY=pY, height=pedalsHeight, width=pedalsWidth, 
                                subLabelName="C", dataSource=self.dataSource, dataFieldName="MCLUTCH",
                                subLabelFontSize=pedalsLabelFontSize, subLabelFontName = 'Digital-7 Mono',
                                barColor='#8080FF', subLabelColor='#8080FF',
                                transFunc=lambda x: x*100)   
        pedalBar.place()
        self.addItem(pedalBar)
        
        
        # Damages
        
        # Crash State
        posX                = 200
        posY                = 570
        damHeight           = 40
        damWidth            = 250
        damFontSize         = 30
        damSubFonSize       = 20
        
        crashStateLabel = GenericLabel(     master=self, posX=posX, posY=posY, height=damHeight, width=damWidth, 
                                            subLabelName="CRASH STATE ", subLabelFontSize=damSubFonSize, subLabelColor='#FF8080', subLabelSide=tk.LEFT, labelFontName='Digital-7 Mono',
                                            dataSource=self.dataSource, dataFieldName="EXT_MCRASHSTATE", defaultValue='0',  subLabelFontName='Digital-7 Mono',
                                            labelFontSize=damFontSize, labelColor='#ffc90e',
                                            colorTransFunc=lambda x: '#ffc90e' if (x == 'NONE') else '#f00')
        crashStateLabel.place()
        self.addItem(crashStateLabel)
        
        # Aero Damage
        posY = posY + damHeight
        aeroDamLabel = GenericLabel(    master=self, posX=posX, posY=posY, height=damHeight, width=damWidth, 
                                        subLabelName="AERO DMG    ", subLabelFontSize=damSubFonSize, subLabelColor='#FF8080', subLabelSide=tk.LEFT, labelFontName='Digital-7 Mono',
                                        dataSource=self.dataSource, dataFieldName="MAERODAMAGE", defaultValue='0',  subLabelFontName='Digital-7 Mono',
                                        labelFontSize=damFontSize, labelColor='#ffc90e',
                                        transFunc=lambda x: '-' if (x < 0) else int(x*100),
                                        colorTransFunc=lambda x: '#ffc90e' if (x <= 0) else '#f00')
        aeroDamLabel.place()
        self.addItem(aeroDamLabel)
        
        # Engine Damage
        posY = posY + damHeight
        engineDamLabel = GenericLabel(      master=self, posX=posX, posY=posY, height=damHeight, width=damWidth, 
                                            subLabelName="ENGINE DMG  ", subLabelFontSize=damSubFonSize, subLabelColor='#FF8080', subLabelSide=tk.LEFT, labelFontName='Digital-7 Mono',
                                            dataSource=self.dataSource, dataFieldName="MENGINEDAMAGE", defaultValue='0',  subLabelFontName='Digital-7 Mono',
                                            labelFontSize=damFontSize, labelColor='#ffc90e',
                                            transFunc=lambda x: '-' if (x < 0) else int(x*100),
                                            colorTransFunc=lambda x: '#ffc90e' if (x <= 0) else '#f00')
        engineDamLabel.place()
        self.addItem(engineDamLabel)
        
        
        
        # Image Example
#        image = Image.open("../ext-resources/bmw_logo.bmp")
#        photo = ImageTk.PhotoImage(image)
#        
#        l = tk.Label(self, image=photo)
#        l.image = photo
#        l.place(x=800, y=130, height=195, width=195)
        

    def addItem(self, item):
        self.widgets.append(item)
        
    def refresh(self):
        # Refresh Data Components
        for i in self.widgets:
            i.refresh()
        
        # RefreskTK Gui
        self.update()

        
class BanWidget(tk.Frame):
    
    id = 0
    
    @staticmethod
    def getId():
        BanWidget.id = BanWidget.id + 1
        return BanWidget.id
    
    def __init__(self, master=None, posX=0, posY=0, height=10, width=10):
        tk.Frame.__init__(self, master)
        
        self.id     = BanWidget.getId()
        self.posX   = posX
        self.posY   = posY
        self.height = height
        self.width  = width
        
        if(DEBUG):
            self.configure(borderwidth=5, relief=tk.GROOVE)
            
    

    def place(self):
        tk.Frame.place(self, x=self.posX, y=self.posY, height=self.height, width=self.width)
        
        
    def refresh(self):
        None
        

class GenericLabel(BanWidget):
    
    def __init__(self, master=None, posX=0, posY=0, height=10, width=10, subLabelName=None, dataSource=None, dataFieldName=None, dataFieldIndex=0, defaultValue=None, labelFormat=None, labelFontName=None, labelFontSize=20, subLabelFontSize=5, labelColor='#fff', subLabelColor='#fff', subLabelFontName=None, subLabelSide=tk.BOTTOM, transFunc=None, colorTransFunc=None):
        
        BanWidget.__init__(self, master, posX, posY, height, width)
        
        # Data Source
        self.dataSource     = dataSource
        self.dataFieldName  = dataFieldName
        self.dataFieldIndex = dataFieldIndex
        self.defaultValue   = defaultValue
        
        # Tk
        self.master             = master
        self.labelVar           = tk.StringVar()
        self.subLabelName       = subLabelName
        self.labelFontSize      = labelFontSize;
        self.subLabelFontSize   = subLabelFontSize;
        self.labelColor         = labelColor
        self.subLabelColor      = subLabelColor
        self.labelFormat        = labelFormat
        self.subLabelSide       = subLabelSide
        self.labelFontName      = labelFontName
        self.subLabelFontName   = subLabelFontName
        self.colorTransFunc     = colorTransFunc
        
        
        # Misc
        self.transFunc      = transFunc
        
        # Label Var
        self.labelVar.set(self.defaultValue)
        
        self.draw()
        
    def draw(self):
        if(DEBUG):
            self.configure(borderwidth=5, relief=tk.GROOVE)
        
        if(self.labelFontName != None):
            mainLabelFont   = tkFont.Font(family=self.labelFontName, size=self.labelFontSize)
        else:
            mainLabelFont   = tkFont.Font(size=self.labelFontSize)
        
        self.mainLabel  = tk.Label(self, textvariable=self.labelVar, background='#000', foreground=self.labelColor, font=mainLabelFont)
        
        if(self.subLabelSide == tk.LEFT or self.subLabelSide == tk.RIGHT):
            if(self.subLabelSide == tk.LEFT):
                self.mainLabel.pack(fill=tk.BOTH, side=tk.RIGHT, expand = 1) # , expand = 1
            else:
                self.mainLabel.pack(fill=tk.BOTH, side=tk.LEFT, expand = 1) # , expand = 1
        else:
            if(self.subLabelSide == tk.TOP):
                self.mainLabel.pack(fill=tk.BOTH, side=tk.BOTTOM, expand = 1) #, expand = 1
            else:
                self.mainLabel.pack(fill=tk.BOTH, side=tk.TOP, expand = 1) #, expand = 1
        
        
        if(DEBUG):
            self.configure(borderwidth=5, relief=tk.GROOVE)
            
        if(self.subLabelName != None):
            if(self.subLabelFontName != None):
                subLabelFont    = tkFont.Font(family=self.subLabelFontName, size=self.subLabelFontSize)
            else:
                subLabelFont    = tkFont.Font(size=self.subLabelFontSize)
                
            self.subLabel   = tk.Label(self, text=self.subLabelName, background='#000', foreground=self.subLabelColor, font=subLabelFont)
            #self.subLabel.pack(fill=tk.BOTH, expand=1)
            
            if(self.subLabelSide == tk.LEFT or self.subLabelSide == tk.RIGHT):
                self.subLabel.pack(fill=tk.Y, side=self.subLabelSide) # , expand = 1
            else:
                self.subLabel.pack(fill=tk.X, side=self.subLabelSide) #, expand = 1
                
            if(DEBUG):
                self.subLabel.configure(borderwidth=5, relief=tk.GROOVE)
        
    # Update Label var with Source Data
    def refresh(self):
        val = self.dataSource.getField(self.dataFieldName)
        
        if(isinstance(val, (list))):
            val = self.dataSource.getField(self.dataFieldName)[self.dataFieldIndex]
        
        if(val == None):
            self.labelVar.set(self.defaultValue)
        else:
            if(self.transFunc != None):
                val = self.transFunc(val)
                
            if(self.labelFormat != None):
                val = self.labelFormat.format(val)
            
            self.labelVar.set(str(val))
            
        if(self.colorTransFunc != None):
            color = self.colorTransFunc(val)
            self.mainLabel.configure(foreground=color)
                
class TimeLabel(GenericLabel):
    def __init__(self, master=None, posX=0, posY=0, height=10, width=10, subLabelName=None, dataSource=None, dataFieldName=None, dataFieldIndex=0, defaultValue=None, labelFormat=None, labelFontName=None, labelFontSize=20, subLabelFontSize=5, labelColor='#fff', subLabelColor='#fff', subLabelFontName=None, subLabelSide=tk.BOTTOM, transFunc=None, colorTransFunc=None, condColor='#f00'):
        GenericLabel.__init__(self, master, posX, posY, height, width, subLabelName, dataSource, dataFieldName, dataFieldIndex, defaultValue, labelFormat, labelFontName, labelFontSize, subLabelFontSize, labelColor, subLabelColor, subLabelFontName, subLabelSide, transFunc, colorTransFunc)
        
        self.condColor = condColor
        
    # Update Label var with Source Data
    def refresh(self):
        val = self.dataSource.getField(self.dataFieldName)
        
        
        if(isinstance(val, (list))):
            if(val[1] == 1):
                self.mainLabel.configure(foreground=self.condColor)
            else:
                self.mainLabel.configure(foreground=self.labelColor)
            
            val = val[0]
        
        if(val == None or val == -1):
            self.labelVar.set("--:--:---")
        else:
            if(self.transFunc != None):
                val = self.transFunc(val)
            
            dec  = int((val % 1)*1000)
            r    = val
            
            mins = int(r / 60)
            secs = int(r % 60)
            
            self.labelVar.set('{:02d}:{:02d}:{:03d}'.format(mins, secs, dec))

class BarLabel(BanWidget):

    def __init__(self, master=None, posX=0, posY=0, height=10, width=10, subLabelName=None, dataSource=None, dataFieldName=None, defaultValue=None, subLabelFontSize=5, barColor='#0f0', subLabelColor='#fff', subLabelFontName=None, transFunc=None):
        BanWidget.__init__(self, master, posX, posY, height, width)
        
        # Data Source
        self.dataSource         = dataSource
        self.dataFieldName      = dataFieldName
        self.defaultValue       = defaultValue
        
        # Tk
        self.master             = master
        self.barVar             = tk.DoubleVar()
        self.barColor           = barColor
        self.subLabelName       = subLabelName
        self.subLabelFontSize   = subLabelFontSize;
        self.subLabelColor      = subLabelColor
        self.subLabelFontName   = subLabelFontName;
        
        # Misc
        self.transFunc          = transFunc
        
        self.draw()
        
    def draw(self):
        if(DEBUG):
            self.configure(borderwidth=5, relief=tk.GROOVE)
        
        s = ttk.Style() # s.theme_names() To show availables
        # print s.theme_names():  ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        #s.theme_use('classic') 
        s.theme_use('classic') 

        # WARN: Posible name colission with severals BarLabels
        styleId = 'barLabel_'+str(self.id)+'.Vertical.TProgressbar'
        s.configure(styleId, foreground='green', background=self.barColor, troughcolor ='#808080')
            
        self.progressBar = ttk.Progressbar(self, orient='vertical', mode='determinate', variable=self.barVar, style=styleId)
        
        self.progressBar.pack(fill=tk.BOTH, expand=1)

        if(self.subLabelName != None):
            if(self.subLabelFontName != None):
                subLabelFont    = tkFont.Font(family=self.subLabelFontName, size=self.subLabelFontSize)
            else:
                subLabelFont    = tkFont.Font(size=self.subLabelFontSize)
                
            self.subLabel   = tk.Label(self, text=self.subLabelName, background='#000', foreground=self.subLabelColor, font=subLabelFont)
            #self.subLabel.pack(fill=tk.BOTH, expand=1)
            self.subLabel.pack(fill=tk.X)
            print self.subLabelName

            if(DEBUG):
                self.subLabel.configure(borderwidth=5, relief=tk.GROOVE)
            
            
    # Update Label var with Source Data
    def refresh(self):
        val = self.dataSource.getField(self.dataFieldName)

        if(val == None):
            self.barVar.set(float(0))
        else:
            if(self.transFunc != None):
                val = self.transFunc(val)
            
            self.barVar.set(float(val))


class TableLabels(BanWidget):
    def __init__(self, master=None, posX=0, posY=0, height=10, width=10, rows=0, columns=0, dataSource=None, dataFieldName=None, defaultValue='-', labelFontSize=5, tableLabelName=None, tableLabelFontSize=5, labelColor='#fff', tableLabelColor='#fff', tableLabelFontName=None, transFunc=None, colorTransFunc=None):
        BanWidget.__init__(self, master, posX, posY, height, width)
        
        
        self.rows                   = rows
        self.columns                = columns
        self.dataFieldName          = dataFieldName
        
        # Data Source
        self.dataSource             = dataSource
        self.dataFieldName          = dataFieldName
        self.defaultValue           = defaultValue
        
        # Tk
        self.master                 = master
        self.labelFontSize          = labelFontSize
        self.labelColor             = labelColor

        self.tableLabelName         = tableLabelName
        self.tableLabelFontSize     = tableLabelFontSize;
        self.tableLabelColor        = tableLabelColor
        self.tableLabelFontName     = tableLabelFontName
        self.colorTransFunc         = colorTransFunc
        
        # Misc
        self.transFunc            = transFunc
        
        self.items                = []
        self.draw()
        
    def draw(self):
        
        tableFrame = tk.Frame(self)
        tableFrame.pack(fill=tk.BOTH, expand = 1, side = tk.BOTTOM)
        
        if(DEBUG):
            tableFrame.configure(borderwidth=5, relief=tk.GROOVE, background='#123')
            
        if(self.dataFieldName != None):
        
            # Create Label Widgets
            for r in range(0, self.rows):
                for c in range(0, self.columns):
                    tyreLabel = GenericLabel(   master=tableFrame,
                                                dataSource=self.dataSource, dataFieldName=self.dataFieldName, dataFieldIndex=((r*self.columns)+c), defaultValue=self.defaultValue,
                                                labelFontSize=self.labelFontSize, labelColor=self.labelColor, labelFontName=self.tableLabelFontName, transFunc=self.transFunc, colorTransFunc=self.colorTransFunc)
                    tyreLabel.grid(row=r, column=c, sticky=(tk.W,tk.E,tk.N,tk.S)) 
                    
                    self.items.append(tyreLabel)
                    
                    if(DEBUG):
                        tyreLabel.configure(borderwidth=5, relief=tk.GROOVE, background='#fff')
            
            # WTF Si no relleno con otro elemento una fila mas,  el ultimo elemento de la tabla sale mas pequeno si la tabla tiene etiqueta ??
            tmpLabel=tk.Label(tableFrame,background='#000')
            tmpLabel.grid(row=self.rows+1, column=0, sticky=(tk.W,tk.E), columnspan=self.columns) 
            
#            if(DEBUG):
#                tmpLabel.configure(borderwidth=5, relief=tk.GROOVE)
            
            for r in range(0, self.rows):
                tableFrame.rowconfigure(r, weight=1)
                
            for c in range(0, self.columns):
                tableFrame.columnconfigure(c, weight=1)
        
        if(self.tableLabelName != None):
            if(self.tableLabelFontName != None):
                tableLabelFont    = tkFont.Font(family=self.tableLabelFontName, size=self.tableLabelFontSize)
            else:
                tableLabelFont    = tkFont.Font(size=self.tableLabelFontSize)
                
            self.tableLabel   = tk.Label(self, text=self.tableLabelName, background='#000', foreground=self.tableLabelColor, font=tableLabelFont)
            self.tableLabel.pack(fill=tk.BOTH, side = tk.TOP) # side= tk.BOTTOM, LEFT, RIGHT, TOP
            
#            if(DEBUG):
#                self.tableLabel.configure(borderwidth=5, relief=tk.GROOVE)
    
    def refresh(self):
        for i in self.items:
            i.refresh()
            
        
class PCarsDataSource():
    
    def __init__(self):
        # Inifializar WS
        self.jsonData           = None
        self.url                = 'http://localhost:8080/getdata'
        self.json_dataFields    = json.dumps({"fields": ["MGEAR", "MRPM", "MSPEED", "MFUELLEVEL", 
                                                         "EXT_MCURRENTTIME",  "MBESTLAPTIME", "EXT_MLASTLAPTIME",
                                                         "MBOOSTAMOUNT", "MFUELLEVEL", "MTYRETREADTEMP", "MBRAKETEMPCELSIUS", 
                                                         "MCARNAME", "MOILTEMPCELSIUS", "MWATERTEMPCELSIUS",
                                                         "EXT_MSESSIONSECTORGAP", "EXT_MSESSIONSECTORDELTA", "EXT_MPOSITION",
                                                         "MTHROTTLE", "MCLUTCH", "MBRAKE",
                                                         "MAERODAMAGE", "MENGINEDAMAGE", "EXT_MCRASHSTATE"]})                                                         
                                                         
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.URL, self.url)
        self.curl.setopt(pycurl.POST, 1)
        self.curl.setopt(pycurl.POSTFIELDS, self.json_dataFields)
        
        if(DEBUG):
            self.curl.setopt(pycurl.VERBOSE, 1)
        
    def getField(self, fieldName):
        if (self.jsonData == None):
            return None
        else:
            return self.jsonData["data"][fieldName]
        
    def update(self):
        # Rest Call updating Data Source values
        
        # Option 1: requests library. So slow! 1 second per request
        #start       = time.time()
        #response    = requests.post(self.url, data=self.json_dataFields, verify=False)
        #print("Time Rest Request: "+ str(time.time()-start))
        #data_json = json.loads(response.content)
        
            
        # Option 2: pycurl
        buffer  = StringIO()
        self.curl.setopt(self.curl.WRITEDATA, buffer)
        self.curl.perform()
        
        # Update Data Source
        self.jsonData = json.loads(buffer.getvalue())
        buffer.close()
        #c.close()
        #print self.jSonData
        
        return
    
    
#def refreshData(dataSrc):
#    while True:
#        dataSrc.update()
#        time.sleep(DATA_REFRESH_DELAY_MILLIS/1000)
        
def refreshGui():
    
    # Data refresh
    if(DEBUG):
        start = time.time()
        
    DATA.update()
    
    if(DEBUG):
        print("Time Get Data : "+ str(time.time()-start))
    
    if(DEBUG):
        start = time.time()
        
    # Gui refresh
    GUI.refresh()
    
    if(DEBUG):
        print("Time Refresh Gui : "+ str(time.time()-start))
    
    GUI.after(GUI_REFRESH_DELAY_MILLIS, refreshGui)
    
        

# Constants 
GUI_REFRESH_DELAY_MILLIS = 50

# Global Vars
GUI     = None
DATA    = None
DEBUG   = False 

#######
# Main
#######

if __name__ == "__main__":
    
    win = Win()
    win.geometry('%dx%d+%d+%d' % (1280, 720, 350, 150))

    DATA = PCarsDataSource()
    GUI  = Application(master=win, dataSource=DATA)
    GUI.master.title('BanPCars Display')
    
    #t = threading.Thread(target=refreshData, args=[dataSrc])
    #t.start()
    
    GUI.after(GUI_REFRESH_DELAY_MILLIS, refreshGui)
    win.mainloop()
    

