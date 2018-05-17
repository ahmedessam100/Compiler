from Lexical_analyzer import scan_table
from Conversion import conversion
from  pythonds.basic.stack import Stack

Registers={ 'S':'','T':'','A':''}
operators = [ '+', '-', '*', '/', '%']
def ProgName(fileName,program_Name):
    f = open(fileName+'.asm','w')
    f.write(program_Name +'\t'+ 'START\t' + '0')
    f.write('\n')
    f.close()

def loads(line_index,fileName):
    f=open(fileName+'.asm','a')
    if str(scan_table['Token_specifier'][line_index]).isdigit():
        f.write('\tLDT\t#'+scan_table['Token_specifier'][line_index])
    else:
        f.write('\tLDT\t'+scan_table['Token_specifier'][line_index])
    line_index+=2
    f.write('\n')
    if str(scan_table['Token_specifier'][line_index]).isdigit():
        f.write('\tLDS\t#'+scan_table['Token_specifier'][line_index])
    else:
        f.write('\tLDS\t'+scan_table['Token_specifier'][line_index])
    f.write('\n')
    f.write('LOOP')
    f.close()

def variables(line_index,fileName,line_numb):
    f=open(fileName+'.asm','a')
    while scan_table['Line_numb'][line_index]==line_numb :
            if scan_table['Token_type'][line_index]=='14' and scan_table['Token_type'][line_index+1]=='14':
                raise Exception('Syntax Error in line '+line_numb)
            if scan_table['Token_type'][line_index]=='22':
                f.write(scan_table['Token_specifier'][line_index] + '\t' +'RESW\t' + '1')
                f.write('\n')
            line_index+=1
    f.close()

def ReadGenerator(line_index_read,line_index_write,read,write,fileName,vars):
    f=open(fileName+'.asm','a')
    if write==True:
        f.write('EXTREF\tXREAD,XWRITE\n')
        f.write('STL\tRETADR\n')
        f.write('J\tEX\n')
        f.close()
        variables(vars[0],fileName,vars[1])
    else:
        f.write('\tEXTREF\tXREAD\n')
        f.write('STL\tRETADR\n')
        f.write('J\tEXADDR\n')
        f.close()
        variables(vars[0], fileName, vars[1])
    f = open(fileName+'.asm','a')
    f.write('EX')
    f.close()


def variables_def(vars,fileName):
    f = open(fileName + '.asm', 'a')
    vars=set(vars)
    for i in vars:
        f.write(i+'\t'+'RESW\t'+'1\n')
    f.close()

def add_generation(operand1,operand2,fileName):
    if operand1==Registers['A']:
        f=open(fileName+'.asm','a')
        f.write('\tLDT\t'+operand2+'\n')
        f.write('\tADDR\t'+'A,T'+'\n')
        f.close()
    elif operand2==Registers['A']:
        f=open(fileName+'.asm','a')
        f.write('\tLDT\t' + operand1 + '\n')
        f.write('\tADDR\t'+'A,T'+'\n')
        f.close()
    else:
        f=open(fileName+'.asm','a')
        f.write('\tLDA\t'+operand1+'\n')
        f.write('\tLDT\t' + operand2 + '\n')
        f.write('\tADDR\t' + 'A,T' + '\n')
        f.close()


def multiply_generation(operand1,operand2,fileName):
    if operand1==Registers['A']:
        f=open(fileName+'.asm','a')
        f.write('\tLDT\t'+operand2+'\n')
        f.write('\tMULR\t'+'A,T'+'\n')
        f.close()
    elif operand2==Registers['A']:
        f=open(fileName+'.asm','a')
        f.write('\tLDT\t' + operand1 + '\n')
        f.write('\tMULR\t'+'A,T'+'\n')
        f.close()
    else:
        f=open(fileName+'.asm','a')
        f.write('\tLDA\t'+operand1+'\n')
        f.write('\tLDT\t' + operand2 + '\n')
        f.write('\tMULR\t' + 'A,T' + '\n')
        f.close()


def subtract_generation(operand1,operand2,fileName):
    if operand1==Registers['A']:
        f=open(fileName+'.asm','a')
        f.write('\tLDT\t'+operand2+'\n')
        f.write('\tSUBR\t'+'A,T'+'\n')
        f.close()
    elif operand2==Registers['T']:
        f=open(fileName+'.asm','a')
        f.write('\tLDT\t' + operand1 + '\n')
        f.write('\tLDA\t' + operand1 + '\n')
        f.write('\tSUBR\t'+'A,T'+'\n')
        f.close()
    else:
        f=open(fileName+'.asm','a')
        f.write('\tLDA\t'+operand1+'\n')
        f.write('\tLDT\t' + operand2 + '\n')
        f.write('\tSUBR\t' + 'A,T' + '\n')
        f.close()


