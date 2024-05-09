import cv2
from math import ceil
import yaml


def gen_bubble(top_left, size):
    x, y = top_left
    return [(x, y), (x+size, y), (x+size, y+size), (x, y+size)]


def right(point, dist):
    return (point[0] + dist, point[1])


def bot(point, dist):
    return (point[0], point[1] + dist)


def build_question_grid(first, bubble_dist, bubble_radius):
    return [gen_bubble(right(first, bubble_dist * i), bubble_radius) for i in range(4)]


def build_box_grid(top_left,  question_dist, bubble_dist,  bubble_radius):
    return [build_question_grid(bot(top_left, question_dist * i), bubble_dist,  bubble_radius) for i in range(5)]


def build_column_grid(top_left, box_dist, question_dist, bubble_dist,  bubble_radius):
    return [build_box_grid(bot(top_left, box_dist * i),  question_dist, bubble_dist,  bubble_radius) for i in range(6)]


def build_page_grid(top_left, column_dist, box_dist, question_dist, bubble_dist,  bubble_radius):
    return [build_column_grid(right(top_left, column_dist * i), box_dist, question_dist, bubble_dist,  bubble_radius) for i in range(4)]


def grid_visualize(img, grid):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        COLOR = config['GRID_COLOR']
        THICKNESS = config['GRID_THICKNESS']

    vimg = img.copy()
    # for column_grid in grid:
    for box_grid in grid:
        for qgrid in box_grid:
            for bb in qgrid:
                cv2.rectangle(vimg, bb[0], bb[2], COLOR, THICKNESS)
    return vimg


def scale_new_grid(column, config):
    col_width = config['COL_WIDTH']
    col_height = config['COL_HEIGHT']
    top1a = config['TOP_1A']
    left1a = config['LEFT_1A']
    size = config['BUBBLE_SIZE']
    bubble_dist = config['BUBBLE_DIST']
    question_dist = config['QUESTION_DIST']
    box_dist = config['BOX_DIST']


    x, y, w, h = column
    size = 23
    q1x = ceil(top1a * w / col_width)
    q1y = ceil(left1a * h / col_height)
    bbdis = ceil(bubble_dist * w / col_width)
    qdis = ceil(question_dist * h / col_height)
    boxdis = ceil(box_dist * h / col_height)
    
    grid = build_column_grid((q1x, q1y), boxdis, qdis, bbdis, size)
    return grid


if __name__ == "__main__":
    img_path = r"img\template.png"
    # img = cv2.imread(img_path)
    # grid = build_page_grid(top_left, coldist, boxdist, qdist, bbdist, r)
    # cv2.imwrite(r"debug\7_grid.jpg", visualize(img, grid))
    scale_new_grid((81, 505, 198, 908))
    