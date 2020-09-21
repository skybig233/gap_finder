import os
from myclass import scaffold
import logging
CHR_ID=0
START=1
END=2
REPEAT_TYPE=3
sine_d,line_d,cgi_d,ltr_d={},{},{},{}

def readtxt(path:str):
    with open(path,mode='r') as file:
        d={str:[(int,int,str)]}
        for line in file:
            line_list=line.split()
            if line_list[CHR_ID] in d:
                d[line_list[CHR_ID]].append((int(line_list[START]),int(line_list[END]),line_list[REPEAT_TYPE]))
            else:
                d[line_list[CHR_ID]]=[(int(line_list[START]),int(line_list[END]),line_list[REPEAT_TYPE])]
        for i in d:
            #去除repeat database中的重复元素（尤其是TRF），并根据start排序
            d[i]=list(set(d[i]))
            d[i].sort()
        return d
sine_d=readtxt('C:\\Users\\jiangzhesheng\\PycharmProjects\\gapfinder\\gaptype_ref\\Alu.txt')
line_d=readtxt('C:\\Users\\jiangzhesheng\\PycharmProjects\\gapfinder\\gaptype_ref\\LINE.txt')
cgi_d=readtxt('C:\\Users\\jiangzhesheng\\PycharmProjects\\gapfinder\\gaptype_ref\\hg19_CpGIsland.txt')
ltr_d=readtxt('C:\\Users\\jiangzhesheng\\PycharmProjects\\gapfinder\\gaptype_ref\\LTR.txt')
REPEAT_TYPE=1
START=3
END=4
trf_d=readtxt('C:\\Users\\jiangzhesheng\\PycharmProjects\\gapfinder\\gaptype_ref\\Human_Full_Genome_tandem_repeats.gff')
logging.info('repeat database finished')
class Gap:
    def __init__(self, gapid:int, gapstart:int, gapend:int, gap_on_scaffold_id:str,gap_preseq:str='',gap_postseq:str='') -> None:
        self.id=gapid
        self.start=gapstart
        self.end=gapend
        self.scaffold_id=gap_on_scaffold_id
        self.length=self.end-self.start+1
        self.preseq=gap_preseq
        self.postseq=gap_postseq
        self.type_list=self.gettype()
    def getseq(self,refdir:str)->str:
        filename= self.scaffold_id + '.fa'
        fastapath=os.path.join(refdir,filename)
        tmp=scaffold.Scaffold(fastapath=fastapath)
        return tmp.getseq(self.start,self.end)
    def gettype(self)->[]:
        type_list=[]
        for dict in [sine_d,line_d,cgi_d,ltr_d,trf_d]:
            if self.scaffold_id not in dict:
                continue
            for start,end,repeat_type in dict[self.scaffold_id]:
                if end<self.start:
                   #                     s.s      s.e
                   #                      |________|
                   #    s___e  s_____e
                    continue
                elif start>self.end:
                    #                     s.s      s.e
                    #                      |________|
                    #                                    s________e
                    break
                elif self.end>=end>self.start and start<self.start:
                    #                     s.s      s.e
                    #                      |________|
                    #                  s______e
                    type_list.append((self.start,end,repeat_type))
                elif self.end>=end>self.start and start>=self.start:
                    #                     s.s      s.e
                    #                      |________|
                    #                         s__e
                    type_list.append((start,end,repeat_type))
                elif self.start>=start and self.end<=end:
                    #                     s.s      s.e
                    #                      |________|
                    #                  s________________e
                    type_list.append((self.start,self.end,repeat_type))
                elif self.end>=start>=self.start and end>self.end   :
                    #                     s.s      s.e
                    #                      |________|
                    #                            s________e
                    type_list.append((start,self.end,repeat_type))
        return type_list
    def __str__(self) -> str:
        ans=[SCAFFOLD_HEADER+'gap'+str(self.id),
             self.scaffold_id,
             str(self.length),
             str(self.start),
             str(self.end),
             str(self.type_list),
             self.preseq,
             self.postseq]
        return '\t'.join(ans)

if __name__ == '__main__':
    a=Gap(0,67161,68334,'chr2')
    print(a.gettype())