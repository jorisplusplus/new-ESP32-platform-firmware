#Include all files that contain MP bindings
set(mods
    "${COMPONENT_DIR}/modi2c.c"
)

#Define the name of your module here
set(mod_name "i2c")

if(CONFIG_DRIVER_I2C_ENABLE)
    message(STATUS "i2c enabled")
    set(EXTMODS "${EXTMODS}" "${mods}" CACHE INTERNAL "")
    set(EXTMODS_NAMES "${EXTMODS_NAMES}" "${mod_name}" CACHE INTERNAL "")
else()
    message(STATUS "i2c disabled")
endif()