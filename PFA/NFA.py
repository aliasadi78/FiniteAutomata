
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


# nodes for dfa and nfa state"
class NODE:
    def __init__(self, name, Alphabet):
        # for dfa node to determine what states on nfa constract nodes of dfa"
        self.nfa_states = []

        self.Nueighbor = dict()
        # creat dict with empty list for transitions"
        for key in Alphabet:
            self.Nueighbor[key] = []
        self.Final_state = False
        self.Name = name
        self.Tag = ''


# class for dfa and nfa"
class Finite_Automata:
    def __init__(self, Alphabet, Number_state, dfa_or_nfa):
        self.Start_Variable = None
        self.Alphabet = Alphabet
        self.Number_State = Number_state

        # list of states of finite automata for acsess them
        self.States = []

        # build states for nfa beacuse know them"
        if dfa_or_nfa == "nfa":
            for number in range(Number_state):
                name = 'q' + str(number)
                new_node = NODE(name, self.Alphabet)
                self.States += [new_node]

    # sort list of nodes for checking new_list==dfa_states[i] base of bubble sort"
    def sort_nodes_list(self, nodes_list):
        n = len(nodes_list)
        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                if nodes_list[j].Name > nodes_list[j + 1].Name:
                    nodes_list[j], nodes_list[j + 1] = nodes_list[j + 1], nodes_list[j]

    # lambda covert for find all lambda transition"
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

    # symbol convert"
    def symbol_convert(self, states, symbol):
        result_list = []
        for state in states:
            for nueighbor in state.Nueighbor[symbol]:
                if nueighbor not in result_list:
                    result_list += [nueighbor]

        return result_list

    def convert_nfa_to_dfa(self, dfa):
        dfa_states = []
        # add start varieble and lambda transition to dfa state"
        dfa_states += [self.lambda_convert([self.Start_Variable])]

        # after build list of nfa states for each dfs node should sort this for compare in futur
        self.sort_nodes_list(dfa_states[0])

        # number of states in dfa
        number_dfa_nodes = 0

        # creat first dfa node"
        name = "q0"
        new_dfa_node = NODE(name, dfa.Alphabet)
        dfa.Start_Variable = new_dfa_node
        new_dfa_node.nfa_states = dfa_states[0]
        # add new state to dfa states"
        dfa.States += [new_dfa_node]
        # end creat"

        # creat queue to check tansition of all of new node in dfa "
        state_queue = queue()
        state_queue.enqueue(new_dfa_node)

        # add one by one dfa states to queue and find this transiton"
        while state_queue.size > 0:
            current_node = state_queue.dequeue()
            for symbol in dfa.Alphabet:

                # bolean for check the new list of nfa nodes created befor
                creat_new_node = True

                # find transotion of dfa node
                new_list = self.symbol_convert(current_node.nfa_states, symbol).copy()
                new_list = self.lambda_convert(new_list).copy()
                self.sort_nodes_list(new_list)

                # check the new list of nfa nodes created befor
                for i in range(number_dfa_nodes + 1):
                    if new_list == dfa_states[i]:
                        current_node.Nueighbor[symbol] = dfa.States[i]
                        creat_new_node = False
                        break
                if creat_new_node:
                    # creat new node for dfa
                    number_dfa_nodes += 1
                    name = "q" + str(number_dfa_nodes)
                    new_node = NODE(name, dfa.Alphabet)
                    dfa_states += [new_list.copy()]
                    new_node.nfa_states = new_list.copy()
                    dfa.States += [new_node]
                    state_queue.enqueue(new_node)
                    current_node.Nueighbor[symbol] = new_node

                    # check the new node is final state
                    for state in new_node.nfa_states:
                        if state.Final_state:
                            new_node.Final_state = True
                            break

        # number of dfa state
        dfa.Number_State = number_dfa_nodes + 1

