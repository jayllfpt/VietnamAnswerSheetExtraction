import cv2
import os

from .grid import scale_new_grid, grid_visualize
from .utils import process_img


class AnswerExtract():
    def __init__(self, config):
        self.config = config

    def __call__(self, img):
        ANSWER = self.config['ANSWER']
        PIXEL_THRESHOLD = self.config['PIXEL_THRESHOLD']
        DEBUG_DIR = self.config['ANSWER_DEBUG_DIR']
        if self.config['ANSWER_VISUALIZE']:
            os.makedirs(DEBUG_DIR, exist_ok=True)
            os.makedirs(os.path.join(DEBUG_DIR, "slice"), exist_ok=True)

        # Crop answer area
        h = img.shape[0]
        img = img[int(h * 0.2): int(h * 0.95), :]

        blur_img = process_img(img, self.config)
        # apply canny edge detection algorithm
        canny_img = cv2.Canny(blur_img, 125, 200)
        if self.config['ANSWER_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "4_canny.jpg", canny_img)
        canny_img = cv2.dilate(canny_img, cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
        if self.config['ANSWER_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "5_dilate_canny.jpg", canny_img)

        # Finding contours for the detected edges.
        contours, hierarchy = cv2.findContours(
            canny_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # Keeping only the largest detected contour. select top 7
        boxes_cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:4]
        boxes_img = cv2.drawContours(
            img.copy(), boxes_cnts, -1, (0, 0, 255), 3)
        if self.config['ANSWER_VISUALIZE']:
            cv2.imwrite(DEBUG_DIR + "6_boxes.jpg", boxes_img)

        columns = []
        if len(boxes_cnts) > 0:
            for cnt in boxes_cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                columns.append((x, y, w, h))

        # sort left to right
        columns = sorted(columns, key=lambda x: x[0])
        result = {}

        for column_index, col in enumerate(columns):
            x, y, col_w, col_h = col
            x += 5
            y += 5
            col_w -= 10
            col_h -= 10

            column_img = img.copy()[y:y + col_h, x:x +
                                    col_w]  # crop column img
            grid = scale_new_grid((x, y, col_w, col_h), self.config)
            _img_with_box = column_img.copy()
            if self.config['ANSWER_VISUALIZE']:
                cv2.imwrite(DEBUG_DIR + f"4_{column_index}.jpg",
                            grid_visualize(column_img, grid))
            for box_index, box_grid in enumerate(grid):
                for qindex, qgrid in enumerate(box_grid):
                    question_id = column_index * 30 + box_index * 5 + qindex + 1
                    result[question_id] = []
                    for answer_index, bb in enumerate(qgrid):
                        choice_img = column_img.copy(
                        )[bb[0][1]:bb[3][1], bb[0][0]:bb[2][0]]
                        bubble_choice = cv2.cvtColor(
                            choice_img, cv2.COLOR_BGR2GRAY)
                        bubble_choice = cv2.threshold(
                            bubble_choice, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                        # remove noise after threshold
                        kernel = cv2.getStructuringElement(
                            cv2.MORPH_RECT, (3, 3))
                        bubble_choice = cv2.morphologyEx(
                            bubble_choice, cv2.MORPH_OPEN, kernel, iterations=2)
                        if self.config['ANSWER_VISUALIZE']:
                            cv2.imwrite(os.path.join(
                                DEBUG_DIR, "slice", f"{question_id}_{answer_index}.jpg"), bubble_choice)
                        # print(question_id, answer_index, cv2.countNonZero(bubble_choice))
                        if cv2.countNonZero(bubble_choice) > PIXEL_THRESHOLD:
                            cv2.rectangle(
                                _img_with_box, (bb[0][0], bb[0][1]), (bb[2][0], bb[2][1]), (0, 255, 0), 2)
                            result[question_id].append(ANSWER[answer_index])
                            
        # Delete last character of result
        return result
