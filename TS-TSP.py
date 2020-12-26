import copy,random,datetime
import matplotlib.pyplot as plt


city_list = [[1, (41, 94)], [2, (37, 84)], [3, (54, 67)], [4, (25, 62)], [5, (7, 64)], 
             [6, (2, 99)], [7, (68, 58)], [8, (71, 44)], [9, (54, 62)], [10, (83, 69)], 
             [11, (64, 60)], [12, (18, 54)], [13, (22, 60)], [14, (83, 46)], [15, (91, 38)], 
             [16, (25, 38)], [17, (24, 42)], [18, (58, 69)], [19, (71, 71)], [20, (74, 78)],
             [21, (87, 76)], [22, (18, 40)], [23, (13, 40)], [24, (82, 7)], [25, (62, 32)], 
             [26, (58, 35)], [27, (45, 21)], [28, (41, 26)], [29, (44, 35)], [30, (4, 50)]]


class Taboo_search:
    def __init__(self,city_list,is_random = True):
        self.city_list = city_list   #城市列表
        self.candidate_count = 100   #候选集合长度
        self.taboo_list_length = 10  #禁忌表长度
        self.iteration_count = 1000   #迭代次数
        self.min_route, self.min_cost = self.random_first_full_road() if is_random else self.greedy_first_full_road()
        self.taboo_list = []


    #计算两城市间的距离
    def city_distance(self,city1,city2):
        distance = ( (float(city1[1][0] - city2[1][0]))**2 + (float(city1[1][1] - city2[1][1]))**2 )**0.5
        return distance

    #获取当前城市邻居城市中距离最短的一个
    def next_shotest_road(self,city1,other_cities):
        tmp_min = 999999
        tmp_next = None
        for i in range(0,len(other_cities)):
            distance = self.city_distance(city1,other_cities[i])
            #print(distance)
            if distance < tmp_min:
                tmp_min = distance
                tmp_next = other_cities[i]
        return tmp_next,tmp_min


    #随机生成初始线路
    def random_first_full_road(self):
        cities = copy.deepcopy(self.city_list)
        cities.remove(cities[0])#初始城市移除
        route = copy.deepcopy(cities)
        random.shuffle(route)#随机排序列表
        cost = self.route_cost(route)
        return route,cost#返还路径和距离

    #根据贪婪算法获取初始线路
    def greedy_first_full_road(self):
        remain_city = copy.deepcopy(self.city_list)
        current_city = remain_city[0]#当前城市
        road_list = []
        remain_city.remove(current_city)#初始城市移除
        all_distance = 0
        while len(remain_city) > 0:#还有城市时
            next_city, distance = self.next_shotest_road(current_city,remain_city)#从当前城市找到最近的城市
            all_distance += distance
            road_list.append(next_city)
            remain_city.remove(next_city)
            current_city = next_city#当前城市转移成最近城市
        all_distance += self.city_distance(self.city_list[0],road_list[-1])
        return road_list,round(all_distance,2)#返还路径和距离

    #随机交换2个城市位置
    def random_swap_2_city(self,route):
        #print(route)
        road_list = copy.deepcopy(route)
        two_rand_city = random.sample(road_list,2)#随机选择两个城市
        #print(two_rand_city)
        index_a = road_list.index(two_rand_city[0])
        index_b = road_list.index(two_rand_city[1])
        road_list[index_a] = two_rand_city[1]
        road_list[index_b] = two_rand_city[0]
        return road_list,sorted(two_rand_city)

    #计算线路路径长度
    def route_cost(self,route ):
        road_list = copy.deepcopy(route)
        current_city = self.city_list[0]
        while current_city in road_list:
            road_list.remove(current_city)
        all_distance = 0
        while len(road_list) > 0 :
            distance = self.city_distance(current_city,road_list[0])
            all_distance += distance
            current_city = road_list[0]
            road_list.remove(current_city)
        all_distance += self.city_distance(current_city,self.city_list[0])
        return round(all_distance,2)

    #获取下一条线路
    def single_search(self,route):
        #生成候选集合列表和其对应的移动列表
        candidate_list = []
        candidate_move_list = []
        while len(candidate_list) < self.candidate_count:
            tmp_route,tmp_move = self.random_swap_2_city(route)
            #print("tmp_route:",tmp_route)
            if tmp_route not in candidate_list:
                candidate_list.append(tmp_route)
                candidate_move_list.append(tmp_move)
        #计算候选集合各路径的长度
        candidate_cost_list = []
        for candidate in candidate_list:
            candidate_cost_list.append(self.route_cost(candidate))
        #print(candidate_list)

        min_candidate_cost = min(candidate_cost_list)                           #候选集合中最短路径
        min_candidate_index = candidate_cost_list.index(min_candidate_cost)
        min_candidate = candidate_list[min_candidate_index]                     #候选集合中最短路径对应的线路
        move_city = candidate_move_list[min_candidate_index]

        if min_candidate_cost < self.min_cost:
            self.min_cost = min_candidate_cost
            self.min_route = min_candidate
            if move_city in self.taboo_list:                                    #藐视法则，当此移动导致的值更优，则无视该禁忌列表
                self.taboo_list.remove(move_city)
            if len(self.taboo_list) >= self.taboo_list_length:                  #判断该禁忌列表长度是否以达到限制，是的话移除最初始的move
                self.taboo_list.remove(self.taboo_list[0])
            self.taboo_list.append(move_city)                                    #将该move加入到禁忌列表
            return min_candidate

        else:
            #当未找到更优路径时，选择次优路线，如果该次优路线在禁忌表里，则更次一层，依次类推，找到一条次优路线
            if move_city in self.taboo_list:
                tmp_min_candidate = min_candidate
                tmp_move_city = move_city

                while move_city in self.taboo_list:
                    candidate_list.remove(min_candidate)
                    candidate_cost_list.remove(min_candidate_cost)
                    candidate_move_list.remove(move_city)

                    min_candidate_cost = min(candidate_cost_list)  # 候选集合中最短路径
                    min_candidate_index = candidate_cost_list.index(min_candidate_cost)
                    min_candidate = candidate_list[min_candidate_index]  # 候选集合中最短路径对应的线路
                    move_city = candidate_move_list[min_candidate_index]
                    if len(candidate_list) < 10:                   #防止陷入死循环，在候选集个数小于10的时候跳出
                        min_candidate = tmp_min_candidate
                        move_city = tmp_move_city
            if len(self.taboo_list) >= self.taboo_list_length:  # 判断该禁忌列表长度是否以达到限制，是的话移除最初始的move
                self.taboo_list.remove(self.taboo_list[0])
            self.taboo_list.append(move_city)
            return min_candidate

    #进行taboo_search直到达到终止条件:循环100次
    def taboo_search(self):
        route = copy.deepcopy(self.min_route)
        for i in range(self.iteration_count):
            route = self.single_search(route)
        new_route = [self.city_list[0]]
        new_route.extend(self.min_route)
        new_route.append(self.city_list[0]) #前后插入首个城市信息
        return new_route,self.min_cost


#画线路图
def draw_line_pic(route,cost,duration,desc):
    x = []
    y = []
    for item in route:
        x.append(item[1][0])
        y.append(item[1][1])
    x0 = [x[0],]
    y0 = [y[0],]
    plt.plot(x,y)
    plt.scatter(x0,y0,marker="o",c="r")
    for a, b in zip(x0, y0):
        plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=10)
    plt.title("Taboo_Search("+desc +": "+ str(cost) + ")")
    plt.show()



if __name__ == "__main__":
    ts_random = Taboo_search(city_list)
    ts_greedy = Taboo_search(city_list,is_random=False)
    start_time1 = datetime.datetime.now()
    route_random,cost_random = ts_random.taboo_search()
    end_time1 = datetime.datetime.now()
    duration1 = (end_time1 - start_time1).seconds
    #draw_line_pic(route_random,cost_random,duration1,"random")
    route_greedy,cost_greedy = ts_greedy.taboo_search()
    end_time2 = datetime.datetime.now()
    duration2 = (end_time2 - end_time1).seconds
    draw_line_pic(route_greedy,cost_greedy,duration2,"greedy")


