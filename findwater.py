import MDAnalysis
from tqdm import tqdm

class Orientation(object):
    def __init__(self,universe,selection_water):
        # class universe
        self.universe = universe
        # str
        self.selection_water = selection_water
        # str
        self.universe.trajectory = universe.trajectory

    def position(self,selection_water_array):

        O_atom = selection_water_array[::3]
        y = O_atom.positions
        #print(y)
        n = 0
        for i in y:
            if i[1] >= 0 and i[1] <= 42.6:
                n += 1
        return n


    def run(self):
        count = 0
        array = []
        for i in tqdm(range(self.universe.trajectory.n_frames)):
            self.universe.trajectory[i]
            selection_water_array = self.universe.select_atoms(self.selection_water)
            temp = self.position(selection_water_array)
            array.append(temp)
            count += temp
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        print(array)
        print(count / self.universe.trajectory.n_frames)


if __name__ == '__main__':
    tpr = "equilibrium.tpr"
    xtc = "equilibrium2.xtc"

    universe = MDAnalysis.Universe(tpr, xtc)
    selection = "resname SOL"
    Orientation(universe, selection).run()
