
def eliminateImplication(logic):

    result = []
    result.append('|')
    result.append(['!', logic[1]])
    result.append(logic[2])

    return result


def eliminateIFF(logic):

    result = []
    result.append('&')
    result.append(eliminateImplication(['>', logic[1], logic[2]]))
    result.append(eliminateImplication(['>', logic[2], logic[1]]))

    return result


def propogateNOT(logic):

    result = []

    if(logic[1][0] == '|'):
        result.append('&')
    elif(logic[1][0] == '&'):
        result.append('|')
    elif(logic[1][0] == '!'):
        return logic[1][1]

    for i in range(1, len(logic[1])):
        if len(logic[1][i]) != 1:
            result.append(propogateNOT(['!', logic[1][i]]))
        else:
            result.append(['!', logic[1][i]])

    return result


def distributeOR(logic):

    result = []
    result.append('&')

    # Check if both the lists are ands
    if logic[1][0] == '&' and logic[2][0] == '&':
        # Distribute the literals
        result.append(parseDistribution(['|', logic[1][1], logic[2][1]]))
        intermediate_term = result.pop()
        result.append(parseDistribution(
            ['&', intermediate_term, ['|', logic[1][1], logic[2][2]]]))
        intermediate_term = result.pop()
        result.append(parseDistribution(
            ['&', intermediate_term, ['|', logic[1][2], logic[2][1]]]))
        result.append(parseDistribution(['|', logic[1][2], logic[2][2]]))

    else:
        if logic[1][0] == '&':

            if len(logic[2]) > 2:
                if isDistributionCandidate(logic[2]):
                    logic[2] = parseDistribution(logic[2])

                    result.append(parseDistribution(
                        ['|', logic[1][1], logic[2][1]]))
                    intermediate_term = result.pop()
                    result.append(parseDistribution(
                        ['&', intermediate_term, ['|', logic[1][1], logic[2][2]]]))
                    intermediate_term = result.pop()
                    result.append(parseDistribution(
                        ['&', intermediate_term, ['|', logic[1][2], logic[2][1]]]))
                    result.append(parseDistribution(
                        ['|', logic[1][2], logic[2][2]]))

                else:
                    result.append(parseDistribution(
                        ['|', logic[1][1], logic[2]]))
                    result.append(parseDistribution(
                        ['|', logic[1][2], logic[2]]))

            else:
                result.append(parseDistribution(['|', logic[1][1], logic[2]]))
                result.append(parseDistribution(['|', logic[1][2], logic[2]]))
        else:

            if len(logic[1]) > 2:
                if isDistributionCandidate(logic[1]):
                    logic[1] = parseDistribution(logic[1])

                    result.append(parseDistribution(
                        ['|', logic[1][1], logic[2][1]]))
                    intermediate_term = result.pop()
                    result.append(parseDistribution(
                        ['&', intermediate_term, ['|', logic[1][1], logic[2][2]]]))
                    intermediate_term = result.pop()
                    result.append(parseDistribution(
                        ['&', intermediate_term, ['|', logic[1][2], logic[2][1]]]))
                    result.append(parseDistribution(
                        ['|', logic[1][2], logic[2][2]]))
                else:
                    # Keep the second as it is
                    result.append(parseDistribution(
                        ['|', logic[1], logic[2][1]]))
                    result.append(parseDistribution(
                        ['|', logic[1], logic[2][2]]))
            else:
                # Keep the second as it is
                result.append(parseDistribution(['|', logic[1], logic[2][1]]))
                result.append(parseDistribution(['|', logic[1], logic[2][2]]))

    return result


def parseImplications(logic):
    if logic[0] == '=' and len(logic) == 3:
        logic = eliminateIFF(logic)
    elif logic[0] == '>' and len(logic) == 3:
        logic = eliminateImplication(logic)

    for i in range(1, len(logic)):
        if len(logic[i]) > 1:
            logic[i] = parseImplications(logic[i])

    if logic[0] == '=' and len(logic) == 3:
        logic = eliminateIFF(logic)
    elif logic[0] == '>' and len(logic) == 3:
        logic = eliminateImplication(logic)

    return logic


def parseNOTs(logic):

    if logic[0] == '!' and len(logic) == 2 and len(logic[1]) != 1:
        logic = propogateNOT(logic)

    for i in range(1, len(logic)):
        if len(logic[i]) > 1:
            logic[i] = parseNOTs(logic[i])

    if logic[0] == '!' and len(logic) == 2 and len(logic[1]) != 1:
        logic = propogateNOT(logic)

    return logic


def isDistributionCandidate(logic):

    if logic[0] == '|':
        for i in range(1, len(logic)):
            if len(logic[i]) > 1:
                if logic[i][0] == '&':
                    return True
    return False


def parseDistribution(logic):

    if isDistributionCandidate(logic):
        logic = distributeOR(logic)

    for i in range(1, len(logic)):
        if len(logic[i]) > 1:
            logic[i] = parseDistribution(logic[i])

    if isDistributionCandidate(logic):
        logic = distributeOR(logic)

    return logic


def convert_to_cnf(sentence):
    if len(sentence) == 0:
        return sentence
    if len(sentence) == 1:
        return sentence[0]

    result = parseImplications(sentence)
    result = parseNOTs(result)
    result = parseDistribution(result)

    return result
