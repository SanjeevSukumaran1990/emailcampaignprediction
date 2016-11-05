# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 19:19:11 2016

@author: sanjeev sukumaran
"""
#return path

import pandas as pd
import matplotlib.pyplot as plt

#loading data as dataframe
input=pd.read_csv("assessment_challenge.csv")
print(input)

print(input.describe())
#checking for missing data
input.isnull().sum()
input
'''
Below is the result
id                               0
read_rate                        0
from_domain_hash                 0
Domain_extension                 5
day                              1
campaign_size                    1
unique_user_cnt                  1
avg_domain_read_rate             1
avg_domain_inbox_rate            1
avg_user_avg_read_rate           1
avg_user_domain_avg_read_rate    1
mb_superuser                     1
mb_engper                        1
mb_supersub                      1
mb_engsec                        1
mb_inper                         1
mb_insec                         1
mb_unengsec                      1
mb_idlesub                       1
'''
len(input.index)
#identify row with all nulls
null_data = input[input.isnull().any(axis=1)]
null_data
input.drop_duplicates(subset=['id'], keep='last')
# remvoving row 59975,since all the rows were missing
input.drop(input.index[['59975']],inplace=True)

len(input.index)

print(input.describe())

#check distribution of data
input.hist()
#see correlation between the data

plt.matshow(input.corr())


def plot_corr(df,size=10):
    '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot'''

    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    labels=['id','RR','C_S','U_U_C','A_D_R_R','a_d_i_r','a_d_a_r_r','a_u_d_a_r_r','mb_s','mb_e','mb_sub','mb_esec','mb_inp','mb_insec','mb_uneng','mb_idles']
    ax.set_xticklabels(labels,fontsize=10)
    ax.set_yticklabels(labels,fontsize=6)
    ax.matshow(corr)
    
    plt.xticks(range(len(corr.columns)), corr.columns);
    plt.yticks(range(len(corr.columns)), corr.columns);






plot_corr(input,15)


from pandas import scatter_matrix
scatter_matrix(input, diagonal='kde')

san=input.corr()
corr=pd.DataFrame(san)
#plotting categorical variables

san=input.day
san.value_counts().plot(kind='bar')


#looking for unique domains:
len(set(input.from_domain_hash))



#sendex approach





# anova test for weekly data
from statsmodels.formula.api import ols
 
mod = ols('read_rate~day',
                data=input).fit()   
print(mod.summary())

'''
import statsmodels.api as sm
from statsmodels.formula.api import ols
 
mod = ols('read_rate ~ day',
                data=input).fit()
                

print (sm.stats.anova_lm(mod,typ=2))
'''
'''
#Alternate way for anova
import scipy.stats as stats 
groups = input.groupby("day").groups

# Etract individual groups
Mon = input[groups["Mon"]]
Tues= input[groups["Tues"]]
Wed = input[groups["Wed"]]
Thurs = input[groups["Thurs"]]
Fri = input[groups["Fri"]]
Sat = input[groups["Sat"]]
Sun = input[groups["Sun"]]
# Perform the ANOVA
stats.f_oneway(Mon, Tues, Wed, Thurs, Fri,Sat,Sun)
'''


input=input.set_index(['id'])
#Delete website related information

input.drop('from_domain_hash', axis=1, inplace=True)
input.drop('Domain_extension', axis=1, inplace=True)

# convert week variables into dummy variables

input_day = pd.get_dummies(input['day'])
input= pd.concat([input,input_day], axis=1)
input
'''
#drop variable for day
input.drop('day',axis=1,inplace=True)

#seperating the output from input
read_rate=input.read_rate
input.drop('read_rate', axis=1, inplace=True)

'''
#sendex approach
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



'''

# performing minmax transformation on data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
input_scaled = pd.DataFrame(scaler.fit_transform(input), columns=input.columns)
input_scaled

input_scaled.hist()

#standaridizing data with gaussian distribution
from sklearn.preprocessing import StandardScaler


scaler=StandardScaler()
input_scaled = pd.DataFrame(scaler.fit_transform(input_scaled), columns=input_scaled.columns)

input_scaled.hist()
# summarize transformed data
read_rate=pd.Series(read_rate)
input_scaled["read_rate"]=read_rate.values

id=pd.Series(id)
input_scaled["id"]=id.values

#removing campaign size to avoid the problem of multicollinearity

input_scaled.drop('unique_user_cnt', axis=1, inplace=True)

#crossvalidation

from sklearn import cross_validation

features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(input_scaled.iloc[:,0:20], input_scaled['read_rate'], test_size=0.3, random_state=0)


#running regression
from sklearn import  linear_model

regr = linear_model.LinearRegression()
regr.fit(features_train, labels_train)

print(regr.coef_)
regr.summary()
regr.score(features_test, labels_test)




#using statsmodel

from sklearn import svm


regr = svm.SVR()
regr.fit(features_train, labels_train)
print(regr.coef_)
regr.score(features_test, labels_test)

'''




