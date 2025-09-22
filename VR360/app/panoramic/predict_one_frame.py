"""## Define the Processes for the Improved Object Detection on One Frame

Using the functions defined previously, the process of the improved object detection on one frame is defined by the function predict_one_frame().

* FOV: The field of view of the sub-images.

* THETAs: A list that contains the theta of each sub-image whose length should be the same as the number of sub-images.

* PHIs: A list that contains the Phi of each sub-image whose length should be the same as the number of sub-images.

* im: The image on which to do the object detection.

* predictor: YOLOv5 or Faster RCNN object detection model.

* video_width, video_height: Width and Height of the input image frame.

* sub_image_width: Width (or height) of the sub-images.

* classes_to_detect: Index numbers of the classes to detect according to COCO, default to [0, 1, 2, 3, 5, 7, 9].

* split_image2: Whether to split the bboxes across the centre line of sub-image 2 into two when reprojecting the bboxes back into the original image using reproject_bboxes().
"""

#import time

from .framework.transform import equir2pers
from .framework.reproject import reproject_bboxes
from .framework.match_subimages import number_of_left_and_right_boundary
from .framework.merge import merge_bbox_across_boundary
from .framework.additional import filter_classes, xyxy2xcycwh

from detectron2.layers import batched_nms
import cv2
import torch
import torchvision
from ultralytics import YOLO

# Load once globally
_model = YOLO("yolov8n.pt")


def predict_one_frame(FOV, THETAs, PHIs, im, video_width, video_height,
                      sub_image_width, predictor=_model,
                      classes_to_detect=[0, 1, 2, 3, 5, 7, 9],
                      split_image2=True) :
    
    
    
    ### check processing speed, record the current time first ###
    #time1 = time.time()













    # =============================================================================
    # =======================IMPROVED-OBJECT-DETECTOR==============================
    # =============================================================================

    ### split the frame into 4 sub images (of perspective projection), get the maps and the output images ###
    lon_maps, lat_maps, subimgs = equir2pers( im, FOV, THETAs, PHIs, sub_image_width, sub_image_width)

    
    ### lists for storing the detection results from all sub-images ###
    bboxes_all = []
    classes_all = []
    scores_all = []

    ### list for storing the index of the bounding boxes that intersect with the boundaries of the sub-images ###
    bboxes_boundary = [None] * 8
    
    

























    #---------------------------------YOLO----------------------------------


    """
    ### for each sub image, first change the color from BGR to RGB ###
    for i in range(len(subimgs)) :
        subimgs[i] = cv2.cvtColor(subimgs[i], cv2.COLOR_BGR2RGB)
    """
    
    
    
    ### YOLO supports detecting several images at the same time, so input all the sub images at once to the predictor ###
    #results = predictor(subimgs, size=sub_image_width)  # includes NMS
    results = predictor(subimgs, imgsz=sub_image_width)  # includes NMS


    
    
    """
    # --------  if you want to save and check the detail of the results on each sub image, run the code below  ----------
    # results.save()
    # --------  end of this part  ----------
    """


    for i in range(len(subimgs)) : # for each sub-image

        bboxes  = results[i].boxes.xyxy.tolist()
        classes = list(map(int, results[i].boxes.cls.tolist()))
        scores  = results[i].boxes.conf.tolist()

    
        """
        ### Originally, YOLO outputs the positions using the relative coordinates [0-1], so transform the output format by multiplying by the width/height of the sub-image ###
        bboxes = (results.xyxyn[i].cpu().numpy()[:, 0:4]  *  [sub_image_width,sub_image_width,sub_image_width,sub_image_width] ).tolist()
        classes = list(map(int, results.xyxyn[i].cpu().numpy()[:, 5].tolist()))
        scores = results.xyxyn[i].cpu().numpy()[:, 4].tolist()
        """


        ### for each bbox in the current sub image, reproject it to the original image ###
        (reprojected_bboxes,classes,scores,left_boundary_box,right_boundary_box) = reproject_bboxes(bboxes, lon_maps[i], lat_maps[i], classes, scores,
                                                                                                            10, i, video_width, video_height, len(subimgs),
                                                                                                            sub_image_width / 640 * 20,
                                                                                                            split_image2)



    
        ### get the indeces of the bboxes that intersect the boundaries of the sub-images ###
        if left_boundary_box != None :
            bboxes_boundary[number_of_left_and_right_boundary(i)[0] ] = left_boundary_box + len(bboxes_all)
        if right_boundary_box != None :
            bboxes_boundary[number_of_left_and_right_boundary(i)[1] ] = right_boundary_box + len(bboxes_all)

        ### add the bboxes after reprojection to the previous lists ###
        bboxes_all = bboxes_all + reprojected_bboxes
        classes_all = classes_all + classes
        scores_all = scores_all + scores




















    ### merge the boxes that goes across the boundaries using merge_bbox_across_boundary() ###
    bboxes_all, classes_all, scores_all = merge_bbox_across_boundary(bboxes_all, classes_all, scores_all, video_width, video_height, bboxes_boundary)

    
    ### do NMS on the output bboxes again to get the indeces of the boxes that should be kept ###
    keep = batched_nms( torch.tensor(bboxes_all),
                            torch.tensor(scores_all),
                            torch.tensor(classes_all), 0.3)

    
    ### only keep the instances of the classes we need (person, bike, car, motorbike, bus, truck, traffic light by default) ###
    bboxes_all, classes_all, scores_all = filter_classes( torch.tensor(bboxes_all)[keep],
                                                              torch.tensor(classes_all)[keep],
                                                              torch.tensor(scores_all)[keep],
                                                              classes_to_detect)





    ### convert the bboxes from [x,y,x,y] to [xc,yc,w,h] ###
    bboxes_all_xcycwh = xyxy2xcycwh(bboxes_all)


































    ### record the current time again and calculate the running time ###
    #time2 = time.time()
    # print(time2 - time1)

    return bboxes_all_xcycwh, classes_all, scores_all