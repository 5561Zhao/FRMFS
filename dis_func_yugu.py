
import numpy as np
from numpy import *


def g_station(w,h,m,begin_place  = [0,0],jiaodu = 65 ,lb = 2, lp=1, la=2): # 生成控制台
    jiaodu = jiaodu /360 * 2* np.pi
    place_list = []
    place_list.append([0,lb/4])
    for i in np.arange(0, (w / 2+1), m):
        place_list.append([i, 0 + h - lb / 4])
        place_list.append([-i, 0 + h - lb / 4])
    # y_max = np.arctan(w/2)
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



def g_location(w, h, m, begin_place=[0, 0],jiaodu = 65 ,la=2, lb=2, lp=1):  # 鱼骨布局货位坐标
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

def is_in_poly(p, poly=np.array([[1539, 1443], [1861, 1435], [1419, 141], [1365, 181]],
                                      np.int32)):  # 1539,1443 1960,1431 1365,181 1437,,141
    """
    :param p: [x, y]
    :param poly: [[], [], [], [], ...]
    :return:
    """
    px, py = p
    is_in = False
    for i, corner in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = corner
        x2, y2 = poly[next_i]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
            is_in = True
            break
        if min(y1, y2) < py <= max(y1, y2):  # find horizontal edges of polygon
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:  # if point is on edge
                is_in = True
                break
            elif x > px:  # if point is on left-side of line
                is_in = not is_in
    return is_in
def find_areas(w, h, m,point_place, begin_place=[0, 0],jiaodu = 65 ,la=2, lb=2, lp=1):
    s2_x = w/2
    jiaodu = jiaodu / 360 * 2 * np.pi
    s2_y = np.tan(jiaodu) *s2_x
    s2 = [s2_x, s2_y]
    s3 = [0, h]
    if is_in_poly(point_place,[[0,0],s2,[s2_x,0]]):  # 在 A区域
        return 1
    if is_in_poly(point_place,[[0,0],s3,[w/2,h],s2]): # 在B 区域
        return 2
    if is_in_poly(point_place,[[0,0],[-s2_x,s2_y],[-w/2,h],[0,h]]): # 在c 区域
        return 3
    if is_in_poly(point_place, [[0, 0],  [-s2_x, 0],[-s2_x,s2_y]]):  # 在 D区域
        return 4

