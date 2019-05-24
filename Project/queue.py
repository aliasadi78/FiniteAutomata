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
