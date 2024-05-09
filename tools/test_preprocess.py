import sys
import os
import yaml
import cv2

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))

from src.preprocess import Preprocess

if __name__ == "__main__":
    config_path = "config.yaml"
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    P = Preprocess(config)

    img = cv2.imread(r"data\sample (6).jpg")
    cv2.imwrite(r"debug\0_preprocessed.jpg", P(img))