def xy_distance(x, y, sx, sy, m,w, h, jiaodu=65, la=2, lb=2, lp=1):  # 货位的坐标，工作站的坐标
    point_place = [x,y]
    areas_number = find_areas(w, h,m,point_place,jiaodu = 65)#
    jiaodu = jiaodu / 360 * 2 * np.pi
    y_max = h - lb / 4
    x_max = w / 2 - lb / 4
    l_h = x_max / np.cos(jiaodu)  # 1
    l_AD_pS1_h = y / np.sin(jiaodu)  # 2
    l_BC_pS1_h = x / np.cos(jiaodu)  # 3
    l_S1t_AD_h = sy / np.sin(jiaodu)  # 4
    l_AD_ph = abs(x) - y / np.tan(jiaodu)  # 5
    l_BC_ph = y - abs(x) * np.tan(jiaodu)  # 6
    l_ADBC_pt_h = abs(l_AD_pS1_h - abs(sx) / np.cos(jiaodu))  # 7
    l_BCAD_pt_h = abs(abs(x) / np.cos(jiaodu) - l_S1t_AD_h)  # 8
    l_S1t_BC_h = abs(sx) / np.cos(jiaodu)  # 9
    l_pt_BC_top = y_max - abs(sx) * np.tan(jiaodu)  # 10
    l_pt_AD_bro = x_max - sy / np.tan(jiaodu)  # 11
    l_AD_p_top = y_max - y  # 12
    l_A_pS2_h = l_h - l_AD_pS1_h  # 13
    l_B_pS2_h = (x_max - x) / np.cos(jiaodu)  # 14
    l_D_pS4_h = l_h - l_AD_pS1_h  # 15
    l_C_pS4_h = (x_max + x) / np.cos(jiaodu)  # 16
    l_AD_p_bro = x_max - abs(x)  # 17
    l_A_pS2_bro = sy - y  # 18
    l_S2_top = y_max - sy  # 19
    # 当拣选台为S1时，货位在A,D区域时
    if (sx ==0 and sy == lb/4) and (areas_number ==1 or areas_number ==4):
        dxy = (lp + la) / 2 + abs(x) - y / np.tan(jiaodu) + abs(y) / np.sin(jiaodu)
        return dxy
    # 当拣选台为S1时，货位在B,C区域时
    if (sx == 0 and sy == lb / 4) and (areas_number == 2 or areas_number == 3):
        dxy = (lp + la) / 2 + y - abs(x) * np.tan(jiaodu) + abs(x) / np.cos(jiaodu)
        return dxy
    # 当拣选台为S2时，货位在A区域时  s2 = [w/2,np.tan(jiaodu) * w/2]  y_max =
    #print(np.tan(jiaodu) * w/2)
    if (sx == (w/2-lb/4) and sy == np.tan(jiaodu) * (w/2-lb/4)) and areas_number == 1 :
        dxy = min(l_AD_ph + l_A_pS2_h, l_AD_p_bro + l_A_pS2_bro)
        return dxy
    # 当拣选台为S2时，货位在B区域时
    if (sx == (w/2-lb/4) and sy == np.tan(jiaodu) * (w/2-lb/4)) and areas_number == 2:
        dxy = min(l_BC_ph + l_B_pS2_h, l_AD_p_top + x_max - x + l_S2_top)
        return dxy
    # 当拣选台为S2时，货位在c区域时
    if (sx == (w/2-lb/4) and sy == np.tan(jiaodu) * (w/2-lb/4)) and areas_number == 3:
        dxy = min(l_BC_ph + l_BC_pS1_h + l_h, l_AD_p_top + x_max - x + l_S2_top)
        return dxy
    # 当拣选台为S2时，货位d区域时
    if (sx == (w/2-lb/4) and sy == np.tan(jiaodu) * (w/2-lb/4)) and areas_number == 4:
        dxy = min(l_AD_ph + l_AD_pS1_h + l_h, l_AD_p_top + x_max - x + l_S2_top)
        return dxy
    # 当拣选台为S3时   [0, h - lb / 4]
    if (sx == 0 and sy == h - lb / 4) :
        dxy = abs(x) + y_max - y
        return dxy
    # 当拣选台为S4时，货位在A区域时 [-w/2,np.tan(jiaodu) * w/2]
    if(sx == -(w/2-lb/4) and sy == np.tan(jiaodu) * w / 2) and areas_number == 1 :
        dxy = min(l_AD_ph + l_AD_pS1_h + l_h, l_AD_p_top + x_max + x + l_S2_top)
        return dxy
    # 当拣选台为S4时，货位在B区域时
    if (sx == -(w/2-lb/4) and sy == np.tan(jiaodu) * w / 2) and areas_number == 2:
        dxy = min(l_BC_ph + l_BC_pS1_h + l_h, l_AD_p_top + x_max + x + l_S2_top)
        return dxy
    # 当拣选台为S4时，货位在c区域时
    if (sx == -(w/2-lb/4) and sy == np.tan(jiaodu) * w / 2) and areas_number == 3:
        dxy = min(l_BC_ph + l_C_pS4_h, l_AD_p_top + x_max + x + l_S2_top)
        return dxy
    # 当拣选台为S4时，货位d区域时
    if (sx == -(w/2-lb/4) and sy == np.tan(jiaodu) * w / 2) and areas_number == 4:
        dxy = min(l_AD_ph + l_D_pS4_h, l_AD_p_bro + l_A_pS2_bro)
        return dxy
    # 当拣选台为A时，货位在A区域时
    if (sx == (w/2-lb/4) and sy < np.tan(jiaodu) * w / 2) and areas_number == 1:
        dxy = l_AD_p_bro + abs(l_A_pS2_bro)
        return dxy
    # 当拣选台为A时，货位在B区域时
    if (sx == (w/2-lb/4) and sy < np.tan(jiaodu) * w / 2) and areas_number == 2:
        dxy = min(l_BC_ph + l_BCAD_pt_h + l_pt_AD_bro, l_AD_p_top + x_max - x + l_S2_top)
        return dxy
    # 当拣选台为A时，货位在c区域时
    if (sx == (w/2-lb/4) and sy < np.tan(jiaodu) * w / 2) and areas_number == 3:
        dxy = min(l_BC_ph + l_BC_pS1_h + l_S1t_AD_h + l_pt_AD_bro, l_AD_p_top + x_max - x + l_S2_top)
        return dxy
    # 当拣选台为A时，货位d区域时
    if (sx == (w/2-lb/4) and sy < np.tan(jiaodu) * w / 2) and areas_number == 4:
        dxy = min(l_AD_ph + l_AD_pS1_h + l_S1t_AD_h + l_pt_AD_bro,
                  l_AD_p_bro + 2 * x_max + min(y + sy, 2 * y_max - (y + sy)))
        return dxy
        # 当拣选台为B时，货位在A区域时
    if (sx >0 and sy == h - lb / 4) and areas_number == 1:
        dxy = min(l_AD_ph + l_ADBC_pt_h + l_pt_BC_top, l_AD_p_bro + l_AD_p_top + x_max - sx, l_AD_p_top + abs(sx - x))
        return dxy
    # 当拣选台为B时，货位在B区域时
    if (sx > 0 and sy == h - lb / 4) and areas_number == 2:
        dxy = l_AD_p_top + abs(sx - x)
        return dxy
    # 当拣选台为B时，货位在c区域时,同上
    if (sx > 0 and sy == h - lb / 4) and areas_number == 3:
        dxy = l_AD_p_top + abs(sx - x)
        return dxy
    # 当拣选台为B时，货位d区域时
    if (sx > 0 and sy == h - lb / 4) and areas_number == 4:
        dxy = min(l_AD_ph + l_AD_pS1_h + l_S1t_BC_h + l_pt_BC_top, l_AD_p_top + sx - x)
        return dxy
    # 当拣选台为C时，货位A区域时
    if (sx < 0 and sy == h - lb / 4) and areas_number == 1:
        dxy = min(l_AD_ph + l_AD_pS1_h + l_S1t_BC_h + l_pt_BC_top, l_AD_p_top + x - sx)
        return dxy
    # 当拣选台为C时，货位在B区域时
    if (sx < 0 and sy == h - lb / 4) and areas_number == 2:
        dxy = l_AD_p_top + x - sx
        return dxy
    # 当拣选台为C时，货位在C区域时
    if (sx < 0 and sy == h - lb / 4) and areas_number == 3:
        dxy = l_AD_p_top + abs(sx - x)
        return dxy
    # 当拣选台为C时，货位在D区域时
    if (sx < 0 and sy == h - lb / 4) and areas_number == 4:
        dxy = min(l_AD_ph + l_ADBC_pt_h + l_pt_BC_top, l_AD_p_bro + l_AD_p_top + x_max + sx, l_AD_p_top + abs(sx - x))
        return dxy
    # 当拣选台为D时，货位在A区域时
    if (sx == -(w/2-lb/4) and sy < np.tan(jiaodu) * w / 2) and areas_number == 1:
        dxy = min(l_AD_ph + l_AD_pS1_h + l_S1t_AD_h + l_pt_AD_bro,
              l_AD_p_bro + 2 * x_max + min(y + sy, 2 * y_max - (y + sy)))
        return dxy
    # 当拣选台为D时，货位在B区域时
    if (sx == -(w/2-lb/4) and sy < np.tan(jiaodu) * w / 2) and areas_number == 2:
        dxy = min(l_BC_ph + l_BC_pS1_h + l_S1t_AD_h + l_pt_AD_bro, l_AD_p_top + x_max + x + l_S2_top)
        return dxy
    # 当拣选台为D时，货位在c区域时
    if (sx == -(w/2-lb/4) and sy < np.tan(jiaodu) * w / 2) and areas_number == 3:
        dxy = min(l_BC_ph + l_BCAD_pt_h + l_pt_AD_bro, l_AD_p_top + x_max + x + l_S2_top)
        return dxy
    # 当拣选台为D时，货位d区域时
    if (sx == -(w/2-lb/4) and sy < np.tan(jiaodu) * w / 2) and areas_number == 4:
        dxy = l_AD_p_bro + abs(l_A_pS2_bro)
        return dxy
    #print(areas_number)
    return 0


def dxy(x, y, station_z):
    dxy = array([])
    for i in range(0, station_z.shape[0]):  # shape是维度
        dxy = append(dxy, [xy_distance(x, y, station_z[i][0], station_z[i][1])], 0)
    dxy_ = min(dxy)
    return dxy_