Info = []
class App:
    def __init__(self, file_address):
        self.file_address = file_address
        self.NFA = None
        self.DFA = None
        self.Alphabet = None

    def creat_NFA(self):
        # read file
        Lines = open(self.file_address, 'r').readlines()
        self.Alphabet = Lines[1].replace('\n', '').split(',')
        Info = self.Alphabet.copy()
        NFA_Alphabet = self.Alphabet + ["_"]
        self.NFA = Finite_Automata(NFA_Alphabet, int(Lines[0]), 'nfa')
        self.NFA.Start_Variable = self.NFA.States[0]
        # complete nfa"
        for line in range(2, len(Lines)):
            info = Lines[line].split(',')
            origin_index = int(info[0].split('q')[1])
            destination_index = int(info[2].replace('\n', '').split('q')[1])
            self.NFA.States[origin_index].Nueighbor[info[1]] += [self.NFA.States[destination_index]]
            # final states"
            if "*" in info[0]:
                self.NFA.States[origin_index].Final_state = True
            if "*" in info[2]:
                self.NFA.States[destination_index].Final_state = True

    def convert_NFA_to_DFA(self):
        self.DFA = Finite_Automata(self.Alphabet, 0, 'dfa')
        self.NFA.convert_nfa_to_dfa(self.DFA)

    def print_DFA(self):
        # print number of states
        print(self.DFA.Number_State)

        # print Alphabet
        result = ''
        for symbol in self.Alphabet:
            result += symbol + ','
        print(result)

        # print start variable with this transition
        if self.DFA.States[0].Final_state:
            origin_str = '->*' + self.DFA.States[0].Name
        else:
            origin_str = '->' + self.DFA.States[0].Name

        for symbol in self.Alphabet:
            if self.DFA.States[0].Nueighbor[symbol].Final_state:
                dest_str = '*' + self.DFA.States[0].Nueighbor[symbol].Name
            else:
                dest_str = self.DFA.States[0].Nueighbor[symbol].Name

            result = origin_str + ',' + symbol + ',' + dest_str
            print(result)

        # print other state with them transition
        for state_index in range(1, self.DFA.Number_State):
            if self.DFA.States[state_index].Final_state:
                origin_str = '*' + self.DFA.States[state_index].Name
            else:
                origin_str = self.DFA.States[state_index].Name

            for symbol in self.Alphabet:
                if self.DFA.States[state_index].Nueighbor[symbol].Final_state:
                    dest_str = '*' + self.DFA.States[state_index].Nueighbor[symbol].Name
                else:
                    dest_str = self.DFA.States[state_index].Nueighbor[symbol].Name

                result = origin_str + ',' + symbol + ',' + dest_str
                print(result)


App = App("input.txt")
# App = App("test.txt")
App.creat_NFA()
App.convert_NFA_to_DFA()
App.print_DFA()
Info = App.Alphabet
DFA = App.DFA.States
DF = DFA.copy()
print('    a', ' b')
for i in range(len(DFA)):
    print(DFA[i].Name, DFA[i].Nueighbor[Info[0]].Name, DFA[i].Nueighbor[Info[1]].Name)
# for i in range(len(DFA)):
#     print(DFA[i].Name, DFA[i].Nueighbor['a'].Name, DFA[i].Nueighbor['b'].Name)
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
# for tag in Tags:
#     T = False
#     for i in range(len(DFA)):
#         for j in range(len(DFA)):
#             if DFA[i].Tag == tag:
#                 if DFA[i].Tag == DFA[j].Tag:
#                     for symbol in Info:
#                         if DFA[i].Nueighbor[symbol] != DFA[j].Nueighbor[symbol]:
#                             T = True
#                     if T:
#                         print(tag,i,j,DFA[i].Nueighbor[symbol],DFA[j].Nueighbor[symbol])
#                         Tag()
#                         break
print('      a', '  b', '   tag')
print('   ', '---------')
for j in range(len(Tags)):
    for i in range(len(DFA)):
        if DFA[i].Tag == Tags[j]:
            print(DFA[i].Name, '|', DFA[i].Nueighbor[Info[0]], DFA[i].Nueighbor[Info[1]], '|', DFA[i].Tag)
    print('   ', '---------')
