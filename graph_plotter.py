# -*- coding: utf-8 -*-
# @Time : 2020/9/14 9:04
# @Author : Jiangzhesheng
# @File : graph_plotter.py
# @Software: PyCharm
import argparse
import sys
import os
import matplotlib.pyplot as plt

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--outputdir')
    args = parser.parse_args(argv[1:])
    input = args.input
    outputdir = args.outputdir
    with open(os.path.abspath(input),mode='r') as inputfile:
        for line in inputfile:
            title=line[:line.find(':')]
            dict=eval(line[line.find(':')+1:])
            labels=list(dict.keys())
            data=list(dict.values())
            plt.pie(x=data,labels=labels,autopct='%.1f%%')
            plt.title(title)
            plt.savefig(os.path.join(os.path.abspath(outputdir),title+'.jpg'))
            plt.show()

if __name__ == '__main__':
    main(sys.argv)