
def max_acc(y0, x0, y1, x1):
    curr_acc = int(matrix[y0-1][x0-1])
    #print "looking", x0, y0, " -> ", x1, y1

    if (x0 == x1) and (y0 == y1):
        return 0
    elif (x0 == x1):
        curr_acc += max_acc(y0+1, x0, y1, x1)
    elif (y0 == y1):
        curr_acc += max_acc(y0, x0+1, y1, x1)
    else:
        a = max_acc(y0+1, x0, y1, x1)
        b = max_acc(y0, x0+1, y1, x1)

        #print "a =", a
        #print "b =", b

        curr_acc += max(a, b)

    #print "returning ", curr_acc
    return curr_acc


matrix ="""
75 41
93 4
38 52
28 66
74 42
43 83
24 100
99 19
91 91
14 7
7 65
46 35
23 34
30 46
49 76
50 97
59 86
51 57
71 34
"""

checkpoint = """
2 1
9 1
10 1
11 1
12 1
13 1
15 1
17 1
19 2
"""


matrix = matrix[1:-1]
matrix = matrix.split("\n")
matrix = [row.split(" ") for row in matrix]

checkpoint = checkpoint[1:-1]
checkpoint = checkpoint.split("\n")
checkpoint = [row.split(" ") for row in checkpoint]

print matrix
print checkpoint

s = 0
p = [1, 1]
for c in checkpoint:
    cc = [int(c[0]), int(c[1])]

    print "looking", p[0], p[1], " -> ", cc[0], cc[1]
    m = max_acc(p[0],p[1], cc[0],cc[1])

    s += m
    p = cc

len_y = len(matrix)
len_x = len(matrix[0])
s += int(matrix[len_y-1][len_x-1])

print s
