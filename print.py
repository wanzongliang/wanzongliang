# import numpy as np
# import matplotlib.pyplot as plt
# a = [1,2,3,4,5,2,1,6,3,2.1,4,12]
# hist, bin_edges = np.histogram(a, 90, density=True)
# point_x = bin_edges[0:len(bin_edges) - 1]
# point_y = hist * (max(a) - min(a)) /90
# print(sum(point_y))
# print(point_x)
# print(point_y)
# #plt.plot(point_x, point_y)
# #plt.show()

# 打开二进制文件，'rb'表示以二进制读模式打开
with open('product.tpr', 'rb') as file:
    # 读取文件内容
    content = file.read()

# 打印内容（通常是字节数据）
print(content)