input_file = "5.txt"  
output_file = "5_2.txt"  

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        data = line.strip().split()

        text_line = '    '.join(data)

        outfile.write(text_line + '\n')

print(f"Conversion complete. Text data written to {output_file}")
