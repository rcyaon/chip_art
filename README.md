# Installation
You'll need to have the Magic VLSI tool installed. 
# Running
`make clean && make GDS_WIDTH=50 IMAGE=chip_art.png`
The GDS_WIDTH specifies how wide (in um) you want the image to render in the GDS. 
# Output
It will create GDS/LEF files in `gds/` folder. 
# Additional scripts within this fork
* `merge_gds.py`: Merges two gds files together. Helpful if you've already done your chip layout and want to merge the art and chip art together.

* `precheck.py`: Scans your source image for pixels that would diagonally touch corners on the same metal layer, a known cause of BEOL DRC failures.
