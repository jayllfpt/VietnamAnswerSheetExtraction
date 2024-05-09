import cv2
import os

from .utils import remove_text, remove_background, crop_paper


class Preprocess():
    def __init__(self, config):
        self.config = config

    def __call__(self, img):
        REC_SIZE = self.config['GRABCUT_REC_SIZE']
        DEBUG_DIR = self.config['PREP_DEBUG_DIR']
        PAPER_SIZE = self.config['IMAGE_SIZE_DEFAULT']
        if self.config["PREP_VISUALIZE"]:
            os.makedirs(DEBUG_DIR, exist_ok=True)

        # Resize image to workable size
        dim_limit = 1080
        max_dim = max(img.shape)
        if max_dim > dim_limit:
            resize_scale = dim_limit / max_dim
            img = cv2.resize(img, None, fx=resize_scale, fy=resize_scale)

        # Create a copy of resized original image for later use
        orig_img = img.copy()
        if self.config["PREP_VISUALIZE"]:
            cv2.imwrite(DEBUG_DIR + "/1_resize.jpg", img)
        img = remove_text(img)
        if self.config["PREP_VISUALIZE"]:
            cv2.imwrite(DEBUG_DIR + "/2_closing.jpg", img)
        img = remove_background(img, REC_SIZE)
        if self.config["PREP_VISUALIZE"]:
            cv2.imwrite(DEBUG_DIR + "/3_grabCut.jpg", img)

        return cv2.resize(crop_paper(img, orig_img), PAPER_SIZE)
