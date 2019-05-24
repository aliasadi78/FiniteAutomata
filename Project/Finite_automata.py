from NODE import *
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
#class for dfa and nfa"
class Finite_Automata:
    def __init__(self,Alphabet,Number_state,dfa_or_nfa):
        self.Start_Variable = None
        self.Alphabet = Alphabet
        self.Number_State = Number_state
        
        #list of states of finite automata for acsess them
        self.States=[]

        
        #build states for nfa beacuse know them"
        if dfa_or_nfa=="nfa":
            for number in range(Number_state):
                name='q'+str(number)
                new_node=NODE(name,self.Alphabet)
                self.States+=[new_node]


                
    #sort list of nodes for checking new_list==dfa_states[i] base of bubble sort"
    def sort_nodes_list(self,nodes_list):
        n = len(nodes_list)
        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n-i-1):
                if nodes_list[j].Name > nodes_list[j+1].Name :
                    nodes_list[j], nodes_list[j+1] = nodes_list[j+1], nodes_list[j]



                    
    #lambda covert for find all lambda transition in states in list"
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

    
    #symbol convert"
    def symbol_convert(self,states,symbol):
        result_list=[]
        for state in states:
            for nueighbor in state.Nueighbor[symbol]:
                if nueighbor not in result_list:
                    result_list+=[nueighbor]

        return result_list
    

    def convert_nfa_to_dfa(self,dfa):
        dfa_states=[]
        #add start varieble and lambda transition to dfa state"
        dfa_states+=[self.lambda_convert([self.Start_Variable])]
        
        #after build list of nfa states for each dfs node should sort this for compare in futur
        self.sort_nodes_list(dfa_states[0])

        #number of states in dfa
        number_dfa_nodes=0
        
        #creat first dfa node"
        name="q0"
        new_dfa_node=NODE(name,dfa.Alphabet)
        dfa.Start_Variable=new_dfa_node
        new_dfa_node.nfa_states=dfa_states[0]
        #add new state to dfa states"
        dfa.States+=[new_dfa_node]
        #end creat"

        #creat queue to check tansition of all of new node in dfa "
        state_queue=queue()
        state_queue.enqueue(new_dfa_node)
        
        #add one by one dfa states to queue and find this transiton"
        while state_queue.size > 0:
            current_node=state_queue.dequeue()
            for symbol in dfa.Alphabet:
                
                #bolean for check the new list of nfa nodes created befor
                creat_new_node=True

                #find transotion of dfa node
                new_list=self.symbol_convert(current_node.nfa_states,symbol).copy()
                new_list=self.lambda_convert(new_list).copy()
                self.sort_nodes_list(new_list)

                #check the new list of nfa nodes created befor
                for i in range(number_dfa_nodes+1):
                    if new_list==dfa_states[i]:
                        current_node.Nueighbor[symbol]=dfa.States[i]
                        creat_new_node=False
                        break
                if creat_new_node:
                    #creat new node for dfa 
                    number_dfa_nodes+=1
                    name="q"+str(number_dfa_nodes)
                    new_node=NODE(name,dfa.Alphabet)
                    dfa_states+=[new_list.copy()]
                    new_node.nfa_states=new_list.copy()
                    dfa.States+=[new_node]
                    state_queue.enqueue(new_node)
                    current_node.Nueighbor[symbol]=new_node

                    #check the new node is final state 
                    for state in new_node.nfa_states:
                        if state.Final_state:
                            new_node.Final_state=True
                            break

        
        #number of dfa state
        dfa.Number_State=number_dfa_nodes+1
