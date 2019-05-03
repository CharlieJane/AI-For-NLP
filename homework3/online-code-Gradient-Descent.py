import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

content0 = pd.read_csv('H:/assignment/project/tt0')
content1 = pd.read_csv('H:/assignment/project/tt1')
content0 = content0.dropna()
content1 = content1.dropna()
age_with_fares0 = content0[
    (content0['Age'] > 22) & (content0['Fare'] < 400) & (content0['Fare'] > 130)
]
age_with_fares1 = content1[
    (content1['Age'] > 22) & (content1['Fare'] < 400) & (content1['Fare'] > 130)
]
sub_fare = age_with_fares0['Fare'].append(age_with_fares1['Fare'])
sub_age = age_with_fares0['Age'].append(age_with_fares1['Age'])


def func(age ,k ,b):return k *age +b

def loss(y,yhat):
    """
       :param y: the real fares
       :param yhat: the estimated fares
       :return: how good is the estimated fares
       """
    return np.mean(np.abs(y - yhat))
    #return np.mean(np.square(y - yhat))
    #return np.mean(np.sqrt(y - yhat))

loop_times=5000
losses=[]

k_hat = random.random() * 20 - 10
b_hat = random.random() * 20 - 10

def derivate_k(y,yhat,x):
    abs_values = [1 if (y_i - yhat_i)>0 else -1 for y_i,yhat_i in zip(y,yhat)]
    return np.mean([a * -x_i for a,x_i in zip(abs_values,x)])

def derivate_b(y,yhat):
    abs_values = [1 if (y_i - yhat_i)>0 else -1 for y_i,yhat_i in zip(y,yhat)]
    return np.mean([a * -1 for a in abs_values])

learning_rate = 1e-2

while loop_times > 0:

    k_delta = -1 * learning_rate * derivate_k(sub_fare,func(sub_age,k_hat,b_hat),sub_age)
    b_delta = -1 * learning_rate * derivate_b(sub_fare,func(sub_age,k_hat,b_hat))

    k_hat += k_delta
    b_hat += b_delta

    estimated_fares = func(sub_age, k_hat, b_hat)
    error_rate = loss(y=sub_fare,yhat=estimated_fares)

    print('loop=={}'.format(loop_times))
    print('f(age) = {} *age + {}, with error rate: {}'.format(k_hat,b_hat,error_rate))
    losses.append(error_rate)
    loop_times-=1
#plt.scatter(sub_age,sub_fare)
#plt.plot(sub_age,func(sub_age,best_k,best_b),c='r')
#plt.show()

plt.plot(range(len(losses)),losses)
plt.show()