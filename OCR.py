import time
import pickle
import numpy as np
from Line_segmentation import GetParagraph_chars, horizintal_projection,vertical_projection
import shutil
import os
import sys
import cv2
from sklearn.preprocessing import StandardScaler
def prepare_output(model_path,img_path):
  char_dic={'alif':'ا','baa':'ب','taa':'ت','seh':'ث','jiim':'ج','haa':'ح',
            'khaa':'خ',
            'daal':'د','zaal':'ذ','raa':'ر','zeen':'ز','siin':'س','shiin':'ش',
            'saad':'ص','daad':'ض','tah':'ط','zaa':'ظ','een':'ع',
            'ghin':'غ','faa':'ف','qaaf':'ق','kaaf':'ك',
            'laam':'ل','miim':'م','noon':'ن','heh':'ه'
            ,'waaw':'و','yaa2':'ي','laamalif':'لا'}
  
  img = cv2.imread(img_path, 0)
  start=time.time()
  word_chars=GetParagraph_chars(img)
  chars2write=[]
  with open(model_path, 'rb') as fid:
    NN_loaded = pickle.load(fid)

  
  w,h=50,50
  imgs=[]
  for i in range(0,len(word_chars)):
     X=np.zeros((0,w,h))
     projections=np.zeros((0,w))
     projections_v=np.zeros((0,h))
     for j in range(0,len(word_chars[i])):
          char=word_chars[i][j]
          char=cv2.resize(char,(50,50))
          imgs.append(char)
          proj=np.array(horizintal_projection(char))
          proj_v=np.array(vertical_projection(char))
          char=np.reshape(char,(1,)+char.shape)
          X=np.concatenate([X,char],axis=0)
          proj=np.reshape(proj,(1,)+proj.shape)
          proj_v=np.reshape(proj_v,(1,)+proj_v.shape)
          projections=np.concatenate([ projections,proj],axis=0)
          projections_v=np.concatenate([ projections_v,proj_v],axis=0)
     
     if(X.shape[0]!=0):
        chars_labels=[]
        X=np.reshape(X,(X.shape[0],X.shape[1]*X.shape[2]))
        X=np.concatenate([X,projections],axis=1)
        X=np.concatenate([X,projections_v],axis=1)
        scaler = StandardScaler()
        scaler.fit(X)
        X= scaler.transform(X)
        #for i in range(0,len(X)):
          #chars_labels.append(NN_loaded.predict([X[i]])[0])
        chars_labels=NN_loaded.predict(X)
        chars2write.append(chars_labels)

     imgs=[]
  end=time.time()
  if(not(os.path.exists("Output"))):
      os.mkdir('Output')
      os.mkdir('Output/text')
  img_name=img_path.split('/')[-1].replace('.png','.txt')
  outputfile='Output/text/'+img_name
 
  
  with open(outputfile,'w') as f: 
      for i in range(0,len( chars2write)):
        for j in range(0,len(chars2write[i])):
            f.write(char_dic[chars2write[i][j]])
        f.write(' ')
        if(i%8==0):
          f.write('\n')
      print(outputfile+' done')

  with open('Output/run_time.txt','a') as f:
      f.write(str(end-start)+'\n')


 

 

 

def RunOCR(testfile):
  path=testfile
  tests=os.listdir(path)
  
  for test in tests:
    image_path=path+'/'+test
    prepare_output('models/my_dumped_classifier.pkl',image_path)



if __name__ == "__main__":
    filename=sys.argv[1]
    RunOCR(filename)
   
 
