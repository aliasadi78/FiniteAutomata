

readme = open('input.txt','r').readlines()
a = ''
b = []
for i in readme:
    a = i.replace('\n','')
    b.append(a)
#     print(b[i])
print(b)