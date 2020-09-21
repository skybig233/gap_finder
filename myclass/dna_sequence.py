# -*- coding: utf-8 -*-
# @Time : 2020/9/10 15:32
# @Author : Jiangzhesheng
# @File : dna_sequence.py
# @Software: PyCharm
import argparse
import sys
import logging
BASE_LIST=['A','G','C','T','a','g','c','t','N','n']
PRINCIPLE_DICT={'A':'T','a':'T','T':'A','t':'A',
                'C':'G','c':'G','G':'C','g':'C'}
class Sequence:
    def __init__(self,string,orient='+') -> None:
        for i in string:
            if not i in BASE_LIST:
                logging.warning(string+' is not a DNA seq')
                return
        self.value=string
        self.orient=orient
    def reverse(self)->str:
        ans=''
        for i in self.value:
            ans=PRINCIPLE_DICT[i]+ans
        return ans

if __name__ == '__main__':
    s=Sequence('AGCTatcc')
    print(s.reverse())