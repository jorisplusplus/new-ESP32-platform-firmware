set(srcs
    "driver_i2c.c"
    "modi2c.c"
)

set(includes
    "include"
    )

execute_process(COMMAND "echo test")

idf_component_register(SRCS "${srcs}"
                       INCLUDE_DIRS ${includes}
                       REQUIRES micropython)