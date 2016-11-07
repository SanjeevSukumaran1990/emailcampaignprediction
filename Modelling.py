from sklearn import preprocessing,cross_validation
import numpy as np
from sklearn.linear_model import LinearRegression

X=np.array(input.drop(['read_rate'],1))
y=np.array(input['read_rate'])
X=preprocessing.scale(X)

X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)



clf=LinearRegression()
clf.fit(X_train,y_train)

clf.score(X_test,y_test)



#without scaling

from sklearn import preprocessing,cross_validation
import numpy as np
from sklearn.linear_model import LinearRegression

X=np.array(input.drop(['read_rate'],1))
y=np.array(input['read_rate'])


X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)

clf=LinearRegression()
clf.fit(X_train,y_train)

clf.score(X_test,y_test)


