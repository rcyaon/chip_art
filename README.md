# Installation
You'll need to have the Magic VLSI tool installed. I've tested it within OpenLANE (https://github.com/The-OpenROAD-Project/OpenLane) docker (run `make mount`).

# Running
`make clean && make GDS_WIDTH=50 IMAGE=chip_art.png`

The GDS_WIDTH specifies how wide (in um) you want the image to render in the GDS. 

# Output
It will create GDS/LEF files in `gds/` folder. 

# Additional scripts within this fork
`merge_gds.py`: Merges two gds files together. Helpful if you've already done your chip layout and want to merge the art and chip art together.
`run_drc.py`:
`precheck_art.py`:
