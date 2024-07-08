from numpy import *
import  numpy as np
a = np.zeros((4,5))

"""h = 5
si_cor = array([[0, 0], [0, h]])
print(si_cor.tolist())
print(si_cor)
i = 3
w = 5
si_cor = append(arr=si_cor, values=[[w, i]], axis=0)
print(si_cor)
li_cor = mat(zeros((0, 2)))
print("," * 100)
print(li_cor)
print(li_cor.shape)
li_cor = append(li_cor, [[2, 3]], 0)
print(li_cor)
print(li_cor.shape)
print(li_cor.shape[0])
print(li_cor.shape[1])
"""
"""counts = 0
for i in range(1.5, w + 1, 1):
    counts += 1
    if counts == 1:
        counts = 0
    if counts == 0:
        for i in range(0.5, w + 1, 3):
            """
w = 10
h = 5
def g_location(w, h):  # 货位位置
    li_cor = mat(zeros((0, 2)))  # mat：将数组转化为矩阵方便运算 对其维度进行约束
    counts = 0
    for i in range(1.5, w + 1, 1):
        for j in range(0, h + 1):
            if [i, j] not in li_cor.tolist():
                li_cor = append(li_cor, [[i, j]], 0)
        counts += 1
        if counts == 1:
            counts = 0
        if counts == 0:
            for i in range(1.5, w + 1, 3):
                for j in range(0, h + 1):
                    if [i, j] not in li_cor.tolist():
                        li_cor = append(li_cor, [[i, j]], 0)
    return li_cor
   # print(li_cor)



def g_station(w,h,m,begin_place  = [0,0],lb = 2):  # 生成挑选台的位置
    # w 宽 h 高 m 步长
    place_list = []
    for i in range(0,int(w/2)+1,m):
        place_list.append([i,0+lb/4])
        place_list.append([-i, 0+lb/4])
        place_list.append([i, 0 + h-lb/4])
        place_list.append([-i, 0+h-lb/4])
    place_list = np.array(place_list)
    return place_list

def g_location(w,h,m,begin_place = [0,0],la = 2,lb = 2,lp = 1):  # 货位坐标
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

def generate_yugu_place_of_contral_S(w,h,m,begin_place = [0,0],jiaodu = 45 ,lb = 1, lp=1, la=1): # 生成控制台
    jiaodu = jiaodu /360 * 2* np.pi
    place_list = []
    place_list.append([0,lb/4])
    y_max = np.tan(jiaodu) * (w / 2 - lb / 4)
    place_list.append([(w/2-lb/4), y_max])
    place_list.append([0, 0 + h - lb / 4])
    place_list.append([-(w/2-lb/4), y_max])
    place_list = np.array(place_list)
    return place_list



def generate_yugu_place_of_contral_AD(w, h, m, begin_place=[0, 0], jiaodu=45, lb=2, lp=1, la=2):  # 生成控制台
    jiaodu = jiaodu / 360 * 2 * np.pi
    place_list = []
    y_min = np.tan(jiaodu) * (w / 2 - lb - lp)
    for y_i in np.arange((lb + 2 * lp + la / 2), y_min, m):
        place_list.append([(w / 2 - lb / 4), y_i])
        place_list.append([-(w / 2 - lb / 4), y_i])
    place_list.append([(w / 2 - lb / 4), lb / 4])
    place_list.append([-(w / 2 - lb / 4), lb / 4])
    place_list = np.array(place_list)
    return place_list

def generate_yugu_place_of_contral_BC(w, h, m, begin_place=[0, 0], jiaodu=45, lb=2, lp=1, la=2):  # 生成控制台
    jiaodu = jiaodu / 360 * 2 * np.pi
    place_list = []
    for i in np.arange(0, (w / 2 + 1), m):
        if i == 0:
            continue
        place_list.append([i, 0 + h - lb / 4])
        place_list.append([-i, 0 + h - lb / 4])
    place_list = np.array(place_list)
    return place_list

def generate_place_jiazi_yugu_AD(w, h, m, begin_place=[0, 0],jiaodu = 45 ,la=2, lb=2, lp=1):  # 鱼骨布局货位坐标
    jiaodu = jiaodu / 360 * 2 * np.pi
    y_max = np.tan(jiaodu) * w / 2- (la /2)/np.cos(jiaodu)
    place_list = []
    for y_place in np.arange(lb+lp, y_max, lp*2+la):
        x_place = y_place/np.tan(jiaodu)
        for x_place_new in np.arange(x_place,w/2-lb,lp):
            place_list.append([x_place_new+lp/2,y_place-lp/2])
            place_list.append([-(x_place_new + lp / 2), y_place - lp / 2])
        y_place = y_place+lp
        x_place = y_place / np.tan(jiaodu)
        for x_place_new in np.arange(x_place,w/2-lb,lp):
            place_list.append([x_place_new+lp/2,y_place-lp/2])
            place_list.append([-(x_place_new + lp / 2), y_place - lp / 2])

    place_list = np.array(place_list)


    return place_list

def generate_place_jiazi_yugu_BC(w, h, m, begin_place=[0, 0],jiaodu = 45 ,la=2, lb=2, lp=1):  # 鱼骨布局货位坐标
    jiaodu = jiaodu / 360 * 2 * np.pi
    y_max = np.tan(jiaodu) * w / 2- (la /2)/np.cos(jiaodu)
    place_list = []
    for x_place in np.arange((la/2+lp),w/2-lb, lp*2+la):
        y_place = x_place * np.tan(jiaodu)+(la /2)/np.cos(jiaodu)
        for y_place_new in np.arange(y_place, h - lb, lp):
            place_list.append([x_place-lp/2,y_place_new+lp/2])
            place_list.append([-(x_place - lp / 2), y_place_new + lp / 2])
        x_place = x_place + lp
        y_place = x_place * np.tan(jiaodu)+(la /2)/np.cos(jiaodu)
        for y_place_new in np.arange(y_place, h - lb, lp):
            place_list.append([x_place - lp / 2, y_place_new + lp / 2])
            place_list.append([-(x_place - lp / 2), y_place_new + lp / 2])

    place_list = np.array(place_list)


    return place_list

def xy_distance(x, y, sx, sy):  # 货位的坐标，工作站的坐标
    xy_distance_ = abs(x - sx) + abs(y - sy)
    return xy_distance_

if __name__ == '__main__':
    place1 = generate_yugu_place_of_contral_AD(40,20,4)
    place = generate_yugu_place_of_contral_BC(40,20,4)
    place2 = generate_yugu_place_of_contral_S(40, 20, 4)
    place3 = generate_place_jiazi_yugu_AD(40, 20, 4)
    place4 = generate_place_jiazi_yugu_BC(40, 20, 4)
    print(place)
