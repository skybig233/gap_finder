# -*- coding: utf-8 -*-
# @Time : 2020/9/3 11:37
# @Author : Jiangzhesheng
# @File : paf_washer.py
# @Software: PyCharm
import argparse
import sys
import os
import logging
from myclass import minimap_paf
def multialign_chooser(list:[minimap_paf.Paf])->minimap_paf.Paf:
    if len(list)==0:
        return minimap_paf.Paf('')
    elif len(list)==1:
        return list[0]
    else:
        return list[0]

def reverse_adjust(list:[minimap_paf.Paf])->[]:
    ans=[]
    reverse_list=[]
    missing_cnt=0
    pre_paf=minimap_paf.Paf('')
    for paf in list:
        if pre_paf.scaffold_id==paf.scaffold_id and paf.ref_id-pre_paf.ref_id>1:
            logging.warning(' missing ref between '+pre_paf.qid + 'and '+paf.qid)
            missing_cnt+=paf.ref_id-pre_paf.ref_id
        if pre_paf.orient=='-' and paf.orient=='+' and reverse_list!=[]:
            ans=ans+reverse_list
            reverse_list=[]
        if paf.orient=='+':
            ans.append(str(paf))
        elif paf.orient=='-':
            reverse_list.insert(0,str(paf))
        pre_paf=paf
    ans = ans + reverse_list
    print(missing_cnt)
    return ans

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',required=True)
    parser.add_argument('-o', '--outputdir',default='paf_washer')
    args = parser.parse_args(argv[1:])
    input = os.path.abspath(args.input)
    outputdir = os.path.abspath(args.outputdir)
    try:
        os.mkdir(outputdir)
    except FileExistsError as e:
        logging.warning(outputdir + ' is exist, files in it may be overwritten')
    with open(input,mode='r') as inputfile,open(os.path.join(outputdir,'paf_washer.result'),mode='w') as outputfile:
        pre_paf=minimap_paf.Paf('')
        multipaf_list = []
        write_list=[]
        reverse_list=[]
        for line in inputfile:
            paf=minimap_paf.Paf(line)
            if paf.qid==pre_paf.qid:
                multipaf_list.append(paf)
            else:
                choosed_paf=multialign_chooser(multipaf_list)
                write_list.append(choosed_paf)
                multipaf_list = []
                multipaf_list.append(paf)
            pre_paf=paf
        choosed_paf = multialign_chooser(multipaf_list)
        write_list.append(choosed_paf)
        write_list=reverse_adjust(write_list)
        outputfile.writelines(write_list)
if __name__ == '__main__':
    main(sys.argv)