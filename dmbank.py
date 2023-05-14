# -*- coding: utf-8 -*-
"""DMBank.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XdL3UlixNATDZ75kMgkQ3giNhV-cqp4g
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering

Orgdf = pd.read_csv (r'/content/drive/MyDrive/DM/bank_transactions.csv',index_col=False)
Orgdf.head()

from scipy.spatial.distance import pdist, squareform

Orgdf.describe()



Orgdf.info()
# total row is around 1,000,000

#checking null values

Orgdf.isnull().sum()
# we can see Customer Account balance is around 2370 null values

# we can drop the row with null value in Customer Account Balances
# and for Customer DOB and Location we can fill it with 0
df=Orgdf
df.CustGender.fillna(df.CustGender.mode().values[0],inplace=True)
df.CustLocation.fillna(df.CustLocation.mode().values[0],inplace=True)

df.head().T

df=df.dropna(axis=0)
df.info()

# we can drop customer id
df=df.drop(['CustomerID','TransactionID'], axis =1 )

df.info()
# we have 7 columns at last each with 1042802 non-null values

CorMat= df.corr()
for i in range(len(CorMat)):
  CorMat.iloc[i,i]=0

CorMat
plt.figure(figsize=(5,5))
sns.heatmap(CorMat,annot= True)

CorMat.abs().max().sort_values(ascending=False)

# Skewness is a measurement of the distortion of symmetrical distribution or asymmetry in a data set
# It is a positively skewed
skew_col = df.skew().sort_values(ascending=False)
skew_col = skew_col.loc[skew_col>0.75]
print(skew_col)

# Transforming skew data using Log Transformation
for col in skew_col.index.tolist():
  df[col]= np.log1p(df[col])

  # making a df with out TransactionDate,CustGender, CustLocation and CustomerDOB  because we cant convert string to float    
  df2=df.drop(['TransactionDate','CustomerDOB','CustGender','CustLocation' ], axis=1)

#Standardize all column
S= StandardScaler()
        


df2=S.fit_transform(df2)

df2=pd.DataFrame(df2, columns= CorMat.columns)
df2

#Clustering with K Means with n = 10

KM=KMeans(n_clusters=5)
y_pred=KM.fit_predict(df2)
df2['K_Cluster']=y_pred
# Adding it to the dataframe(df)
df['K_Cluster']=y_pred

df.head()

print(df['K_Cluster'].value_counts())

# create a scatter plot with data points colored by cluster
plt.scatter(df2['CustAccountBalance'], df2['TransactionAmount (INR)'], c=df2['K_Cluster'])
plt.scatter(KM.cluster_centers_[:, 0], KM.cluster_centers_[:, 1], c='red',marker='x', s=100)
plt.show()

u_labels = np.unique(df['K_Cluster'])
u_labels

sns.countplot(x=df["K_Cluster"])

sns.scatterplot(data=df, x=df["CustAccountBalance"], y=df["TransactionAmount (INR)"], hue=df["K_Cluster"])