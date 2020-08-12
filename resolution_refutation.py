import copy
from PLparser import segregate,convertToClause


def resolvePair(firstClause, secondClause):
    newClause = []
    sndClause = copy.deepcopy(secondClause)
    literalFirstClause = segregate([firstClause], '|')
    literalSecondClause = segregate([secondClause], '|')
    literalSndClause = segregate([sndClause],'|')
    # print(literalFirstClause)
    # print(literalSecondClause)
    # print(literalSndClause)

    for literal in literalFirstClause:
        if len(literal) == 1 and ['!', literal] in literalSecondClause:
            literalSndClause.remove(['!',literal])
        elif len(literal) == 2 and literal[1] in literalSecondClause:
            literalSndClause.remove(literal[1])
        else:
            newClause.append(literal)

    for ele in literalSndClause:
        if ele not in newClause:
            newClause.append(ele)
    return newClause


def isResolveableWith(clause, otherClause):
    literalClause = segregate([clause], '|')
    literalOtherClause = segregate([otherClause], '|')
    for literal in literalClause:
        if len(literal) == 1 and ['!', literal] in literalOtherClause:
            return True
        elif len(literal) == 2 and literal[1] in literalOtherClause:
            return True
    return False


def selectClauses(clauses, setOfSupport, resolvedPairs):

    selectedPairs = []
    allClauses = clauses
    for ele in setOfSupport:
        if ele not in allClauses:
            allClauses.append(ele)
    for sos in setOfSupport:
        for clause in allClauses:
            if clause != sos and isResolveableWith(clause, sos):
                newPair = clause, sos
                if newPair not in resolvedPairs:
                    selectedPairs.append(newPair)

    return selectedPairs


def resolution(clauses, goal):

    resolvedPairs = []
    setOfSupport = goal

    while True:
        # print('setofs: ',setOfSupport)
        # print('resolved: ',resolvedPairs)
        pairs = selectClauses(clauses, setOfSupport, resolvedPairs)
        # print('pairs: ',pairs)

        if not pairs:
            return False

        newClauses = []
        for pair in pairs:
            c1, c2 = pair
            resolvents = resolvePair(c1, c2)
            resolvedPairs.append(pair)

            # check for NIL
            if not resolvents:
                print('Empty: [] ( Using Pair - ',pair,')')
                return True

            print('Resolvents: ',resolvents,'( Using Pair - ',pair,')')
            newClauses.append(convertToClause(resolvents))

        # print('sos: ',setOfSupport)
        # print('newEle: ',newClauses)
        for ele in newClauses:
            if ele not in setOfSupport:
                setOfSupport.append(ele)