def divide_generation(operand1,operand2,fileName):
    if operand1==Registers['A']:
        f=open(fileName+'.asm','a')
        f.write('\tLDT\t'+operand2+'\n')
        f.write('\tDIVR\t'+'A,T'+'\n')
        f.close()
    elif operand2==Registers['T']:
        f=open(fileName+'.asm','a')
        f.write('\tLDT\t' + operand1 + '\n')
        f.write('\tLDA\t' + operand1 + '\n')
        f.write('\tDIVR\t'+'A,T'+'\n')
        f.close()
    else:
        f=open(fileName+'.asm','a')
        f.write('\tLDA\t'+operand1+'\n')
        f.write('\tLDT\t' + operand2 + '\n')
        f.write('\tDIVR\t' + 'A,T' + '\n')
        f.close()


def assigning(fileName,line_index):
    f = open(fileName + '.asm', 'a')
    f.write('\tLDA\t#'+scan_table['Token_specifier'][line_index+2]+'\n')
    f.write('\tSTA\t'+scan_table['Token_specifier'][line_index]+'\n')
    f.close()

def assign_precedence(line_index,line_numb,fileName,counter):
    stat = ''
    if(scan_table['Token_type'][line_index+3]=='12'):
        assigning(fileName,line_index)
        return None
    index=line_index+2
    while scan_table['Line_numb'][index]==line_numb :
        if scan_table['Token_specifier'][index] in operators:
            stat += scan_table['Token_specifier'][index]
            stat += ' '
            index += 1
            continue
        elif(scan_table['Token_type'][index]=='20' or scan_table['Token_type'][index]=='21'):
            stat += scan_table['Token_specifier'][index]
            stat+=' '
            index+=1
            continue
        elif scan_table['Token_type'][index]=='22':
            stat += str(index)
            stat += ' '
            index+=1
            continue
        else:
           break
    stat = conversion(stat)
    stat = stat.split()
    index=0
    for i in stat:
        if i not in operators:
            specifier = scan_table['Token_specifier'][int(i)]
            stat[index]= specifier
        index+=1
    index=0
    res='x'
    stack = Stack()
    while len(stat)>1:
        while stat[index] not in operators:
            stack.push(stat[index])
            stat.remove(stat[index])
        if stat[index] in operators:
            if stat[index]=='+':
                a = stack.pop()
                b = stack.pop()
                if counter!=' ':
                    if counter==a:
                        add_generation('X',b,fileName)
                    elif counter==b:
                        add_generation(a,'X', fileName)
                    else:
                        add_generation(a,b,fileName)
                else:
                    if counter == a:
                        add_generation('X', b, fileName)
                    elif counter == b:
                        add_generation(a, 'X', fileName)
                    else:
                        add_generation(a, b, fileName)
                Registers['A']=res
            elif stat[index]=='-':
                a = stack.pop()
                b = stack.pop()
                if counter != ' ':
                    if counter == a:
                        subtract_generation('X', b, fileName)
                    elif counter == b:
                        subtract_generation(a, 'X', fileName)
                    else:
                        subtract_generation(a, b, fileName)
                else:
                    if counter == a:
                        subtract_generation('X', b, fileName)
                    elif counter == b:
                        subtract_generation(a, 'X', fileName)
                    else:
                        subtract_generation(a, b, fileName)
                Registers['A']=res
            elif stat[index]=='*':
                a = stack.pop()
                b = stack.pop()
                if counter != ' ':
                    if counter == a:
                        multiply_generation('X', b, fileName)
                    elif counter == b:
                        multiply_generation(a, 'X', fileName)
                    else:
                        multiply_generation(a, b, fileName)
                else:
                    if counter == a:
                        multiply_generation('X', b, fileName)
                    elif counter == b:
                        multiply_generation(a, 'X', fileName)
                    else:
                        multiply_generation(a, b, fileName)
                Registers['A']=res
            elif stat[index]=='/':
                a = stack.pop()
                b = stack.pop()
                if counter != ' ':
                    if counter == a:
                        divide_generation('X', b, fileName)
                    elif counter == b:
                        divide_generation(a, 'X', fileName)
                    else:
                        divide_generation(a, b, fileName)
                else:
                    if counter == a:
                        divide_generation('X', b, fileName)
                    elif counter == b:
                        divide_generation(a, 'X', fileName)
                    else:
                        divide_generation(a, b, fileName)
            stat[index] = res
    f = open(fileName + '.asm', 'a')
    f.write('\tSTA\t' + scan_table['Token_specifier'][line_index] + '\n')
    f.close()