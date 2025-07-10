import os
import numpy as np

import json

import matplotlib.pyplot as plt


plt.rcParams.update({"font.size": 9.5})


# =============================================================================
# ================================variables====================================
# =============================================================================

### open and read the json data ###
json_file = os.getcwd() + "/out.json"
with open(json_file, 'r') as j_in :
    json_read = json.load(j_in)




### video frame size in pixels ###
vid_j = os.getcwd() + "/vid.json"
with open(vid_j, 'r') as vid_in :
    vid_info = json.load(vid_in)
x_ext = vid_info["info"]["x_extent"]
y_ext = vid_info["info"]["y_extent"]


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
def get_distance2camera(dictionary, x_extent, y_extent) :
    dict_D = {}
    for key in dictionary.keys() :
        x,y,half_w,half_h, left,right,top,bottom = get_points(dictionary[key])
        D = calculate_D(bottom, y_extent)
        dict_D[key] = D
    return dict_D
"""
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

"""
def calculate_R(D1, D2, alpha) :
    R = np.sqrt(D1**2 + D2**2 - 2*D1*D2 * np.cos(alpha) )
    return R
"""





def plot_heatmap(data, person_idx) :
    plt.clf()
    fig, axs = plt.subplots(nrows=4, ncols=2, figsize=(8,8) )
    axs = axs.ravel()

    fig.suptitle("ID: %s"%person_idx)
    axs[0].set_title("Angry")
    axs[1].set_title("Disgust")
    axs[2].set_title("Fear")
    axs[3].set_title("Happy")
    axs[4].set_title("Sad")
    axs[5].set_title("Surprise")
    axs[6].set_title("Neutral")

    for i in range(7) :
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




    ### for the bar plot ###
    Angry_count    = 0
    Disgust_count  = 0
    Fear_count     = 0
    Happy_count    = 0
    Sad_count      = 0
    Surprise_count = 0
    Neutral_count  = 0


    
    
    ### plot the location points ###
    Px = []
    Py = []
    for frame in data[person_idx].keys() :
        x = data[person_idx][frame]['x']
        y = data[person_idx][frame]['y']
        D = data[person_idx][frame]['D']
        dominant_expression = data[person_idx][frame]['emotion']
        
        alpha = calculate_alpha(0, x, x_ext)
        
        Px.append(D*np.cos(alpha))
        Py.append(D*np.sin(-alpha))
        
        if dominant_expression == 'angry' :
            axs[0].scatter(Px,Py, s=100, edgecolor=None, alpha=1./255, marker='H', c='red')
            Angry_count += 1
        elif dominant_expression == 'disgust' :
            axs[1].scatter(Px,Py, s=100, edgecolor=None, alpha=1./255, marker='H', c='darkgoldenrod')
            Disgust_count += 1
        elif dominant_expression == 'fear' :
            axs[2].scatter(Px,Py, s=100, edgecolor=None, alpha=1./255, marker='H', c='orange')
            Fear_count += 1
        elif dominant_expression == 'happy' :
            axs[3].scatter(Px,Py, s=100, edgecolor=None, alpha=1./255, marker='H', c='lime')
            Happy_count += 1
        elif dominant_expression == 'sad' :
            axs[4].scatter(Px,Py, s=100, edgecolor=None, alpha=1./255, marker='H', c='blue')
            Sad_count += 1
        elif dominant_expression == 'surprise' :
            axs[5].scatter(Px,Py, s=100, edgecolor=None, alpha=1./255, marker='H', c='magenta')
            Surprise_count += 1
        elif dominant_expression == 'neutral' :
            axs[6].scatter(Px,Py, s=100, edgecolor=None, alpha=1./255, marker='H', c='tab:gray')
            Neutral_count += 1
        else :
            print("Warning! Dominant expression not accounted for!")
    



    ### plot the bar plot ###
    expressions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
    expression_counts = [Angry_count, Disgust_count, Fear_count,
                            Happy_count, Sad_count, Surprise_count,
                            Neutral_count ]
    bars = axs[7].bar(x=expressions, height=expression_counts, color='k')
    bars[0].set_color('red')
    bars[1].set_color('darkgoldenrod')
    bars[2].set_color('orange')
    bars[3].set_color('lime')
    bars[4].set_color('blue')
    bars[5].set_color('magenta')
    bars[6].set_color('tab:gray')


    """
    legend_elements = [Line2D([0],[0], marker='H', label='Angry',
                        alpha=0.5, markersize=13,
                        color='w', markerfacecolor='red'),

                        Line2D([0],[0], marker='H', label='Disgust',
                        alpha=0.5, markersize=13,
                        color='w', markerfacecolor='darkgoldenrod'),

                        Line2D([0],[0], marker='H', label='Fear',
                        alpha=0.5, markersize=13,
                        color='w', markerfacecolor='orange'),

                        Line2D([0],[0], marker='H', label='Happy',
                        alpha=0.5, markersize=13,
                        color='w', markerfacecolor='lime'),

                        Line2D([0],[0], marker='H', label='Sad',
                        alpha=0.5, markersize=13,
                        color='w', markerfacecolor='blue'),

                        Line2D([0],[0], marker='H', label='Surprise',
                        alpha=0.5, markersize=13,
                        color='w', markerfacecolor='magenta'),

                        Line2D([0],[0], marker='H', label='Neutral',
                        alpha=0.5, markersize=13,
                        color='w', markerfacecolor='tab:gray'),]


    axs[7].axis("off")
    axs[7].legend(handles=legend_elements, loc='upper center')
                    #bbox_to_anchor=(0.5,-0.05), fancybox=True, shadow=False, ncol=4)
    """


    plt.tight_layout()
    plt.savefig(os.getcwd()+"/plots/heatmap%s.jpg"%person_idx)
    plt.close()








# =============================================================================
# =============================================================================
# =============================================================================


data = reorganise_database() # rearrange according to person id as suppose to frame number

for personID in data.keys() :
    plot_heatmap(data, personID)