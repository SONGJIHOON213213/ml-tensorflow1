from bayes_opt import BayesianOptimization
from lightgbm import LGBMRegressor
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')
import time
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score

#1 데이터
# 1.1 경로, 가져오기
path = 'c:/study/_data/kaggle_bike/'
df = pd.read_csv(path + 'train.csv', index_col=0)
train_csv = pd.read_csv(path + 'train.csv', index_col=0)

# 1.2 train, test split
x = df.iloc[:, :-1]
y = df.iloc[:, -1]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, random_state=123, train_size=0.8, shuffle=True, stratify=y
)

# 1.3 결측치 처리
num_cols = x_train.select_dtypes(include=np.number).columns
x_train[num_cols] = x_train[num_cols].fillna(x_train[num_cols].median())
x_test[num_cols] = x_test[num_cols].fillna(x_train[num_cols].median())

# 1.4 라벨인코딩
le = LabelEncoder()
for i in x_train.columns:
    if x_train[i].dtype == 'object':
        x_train[i] = le.fit_transform(x_train[i])
        x_test[i] = le.transform(x_test[i])

print(len(x_train.columns))
print(x_train.info())
print(x_test.info())

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

model = BaggingClassifier(
    n_estimators=12,
    n_jobs=-1,
    random_state=337,
    bootstrap=True
)
lgbm_bayesian_params = {'n_estimators' : (100, 500),
                        'learning_rate' : (0.3, 0.7),
                        'max_depth' : (3, 16),
                        'num_leaves' : (24, 64),
                        'min_child_samples' : (10, 200),
                        'min_child_weight' : (1, 50),
                        'subsample' : (0.5, 1), # 0 ~ 1 사이
                        'colsample_bytree' : (0.5, 1),
                        'max_bin' : (10, 500),
                        'reg_lambda' : (-0.001, 10), # 
                        'reg_alpha' : (0.01, 50)}

def lgb_hamsu(n_estimators, learning_rate, max_depth, num_leaves, min_child_samples, min_child_weight, subsample, colsample_bytree, max_bin, reg_lambda, reg_alpha):
    params = {'n_estimators' : int(n_estimators), # 무조건 정수형
              'learning_rate' : learning_rate,
              'max_depth' : int(round(max_depth)), # 무조건 정수형
              'num_leaves' : int(round(num_leaves)), # 무조건 정수형
              'min_child_samples' : int(round(min_child_samples)), # 무조건 정수형
              'min_child_weight' : int(round(min_child_weight)), # 무조건 정수형
              'subsample' : max(min(subsample, 1), 0), # 0 ~ 1 사이 min() 1보다 작은값, max() 0보다 큰값
              'colsample_bytree' : colsample_bytree,
              'max_bin' : max(int(round(max_bin)), 10), # max_bin와 10을 비교해서 가장 높은 값을 뽑아준다. # 무조건 정수형
              'reg_lambda' : max(reg_lambda, 0), # 무조건 양수만 나온다.
              'reg_alpha' : reg_alpha}
    
    model = LGBMRegressor(**params)
    
    model.fit(x_train, y_train,
              eval_set = [(x_train, y_train), (x_test, y_test)],
              eval_metric = 'rmse',
              verbose = 0,
              early_stopping_rounds = 50)
    
    y_predict = model.predict(x_test)
    results = r2_score(y_test, y_predict)
    return results

lgb_bo = BayesianOptimization(f = lgb_hamsu,
                              pbounds = lgbm_bayesian_params,
                              random_state = 1234)
s_time = time.time()
n_iter = 500
lgb_bo.maximize(init_points = 5, # 초기점
                n_iter = n_iter) # 총 105번
e_time = time.time()
print(lgb_bo.max)
print(n_iter, '번 걸린시간 : ', e_time - s_time)