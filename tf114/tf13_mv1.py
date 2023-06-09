import tensorflow as tf
tf.compat.v1.set_random_seed(123)

# 1. 데이터
x1_data = [73, 93, 89, 96, 73]
x2_data = [80, 88, 91, 98, 66]
x3_data = [75, 93, 90, 100, 70]
y_data = [152, 185, 189, 196, 142]

x1 = tf.compat.v1.placeholder(tf.float32)
x2 = tf.compat.v1.placeholder(tf.float32)
x3 = tf.compat.v1.placeholder(tf.float32)
y = tf.compat.v1.placeholder(tf.float32)

w1 = tf.compat.v1.Variable(tf.compat.v1.random_normal([1]))
w2 = tf.compat.v1.Variable(tf.compat.v1.random_normal([1]))
w3 = tf.compat.v1.Variable(tf.compat.v1.random_normal([1]))
b = tf.compat.v1.Variable(tf.compat.v1.random_normal([1]))

# 2. 모델
hypothesis = x1 * w1 + x2 * w2 + x3 * w3 + b

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.00001)

# 3. 훈련
cost = tf.reduce_mean(tf.square(hypothesis - y))
train = optimizer.minimize(cost)

sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())
epochs = 1000
batch_size = len(x1_data)

for epoch in range(epochs):
    for step in range(batch_size):
        x1_batch = x1_data[step]
        x2_batch = x2_data[step]
        x3_batch = x3_data[step]
        y_batch = y_data[step]
        cost_val, hy_val, _ = sess.run([cost, hypothesis, train],
                                       feed_dict={x1: x1_batch, x2: x2_batch, x3: x3_batch, y: y_batch})
        if step % 100 == 0:
            print(f"Epoch: {epoch+1}, Step: {step}, Cost: {cost_val}, Prediction:\n{hy_val}")
    
# R2 score 계산
mean_y = tf.reduce_mean(y)
ss_tot = tf.reduce_sum(tf.square(y - mean_y))
ss_res = tf.reduce_sum(tf.square(y - hypothesis))
r_squared = 1 - (ss_res / ss_tot)

print("R2 score:", sess.run(r_squared, feed_dict={x1: x1_data, x2: x2_data, x3: x3_data, y: y_data}))

sess.close()


