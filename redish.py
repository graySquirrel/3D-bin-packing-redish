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
#Tower = [(40, 28, 60), 'Tower', 'blue']
Tower = [(40, 28, 60), 'Tower', 'blue']

choices = list([sixBy9,Round,Cup,nineBy9,fiveInch,eightOz,eightBy8,aPalletOfStuff,Tower])
choices_names = list(map(lambda x: (x[1]), choices))

# Uhaul 20' truck dims are 7' 3" wide, 6' 5" high, 16' 10" deep
# But we are considering that stuff only goes 5' high
# and only half of the width 3' 7" is available for totes, since towers go on other side
# Bin dims go W, D, H
TwentyFootTruckHalf = [(41, 202, 60), 'TwentyFootTruckHalf']
TwentyFootTowerTruckHalf = [(41, 202, 71), 'TwentyFootTruckHalf']
TwentyFootTruck = [(82, 202, 60), 'TwentyFootTruck']
# init packing function
packer = Packer()

re.addTruck(packer, TwentyFootTruck)
#re.addTruck(packer, TwentyFootTruck)
# stop,item,count,customer
# 1,1,5,MOMA
# 1,2,2,MOMA
# 2,3,10,LOreal
# 3,4,10,The Hub
# 4,5,10,JPM
# 5,8,1,New

# item,W,D,H,Name,Color
# 0 ,22, 10, 15.25,six By 9,cyan
# 1 ,22, 10, 15.25,Round,yellow
# 2 ,22, 10, 15.25,Cup,black
# 3 ,23, 12, 19,nine By 9,gray
# 4,21, 12, 15,five Inch,red
# 5,13, 8.9, 8.8,eight Oz,green
# 6 ,23, 12, 19,eight By 8,green
# 7 ,40, 40, 40,a Pallet,orange
# 8,40, 28, 60,Tower,blue
# re.addTotes(packer, container object, number of totes, priority- 1 is highest)
#re.addTotes(packer, Tower, 1, 1) # New, Blue
#re.addTotes(packer, aPalletOfStuff, 1, 1) # New, Blue
re.addTotes(packer, Cup, 2, 1) # MOMA 
re.addTotes(packer, Round, 5, 1) # MOMA, cyan
re.addTotes(packer, aPalletOfStuff, 1, 2)
re.addTotes(packer, nineBy9, 10, 2) # L'Oreal, yellow
#re.addTotes(packer, aPalletOfStuff, 1, 2) # New, Blue

re.addTotes(packer, fiveInch, 10, 3) # The Hub - NJ, red
re.addTotes(packer, eightOz, 10, 4) # JPM, green
re.addTotes(packer, Tower, 1, 5) # New, Blue
#re.addTotes(packer, eightOz, 1, 4) # JPM, green

painter, retstr = re.packAndPrintResults(packer)
painter.plotBoxAndItems()


# packer2 = Packer()
# re.addTruck(packer2, TwentyFootTowerTruckHalf)
# re.addTotes(packer2, Tower, 8, 1)
# painter2 = re.packAndPrintResults(packer2)
# painter2.plotBoxAndItems()