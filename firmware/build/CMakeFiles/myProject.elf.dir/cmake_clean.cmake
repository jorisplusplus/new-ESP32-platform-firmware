file(REMOVE_RECURSE
  "bootloader/bootloader.bin"
  "bootloader/bootloader.elf"
  "bootloader/bootloader.map"
  "config/sdkconfig.cmake"
  "config/sdkconfig.h"
  "myProject.bin"
  "myProject.map"
  "project_elf_src.c"
  "CMakeFiles/myProject.elf.dir/project_elf_src.c.obj"
  "myProject.elf"
  "myProject.elf.pdb"
  "project_elf_src.c"
)

# Per-language clean rules from dependency scanning.
foreach(lang C)
  include(CMakeFiles/myProject.elf.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
