import cv2

def draw_results(frame, detections):
    for det in detections:
        label = det.get("label", "")
        bbox = det.get("bbox", [0,0,0,0])
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        desc = label
        for k in ["gender", "age", "emotion", "height", "weight"]:
            if k in det and det[k] is not None:
                desc += f', {k}: {det[k]}'
        cv2.putText(frame, desc, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    return frame
