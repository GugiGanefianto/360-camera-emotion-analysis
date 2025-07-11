import os
import numpy as np

import json

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






if not os.path.exists(os.getcwd()+"/profiles") :
    os.mkdir(os.getcwd()+"/profiles")


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






def read_table() :
    df = pd.read_csv(input_table, index_col=False, header=None)
    print(df)
    return df






def rose_profile(table, keys, personID) :
    x_loc = np.linspace(0.0, 2*np.pi, num_of_ids, endpoint=False)
    i = keys[personID]
    norm_param = max(table[i])

    print(table)
    print(IDs)
    print(personID, i, norm_param)

    if norm_param > 0 :
        ax = plt.subplot(projection="polar")
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.yaxis.set_ticks(np.arange(0, 1.1, 0.2), [])
        ax.set_ylim([0.0, 1.0])
        ax.set_title("PersonID: %s\n"%personID)



        for idx in IDs :
            j = keys[idx]
            x = x_loc[j]
            h = table.at[i, j] / norm_param # normalise according to the max interaction count

            """
            print("The distance between person%s and person%s is %s m." %
                                                    (personID, idx, table.at[i, j]))
            """
            if str(i) == j :
                ax.bar(x, h, width=0.4, color="tab:green", alpha=0.0)
            else :
                ax.bar(x, h, width=0.4, color="tab:green", alpha=0.9)
                if h>0 :
                    ax.text(x, h, idx, fontsize=10, color="black",
                        bbox=dict(facecolor="w", alpha=0.8) )


        plt.tight_layout()
        plt.savefig(os.getcwd()+"/profiles/rose_%s.png"%personID)
        plt.close()


# =============================================================================
# =============================================================================
# =============================================================================


data = reorganise_database()

table = read_table()

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





for ID in IDs :
    rose_profile(table, order_keys, ID)