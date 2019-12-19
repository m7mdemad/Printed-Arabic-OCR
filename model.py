from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import random
import matplotlib.pyplot as plt
import pickle
scaler = StandardScaler()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform (X_test)
NN=MLPClassifier(verbose=True,shuffle=True)
NN.fit(X_train,Y_train)

 ##save model
    
with open('classifier.pkl', 'wb') as fid:
    pickle.dump(NN, fid)    


##test model
if __name__ == "__main__":
   
    train_score=NN.score(X_train,Y_train)
    print('train score',train_score)
    test_score=NN.score(X_test,Y_test)
    print('test score',test_score)
    random_idx=random.randrange(0,len(X_test))
    sample=X_test[random_idx]
    sample=np.reshape(sample,((1,)+sample.shape))
    print('prediction',NN.predict(sample),Y_test[random_idx])
    sample=scaler.inverse_transform(sample)
    img=np.reshape(sample,(50,50))
    plt.imshow(img)
    plt.show()


   
