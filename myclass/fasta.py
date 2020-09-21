import os
SCAFFOLD_HEADER='>'

class Fasta:
    def __init__(self,fastapath:str) -> None:
        self.path=fastapath
    def delete_linebreak(self,overwriteflag:bool=False):
        filename = os.path.basename(self.path)
        tmp_filename=filename+'.delblank'
        tmp_filepath=os.path.join(os.path.dirname(self.path), tmp_filename)
        with open(self.path,mode='r') as sourcefasta,open(tmp_filepath,mode='w') as newfile:
            newfile.write(sourcefasta.readline())
            s=''
            for line in sourcefasta:
                if SCAFFOLD_HEADER in line:
                    if s!='':
                        newfile.write(s+'\n')
                    newfile.write(line)
                else:
                    s=s+line.strip()
                if s!='':
                    newfile.write(s+'\n')
            if overwriteflag:
                os.remove(self.path)
                os.rename(tmp_filepath,filename)