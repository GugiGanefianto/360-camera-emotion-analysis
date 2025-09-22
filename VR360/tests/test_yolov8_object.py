import unittest
import numpy as np
from app.detectors.yolov8_object import detect_objects

class TestYOLOv8Object(unittest.TestCase):
    def test_object_detection_no_person(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)  # blank image
        output = detect_objects(frame)
        self.assertEqual(output, [])  # Should be no detections

if __name__ == '__main__':
    unittest.main()
