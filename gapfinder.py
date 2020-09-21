import argparse
import linecache

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfasta')
parser.add_argument('-o', '--outputgapinformation', default='gapfinder.result')
parser.add_argument('-l', '--getlength', default=50, type=int)
args = parser.parse_args()

inputfasta = args.inputfasta
output = args.outputgapinformation
getlength = args.getlength

i = 0
Nflag = False
line_length = len(linecache.getline(inputfasta, 2)) - 1


def getpoststr(filename: str, line_number: int, char_number: int, getstrlength: int) -> str:
    # 从第line_number行，第char_number列的字符开始，向后截取getstrlength的字符串，包括本身
    ans = ''
    line = linecache.getline(filename, line_number)
    if ('>' in line):
        return ans
    if (getstrlength <= line_length - char_number):
        return line[char_number:char_number + getstrlength]
    else:
        ans = line[char_number:-1]
        getstrlength = getstrlength - (line_length - char_number)
        ans = ans + getpoststr(filename, line_number + 1, 0, getstrlength)
    return ans


def getprestr(filename: str, line_number: int, char_number: int, getstrlength: int) -> str:
    # 从第line_number行，第char_number列的字符开始，向前截取getstrlength的字符串，包括本身
    ans = ''
    line = linecache.getline(filename, line_number)
    if ('>' in line):
        return ans
    if (getstrlength <= char_number + 1):
        return line[char_number - getstrlength + 1:char_number + 1]
    else:
        ans = line[:char_number + 1]
        getstrlength = getstrlength - (char_number + 1)
        ans = getprestr(filename, line_number - 1, line_length - 1, getstrlength) + ans
    return ans


# inputfasta = 'Mat_pshap2.mother.fa'
# output = 'gapinform'
# getlength = 50
gapcount=0

with open(inputfasta, mode='r')as inputfile, open(output, mode='w')as outputfile:
    for line in inputfile:
        i += 1
        if ('>' in line):
            scaffold_information = line[:-1]
        if('N' in line or Nflag==True):
            j = 0
            for char in line.strip():
                if (char == 'N' and Nflag == False):
                    gapcount+=1

                    tmp = getprestr(inputfasta, i, j, getlength + 1)[:-1]
                    line_information = 'gap'+str(gapcount)+'.'+'gap_line_location:' + str(i) + '.' + 'prestr' + '.' + 'str_len:' + str(len(tmp))
                    outputfile.write(scaffold_information + '.' + line_information + '\n')
                    outputfile.write(tmp + '\n')
                    Nflag = True
                if (Nflag == True and char != 'N'):
                    tmp = getpoststr(inputfasta, i, j, getlength).strip()
                    line_information = 'gap'+str(gapcount)+'.'+'gap_line_location:' + str(i) + '.' + 'poststr' + '.' + 'str_len:' + str(len(tmp))
                    outputfile.write(scaffold_information + '.' + line_information + '\n')
                    outputfile.write(tmp + '\n')
                    Nflag = False
                j += 1
