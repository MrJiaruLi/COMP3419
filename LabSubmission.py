
import numpy as np
import cv2
import sys
import math
import os

readImgFolder = 'img'

outputImgFolder = 'boundary'

if not os.path.exists(readImgFolder):
    os.makedirs(readImgFolder)

if not os.path.exists(outputImgFolder):
    os.makedirs(outputImgFolder)

# Input the video you want to generate the motion detection
cap = cv2.VideoCapture("monkey.mov")

if not cap.isOpened():
    print("Video is not opened")
    sys.exit(1)

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

block_size = 9;

print("Frame height: ", frame_height, " Frame Width: ", frame_width)

# This function is used to calculate the sum squard distance (SSD)
def MAD(current, previous):

    result = (((previous - current)**2).sum())**(1/2)

    return result

# This is the function used to draw the arrow based on two pixel's coordinate
def arrowDraw(img, x1, x2, y1, y2):

    radians = math.atan2(x1-x2, y2-y1)

    x11 = 0
    y11 = 0
    x12 = -10
    y12 = -10
    u11 = 0
    v11 = 0
    u12 = 10
    v12 = -10

    x11_ = x11 * math.cos(radians) - y11 * math.sin(radians) + x2
    y11_ = x11 * math.sin(radians) + y11 * math.cos(radians) + y2

    x12_ = x12 * math.cos(radians) - y12 * math.sin(radians) + x2
    y12_ = x12 * math.sin(radians) + y12 * math.cos(radians) + y2

    u11_ = u11 * math.cos(radians) - v11 * math.sin(radians) + x2
    v11_ = u11 * math.sin(radians) + v11 * math.cos(radians) + y2

    u12_ = u12 * math.cos(radians) - v12 * math.sin(radians) + x2
    v12_ = u12 * math.sin(radians) + v12 * math.cos(radians) + y2

    img = cv2.line(img, (x1,y1), (x2,y2), (255,0,0), 5)
    img = cv2.line(img, (int(x11_), int(y11_)), (int(x12_),int(y12_)), (255, 0, 0), 5)
    img = cv2.line(img, (int(u11_), int(v11_)), (int(u12_), int(v12_)), (255, 0, 0), 5)

    return img

# To get the block of the image with given blocksize
def getSubImage(img, center, blocksize):
    height = img.shape[0]
    width = img.shape[1]

    x, y = int(center[1]), int(center[0])

    half = int(blocksize/2)

    if x + half >= width:
        x = width - half - 1

    if x < half:
        x = half

    if y + half >= height:
        y = height - half - 1

    if y < half:
        y = half

    return img[y - half : y + half + 1, x - half : x + half + 1]

# Implement the search algorithm called three step search, used to find the similar block among two frames
def ThreeStepSearch(currentSub, previous, center, S, blocksize):

    if S < 1:
        return center

    itself = (int(center[0]), int(center[1]))
    itselfSubimg = getSubImage(previous, itself, blocksize)

    top = (int(center[0]- S), int(center[1]))
    topsubimg = getSubImage(previous, top, blocksize)

    bottom = (int(center[0] + S), int(center[1]))
    b_subimg = getSubImage(previous, bottom, blocksize)

    left = (int(center[0]), int(center[1] - S))
    l_subimg = getSubImage(previous, left, blocksize)

    right = (int(center[0]), int(center[1] + S))
    r_subimg = getSubImage(previous, right, blocksize)

    topleft = (int(center[0] - S), int(center[1] - S))
    tl_subimg = getSubImage(previous, topleft, blocksize)

    topright = (int(center[0] - S), int(center[1] + S))
    tr_subimg = getSubImage(previous, topright, blocksize)

    bottomleft = (int(center[0] + S), int(center[1] - S))
    bl_subimg = getSubImage(previous, bottomleft, blocksize)

    bottomright = (int(center[0] + S), int(center[1] + S))
    br_subimg = getSubImage(previous, bottomright, blocksize)

    rIt = MAD(currentsunImg, itselfSubimg)

    rTop = MAD(currentSub, topsubimg)

    rBot = MAD(currentSub, b_subimg)

    rL = MAD(currentSub, l_subimg)

    rR = MAD(currentSub, r_subimg)

    rTL = MAD(currentSub, tl_subimg)

    rTR = MAD(currentSub, tr_subimg)

    rBL = MAD(currentSub, bl_subimg)

    rBR = MAD(currentSub, br_subimg)

    sequence = (itself, top, bottom, left, right, topleft, topright, bottomleft, bottomright)

    result = (rIt, rTop, rBot, rL, rR, rTL, rTR, rBL, rBR)

    idx = result.index(min(result))

    center = sequence[idx]

    S = S / 2

    return ThreeStepSearch(currentSub, previous, center, S, blocksize)

