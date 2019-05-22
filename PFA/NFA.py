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
        
"nodes for dfa and nfa state"
class NODE:
    def __init__(self,name,Alphabet):
        "for dfa node"
        self.nfa_states=[]
        "end dfa athribute"
        self.Nueighbor=dict()
        for key in Alphabet:
            self.Nueighbor[key]=[]
        self.Final_state=bool()
        self.Name=name
"class for dfa and nfa"
class Finite_Automata:
    def __init__(self,Alphabet,Number_state,dfa_or_nfa):
        self.Start_Variable = None
        self.Alphabet = Alphabet
        self.Number_State = Number_state
        self.States=[]
        "build states for nfa and add to self.states"
        if dfa_or_nfa=="nfa":
            for number in range(Number_state):
                name='q'+str(number)
                new_node=NODE(name,self.Alphabet)
                self.States+=[new_node]

    "lambda covert for convert nfa to dfa"
    def lambda_convert(self,states):
        state_queue=queue()
        for state in states:
            state_queue.enqueue(state)
        while state_queue.size>0:
            current_state=state_queue.dequeue()
            for state in current_state.Nueighbor['_']:
                if state not in states:
                    state_queue.enqueue(state)
                    states+=[state]
                    
            
        return states.copy()

    
    "symbol convert"
    def symbol_convert(self,states,symbol):
        result_list=[]
        for state in states:
            for nueighbor in state.Nueighbor[symbol]:
                if nueighbor not in result_list:
                    result_list+=[nueighbor]

        return result_list

    def convert_nfa_to_dfa(self,dfa):
        dfa_states=[]
        dfa_states+=[self.lambda_convert([self.Start_Variable])]
        print(dfa_states)
        "creat dfa node"
        number_dfa_nodes=0
        name="g0"
        new_dfa_node=NODE(name,dfa.Alphabet)
        dfa.Start_Variable=new_dfa_node
        new_dfa_node.nfa_states=dfa_states[0]
        "add new state to dfa states"
        dfa.States+=[new_dfa_node]
        "end creat"
        state_queue=queue()
        state_queue.enqueue(new_dfa_node)
        "add one by one dfa states to queue and find this transiton"
        j=0
        while state_queue.size > 0:
            current_node=state_queue.dequeue()
            for symbol in dfa.Alphabet:
                j+=1
                creat_new_node=True
                for state in current_node.nfa_states:
                    print(state.Name)
                new_list=self.symbol_convert(current_node.nfa_states,symbol).copy()
                new_list=self.lambda_convert(new_list).copy()
                new_list.sort()
                for i in range(number_dfa_nodes+1):
                    if new_list==dfa_states[i]:
                        print("*****************"+str(j))
                        current_node.Nueighbor[symbol]=dfa.States[i]
                        creat_new_node=False
                        break
                if creat_new_node:
                    print(j)
                    number_dfa_nodes+=1
                    name="g"+str(number_dfa_nodes)
                    "print(number_dfa_nodes)"
                    new_node=NODE(name,dfa.Alphabet)
                    dfa_states+=[new_list.copy()]
                    new_node.nfa_states=new_list.copy()
                    dfa.States+=[new_node]
                    state_queue.enqueue(new_node)
                    current_node.Nueighbor[symbol]=new_node
                    
                



Lines=open("input.txt",'r').readlines()
DFA_Alphabet=Lines[1].replace('\n','').split(',')
NFA_Alphabet=DFA_Alphabet+["_"]
NFA=Finite_Automata(NFA_Alphabet,int(Lines[0]),'nfa')
DFA=Finite_Automata(DFA_Alphabet,0,'dfa')
"complete nfa"
for line in range(2,len(Lines)):
    info=Lines[line].split(',')
    origin_index=int(info[0].split('q')[1])
    destination_index=int(info[2].replace('\n','').split('q')[1])
    NFA.States[origin_index].Nueighbor[info[1]]+=[NFA.States[destination_index]]

"convert nfa to dfa"
print(NFA.States)
NFA.Start_Variable=NFA.States[0]
NFA.convert_nfa_to_dfa(DFA)


