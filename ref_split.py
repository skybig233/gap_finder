import sys
import argparse
import os
import logging

SCAFFOLD_HEADER='>'

def ref_split(filepath:str,outputdir:str):
    with open(filepath,mode='r') as fastafile:
        os.chdir(outputdir)
        for line in fastafile:
            if(SCAFFOLD_HEADER in line):
                scaffold_id=line[line.find(SCAFFOLD_HEADER)+1:].strip()
                nextflag=True
            else:nextflag=False
            if(nextflag==True):
                try:
                    outfasta.close()
                except UnboundLocalError: pass
                logging.info(scaffold_id+' is processing')
                outfasta=open(scaffold_id+'.fa',mode='w')
            outfasta.write(line)

def main(argv):
    #read the arguments
    parser=argparse.ArgumentParser(description='Split whole ref fasta into single ref fasta')
    parser.add_argument('-i','--input_ref_fasta',required=True)
    parser.add_argument('-o','--outputdir',default='hg38')
    args=parser.parse_args(argv[1:])
    outputdir=args.outputdir
    input_ref_fasta = args.input_ref_fasta

    # create the output direction
    try:
        os.mkdir(outputdir)
    except FileExistsError as e:
        logging.warning(outputdir + ' is exist, files in it may be overwritten')

    #process
    ref_split(os.path.abspath(input_ref_fasta),os.path.abspath(outputdir))
if __name__ == '__main__':
    main(sys.argv)