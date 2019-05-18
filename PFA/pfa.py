

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
            final_state.append(d)
    # print(c)
fs = []
print(final_state)
for i in range(len(final_state)-1):
    for j in range(i + 1,len(final_state)-2):
        if final_state[i] == final_state[j]:
            print(j)
            print(final_state[j])
            final_state.remove(final_state[j])
            # print(len(final_state))
            print(final_state)
            j = j -1
            print(j)
#             fs.append(final_state)
# print(fs)
print(final_state)


# cities = "Tehran, Esfehan, Zahedan, Kerman, Shirvn, Sanandaj"
# cities_list = cities.split(",")
# cities_list.remove(cities_list[3])
# print (cities_list)