import numpy
from collections import deque


class Node:
    def __init__(self, val):
        self.val = val
        self.values = []
        self.next = None

    def addList(self, list):
        if list.val == self.val:
            return None

        def addNode(root, Nodo):
            while root.next != None:

                if root.val == Nodo.val or Nodo.val == self.val:
                    break
                root = root.next
            if root.next == None:
                root.next = Nodo

        while list != None:
            temporal = list
            temporal.next = None
            addNode(self, temporal)
            list = list.next

    def addValue(self, value):
        if isinstance(value, list):
            self.values.extend(value)
        else:
            self.values.append(value)


class Grammar:
    def __init__(self):
        self.terminals = []
        self.nonterminals = []
        self.rules = {}
        self.firsts = {}
        self.follows = {}
        self.lookAhead = {}

    def readGrammar(self):
        print("Para el correcto funcionamiento del Top_Down implementa la siguiente estructura:")
        print("S->AB|abc")
        print("Para finalizar ingresa el símbolo '$'")
        entrada = (input("Ingresa la regla\n"))
        while (entrada != "$"):
            entrada = entrada.replace(" ", "")
            entrada = entrada.split("->")
            rules = entrada[1].split("|")
            self.rules[entrada[0]] = []
            for rule in rules:
                self.rules[entrada[0]].append(rule)
            entrada = input("Ingresa la regla\n")

    def eliminateLeftRecursion(self, key):
        newString = key + "'"
        self.rules[newString] = []
        beta = []
        gamma = []
        for rul in self.rules[key]:
            if len(rul) > 0 and key == rul[0]:
                beta.append(rul[1:] + newString)
            else:
                gamma.append(rul + newString)
        if '' in self.rules[key]:
            gamma.append('')
        self.rules[key] = gamma
        self.rules[newString] = beta + ['ε']

    def indirectLeftRecursion(self):
        def deepWay(regla, Ai):
            for char in regla:
                if char in self.rules.keys():
                    if 'ε' in self.rules[char]:
                        self.rules[Ai].append(regla[1:])
                else:
                    break

        def alternativesWays(diccionario):
            for nont, reglas in diccionario.items():
                for regla in reglas:
                    if len(regla) == 1 and regla[0] in list(self.rules.keys()) and regla[0] != nont:
                        self.rules[nont] += self.rules[regla[0]]
                    if regla[0] in list(diccionario.keys()) and len(regla) > 1:
                        deepWay(regla, nont)

        def auxiliary(Aj, Ai, rule1, temporal):
            gamma = rule1[1:]
            self.rules[Ai].remove(rule1)
            for regla in list(temporal[Aj]):
                self.rules[Ai].append(regla + gamma)

        # alternativesWays(dict(self.rules))
        temporal = self.rules.copy()
        Nonterminals = list(temporal.keys())
        for i in range(len(Nonterminals)):
            array = Nonterminals[:i]
            for rule2 in list(temporal[Nonterminals[i]]):
                if len(rule2) > 0 and rule2[0] in array:
                    #                    print("Regla aplica",Nonterminals[i],rule2)
                    auxiliary(rule2[0], Nonterminals[i], rule2, temporal.copy())
        self.removeLeftRecursion()
        for nont, rules in dict(self.rules).items():
            self.rules[nont] = list(set(rules))

    def removeLeftRecursion(self):
        # direct left recursion
        temp = self.rules.copy()
        for key, value in temp.items():
            temp = []
            temp.extend(value)
            for i in range(len(temp)):
                if temp[i][0] == key:
                    self.eliminateLeftRecursion(key)
                    break

    def readGrammar(self):
        print("Para el correcto funcionamiento implementa la siguiente estructura:")
        print("S->AB|abc")
        print("Para finalizar ingresa el símbolo '$'")
        entrada = input("Ingresa la regla\n")
        while entrada != "$":
            entrada = entrada.replace(" ", "")
            entrada = entrada.split("->")
            rules = entrada[1].split("|")
            self.rules[entrada[0]] = []
            for rule in rules:
                self.rules[entrada[0]].append(rule)
            entrada = input("Ingresa la regla\n")

    def calculateFirst(self):
        self.firsts = {}

        # Inicializar el conjunto de First para todos los símbolos
        for symbol in self.terminals + self.nonterminals:
            self.firsts[symbol] = set()

        changed = True
        while changed:
            changed = False
            for nonterminal in self.nonterminals:
                for production in self.rules[nonterminal]:
                    index = 0
                    while index < len(production):
                        currentSymbol = production[index]

                        if currentSymbol in self.terminals:
                            if currentSymbol not in self.firsts[nonterminal]:
                                self.firsts[nonterminal].add(currentSymbol)
                                changed = True
                            break
                        elif currentSymbol in self.nonterminals:
                            if 'ε' not in self.firsts[currentSymbol]:
                                for symbol in self.firsts[currentSymbol]:
                                    if symbol not in self.firsts[nonterminal]:
                                        self.firsts[nonterminal].add(symbol)
                                        changed = True
                                break
                            else:
                                for symbol in self.firsts[currentSymbol]:
                                    if symbol != 'ε' and symbol not in self.firsts[nonterminal]:
                                        self.firsts[nonterminal].add(symbol)
                                        changed = True
                        else:
                            if currentSymbol != 'ε' and currentSymbol not in self.firsts[nonterminal]:
                                self.firsts[nonterminal].add(currentSymbol)
                                changed = True
                            break

                        index += 1
                    else:
                        if 'ε' not in self.firsts[nonterminal]:
                            self.firsts[nonterminal].add('ε')

    def first(self):
        self.nonterminals = list(set(self.rules.keys()))
        self.terminals = []

        for rules in self.rules.values():
            for rule in rules:
                for symbol in rule:
                    if symbol not in self.nonterminals:
                        self.terminals.append(symbol)

        self.terminals = list(set(self.terminals))

        # Calcular el conjunto de First
        self.calculateFirst()

        for clave in self.terminals:
            if clave in self.firsts:
                del self.firsts[clave]

    def getChar(self, rule):
        if len(rule) == 0:
            return "", ""
        else:
            try:
                if rule[1] == "'":
                    return (rule[0] + rule[1]), rule[2:]
            except:
                pass
            return rule[0], rule[1:]

    def FirstOfString(self, string, first=[], cond=False):
        if len(string) == 0 or string == " ":
            if cond:
                first += ['ε']
            return first
        else:
            char, string1 = self.getChar(string)
            if char in list(self.rules.keys()):
                first += list(set(self.firsts[char]) - {'ε'})

            else:
                return first+ [char]
            if 'ε' in self.firsts[char]:
                return self.FirstOfString(string1, first, True)
            else:
                return first

    def follow(self):
        for key in list(self.rules.keys()):
            self.follows[key] = [Node(key)]
        self.follows[list(self.rules.keys())[0]] += ['$']

        def followsf(A, rule):
            if len(rule) > 0:
                char, rule1 = self.getChar(rule)
                if char not in list(self.rules.keys()):
                    followsf(A, rule1)
                else:
                    firstsBeta = self.FirstOfString(rule1, [])
                    self.follows[char] += list(set(firstsBeta) - {'ε'})
                    if 'ε' in firstsBeta and char != A:
                        self.follows[char].append(self.follows[A][0])
                    elif len(rule1) == 0 and char != A:
                        self.follows[char].append(self.follows[A][0])
                    followsf(A, rule1)

        for key, value in dict(self.rules).items():
            self.lookAhead[key] = {}
            for arr in value:
                followsf(key, arr)
        for key, value in dict(self.follows).items():
            self.follows[key] = set(convertList(value[0], self.follows, [], []))

    def LL1(self):
        def comparator(A, rules):
            if len(rules) > 1:
                rule1 = rules[0]
                first1 = set(self.FirstOfString(rule1))
                for rule in rules[1:]:
                    first2 = set(self.FirstOfString(rule))
                    if first1.intersection(first2) != set():
                        return False
                    if 'ε' in first1:
                        return first2.intersection(set(self.follows[A])) == set()
                    elif 'ε' in first2:
                        return first1.intersection(set(self.follows[A])) == set()
                return comparator(A, rules[1:])
            elif len(rules) == 1:
                # print(A,rules)
                rule1 = rules[0]
                first1 = set(self.FirstOfString(rule1))
            return True

        for key, value in dict(self.rules).items():
            self.createTableL(key, value)
            if not comparator(key, value):
                return False
        return True

    def createTableL(self, A, rules):
        if len(rules) > 0:
            rule = rules[0]
            firstBeta = self.FirstOfString(rule)
            for elem in (set(firstBeta) - {'ε'}):
                self.lookAhead[A][elem] = rule
            if 'ε' in firstBeta:
                for elem in self.follows[A]:
                    self.lookAhead[A][elem] = rule
            self.createTableL(A, rules[1:])

    def getTNT(self):
        self.nonterminals = list(self.rules.keys())

        def getTerminals(rule):
            if len(rule) > 0:
                char, rule = self.getChar(rule)
                if char not in list(self.rules.keys()):
                    self.terminals.append(char)
                    self.terminals = list(set(self.terminals))
                getTerminals(rule)

        for key, value in self.rules.items():
            for arr in value:
                getTerminals(arr)

    def printLookAhead(self):
        for key, value in self.lookAhead.items():
            print(key)
            for key1, value1 in value.items():
                print(f'{key1}:{value1}')

    def lookAheadAnalysis(self, input):
        def addElements(rule, elements):
            if len(rule) > 0:
                char, rule = self.getChar(rule)
                if char != 'ε':
                    elements.append(char)
                return addElements(rule, elements)
            else:
                return elements

        pila = deque()
        pila.append('$')
        pila.append(list(self.rules.keys())[0])
        input += '$'
        ip = input[0]
        input = input[1:]
        X = pila[-1]
        while X != '$':
            if X == ip:
                ip = input[0]
                input = input[1:]
                pila.pop()
            elif X not in self.nonterminals:
                return "no"
            elif self.lookAhead[X].get(ip) is None:
                return "no"
            else:
                pila.pop()
                pila.extend(addElements(self.lookAhead[X][ip], [])[::-1])
            X = pila[-1]
        if ip == '$':
            return "si"
        else:
            return "no"


def convertList(A, follows, visitados, follow=[]):
    visitados.append(A)
    for elem in list(follows[A.val]):
        if isinstance(elem, str) and elem not in list(follows.keys()):
            follow.append(elem)
        elif elem not in visitados and isinstance(elem, Node):
            follow += convertList(elem, follows, visitados, follow)
    return follow


def main():
    G = Grammar()
    G.readGrammar()
    G.indirectLeftRecursion()
    G.removeLeftRecursion()
    G.getTNT()
    # print("Rules->",G.rules)
    G.first()
    # print("Firsts->",G.firsts)
    G.follow()
    # print(G.LL1())
    # print(G.lookAhead)
    # print("Follows->",G.follows)
    strings =[]
    if G.LL1():
        string = ""
        print("Ingrese las cadenas para verificar, finalice con una linea en blanco")
        while True:
            string = input()
            if len(string) == 0:
                break
            strings.append(string)
            
        for i in range(len(strings)):
            print(G.lookAheadAnalysis(strings[i]))
    else:
        print("Error. The grammar you provided is not LL(1)")
    
        


if __name__ == "__main__":
    main()
