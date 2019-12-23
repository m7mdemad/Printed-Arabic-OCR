import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
from newChar import get_characters


def horizintal_projection(im):
    #im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im = 255 - im  # invert
    projection = np.sum(im, 1)  # Calculate horizontal projection
    return projection

def vertical_projection(im):
    #im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im = 255 - im  # invert
    projection = np.sum(im, 0)  # Calculate horizontal projection
    return projection

def skew_correction(image):
    gray = cv2.bitwise_not(image)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated




def segment_lines(img):
    hist = np.sum(255 - img, axis=1)
    i = 0
    lines = []
    while i < len(hist):
        if hist[i] != 0:
            x, y = i, i
            while y < len(hist):
                y += 1
                if y < len(hist) and hist[y] == 0:
                    break
            lines.append(img[x:y, 0:len(img[0])])
            i = y
        else:
            i += 1
    kernel = np.ones((2, 2), np.uint8)

    lines_dil = []
    for i in range(len(lines)):
        x = cv2.dilate(lines[i], kernel, iterations=1)
        lines_dil.append(x)

    return lines,lines_dil



def find_gaps(line, threshold=2):
    hist = np.sum(255 - line, axis=0)
    gaps = []
    i = 0
    while i < len(hist):
        if hist[i] == 0:
            y = i + 1
            while True:
                if y < len(hist) and hist[y] == 0:
                    y += 1
                else:
                    if y - i > threshold:
                        gaps.append([i, y - 1])
                    break
            i = y
            continue
        i += 1
    return gaps

def segment_words_of_line(line, line_dil):
    gaps = find_gaps(line_dil)
    words = []
    for i in range(0, len(gaps) - 1):
        words.append(line[::, gaps[i][1]:gaps[i+1][0]])
    if len(line[0]) - 1 - gaps[-1][1] > 0:
        words.append(line[::, gaps[-1][1]:])
    if gaps[0][0] != 0:
        words.insert(0, line[::, 0:gaps[0][0]])
    words.reverse()
    return words


def segment_words(lines,lines_dil):
        line_words = []
        length = 0
        for line_idx, line in enumerate(lines):
            words = segment_words_of_line(line, lines_dil[line_idx])
            length += len(words)
            line_words.append(words)

        return line_words, length
 

def GetParagraph_chars(img):
    img = skew_correction(img)
    lines, lines_dil = segment_lines(img)
    words, length = segment_words(lines, lines_dil)
    return get_characters(lines, words)