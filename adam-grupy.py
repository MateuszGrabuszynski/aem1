import matplotlib.pyplot as plt
import re

file = open("Rezultaty2.txt")
data = file.read()

lines = data.split('\n')
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

for line in lines:
    if re.search(r'For group number [0-9]+', line):
        group_nr = int(line.split(' ')[-1])
        print(f'Group: {group_nr}')
    elif re.search(r'First Point\(x: [0-9]+, y: [0-9]+\)', line):
        pass
    else:
        print(line.split(' '))
        x1, y1, x2, y2, _, _ = line.split(' ')
        x = [int(x1), int(x2)]
        y = [int(y1), int(y2)]
        plt.plot(x, y , marker='o', c=colors[group_nr])
plt.show()







