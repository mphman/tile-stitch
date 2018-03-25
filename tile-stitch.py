# tile-stitch MapTile raw file stitcher
# Utilizing Pillow
# github.com/mphman/tile-stitch

from PIL import Image
from tqdm import tqdm
import os, re, time

# Setup Variables
TILE_EXTENSION = '.jpg' # Define MapTile Format
DATA_PATH = './data' # Data Directory
EXPORT_FORMAT = 'TIFF' # Final Map Format

file_list = []
for path, subdir, filenames in os.walk(DATA_PATH):
    for elm in filenames:
        if os.path.splitext(elm)[1] == TILE_EXTENSION:
            file_list.append(os.path.join(path,elm))

print("Analyzing MapTile File List...")
# Use some regex to determine the patterns in the maptile files...
# The filenames are defined as follows: zz-xx-yy.jpg
# z - zoom level
# x - x-level (start left, going right)
# y - y-level (start top, going down) 
extract_lvl = re.compile('(?<!\w)([0-9]+)[^/]')

z_list = [] # hold zoom levels
for elm in file_list:
    z_list.append(int(extract_lvl.findall(elm)[0])) # z-level search
x_list = []
for elm in file_list:
    if int(extract_lvl.findall(elm)[0]) == max(z_list):
        x_list.append(int(extract_lvl.findall(elm)[1])) # x-level search
y_list = []
for elm in file_list:
    if int(extract_lvl.findall(elm)[0]) == max(z_list):
        y_list.append(int(extract_lvl.findall(elm)[2])) # y-level search

selected_files = []
for elm in file_list:
    if int(extract_lvl.findall(elm)[0]) == max(z_list):
        selected_files.append(elm)

print("Total Tiles to Stitch: " + str(len(selected_files)))

# Now need to iterate through all of the tiles and build the image:
# 1) get size of tile, extrapolate the max canvas size 
# 2) iterate through canvas adding elements on the way
# 3) export to tiff image

img = Image.open(next((elm for elm in selected_files if (str(max(z_list)) + "-0-0") in elm), None))
tile_w, tile_h = img.size
canvas_w = tile_w * (max(x_list))
canvas_h = tile_h * (max(y_list))
canvas = Image.new('RGB', (canvas_w,canvas_h))

for y_coord in tqdm(range(min(y_list),max(y_list)), desc=' Processing Image Rows: '):
    for x_coord in range(min(x_list),max(x_list)):
        # Get next tile
        next_file = next((elm for elm in selected_files if (str(max(z_list)) + "-" + str(x_coord) + "-" + str(y_coord) + ".") in elm), None)
        paste_img = Image.open(next_file)
        canvas.paste(paste_img, ((x_coord * tile_w), (y_coord * tile_h)))

canvas.save("FinalMap" + str(time.time()) + "." + EXPORT_FORMAT.lower() ,EXPORT_FORMAT)