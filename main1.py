import  numpy as np
from  numpy import  *
import pandas as pd
import matplotlib.pyplot as plt

#from matplotlib.path import Path

def g_station(w, h, m):  # 工作站位置
    """

    :param w: 仓库长
    :param h: 仓库高
    :param m: 步长
    :return: 生成的工作站坐标位置
    """
    si_cor = array([[0, 0], [0, h]])
    """
    si_cor = [[0 0]
             [0 h]]
    """
    for i in range(0, h + 1, m):  # start = 0 , end = h+1 ， 步长 = m
        if [w, i] not in si_cor.tolist():
            si_cor = append(arr=si_cor, values=[[w, i]], axis=0)
            """
            arr： 添加列表的目标
            values: 添加值
            axis: 0 = 列；1 = 行
            """
        if [-w, i] not in si_cor.tolist():
            si_cor = append(arr=si_cor, values=[[-w, i]], axis=0)
    return si_cor
def generage_place(w,h,m,begin_place  = [0,0],lb = 1):  # 生成传统布局挑选台的位置
    # w 宽 h 高 m 步长
    place_list = []
    for i in np.arange(0,int(w/2)+1,m):
        place_list.append([i,0+lb/4])
        place_list.append([i, 0 + h - lb / 4])
        if i == 0:
            continue
        place_list.append([-i, 0 + lb / 4])
        place_list.append([-i, 0+h-lb/4])
    place_list = np.array(place_list)
    return place_list

def generate_place_jiazi(w,h,m,begin_place = [0,0],la = 1,lb = 1,lp = 1):  # 传统布局货位坐标
    # pass
    # for i in range(lb,h-lb,lp):
    place_list = []
    for x_place in np.arange(0, w / 2,la+2*lp):  # 等差数列
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


def generate_yugu_place_of_contral(w,h,m,begin_place = [0,0],jiaodu = 60 ,lb = 1, lp=1, la=1): # 生成控制台
    jiaodu = jiaodu /360 * 2* np.pi
    place_list = []
    place_list.append([0,lb/4])
    for i in np.arange(0, w / 2, m):
        place_list.append([i, 0 + h - lb / 4])
        if i ==0:
            continue
        place_list.append([-i, 0 + h - lb / 4])
    y_max = np.tan(jiaodu) * (w/2-lb/4)
    y_min = np.tan(jiaodu) * (w / 2 - lb-lp)
    place_list.append([(w/2-lb/4), y_max])
    place_list.append([-(w/2-lb/4), y_max])
    place_list.append([(w/2-lb/4), lb/4])
    place_list.append([-(w / 2 - lb / 4), lb / 4])
    for y_i in np.arange((lb+2*lp+la/2), y_min, m):
        place_list.append([(w/2-lb/4), y_i])
        place_list.append([-(w/2-lb/4), y_i])

    place_list = np.array(place_list)
    return place_list

def generate_place_jiazi_yugu(w, h, m, begin_place=[0, 0],jiaodu = 60 ,la=1, lb=1, lp=1):  # 鱼骨布局货位坐标
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

def show_img(list_array,contral_place):
    x_list,y_list,contral_x_list,contral_y_list = [],[],[],[]
    for a in list_array:
        x_list.append(a[0])
        y_list.append(a[1])
    for a in contral_place:
        contral_x_list.append(a[0])
        contral_y_list.append(a[1])
    plt.figure(figsize=(8, 4))  # figsize:确定画布大小
    # 2. 绘图
    plt.scatter(x_list,  # 横坐标
                y_list,  # 纵坐标
                c='blue',  # 点的颜色
                label='function',
                marker = 's',
                linewidths = 5)  # 标签 即为点代表的意思
    for a, b in zip(x_list, y_list):
        plt.text(a, b, find_areas(w, h, m, [a, b], jiaodu=jiaodu), ha='center', va='bottom', fontsize=20)

    plt.scatter(contral_x_list,  # 横坐标
                contral_y_list,  # 纵坐标
                c='red',  # 点的颜色
                label='function',
                marker='s',
                linewidths=10)  # 标签 即为点代表的意思
    # 3.展示图形
    # plt.legend()  # 显示图例
    plt.show()  # 显示所绘图形


