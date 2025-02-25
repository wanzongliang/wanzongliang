def add_columns(file_path, output_file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    first_column = []
    second_column = []

    for line in lines:
        parts = line.split()
        if len(parts) == 2:
            first_column.append(float(parts[0]))
            second_column.append(float(parts[1]))
        elif len(parts) != 2:
            first_column.append(float(parts[0]))

    with open(output_file_path, 'w') as output_file:
        for first_val in first_column:
            for second_val in second_column:
                sum_value = first_val + second_val
                output_file.write(f"{sum_value:.3f}\t")
            output_file.write("\n")  

if __name__ == "__main__":
    file_path = "awh_15.txt"  
    output_file_path = "data_15.txt"  
    add_columns(file_path, output_file_path)


