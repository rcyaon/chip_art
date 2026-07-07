import gdstk

## Change paths below to match your files
chip_art_lib = gdstk.read_gds("chip_art.gds")
my_lib = gdstk.read_gds("chip_without_art.gds")

chip_art_cell = chip_art_lib.top_level()[0]
my_lib.add(chip_art_cell)

my_top = my_lib.top_level()[0]

## Origin defines offset
my_top.add(gdstk.Reference(chip_art_cell, origin=(30, 150)))

## Change path below to where you want merged GDS to be located
my_lib.write_gds("final_chip.gds")
