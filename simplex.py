import sys

if len(sys.argv) <= 1:
    print("No file passed as argument")
    sys.exit()

f = open(sys.argv[1])

dimensions = f.readline().split(" ")
dimensions = map(int,dimensions) #converte string para inteiro.
m = dimensions[0]-1
n = dimensions[1] - m

M = []
for line in f:
    line = line.split(" ")
    M.append(map(int,line))

f.close()

print M
