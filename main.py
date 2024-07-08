from docplex.mp.model import Model
from docplex.util.environment import get_environment

#from dis_func import *
from dis_func_yugu import *

def build_model(w, h, m, Q):#模型建立
    location_z = g_location(w, h,m)#货位
    station_z = g_station(w, h, m)#拣选台

    if Q > station_z.shape[0]:#Q大于拣选台数量
        print('输入数量超出实际工作站数量')
        input()

    mat_dis = zeros((station_z.shape[0], location_z.shape[0]))#全零s行l列数列

    for i in range(0, station_z.shape[0]):#罗列候选拣选台
        for j in range(0, location_z.shape[0]):#罗列货位
            #mat_dis[i, j] = xy_distance(location_z[j, 0], location_z[j, 1], station_z[i, 0], station_z[i, 1])#传统布局，计算罗列的两点间的距离  (x, y, sx, sy, m,w, h, jiaodu=45, la=2, lb=1, lp=1)
            mat_dis[i, j] = xy_distance(location_z[j, 0], location_z[j, 1], station_z[i, 0], station_z[i, 1],m,w,h)#鱼骨布局

    I = [i for i in range(1, station_z.shape[0] + 1)]
    L = [i for i in range(1, location_z.shape[0] + 1)]

    xb = {(i, j) for i in I for j in L}

    mdl = Model('MIP')

    x = mdl.binary_var_dict(xb, name='x')
    o = mdl.binary_var_dict(I, name='o')

    mdl.minimize(mdl.sum(x[i, j] * mat_dis[i - 1, j - 1] for i in I for j in L))

    mdl.add_constraints(mdl.sum(o) == Q for i in I)
    mdl.add_constraints((mdl.sum(x[i, j] for i in I) == 1) for j in L)
    mdl.add_constraints(x[i, j] <= o[i] for i in I for j in L)

    return mdl


def solve_model(mdl, i):  # 模型求解
    print("Solve log_output:")
    sol = mdl.solve(log_output=True)

    if not sol:
        print("*** Problem has no solution")
    else:
        mdl.float_precision = 3
        # print("* model solved as function:")
        # mdl.print_solution()

        with get_environment().get_output_stream("solution.json") as fp:
            mdl.solution.export(fp, "json")

        DATA = open('traditional_random_data' + str(i) + '.txt', mode="a")
        DATA.write('w = ' + str(w) + '; h = ' + str(h) + '; m = ' + str(m) + '; Q = ' + str(Q) + '\n')
        DATA.write('工作站坐标有：' + str(g_station(w, h, m).shape[0]) + '个' + '\n')
        # DATA.write(str(g_station(w, h, m)) + '\n')
        DATA.write('货架位置坐标有：' + str(g_location(w, h, m).shape[0]) + '个' + '\n')
        # DATA.write(str(g_location(w, h)) + '\n')

        print()
        print("Solve details:")
        print(sol.solve_details)
        DATA.write(str(sol.solve_details))

        print()
        print("Solve information:")
        mdl.print_information()

        print()
        print("Solution values:")
        t = 0
        for i in range(1, g_station(w, h, m).shape[0] + 1):
            if sol['o_' + str(i)] == 1:
                t += 1
                print('选中的第', str(t), '个工作站坐标为: ', g_station(w, h, m)[i - 1])
                DATA.write('选中的第' + str(t) + '个工作站坐标为: ' + str(g_station(w, h, m)[i - 1]) + '\n')
        print()
        # print("Solution status: ", mdl.solution.get_status())
        print("拣选行走总距离为: {0:.2f}".format(mdl.solution.get_objective_value()))
        DATA.write("拣选行走总距离为: {0:.2f}".format(mdl.solution.get_objective_value()) + '\n' + '\n')
        DATA.close()


if __name__ == '__main__':
   w_list = [120]#80, 60, 40, 20] # 10, 20, 30, 40, 50, 60,
   h_list = [120]#
   Q_list = [3,4,5,6,7,8]# 8, 9, 10, 11, 12, 13, 14, 15]
   for w in w_list:
       for h in h_list:
           m = 4
           for Q in Q_list:
               if Q <= g_station(w, h, m).shape[0]:
                   print('w = ' + str(w) + '; h = ' + str(h) + '; m = ' + str(m) + '; Q = ' + str(Q) + '\n')
                   mdl = build_model(w, h, m, Q)
                   solve_model(mdl, 6)
