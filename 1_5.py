input_file_path = '1.txt'

output_file_path = '1_m.txt'

with open(input_file_path, 'r') as file:
    lines = file.readlines()

with open(output_file_path, 'w') as file:
    for line in lines:
        parts = line.rstrip().split()  
        if len(parts) >= 3:
            if len(parts[0]) == 3:
                parts[0] = parts[0]
            elif len(parts[0]) == 2 :
                parts[0] = " " + parts[0]
            else :
                parts[0] = "  " + parts[0]
            if len(parts[1]) == 3:
                parts[1] = parts[1]
            elif len(parts[1]) == 2 :
                parts[1] = " " + parts[1]
            else :
                parts[1] = "  " + parts[1]
            if len(parts[2]) <= 1:
                parts[2] = parts[2]             
            modified_line = "  " + parts[0] + "   " + parts[1] + "     " + "5" + "\n"
            file.write(modified_line)
        else:
            file.write(line)


