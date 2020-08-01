set(srcs
    "main.c"
    "factory_reset.c"
    "nvs_init.c"
    "ota_update.c"
    "platform.c"
    "zip.c"
    "system.c"
)

idf_component_register(SRCS "${srcs}"
                    INCLUDE_DIRS "./")