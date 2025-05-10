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
        # arr
        self.array = [0] * 91


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
                if temp < 3.58 :
                    dipVector0 = O_atom.positions[i] - ((H1_atom.positions[i] + H2_atom.positions[i]) * 0.5)
                    unitdipVector0.append(dipVector0/np.linalg.norm(dipVector0))
                    unitcoVector0.append(coVector0[i]/temp)



        for i in range(len(unitcoVector0)):
            #cos_angle.append(np.dot(unitdipVector0[i], unitcoVector0[i]))
            #cos_angle.append(np.clip(np.dot(unitdipVector0[i], unitcoVector0[i])/(np.linalg.norm(unitdipVector0[i])*np.linalg.norm(unitcoVector0[i])), -1.0, 1.0))
            cos_angle = (np.clip(np.dot(unitdipVector0[i], unitcoVector0[i]) , -1.0, 1.0))
            angle = np.arccos(cos_angle)/np.pi * 180
            index = int(np.floor(angle/2))
            self.array[index] += 1




    def _plot(self):
        plt.figure(1, figsize=(18, 6))
        plt.xlabel('theta')
        plt.ylabel('P(cos theta)')
        plt.title('PDF cos theta for O-CL')
        point_x = [i for i in range(0,180,2)]
        point_y = self.array /2
        print(point_x)
        print(point_y)

        write = wrtieExcel.WriteExcel("K_first.csv",mode = 1)
        write.setData('point_x',point_x)
        write.setData('point_y',point_y)
        write.write()

        plt.plot(point_x, point_y) #'o'
        plt.show()
        plt.close()


    def run_single(self, i):
        self.universe.trajectory[i]
        selection_water_array = self.universe.select_atoms(self.selection_water)
        selection_CL_array = self.universe.select_atoms(self.selection_CL)
        self._getOneDeltaPoint(selection_water_array, selection_CL_array)


    def run(self):

        for i in tqdm(range(0, self.universe.trajectory.n_frames)):

            self.run_single(i)

        self._plot()

if __name__ == '__main__':
    tpr = "product.tpr"
    xtc = "product.trr"

    universe = MDAnalysis.Universe(tpr, xtc)
    selection = "resname SOL"
    selection2 = "resname K"
    orientation = Orientation(universe, selection, selection2)


    #orientation.run_single(1)
    orientation.run()
