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

# Redish containers (W, D, H) in inches
sixBy9 = [(22, 10, 15.25), 'sixBy9', 'cyan']
Round = [(22, 10, 15.25), 'Round', 'yellow']
Cup = [(22, 10, 15.25), 'Cup', 'k']
nineBy9 = [(23, 12, 19), 'nineBy9', 'gray']
fiveInch = [(21, 12, 15), 'fiveInch', 'red']
eightOz = [(13, 8.9, 8.8), 'eightOz', 'green']
eightBy8 = [(23, 12, 19), 'eightBy8', 'green']
aPalletOfStuff = [(40, 40, 40), 'aPallet', 'orange']
Tower = [(40, 28, 70), 'Tower', 'blue']

choices = list([sixBy9,Round,Cup,nineBy9,fiveInch,eightOz,eightBy8,aPalletOfStuff,Tower])
choices_names = list(map(lambda x: (x[1]), choices))

# Uhaul 20' truck dims are 7' 3" wide, 6' 5" high, 16' 10" deep
# But we are considering that stuff only goes 5' high
# and only half of the width 3' 7" is available for totes, since towers go on other side
# Bin dims go W, D, H
TwentyFootTruckHalf = [(41, 202, 60), 'TwentyFootTruckHalf']
TwentyFootTowerTruckHalf = [(41, 202, 71), 'TwentyFootTruckHalf']
TwentyFootTruck = [(82, 202, 71), 'TwentyFootTruck']
# init packing function
packer = Packer()

#re.addTruck(packer, TwentyFootTruckHalf)
re.addTruck(packer, TwentyFootTruck)

# re.addTotes(packer, container object, number of totes, priority- 1 is highest)
re.addTotes(packer, sixBy9, 25, 1) # MOMA, cyan
re.addTotes(packer, Tower, 2, 2) # MOMA towers

re.addTotes(packer, Round, 30, 3) # L'Oreal, yellow

re.addTotes(packer, fiveInch, 20, 3) # The Hub - NJ, red
re.addTotes(packer, eightBy8, 20, 4) # JPM, green

painter, retstr = re.packAndPrintResults(packer)
painter.plotBoxAndItems()


# packer2 = Packer()
# re.addTruck(packer2, TwentyFootTowerTruckHalf)
# re.addTotes(packer2, Tower, 8, 1)
# painter2 = re.packAndPrintResults(packer2)
# painter2.plotBoxAndItems()