import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer, load_digits,load_iris,load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import StackingClassifier, StackingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier
from sklearn.ensemble import VotingClassifier #투표

#1. 데이터
datasets = [load_iris,load_breast_cancer, load_digits,load_wine]

for data in datasets:
    dataset_name = data.__name__
    x, y = data(return_X_y=True)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, shuffle=True, train_size=0.8, random_state=1030
    )

    scaler = StandardScaler()
    x_train =  scaler.fit_transform(x_train)
    x_test =  scaler.transform(x_test)

    #2. 모델
    lr = LogisticRegression()
    knn = KNeighborsClassifier(n_neighbors=8)
    dt = DecisionTreeClassifier()

    model = StackingClassifier(
    estimators=[('LR', lr), ('KNN', knn), ('DT', dt)],
    final_estimator=DecisionTreeClassifier()
    # final_estimator=LogisticRegression()
    # final_estimator=RandomForestClassfier()
    # final_estimator=VotingClassifier()
     # 또는 'hard'
    # final_estinator=KNeighborsClassifier(),
)
    #3. 훈련
    model.fit(x_train,y_train)

    #4. 평가, 예측
    y_pred = model.predict(x_test)
    print(f'{dataset_name} 데이터')
    print('Model score : ', model.score(x_test, y_test))
    print("Stacking ACC : ", accuracy_score(y_test, y_pred))
    print()


    Classifiers = [lr, knn, dt]

    for model2 in Classifiers:
        model2.fit(x_train, y_train)
        y_pred = model2.predict(x_test)
        score2 = accuracy_score(y_test, y_pred)
        class_name = model2.__class__.__name__
        print(f"{dataset_name} 데이터 {class_name} 정확도 : {score2:4f}")
    print()
    
    