#
for i in range(len(St)):
    St[i].Name = 'g' + str(i + 1)
for i in range(len(St)):
    if St[i].Final_state:
        St[i].Name = '*g' + str(i + 1)
# print('      a', '  b', '   tag')
# print('   ', '---------')
# for j in range(len(Tags)):
#     for i in range(len(St)):
#         if St[i].Tag == Tags[j]:
#             print(St[i].Name, '|', St[i].Nueighbor[Info[0]], St[i].Nueighbor[Info[1]], '|', St[i].Tag)
#     print('   ', '---------')
for i in range(len(St)):
    for j in range(len(St)):
        for symbol in Info:
            if St[i].Nueighbor[symbol] == St[j].Tag:
                St[i].Nueighbor[symbol] = St[j].Name
#
# print('      a', '  b')
# print('   ', '-------')
# for j in range(len(Tags)):
#     for i in range(len(St)):
#         if St[i].Tag == Tags[j]:
#             print(St[i].Name, '|', St[i].Nueighbor[Info[0]], St[i].Nueighbor[Info[1]])
#     print('   ', '-------')
Alphabet = ['a', 'b']
print(len(St))
for i in range(len(St)):
    for sy in Info:
        if i == 0 :
            result = '->' + St[i].Name + ',' + sy + ',' + St[i].Nueighbor[sy]
            print(result)
        else:
            result = St[i].Name + ',' + sy + ',' + St[i].Nueighbor[sy]
            print(result)

