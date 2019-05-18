

readme = open('input.txt','r').readlines()
a = ''
b = []
for i in readme:
    a = i.replace('\n','')
    b.append(a)
#     print(b[i])
# print(b)
start_state = ['q0']
final_state = []
c =[]
d = []
e = []
for i in range(len(b)):
    if i > 1:
        c = b[i].split(",")
        d = c[2].split(" ")
        e = d[0][0]
        if e[0] == "*":
            final_state.append(d[0])

fs = list(set(final_state))
print(fs)
