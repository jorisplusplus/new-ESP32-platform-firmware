#Include all files that contain MP bindings
set(mods
    "${COMPONENT_DIR}/modconsts.c"
)

#Define the name of your module here
set(mod_name "consts")
set(mod_register "CONSTS")

set(EXTMODS "${EXTMODS}" "${mods}" CACHE INTERNAL "")
set(EXTMODS_NAMES "${EXTMODS_NAMES}" "${mod_name}" CACHE INTERNAL "")