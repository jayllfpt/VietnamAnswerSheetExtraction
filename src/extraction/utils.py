import cv2


def process_img(img, config):

    # DEBUG_DIR = config['DEBUG_DIR']
    # convert image from BGR to GRAY to apply canny edge detection algorithm
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(DEBUG_DIR + "1_gray.jpg", gray_img)

    # clahe remove noise
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray_img)
    # cv2.imwrite(DEBUG_DIR + "2_equalize.jpg", clahe_img)

    # remove noise by blur image
    blur_img = cv2.GaussianBlur(clahe_img, (5, 5), 0)
    # cv2.imwrite(DEBUG_DIR + "3_blur.jpg", blur_img)
    return blur_img
