Parantheses = ['(', ')']
Operators = ['|', '&', '!', '>', '=']


def parse(sentence):
    # print(sentence)
    expressions = []
    operators = []
    i = 0
    while i < len(sentence):
        if sentence[i] == '!':
            if sentence[i+1] == '(':
                i += 2
                sub_str = ''
                count = 1
                while count != 0:
                    if sentence[i] == '(':
                        count += 1
                    elif sentence[i] == ')':
                        count -= 1
                    if count > 0:
                        sub_str += sentence[i]
                    i += 1
                expressions.append(['!', parse(sub_str)])
            else:
                expressions.append(['!', sentence[i+1]])
                i += 2

        elif sentence[i] not in Parantheses and sentence[i] not in Operators:
            expressions.append(sentence[i])
            i += 1

        elif sentence[i] in Operators:
            operators.append(sentence[i])
            i += 1

        elif sentence[i] == '(':
            i += 1
            sub_str = ''
            count = 1
            while count != 0:
                if sentence[i] == '(':
                    count += 1
                elif sentence[i] == ')':
                    count -= 1
                if count > 0:
                    sub_str += sentence[i]
                i += 1
            expressions.append(parse(sub_str))

    # print(expressions)
    # print(operators)
    while operators:
        operand1 = expressions.pop()
        operand2 = expressions.pop()
        operator = operators.pop()
        expressions.append([operator, operand2, operand1])

    if len(expressions) == 1:
        return expressions[0]
    return expressions


def isSegregationRequired(clauses,symbol):
    for clause in clauses:
        if clause[0] == symbol:
            return clause, True
    return None, False


def segregate(clauses,symbol):
    # print('segregation: ',clauses)
    clauseSet = []
    i = 0
    while 1:
        clause, flag = isSegregationRequired(clauses,symbol)
        if flag == False:
            break
        clauses.append(clause[1])
        clauses.append(clause[2])
        clauses.remove(clause)

    return clauses


def cleanUp(clauses):
    for clause in clauses:
        if len(clause) > 2:
            if clause[1] == clause[2]:
                ele = clause[1]
                clauses.remove(clause)
                clauses.append(ele)
            elif len(clause[1]) == 2 and len(clause[2]) == 1:
                if clause[1][1] == clause[2]:
                    clauses.remove(clause)
            elif len(clause[2]) == 2 and len(clause[1]) == 1:
                if clause[2][1] == clause[1]:
                    clauses.remove(clause)

def convertToClause(literals):
    if len(literals)==1:
        return literals[0]
    while 1:
        if len(literals)==1 and literals[0][0]=='|':
            return literals[0]
        literalFirst = literals.pop(0)
        literalSecond = literals.pop(0)
        literals.append(['|',literalFirst,literalSecond])
    
    
