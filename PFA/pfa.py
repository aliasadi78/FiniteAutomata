

readme = open('input.txt','r').readlines()
a = ''
b = []
for i in readme:
    a = i.replace('\n','')
    b.append(a)
#     print(b[i])
# print(b)
start_state = []
final_state = []
c =[]
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
print(final_state)
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
print(start_state)
