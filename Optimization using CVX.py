# -*- coding: utf-8 -*-
"""NotLinear8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MzpinLCakyFUrk13xFHlS7lHt8Mjk0bN
"""



from cvxpy import constraints
from cvxpy.problems.objective import Objective
import cvxpy as cp
import numpy as np

Q = np.array([1,-1,1])
c = (1,1,0)
x = cp.Variable(3)

f = cp.square(x[0]+x[1]) + cp.square(x[2]) + 3*x[0] -4*x[1]
Objective = cp.Minimize(f)
s = np.array([[0.5,1,0], [np.sqrt(7/4),0,0], [0,np.sqrt(3),0],[0,0,0]])
constraints = [cp.norm(s@x + np.array([0,0,0,2])) + cp.quad_over_lin(Q@x + 1,c@x) <= 6, x >= 1]
prob = cp.Problem(Objective, constraints)
print(f"Optimal value : {prob.solve():.4f}")
print(f"Optimal var: {x.value}")

Q = np.array([1,0])
c = (1,1)
c2 = (0,1)
y = cp.Variable(2)

f = cp.square(y[0]+y[1]) + 2*y[0] + 3*y[1] - cp.sqrt(2*y[1] + 5)
Objective2 = cp.Minimize(f)
constraints2 = [cp.quad_over_lin(Q@y,c@y) + cp.power(cp.quad_over_lin(Q@y,c2@y) + 1 , 8) <= 100,
               y[0] + y[1] >= 4,
               y[1] >= 1]
prob = cp.Problem(Objective2, constraints2)
print(f"Optimal value : {prob.solve():.4f}")
print(f"Optimal var: {y.value}")



import matplotlib.pyplot as plt
import numpy as np



m=50
n=2
outliers_num=10
np.random.seed(314)
A = 3000*np.random.rand(n,m)
A[:,:outliers_num] += 3000
p = (10*np.random.rand(m,1)+10).round()
alpha = 0.01
gamma = 1.2
eta1 = 20
eta2 = 30
mu1 = 2
mu2 = 5

Q = np.array([1,0])
z = cp.Variable(2)
f3 = 0
for i in range (1,m):
  f3 += p[i]*alpha*cp.norm(A[:,i] - z)
  #can do without alpha 
Objective3 = cp.Minimize(f3)
prob = cp.Problem(Objective3)
print(f"Optimal value : {prob.solve():.4f}")
print(f"Optimal var: {z.value}")

t = cp.Variable(2)
f4 = 0
for i in range (1,m):
  f4 += p[i]*(cp.maximum(0,alpha*cp.norm(A[:,i] - t) - eta1)*mu1 + cp.maximum(0,alpha*cp.norm(A[:,i] - t) - eta2)*(mu2-mu1))
  #can do without alpha 
Objective4 = cp.Minimize(f4)
prob = cp.Problem(Objective4)
print(f"Optimal value : {prob.solve():.4f}")
print(f"Optimal var: {t.value}")

plt.scatter(A[0],A[1])
plt.scatter(z.value[0],z.value[1],color = 'r',label = "Section A, warhousr location")
plt.scatter(t.value[0],t.value[1],color = 'g',label = "Section B , warhouse location")
plt.legend()