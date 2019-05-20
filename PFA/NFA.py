class NODE:
    def __init__(self,name,Alphabet):
        self.Nueighbor = dict()
        for key in Alphabet:
            self.Nueighbor[key] = []
        self.Final_state=bool()
        self.Name = name

class NFA:
    def __init__(self,Alphabet,Number_state):
        self.Start_Variable = None
        self.Alphabet = Alphabet
        self.Number_State = Number_state
        self.States = []
        for number in range(Number_state):
            name = 'q' + str(number)
            new_node = NODE(name,self.Alphabet)
            self.States += [new_node]

Lines = open("input.txt",'r').readlines()
Alphabet = Lines[1].replace('\n','').split(',')
Alphabet.append("_")
NFA = NFA(Alphabet,int(Lines[0]))
for line in range(2,len(Lines)):
    info = Lines[line].split(',')
    origin_index = int(info[0].split('q')[1])
    destination_index = int(info[2].replace('\n','').split('q')[1])
    NFA.States[origin_index].Nueighbor[info[1]] += [NFA.States[destination_index]]

# print(NFA.States)
print(NFA.States[0].Nueighbor)
# for i in range(NFA.Number_State):
#     NFA.Number_State[i]
def Convert():
