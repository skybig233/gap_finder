import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfasta',required=True)
parser.add_argument('-o', '--outputgapinformation', default='gapsplit.result')
args = parser.parse_args()

inputfasta = args.inputfasta
output = args.outputgapinformation

# inputfasta='test'
# inputfasta = r'C:\Users\jiangzhesheng\Desktop\Mat_pshap2.mother.fa'
# output = 'gapinform'

s = ''
debugflag = False
with open(inputfasta, mode='r')as inputfile, open(output, mode='w')as outputfile:
    for line in inputfile:
        if ('>' in line):
            #to fuck pycharm
            debugflag = True
            debugflag = True
            #去掉那些完全没有N的scaffold，也就是组装好的没有gap的scaffold
            if (s != '' and Nflag == True):
                outputfile.write(scaffolf_info + str(count) + '.length:' + str(len(s)) + '\n')
                outputfile.write(s + '\n')
            s = ''
            count = 0
            scaffolf_info = line[:-1] + '.contig'
            Nflag = False
        else:
            line = line.strip()
            if ('N' in line):
                Nflag = True
                for char in line:
                    if (char == 'N'):
                        if (s != ''):
                            outputfile.write(scaffolf_info + str(count) + '.length:' + str(len(s)) + '\n')
                            outputfile.write(s + '\n')
                            s = ''
                            count += 1
                    else:
                        s = s + char
            else:
                s = s + line
    if (s != ''):
        outputfile.write(scaffolf_info + str(count) + '.length:' + str(len(s)) + '\n')
        outputfile.write(s + '\n')
