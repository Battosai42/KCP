import pathlib
from json_import.parse_json import *
import matplotlib.pyplot as plt
import numpy as np
import math
import pcbnew

config_file = pathlib.Path('D:\Git\Battosai13\ErgoChoc\config\keyboard-layout_v2.json')

test = load(config_file)
keys = test.get_key_locations()

# Load the board
pcb = pcbnew.LoadBoard("take2.kicad_pcb")

# Find the component
c = pcb.FindModuleByReference("D1")

# Place it somewhere
c.SetPosition(pcbnew.wxPointMM(100, 100))

# Rotate it (angle in 1/10 degreee)
c.SetOrientation(45 * 10)

# and save the file under a different name
pcb.Save("take2_mod.kicad_pcb")

for k in keys:
    x, y, rotation, name = k
