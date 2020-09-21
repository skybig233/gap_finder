LINE_COUNT=50
class Scaffold:
    def __init__(self,fastapath:str) -> None:
        self.fastapath=fastapath
    def getseq(self,start:int,end:int)->str:
        #取得的序列包括start和end，scaffold从1开始计数
        with open(self.fastapath,mode='r') as fastafile:
            fastafile.readline()
            blank_num=(start-1)//LINE_COUNT
            rest=LINE_COUNT-(start-1)%LINE_COUNT
            fastafile.read(start-1+blank_num)
            blank_num=((end-start-rest)//LINE_COUNT)+1 if end-start-rest>=0 else 0
            s=fastafile.read(end-start+1+blank_num)
            return s

if __name__ == '__main__':
    print('testing scaffold class')
    test=Scaffold(r'C:\Users\jiangzhesheng\PycharmProjects\gapfinder\hg38\chr2.fa')
    print(test.getseq(11229,46269))