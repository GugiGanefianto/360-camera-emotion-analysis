import cv2
import numpy as np

from deepface import DeepFace

import config

from panoramic.predict_one_frame import predict_one_frame
from panoramic.framework.additional import convert_y_to_D, draw_bboxes

"""
from detectors.yolov8_object import detect_objects
from detectors.face_detector import detect_faces
from detectors.gender_age import predict_gender_age
from detectors.emotion import predict_emotion
from detectors.body_attr import predict_height_weight
from utils.draw import draw_results
"""



def process_stream(input_frame, tracker, cH):

    # If input is a frame (NumPy array)
    if isinstance(input_frame, np.ndarray):
        frame = input_frame
    # If using Streamlit WebRTC
    elif hasattr(input_frame, "to_ndarray"):
        frame = input_frame.to_ndarray(format="bgr24")
    # If uploaded file (file-like object)
    elif hasattr(input_frame, "read"):
        file_bytes = np.asarray(bytearray(input_frame.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)
    # If input is a file path (string)
    elif isinstance(input_frame, str):
        frame = cv2.imread(input_frame)
    else:
        raise ValueError("Unsupported input type for process_stream")

    
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    

    bboxes, classes, scores = predict_one_frame(config.FOV, config.THETAs, config.PHIs,
                        frame, frame_width, frame_height,
                        config.sub_image_width,
                        classes_to_detect=[0],
                        split_image2=not config.match_across_boundary)
    
    # update deepsort and get the tracking results
    tracks = tracker.update(np.array(bboxes), np.array(classes),
                            np.array(scores), frame,
                            config.prevent_different_classes_match,
                            config.match_across_boundary)
    if len(tracks) > 0 :
        bbox_xyxy = tracks[:, :4]
        track_classes = tracks[:, 4]
        track_scores = tracks[:, 5]
        identities = tracks[:, -1]
        # get distances and emotions
        distances_to_camera = []
        dominant_emotions = []
        for bbox in bbox_xyxy :
            x1,y1,x2,y2 = map(int, bbox)
            # calculate distance
            D = convert_y_to_D(y2, frame_height, cH)
            distances_to_camera.append(D)
            # determine the dominant emotion
            yq = int(np.round(y1+(y2-y1)/4, decimals=0))
            face = frame[y1:yq, x1:x2]
            # use tf.config.set_visible_devices to ensure subsequent TensorFlow ops (e.g., DeepFace.analyze) run on CPU.
            analysis = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
            try :
                emotion = analysis[0]['dominant_emotion']
            except IndexError :
                emotion = 'unknown'
            dominant_emotions.append(emotion)

    # plot the tracking results
    try :
        annotated = draw_bboxes(frame, bbox_xyxy, track_classes, track_scores,
                                frame_width, identities, distances_to_camera, dominant_emotions)
    except UnboundLocalError :
        print("No Tracks!")
        annotated = frame
    except :
        print("Unexpected Error!")
        annotated = frame
        raise

    
    
    
    
    """
    results = detect_objects(frame)
    people = [det for det in results if det["label"] == "person"]

    for person in people:
        x1, y1, x2, y2 = person["bbox"]
        person_crop = frame[y1:y2, x1:x2]
        face_bbox = detect_faces(person_crop)
        if face_bbox:
            fx1, fy1, fx2, fy2 = face_bbox[0]
            face_img = person_crop[fy1:fy2, fx1:fx2]
            gender, age = predict_gender_age(face_img)
            emotion = predict_emotion(face_img)
        else:
            gender, age, emotion = None, None, None
        height, weight = predict_height_weight(person_crop)
        person.update({
            "gender": gender,
            "age": age,
            "emotion": emotion,
            "height": height,
            "weight": weight,
        })

    annotated = draw_results(frame, results)
    """

    return annotated