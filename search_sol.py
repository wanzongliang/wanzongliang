


def read_gro_file(file_path):
    n = 0
    with open(file_path, 'r') as file:
        for line in file:
            data = line.split()
            if len(data) >= 6 and 'SOL' in data[0] and 'O' in data[1]:  
                try:
                    y_coordinate = float(data[4])  
                    if 0 <= y_coordinate <= 4.26:
                        n += 1
                except ValueError:
                    continue
    return n

if __name__ == "__main__":
    file_path = 'eq.gro'  
    n = read_gro_file(file_path)
    print(n)
