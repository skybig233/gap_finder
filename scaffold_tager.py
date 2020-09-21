import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfasta',required=True,\
                    help='input fasta file path')
parser.add_argument('-o', '--output', default='scaffold_tager.result')
parser.add_argument('-l','--limit',type=int,default=500,\
                    help='get part of the seq of a scaffold'
                         'DEFAULT = 500')

args = parser.parse_args()

inputfasta = args.inputfasta
output = args.output
limit=args.limit

# inputfasta='Mat_pshap2.mother.fa'


findflag=False
write_list=[]
cnt=0
mincnt=limit
with open(inputfasta,mode='r')as inputfastafile,open(output,mode='w')as outputfile:
    for line in inputfastafile:
        if(line[0]=='>'):
            try:
                write_list[0] += '.length' + str(cnt) + '\n'
                if(cnt<mincnt):
                    mincnt=cnt
            except IndexError: pass
            outputfile.writelines(write_list)
            scaffold_info=line.split()[0].strip()
            write_list=[scaffold_info]
            cnt=0
            s=''
            findflag=False
        else:
            if (findflag == True):
                continue
            if('N' in line):
                tmp=line[:line.find('N')]
                cnt+=len(tmp)
                write_list.append(tmp+'\n')
                findflag = True
            else:
                if(cnt<limit and findflag==False):
                    write_list.append(line)
                    cnt+=len(line)-1
                else:
                    findflag=True

    try:
        write_list[0] += '.length' + str(cnt) + '\n'
        if (cnt < mincnt):
            mincnt = cnt
    except IndexError:
        pass
    outputfile.writelines(write_list)

print('mincnt:'+str(mincnt))