def xy_distance(x, y, sx, sy, w, h, jiaodu = 45 ,la=2, lb=1, lp=1):  # 货位的坐标，工作站的坐标
    jiaodu = jiaodu / 360 * 2 * np.pi
    y_max = h-lb/4
    x_max = w /2- lb /4
    l_h = x_max/np.cos(jiaodu)#1
    l_AD_pS1_h = y/np.sin(jiaodu)#2
    l_BC_pS1_h = x/np.cos(jiaodu)#3
    l_S1t_AD_h = sy / np.sin(jiaodu)#4
    l_AD_ph = abs(x)-y/np.tan(jiaodu)#5
    l_BC_ph = y-abs(x)*np.tan(jiaodu)#6
    l_ADBC_pt_h = abs(l_AD_pS1_h-abs(sx)/np.cos(jiaodu))#7
    l_BCAD_pt_h = abs(abs(x) / np.cos(jiaodu) - l_S1t_AD_h)#8
    l_S1t_BC_h = abs(sx) / np.cos(jiaodu)#9
    l_pt_BC_top = y_max-abs(sx)*np.tan(jiaodu)#10
    l_pt_AD_bro = x_max-sy/np.tan(jiaodu)#11
    l_AD_p_top = y_max-y#12
    l_A_pS2_h = l_h - l_AD_pS1_h#13
    l_B_pS2_h =(x_max-x)/np.cos(jiaodu)#14
    l_D_pS4_h = l_h - l_AD_pS1_h#15
    l_C_pS4_h = (x_max+x)/np.cos(jiaodu)#16
    l_AD_p_bro = x_max-abs(x)#17
    l_A_pS2_bro = sy-y#18
    l_S2_top = y_max-sy#19
    #当拣选台为S1时，货位在A,D区域时
    dxy=(lp+la)/2+abs(x)-y/np.tan(jiaodu)+abs(y)/np.sin(jiaodu)
    # 当拣选台为S1时，货位在B,C区域时
    dxy = (lp + la) / 2 + y-abs(x) * np.tan(jiaodu) + abs(x) / np.cos(jiaodu)
    # 当拣选台为S2时，货位在A区域时
    dxy=min( l_AD_ph+l_A_pS2_h,l_AD_p_bro+l_A_pS2_bro)
    # 当拣选台为S2时，货位在B区域时
    dxy = min(l_BC_ph + l_B_pS2_h, l_AD_p_top +x_max-x+ l_S2_top)
    # 当拣选台为S2时，货位在c区域时
    dxy = min (l_BC_ph + l_BC_pS1_h+l_h, l_AD_p_top + x_max - x + l_S2_top)
    # 当拣选台为S2时，货位d区域时
    dxy = min (l_AD_ph + l_AD_pS1_h+l_h, l_AD_p_top + x_max - x + l_S2_top)
    # 当拣选台为S3时
    dxy=abs(x)+y_max-y
    # 当拣选台为S4时，货位在A区域时
    dxy = min(l_AD_ph + l_AD_pS1_h + l_h, l_AD_p_top + x_max +x + l_S2_top)
    # 当拣选台为S4时，货位在B区域时
    dxy = min(l_BC_ph + l_BC_pS1_h + l_h, l_AD_p_top + x_max + x + l_S2_top)
    # 当拣选台为S4时，货位在c区域时
    dxy = min(l_BC_ph + l_C_pS4_h, l_AD_p_top + x_max +x + l_S2_top)
    # 当拣选台为S4时，货位d区域时
    dxy = min(l_AD_ph + l_D_pS4_h, l_AD_p_bro + l_A_pS2_bro)
    # 当拣选台为A时，货位在A区域时
    dxy = l_AD_p_bro+abs(l_A_pS2_bro)
    # 当拣选台为A时，货位在B区域时
    dxy = min(l_BC_ph+l_BCAD_pt_h+l_pt_AD_bro,l_AD_p_top + x_max - x+l_S2_top)
    # 当拣选台为A时，货位在c区域时
    dxy = min(l_BC_ph+l_BC_pS1_h+l_S1t_AD_h+l_pt_AD_bro,l_AD_p_top + x_max - x+l_S2_top)
    # 当拣选台为A时，货位d区域时
    dxy = min(l_AD_ph+l_AD_pS1_h+l_S1t_AD_h+l_pt_AD_bro,l_AD_p_bro+2*x_max+min(y+sy,2*y_max-(y+sy)))
    # 当拣选台为B时，货位在A区域时
    dxy=min(l_AD_ph+l_ADBC_pt_h+l_pt_BC_top,l_AD_p_bro+l_AD_p_top+x_max-sx,l_AD_p_top+abs(sx-x))
    # 当拣选台为B时，货位在B区域时
    dxy=l_AD_p_top+abs(sx-x)
    # 当拣选台为B时，货位在c区域时,同上
    dxy = l_AD_p_top + abs(sx - x)
    # 当拣选台为B时，货位d区域时
    dxy = min(l_AD_ph+l_AD_pS1_h+l_S1t_BC_h+l_pt_BC_top,l_AD_p_top+sx-x)
    # 当拣选台为C时，货位A区域时
    dxy = min(l_AD_ph + l_AD_pS1_h + l_S1t_BC_h + l_pt_BC_top, l_AD_p_top + x - sx)
    # 当拣选台为C时，货位在B区域时
    dxy=l_AD_p_top + x - sx
    # 当拣选台为C时，货位在C区域时
    dxy = l_AD_p_top + abs(sx - x)
    # 当拣选台为C时，货位在D区域时
    dxy = min(l_AD_ph + l_ADBC_pt_h + l_pt_BC_top, l_AD_p_bro + l_AD_p_top + x_max + sx, l_AD_p_top + abs(sx - x))
    # 当拣选台为D时，货位在A区域时
    dxy = min(l_AD_ph + l_AD_pS1_h + l_S1t_AD_h + l_pt_AD_bro,l_AD_p_bro + 2 * x_max + min(y + sy, 2 * y_max - (y + sy)))
    # 当拣选台为D时，货位在B区域时
    dxy = min(l_BC_ph + l_BC_pS1_h + l_S1t_AD_h + l_pt_AD_bro, l_AD_p_top + x_max + x + l_S2_top)
    # 当拣选台为D时，货位在c区域时
    dxy = min(l_BC_ph + l_BCAD_pt_h + l_pt_AD_bro, l_AD_p_top + x_max + x + l_S2_top)
    # 当拣选台为D时，货位d区域时
    dxy = l_AD_p_bro + abs(l_A_pS2_bro)


    xy_distance_=1
    #xy_distance_ = abs(x - sx) + abs(y - sy)
    return xy_distance_

if __name__ == '__main__':
    place1 = generage_place(80,10,4,lb = 2)  # generage_place  g_station
    place4 = generate_place_jiazi(80,10,4,la = 2,lb = 2,lp = 1)
    place = generate_place_jiazi_yugu(40, 30, 4,jiaodu = 45, la = 2, lb = 2, lp = 1)#generate_place_jiazi(10, 10, 2)   generate_place_jiazi  generate_place_jiazi
    place3 = generate_yugu_place_of_contral(40, 30, 4,jiaodu = 45, lb = 2,la=2,lp=1)
    show_img(place,place3)
    print(place,place3)
