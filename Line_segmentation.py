import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
from newChar import get_characters
from WordSegmentor import WordSegmentor
from LineSegmentor import LineSegmentor
from padding import pad

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

def Trim(projection, image, tolerance, min_accepted):
    lines = []
    i = 0
    # print(projection)
    while i < len(projection):
        if projection[i] != 0:
            count = 0
            start = i
            end = i
            threshold = 0
            while end < len(projection) and threshold <= tolerance:
                end += 1
                count += 1
                if end < len(projection) and projection[end] == 0:
                    threshold += 1
                    
            if count > min_accepted: lines.append(image[start:end, 0:len(image[0])])
            i = end

        else:
            i += 1

    return lines


def get_words(lines):
    Lines_in_words = []
    writer = 0
    for i in range(len(lines)):
        lines[i] = cv2.rotate(lines[i], cv2.ROTATE_90_COUNTERCLOCKWISE)
        words = Trim(horizintal_projection(lines[i]), lines[i], 1, 5)   
        for k in range(len(words)):
            words[k] = cv2.rotate(words[k], cv2.ROTATE_90_CLOCKWISE)

        Lines_in_words.append(words)

        # for visualization
        # for j in range(len(words)):
        #     name = 'w' + str(writer) + '.png'
        #     cv2.imwrite(name, words[j])
        #     writer += 1
    return Lines_in_words



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

def segment_paragragh(lines, words):

    # img = cv2.imread('image.png',0)
  #  img = skew_correction(img)
    #  Extract Lines from text
 #   lines = LineSegmentor(img).segment_lines()
    #for i in range(len(lines)):
    #    lines[i] = cv2.rotate(lines[i], cv2.ROTATE_90_CLOCKWISE)
    #for i in range(len(lines)):
    #    lines[i] = skew_correction(lines[i])
    #  Extract words from lines
#    words = WordSegmentor(lines).segment_words()

    #  Extract letters from words

    
    # chars = get_characters(lines, words)
    # res = []
    # for i in range(len(chars)):
      #   for j in range(len(chars[i])):
        #     for k in range(len(chars[i][j])):
          #       chars[i][j][k] = pad(chars[i][j][k])
                
    # for i in range(len(chars)):
      #   for j in range(len(chars[i])):
        #     res.append(chars[i][j])

    # return res
 

def GetParagraph_chars(img):
    img = skew_correction(img)
    lines, lines_dil = LineSegmentor(img).segment_lines()
    words, length = WordSegmentor(lines, lines_dil).segment_words() 
    return get_characters(lines, words)

