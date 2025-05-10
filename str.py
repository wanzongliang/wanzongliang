mapping = {}
for i in range(1, 59):
    if i !=7 and i!=43:
        mapping[str(i)] = 'C'
    else:
        mapping[str(i)] = 'N'
for i in range(59, 133):
    mapping[str(i)] = 'H'

data = []
with open('5.txt', 'r') as file:
    for line in file:
        data.append(line.strip().split('\t'))

for i in range(len(data)):
    for j in range(len(data[i])):
        data[i][j] = mapping.get(data[i][j], data[i][j])

with open('5_1.txt', 'w') as file:
    for row in data:
        file.write('\t'.join(row) + '\n')
