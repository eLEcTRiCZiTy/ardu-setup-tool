#Front-end tool to set arguments for arduino-like compiler.
#Copyright (C) 2015  Jan Vojnar

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


from Tkinter import Tk, Frame, LabelFrame, Label, Text, Listbox, Button, Entry, StringVar, Scrollbar
from Tkinter import LEFT, RIGHT, N, S, W, E, X, Y, BOTH, END, GROOVE, BOTTOM, ACTIVE, WORD, DISABLED
import tkFileDialog
import tkSimpleDialog
import subprocess
import sys
import argparse


from platform import system
WINDOWS = "Windows"

PROJECT_TEXT = "eLEcTRiCZiTy's Ardu-Setup-Tool"
COPYRIGHT_TEXT = "Copyright (C) 2015  Jan Vojnar"
SHORTABOUT_TEXT= """
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it under
certain conditions;

LICENSE file was not found.
For a copy of the GNU General Public License Version 3
see http://www.gnu.org/licenses/gpl-3.0.html."""

#--Read Windows COM ports-----------------------------------------------
#TODO Linux support
import _winreg as winreg
import itertools
import unicodedata

def serial_ports():
	ports = []
	devices = []
	pathports = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
	pathdevices = 'SYSTEM\\CurrentControlSet\\Enum\\USB'
	try:
		keyports = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pathports)
	except WindowsError:
		raise IterationError
	try:
		keydevs = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pathdevices)
	except WindowsError:
		raise IterationError
	for i in xrange(winreg.QueryInfoKey(keyports)[1]):
		val = winreg.EnumValue(keyports, i)
		ports.append( (str(val[1]), str(val[0])) )
	for j in xrange(winreg.QueryInfoKey(keydevs)[0]):
		skeyname = winreg.EnumKey(keydevs, j)
		skey = winreg.OpenKey(keydevs,skeyname)
		for sj in xrange(winreg.QueryInfoKey(skey)[0]):
			sskeyname = winreg.EnumKey(skey, sj)
			sskey = winreg.OpenKey(skey,sskeyname)
			for ssj in xrange(winreg.QueryInfoKey(sskey)[1]):
				ssval = winreg.EnumValue(sskey, ssj)
				name = ssval[0]
				if 'FriendlyName' == name:
					devices.append( unicodedata.normalize('NFKD',ssval[1]).encode('ascii', 'ignore'))
	result = []
	for p in ports:
		for s in devices:
			if p[0] in s:
				result.append((p[0], (p[1]), (s)))
	return result
	
	
class AboutDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		self.resizable(width=False, height=False)
		frametop = Frame(master)
		Label(frametop, text="Project: "+PROJECT_TEXT).pack(anchor=W)
		Label(frametop, text=COPYRIGHT_TEXT).pack(anchor=W)
		frametop.pack(fill=X)
		frametext = Frame(master)
		scrollbar = Scrollbar(frametext)
		scrollbar.pack(side=RIGHT, fill=Y)
		text = Text(frametext, width=75, wrap=WORD, yscrollcommand=scrollbar.set)
		try:
			f = open("LICENSE","r") #opens file with name of "test.txt"
			text.insert(END, f.read())
		except(IOError):
			text.insert(END, SHORTABOUT_TEXT)
		scrollbar.config(command=text.yview)
		text.pack(fill=X)
		frametext.pack(fill=X)
		
	def buttonbox(self):
		box = Frame(self)
		w = Button(box, text="Close", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		box.pack(side=BOTTOM)
		
class ArduinoSetup():
	def __init__(self, master, args):
		self.master = master
		self.master.minsize(width=360, height=600)
		self.master.title(PROJECT_TEXT)
		
		#GUI PROPS
		self.padXOut = 5
		self.padYOut = 3
		self.padXIn = 5
		self.padYIn = 3
		self.frameRelief = GROOVE
		self.frameBorder = 2
		self.infoFG = "teal"
		self.selectBG = "teal"
		self.textBG = "white"
		self.errorBG = "red"
		
		self.vAction = StringVar()
		if args.verify:
			self.vAction.set("--verify")
		elif args.upload:
			self.vAction.set("--upload")
		else:
			self.vAction.set("")
			
		self.verify = args.verify
		self.upload = args.upload
		self.vPath = StringVar()
		self.vPath.set(args.arduino)
		self.vBoard = StringVar()
		self.vBoard.set(args.board)
		self.vPort = StringVar()
		self.vPort.set(args.port)
		self.vFile = StringVar()
		self.vFile.set(args.file)
		
		#GUI WIDGETS
		self.errorPath = True
		self.errorBoard = True
		self.errorPort = True
		self.errorFile = True
		
		self.enablePath = True
		self.enableBoard = True
		self.enablePort = True
		self.enableFile = True
		
		if self.vPath.get() != "": self.enablePath = False
		if self.vBoard.get() != "": self.enableBoard = False
		if self.vPort.get() != "": self.enablePort = False
		if self.vFile.get() != "": self.enableFile = False
		
		if self.enablePath:
			optArdu = {}
			optArdu['defaultextension'] = '.exe'
			optArdu['filetypes'] = [('exe files', '.exe'), ('all files', '.*')]
			#options['initialdir'] = 'C:\\'
			optArdu['initialfile'] = 'arduino.exe'
			optArdu['parent'] = master
			optArdu['title'] = 'Open arduino.exe'
			
			if(system()==WINDOWS):
				pathexample="""Example: C:/Program Files/Arduino/arduino.exe"""
			else:
				pathexample="""Location of arduino executable"""
			
			self.vcmdPath = master.register(self.validatePath)
			self.framePath = LabelFrame(master, text="Arduino.exe path:", bd=self.frameBorder, relief=self.frameRelief)
			self.entryPath = Entry(self.framePath, bg=self.textBG, validate='all', validatecommand=(self.vcmdPath, '%P'), textvar=self.vPath, selectbackground=self.selectBG)
			self.entryPath.pack(fill=X, padx=self.padXIn, pady=self.padYIn)
			self.buttonPath = Button(self.framePath, text="Find arduino...", command=lambda: self.openPath(optArdu, self.vPath))
			self.buttonPath.pack(fill=X, padx=self.padXIn, pady=self.padYIn)
			self.labelPathInfo = Label(self.framePath, fg=self.infoFG,
			text=pathexample)
			self.labelPathInfo.pack(fill=X)
			self.framePath.pack(fill=X, padx=self.padXOut, pady=self.padYOut)
			
		if self.enableBoard:
			self.vcmdBoard = master.register(self.validateBoard)
			self.frameBoard = LabelFrame(master, text="Board:", bd=self.frameBorder, relief=self.frameRelief)
			self.entryBoard = Entry(self.frameBoard, bg=self.textBG, validate='all', validatecommand=(self.vcmdBoard, '%P'), textvar=self.vBoard, selectbackground=self.selectBG)
			self.entryBoard.pack(fill=X, padx=self.padXIn, pady=self.padYIn)
			self.labelBoardInfo = Label(self.frameBoard, fg=self.infoFG, 
			text="""package:arch:board[:parameters]""")
			self.labelBoardInfo.pack(fill=X, padx=self.padXIn, pady=self.padYIn)
			self.textBoardExample = Text(self.frameBoard, fg=self.infoFG, width = 50, height=6)
			self.textBoardExample.insert(END,"""Packages: arduino, sparkfun, ...
Arch: avr, sam, ...
Boards: uno, mega, promicro, ...
Parameters: cpu=CPU, ...
Example:	 arduino:avr:nano:cpu=atmega168
	 sparkfun:avr:promicro:cpu=8MHzatmega32U4""")
			self.textBoardExample.config(state=DISABLED)
			self.textBoardExample.pack(fill=X, padx=self.padXIn, pady=self.padYIn)
			
			self.frameBoard.pack(fill=X, padx=self.padXOut, pady=self.padYOut)
			
		if self.enablePort:
			self.framePort = LabelFrame(master, text="Port:", bd=self.frameBorder, relief=self.frameRelief)
			if (system() == WINDOWS):
				self.ports = serial_ports()
				#only for testing
				#self.ports.append(("COM", "Device 123"))
				self.frameListbox = Frame(self.framePort)
				scrollbar = Scrollbar(self.frameListbox)
				scrollbar.pack(side=RIGHT, fill=Y)
				self.listboxPort = Listbox(self.frameListbox, height=2, bg=self.textBG, selectbackground=self.selectBG, yscrollcommand=scrollbar.set)
				scrollbar.config(command=self.listboxPort.yview)
				self.listboxPort.insert(END, *self.ports)
				self.listboxPort.pack(fill=BOTH, expand=1)
				self.listboxPort.bind('<<ListboxSelect>>', self.portSelected)
				self.frameListbox.pack(fill=BOTH, expand=1, padx=self.padXIn, pady=self.padYIn)
				self.labelPortInfo = Label(self.framePort, fg=self.infoFG, text="port | port name | device name")
				self.labelPortInfo.pack(side=BOTTOM, fill=X, padx=self.padXIn, pady=self.padYIn)
			else:
				self.vcmdPort = master.register(self.validatePort)
				self.entryPort = Entry(self.framePort, bg=self.textBG, validate='all', validatecommand=(self.vcmdPort, '%P'), textvar=self.vPort, selectbackground=self.selectBG)
				self.entryPort.pack(fill=X, padx=self.padXIn, pady=self.padYIn)
				self.labelPortInfo = Label(self.framePort, fg=self.infoFG, text="""Example: /dev/ttyUSB0""")
				self.labelPortInfo.pack(side=BOTTOM, fill=X, padx=self.padXIn, pady=self.padYIn)
			self.framePort.pack(fill=BOTH, expand=1, padx=self.padXOut, pady=self.padYOut)
			
		
		if self.enableFile:
			optFile = {}
			optFile['defaultextension'] = '.ino'
			optFile['filetypes'] = [('arduino source files', '.ino'),('all files', '.*')]
			#options['initialdir'] = 'C:\\'
			optFile['initialfile'] = ''
			optFile['parent'] = master
			optFile['title'] = 'Open arduino source code'
			
			self.vcmdFile = master.register(self.validateFile)
			self.frameFile = LabelFrame(master, text="Source code path:", bd=self.frameBorder, relief=self.frameRelief)
			self.entryFile = Entry(self.frameFile, bg=self.textBG, validate='all', validatecommand=(self.vcmdFile, '%P'), textvar=self.vFile, selectbackground=self.selectBG)
			self.entryFile.pack(fill=X, padx=self.padXIn, pady=self.padYIn)
			self.buttonFile = Button(self.frameFile, text="Find source code...", command=lambda: self.openPath(optFile, self.vFile))
			self.buttonFile.pack(fill=X, padx=self.padXIn, pady=self.padYIn)
			self.labelFileInfo = Label(self.frameFile, fg=self.infoFG,
			text="""Source code to compile (file extension .ino)""")
			self.labelFileInfo.pack(fill=X)
			self.frameFile.pack(fill=X, padx=self.padXOut, pady=self.padYOut)
		
		#BOTTOM side items (reversed order)
		self.frameAbout = Frame(master, cursor="heart")
		self.labelAbout=Label(self.frameAbout, text=COPYRIGHT_TEXT, fg=self.infoFG)
		self.labelAbout.pack(side=LEFT)
		self.buttonAbout=Button(self.frameAbout, text="About app...", fg=self.infoFG, command=self.openAboutBox, borderwidth=1)
		self.buttonAbout.pack(side=RIGHT)
		self.frameAbout.pack(side=BOTTOM, fill=X, padx=self.padXOut, pady=self.padYOut)
		
		if self.vAction.get() != "":
			self.buttonContinue = Button(master, text="Continue", command=self.doContinue)
			self.buttonContinue.pack(fill=X, padx=self.padXOut, pady=self.padYOut)
		else:
			if self.verify is False:
				self.buttonVerify = Button(master, text="Verify", command=self.doVerify)
				self.buttonVerify.pack(side=BOTTOM, fill=X, padx=self.padXOut, pady=self.padYOut)
			if self.upload is False:
				self.buttonUpload = Button(master, text="Upload", command=self.doUpload)
				self.buttonUpload.pack(side=BOTTOM, fill=X, padx=self.padXOut, pady=self.padYOut)
		
	def openAboutBox(self):
		dialog = AboutDialog(self.master)

	def portSelected(self, P):
		self.errorPort = False
		self.listboxPort.config(bg=self.textBG)
		try:
			porti = map(int, self.listboxPort.curselection())[0]
			self.vPort.set(self.ports[porti][0])
		except (IndexError):
			self.errorPort = True
			self.listboxPort.config(bg=self.errorBG)
		
	#only for linux
	def validatePort(self, P):
		if self.vPort.get() == "" and P == "":
			self.errorPort = True
			self.entryPort.config(bg=self.errorBG)
			return False
		else:
			self.errorPort = False
			self.entryPort.config(bg=self.textBG)
			return True
	
	def validatePath(self, P):
		if self.vPath.get() == "" and P == "":
			self.errorPath = True
			self.entryPath.config(bg=self.errorBG)
			return False
		else:
			self.errorPath = False
			self.entryPath.config(bg=self.textBG)
			return True
	
	def validateBoard(self, P):
		if self.vBoard.get() == "" and P == "":
			self.errorBoard = True
			self.entryBoard.config(bg=self.errorBG)
			return False
		else:
			self.errorBoard = False
			self.entryBoard.config(bg=self.textBG)
			return True
	
	def validateFile(self, P):
		if self.vFile.get() == "" and P == "":
			self.errorFile = True
			self.entryFile.config(bg=self.errorBG)
			return False
		else:
			self.errorFile = False
			self.entryFile.config(bg=self.textBG)
			return True
	
	def openPath(self, opt, sv):
		sv.set(tkFileDialog.askopenfilename(**opt))
		
	def doVerify(self):
		self.vAction.set("--verify")
		self.doContinue()
		
	def doUpload(self):
		self.vAction.set("--upload")
		self.doContinue()
		
	def doContinue(self):
		if self.enablePath:
			self.validatePath(self.vPath.get())
		if self.enableBoard:
			self.validateBoard(self.vBoard.get())
		if self.enableFile:
			self.validateFile(self.vFile.get())
		if self.enablePort and system() != WINDOWS:
			print self.vPort.get()
			self.validatePort(self.vPort.get())
		self.doAction()
		
	def doAction(self):
		result = 3
		if (self.errorPath or self.errorBoard or self.errorPort or self.errorFile): return
		command = ""
		command += self.vPath.get()
		command += " " + self.vAction.get()
		command += " --board " + self.vBoard.get()
		command += " --port " + self.vPort.get()
		command += " --verbose"
		command += " " + self.vFile.get()
		print "command:", command
		result = subprocess.call(arduinoCommand, shell=True)
		
		if (result == 0):
			print "{}: Success.".format(self.vPath.get())
			quit(0)
		elif (result == 1):
			print "{}: Build failed or upload failed".format(self.vPath.get())
			quit(1)
		elif (result == 2):
			print "{}: Sketch not found".format(self.vPath.get())
			quit(2)
		elif (result == 3):
			print "{}: Invalid (argument for) commandline option".format(self.vPath.get())
			quit(3)
		
if __name__ == "__main__":
	#ARGUMENT PARSER
	parser = argparse.ArgumentParser(description="Setup Tool")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--verify", action="store_true", help="only verify(build) source code")
	group.add_argument("--upload", action="store_true", help="verify(build) and upload source code")
	parser.add_argument("--arduino", type=str, default="", help="specify arduino.exe path")
	parser.add_argument("--board", type=str, default="", help="specify package:arch:board[:parameters]")
	parser.add_argument("--port", type=str, default="", help="specify serial port")
	parser.add_argument("--file", type=str, default="", help="source file")
	args = parser.parse_args()

	root = Tk()	
	gui = ArduinoSetup(root, args)
	root.mainloop()
