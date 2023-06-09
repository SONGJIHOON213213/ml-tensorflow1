import tensorflow as tf
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt

x_train = [1,2,3]
y_train = [4,5,6]
x_test = [1,2,3]
y_test = [4,5,6]


x = tf.compat.v1.placeholder(tf.float32)
y = tf.compat.v1.placeholder(tf.float32)

w = tf.compat.v1.Variable([10], dtype=tf.float32, name='weight')

# model
hypothesis = x * w

# compile
loss = tf.reduce_mean(tf.square(hypothesis - y))
lr = 0.1
gradient = tf.reduce_mean((x * w - y) * x)
descant = w - lr * gradient
update = w.assign(descant)

w_history = []
loss_history = []

sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())

for step in range(21):
    _, loss_v, w_v = sess.run([update, loss, w], feed_dict={x: x_train, y: y_train})
    print(step, '\t', loss_v, '\t', w_v)
    w_history.append(w_v)
    loss_history.append(loss_v)

y_pred = np.array(w_history) * np.array(x_train)
r2 = r2_score(y_train * np.ones_like(w_history), y_pred)
mae = mean_absolute_error(y_train * np.ones_like(w_history), y_pred)

# y_pred = np.array(w_history) * np.array(x_train)
# r2 = r2_score(y_train * np.ones_like(w_history), y_pred)
# mae = mean_absolute_error(y_train * np.ones_like(w_history), y_pred)

sess.close()

print("====================w history==========================")
print(w_history)
print("====================Hypothesis history==========================")
print(loss_history)
print("====================R2 score==========================")
print(r2)
print("====================MAE==========================")
print(mae)