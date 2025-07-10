import numpy as np
import os
import json
import matplotlib.pyplot as plt

# =============================================================================
# ================================variables====================================
# =============================================================================

### open and read the json data ###
json_file = os.getcwd() + "/out.json"
with open(json_file, 'r') as j_in :
    json_read = json.load(j_in)

#total_txtFiles = 0


#Angry_score    = 0
#Disgust_score  = 0
#Fear_score     = 0
#Happy_score    = 0
#Sad_score      = 0
#Surprise_score = 0
#Neutral_score  = 0

Angry_count    = 0
Disgust_count  = 0
Fear_count     = 0
Happy_count    = 0
Sad_count      = 0
Surprise_count = 0
Neutral_count  = 0


# =============================================================================
# ================================functions====================================
# =============================================================================



# =============================================================================
# =============================================================================
# =============================================================================


### collect the information ###
for frame in json_read.keys() :
    i = 0
    while i < len(json_read[frame]['ids']) :
        personID = int(json_read[frame]['ids'][i])
        dominant_expression = str(json_read[frame]['emotion'][i])

        if   dominant_expression == 'angry' :
            Angry_count    += 1
        elif dominant_expression == 'disgust' :
            Disgust_count  += 1
        elif dominant_expression == 'fear' :
            Fear_count     += 1
        elif dominant_expression == 'happy' :
            Happy_count    += 1
        elif dominant_expression == 'sad' :
            Sad_count      += 1
        elif dominant_expression == 'surprise' :
            Surprise_count += 1
        elif dominant_expression == 'neutral' :
            Neutral_count  += 1
        
        i += 1
    
    print("%s people detected in frame %s!" % (i, frame))




# =============================================================================
# =============================================================================
# =============================================================================

### print the numbers ###

print("Angry_count    : %s" % Angry_count)
print("Disgust_count  : %s" % Disgust_count)
print("Fear_count     : %s" % Fear_count)
print("Happy_count    : %s" % Happy_count)
print("Sad_count      : %s" % Sad_count)
print("Surprise_count : %s" % Surprise_count)
print("Neutral_count  : %s" % Neutral_count)
print("               = %s" % (Angry_count+Disgust_count+Fear_count \
                        +Happy_count+Sad_count+Surprise_count+Neutral_count))

# =============================================================================
# =============================================================================
# =============================================================================

### plot the graph ###

x = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]


expression_counts = [Angry_count, Disgust_count, Fear_count, Happy_count,
                    Sad_count, Surprise_count, Neutral_count]

fig, ax = plt.subplots(nrows=1, ncols=1)
ax.set_title("Overall facial expression")
ax.set_ylabel("Count")
ax.bar(x=x, height=expression_counts, color='tab:gray')
plt.tight_layout()
plt.savefig(os.getcwd()+"/overall_expression_counts.jpg")
plt.show()