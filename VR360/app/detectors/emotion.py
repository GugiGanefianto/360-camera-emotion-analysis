from deepface import DeepFace

def predict_emotion(face_img):
    analysis = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
    return analysis.get("dominant_emotion")
