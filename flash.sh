#!/usr/bin/env bash

. ./setenv.sh
cd firmware
rm -rf components/micropython/ports/esp32/build-GENERIC/*
idf.py flash -b 2000000
