import numpy as np
from numpy import *

def g_station(w,h,m,begin_place  = [0,0],lb = 2):  # 生成传统挑选台的位置
    # w 宽 h 高 m 步长
    place_list = []
    for i in range(0,int(w/2)+1,m):
        place_list.append([i, 0 + lb / 4])
        place_list.append([i, 0 + h - lb / 4])
        if i == 0:
            continue
        place_list.append([-i, 0 + lb / 4])
        place_list.append([-i, 0 + h - lb / 4])
    place_list = np.array(place_list)
    return place_list

def g_location(w,h,m,begin_place = [0,0],la = 2,lb = 2,lp = 1):  # 传统货位坐标
    place_list = []
    for x_place in np.arange(0, w / 2,la+2*lp):
        x_place = x_place + la/2
        for y_place in np.arange(lb, h - lb, lp):
            if x_place+lp/2 > w/2:
                continue
            place_list.append([x_place+lp/2,y_place+lp/2])
            place_list.append([-(x_place + lp / 2), y_place + lp / 2])
            if x_place+lp*3/2 > w/2:
                continue
            place_list.append([x_place + lp *3/ 2, y_place + lp / 2])
            place_list.append([-(x_place + lp * 3 / 2), y_place + lp / 2])
    return np.array(place_list)


def xy_distance(x, y, sx, sy):  # 货位的坐标，工作站的坐标
    xy_distance_ = abs(x - sx) + abs(y - sy)
    return xy_distance_


def dxy(x, y, station_z):
    dxy = array([])
    for i in range(0, station_z.shape[0]):  # shape是维度
        dxy = append(dxy, [xy_distance(x, y, station_z[i][0], station_z[i][1])], 0)
    dxy_ = min(dxy)
    return dxy_
