from src.preprocess import Preprocess
from src.extraction import examCodeExtract
from src.extraction import AnswerExtract
from src.extraction import StudentIDExtract
import sys
import os
import yaml
import cv2
import pprint

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))


image_path = r"data\sample (6).jpg"


if __name__ == "__main__":
    config_path = "config.yaml"
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    prep = Preprocess(config)
    answerExt = AnswerExtract(config)
    ECExt = examCodeExtract(config)
    SIDExt = StudentIDExtract(config)

    img = cv2.imread(image_path)
    processed_img = prep(img)
    cv2.imwrite(r"debug\0_preprocessed.jpg", processed_img)

    print(r"[o] Preprocess done! Result saved at: debug\0_preprocessed.jpg")
    print(f"[o] Student ID extraction result: {SIDExt(processed_img)}")
    print(f"[o] Exam code result: {ECExt(processed_img)}")
    print("[o] Answer extraction result: ")
    pprint.pprint(answerExt(processed_img), indent=2)
