#gapfinder
gap区序列分析
##概要
###flanking region提取及比对
从supernova组装结果中提取gap区域前后的flanking region，再将其用minimap2软件比对到参考基因组上，得到flanking region的位置

ref_split.py将ref的每条scaffold（chromosome）拆成多个文件

gapsplit.py将组装结果中gap前后的flanking region提取出来
###比对结果清洗
paf_washer.py将得到的paf文件清洗，保留best match
###gap区域序列提取及分析
gap_locater.py根据paf清洗的结果，根据上下两条paf信息提取gap序列，使用rmsk数据库分析gap类型

graph_plotter.py根据gap类型统计信息画出饼图