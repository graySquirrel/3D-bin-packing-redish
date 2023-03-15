from py3dbp import Packer, Bin, Item, Painter
import time


def addTruck(p, t):
    box = Bin(
        partno=t[1],
        WHD=t[0],
        max_weight=28080,
        corner=0,
        put_type=0
    )
    p.addBin(box)

def addTotes(p, x, n, l):
    for i in range(n):
        p.addItem(Item(
            partno='{}_{}'.format(str(x[1]), str(i + 1)),
            name=x[1],
            typeof='cube',
            WHD=x[0],
            weight=1,
            level=l,
            loadbear=100,
            updown=False,
            color=x[2])
        )

def packAndPrintResults(p):
    # calculate packing
    p.pack(
        bigger_first=True,
        distribute_items=False,
        fix_point=True,
        number_of_decimals=0
    )
    # print result
    box = p.bins[0]
    volume = box.width * box.height * box.depth
    #print(":::::::::::", box.string())

    # print("FITTED ITEMS:")
    volume_t = 0
    volume_f = 0
    unfitted_name = ''

    # '''
    for item in box.items:
        # print("partno : ",item.partno)
        # print("type : ",item.name)
        # print("color : ",item.color)
        # print("position : ",item.position)
        # print("rotation type : ",item.rotation_type)
        # print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
        # print("volume : ",float(item.width) * float(item.height) * float(item.depth))
        # print("weight : ",float(item.weight))
        volume_t += float(item.width) * float(item.height) * float(item.depth)
        # print("***************************************************")
    #print("***************************************************")
    # '''
    unfittedItems = {}
    if (len(box.unfitted_items) > 0):
        notfitnum=len(box.unfitted_items)
        print(str(notfitnum) + " Items dont fit:")
        for item in box.unfitted_items:
            if item.name not in unfittedItems:
                unfittedItems[item.name] = 0
            unfittedItems[item.name] = unfittedItems[item.name] + 1
            # print("partno : ", item.partno)
            # print("type : ", item.name)
            # print("color : ", item.color)
            # print("W*H*D : ", str(item.width) + '*' + str(item.height) + '*' + str(item.depth))
            # print("volume : ", float(item.width) * float(item.height) * float(item.depth))
            # print("weight : ", float(item.weight))
            # volume_f += float(item.width) * float(item.height) * float(item.depth)
            # unfitted_name += '{},'.format(item.partno)
            # print("***************************************************")
    #print("***************************************************")
        for key in unfittedItems:
            print(key, unfittedItems[key])
    else:
        print("all totes fit!!")
    print('space utilization : {}%'.format(round(volume_t / float(volume) * 100, 2)))
    print('residual volume : ', float(volume) - volume_t)
    #print('unpack item : ', unfitted_name)

    #print('unpack item volume : ', volume_f)
    #print("gravity distribution : ", box.gravity)
    # '''
    stop = time.time()
    #print('used time : ', stop - start)
    print("***************************************************")
    return(Painter(box))
