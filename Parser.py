from Lexical_analyzer import scan_table,line_count
from CodeGenerator import *
class parser(object):
    def __init__(self,fileName):
        self.fileName=fileName
    def program(self):
        i=1
        next_line = 0
        vars=list()
        x=scan_table['Line_numb'].index(6)
        while i <= line_count:
            if  scan_table['Token_type'][next_line]=='1':
                ProgName(self.fileName,scan_table['Token_specifier'][i])
                next_line=scan_table['Line_numb'].index(i+1)
                i += 1
                continue
            elif scan_table['Token_type'][next_line]=='2':
                i += 1
                if scan_table['Token_specifier'][next_line]=='VAR':
                    next_line = scan_table['Line_numb'].index(i)
                    continue
                else:
                    raise Exception('Syntax Error in line %d', + (i-1))
                    pass
            elif scan_table['Token_type'][next_line]=='22' and scan_table['Token_type'][next_line+1]=='14':
                vars.append(next_line)
                vars.append(i)
                i += 1
                next_line = scan_table['Line_numb'].index(i)
                continue
            elif scan_table['Token_type'][next_line] == '8':
                i+=1
                next_line += 1
                write=False
                read=False
                write_index=0
                if scan_table['Token_type'].__contains__('9'):
                    write_index = scan_table['Token_type'].index('9')
                    x=0
                    if READ(x,write_index)==True:
                        write=True
                    else:
                        raise Exception('Syntax Error in line ',x)
                if READ(i, next_line-1)==True:
                    read=True
                else:
                    raise Exception('Syntax Error in line ',i-1)
                if read==True or write==True:
                    ReadGenerator(next_line,write_index,read,write,self.fileName,vars)
                    vars.clear()
                    next_line = scan_table['Line_numb'].index(i)
                    continue
            elif scan_table['Token_type'][next_line]=='3' or scan_table['Token_type'][next_line]=='4':
                i+=1
                next_line = scan_table['Line_numb'].index(i)
                continue
            elif scan_table['Token_type'][next_line]=='22' and scan_table['Token_type'][next_line+1]=='15':
                i+=1
                statement=''
                vars.append(scan_table['Token_specifier'][next_line])
                if ASSIGN(next_line):
                    assign_precedence(next_line,i-1,self.fileName,' ')
                else:
                    raise Exception('Syntax Error in line ',i-1)
                next_line = scan_table['Line_numb'].index(i)
                continue
            elif scan_table['Token_type'][next_line]=='9':
                i+=1
                next_line = scan_table['Line_numb'].index(i)
                continue
            elif scan_table['Token_type'][next_line]=='5':
                break
            elif scan_table['Token_type'][next_line]=='7':
                i+=1
                next_line+=1
                loop = False
                counter = scan_table['Token_specifier'][next_line]
                loop,dum=FOR(i-1,next_line)
                if loop:
                   loads(next_line+2,fileName=self.fileName)
                   i+=1
                   next_line = scan_table['Line_numb'].index(i)
                   while scan_table['Token_type'][next_line]!='4':
                        assign_precedence(next_line,i,self.fileName,counter)
                        i+=1
                        next_line = scan_table['Line_numb'].index(i)
                else:
                    print("FAILURE!")
                f = open(self.fileName + '.asm', 'a')
                f.write('\tTIXR\tS\n')
                f.write('\tJLT\tLOOP\n')
                f.close()
        f=open(self.fileName+'.asm','a')
        f.write('\tEND'+'\t'+'0')
        f.close()


def FOR(line_numb,line_index):
    found = False
    correct = False
    body = False
    next = 0
    if scan_table['Token_type'][line_index]=='22':
        line_index+=1
        correct,line_index=index_exp(line_index)
        if correct and scan_table['Token_type'][line_index]=='11':
            line_index+=1
            line_numb+=1
            body,line_index = BODY_CHECK(line_numb,line_index)
    if body:
        return True,line_index
    else:
        return False,line_index


def BODY_CHECK(line_numb,line_index):
    found = False
    correct = False
    count = 0
    if scan_table['Token_type'][line_index]=='3':
        count+=1
        line_index+=1
        line_numb+=1
        while scan_table['Token_type'][line_index]!='4':
            if ASSIGN(line_index):
                count+=1
            else:
                raise Exception('Wrong Syntax')
            line_numb+=1
            line_index=scan_table['Line_numb'].index(line_numb)
        line_numb+=1
        found=True
    if found:
        return True,scan_table['Line_numb'].index(line_numb)
    else:
        return False,scan_table['Line_numb'].index(line_numb)


def index_exp(line_index):
    found = False
    correct = False
    if scan_table['Token_type'][line_index]=='15':
        line_index+=1
        if scan_table['Token_type'][line_index]=='23':
            line_index+=1
            if scan_table['Token_type'][line_index]=='10':
                line_index+=1
                if scan_table['Token_type'][line_index]=='22':
                    line_index+=1
                    found = True
    if found:
        return True,line_index
    else:
        return False,line_index



def READ(line_numb,line_index):
    found = False
    line_index+=1
    reader = False
    if scan_table['Token_type'][line_index]=='20':
        line_index+=1
        reader,line_index=IDLIST(line_numb,line_index)
        if reader==True:
            if scan_table['Token_type'][line_index]=='21':
                found=True
                line_index+=1
    if found==True:
        return True
    else:
        return False


def IDLIST(line_numb,line_index):
    found = False
    if scan_table['Token_type'][line_index]=='22':
        found = True
        line_index+=1
        while scan_table['Token_type'][line_index]=='14' and found==True:
            line_index+=1
            if scan_table['Token_type'][line_index]=='22':
                line_index+=1
            else:
                found = False
        if found == True:
            return True,line_index
        else:
            return False,line_index


def ASSIGN(line_index):
    found=False
    #line_index+=2
    if scan_table['Token_type'][line_index]=='22':
        line_index+=1
        if scan_table['Token_type'][line_index]=='15':
            line_index+=1
            exp,line_index=EXP(line_index)
            if exp:
                found=True
    if found:
        return True
    else:
        return False


def EXP(line_index):
    found=False
    term,line_index=TERM(line_index)
    if term:
        found=True
        while (scan_table['Token_type'][line_index]=='16' or scan_table['Token_type'][line_index]=='17') and found==True:
            line_index+=1
            term,line_index=TERM(line_index)
            if term==False:
                found=False
    if found:
        return True,line_index
    else:
        return False,line_index


def TERM(line_index):
    found=False
    factor,line_index=Factor(line_index)
    if factor:
        found=True
        while scan_table['Token_type'][line_index]=='18' or scan_table['Token_type'][line_index]=='19' and found==True:
            line_index+=1
            factor,line_index=Factor(line_index)
            if factor==False:
                found=False
    if found:
        return True,line_index
    else:
        return False,line_index


def Factor(line_index):
    found=False
    if scan_table['Token_type'][line_index]=='22' or scan_table['Token_type'][line_index]=='23' or scan_table['Token_type'][line_index]=='20' or scan_table['Token_type'][line_index]=='21' :
        found=True
        line_index+=1
    if found==True:
        return True,line_index
    else:
        return False,line_index