import os
import numpy as np

import json

import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 12})

# =============================================================================
# ================================variables====================================
# =============================================================================


### distance threshold to define proximity ###
thshld = 1 # metre






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





def draw_pie_chart(ls) :
    other0     = 0
    other1     = 0
    other2     = 0
    other3plus = 0
    total      = len(ls)

    for i in ls :
        if i == 0 :
            other0 += 1
        elif i == 1 :
            other1 += 1
        elif i == 2 :
            other2 += 1
        elif i > 2 :
            other3plus += 1

    labels = ['1 (alone)', '2', '3', '4+']
    pie_slices = [other0/total*100, other1/total*100,
                    other2/total*100, other3plus/total*100]

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.pie(pie_slices, labels=labels)
    plt.legend(bbox_to_anchor=(1.0,-0.0), fancybox=False, shadow=False, ncol=4)
    plt.savefig(os.getcwd()+"/plots/pie%s.jpeg"%use_id)
    plt.close()




# =============================================================================
# =============================================================================
# =============================================================================



data = reorganise_database()


for use_id in data.keys() :
    proximity_ls = []
    for frame0 in data[use_id].keys() :
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
                    
                    if R<thshld :
                        current_frame_proximity_counter += 1
        
        proximity_ls.append(current_frame_proximity_counter)




    draw_pie_chart(proximity_ls)