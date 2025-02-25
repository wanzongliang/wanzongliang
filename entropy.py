import numpy as np
import math
import wrtieExcel

def read_xvg_file(file_path):
    r = []
    g_r = []
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith(('#', '@')):
                data = line.split()
                if len(data) >= 2:
                    r.append(float(data[0]))
                    g_r.append(float(data[1]))
    return r, g_r

def calculate_s(r, g_r, rho):
    sum = 0
    sum_S = []
    R = 8.314
    for i in range(len(r)-1):
        y = None
        p = r[i+1]-r[i]
        k = g_r[i+1]
        if k == 0:
            y = 0
        else :
            y = math.log(k)
        b = k * y - (k - 1)
        c = b * r[i+1]**2
        s = c * p
        S = -2 * np.pi * rho * s * R
        sum = sum + S
        sum_S.append(sum)
    return sum_S



if __name__ == "__main__":
    file_path = 'rdf_CL_SOL.xvg'
    rho = 98.724506 
    gr_data = read_xvg_file(file_path)

    S = calculate_s(gr_data[0],gr_data[1],rho)

    wrtieExcel = wrtieExcel.WriteExcel("Ca_entropy.csv",mode=1) 
    r = gr_data[0][1::]
    wrtieExcel.setData('r',list(r))
    wrtieExcel.setData('e',list(S))
    wrtieExcel.write()





