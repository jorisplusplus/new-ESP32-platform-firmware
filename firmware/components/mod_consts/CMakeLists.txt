set(srcs
    "modconsts.c"
)

idf_component_register(SRCS "${srcs}"
                       REQUIRES micropython)