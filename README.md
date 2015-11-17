# ardu-setup-tool.py
Front-end tool to set arguments for arduino-like compiler.

####TODO list
- [x] command-line interface
- [x] all arguments are optional and configurable from GUI
- [x] search for serial ports on Windows platform
- [ ] full Linux platform support
- [ ] search for serial ports on Linux platform
- [ ] default settings saved to/loaded from a file
- [ ] full arduino command-line interface support
- [ ] select list for board specifications
- [ ] write a proper manual
- [ ] natively support other compilers and uploaders (avrdude, ...)
  - [ ] It will mean rename, fork or new repository

##ARDU-SETUP-TOOL

###NAME
ardu-setup-tool - Front-end tool to set arguments for arduino-like compiler.

###SYNOPSIS
*ardu-setup-tool.py*

*ardu-setup-tool.py* [*--arduino __arduinopath__] [*--verify*|*--upload*] [*--board* __package__:__arch__:__board__[:__parameters__]] [*--port* __portname__] [*--file* __FILE.ino__]

###DESCRIPTION

The *ardu-setup-tool* is a front-end for Arduino CLI and allows setup mutable arguments before compile or upload the program board.

The main purpose of this tool is the direct compilation and uploading of arduino projects in an integrated development environment that allows the execution of commands.

###ACTIONS

*--verify*::
	Build the sketch

*--upload*::
	Build and upload the sketch

###OPTIONS

*--arduino* __arduinopath__::
	Path to arduino executable
	
*--board* __package__:__arch__:__board__[:__parameters__]::
	Identification of the development board / CPU
	
*--port* __portname__::
	Serial port to perform upload of the program
	
*--file* __filename__::
	Source code file name
