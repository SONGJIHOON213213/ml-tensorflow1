import numpy as np
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split


#1. 데이터
datasets = load_wine()
print(datasets.feature_names)
x = datasets['data']
y = datasets.target 

pca = PCA(n_components=5)
x = pca.fit_transform(x)
print(x)
print(x.shape)

x_train,x_test,y_test,y_train = train_test_split(
    x, y ,    
) 
#2.모델
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(random_state=1234)

#3.훈련
model.fit(x_train,y_train)

#4.평가,예측
result = model.score(x_test,y_test)
print("결과: ",result)