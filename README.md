# new-ESP32-platform-firmware
Experimental try at making esp idf v4.0 micropython project

## Supported environments
* Linux
* Mac OS
* (Maybe WSL 2 on Windows?)

## Setup
1. Clone the repo  
2. run git submodule update --init --recursive  
3. run install.sh  
4. source setenv.sh to get all the right environment variables
5. ???  
6. Profit  

## Build
* ./build.sh for iteratively building changed code
* ./clean.sh to clean build cache
* ./flash.sh to flash to a badge
* ./monitor.sh to open serial monitor

## Configuration
* ./config.sh

## Changes over old firmware
1. python module bridges (e.g. modi2c.c) are now placed inside the driver folder. So the micropython folder stays untouched. You need to register the file for it to be include in the build. More on this later.  
2. Init in platform.c are now also handled with a generator so you only need to register the init function with cmake. When properly done no dummy init functions are necessary when the driver is disabled.  
3. All drivers are now compiled with cmake.  
4. uPy is now based on upstream micropython.    
5. Bluetooth support is enabled (BLE only for now).    

## Registering a new driver
A working example can be found in de driver_bus_i2c folder.  
In CMakelists.txt added all sources necessary for your driver and requirement for micropython and any other module.  
If there is configuration option to disable the driver wrap you srcs in an cmake if statement.  
To register the micropython bindings append your files/name as follows:
 >set(EXTMODS "${EXTMODS}" "${mods}" CACHE INTERNAL "")  
 >set(EXTMODS_NAMES "${EXTMODS_NAMES}" "${mod_name}" CACHE INTERNAL "")  
 
 where mods is all the full filepaths containing micropython bindings and mod_name contains the module name
 in the module files all includes not from uPy should be wrapped in #ifndef NO_QSTR 
To register driver with an init function register as followed:  
 >set(EXTMODS_INIT "${EXTMODS_INIT}" "\"${mod_name}\"@\"${mod_register}\"^" CACHE INTERNAL "")  
 
 where mod_register is the register message 
 This can also be done in a cmake if statement to not register the init/module when the driver is disabled.



## Issues
1. QSTR regeneration is currently not performed and requires a idf.py clean
2. uPy configuration options need to be readded.
3. QSTR generation is still done by calling the uPy makefile this should be ported to cmake but is a bit of black magic
4. Some parts of micropython still need to be compiled with certain flags set.
5. Expect a lot of bugs ;)
