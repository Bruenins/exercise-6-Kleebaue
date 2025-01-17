# -----------------------------------------------------------------------
# Exercise 6
# -----------------------------------------------------------------------
# load libs
from pathlib import Path
from satpy import Scene, find_files_and_readers
# -----------------------------------------------------------------------
# set paths
exercise = Path('/home/mklee/git/exercise-6-Kleebaue')
data_dir = Path('/home/mklee/git/py_skripte/data')
output_dir = exercise / 'results'
data_dir.mkdir(parents=True,exist_ok=True)
output_dir.mkdir(parents=True,exist_ok=True)
# -----------------------------------------------------------------------

# 1. Read the Scene that you downloaded from the data directory using SatPy. [2P]
files = find_files_and_readers(base_dir = data_dir,reader="seviri_l1b_nc")
scn = Scene(filenames=files)

# 2. Load the composites "natural_color" and "convection" [2P]

# list all composite names
scn.available_composite_names()

# load natural_color and convection
scn.load(["natural_color"])
scn.load(["convection"])

# 3. Resample the fulldisk to the Dem. Rep. Kongo and its neighbours [4P] 
#    by defining your own area in Lambert Azimuthal Equal Area. 
#    Use the following settings:
#      - lat and lon of origin: -3/23
#      - width and height of the resulting domain: 500px
#      - projection x/y coordinates of lower left: -15E5
#      - projection x/y coordinates of upper right: 15E5 

from pyresample.geometry import AreaDefinition

area_id = "Dem. Rep. Kongo and its neighbours"
description = "Dem. Rep. Kongo in Lambert Azimuthal Equal Area"
proj_id = "Dem. Rep. Kongo and its neighbours"
proj_dict = {"proj": "laea", "lat_ts": -3, "lon_0": 23}

width = 500    # width of the result domain in pixels
height = 500   # height of the result domain in pixels

llx = -15E5   # projection x coordinate of lower left corner of lower left pixel
lly = -15E5   # projection y coordinate of lower left corner of lower left pixel
urx = 15E5    # projection x coordinate of upper right corner of upper right pixel
ury = 15E5    # projection y coordinate of upper right corner of upper right pixel

area_extent = (llx,lly,urx,ury)
area_def = AreaDefinition(area_id, proj_id, description, proj_dict, width, height, area_extent)

local_scn = scn.resample(area_def)
local_scn.show("natural_color")

# 4. Save both loaded composites of the resampled Scene as simple png images. [2P]
local_scn.save_datasets(writer="simple_image",
                  datasets=["natural_color", "convection"],
                  filename="{name}_{start_time:%Y%m%d_%H%M%S}.png",
                  base_dir=output_dir)
# -----------------------------------------------------------------------