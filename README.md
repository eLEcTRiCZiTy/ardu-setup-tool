# ardu-setup-tool.py
Front-end tool to set arguments for arduino-like compiler.

####TODO list
- [x] command-line interface
- [x] all arguments are optional and configurable from the GUI
- [x] discover the serial ports on Windows
- [ ] full Linux platform support
- [ ] discover the serial ports on Linux
- [ ] default settings saved to/loaded from a file
- [ ] full arduino command-line interface support
- [ ] select list for board specifications
- [ ] write a proper manual
- [ ] natively support other compilers and uploaders (avrdude, ...)
  - [ ] It will mean rename, fork or new repository

##ARDU-SETUP-TOOL

###NAME
ardu-setup-tool - Front-end tool to set arguments for an arduino-like compiler.

###SYNOPSIS
*ardu-setup-tool.py*

*ardu-setup-tool.py* [*--arduino __arduinopath__] [*--verify*|*--upload*] [*--board* __package__:__arch__:__board__[:__parameters__]] [*--port* __portname__] [*--file* __FILE.ino__]

###DESCRIPTION

The *ardu-setup-tool* is a front-end for the Arduino command-line interface (CLI) and allows setup mutable arguments before compile or upload to the development board.

The main purpose of this tool is the direct compilation and uploading of an arduino projects in an integrated development environment (IDE) that allows the execution of commands.

###ACTIONS

*--verify*::
	Build the program

*--upload*::
	Build and upload the program

###OPTIONS

*--arduino* __arduinopath__::
	Path to the arduino executable
	
*--board* __package__:__arch__:__board__[:__parameters__]::
	Identification of the development board / CPU
	
*--port* __portname__::
	Serial port to perform upload of the program
	
*--file* __filename__::
	File name of the source code
