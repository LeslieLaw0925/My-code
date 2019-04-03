import random as rand

class Content:
    content_num=10

    def __init__(self,id):
        self.content_id=id

        self.input_block_num = rand.randint(50,100) # block的数目

        self.block_size=rand.randint(1,5)*1024*8# KB 每个block的大小

        self.input_size=self.input_block_num*self.block_size
