import sys
import os
import yaml
import cv2

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))

from src.extraction import AnswerExtract


if __name__ == "__main__":
    config_path = "config.yaml"
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    AE = AnswerExtract(config)

    img = cv2.imread(r"debug\0_preprocessed.jpg")
    print(AE(img))
