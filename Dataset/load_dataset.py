import numpy as np
import sklearn
import os
import pandas as pd
import cv2
from google.colab.patches import cv2_imshow
def load_dataset(path):


  w,h=50,50

  letters_paths=os.listdir(path)

  X=np.zeros((0,w,h))
  Y=np.zeros((0,1))

  dataset=[]
  batch_size=8
  

  
  for i in letters_paths:
    letters_shapes=os.listdir(path+'/'+i)
    count=0
    for j in  letters_shapes:
      if(count<=200):
        path1=path+'/'+i+'/'+j
        print(path1,count)
        label=i
        img1=cv2.imread(path1)
        #img1=crop_img(img1)
        img1=cv2.resize(img1,(50,50))
        img1=cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img1=np.reshape(img1,(1,)+img1.shape)
        X=np.concatenate([X,img1],axis=0)
        Y=np.concatenate([Y,np.array([[label]])],axis=0)
        count+=1
      

     
  
  # img=np.reshape(X[48],(50,50))
  # cv2_imshow(img)
  # print(Y[48])
  X=np.reshape(X,(X.shape[0],X.shape[1]*X.shape[2]))
  return X,Y

X,Y=load_dataset('res')
print(X.shape,Y.shape)
  
