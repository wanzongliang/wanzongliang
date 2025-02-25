import MDAnalysis
import sys
import numpy as np
import matplotlib.pyplot as plt
from MDAnalysis.lib.log import ProgressBar
from datetime import datetime
from time import sleep
from tqdm import tqdm
import wrtieExcel


class Orientation(object):
    def __init__(self,universe,selection_water,selection_CL):
        # class universe
        self.universe = universe
        # str
        self.selection_water = selection_water
        # str
        self.selection_CL = selection_CL


    def _getOneDeltaPoint(self,selection_water_single,selection_CL_single):

        O_atom = selection_water_single[::3]
        H1_atom = selection_water_single[1::3]
        H2_atom = selection_water_single[2::3]

        #已知CL原子为1个
        CL_atoms = selection_CL_single
        #print(CL_positions)
        unitdipVector0 = []
        unitcoVector0 = []


        for CL_atom in CL_atoms:
            coVector0 = CL_atom.position - O_atom.positions
            for i in range(len(O_atom)):
                temp = np.linalg.norm(coVector0[i])
                if temp > 3.06 and temp < 5.50 :
                    dipVector0 = O_atom.positions[i] - ((H1_atom.positions[i] + H2_atom.positions[i]) * 0.5)
                    unitdipVector0.append(dipVector0/np.linalg.norm(dipVector0))
                    unitcoVector0.append(coVector0[i]/temp)


        #单位向量
        cos_angle = []
        angle = []
        for i in range(len(unitcoVector0)):
            #cos_angle.append(np.dot(unitdipVector0[i], unitcoVector0[i]))
            #cos_angle.append(np.clip(np.dot(unitdipVector0[i], unitcoVector0[i])/(np.linalg.norm(unitdipVector0[i])*np.linalg.norm(unitcoVector0[i])), -1.0, 1.0))
            cos_angle.append(np.clip(np.dot(unitdipVector0[i], unitcoVector0[i]) , -1.0, 1.0))

        angle = np.arccos(cos_angle)/np.pi * 180

        return angle


    def _histogram(self,angle):

        hist, bin_edges = np.histogram(angle, 181, density=True, range=(0, 181))
        return hist,bin_edges

    def _plot(self,hist,bin_edges):
        plt.figure(1, figsize=(18, 6))
        plt.xlabel('theta')
        plt.ylabel('P(cos theta)')
        plt.title('PDF cos theta for O-CL')
        point_x = bin_edges[0:len(bin_edges) - 1]
        point_y = hist
        print(point_x)
        print(point_y)

        write = wrtieExcel.WriteExcel("Na_second.csv",mode = 1)
        write.setData('point_x',point_x)
        write.setData('point_y',point_y)
        write.write()

        f = open('run.txt', mode='a')
        f.writelines("\n")
        f.writelines("已输出到excel文件")
        print("已输出到excel文件")
        f.writelines(str(point_x))
        f.writelines("\n")
        f.writelines(str(point_x))
        f.writelines("\n")

        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d  %H:%M:%S')

        f.writelines("****************************************************************")
        f.writelines("运行完成时间")
        f.writelines(formatted_time)

        f.close()


        plt.plot(point_x, point_y) #'o'
        plt.show()
        plt.close()


    def run_single(self, i):
        self.universe.trajectory[i]
        selection_water_array = self.universe.select_atoms(self.selection_water)
        selection_CL_array = self.universe.select_atoms(self.selection_CL)
        angle = self._getOneDeltaPoint(selection_water_array, selection_CL_array)
        #hist = self._histogram(angle)
        #self._plot(hist[0],hist[1],hist[2],hist[3])
        return angle
        #self._plot(hist[0], hist[1])


    def run(self):
        i=0
        angle = []



        for i in tqdm(range(0, self.universe.trajectory.n_frames)):

            angle = np.concatenate((angle,self.run_single(i)))
            i = i + 1

        hist = self._histogram(angle)
        self._plot(hist[0],hist[1])

if __name__ == '__main__':
    tpr = "product.tpr"
    xtc = "product.trr"

    universe = MDAnalysis.Universe(tpr, xtc)
    selection = "resname SOL"
    selection2 = "resname Na"
    orientation = Orientation(universe, selection, selection2)

    f = open('run.txt' , mode = 'a')
    f.writelines("\n")
    f.writelines("****************************************************************")
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d  %H:%M:%S')
    f.writelines("程序开始运行时间：")
    f.writelines(formatted_time)
    f.writelines("\n")
    f.writelines(selection)
    f.writelines("\n")
    f.writelines(selection2)
    f.writelines("\n")
    f.close()


    #orientation.run_single(1)
    try:
        orientation.run()

    except:
        f = open('run.txt', mode='a')
        f.writelines("*************************************************************************")
        f.writelines("运行出现未知问题？")

    finally:
        f.close()