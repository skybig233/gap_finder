import argparse
from myclass import myhit
from typing import List
parser=argparse.ArgumentParser()
parser.add_argument('-blastn','--inputblastn')
parser.add_argument('-fasta','--inputfasta')
parser.add_argument('-o','--outputfasta',default='tagged_fasta')
parser.add_argument('-l','--lengthlimit',type=int,default=10)

args=parser.parse_args()
inputblastn=args.inputblastn
inputfasta=args.inputfasta
outputfasta=args.outputfasta
lengthlimit=args.lengthlimit

d={}
hits_message_list=[]

inputblastn=r'C:\Users\jiangzhesheng\Desktop\blastn.result'
inputfasta='Mat_pshap2.mother.fa'

def process_hit_list(hits_message_list:List, hits_num:int):
    if(len(hits_message_list)!=hits_num):
        print('error')
        return

    # 对于单个hit的直接加入d
    if (hits_num == 1):
        hit=myhit.Hit(hits_message_list[0])
        d[hit.qseqid] = hit.sseqid
        if (hit.error > lengthlimit):
            print(hit.sseqid + ' may have error ' + str(hit.error))
        return

    cnt=0
    #获取hit信息
    hit_list=myhit.get_hit_list(hits_message_list)
    for hit in hit_list:
        if(hit.error<=lengthlimit):
            cnt+=1
    if(cnt<2):
        d[hit_list[0].qseqid]=hit_list[0].sseqid
    else:
        print('scaffold:'+hit_list[0].qseqid+' has too many blastn result:')
        for i in hit_list:
            myhit.Hit.print(i)

with open(inputblastn,mode='r')as inputblastnfile:
    for line in inputblastnfile:
        if ('hits' in line):
            hits_num = int(line.split()[1])
        if (line[0]!='#'):
            #如果这行是hit，就可以得到各个field值
            hits_message_list.append(line)
        else:
            if(hits_message_list!=[]):
                process_hit_list(hits_message_list, hits_num)
                hits_message_list=[]


with open(inputfasta,mode='r') as inputfastafile,open(outputfasta,mode='w')as outputfastafile:
    for line in inputfastafile:
        if('>'in line):
            scaffold_id=line.strip()[1:]
            if(scaffold_id in d):
                line_info=line.strip()+'\t'+d[scaffold_id]+'\n'
                outputfastafile.write(line_info)
            else:
                line_info = line.strip() + '\t' + 'nochr' + '\n'
                outputfastafile.write(line_info)
        else:
            outputfastafile.write(line)