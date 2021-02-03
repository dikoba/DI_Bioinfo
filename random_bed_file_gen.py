import random

file = open('regions4.bed', 'w')

for i in range(200_000):
    file.write('\t'.join(['chr1', str(random.randint(0,100)), str(random.randint(110, 700)), 'name', '0', '+']))
    file.write('\n')
file.close()


