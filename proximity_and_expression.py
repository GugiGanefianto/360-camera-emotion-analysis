import os
import numpy as np

import json

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


plt.rcParams.update({"font.size": 12})

# =============================================================================
# ================================variables====================================
# =============================================================================


### distance threshold to define proximity ###
thsld = 1 ### metre ###






### open and read the json data ###
json_file = os.getcwd() + "/out.json"
with open(json_file, 'r') as j_in :
    json_read = json.load(j_in)

expressions = ["angry","disgust","fear","happy","sad","surprise","neutral"]




### input video information ###
vid_j = os.getcwd() + "/vid.json"
with open(vid_j, 'r') as vid_in :
    vid_info = json.load(vid_in)

x_ext = vid_info["info"]["x_extent"] # in pixels
y_ext = vid_info["info"]["y_extent"]

fps = vid_info["info"]["fps"]
total_frame = max([int(item) for item in json_read.keys()])
video_duration = total_frame/fps




if not os.path.exists(os.getcwd()+"/plots/") :
    os.mkdir(os.getcwd()+"/plots/")


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



"""
def calculate_D(y_bottom, y_extent) :
    ### calculate beta first, in rad ###
    beta = (y_bottom/y_extent * np.pi) - (np.pi/2)
    D = camera_h / np.tan(beta)
    if beta <= 0 :
        print("WARNING! Negative beta.")
    else :
        return D
"""


def calculate_alpha(x1, x2, x_extent) :
    alpha = 2*np.pi/x_extent * abs(x2-x1)
    return alpha



def calculate_R(D1, D2, alpha) :
    R = np.sqrt(D1**2 + D2**2 - 2*D1*D2 * np.cos(alpha) )
    return R




def set_colour(emotion) :
    if emotion == 'angry' :
        colour = 'red'
    elif emotion == 'disgust' :
        colour = 'darkgoldenrod'
    elif emotion ==  'fear' :
        colour = 'orange'
    elif emotion == 'happy' :
        colour = 'lime'
    elif emotion == 'sad' :
        colour = 'blue'
    elif emotion == 'surprise' :
        colour = 'magenta'
    elif emotion == 'neutral' :
        colour = 'tab:gray'
    return colour






def get_scatter_data(use_id) :
    x = []
    y = []
    z = []

    for frame0 in data[use_id].keys() :
        dominant_expression_colour = set_colour(data[use_id][frame0]['emotion'])
        print(frame0, dominant_expression_colour)
        current_frame_proximity_counter = 0
        
        for person1 in data.keys() :
            for frame1 in data[person1].keys() :
                if person1!=use_id and frame0==frame1 :
                    
                    x0 = data[use_id][frame0]['x']
                    x1 = data[person1][frame1]['x']
                    
                    D0 = data[use_id][frame0]['D']
                    D1 = data[person1][frame1]['D']
                    
                    alpha = calculate_alpha(x0, x1, x_ext)
                    R = calculate_R(D0, D1, alpha)
                    
                    print("The distance between person%s and person%s at frame%s is %s m!"\
                                    %(use_id, person1, frame0, R))
                    if R<thsld :
                        current_frame_proximity_counter += 1
                    
        
        
        
        #x.append(frame0*video_duration/total_frame)
        x.append(int(frame0)/fps)
        y.append(current_frame_proximity_counter)
        z.append(dominant_expression_colour)
        

    return x,y,z








def plot_result(x, y, z) :
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16,4))
    ax.set_title("Person ID: %s" % use_id)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("# of other people in proximity")
    ax.set_yticks(range(0,10))
    ax.set_ylim([-0.25, 5.5])
    ax.set_xlim([0,video_duration])
    #ax.set_xticks([])
    
    
    ax.scatter(x,y, c=z, s=100, marker='s', alpha=0.25)
    
    
    legend_elements = [Line2D([0],[0], marker='s', label='Angry',
                        alpha=1, markersize=10,
                        color='w', markerfacecolor='red'),

                        Line2D([0],[0], marker='s', label='Disgust',
                        alpha=1, markersize=10,
                        color='w', markerfacecolor='darkgoldenrod'),

                        Line2D([0],[0], marker='s', label='Fear',
                        alpha=1, markersize=10,
                        color='w', markerfacecolor='orange'),

                        Line2D([0],[0], marker='s', label='Happy',
                        alpha=1, markersize=10,
                        color='w', markerfacecolor='lime'),

                        Line2D([0],[0], marker='s', label='Sad',
                        alpha=1, markersize=10,
                        color='w', markerfacecolor='blue'),

                        Line2D([0],[0], marker='s', label='Surprise',
                        alpha=1, markersize=10,
                        color='w', markerfacecolor='magenta'),

                        Line2D([0],[0], marker='s', label='Neutral',
                        alpha=1, markersize=10,
                        color='w', markerfacecolor='tab:gray'),]
    ax.legend(handles=legend_elements, loc='upper center',
                    bbox_to_anchor=(0.5,-0.2), fancybox=False, shadow=False, ncol=7)
    
    
    plt.tight_layout()
    plt.savefig(os.getcwd()+'/plots/result%s.jpg' % use_id)
    plt.close()
    




# =============================================================================
# =============================================================================
# =============================================================================



data = reorganise_database()



for use_id in data.keys() :
    x,y,z = get_scatter_data(use_id)
    plot_result(x,y,z)