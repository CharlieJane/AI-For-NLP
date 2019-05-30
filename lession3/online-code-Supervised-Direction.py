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


#print (sub_age)
#print(sub_fare)
#plt.scatter(sub_age,sub_fare)
#plt.show()


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

min_error_rate = float('inf')

loop_times=10000
losses=[]

change_directions = [
    #(k,b)
    (+1,-1),
    (+1,+1),
    (-1,+1),
    (-1,-1)
]
k_hat = random.random() * 20 - 10
b_hat = random.random() * 20 - 10

best_direction = None
best_k,best_b= None,None

def step():return random.random()*1
direction = random.choice(change_directions)

while loop_times>0:
    k_delta_direction,b_delta_direction = direction

    k_delta = k_delta_direction * step()
    b_delta = b_delta_direction * step()

    new_k = k_hat + k_delta
    new_b = b_hat + b_delta

    estimated_fares = func(sub_age, new_k, new_b)
    error_rate = loss(y=sub_fare,yhat=estimated_fares)

    if error_rate< min_error_rate:
        min_error_rate=error_rate
        best_k,best_b = new_k,new_b

        direction = (k_delta_direction,b_delta_direction)

        print('loop=={}'.format(loop_times))
        print('f(age) = {} *age + {}, with error rate: {}'.format(best_k,best_b,min_error_rate))
        losses.append(min_error_rate)
    else:
        direction = random.choice(list(set(change_directions)-{(k_delta_direction,b_delta_direction)}))
    loop_times-=1

#plt.scatter(sub_age,sub_fare)
#plt.plot(sub_age,func(sub_age,best_k,best_b),c='r')
#plt.show()

plt.plot(range(len(losses)),losses)
plt.show()