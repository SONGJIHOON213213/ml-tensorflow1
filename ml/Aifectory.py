import numpy as np
import pandas as pd
import glob
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import time
from sklearn.metrics import mean_absolute_error,r2_score

#1-1경로 생성.
path = 'c:/study/_data/aifact_05/'
path_save = 'c:/study/_data/aifact_05/'
train_files = glob.glob(path + "TRAIN/*.csv") 
test_input_files = glob.glob(path + "test_input/*.csv")

###################################train폴더##########################################
li = [] #리스트 값 저장.
for filename in train_files:
    df = pd.read_csv(filename, index_col=None, header= 0, #-> header= 0맨위에 행 제거
                     encoding='utf-8-sig') #'utf-8-sig'가 한글로 인코딩 해주는거
    
    li.append(df)

train_dataset = pd.concat(li, axis=0,
                          ignore_index=True) #인덱스 제거

#####################################test폴더###########################################
li = []
for filename in test_input_files:
    df = pd.read_csv(filename, index_col=None, header= 0,
                     encoding='utf-8-sig')
    
    li.append(df)

test_dataset = pd.concat(li, axis=0,
                          ignore_index=True) #인덱스 제거
#print(test_dataset) #[131376 rows x 4 columns]

###################################측정소 라벨인코더##########################################
le = LabelEncoder()
train_dataset['locate'] = le.fit_transform(train_dataset['측정소'])
test_dataset['locate'] = le.transform(test_dataset['측정소']) 

#print(train_dataset) #[596088 rows x 5 columns]
#print(test_dataset) #[131376 rows x 5 columns]
#print("=======================드랍후=============================")
train_dataset = train_dataset.drop(['측정소'], axis = 1)
test_dataset = test_dataset.drop(['측정소'], axis = 1)
#print(train_dataset) #[596088 rows x 4 columns]
#print(test_dataset) #[131376 rows x 4 columns]

################################일시 -> 월,일 시간으로 분리 ##################################

train_dataset['Month'] = train_dataset['일시'].str[:2]
train_dataset['hour'] = train_dataset['일시'].str[6:8]

test_dataset['Month'] = test_dataset['일시'].str[:2]
test_dataset['hour'] = test_dataset['일시'].str[6:8]

#일시 드랍.
train_dataset = train_dataset.drop(['일시'], axis = 1)
test_dataset = test_dataset.drop(['일시'], axis = 1)

###str -> int
train_dataset['Month'] = pd.to_numeric(train_dataset['Month']).astype('int16')
train_dataset['hour'] = pd.to_numeric(train_dataset['hour']).astype('int16')

test_dataset['Month'] = pd.to_numeric(test_dataset['Month']).astype('int16')
test_dataset['hour'] = pd.to_numeric(test_dataset['hour']).astype('int16')

train_dataset = train_dataset.dropna()

y = train_dataset['PM2.5']
x = train_dataset.drop(['PM2.5'], axis = 1)
print(x.shape, '\n', y.shape) 

x_train, x_test, y_train, y_test = train_test_split(
    x, y, shuffle= True, train_size= 0.75, random_state=24
)

parameter =  {
    "n_estimators" : 1000, # 디폴트 100 / 1 ~ inf / 정수
    "learning_rate" : 0.3, # 디폴트 0.3 / 0 ~ 1 / eta
    "max_depth" : 10, # 디폴트 6 / 0 ~ inf / 정수
    # "gamma" : 1, # 디폴트 0 / 0 ~ inf 
    # "min_child_weight" : 1, # 디폴트 1 / 0 ~ inf 
    # "subsample" : 3, # 디폴트 1 / 0 ~ 1 
    # "colsample_bytree" : 1, # 디폴트 / 0 ~ 1 
    # "colsample_bylevel":1, # 디폴트 / 0 ~ 1 
    # "colsample_bynode":1, # 디폴트 / 0 ~ 1 
    # "reg_alpha":0, # 디폴트 0 / 0 ~ inf / L1 절대값 가중치 규제 / alpha
    # "reg_lambda":1, # 디폴트 1 / 0 ~ inf / L2 제곱 가중치 규제 / lambda
    # "random_state":3377, # 디폴트 1 / 0 ~ inf / L2 제곱 가중치 규제 / lambda
    # "verbose":0, 
    "n_jobs" : -1
}

model = XGBRegressor()

#3. 컴파일, 훈련
model.set_params(
    **parameter,
    eval_metric='mae',
    early_stopping_rounds=50
)
start = time.time()
model.fit(x_train, y_train,
          eval_set=[(x_train, y_train), (x_test, y_test)],
          )
end = time.time()

#4.평가, 예측
results = model.score(x_test, y_test)
print("걸린 시간 : ", round(end -start, 2), "초")

#4.평가, 예측

y_predict = model.predict(x_test)

results = model.score(x_test, y_test)
print("model_score :", results)

r2 = r2_score(y_test,y_predict)
print("r2스코어 :", r2)

mae = mean_absolute_error(y_test,y_predict)
print("mae :", mae)

#print(train_dataset.shape, test_dataset.shape)
print(x_train)
#파일저장.
predict_y = test_dataset[test_dataset['PM2.5'].isnull()].drop('PM2.5', axis=1)
y_submit = model.predict(predict_y)
y_submit = y_submit.round(3)
submission = pd.read_csv(path + 'answer_sample.csv',index_col= 0)
submission['PM2.5'] = y_submit
submission.to_csv(path_save + '05023.csv') 

