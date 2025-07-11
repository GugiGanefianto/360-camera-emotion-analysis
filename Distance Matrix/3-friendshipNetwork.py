import os
import numpy as np

import json

import networkx as nx


import pandas as pd

import matplotlib.pyplot as plt
#from matplotlib.colors import LinearSegmentedColormap as lincmap

plt.rcParams.update({"font.size": 14})

# =============================================================================
# ================================variables====================================
# =============================================================================


input_table = os.getcwd() + "/weight.csv"





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




def read_array() :
    df = pd.read_csv(input_table, index_col=False, header=None)
    array = df.to_numpy()
    print(array)
    return array










# =============================================================================
# =============================================================================
# =============================================================================


data = reorganise_database()

### get all IDs, assign into an order ###
IDs = list(data.keys())
labels = {}
i = 0
while i < len(IDs) :
    labels[i] = IDs[i]
    i += 1

print(IDs)
print(labels)


### read the distance matrix (weight) ###
array = read_array()



### plot the network ###
G = nx.from_numpy_array(array)

fig, ax = plt.subplots(ncols=1, nrows=1)
nx.draw(G, with_labels=True, style='-', edge_color="k", node_color="lime", node_size=400,
        alpha=0.5, font_size=14, ax=ax, labels=labels)
#nx.draw_planar(G, with_labels=True, style=':', edge_color="k", node_color="lime", labels=labels)
plt.savefig(os.getcwd()+"/network.pdf")
plt.close()