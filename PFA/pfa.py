

readme = open('input.txt','r').readlines()
a = ''
bb = []
b = []
for i in readme:
    a = i.replace('\n','')
    b.append(a)
#     print(b[i])

start_state = []
final_state = []
c = []
d = []
d1 = []
e = []
e1 = []
for i in range(len(b)):
    if i > 1:
        c = b[i].split(",")
        d = c[2].split(" ")
        d1 = c[2].split(" ")
        e = d[0][0]
        e1 = d[0][0]
        if e[0] == "*":
            final_state.append(d[0])
        if e1[0] == "*":
            final_state.append(d1[0])

final_state = list(set(final_state))
# print(final_state)
for i in range(len(b)):
    if i > 1:
        c = b[i].split(",")
        d = c[0].split(" ")
        d1 = c[0].split(" ")
        e = d[0][0]
        e1 = d[0][0]
        if e[0] == "-":
            start_state.append(d[0])
        if e1[0] == "-":
            start_state.append(d1[0])

start_state = list(set(start_state))
h = start_state[0].replace('->','')
start_state[0] = h
print(start_state)

a = b[2].replace('->','')
b[2] = a
bn = b
b.remove(b[0])
b.remove(b[0])
print(b)
A = []
B = []
T = []
A1 = []
B1 = []
T1 = []

tb = b.copy()
S = len(tb)
v = 0
for i in range(S):
    if S > 0:
        B1 = []
        if i > 0:
            i -= v
        A1 = tb[i].split(',')
        B1.append(A1[0])
        a1 = []
        b1 = []
        t1 = []
        u = 0
        for j in range(S):

            if j > 0:
                j -= u
            Q = tb[j].split(',')

            if B1[0] == Q[0]:
                del tb[j]
                u += 1
                S = len(tb)

                if Q[1] == "a":
                    a1.append(Q[2])
                if Q[1] == "b":
                    b1.append(Q[2])
                if Q[1] == "_":
                    t1.append(Q[2])
            else:
                v += 1
                break

        A.append(a1)
        B.append(b1)
        T.append(t1)

print(A)
print(B)
print(T)
T1 = []
T2 = []
for i in range(len(b)):
    a = []
    a = b[i].split(',')
    if a[1] == '_':
        T1.append(a[0])
        T2.append(a[2])
# print(T1)
# print(T2)
matrix = []
matrixA = []
matrixB = []
matrix.append(start_state)
print(matrix)

matrixA.append(A[0])
print(matrixA)































