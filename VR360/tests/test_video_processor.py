import unittest
import cv2
import numpy as np
from app.video_processor import process_stream

class TestVideoProcessor(unittest.TestCase):
    def test_process_static_image(self):
        sample = np.zeros((256, 256, 3), dtype=np.uint8)
        result = process_stream(sample)
        # Ensure output is same shape
        self.assertEqual(result.shape, sample.shape)

    def test_process_invalid_input(self):
        with self.assertRaises(Exception):
            process_stream(None)

if __name__ == '__main__':
    unittest.main()
