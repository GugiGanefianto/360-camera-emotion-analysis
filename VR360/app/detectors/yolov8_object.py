from ultralytics import YOLO

# Load once globally
_model = YOLO("yolov8n.pt") # Download from Ultralytics if not present

def detect_objects(frame):
    results = _model(frame)
    detections = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls)
            label = _model.names[cls]
            if label in ["person", "chair", "table", "car", "building", "cafe"]:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

                detections.append({
                    "label": label,
                    "bbox": [x1, y1, x2, y2],
                    "confidence": float(box.conf),
                })
    return detections
