# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 01:27:20 2018
@author: hp1
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sklearn
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import scale
import sklearn.metrics as sm
from sklearn import datasets
from sklearn.metrics import confusion_matrix, classification_report

plt.figure(figsize=(7,4))

iris = datasets.load_iris()

X = scale(iris.data)
y = pd.DataFrame(iris.target)

variable_names = iris.feature_names

print(X[0:10])

clustering = KMeans(n_clusters = 3, random_state=5) # 3 for groups and 5 are random points

clustering.fit(X)

###############ploting#############################

iris_df = pd.DataFrame(iris.data)
iris_df.columns = ['S_length', 'S_width', 'P_length', 'P_width']
y.columns = ['target']

color_theme = np.array(['darkgray', 'lightsalmon', 'powderblue'])

plt.subplot(1,2,1)
plt.scatter(x=iris_df.P_length, y=iris_df.P_width, c=color_theme[iris.target], s=50)
plt.title('Ground Truth Classification')

plt.subplot(1,2,2)
plt.scatter(x=iris_df.P_length, y=iris_df.P_width, c=color_theme[clustering.labels_], s=50)
plt.title('KMeans Classification')

relabel = np.choose(clustering.labels_, [2, 0,1]).astype(np.int64)

plt.subplot(1,2,1)
plt.scatter(x=iris_df.P_length, y=iris_df.P_width, c=color_theme[iris.target], s=50)
plt.title('Ground Truth Classification')

plt.subplot(1,2,2)
plt.scatter(x=iris_df.P_length, y=iris_df.P_width, c=color_theme[relabel], s=50)
plt.title('KMeans Classification')

print(classification_report(y, relabel))