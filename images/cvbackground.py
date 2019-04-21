import face_recognition
import cv2 as cv
import numpy as np
from os import mkdir
import pickle
filename = '../static/IMG_1117.JPG'
thickness =9
alpha = 120

def get_watercolour_image(filename,thickness,alpha,username):
    file = open("heeracurves.obj", 'rb')
    heera_face = pickle.load(file)
    file.close()
    print("done")
    src = cv.imread(filename)
    if src is None:
        print('Could not open or find the image:')
        exit(0)
    try:
        mkdir("photo/"+username)
    except:
        pass
    # Convert image to gray and blur it
    h, w = src.shape[:2]
    scale = 980.0 / w
    h = int(scale * h)
    src = cv.resize(src, (980, h), interpolation=cv.INTER_AREA)
    cv.imwrite("photo/"+username+"/girl.png", src)
    src_gray = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    src_gray = cv.blur(src_gray, (3, 3))
    # Create Window

    threshold = 0
    # Detect edges using Canny
    image = face_recognition.load_image_file("photo/"+username+"/girl.png")
    unknown_face_encoding = face_recognition.face_encodings(image)[0]
    print('done')
    results = face_recognition.compare_faces([heera_face], unknown_face_encoding)
    face_locations = face_recognition.face_locations(image)
    face1 = face_locations[0]
    y1, x1, y2, x2 = face1
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    # Find contours
    contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    p = []
    LENGTH = len(contours)
    for i, cnt in enumerate(contours):
        x, y, w, h = cv.boundingRect(cnt)  # offsets - with this you get 'mask'
        color = np.array(cv.mean(src[y:y + h, x:x + w])).astype(list)
        ps = []
        for j in color[:3]:
            ps.append(float(j))
        p.append([cnt, ps])
    for i, pro in enumerate(p):
        thickness = 9
        cv.drawContours(drawing, [pro[0]], 0, pro[1], thickness, cv.LINE_AA, hierarchy, 0, )

    s_img = src
    s_img = s_img[y1:y2, x1:x2]

    b_channel, g_channel, r_channel = cv.split(s_img)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * alpha  # creating a dummy alpha channel image.

    s_img = cv.merge((b_channel, g_channel, r_channel, alpha_channel))

    l_img = drawing


    alpha_s = s_img[:, :, 3] / 255
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] + alpha_l * l_img[y1:y2, x1:x2, c])
    cv.imwrite("photo/"+username+"/final1.png", l_img)
    return results[0]
# Load source image