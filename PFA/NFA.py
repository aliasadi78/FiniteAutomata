class queue:
    def __init__(self):
        self.queue = []
        self.size = 0

    def enqueue(self, item):
        self.queue += [item]
        self.size += 1

    def dequeue(self):
        if self.size > 0:
            item = self.queue[0]
            del self.queue[0]
            self.size -= 1
            return item

"nodes for dfa and nfa state"
class NODE:
    def __init__(self, name, Alphabet):
        "for dfa node"
        self.nfa_states = []
        "end dfa athribute"
        self.Nueighbor = dict()
        "creat dict of transition for node"
        self.Nueighbor = dict()
        for key in Alphabet:
            self.Nueighbor[key] = []
        self.Final_state = bool()
        self.Name = name
        self.Tag = ''

"class for dfa and nfa"
class Finite_Automata:
    def __init__(self, Alphabet, Number_state, dfa_or_nfa):
        self.Start_Variable = None
        self.Alphabet = Alphabet
        self.Number_State = Number_state
        self.States = []

        "build states for nfa and add to self.states"
        if dfa_or_nfa == "nfa":
            for number in range(Number_state):
                name = 'q' + str(number)
                new_node = NODE(name, self.Alphabet)
                self.States += [new_node]

    "sort list of nodes for checking new_list==dfa_states[i] base of bubble sort"
    def sort_nodes_list(self, nodes_list):
        n = len(nodes_list)

        # Traverse through all array elements
        for i in range(n):

            # Last i elements are already in place
            for j in range(0, n - i - 1):

                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if nodes_list[j].Name > nodes_list[j + 1].Name:
                    nodes_list[j], nodes_list[j + 1] = nodes_list[j + 1], nodes_list[j]

    "lambda covert for find all lambda transition"
    def lambda_convert(self, states):
        state_queue = queue()
        for state in states:
            state_queue.enqueue(state)
        while state_queue.size > 0:
            current_state = state_queue.dequeue()
            for state in current_state.Nueighbor['_']:
                if state not in states:
                    state_queue.enqueue(state)
                    states += [state]
        return states.copy()

    "symbol convert"
    def symbol_convert(self, states, symbol):
        result_list = []
        for state in states:
            for nueighbor in state.Nueighbor[symbol]:
                if nueighbor not in result_list:
                    result_list += [nueighbor]

        return result_list

    def convert_nfa_to_dfa(self, dfa):
        dfa_states = []
        "add start varieble and lambda transition to dfa state"
        dfa_states += [self.lambda_convert([self.Start_Variable])]
        "sort all of nodes list"
        self.sort_nodes_list(dfa_states[0])
        # print(dfa_states)
        "creat first dfa node"
        number_dfa_nodes = 0
        name = "q0"
        new_dfa_node = NODE(name, dfa.Alphabet)
        dfa.Start_Variable = new_dfa_node
        new_dfa_node.nfa_states = dfa_states[0]
        "add new state to dfa states"
        dfa.States += [new_dfa_node]
        "end creat"
        "creat queue to check"
        state_queue = queue()
        state_queue.enqueue(new_dfa_node)
        "add one by one dfa states to queue and find this transiton"
        j = 0
        while state_queue.size > 0:
            current_node = state_queue.dequeue()
            for symbol in dfa.Alphabet:
                # j+=1
                creat_new_node = True
                # for state in current_node.nfa_states:
                # print(state.Name)
                new_list = self.symbol_convert(current_node.nfa_states, symbol).copy()
                new_list = self.lambda_convert(new_list).copy()
                self.sort_nodes_list(new_list)
                for i in range(number_dfa_nodes + 1):
                    if new_list == dfa_states[i]:
                        # print("*****************"+str(j))
                        current_node.Nueighbor[symbol] = dfa.States[i]
                        creat_new_node = False
                        break
                if creat_new_node:
                    # print(j)
                    number_dfa_nodes += 1
                    name = "q" + str(number_dfa_nodes)
                    # print(number_dfa_nodes)
                    new_node = NODE(name, dfa.Alphabet)
                    dfa_states += [new_list.copy()]
                    new_node.nfa_states = new_list.copy()
                    dfa.States += [new_node]
                    state_queue.enqueue(new_node)
                    current_node.Nueighbor[symbol] = new_node
                    for state in new_node.nfa_states:
                        if state.Final_state:
                            new_node.Final_state = True
                            break
                            # return dfa_states

