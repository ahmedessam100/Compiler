import tokenize,re
from sys import argv
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
script,FileName = argv
url = dir_path+'/PASCAL Examples/'+FileName
f = open(url,'r')
f_line = f.readline()
rest = f.readlines()
f_line = f_line.replace('\n','')
f_line = f_line.split()
pattern = re.compile(r'^[a-z]+([0-9])*[A-Z]*|^[A-Z]+[0-9]*[_]*([A-Z]*[0-9]*[_]*)*|^[A-Z]+[0-9]*[_]*([0-9]*[A-Z]*[_]*)*')
i=0
y=list()
string=''
operators=[';','(',')','+','-','*','/','%','=',',','.',':']
coding_sch = {'Token':['PROGRAM','VAR','BEGIN','END','END.','INTEGER','FOR','READ','WRITE','TO','DO',';',':',',',
                       '=','+','-','*','/','(',')','id','int'],'Code':['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                                                                       '12', '13',
                                                                       '14', '15', '16', '17', '18', '19', '20','21','22','23']}
counter = 0
scan_table = {'Token_type':[],'Token_specifier':[],'Line_numb':[]}
if(f_line[0]!='PROGRAM'):
    raise Exception('MISSING PROGRAM START')
li = list()
scan_table['Token_type'].append(coding_sch['Code'][0])
scan_table['Token_specifier'].append(' ')
scan_table['Line_numb'].append(1)
scan_table['Token_type'].append('22')
scan_table['Token_specifier'].append(f_line[1])
scan_table['Line_numb'].append(1)
line_count=2
bonus = False
li.append(1)
li.append(1)
for line in rest:
    i=0
    y.clear()
    line = line.replace('\n', '')
    m = line[i] + line[i+1] + line[i+2]
    if(m!='FOR'):
        line = line.replace(' ','')
    else:
        line = line.replace(' ', '')
        bonus = True
    string = ''
    counter = 0
    while(i<len(line)):
        temp=''
        if(bonus==True):
            bonus = False
            line = line.replace(' ','')
            string = m
            y.append(string)
            string = ''
            i+=3
            while line[i] not in operators:
                string += line[i]
                i+=1
            y.append(string)
            string = ''
            y.append(line[i])
            i+=1
            while line[i].isdigit():
                string += line[i]
                i+=1
            y.append(string)
            string = ''
            string = line[i]+line[i+1]
            y.append(string)
            string = ''
            i+=2
            while line[i]!='D' and line[i+1]!='O':
                string+=line[i]
                i+=1
            y.append(string)
            string=''
            string=line[i]+line[i+1]
            y.append(string)
            string=''
            i+=1
        else:
            if string == 'BEGIN':
                y.append(string)
                string = ''
                i += 1
            if (string == 'END'):
                if line[i] == '.':
                    string = string + line[i]
                    y.append(string)
                    string = ''
                    i += 1
                    continue
                else:
                    y.append(string)
                    string = ''
                    i += 1
            if len(string)==0 and line[i].isdigit() and line[i+1].isdigit():
                j=i
                count=0
                while(line[j].isdigit()):
                    string+=line[j]
                    j+=1
                    count+=1
                i+=count
                y.append(string)
                string=''
                continue
            if(i!=0) and line[i] not in operators :
                temp=string+line[i]
            if (((re.match(pattern,temp) ) or string=='' ) or (len(string)==1 and line[i].isdigit()==False)) and line[i] not in operators :
                string=string+line[i]
                if i == len(line)-1:
                   y.append(string)
            else:
                if(len(string)==0):
                    string=line[i]
                    y.append(string)
                    string=''
                    i+=1
                    continue
                string=str(string)
                y.append(string)
                if(line[i] in operators ):
                    y.append(line[i])
                string=''
        i+=1
    for token in y:
        if token in coding_sch['Token']:
            scan_table['Token_specifier'].append(token)
            index = coding_sch['Token'].index(token)
            scan_table['Line_numb'].append(line_count)
            scan_table['Token_type'].append(coding_sch['Code'][index])
        elif str(token[0]).isalpha():
            scan_table['Line_numb'].append(line_count)
            scan_table['Token_type'].append('22')
            scan_table['Token_specifier'].append(token)
        elif str(token[0]).isdigit():
            scan_table['Line_numb'].append(line_count)
            scan_table['Token_specifier'].append(token)
            scan_table['Token_type'].append('23')
    line_count += 1
line_count-=1
