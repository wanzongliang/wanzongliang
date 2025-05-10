def remove_duplicates(input_file, output_file):
    unique_values = set()  
    with open(input_file, 'r') as f:
        lines = f.readlines()  
    with open(output_file, 'w') as f:
        for line in lines:
            parts = line.split()  
            if len(parts) >= 2:
                value = parts[1]  
                if value not in unique_values: 
                    unique_values.add(value)  
                    f.write(line)  

if __name__ == "__main__":
    input_file = "fes.dat"
    output_file = "fes.txt"
    remove_duplicates(input_file, output_file)
    print("Duplicates removed and saved to output.txt")
