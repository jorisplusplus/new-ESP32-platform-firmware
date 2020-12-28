#!/bin/bash
git submodule update --init --recursive
cd firmware
make menuconfig