class App:
    def __init__(self, file_address):
        self.file_address = file_address
        self.NFA = None
        self.DFA = None
        self.Alphabet = None

    def creat_NFA(self):
        Lines = open(self.file_address, 'r').readlines()
        self.Alphabet = Lines[1].replace('\n', '').split(',')
        NFA_Alphabet = self.Alphabet + ["_"]
        self.NFA = Finite_Automata(NFA_Alphabet, int(Lines[0]), 'nfa')
        self.NFA.Start_Variable = self.NFA.States[0]
        "complete nfa"
        for line in range(2, len(Lines)):
            info = Lines[line].split(',')
            origin_index = int(info[0].split('q')[1])
            destination_index = int(info[2].replace('\n', '').split('q')[1])
            self.NFA.States[origin_index].Nueighbor[info[1]] += [self.NFA.States[destination_index]]
            "final states"
            if "*" in info[0]:
                self.NFA.States[origin_index].Final_state = True
            if "*" in info[2]:
                self.NFA.States[destination_index].Final_state = True

    def convert_NFA_to_DFA(self):
        self.DFA = Finite_Automata(self.Alphabet, 0, 'dfa')
        self.NFA.convert_nfa_to_dfa(self.DFA)

    def print_DFA(self):
        for state in self.DFA.States:
            for symbol in self.Alphabet:
                result = state.Name + ',' + symbol + ',' + state.Nueighbor[symbol].Name
                print(result)

App = App("input.txt")
App.creat_NFA()
App.convert_NFA_to_DFA()
# App.print_DFA()
DFA = App.DFA.States

print('    a',' b')
for i in range(len(DFA)):
    print(DFA[i].Name, DFA[i].Nueighbor['a'].Name,DFA[i].Nueighbor['b'].Name)

Final_States = []
Non_Final_States = []
l = 0
for i in range(len(DFA)):
    if DFA[i].Final_state == True:
        DFA[i].Tag = 'g' + str(l) + '2'
    else:
        DFA[i].Tag = 'g' + str(l) + '1'
Tags = ['g01','g02']
for i in range(len(DFA)):
    if App.DFA.States[i].Final_state == True:
        Final_States.append(App.DFA.States[i])
    else:
        Non_Final_States.append(App.DFA.States[i])

g01 = Non_Final_States.copy()
g02 = Final_States.copy()
# for i in range(len(DFA)):
#     if DFA[i].Nueighbor['a'] in g01:
#         DFA[i].Nueighbor['a'] = 'g01'
#     if DFA[i].Nueighbor['a'] in g02:
#         DFA[i].Nueighbor['a']= 'g02'
#     if DFA[i].Nueighbor['b'] in g01:
#         DFA[i].Nueighbor['b'] = 'g01'
#     if DFA[i].Nueighbor['b'] in g02:
#         DFA[i].Nueighbor['b'] = 'g02'
for i in range(len(DFA)):
    if DFA[i].Nueighbor['a'].Tag == Tags[0]:
        DFA[i].Nueighbor['a'] = Tags[0]
    elif DFA[i].Nueighbor['a'].Tag == Tags[1]:
        DFA[i].Nueighbor['a'] = Tags[1]
    if DFA[i].Nueighbor['b'].Tag == Tags[0]:
        DFA[i].Nueighbor['b'] = Tags[0]
    elif DFA[i].Nueighbor['b'].Tag == Tags[1]:
        DFA[i].Nueighbor['b'] = Tags[1]


