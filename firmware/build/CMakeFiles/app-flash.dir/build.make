# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/joris/git/new-ESP32-firmware-platform/firmware

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/joris/git/new-ESP32-firmware-platform/firmware/build

# Utility rule file for app-flash.

# Include the progress variables for this target.
include CMakeFiles/app-flash.dir/progress.make

CMakeFiles/app-flash:
	cd /home/joris/git/new-ESP32-firmware-platform/esp-idf/components/esptool_py && /usr/bin/cmake -D IDF_PATH="/home/joris/git/new-ESP32-firmware-platform/esp-idf" -D ESPTOOLPY="/home/joris/.espressif/python_env/idf4.0_py3.8_env/bin/python /home/joris/git/new-ESP32-firmware-platform/esp-idf/components/esptool_py/esptool/esptool.py --chip esp32" -D ESPTOOL_ARGS="write_flash @flash_app_args" -D WORKING_DIRECTORY="/home/joris/git/new-ESP32-firmware-platform/firmware/build" -P /home/joris/git/new-ESP32-firmware-platform/esp-idf/components/esptool_py/run_esptool.cmake

app-flash: CMakeFiles/app-flash
app-flash: CMakeFiles/app-flash.dir/build.make

.PHONY : app-flash

# Rule to build all files generated by this target.
CMakeFiles/app-flash.dir/build: app-flash

.PHONY : CMakeFiles/app-flash.dir/build

CMakeFiles/app-flash.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/app-flash.dir/cmake_clean.cmake
.PHONY : CMakeFiles/app-flash.dir/clean

CMakeFiles/app-flash.dir/depend:
	cd /home/joris/git/new-ESP32-firmware-platform/firmware/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/joris/git/new-ESP32-firmware-platform/firmware /home/joris/git/new-ESP32-firmware-platform/firmware /home/joris/git/new-ESP32-firmware-platform/firmware/build /home/joris/git/new-ESP32-firmware-platform/firmware/build /home/joris/git/new-ESP32-firmware-platform/firmware/build/CMakeFiles/app-flash.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/app-flash.dir/depend

