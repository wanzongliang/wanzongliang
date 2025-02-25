import pandas as pd
import numpy as np

def process_fes_data(file_path, output_path):
    data = pd.read_csv(file_path, delim_whitespace=True, comment='#', names=['d', 's', 'free_energy', 'der_d', 'der_s'])

    d = data['d']
    s = data['s']
    free_energy = data['free_energy']

    unique_d = np.unique(d)
    unique_s = np.unique(s)
    free_energy_matrix = free_energy.values.reshape(len(unique_s), len(unique_d))
    transposed_matrix = np.transpose(free_energy_matrix)

    np.savetxt(output_path, transposed_matrix, delimiter='\t')

process_fes_data('fes.dat', 'fes_data.txt')
