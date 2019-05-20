class NODE:
    def __init__(self,name,Alphabet):
        self.Nueighbor=dict()
        for key in Alphabet:
            self.Nueighbor[key]=[]
        self.Final_state=bool()
        self.Name=name

class NFA:
    def __init__(self,Alphabet,Number_state):
        self.Start_Variable = None
        self.Alphabet = Alphabet
        self.Number_State = Number_state
        self.States=[]
        for number in range(Number_state):
            name='q'+str(number)
            new_node=NODE(name,self.Alphabet)
            self.States+=[new_node]


