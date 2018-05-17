from  pythonds.basic.stack import Stack

def precedence_rank(operator):
    if operator=='*':
        return 5
    elif operator=='/':
        return 4
    elif operator=='%':
        return 3
    elif operator=='+':
        return 2
    elif operator=='-':
        return 1
    elif operator=='(' or operator==')':
        return 0


def conversion(line):
    postfix = ''
    operators = [';', '+', '-', '*', '/', '%', '=', ',', '.', ':']
    stack = Stack()
    line=line.replace(' ','')
    for i in range(len(line)):
        if line[i].isdigit():
            postfix+=line[i]
            if (i+1 >= len(line) or line[i+1].isdigit()==False):
                postfix+=' '

        elif precedence_rank(line[i])!=0:
            while ((stack.isEmpty()==False) and (precedence_rank(stack.peek()) >= precedence_rank(line[i])) and stack.peek() != '(' ):
                if line[i] in operators and line[i+1] in operators:
                    postfix+=' '
                postfix+=stack.peek()
                stack.pop()
                postfix+=' '
            stack.push(line[i])
        elif line[i]=='(':
            stack.push(line[i])
        elif line[i]==')':
            while stack.isEmpty()==False and (stack.peek() != '('):
                postfix+=stack.peek()
                postfix+=' '
                stack.pop()
            stack.pop()
    while stack.isEmpty()==False:
        postfix+=stack.pop()
        postfix+=' '
    return postfix



