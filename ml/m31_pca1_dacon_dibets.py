import numpy as np
import pandas as pd
from sklearn.datasets import load_iris,load_diabetes
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import random
# 1.데이터
# 1.1 경로, 가져오기
path = 'c:/study/_data/dacon_diabets/'

train_csv = pd.read_csv(path + 'train.csv', index_col=0)
test_csv = pd.read_csv(path + 'test.csv', index_col=0)

# 1.2 확인사항 5가지
print(train_csv.shape, test_csv.shape) #(652, 9) (116, 8)
print(train_csv.columns, test_csv.columns)
print(train_csv.info(), test_csv.info())
print(train_csv.describe(), test_csv.describe())
print(type(train_csv), type(test_csv))

# 1.3 결측지 제거
train_csv = train_csv.dropna()

# 1.4 x, y 분리
x = train_csv.drop(['Outcome'], axis=1)
y = train_csv['Outcome']

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=1234, shuffle=True)

def model(x, y, label=''):
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=1234, shuffle=True)
    model = RandomForestRegressor(n_estimators=200, max_depth=20)
    model.fit(x_train, y_train)
    if label:
        print(label + ' 결과')
    print('model score: ' + str(model.score(x_test, y_test)))

# run the model with the original dataset
model(x, y, 'PCA 전')

# apply PCA and run the model again
pca = PCA(n_components=7)
x = pca.fit_transform(x)
print(x.shape)

model(x, y, 'PCA 후')

# PCA이전 결과
# model score : 0.4266586810686236
# (442, 10)
# (442, 7)
# PCA이후 결과
# model score : 0.41876123994258885