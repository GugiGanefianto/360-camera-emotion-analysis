import os
import numpy as np

import json

import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 12})

# =============================================================================
# ================================variables====================================
# =============================================================================

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




def determine_colour(expression) :
    if expression == 'angry' :
        colour = 'red'
    elif expression == 'disgust' :
        colour = 'darkgoldenrod'
    elif expression == 'fear' :
        colour = 'orange'
    elif expression == 'happy' :
        colour = 'lime'
    elif expression == 'sad' :
        colour = 'blue'
    elif expression == 'surprise' :
        colour = 'magenta'
    elif expression == 'neutral' :
        colour = 'tab:gray'

    return colour





def expression_evo(data, person_idx, expression) :
    ### divide the timeframe into 6 periods ###
    interval = int(np.round(total_frame/6, decimals=0))
    periods = range(interval, interval*6+1, interval)
    
    plt.clf()
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8,8) )
    axs = axs.ravel()

    colour = determine_colour(expression)

    
    fig.suptitle("ID: %s %s"%(person_idx, expression))
    timeSpan = np.arange(0, video_duration+1, interval/fps)
    
    
    axs[0].set_title("%s-%s s" % (timeSpan[0],timeSpan[1]) )
    axs[1].set_title("%s-%s s" % (timeSpan[1],timeSpan[2]) )
    axs[2].set_title("%s-%s s" % (timeSpan[2],timeSpan[3]) )
    axs[3].set_title("%s-%s s" % (timeSpan[3],timeSpan[4]) )
    axs[4].set_title("%s-%s s" % (timeSpan[4],timeSpan[5]) )
    axs[5].set_title("%s-%s s" % (timeSpan[5],timeSpan[6]) )


    
    for i in range(6) :
        axs[i].set_xlim([-4.5, 4.5])
        axs[i].set_ylim([-4.5, 4.5])
        axs[i].set_xticks([])
        axs[i].set_yticks([])
        axs[i].set_aspect("equal")
        #axs[i].set_title("ID: %s"%person_idx)

        ### drawing the x y axes ###
        axs[i].axhline(0, color='gainsboro')
        axs[i].axvline(0, color='gainsboro')

        ### the camera at the origin ###
        axs[i].scatter(0, 0, marker='s', color='k', s=50)

        ### draw circles w/ specific radii ###
        circle1 = plt.Circle( (0,0), radius=1, fill=False, edgecolor='silver', ls=':')
        circle2 = plt.Circle( (0,0), radius=2, fill=False, edgecolor='silver', ls=':')
        circle3 = plt.Circle( (0,0), radius=3, fill=False, edgecolor='silver', ls=':')
        circle4 = plt.Circle( (0,0), radius=4, fill=False, edgecolor='silver', ls=':')
        axs[i].add_patch(circle1)
        axs[i].add_patch(circle2)
        axs[i].add_patch(circle3)
        axs[i].add_patch(circle4)
        #axs[i].text(1*np.cos(5/4 *np.pi), 1*np.sin(5/4 *np.pi), "1m", color='silver')
        axs[i].text(2*np.cos(5/4 *np.pi), 2*np.sin(5/4 *np.pi), "2m", color='silver')
        axs[i].text(3*np.cos(5/4 *np.pi), 3*np.sin(5/4 *np.pi), "3m", color='silver')
        axs[i].text(4*np.cos(5/4 *np.pi), 4*np.sin(5/4 *np.pi), "4m", color='silver')

        ### 0 to 2pi ###
        axs[i].text( 2.53,  0.10, "360$^o$", color='silver')
        axs[i].text( 3.50, -0.80, "0$^o$"  , color='silver')
        axs[i].text(-0.30,  3.60, "270$^o$", color='silver')
        axs[i].text(-4.0 ,  0.10, "180$^o$", color='silver')
        axs[i].text(-0.40, -4.40, "90$^o$" , color='silver')


    
    ### plot the location points according to time ###
    for frame in data[person_idx].keys() :
        x = data[person_idx][frame]['x']
        y = data[person_idx][frame]['y']
        w = data[person_idx][frame]['w']
        h = data[person_idx][frame]['h']
        
        D = data[person_idx][frame]['D']
        alpha = calculate_alpha(0, x, x_ext)
        
        dominant_expression = data[person_idx][frame]['emotion']
        
        if dominant_expression == expression :
            if int(frame)>=1 and int(frame)<periods[0] :
                axs[0].scatter(D*np.cos(alpha),D*np.sin(-alpha),s=100,edgecolor=None,alpha=1/160,marker='H',c=colour)
            elif int(frame)>=periods[0] and int(frame)<periods[1] :
                axs[1].scatter(D*np.cos(alpha),D*np.sin(-alpha),s=100,edgecolor=None,alpha=1/160,marker='H',c=colour)
            elif int(frame)>=periods[1] and int(frame)<periods[2] :
                axs[2].scatter(D*np.cos(alpha),D*np.sin(-alpha),s=100,edgecolor=None,alpha=1/160,marker='H',c=colour)
            elif int(frame)>=periods[2] and int(frame)<periods[3] :
                axs[3].scatter(D*np.cos(alpha),D*np.sin(-alpha),s=100,edgecolor=None,alpha=1/160,marker='H',c=colour)
            elif int(frame)>=periods[3] and int(frame)<periods[4] :
                axs[4].scatter(D*np.cos(alpha),D*np.sin(-alpha),s=100,edgecolor=None,alpha=1/160,marker='H',c=colour)
            elif int(frame)>=periods[4] and int(frame)<periods[5] :
                axs[5].scatter(D*np.cos(alpha),D*np.sin(-alpha),s=100,edgecolor=None,alpha=1/160,marker='H',c=colour)
    

    plt.tight_layout()
    plt.savefig(os.getcwd()+"/plots/%s%s.jpg"%(person_idx, expression))
    plt.close()


# =============================================================================
# =============================================================================
# =============================================================================

data = reorganise_database()





for personID in data.keys() :
    for expression in expressions :
        expression_evo(data, personID, expression)