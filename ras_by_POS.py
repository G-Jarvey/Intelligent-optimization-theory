# -*- coding: utf-8 -*-
import sys
import importlib
importlib.reload(sys)
#sys.setdefaultencoding('utf-8')
 
import numpy as np
import matplotlib.pyplot as plt
 
# 目标函数定义
def ras(x):
    y = 20 + x[0]**2 + x[1]**2 - 10*(np.cos(2*np.pi*x[0])+np.cos(2*np.pi*x[1]))
    return y
    
# 参数初始化
w = 1.0
c1 = 1.49445
c2 = 1.49445
 
maxgen = 200   # 进化次数  
sizepop = 20   # 种群规模
 
# 粒子速度和位置的范围
Vmax =  1
Vmin = -1
popmax =  5
popmin = -5
 
 
# 产生初始粒子和速度
pop = 5 * np.random.uniform(-1,1,(2,sizepop))#2*20矩阵
v = np.random.uniform(-1,1,(2,sizepop))#2*20矩阵
 
 
fitness = ras(pop)             # 计算适应度
i = np.argmin(fitness)      # 找最好的个体
gbest = pop                    # 记录个体最优位置
zbest = pop[:,i]              # 记录群体最优位置
fitnessgbest = fitness        # 个体最佳适应度值
fitnesszbest = fitness[i]      # 全局最佳适应度值
 
 
# 迭代寻优
t = 0
record = np.zeros(maxgen)
while t < maxgen:
    
    # 速度更新
    v = w * v + c1 * np.random.random() * (gbest - pop) + c2 * np.random.random() * (zbest.reshape(2,1) - pop)
    v[v > Vmax] = Vmax     # 限制速度
    v[v < Vmin] = Vmin
    
    # 位置更新
    pop = pop + 0.5 * v;
    pop[pop > popmax] = popmax  # 限制位置
    pop[pop < popmin] = popmin
 
    # 计算适应度值
    fitness = ras(pop)
    
    # 个体最优位置更新
    index = fitness < fitnessgbest
    fitnessgbest[index] = fitness[index]
    gbest[:,index] = pop[:,index]
 
    # 群体最优更新
    j = np.argmin(fitness)
    if fitness[j] < fitnesszbest:
        zbest = pop[:,j]
        fitnesszbest = fitness[j]
 
    record[t] = fitnesszbest # 记录群体最优位置的变化   
    t = t + 1
    
 
# 结果分析
print(zbest)
print(min(fitnessgbest))
plt.plot(record,'b-')
plt.xlabel('generation')  
plt.ylabel('fitness')  
plt.title('fitness curve')  
plt.show()