print('      a','  b','   tag')
print('   ','---------')
for i in range(len(DFA)):
    if DFA[i].Tag == Tags[0]:
        print(DFA[i].Name,'|', DFA[i].Nueighbor['a'],DFA[i].Nueighbor['b'],'|',DFA[i].Tag)
print('   ','---------')
for i in range(len(DFA)):
    if DFA[i].Tag == Tags[1]:
        print(DFA[i].Name,'|',DFA[i].Nueighbor['a'],DFA[i].Nueighbor['b'],'|',DFA[i].Tag)
print('   ','---------')

# for i in range(len(g01)):
#     for j in range(1,len(g01)):
#         if g01[i].Nueighbor['a'] != g01[j].Nueighbor['a']:
#             queue.enqueue(g01[j].Nueighbor['a'])
l = 1



def tag():
    l = 1
    v = 1
    tags = Tags.copy()
    Tags.clear()
    a = DFA[0].Tag
    a = 'g' + str(l)
    Tags.append(a)
    for tag in tags:
        for i in range(len(DFA)):
            for j in range(i,len(DFA)):
                if tag == DFA[i].Tag and tag == DFA[j].Tag :
                    if i != j:
                        if DFA[i].Nueighbor['a'] == DFA[j].Nueighbor['a'] and DFA[i].Nueighbor['b'] == DFA[j].Nueighbor['b']:
                            if i != 0:
                                Tags.append('1')
                                l = len(Tags)
                                DFA[i].Tag = 'g' + str(l)
                                # DFA[j].Tag = 'g' + str(l)
                                Tags.append(DFA[i].Tag)
                                Tags.remove('1')
                            else:
                                # DFA[i].Tag = 'g' + '1'
                                DFA[j].Tag = 'g' + '1'
                            # print(DFA[i].Tag, DFA[j].Tag)
                        if DFA[i].Nueighbor['a'] != DFA[j].Nueighbor['a'] or DFA[i].Nueighbor['b'] != DFA[j].Nueighbor['b']:
                            if i != 0:
                                Tags.append('1')
                                l = len(Tags)
                                DFA[i].Tag = 'g' + str(l)
                                # DFA[j].Tag = 'g' + str(l+1)
                                Tags.append(DFA[i].Tag)
                                Tags.remove('1')
                            # else:
                            #     # Tags.append('2')
                            #     # l = len(Tags)
                            #     DFA[i].Tag = 'g' + str(l)
                            #     # Tags.remove('2')
    DFA[0].Tag = 'g' + str(1)
    # print(DFA)

    print(Tags)
tag()


print('      a','  b','   tag')
print('   ','---------')
# for i in range(len(DFA)):
#     if DFA[i].Tag == Tags[0]:
#         print(DFA[i].Name,'|', DFA[i].Nueighbor['a'],DFA[i].Nueighbor['b'],'|',DFA[i].Tag)
# print('   ','---------')
# for i in range(len(DFA)):
#     if DFA[i].Tag == Tags[1]:
#         print(DFA[i].Name,'|',DFA[i].Nueighbor['a'],DFA[i].Nueighbor['b'],'|',DFA[i].Tag)
# print('   ','---------')
# for i in range(len(DFA)):
#     if DFA[i].Tag == Tags[2]:
#         print(DFA[i].Name,'|',DFA[i].Nueighbor['a'],DFA[i].Nueighbor['b'],'|',DFA[i].Tag)
# print('   ','---------')
# for i in range(len(DFA)):
#     if DFA[i].Tag == Tags[3]:
#         print(DFA[i].Name,'|',DFA[i].Nueighbor['a'],DFA[i].Nueighbor['b'],'|',DFA[i].Tag)
# print('   ','---------')

for j in range(len(Tags)):
    for i in range(len(DFA)):
        if DFA[i].Tag == Tags[j]:
            print(DFA[i].Name,'|',DFA[i].Nueighbor['a'],DFA[i].Nueighbor['b'],'|',DFA[i].Tag)
    print('   ','---------')

