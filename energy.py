import math

import MDAnalysis
import numpy as np
from MDAnalysis.lib.log import ProgressBar
import time
import progressbar
from fontTools.tfmLib import MATHSY
from tqdm import tqdm


qi = 1   #
qO = -0.834
qH = 0.417
#k = 8.988e9  # 真空中的库仑常数，单位为 N·m^2/C^2
k = 1389.354845736

sigmai = 2.62815e-01
epsiloni = 1.32695e-01
sigmaO = 3.15061e-01
epsilonO = 6.36386e-01
epsilonH = 0
sigmaH = 0
sigmaiO = math.sqrt(sigmai * sigmaO)
epsiloniO = math.sqrt(epsiloni * epsilonO)
sigmaiH = math.sqrt(sigmai * sigmaH)
epsiloniH = math.sqrt(epsiloni * epsilonH)


class Energy(object):
    def __init__(self, universe, selection_water, selection_CL):
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
    # def _selection_serial(self):
    #     selection_water = []
    #     selection_CL = []
    #     for ts in ProgressBar(self.universe.trajectory, verbose=True, total=self.universe.trajectory.n_frames):
    #         selection_water.append(self.universe.select_atoms(self.selection_water).positions)
    #         selection_CL.append(self.universe.select_atoms(self.selection_CL).positions)
    #     self.selection_water_array = np.array(selection_water)
    #     self.selection_CL_array = np.array(selection_CL)

    def _getOneDeltaPoint(self, selection_water_single, selection_CL_single):
        O_atom = selection_water_single[::3]
        H1_atom = selection_water_single[1::3]
        H2_atom = selection_water_single[2::3]

        # 已知CL原子为1个
        CL_atoms = selection_CL_single


        # 水分子的氧原子和CL原子组成的向量
        #coVector0 = CL_atom - O_atom
        #coVectorH1 = CL_atom - H1_atom
        #coVectorH2 = CL_atom - H2_atom



        sum_coulomb = 0
        sum_lj = 0
        sum_coulomb_average = 0
        sum_lj_average = 0
        average_water = 0
        n = 0

        for CL_atom in CL_atoms:
            coVector0 = CL_atom.position - O_atom.positions
            coVectorH1 = CL_atom.position - H1_atom.positions
            coVectorH2 = CL_atom.position - H2_atom.positions
            for i in range(len(coVector0)):
                if np.linalg.norm(coVector0[i]) < 4:
                    average_water = average_water + 1
                    potential_coulomb1 = k * qi * qO / ((np.linalg.norm(coVector0[i]) * 1e-10))
                    potential_coulomb2 = k * qi * qH / ((np.linalg.norm(coVectorH1[i]) * 1e-10))
                    potential_coulomb3 = k * qi * qH / ((np.linalg.norm(coVectorH2[i]) * 1e-10))
                    potential_coulomb = potential_coulomb1 + potential_coulomb2 + potential_coulomb3
                    sum_coulomb = sum_coulomb + potential_coulomb

                    r6iO = (sigmaiO / (np.linalg.norm(coVector0[i]))) ** 6
                    r12iO = r6iO ** 2
                    potential_lj_iO = 4 * epsiloniO * (r12iO - r6iO)
                    r6iH1 = (sigmaiH / (np.linalg.norm(coVectorH1[i]))) ** 6
                    r12iH1 = r6iH1 ** 2
                    potential_lj_iH1 = 4 * epsiloniH * (r12iH1 - r6iH1)
                    r6iH2 = (sigmaiH / (np.linalg.norm(coVectorH2[i]))) ** 6
                    r12iH2 = r6iH2 ** 2
                    potential_lj_iH2 = 4 * epsiloniH * (r12iH2 - r6iH2)
                    potential_lj = potential_lj_iO + potential_lj_iH1 + potential_lj_iH2
                    sum_lj = sum_lj + potential_lj
        if average_water != 0:
            sum_coulomb_average = sum_coulomb / average_water
            sum_lj_average = sum_lj / average_water
        else:
            n += 1

        return sum_coulomb_average, sum_lj_average, n

    def run(self):
        sum_coulomb_fin = 0
        sum_lj_fin = 0
        sum_n = 0
        #self._selection_serial()
