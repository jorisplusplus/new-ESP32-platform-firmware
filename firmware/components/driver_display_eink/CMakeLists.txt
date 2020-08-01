set(srcs
    "driver_eink.c"
    "driver_eink_dev.c"
    "driver_eink_lut.c"
)

set(includes
    "include"
    )

idf_component_register(SRCS "${srcs}"
                       INCLUDE_DIRS ${includes}
                       REQUIRES nvs_flash)
