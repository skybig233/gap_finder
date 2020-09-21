import sys
import argparse
import os
import logging
from myclass import minimap_paf
from myclass import gap
def gap_locat(filepath:str,ref_split_result_path:str,outputdir:str):
    gap_count={}
    base_count={}
    with open(filepath,mode='r') as paffile,\
            open(os.path.join(outputdir,'gap_locater.result'),mode='w')as outputfile,\
            open(os.path.join(outputdir,'gap_base.count'),mode='w')as countfile,\
            open(os.path.join(outputdir,'gap_locater.totallog'),mode='w')as totallog:
        pre_paf=minimap_paf.Paf(paffile.readline())
        pre_start,pre_end=pre_paf.relocate()
        i=0
        overlap_cnt,different_chr_cnt=0,0
        for line in paffile:
            paf=minimap_paf.Paf(line)
            paf_relocate_start,paf_relocate_end=paf.relocate()
            if pre_paf.scaffold_id!=paf.scaffold_id:
                logging.info('processing scaffold'+str(paf.scaffold_id))
                pre_paf=paf
                pre_end = paf_relocate_end
                continue
            if paf.tid!=pre_paf.tid:
                different_chr_cnt+=1
                logging.warning('different chr'+pre_paf.qid+'on'+pre_paf.tid+'and'+paf.qid+'on'+paf.tid)
                pre_paf=paf
                pre_end = paf_relocate_end
                continue
            if pre_end>=paf_relocate_start:
                #这里overlap是前后flanking region完全重叠，完全没有gap序列，即：
                #在组装结果中：
                #   flanking region 1       gap       flanking region 2
                #————————————————————————NNNNNNNNNN
                #                                  ————————————————————————
                # 但是在ref（即参考答案）中：
                #   flanking region 1
                #——————————————————————
                #               ——————————————————————
                #                  flanking region 2
                #解决方案：gap的start和end重新定位到flanking region左右一定长度（1kbp）的地方再去对这个区域进行repeattype分析
                #TODO 添加overlaped contig的处理
                overlap_cnt+=1
                logging.warning('overlaped contig'+pre_paf.qid+paf.qid)
                pre_paf=paf
                pre_end = paf_relocate_end
                continue
            i+=1
            tmp_gap=gap.Gap(gapid=i, \
                            gapstart=pre_end+1, \
                            gapend=paf_relocate_start-1, \
                            gap_on_scaffold_id=paf.tid,\
                            gap_preseq=pre_paf.qid,\
                            gap_postseq=paf.qid)
            if tmp_gap.type_list==[]:
                #个人认为notype有两种情况，type_list==[],即全空
                #           notype
                #    |——————————————————|
                #这里的notype只考虑了type_list里完全为空的情况，对于以下情况未考虑
                #      SINE     notype     LINE     notype      TRF
                #    |—————|—————————————|————-|——————————————|—————|
                #TODO 添加notype的第二种情况
                gap_count['notype']=gap_count.get('notype',0)+1
                base_count['notype']=base_count.get('notype',0)+(tmp_gap.end-tmp_gap.start)
            for type in tmp_gap.type_list:
                gap_count[type[2]]=gap_count.get(type[2],0)+1
                base_count[type[2]]=base_count.get(type[2],0)+(type[1]-type[0])
            outputfile.write(str(tmp_gap)+'\n')
            # outputfile.write(tmp_gap.getseq(ref_split_result_path)+'\n')
            pre_paf = paf
            pre_end = paf_relocate_end
            # print(tmp_gap)
            # print(tmp_gap.getseq(ref_split_result_path))
            #

        totallog.write('overlap_cnt:'+str(overlap_cnt)+'\n')
        totallog.write('different_chr_cnt:'+str(different_chr_cnt)+'\n')
        totallog.write('processed gap:'+str(i)+'\n')
        print('overlap_cnt:',overlap_cnt)
        print('different_chr_cnt:',different_chr_cnt)
        print('processed gap:',i)

        countfile.write('gap_count:' + str(gap_count)+'\n')
        countfile.write('base_count:' + str(base_count))
        for i in gap_count:
            print(i,'\t',gap_count[i])
        print('base_count:')
        for i in base_count:
            print(i ,'\t' , base_count[i])

def main(argv):
    #read the arguments
    parser=argparse.ArgumentParser(description='Split whole ref fasta into single ref fasta')
    parser.add_argument('-i','--input_paf',required=True)
    parser.add_argument('-r','--ref_split_result_path',required=True)
    parser.add_argument('-o','--outputdir',default='gap_locater_result')
    args=parser.parse_args(argv[1:])

    outputdir=args.outputdir
    input_paf = args.input_paf
    ref_split_result_path=args.ref_split_result_path

    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # create the output direction
    try:
        os.mkdir(outputdir)
    except FileExistsError as e:
        logging.warning(outputdir + ' is exist, files in it may be overwritten')

    #process
    gap_locat(os.path.abspath(input_paf),os.path.abspath(ref_split_result_path),os.path.abspath(outputdir))
if __name__ == '__main__':
    main(sys.argv)