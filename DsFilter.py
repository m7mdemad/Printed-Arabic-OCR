s = 'C:\\Users\\H S\\PycharmProjects\\arabic_ocr\\r\\zaa'
d = 'C:\\Users\\H S\\PycharmProjects\\arabic_ocr\\res\\zaa'

import cv2
import numpy as np
import os
import glob
import re

numbers = re.compile(r'(\d+)')

def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def operation(src, dst, write):
    imgs = []
    for filename in sorted(glob.glob(os.path.join(dst, '*.png')), key=numericalSort):
        #print(filename)
        _imgs = cv2.imread(filename, 0)
        imgs.append(_imgs)
    
    pxCount = []
    for x in imgs:
        temp = np.count_nonzero(x != 255)
        if temp not in pxCount:
            pxCount.append(temp)
    
    
    print(pxCount)
    test = []
    for filename in sorted(glob.glob(os.path.join(src, '*.png')), key=numericalSort):
        #print(filename)
        _imgs = cv2.imread(filename, 0)
        test.append(_imgs)
    
    results = []
    px = []
    coco = 0
    for x in test:
        count = np.count_nonzero(x != 255)
        px.append(count)
        threshold = 1
        for i in range(-threshold, threshold):
            if count + i in pxCount:
                coco += 1
                results.append(x)
                break
        
        
    print(px)
        
    
    print(coco,'match were found')
    i = 0
    for x in results:
         idx = len(glob.glob(os.path.join(write, '*.png')))
         cv2.imwrite('%d.png' % idx, x)
         i += 1
         
         
folders = ['alif', 'baa', 'taa', 'seh', 'jiim', 'haa', 'khaa', 'daal', 'zaal', 'raa', 'zeen', 'siin', 'shiin',
               'saad', 'daad', 'tah', 'zaa', 'een', 'ghin', 'faa', 'qaaf', 'kaaf', 'laam', 'miim', 'noon', 'heh', 'waaw', 
               'laamalif','yaa2']

for x in folders:
    operation(s+x, d+x, d+x)
