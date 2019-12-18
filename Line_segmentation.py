import cv2
import numpy as np
from newChar import get_characters

def horizintal_projection(im):
    #im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im = 255 - im  # invert
    projection = np.sum(im, 1)  # Calculate horizontal projection
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
        for j in range(len(words)):
            name = 'w' + str(writer) + '.png'
            cv2.imwrite(name, words[j])
            writer += 1
    return Lines_in_words


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

    
    chars = get_characters(lines, words)
    res = []
    for i in range(len(chars)):
        for j in range(len(chars[i])):
            res.append(chars[i][j])
    #        for k in range(len(chars[i][j])):
                # print('writing')
    #            cv2.imwrite('test/l'+str(i)+'w'+str(j)+'c'+str(k)+'.png', chars[i][j][k])

    return res
 

#def tempFunction():
#	img = cv2.imread('img.png', 0)
#	img = skew_correction(img)
#	lines, lines_dil = LineSegmentor(img).segment_lines()
#   words, length = WordSegmentor(lines, lines_dil).segment_words() 
#	return segment_paragragh(lines, words)

#tempFunction()