# Another search method by going through each block that is within a limited radius
# Below the radius is 6
def neighborblock(currentSub, previous, center,block_size):

    min_center = None
    min_dis = 10000

    for y in range (-3,4):
        for x in range(-3,4):
            temp_center = (center[0] + y, center[1] + x)

            tempSub = getSubImage(previous, temp_center, block_size)

            temp_val = MAD(currentSub, tempSub)

            if (temp_val < min_dis):
                min_dis = temp_val
                min_center = temp_center

    return min_center, min_dis


# Extract each frame of the video and store in the folder, for the further comparasion

count = 0

while(1):
    ret, frame = cap.read()

    if not ret:
        print("Video reached end")
        break;


    cv2.imwrite("img/frame%d.tif" % count, frame)

    cv2.imshow("Monkey Frame", frame)

    count = count + 1

    if cv2.waitKey(30) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


count_pre = 0
count_cur = 1

# Get the previous and current frame and store the modified frame into a folder

while (1):

    previous = cv2.imread("img/frame%d.tif" % count_pre)

    current = cv2.imread("img/frame%d.tif" % count_cur)

    modify = np.copy(current)

    if previous is None:
        print("Previous Frame is not found")
        break

    if current is None:
        print("Current Frame is not found")
        break

    for y in range (0, frame_height, block_size):
        for x in range (0, frame_width, block_size):

            center = (y + int(block_size/2), x + int(block_size/2))

            currentsunImg = getSubImage(current, center, block_size)

            # Using Search radius block Search algorithm
            # displacement_center, difference = neighborblock(currentsunImg, previous, center, block_size)

            # Three Step Search algorithm
            displacement_center = ThreeStepSearch(currentsunImg, previous, center, 4, block_size)

            displacementImg = getSubImage(previous, displacement_center, block_size)

            difference = MAD(currentsunImg, displacementImg)

            if difference > 60:
                modify[center[0], center[1]] = [255, 255, 255]


    # used to add the boundary to the object that moves most.

    kernel = np.ones((10, 10), np.uint8)

    dilation = cv2.dilate(modify, kernel, iterations = 3)

    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

    closing = cv2.cvtColor(closing, cv2.COLOR_BGR2GRAY)

    ret, binary = cv2.threshold(closing, 240, 255, cv2.THRESH_BINARY)


    im_back, countours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(modify, countours, -1, (255, 255, 255), 1)

    cv2.imshow("Modify", modify)

    print("Center: ", center[0], " x ", center[1])
    print("Difference", difference)

    cv2.imwrite("boundary/frame%d.tif" % count_pre, modify)

    count_pre = count_pre + 1

    count_cur = count_cur + 1

    if cv2.waitKey(30) & 0xff == ord('q'):
        break

# Output the video based on the frame that stored previously.
maker = 0
out = cv2.VideoWriter('Boudary_demo.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (int(frame_width), int(frame_height)))
while(1):
    img = cv2.imread('boundary/frame%d.tif' % maker)
    if img is None:
        break;

    out.write(img)
    maker = maker + 1
out.release()
cv2.destroyAllWindows()