'''
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


# nodes for dfa and nfa state"
class NODE:
    def __init__(self, name, Alphabet):
        # for dfa node to determine what states on nfa constract nodes of dfa"
        self.nfa_states = []

        self.Nueighbor = dict()
        # creat dict with empty list for transitions"
        for key in Alphabet:
            self.Nueighbor[key] = []
        self.Final_state = False
        self.Name = name
        self.Tag = ''


# class for dfa and nfa"
class Finite_Automata:
    def __init__(self, Alphabet, Number_state, dfa_or_nfa):
        self.Start_Variable = None
        self.Alphabet = Alphabet
        self.Number_State = Number_state

        # list of states of finite automata for acsess them
        self.States = []

        # build states for nfa beacuse know them"
        if dfa_or_nfa == "nfa":
            for number in range(Number_state):
                name = 'q' + str(number)
                new_node = NODE(name, self.Alphabet)
                self.States += [new_node]

    # sort list of nodes for checking new_list==dfa_states[i] base of bubble sort"
    def sort_nodes_list(self, nodes_list):
        n = len(nodes_list)
        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                if nodes_list[j].Name > nodes_list[j + 1].Name:
                    nodes_list[j], nodes_list[j + 1] = nodes_list[j + 1], nodes_list[j]

    # lambda covert for find all lambda transition"
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

    # symbol convert"
    def symbol_convert(self, states, symbol):
        result_list = []
        for state in states:
            for nueighbor in state.Nueighbor[symbol]:
                if nueighbor not in result_list:
                    result_list += [nueighbor]

        return result_list

    def convert_nfa_to_dfa(self, dfa):
        dfa_states = []
        # add start varieble and lambda transition to dfa state"
        dfa_states += [self.lambda_convert([self.Start_Variable])]

        # after build list of nfa states for each dfs node should sort this for compare in futur
        self.sort_nodes_list(dfa_states[0])

        # number of states in dfa
        number_dfa_nodes = 0

        # creat first dfa node"
        name = "q0"
        new_dfa_node = NODE(name, dfa.Alphabet)
        dfa.Start_Variable = new_dfa_node
        new_dfa_node.nfa_states = dfa_states[0]
        # add new state to dfa states"
        dfa.States += [new_dfa_node]
        # end creat"

        # creat queue to check tansition of all of new node in dfa "
        state_queue = queue()
        state_queue.enqueue(new_dfa_node)

        # add one by one dfa states to queue and find this transiton"
        while state_queue.size > 0:
            current_node = state_queue.dequeue()
            for symbol in dfa.Alphabet:

                # bolean for check the new list of nfa nodes created befor
                creat_new_node = True

                # find transotion of dfa node
                new_list = self.symbol_convert(current_node.nfa_states, symbol).copy()
                new_list = self.lambda_convert(new_list).copy()
                self.sort_nodes_list(new_list)

                # check the new list of nfa nodes created befor
                for i in range(number_dfa_nodes + 1):
                    if new_list == dfa_states[i]:
                        current_node.Nueighbor[symbol] = dfa.States[i]
                        creat_new_node = False
                        break
                if creat_new_node:
                    # creat new node for dfa
                    number_dfa_nodes += 1
                    name = "q" + str(number_dfa_nodes)
                    new_node = NODE(name, dfa.Alphabet)
                    dfa_states += [new_list.copy()]
                    new_node.nfa_states = new_list.copy()
                    dfa.States += [new_node]
                    state_queue.enqueue(new_node)
                    current_node.Nueighbor[symbol] = new_node

                    # check the new node is final state
                    for state in new_node.nfa_states:
                        if state.Final_state:
                            new_node.Final_state = True
                            break

        # number of dfa state
        dfa.Number_State = number_dfa_nodes + 1


class App:
    def __init__(self, file_address):
        self.file_address = file_address
        self.NFA = None
        self.DFA = None
        self.Alphabet = None

    def creat_NFA(self):
        # read file
        Lines = open(self.file_address, 'r').readlines()
        self.Alphabet = Lines[1].replace('\n', '').split(',')
        NFA_Alphabet = self.Alphabet + ["_"]
        self.NFA = Finite_Automata(NFA_Alphabet, int(Lines[0]), 'nfa')
        self.NFA.Start_Variable = self.NFA.States[0]
        # complete nfa"
        for line in range(2, len(Lines)):
            info = Lines[line].split(',')
            origin_index = int(info[0].split('q')[1])
            destination_index = int(info[2].replace('\n', '').split('q')[1])
            self.NFA.States[origin_index].Nueighbor[info[1]] += [self.NFA.States[destination_index]]
            # final states"
            if "*" in info[0]:
                self.NFA.States[origin_index].Final_state = True
            if "*" in info[2]:
                self.NFA.States[destination_index].Final_state = True

    def convert_NFA_to_DFA(self):
        self.DFA = Finite_Automata(self.Alphabet, 0, 'dfa')
        self.NFA.convert_nfa_to_dfa(self.DFA)

    def print_DFA(self):
        # print number of states
        print(self.DFA.Number_State)

        # print Alphabet
        result = ''
        for symbol in self.Alphabet:
            result += symbol + ','
        print(result)

        # print start variable with this transition
        if self.DFA.States[0].Final_state:
            origin_str = '->*' + self.DFA.States[0].Name
        else:
            origin_str = '->' + self.DFA.States[0].Name

        for symbol in self.Alphabet:
            if self.DFA.States[0].Nueighbor[symbol].Final_state:
                dest_str = '*' + self.DFA.States[0].Nueighbor[symbol].Name
            else:
                dest_str = self.DFA.States[0].Nueighbor[symbol].Name

            result = origin_str + ',' + symbol + ',' + dest_str
            print(result)

        # print other state with them transition
        for state_index in range(1, self.DFA.Number_State):
            if self.DFA.States[state_index].Final_state:
                origin_str = '*' + self.DFA.States[state_index].Name
            else:
                origin_str = self.DFA.States[state_index].Name

            for symbol in self.Alphabet:
                if self.DFA.States[state_index].Nueighbor[symbol].Final_state:
                    dest_str = '*' + self.DFA.States[state_index].Nueighbor[symbol].Name
                else:
                    dest_str = self.DFA.States[state_index].Nueighbor[symbol].Name

                result = origin_str + ',' + symbol + ',' + dest_str
                print(result)


App = App("input.txt")
# App = App("test.txt")
App.creat_NFA()
App.convert_NFA_to_DFA()
App.print_DFA()

DFA = App.DFA.States
DF = DFA.copy()
print('    a', ' b')
for i in range(len(DFA)):
    print(DFA[i].Name, DFA[i].Nueighbor['a'].Name, DFA[i].Nueighbor['b'].Name)

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
    N = []
    for i in range(S):
        for j in range(i,S):
            if i != j:
                if j < S:
                    if States[i].Tag == States[j].Tag:
                        if States[i].Nueighbor['a'] == States[j].Nueighbor['a'] and States[i].Nueighbor['b'] == \
                                States[j].Nueighbor['b']:
                            K.append(States[i].Tag)
                            N.append(States[j].Nueighbor['a'].Tag)
                            N.append(States[j].Nueighbor['b'].Tag)
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
    for i in range(ss):
        if i >= ss:
            i -= 1
        for j in range(len(SS)):
            if States[i].Tag == K[0]:
                if States[i].Nueighbor['a'].Name == SS[j].Name and States[i].Nueighbor['b'].Name == \
                        SS[j].Nueighbor['b'].Name:
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
        DFA[i].Nueighbor['a'] = DFA[i].Nueighbor['a'].Tag
        DFA[i].Nueighbor['b'] = DFA[i].Nueighbor['b'].Tag


Tag()
# tag()
for tag in Tags:
    for i in range(len(DFA)):
        for j in range(len(DFA)):
            if DFA[i].Tag == tag:
                if DFA[i].Tag == DFA[j].Tag:
                    if DFA[i].Nueighbor['a'] != DFA[j].Nueighbor['a'] or DFA[i].Nueighbor['b'] != DFA[j].Nueighbor['b']:
                        print('1')
                        Tag()
print('      a', '  b', '   tag')
print('   ', '---------')
for j in range(len(Tags)):
    for i in range(len(DFA)):
        if DFA[i].Tag == Tags[j]:
            print(DFA[i].Name, '|', DFA[i].Nueighbor['a'], DFA[i].Nueighbor['b'], '|', DFA[i].Tag)
    print('   ', '---------')
#
for i in range(len(St)):
    St[i].Name = 'g' + str(i + 1)
for i in range(len(St)):
    if St[i].Final_state:
        St[i].Name = '*g' + str(i + 1)
print('      a', '  b', '   tag')
print('   ', '---------')
for j in range(len(Tags)):
    for i in range(len(St)):
        if St[i].Tag == Tags[j]:
            print(St[i].Name, '|', St[i].Nueighbor['a'], St[i].Nueighbor['b'], '|', St[i].Tag)
    print('   ', '---------')
for i in range(len(St)):
    for j in range(len(St)):
        if St[i].Nueighbor['a'] == St[j].Tag:
            St[i].Nueighbor['a'] = St[j].Name
        if St[i].Nueighbor['b'] == St[j].Tag:
            St[i].Nueighbor['b'] = St[j].Name
#
print('      a', '  b')
print('   ', '-------')
for j in range(len(Tags)):
    for i in range(len(St)):
        if St[i].Tag == Tags[j]:
            print(St[i].Name, '|', St[i].Nueighbor['a'], St[i].Nueighbor['b'])
    print('   ', '-------')
Alphabet = ['a', 'b']
print(len(St))
for i in range(len(St)):
    for sy in Alphabet:
        if i == 0 :
            result = '->' + St[i].Name + ',' + sy + ',' + St[i].Nueighbor[sy]
            print(result)
        else:
            result = St[i].Name + ',' + sy + ',' + St[i].Nueighbor[sy]
            print(result)
            
            
'''