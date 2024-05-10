import cv2
import os


from .utils import process_img


class examCodeExtract():
    def __init__(self, config):
        self.config = config

    def __call__(self, img):
        t = self.config['EC_TOP'] 
        l = self.config['EC_LEFT']
        b = self.config['EC_BOT'] 
        r = self.config['EC_RIGHT']
        DEBUG_DIR = self.config['EXAM_CODE_DEBUG_DIR']
        if self.config['EC_VISUALIZE']:
            os.makedirs(DEBUG_DIR, exist_ok=True)

        img = img[t:b, l:r]
        if self.config['EC_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + f"0_examcode.jpg", img)

        blur_img = process_img(img, self.config)
        # apply canny edge detection algorithm
        canny_img = cv2.Canny(blur_img, 125, 200)
        if self.config['EC_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "4_canny.jpg", canny_img)
        canny_img = cv2.dilate(canny_img, cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
        if self.config['EC_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "5_dilate_canny.jpg", canny_img)

        # Finding contours for the detected edges.
        contours, hierarchy = cv2.findContours(
            canny_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # Keeping only the largest detected contour. select top 7
        boxes_cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
        boxes_img = cv2.drawContours(
            img.copy(), boxes_cnts, -1, (0, 255, 255), 1)
        if self.config['EC_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "6_boxes.jpg", boxes_img)

        boxes = []
        if len(boxes_cnts) > 0:
            for cnt in boxes_cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                boxes.append((x, y, w, h))

        # sort left to right
        boxes = sorted(boxes, key=lambda x: x[0])

        x, y, w, h = boxes[0]
        crop_img = img.copy()[y:y + h, x:x + w]
        if self.config['EC_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "6_box0.jpg", crop_img)

        binary_image = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        binary_image = cv2.threshold(
            binary_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        binary_image = cv2.erode(binary_image, cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (3, 3)), iterations=4)
        binary_image = cv2.dilate(binary_image, cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)

        if self.config['EC_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "7_binary.jpg", binary_image)

        contours, hierarchy = cv2.findContours(
            binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # Keeping only the largest detected contour. select top 7
        boxes_cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:3]
        boxes_img = cv2.drawContours(
            img.copy(), boxes_cnts, -1, (0, 255, 255), 1)
        if self.config['EC_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "6_boxes.jpg", boxes_img)

        boxes = []
        if len(boxes_cnts) > 0:
            for cnt in boxes_cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                boxes.append((x, y, w, h))

        # sort left to right
        boxes = sorted(boxes, key=lambda x: x[0])

        exam_code = [int(int(box[1] + box[3] / 2) * 10 /
                         binary_image.shape[0]) for box in boxes]
        return "".join(map(str, exam_code))
