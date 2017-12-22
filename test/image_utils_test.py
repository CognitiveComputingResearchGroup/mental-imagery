import unittest

import cv2
import image_utils as img_utils
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_something(self):
        img = cv2.imread('../resources/pixel_layer.png')
        all_white = np.ones_like(img) * 255

        # img_utils.display(img)

        segments = img_utils.get_image_segments(img)

        # Segments correspond to regions that contains something of interest.
        # Segments do not contain any pixel data themselves;
        # they just define an area.
        for segment in segments:
            masked_img = img_utils.get_pixels_for_segment(all_white, segment)
            img_utils.display(masked_img)

        # By combining segments with the "pixel layer",
        # sections of the pixel layer can be extracted
        for segment in segments:
            masked_img = img_utils.get_pixels_for_segment(img, segment)
            img_utils.display(masked_img)

        # For PAM, a slightly larger rectangular region around the
        # segment may be useful, especially when the surrounding region
        # is necessary to give the pixels of interest meaning
        # (e.g., when the object is a hole)
        for segment in segments:
            masked_img = img_utils.get_pixels_for_segment(img, segment)
            cropped_image = img_utils.crop_to_segment(masked_img, segment)
            img_utils.display(cropped_image)


        # Question: When combining images in the workspace for mental imagery,
        # what should the background color be???


if __name__ == '__main__':
    unittest.main()
