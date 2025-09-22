# Configurations for paths, thresholds, etc.

#THRESH_CONFIDENCE = 0.6

prevent_different_classes_match = True # whether to use the support for multiple categories in DeepSORT
match_across_boundary = True # whether to use the support for boundary continuity in DeepSORT
classes_to_detect = [0] # index numbers of the categories to detect in the COCO dataset [0, 1, 2, 3, 5, 7, 9]

FOV = 120 # the field of view of the sub-images
THETAs = [0, 90, 180, 270] # contains the theta of each sub-image whose length should be the same as the number of sub-images
PHIs = [-10, -10, -10, -10] # contains the Phi of each sub-image whose length should be the same as the number of sub-images

sub_image_width = 640 # width (or height) of the sub-images
score_threshold = 0.6 # threshold for the confidence score
nms_threshold = 0.45 # threshold for the Non Maximum Supression