#       for i in range(len(self.selection_water_array)):
        #widgets = [' [', progressbar.Percentage(), '] ', progressbar.Bar(), ' ', progressbar.ETA()]
        #bar = progressbar.ProgressBar(maxval= self.universe.trajectory.n_frames)
        #bar.start()
        for i in tqdm(range(self.universe.trajectory.n_frames)):
            #print(i)
            self.universe.trajectory[i]
            selection_water2 = self.universe.select_atoms(self.selection_water)
            selection_CL2 = self.universe.select_atoms(self.selection_CL)
            delta_coulomb, delta_lj, n = self._getOneDeltaPoint(selection_water2, selection_CL2)
            sum_coulomb_fin = sum_coulomb_fin + delta_coulomb
            sum_lj_fin = sum_lj_fin + delta_lj
            sum_n = sum_n + n
            # i = i + 1
            #bar.update(i)
        #bar.finish()
        sum_coulomb_average = sum_coulomb_fin / (self.universe.trajectory.n_frames - sum_n)
        sum_lj_average = sum_lj_fin / (self.universe.trajectory.n_frames - sum_n)
        print(sum_coulomb_average, sum_lj_average)


    def run_test(self):
        sum_coulomb_fin = 0
        sum_lj_fin = 0
        #self._selection_serial()
#       for i in range(len(self.selection_water_array)):
        #widgets = [' [', progressbar.Percentage(), '] ', progressbar.Bar(), ' ', progressbar.ETA()]
        #bar = progressbar.ProgressBar(maxval= self.universe.trajectory.n_frames)
        #bar.start()
        self.universe.trajectory[60381]
        selection_water2 = self.universe.select_atoms(self.selection_water)
        selection_CL2 = self.universe.select_atoms(self.selection_CL)
        delta_coulomb, delta_lj = self._getOneDeltaPoint(selection_water2, selection_CL2)
        sum_coulomb_fin = sum_coulomb_fin + delta_coulomb
        sum_lj_fin = sum_lj_fin + delta_lj
            # i = i + 1
            #bar.update(i)
        #bar.finish()
        sum_coulomb_average_all = sum_coulomb_fin / self.universe.trajectory.n_frames
        sum_lj_average_all = sum_lj_fin / self.universe.trajectory.n_frames
        print(sum_coulomb_average_all, sum_lj_average_all)

    def test(self):
        sum_coulomb_fin = 0
        sum_lj_fin = 0
        #widgets = [' [', progressbar.Percentage(), '] ', progressbar.Bar(), ' ', progressbar.ETA()]
        for i in tqdm(range(self.universe.trajectory.n_frames )):
            self.universe.trajectory[i]
            selection_water2 = (self.universe.select_atoms(self.selection_water).positions)
            selection_CL2 = (self.universe.select_atoms(self.selection_CL).positions)
            delta_coulomb, delta_lj, n = self._getOneDeltaPoint(selection_water2, selection_CL2)
            sum_coulomb_fin = sum_coulomb_fin + delta_coulomb
            sum_lj_fin = sum_lj_fin + delta_lj

        sum_coulomb_average = sum_coulomb_fin / (self.universe.trajectory.n_frames - n)
        sum_lj_average = sum_lj_fin / (self.universe.trajectory.n_frames - n)
        print(sum_coulomb_average, sum_lj_average)


if __name__ == '__main__':
    tpr = "product.tpr"
    xtc = "product.trr"

    universe = MDAnalysis.Universe(tpr, xtc)
    selection = "resname SOL"
    selection2 = "resname Na"
    energy = Energy(universe, selection, selection2)
    #60381
    energy.run()
    #energy.run_test()

