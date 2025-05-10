import numpy as np

f = open('temp' , mode = 'a')

arr = np.array([1,2,3.0])

f.write(arr[2])
f.close()