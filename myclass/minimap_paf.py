import logging
QID=0
QLEN=1
QSTART=2
QEND=3
ORIENT=4
TID=5
TLEN=6
TSTART=7
TEND=8
MAPQ=11
class Paf:
    def __init__(self,paf_line:str=''):
        if paf_line=='':
            self.tid,self.qid,self.message= '', '', ''
            self.orient='+'
            self.scaffold_id,self.ref_id= 0, 0
        else:#通过paf_line构造paf
            self.message = paf_line
            paf_line=paf_line.split()
            self.qid = paf_line[QID]
            self.qlen = int(paf_line[QLEN])
            self.qstart = int(paf_line[QSTART])
            self.qend = int(paf_line[QEND])
            self.orient=paf_line[ORIENT]
            self.tid = paf_line[TID]
            self.tstart = int(paf_line[TSTART])
            self.tend = int(paf_line[TEND])
            self.mapq=int(paf_line[MAPQ])
            self.scaffold_id=int(self.qid.split('.')[0])
            self.ref_id=int(self.qid.split('.')[1][3:])
    def relocate(self):
        if self.orient=='-':
            relocate_end=self.tend + (self.qstart - 1)
            relocate_start=self.tstart-(self.qlen - self.qend)
        elif self.orient=='+':
            relocate_start = self.tstart - (self.qstart - 1)
            relocate_end = self.tend+(self.qlen - self.qend)
        else:
            logging.warning(self.qid+'has no orient')
        return relocate_start, relocate_end
    def __str__(self):
        return self.message