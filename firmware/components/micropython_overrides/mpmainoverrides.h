//
// Created by Tom on 02/08/2020.
//

#pragma once

#include "sdkconfig.h"

// This lets us configure the stack size via config.sh
#undef MP_TASK_STACK_SIZE
#define MP_TASK_STACK_SIZE CONFIG_MICROPY_STACK_SIZE