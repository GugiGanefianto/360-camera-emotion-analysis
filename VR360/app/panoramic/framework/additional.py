"""### 5. Additional Functions for Improving Object Detection

* classid2name(): A function to get the corresponding class of the index number in COCO dataset.

* filter_classes(): Pre-trained YOLO and Faster RCNN output detection results according to categories in COCO. Here, only parts of them are used.

* xyxy2xcycwh(): A function used to transform the output from [x1,y1,x2,y2] format to [x_centre, y_centre, width, height].

* convert_y_to_D(): A function to calculate the real-world distance to the camera D using the y bottom value of the bounding box.

* draw_bboxes(): A function to annotate the image frame with the results.
"""

import cv2
import numpy as np

def classid2name(id):
    names = [
        "person",
        "bicycle",
        "car",
        "motorbike",
        "aeroplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "backpack",
        "umbrella",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "sofa",
        "pottedplant",
        "bed",
        "diningtable",
        "toilet",
        "tvmonitor",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush",
    ]
    return names[int(id)]


def filter_classes(bboxes_all, classes_all, scores_all, class_needed):
    bboxes_all = bboxes_all.tolist()
    classes_all = classes_all.tolist()
    scores_all = scores_all.tolist()
    # remove the bboxes which are not belong to the needed classes from the lists
    for i in range(len(classes_all), 0, -1):
        if classes_all[i - 1] not in class_needed:
            bboxes_all.pop(i - 1)
            classes_all.pop(i - 1)
            scores_all.pop(i - 1)
    return bboxes_all, classes_all, scores_all

def xyxy2xcycwh(bboxes) :
    bboxes_new = []
    for bbox in bboxes :
        bboxes_new.append( [(bbox[0]+bbox[2])/2,
                            (bbox[1]+bbox[3])/2,
                            (bbox[2] - bbox[0]) ,
                            (bbox[3] - bbox[1]) ] )
    return bboxes_new

def xyxy2ltwh(bboxes) :
    bboxes_new = []
    for bbox in bboxes :
        bboxes_new.append( [ bbox[0],
                             bbox[1],
                            (bbox[2] - bbox[0]) ,
                            (bbox[3] - bbox[1]) ] )
    return bboxes_new


def convert_y_to_D(y_bottom, image_height, camera_height) :
    beta = (y_bottom/image_height * np.pi) - (np.pi/2)
    D = camera_height/np.tan(beta)

    return D


#from panoramic_detection.draw_output import classid2name
def draw_bboxes(img, bbox, track_classes, track_scores, video_width, identities, distances, dominant_emotions, offset=(0, 0)) :
    # for each object, draw the bbox and label
    for i, box in enumerate(bbox) :
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        bbox_size = None
        # box text and bar
        id = int(identities[i]) if identities is not None else 0
        color = (0,204,0)

        label_top = (str(id) + " " + classid2name(track_classes[i]) + " " +
                     str(round(track_scores[i] * 100, 1)) + "%" )
        label_bottom = ("D=" + str(np.round(distances[i], decimals=2)) + "m" + " " +
                        str(dominant_emotions[i]) )

        t_size = cv2.getTextSize(label_top, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]




        # if the bbox is totally in the image frame
        if x2 <= video_width:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
            cv2.rectangle(img, (x1, y1), (x1 + t_size[0] + 15, y1 + t_size[1] + 15), color, -1 )
            cv2.putText(img,label_top, (x1, y1 + t_size[1] + 4), cv2.FONT_HERSHEY_SIMPLEX,
                        1, [255, 255, 255], 2, )
            cv2.putText(img,label_bottom, (x1, y2 +t_size[1] + 4), cv2.FONT_HERSHEY_SIMPLEX,
                        1, color, 2, )

        # if the bbox crosses the boundary of the video
        else:
            cv2.rectangle(img, (x1, y1), (video_width, y2), color, 3)
            # plot the right part
            cv2.rectangle(img, (x1, y1), (x1 + t_size[0] + 15, y1 + t_size[1] + 15), color, -1 )
            cv2.putText(img,label_top, (x1, y1 + t_size[1] + 4), cv2.FONT_HERSHEY_SIMPLEX,
                        1, [255, 255, 255], 2, )
            cv2.putText(img,label_bottom, (x1, y2 + t_size[1] + 4), cv2.FONT_HERSHEY_SIMPLEX,
                        1, color, 2, )
            # plot the left part
            cv2.rectangle(img, (0, y1), (x2 - video_width, y2), color, 3)
            cv2.rectangle(img, (0, y1), (0 + t_size[0] + 15, y1 + t_size[1] + 15), color, -1 )
            cv2.putText(img,label_top, (0, y1 + t_size[1] + 4), cv2.FONT_HERSHEY_SIMPLEX,
                        1, [255, 255, 255], 2, )
            cv2.putText(img,label_bottom, (0, y2 + t_size[1] + 4), cv2.FONT_HERSHEY_SIMPLEX,
                        1, color, 2, )




    return img