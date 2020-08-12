from cnf_converter import convert_to_cnf, parseNOTs
from PLparser import parse, segregate, cleanUp, convertToClause
from resolution_refutation import resolution


def openInputFile():
        f = open("input.txt")
        for line in f:
            numFields = line.split()
            if len(numFields)==0:
                continue
            print(numFields)
            numFormula = (int)(numFields[0])
            mode = numFields[1]
            formulaes = []
            for i in range(numFormula):
                formulaes.append(f.readline().strip())
            proposition = f.readline().strip()
            for i in range(len(formulaes)):
                formulaes[i] = "".join(formulaes[i].split())
            print(formulaes,proposition)
            knowledgeBase = []
            for formula in formulaes:
                knowledgeBase.append(parse(formula))
            proposition = parse(proposition)
            print('\n-----------------------------------------------------------------------------------------')
            print("The statement to prove : ", proposition)
            print("\nThe knowledge base(pretext) conditions are: \n",
                *knowledgeBase, sep='\n')

            CNFconverted_KB = []
            negated_CNFconverted_query = [
                parseNOTs(['!', convert_to_cnf(proposition)])]
            # negated_CNFconverted_query = segregate(negated_CNFconverted_query,'&')
            for kb in knowledgeBase:
                CNFconverted_KB.append(convert_to_cnf(kb))
            print("\n\nThe CNF form of the propositional statement is - \n",
                *CNFconverted_KB, sep='\n')
            print("The negation of the statement to prove : ", negated_CNFconverted_query)

            segregated_CNFterms = []
            segregated_CNFterms = segregate(CNFconverted_KB, '&')
            cleanUp(segregated_CNFterms)
            duplicateRemoved_CNFterms = []
            for terms in segregated_CNFterms:
                if terms not in duplicateRemoved_CNFterms:
                    duplicateRemoved_CNFterms.append(terms)
            print("\n\nThe individual statement of CNF form of the propositional statement are - \n",
                *duplicateRemoved_CNFterms, sep='\n')
            print('\n\nResolution steps:')
            print(resolution(segregated_CNFterms, negated_CNFconverted_query))
            print('-----------------------------------------------------------------------------------------')


if __name__ == "__main__":
    openInputFile()
