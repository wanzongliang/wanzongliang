import MDAnalysis
import sys
import numpy as np
import matplotlib.pyplot as plt
from MDAnalysis.lib.log import ProgressBar
from datetime import datetime
import math

class Orientation(object):
    def __init__(self,universe,selection_water,selection_CL):
        # class universe
        self.universe = universe
        # str
        self.selection_water = selection_water
        # str
        self.selection_CL = selection_CL
        # array
        self.selection_water_array = None
        self.selection_CL_array = None


    # 用进度条的格式，所有帧数下的原子放入数组
    # data : 二维数组
    def _selection_serial(self):
        selection_water = []
        selection_CL = []
        for ts in ProgressBar(self.universe.trajectory, verbose=True,
                              total=self.universe.trajectory.n_frames):
            selection_water.append(self.universe.select_atoms(self.selection_water))
            selection_CL.append(self.universe.select_atoms(self.selection_CL))
        self.selection_water_array = selection_water
        self.selection_CL_array = selection_CL


    def _getOneDeltaPoint(self,selection_water_single,selection_CL_single):

        O_atom = selection_water_single[::3]
        H1_atom = selection_water_single[1::3]
        H2_atom = selection_water_single[2::3]

        #已知CL原子为1个
        CL_atom = selection_CL_single

        #水分子的偶极矩
        dipVector0 = O_atom.positions - ((H1_atom.positions + H2_atom.positions) * 0.5)

        #水分子的氧原子和CL原子组成的向量
        coVector0 = CL_atom.positions - O_atom.positions

        unitdipVector0 = []
        unitcoVector0 = []
        for i in range(len(coVector0)):
            if np.linalg.norm(coVector0[i]) < 2.46 :
                unitdipVector0.append(dipVector0[i]/np.linalg.norm(dipVector0[i]))
                unitcoVector0.append(coVector0[i]/np.linalg.norm(coVector0[i]))

        # #二位范数  sqrt(x1^2 + x2^2 + x3^2 ...)
        # normdipVector0 = np.linalg.norm(dipVector)
        # normcoVector0 = np.linalg.norm(coVector)

        # def myDot(x,y):
        #     x_normal =  math.sqrt(pow(x[0], 2) + pow(x[1], 2) + pow(x[2], 2))
        #     y_normal =  math.sqrt(pow(y[0], 2) + pow(y[1], 2) + pow(y[2], 2))
        #     dot = x[0]*y[0] + x[1]*y[1]+ x[2]*y[2]
        #     return dot/(x_normal*y_normal)

        #单位向量
        cos_angle = []
        angle = []
        for i in range(len(unitcoVector0)):
            #cos_angle.append(myDot(unitdipVector0[i], unitcoVector0[i]))
            cos_angle.append(np.clip(np.dot(unitdipVector0[i], unitcoVector0[i])/(np.linalg.norm(unitdipVector0[i])*np.linalg.norm(unitcoVector0[i])), -1.0, 1.0))


        angle = np.arccos(cos_angle)/np.pi * 180

        return angle


    def _histogram(self,angle):

        hist, bin_edges = np.histogram(angle, 90, density=True)
        return hist,bin_edges

    def _plot(self,hist,bin_edges):
        plt.figure(1, figsize=(18, 6))
        plt.xlabel('theta')
        plt.ylabel('P(cos theta)')
        plt.title('PDF cos theta for O-CL')
        point_x = bin_edges[0:len(bin_edges) - 1]
        point_y = hist*2
        print(point_x)
        print(point_y)
        plt.plot(point_x, point_y) #'o'
        plt.show()
        plt.close()

    def run_single(self, i):
        #self._selection_serial()
        self.universe.trajectory[i]
        selection_water_array = self.universe.select_atoms("resname SOL")
        selection_CL_array = self.universe.select_atoms("resname Mg")
        angle = self._getOneDeltaPoint(selection_water_array, selection_CL_array)
        hist = self._histogram(angle)
        self._plot(hist[0], hist[1])


    def run(self):
        self._selection_serial()
        i=0
        angle = []
        while i <= (len(self.selection_water_array) - 1):
            self.universe.trajectory[i]
            angle = np.concatenate((angle,self._getOneDeltaPoint(self.selection_water_array[i],self.selection_CL_array[i])))
            #angle.append(self._getOneDeltaPoint(self.selection_water_array[i],self.selection_CL_array[i]))
            i = i + 1

        hist = self._histogram(angle)
        self._plot(hist[0],hist[1])

#tpr = "/home/wan/Desktop/water_CL2/product.tpr"
#xtc = "/home/wan/Desktop/water_CL2/product.trr"


# universe = MDAnalysis.Universe(tpr, xtc)
# selection = "resname SOL"
# selection2 = "resname CL"
# orientation = Orientation(universe,selection,selection2)
# universe.trajectory[1]
# selection_water_array = universe.select_atoms("resname SOL")
# selection_CL_array = universe.select_atoms("resname CL")
# angle = orientation._getOneDeltaPoint(selection_water_array, selection_CL_array)
# hist = orientation._histogram(angle)
# orientation._plot(hist[0], hist[1])

if __name__ == '__main__':
    tpr = "product.tpr"
    xtc = "product.trr"

    universe = MDAnalysis.Universe(tpr, xtc)
    selection = "resname SOL"
    selection2 = "resname Mg"
    orientation = Orientation(universe, selection, selection2)


    orientation.run_single(129882)
    #orientation.run()
