import numpy as np
import pandas as pd
import os
import glob
import sys

from mrcfile import write


class WriteExcel(object):

    # 请输入 file.csv  file为自定义文件名
    def __init__(self,filename,mode):
        self.filename = filename
        self.data = {}
        self.flag = False
        self.mode = mode
        self.isExist()

    def isExist(self) -> None:
        # 获取当前目录
        directory = os.getcwd()
        # 获取所有文件
        if self.mode == 1:
            return

        files = os.listdir(directory)
        for file in files:
            if file == self.filename:
                self.flag = True
                return
        self.flag = False


    # 请输入数组，以及字符    例如   'a'  [1,2,3]
    def setData(self,str,arr) -> None:
        self.data[str] = arr

    def write(self) -> None:
        if(self.flag == False):
            df = pd.DataFrame(self.data)
            df.to_csv(self.filename, index=None, encoding="gb2312")
        else:
            print("文件已存在")




if __name__ == "__main__" :
    writeExcel = WriteExcel("writeData.csv",mode = 0)   #   如果mode默认为0  为0则检查文件是否存在，不覆盖，如果为1，不检查


    arr = np.array([1,2,3.0,6])

    writeExcel.setData('1',arr)
    writeExcel.write()




