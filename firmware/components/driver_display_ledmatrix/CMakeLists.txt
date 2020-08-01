set(srcs
    "driver_ledmatrix.c"
)

set(includes
    "include"
    )

idf_component_register(SRCS "${srcs}"
                       INCLUDE_DIRS ${includes}
                       REQUIRES nvs_flash
                       )
