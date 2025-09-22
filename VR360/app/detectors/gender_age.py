from deepface import DeepFace

def predict_gender_age(face_img):
    analysis = DeepFace.analyze(face_img, actions=['age', 'gender'], enforce_detection=False)
    return analysis.get("gender"), analysis.get("age")
