# Import libraries
import matplotlib.colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import itertools
from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()
import redishUtils as re

# Redish containers (W, H, D) in inches
sixBy9 = [(22, 10, 15.25), 'sixBy9', 'cyan']
Round = [(22, 10, 15.25), 'Round', 'yellow']
Cup = [(22, 10, 15.25), 'Cup', 'k']
nineBy9 = [(23, 12, 19), 'nineBy9', 'gray']
fiveInch = [(21, 12, 15), 'fiveInch', 'red']
eightOz = [(13, 8.9, 8.8), 'eightOz', 'green']
eightBy8 = [(23, 12, 19), 'eightBy8', 'green']
aPalletOfStuff = [(36, 36, 36), 'aPallet', 'orange'] # assume a pallet is 3' x 3' and 3 feet high.

# Uhaul 20' truck dims are 7' 3" wide, 6' 5" high, 16' 10" deep
# But we are considering that stuff only goes 5' high
# and only half of the width 3' 7" is available for totes, since towers go on other side
# Bin dims go W, D, H
TwentyFootTruckHalf = [(41, 202, 60), 'TwentyFootTruckHalf']

# init packing function
packer = Packer()

re.addTruck(packer, TwentyFootTruckHalf)
# re.addTotes(packer, container object, number of totes, priority- 1 is highest)
re.addTotes(packer, sixBy9, 25, 1) # MOMA
re.addTotes(packer, Round, 30, 2) # L'Oreal

re.addTotes(packer, fiveInch, 20, 3) # The Hub - NJ
re.addTotes(packer, eightBy8, 15, 4) # JPM

painter = re.packAndPrintResults(packer)




# draw results
# print(painter.width, painter.height, painter.depth) # x, y, z
# for item in painter.items:
#     print(item.name, item.color, item.width, item.depth, item.height, item.position[0], item.position[1], item.position[2])
painter.plotBoxAndItems()
