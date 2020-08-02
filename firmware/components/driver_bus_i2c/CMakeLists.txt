set(srcs
    "driver_i2c.c"
    "modi2c.c"
)

set(mods
    "${COMPONENT_DIR}/modi2c.c"
)

set(includes
    "include"
    )

idf_component_register(SRCS "${srcs}"
                       INCLUDE_DIRS ${includes}
                       REQUIRES micropython)

set(EXTMODS "${EXTMODS};${mods}" CACHE INTERNAL "")