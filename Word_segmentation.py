import cv2
import numpy as np
import time
def horizintal_projection(img):
    im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im = 255 - im                               # invert
    projection = np.sum(im, 1)                  # Calculate horizontal projection
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
        words = Trim(horizintal_projection(lines[i]), lines[i], 4, 5)
        for k in range(len(words)):
            words[k] = cv2.rotate(words[k], cv2.ROTATE_90_CLOCKWISE)

        Lines_in_words.append(words)
		
		# for visualization
        for j in range(len(words)):
            name = 'w' + str(writer) + '.png'
            cv2.imwrite(name, words[j])
            writer += 1


img = cv2.imread('image.png')
#  Extract Lines from text
# print(horizintal_projection( cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)))
lines = Trim(horizintal_projection(img), img, 0, 15)
#  Extract words from lines
words = get_words(lines)



