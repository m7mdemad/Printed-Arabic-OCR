import cv2
import numpy as np
import os
import glob
import re
from Line_segmentation import segment_paragragh



img = 'C:\\Users\\H S\\PycharmProjects\\arabic_ocr\\s'
txt = 'C:\\Users\\H S\\PycharmProjects\\arabic_ocr\\t'
results_path = 'C:\\Users\\H S\\PycharmProjects\\arabic_ocr\\test'


def get_char(text_file):
    words = text_file.split()
    chars = [[] for i in range(len(words))]
    for i in range(0, len(words)):
        for j in range(0, len(words[i])):
            if  j != 0 and words[i][j] == 'ا' and words[i][j - 1] == 'ل':
                chars[i].pop()
                chars[i].append('لا')
            else:
                chars[i].append(words[i][j])
    print(chars)
    return chars


# def get_img(img):  # omda
#     imgs = []  # array of arrays of chars imgs for each word
#     return imgs


def prepare_dataset(imgs, chars):
    data = []
    count = 0  # number of errors :D
    j = 0
    for arr in imgs:
        if j > len(chars) - 1:
            break
        if len(arr) == len(chars[j]):
            for i in range(len(arr)):
                data.append([arr[i], chars[j][i]])
            j += 1
        else:
            #return data
            #j += 1  # skip it.
            #count += 1
            break
        
    k = len(imgs) - 1
    j = len(chars) - 1
    while k >= 0:
        if j < 0:
            break
        if len(imgs[k]) == len(chars[j]):
            for i in range(len(imgs[k])):
                data.append([imgs[k][i], chars[j][i]])
            j -= 1
        else:
            #return data
            #j += 1  # skip it.
            #count += 1
            break
        k -= 1

     #print('no. of errors= ', count)
    return data


def save_data(data, img):
    # if cond only for 7rof rn

    folders = ['alif', 'baa', 'taa', 'seh', 'jiim', 'haa', 'khaa', 'daal', 'zaal', 'raa', 'zeen', 'siin', 'shiin',
               'saad', 'daad', 'tah', 'zaa', 'een', 'ghin', 'faa', 'qaaf', 'kaaf', 'laam', 'miim', 'noon', 'heh', 'waaw', 'yaa',
               'laamalif','yaa2']

    letters = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق',
               'ك', 'ل', 'م', 'ن', 'ه', 'و','ى','لا','ي']

    cnt = 0
    for el in data:
        
        if el[1] in letters:  # :P
            cnt = letters.index(el[1])
            path = results_path + '\\' + folders[cnt]
             #print(path)
            os.chdir(path)
            idx = len(glob.glob(os.path.join(path, '*.png')))
            cv2.imwrite('%d.png' % idx, el[0])
        else:
             print('wtf is this ha? ', el[1])
    return


numbers = re.compile(r'(\d+)')


def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


imgs = []
for filename in sorted(glob.glob(os.path.join(img, '*.png')), key=numericalSort):
    print(filename)
    _imgs = cv2.imread(filename, 0)
    imgs.append(_imgs)

text = []
for filename in sorted(glob.glob(os.path.join(txt, '*.txt')), key=numericalSort):
    with open(filename, 'r', encoding='utf-8') as f:
        _text = f.read()
        print(filename)
        text.append(_text)

for i in range(len(text)):
    lt_txt = get_char(text[i])
    lt_img = segment_paragragh(imgs[i])
    data = prepare_dataset(lt_img, lt_txt)
    save_data(data,img)