from numpy import *
w = 10
h = 5
m = 4
def g_station(w, h, m):  # 工作站位置
    si_cor = array([[0, 0], [0, h]])
    for i in range(0, w, m):  # start = 0 , end = h+1 ， 步长 = m
        if [i, 0] not in si_cor.tolist():
            si_cor = append(arr=si_cor, values=[[i, 0]], axis=1)
        if [i, h] not in si_cor.tolist():
            si_cor = append(arr=si_cor, values=[[i, h]], axis=1)
    for i in range(0, -w, -m):  # start = 0 , end = h+1 ， 步长 = m
        if [i, 0] not in si_cor.tolist():
            si_cor = append(arr=si_cor, values=[[i, 0]], axis=1)
        if [i, h] not in si_cor.tolist():
            si_cor = append(arr=si_cor, values=[[i, h]], axis=1)
    return si_cor

