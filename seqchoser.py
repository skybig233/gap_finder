import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfasta',\
                    help='input fasta file path')
parser.add_argument('-o', '--choose_sequence', default='choose_seq.result')
parser.add_argument('-l','--limit',type=int,default=1,\
                    help='if the seq length lower than limit it won\'t add into result')
parser.add_argument('-n','--number',type=int,default=2)

args = parser.parse_args()

inputfasta = args.inputfasta
output = args.choose_sequence
limit=args.limit
number=args.number


#windows debug
inputfasta='gapinform'

with open(inputfasta,mode='r') as inputfastafile, open(output,mode='w') as outputfile:
    cnt=1
    pre_scaffold_info='>>'
    for line in inputfastafile:
        if('>' in line):#if this line is info line
            scaffold_info=line
            if(pre_scaffold_info[1]!=scaffold_info[1]):
                cnt=1
            pre_scaffold_info=scaffold_info
        else:#if this line is seq line
            if(cnt<=number and len(line)>limit):
                outputfile.write(scaffold_info)
                outputfile.write(line)
                cnt+=1