from typing import List
def process_hit_message(hit_message:str):
    line_list = hit_message.split()
    qseqid = line_list[0].split('.')[0]
    qlength = int(line_list[0].split('.')[1][6:])
    sseqid = line_list[1]
    alignment_length = int(line_list[2])
    error = abs(alignment_length - qlength)
    return qseqid,qlength,sseqid,alignment_length,error

class Hit:
    def __init__(self,hit_message):
        qseqid,qlength,sseqid,alignment_length,error=process_hit_message(hit_message)
        self.qseqid=qseqid
        self.qlength=qlength
        self.sseqid=sseqid
        self.alignment_length=alignment_length
        self.error=error
    def print(self):
        print(self.__dict__)
def get_hit_list(hit_message_list:[str])->[Hit]:
    ans=[]
    for i in hit_message_list:
        ans.append(Hit(i))
    return ans