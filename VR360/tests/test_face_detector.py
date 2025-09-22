import unittest
import numpy as np
from app.detectors.face_detector import detect_faces

class TestFaceDetector(unittest.TestCase):
    def test_no_face(self):
        blank = np.zeros((100, 100, 3), dtype=np.uint8)
        faces = detect_faces(blank)
        self.assertEqual(faces, [])

if __name__ == '__main__':
    unittest.main()
