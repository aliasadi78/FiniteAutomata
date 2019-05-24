#nodes for dfa and nfa state"
class NODE:
    def __init__(self,name,Alphabet):
        #for dfa node to determine what states on nfa constract nodes of dfa"
        self.nfa_states=[]
        
        self.Nueighbor=dict()
        #creat dict with empty list for transitions"
        for key in Alphabet:
            self.Nueighbor[key]=[]
        self.Final_state=False
        self.Name=name
        self.Tag=''
