folders = ['alif', 'baa', 'taa', 'seh', 'jiim', 'haa', 'khaa', 'daal', 'zaal', 'raa', 'zeen', 'siin', 'shiin',
               'saad', 'daad', 'tah', 'zaa', 'een', 'ghin', 'faa', 'qaaf', 'kaaf', 'laam', 'miim', 'noon', 'heh', 'waaw', 'yaa',
               'laamalif','yaa2']

import os
os.chdir('C:\\Users\\H S\\PycharmProjects\\arabic_ocr\\test')

for i in range(len(folders)):
    dirname = folders[i]
    os.mkdir(dirname)