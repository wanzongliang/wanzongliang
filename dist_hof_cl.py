import numpy as np
import re

def parse_gro_file(file_path):
    atoms = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[2:-1]:  
            res_num = int(line[0:5].strip())
            res_name = line[5:10].strip()
            #print(res_name)
            atom_name = line[10:15].strip()
            #print(atom_name)
            atom_num = int(line[15:20].strip())
            x = float(line[20:28].strip())
            y = float(line[28:36].strip())
            z = float(line[36:44].strip())
            atoms.append((res_num, res_name, atom_name, atom_num, x, y, z))
    return atoms

def calculate_distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2 + (coord1[2] - coord2[2])**2)

def find_nearby_oxygens(file_path, cutoff_distance=0.318):
    atoms = parse_gro_file(file_path)
    cl_coords = [atom[4:] for atom in atoms if atom[2] == 'CL']
    #print(cl_coords)
    HOF_coords = [(atom[3], atom[4:]) for atom in atoms if atom[1] == 'SQ' and re.match(r'H\d+', atom[2])]
    #print(o_coords)

    nearby_oxygens = []
    for cl_coord in cl_coords:
        for HOF_num, HOF_coord in HOF_coords:
            distance = calculate_distance(HOF_coord, cl_coord)
            if distance < cutoff_distance:
                nearby_oxygens.append(HOF_num)
                #break  

    return nearby_oxygens


file_path = 'product.gro'
nearby_oxygens = find_nearby_oxygens(file_path)
print("H atoms within 0.318 nm distance from any CL ion:")
for o_num in nearby_oxygens:
    print(o_num)
