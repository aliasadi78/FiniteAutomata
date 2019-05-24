from NODE import *
from Finite_Automata import *
class queue:
    def __init__(self):
        self.queue=[]
        self.size=0
    def enqueue(self,item):
        self.queue+=[item]
        self.size+=1
    def dequeue(self):
        if self.size>0:
            item=self.queue[0]
            del self.queue[0]
            self.size-=1
            return item
        

class App:
    def __init__(self,file_address):
        self.file_address=file_address
        self.NFA=None
        self.DFA=None
        self.Alphabet=None
    def creat_NFA(self):
        #read file
        Lines=open(self.file_address,'r').readlines()
        self.Alphabet=Lines[1].replace('\n','').split(',')
        NFA_Alphabet=self.Alphabet+["_"]
        self.NFA=Finite_Automata(NFA_Alphabet,int(Lines[0]),'nfa')
        self.NFA.Start_Variable=self.NFA.States[0]
        #complete nfa"
        for line in range(2,len(Lines)):
            info=Lines[line].split(',')
            origin_index=int(info[0].split('q')[1])
            destination_index=int(info[2].replace('\n','').split('q')[1])
            self.NFA.States[origin_index].Nueighbor[info[1]]+=[self.NFA.States[destination_index]]
            #final states"
            if "*" in info[0]:
                self.NFA.States[origin_index].Final_state=True
            if "*" in info[2]:
                self.NFA.States[destination_index].Final_state=True
        
    def convert_NFA_to_DFA(self):
        self.DFA=Finite_Automata(self.Alphabet,0,'dfa')
        self.NFA.convert_nfa_to_dfa(self.DFA)

    def print_DFA(self):
        #print number of states
        print(self.DFA.Number_State)

        #print Alphabet
        result=''
        for symbol in self.Alphabet:
            result+=symbol+','
        print(result)

        #print start variable with this transition
        if self.DFA.States[0].Final_state:
            origin_str='->*'+self.DFA.States[0].Name
        else:
            origin_str='->'+self.DFA.States[0].Name

        
        for symbol in self.Alphabet:
            if self.DFA.States[0].Nueighbor[symbol].Final_state:
                dest_str='*'+self.DFA.States[0].Nueighbor[symbol].Name
            else:
                dest_str=self.DFA.States[0].Nueighbor[symbol].Name

            result=origin_str+','+symbol+','+dest_str
            print(result)

        #print other state with them transition
        for state_index in range(1,self.DFA.Number_State):
            if self.DFA.States[state_index].Final_state:
                origin_str='*'+self.DFA.States[state_index].Name
            else:
                origin_str=self.DFA.States[state_index].Name

            
            for symbol in self.Alphabet:
                if self.DFA.States[state_index].Nueighbor[symbol].Final_state:
                    dest_str='*'+self.DFA.States[state_index].Nueighbor[symbol].Name
                else:
                    dest_str=self.DFA.States[state_index].Nueighbor[symbol].Name

                result=origin_str+','+symbol+','+dest_str
                print(result)


App=App("input.txt")
App.creat_NFA()
App.convert_NFA_to_DFA()
App.print_DFA()

Info = App.Alphabet
DFA = App.DFA.States
DF = DFA.copy()

Final_States = []
Non_Final_States = []
l = 0
for i in range(len(DFA)):
    if DFA[i].Final_state == True:
        DFA[i].Tag = 'g' + str(l) + '2'
    else:
        DFA[i].Tag = 'g' + str(l) + '1'
Tags = ['g01', 'g02']

l = 1
States = DFA.copy()
St = DFA.copy()
Tags = []
def Tag():
    tags = Tags.copy()
    Tags.clear()
    v = 1
    l = 1
    S = len(States)
    K = []
    SS = []
    for i in range(S):
        # T = False
        for j in range(i,S):
            # T = False
            if i != j:
                if j < S:
                    if States[i].Tag == States[j].Tag:
                        for symbol in Info:
                            if States[i].Nueighbor[symbol] == States[j].Nueighbor[symbol]:
                                T = True
                            else:
                                T = False
                                break
                        if T:
                            K.append(States[i].Tag)
                            SS.append(States[i])
                            States[i].Tag = 'g' + str(v) + str(l)
                            Tags.append(States[i].Tag)
                            States[j].Tag = 'g' + str(v) + str(l)
                            States.remove(States[i])
                            States.insert(i,'1')
                            if States[j] == '1':
                                States.remove(States[j + 1])
                            else:
                                States.remove(States[j])
                            States.remove('1')
                            St.remove(St[j])
                            l += 1
                            S -= 2
    ss = len(States)
    T = False
    for i in range(ss):
        # T = True
        if i >= ss:
            i -= 1
        for j in range(len(SS)):
            # T = True
            if States[i].Tag == K[0]:
                for k in range(len(Info)):
                    if k + 1 < len(Info):
                        if States[i].Nueighbor[Info[k]].Name == SS[j].Name:
                            if States[i].Nueighbor[Info[k + 1]].Name == SS[j].Nueighbor[Info[k + 1]].Name:
                                T = True
                        else:
                            T = False
                            break
                if T:
                    a = SS[j].Tag[-1]
                    States[i].Tag = 'g' + str(v) + a
                    States.remove(States[i])
                    St.remove(St[i])
                    ss -= 1
    for i in range(len(States)):
        States[i].Tag = 'g' + str(v) + str(l)
        Tags.append(States[i].Tag)
        l += 1
    for i in range(len(DFA)):
        for symbol in Info:
            if type(DFA[i].Nueighbor[symbol]) is str:
                DFA[i].Nueighbor[symbol] = DFA[i].Nueighbor[symbol]
            else:
                DFA[i].Nueighbor[symbol] = DFA[i].Nueighbor[symbol].Tag



Tag()
# tag()
for tag in Tags:
    T = False
    for i in range(len(DFA)):
        for j in range(len(DFA)):
            if DFA[i].Tag == tag:
                if DFA[i].Tag == DFA[j].Tag:
                    for symbol in Info:
                        if DFA[i].Nueighbor[symbol] != DFA[j].Nueighbor[symbol]:
                            T = True
                    if T:
                        print(tag,i,j,DFA[i].Nueighbor[symbol],DFA[j].Nueighbor[symbol])
                        Tag()
                        break

#
for i in range(len(St)):
    St[i].Name = 'g' + str(i + 1)
for i in range(len(St)):
    if St[i].Final_state:
        St[i].Name = '*g' + str(i + 1)

for i in range(len(St)):
    for j in range(len(St)):
        for symbol in Info:
            if St[i].Nueighbor[symbol] == St[j].Tag:
                St[i].Nueighbor[symbol] = St[j].Name

print(len(St))
re = ''
for i in range(len(Info)):
    if i != len(Info) - 1:
        re += Info[i] + ','
    else:
        re += Info[i]
print(re)
for i in range(len(St)):
    for sy in Info:
        if i == 0 :
            result = '->' + St[i].Name + ',' + sy + ',' + St[i].Nueighbor[sy]
            print(result)
        else:
            result = St[i].Name + ',' + sy + ',' + St[i].Nueighbor[sy]
            print(result)
