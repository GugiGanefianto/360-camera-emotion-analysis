import os
import numpy as np

import json
import itertools

import matplotlib.pyplot as plt
#from matplotlib.colors import LinearSegmentedColormap as lincmap

plt.rcParams.update({"font.size": 14})

# =============================================================================
# ================================variables====================================
# =============================================================================


### distance threshold to define proximity ###
R_thsld = 1.0 # metre






### open and read the json data ###
json_file = os.getcwd() + "/out.json"
with open(json_file, 'r') as j_in :
    json_read = json.load(j_in)




### input video information ###
vid_j = os.getcwd() + "/vid.json"
with open(vid_j, 'r') as vid_in :
    vid_info = json.load(vid_in)

x_ext = vid_info["info"]["x_extent"] # in pixels
y_ext = vid_info["info"]["y_extent"]

fps = vid_info["info"]["fps"]
total_frame = max([int(item) for item in json_read.keys()])
video_duration = total_frame/fps


# =============================================================================
# ================================functions====================================
# =============================================================================


def reorganise_database() :
    dictionary = {}
    for frame in json_read.keys() :
        i = 0
        while i < len(json_read[frame]['ids']) :
            personID = int(json_read[frame]['ids'][i])

            x = int(json_read[frame]['x'][i]) # x left
            y = int(json_read[frame]['y'][i]) # y top
            w = int(json_read[frame]['w'][i])
            h = int(json_read[frame]['h'][i])
            
            D = float(json_read[frame]['D'][i])

            emotion = str(json_read[frame]['emotion'][i])
            
            if personID not in dictionary.keys() :
                dictionary[personID] = {frame : {'x':x, 'y':y, 'w':w, 'h':h,
                                                 'D':D, 'emotion':emotion} }
            else :
                dictionary[personID][frame] = {'x':x, 'y':y, 'w':w, 'h':h,
                                               'D':D, 'emotion':emotion}
            
            i += 1
    
    return dictionary








def create_mtx_1_frame(data, frame, dictionary) :
    for pair in itertools.combinations(data.keys(), r=2) :
        try :
            print(pair)
            print("ID %s data: %s" % (pair[0], data[pair[0]][str(frame)]) )
            print("ID %s data: %s" % (pair[1], data[pair[1]][str(frame)]) )
            print("Data available for pair %s at frame %s!"%(pair, frame))
            
            D0 = data[pair[0]][str(frame)]['D']
            D1 = data[pair[1]][str(frame)]['D']
            
            x0 = data[pair[0]][str(frame)]['x']
            x1 = data[pair[1]][str(frame)]['x']
            
            alpha = calculate_alpha(x0, x1, x_ext)
            R = calculate_R(D0, D1, alpha)
            
            
            dictionary[str(frame)][pair] = R
            
            
            print("The distance between person %s and person %s at frame %s is %s m!"\
                                %(pair[0], pair[1], frame, np.round(R, decimals=2)) )
            print('\n')
            
            
        except KeyError :
            print("Incomplete data for pair %s at frame %s!"%(pair, frame))
            print('\n')




def overall_dist_mtx(dictionary) :
    sumTable = np.zeros(shape=(num_of_ids, num_of_ids))
    for frame in dictionary.keys() :
        table = np.zeros(shape=(num_of_ids, num_of_ids))
        for pair in dictionary[frame].keys() :
            R = dictionary[frame][pair]
            if R < R_thsld :
                print("\n")
                print(pair)
                print(order_keys)
                print(order_keys[pair[0]], order_keys[pair[1]])
                table[order_keys[pair[0]]][order_keys[pair[1]]] = 1
                table[order_keys[pair[1]]][order_keys[pair[0]]] = 1
                sumTable += table
    
    return sumTable
            
    



def calculate_alpha(x1, x2, x_extent) :
    alpha = 2*np.pi/x_extent * abs(x2-x1)
    return alpha

def calculate_R(D1, D2, alpha) :
    R = np.sqrt(D1**2 + D2**2 - 2*D1*D2 * np.cos(alpha) )
    return R





def imshow_table(table, savePath, cmap) :
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.imshow(table,cmap=cmap)
    ax.xaxis.tick_top()
    ax.set_xticks(range(len(table)), [i for i in IDs] )
    ax.set_yticks(range(len(table)), [j for j in IDs] )
    plt.tight_layout()
    plt.savefig(savePath)
    plt.close()





# =============================================================================
# =============================================================================
# =============================================================================



data = reorganise_database()

### build a distance matrix per frame ###
dist = {} 
for frame in np.arange(1, total_frame+1, 1) :
    dist[str(frame)] = {}
    create_mtx_1_frame(data, frame, dist)
"""
for frame in dist.keys() :
    print(frame, dist[frame].keys())
    for pair in dist[frame].keys() :
        print(pair, dist[frame][pair])
    print("\n")
"""



### get all IDs, assign into an order ###
IDs = list(data.keys())
order_keys = {}
i = 0
while i < len(IDs) :
    order_keys[IDs[i]] = i
    i += 1
num_of_ids = len(IDs)
"""
print(IDs)
print(order_keys)
print(num_of_ids)
"""




### create the overall distance matrix weight ###
sumTable = overall_dist_mtx(dist)

### save the distance matrix and show as a table ###
np.savetxt(fname="weight.csv", X=sumTable, delimiter=",")
imshow_table(sumTable, os.getcwd()+"/weight.pdf", cmap='binary')