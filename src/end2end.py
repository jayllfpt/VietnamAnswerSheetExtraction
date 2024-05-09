from src.extraction import StudentIDExtract
from src.extraction import AnswerExtract
from src.extraction import examCodeExtract
from src.preprocess import Preprocess

import sys
import os
import yaml
import cv2

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))


class Pipeline():
    def __init__(self, config_path="config.yaml"):

        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.paperExt = Preprocess(self.config)
        self.answerExt = AnswerExtract(self.config)
        self.ECExt = examCodeExtract(self.config)
        self.SIDExt = StudentIDExtract(self.config)

    def __call__(self, img):
        if img.shape[0] < img.shape[1]:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

        processed_img = self.paperExt(img)
        return {
            "studentID": self.SIDExt(processed_img),
            "examCode": self.ECExt(processed_img),
            "answer": self.answerExt(processed_img)
        }


if __name__ == "__main__":
    pass
