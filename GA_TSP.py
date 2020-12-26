import math,random,time
import matplotlib.pyplot as plt
#读取坐标文件
filename = 'tsp.txt' 
city_num = [] #城市编号
city_location = [] #城市坐标
with open(filename, 'r') as f:
    datas = f.readlines()[0:-1]
for data in datas:
    data = data.split()
    city_num.append(int(data[0]))
    x = float(data[1])
    y = float(data[2])
    city_location.append((x,y))#城市坐标
city_count = len(city_num) #总的城市数
origin = 1 #设置起点和终点
remain_cities = city_num[:] 
remain_cities.remove(origin)#迭代过程中变动的城市
remain_count = city_count - 1 #迭代过程中变动的城市数
indexs = list(i for i in range(remain_count))
#计算邻接矩阵
dis =[[0]*city_count for i in range(city_count)] #初始化
for i in range(city_count):
    for j in range(city_count):
        if i != j:
            dis[i][j] = math.sqrt((city_location[i][0]-city_location[j][0])**2 + (city_location[i][1]-city_location[j][1])**2)
        else:
            dis[i][j] = 0

def route_mile_cost(route):
    '''
    计算路径的里程成本
    '''
    mile_cost = 0.0
    mile_cost += dis[0][route[origin-1]-1]#从起始点开始
    for i in range(remain_count-1):#路径的长度
        mile_cost += dis[route[i]-1][route[i+1]-1]
    mile_cost += dis[route[-1]-1][origin-1] #到终点结束
    return mile_cost

#获取当前邻居城市中距离最短的1个
def nearest_city(current_city,remain_cities):
    temp_min = float('inf')
    next_city = None
    for i in range(len(remain_cities)):
        distance = dis[current_city-1][remain_cities[i]-1]
        if distance < temp_min:
            temp_min = distance
            next_city = remain_cities[i]
    return next_city

def greedy_initial_route(remain_cities):
    '''
    采用贪婪算法生成初始解：从第一个城市出发找寻与其距离最短的城市并标记，
    然后继续找寻与第二个城市距离最短的城市并标记，直到所有城市被标记完。
    最后回到第一个城市(起点城市)
    '''
    cand_cities = remain_cities[:]
    current_city = origin
    initial_route = []
    while len(cand_cities) > 0:
        next_city = nearest_city(current_city,cand_cities) #找寻最近的城市及其距离
        initial_route.append(next_city) #将下一个城市添加到路径列表中
        current_city = next_city #更新当前城市
        cand_cities.remove(next_city) #更新未定序的城市
    return initial_route

#物竞天择，适者生存
def selection(population):
    '''
    选出父代个体
    '''
    M = population_size
    parents = []
    for i in range(M):
        if random.random() < (1 - i/M):
            parents.append(population[i])
    return parents
def CPX(parent1,parent2):
    '''
    交叉繁殖：CX与PX的混合双亲产生两个子代
    '''
    cycle = []
    start = parent1[0]
    cycle.append(start)
    end = parent2[0]
    while end != start:
        cycle.append(end)
        end = parent2[parent1.index(end)]
    child = parent1[:]
    cross_points = cycle[:]
    if len(cross_points) < 2 :
        cross_points = random.sample(parent1,2)
    k = 0
    for i in range(len(parent1)):
        if child[i] in cross_points:
            continue
        else:
            for j in range(k,len(parent2)):
                if parent2[j] in cross_points:
                    continue
                else:
                    child[i] = parent2[j]
                    k = j + 1
                    break   
    return child

#变异
def mutation(children,mutation_rate):
    '''
    子代变异
    '''
    for i in range(len(children)):
        if random.random() < mutation_rate:
            child = children[i]
            new_child = child[:]
            index = sorted(random.sample(indexs,2))
            L = index[1] - index[0] + 1
            for j in range(L):
                new_child[index[0]+j] = child[index[1]-j]
            path = [origin] + child + [origin]
            a,b = index[0] + 1,index[1] + 1
            d1 = dis[path[a-1]-1][path[a]-1] + dis[path[b]-1][path[b+1]-1]
            d2 = dis[path[a-1]-1][path[b]-1] + dis[path[a]-1][path[b+1]-1]
            if d2 < d1:
                children[i] = new_child

    return children

def get_best_current(population):
    '''
    将种群的个体按照里程排序，并返回当前种群中的最优个体及其里程
    '''
    graded = [[route_mile_cost(x),x] for x in population]
    graded = sorted(graded)
    population = [x[1] for x in graded]
    return graded[0][0],graded[0][1],population

population_size = 100 #种群数
mutation_rate = 0.2 #变异概率
def main(iter_count):
    #初始化种群
    population = [greedy_initial_route(remain_cities)]
    # population = []
    for i in range(population_size-1):
        #随机生成个体
        individual  = remain_cities[:]
        random.shuffle(individual)
        population.append(individual)
    mile_cost,result,population = get_best_current(population)
    record = [mile_cost] #记录每一次繁殖的最优值
    i = 0
    while i < iter_count:
        #选择繁殖个体群
        parents = selection(population)
        #交叉繁殖
        target_count = population_size - len(parents) #需要繁殖的数量(保持种群的规模)
        children = []
        while len(children) < target_count:
            parent1,parent2 = random.sample(parents,2)
            child1 = CPX(parent1,parent2)
            child2 = CPX(parent2,parent1)
            children.append(child1)
            children.append(child2)
        #父代变异
        parents = mutation(parents,1)
        #子代变异
        children = mutation(children,mutation_rate)
        #更新种群
        population = parents + children
        #更新繁殖结果
        mile_cost,result,population = get_best_current(population) 
        record.append(mile_cost) #记录每次繁殖后的最优解
        i += 1
    route = [origin] + result + [origin]
    return route,mile_cost,record

def fig():
    time_start = time.time()
    N = 1000 #进化次数
    satisfactory_solution,mile_cost,record = main(N)
    time_end = time.time()
    time_cost = time_end - time_start
    print('time cost:',time_cost)
    print("优化里程成本:%d" %(int(mile_cost)))
    print("优化路径:\n",satisfactory_solution)
    #绘制路线图
    X = []
    Y = []
    for i in satisfactory_solution:
        x = city_location[i-1][0]
        y = city_location[i-1][1]
        X.append(x)
        Y.append(y)
    plt.plot(X,Y,'-o')
    plt.title("satisfactory solution of TS:%d"%(int(mile_cost)))
    plt.show()
    #绘制迭代过程图
    A = [i for i in range(N+1)]#横坐标
    B = record[:] #纵坐标
    plt.xlim(0,N)
    plt.xlabel('进化次数',fontproperties="SimSun")
    plt.ylabel('路径里程',fontproperties="SimSun")
    plt.title("solution of GA changed with evolution")
    plt.plot(A,B,'-')
    plt.show()
    return mile_cost,time_cost

fig()
   
record1 = [0]*10
record2 = [0]*10
for i in range(10):
    record1[i],record2[i] = fig()
print(min(record1))
print(sum(record1)/10)
print(record1)
R = 10
Mcosts = [0]*R
Tcosts = [0]*R
for j in range(R):
    Mcosts[j],Tcosts[j] = fig()
AM = sum(Mcosts)/R #平均里程
AT = sum(Tcosts)/R #平均时间
print("最小里程:",min(Mcosts))
print("平均里程:",AM)
print('里程:\n',Mcosts)
print("平均时间:",AT)
