from collections import deque


class Production:
    def __init__(self, key, production: str, cort: str):
        self.key = key
        if production != 'ε':
            self.pro = production
        else:
            self.pro = ''
        if cort != 'ε':
            self.cort = cort
        else:
            self.cort = ''

    def actualizarPuntero(self):
        Gr = Grammar()
        char, string = Gr.getChar(self.cort)
        return string

    def getNextPuntero(self):
        Gr = Grammar()
        char, string = Gr.getChar(self.cort)
        return char


class Node:
    def __init__(self, val):
        self.val = val
        self.values = []
        self.val2 = []


class Grammar:
    def __init__(self):
        self.terminals = []
        self.nonterminals = []
        self.rules = {}
        self.firsts = {}
        self.follows = {}
        self.productions = []
        self.i = 0
        self.nodos = []
        self.anticipate = {}
        self.actions = {}
        self.RR0 = True

    def readGrammar(self):
        print("Para el correcto funcionamiento del Buttom_up implementa la siguiente estructura:")
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
            for arr in value:
                followsf(key, arr)
        for key, value in dict(self.follows).items():
            self.follows[key] = set(convertList(value[0], self.follows, [], []))

    def LR0(self, Nodo, visitados=[]):
        def evaluate(A, visited) -> list:
            if A in self.anticipate:
                return self.anticipate[A]
            if A not in visited:
                visited.append(A)
                producciones = []
                for elem1 in self.rules[A]:
                    producciones.append(self.findProduction(A, elem1, elem1))
                    charo, elem1 = self.getChar(elem1)
                    if charo in self.rules:
                        producciones += evaluate(charo, visited)
                    producciones = list(set(producciones))
                return producciones
            else:
                return []

        for elem in Nodo.val:
            char = elem.getNextPuntero()
            if char in self.rules and char not in visitados:
                visitados.append(char)
                Nodo.val2 += evaluate(char, [])
                Nodo.val2 = list(set(Nodo.val2))
        Nodo.val2 = list(Nodo.val) + list(Nodo.val2)
        self.nodos.append(Nodo)
        self.GoTo(Nodo)

    def GoTo(self, Nodo):
        temporalG = {}
        for elem in Nodo.val2:
            key = elem.getNextPuntero()
            if key != '':
                try:
                    temporalG[key] += [self.findProduction(elem.key, elem.pro, elem.actualizarPuntero())]
                except:
                    temporalG[key] = [self.findProduction(elem.key, elem.pro, elem.actualizarPuntero())]
        for key1, value in dict(temporalG).items():
            index = self.lookForNode(value)
            if index is None:
                self.LR0(Node(value), [])
                idx = self.lookForNode(value)
                temporalG[key1] = self.nodos[idx]
            else:
                temporalG[key1] = self.nodos[index]
        Nodo.values = temporalG

    def setReduces(self):
        for i in range(len(self.nodos)):
            self.actions[i] = {}
        for nodo in self.nodos:
            for p in nodo.val2:
                if p.cort != '':
                    self.setShifts(nodo)
                else:
                    index = self.nodos.index(nodo)
                    if p.key == self.nodos[0].val[0].key:
                        self.actions[index]['$'] = 'A'
                    else:
                        for fol in list(self.follows[p.key]):
                            cadena = ['r' + str(self.lenRegla(p.pro, 0)), p.key]
                            if fol in self.actions[index] and self.actions[index][fol] != cadena:
                                self.RR0 = False
                                return
                            else:
                                self.actions[index][fol] = cadena

    def setShifts(self, node):
        begin = False
        for key, value in dict(node.values).items():
            if key in self.actions[self.nodos.index(node)]:
                temporal = self.actions[self.nodos.index(node)][key]
                begin = True
            if key not in list(self.rules.keys()):
                self.actions[self.nodos.index(node)][key] = 's' + str(self.nodos.index(value))
            else:
                self.actions[self.nodos.index(node)][key] = str(self.nodos.index(value))
            if begin:
                if temporal != self.actions[self.nodos.index(node)][key]:
                    self.RR0 = False
                    return

    def lookForNode(self, valor):
        for i in range(len(self.nodos)):
            if self.nodos[i].val == valor:
                return i
        return None

    def findProduction(self, key, pro, cort):
        for prod in self.productions:
            if prod.key == key and prod.pro == pro and prod.cort == cort:
                return prod
        P = Production(key, pro, cort)
        self.productions.append(P)
        return P

    def lenRegla(self, regla, tamanio):
        if regla == '':
            return tamanio
        else:
            char, regla = self.getChar(regla)
            return self.lenRegla(regla, tamanio + 1)

    def printNodos(self):
        for nodo in self.nodos:
            idx = self.nodos.index(nodo)
            print("newNode:", idx)
            for regla in nodo.val:
                print(f'{regla.key}->{regla.cort}')
            print("---------------")
            for regla in nodo.val2:
                print(f'{regla.key}->{regla.cort}')
            print("---------------")

    def printActions(self):
        for key, value in self.actions.items():
            print("---------------")
            print(key)
            for key1, value1 in value.items():
                print(f'{key1}:{value1}')
        print("---------------")

    def parsing_string(self, string):
        tabla_slr = self.actions
        cadena_analizar = string + "$"
        stack = deque()
        stack.append(0)
        i = 0
        while True:
            estado_actual = stack[-1]
            simbolo_actual = cadena_analizar[i]
            if estado_actual in tabla_slr:
                if simbolo_actual in tabla_slr[estado_actual]:
                    accion = tabla_slr[estado_actual][simbolo_actual]

                    if accion[0] == 's':
                        # Desplazamiento
                        stack.append(int(accion[1:]))
                        i += 1
                    elif isinstance(accion, list):
                        # Reducción
                        regla_index = int(accion[0][1:])
                        for _ in range(regla_index):
                            stack.pop()
                        simbolo_actual = stack[-1]
                        if accion[1] in tabla_slr[simbolo_actual]:
                            stack.append(int(tabla_slr[simbolo_actual][accion[1]]))
                        else:
                            print("no")
                            return
                    elif accion == 'A':
                        # Aceptación
                        print("si")
                        return
                else:
                    # Error de sintaxis
                    print("no")
                    return
            else:
                # Error de sintaxis
                print("La cadena no es valida")
                return
        print("La cadena no es válida. condicion prueba")


def addDict(dict1, dict2):
    for key, value in dict(dict1).items():
        if key in dict2:
            dict1[key] += list(set(dict2[key]))
            dict2.pop(key)
    dict1.update(dict2.items())
    return dict1


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
    p0 = list(G.rules.keys())[0]
    P = Production("Aux", p0, p0)
    Nodo = Node([P])
    G.first()
    G.follow()
    G.LR0(Nodo, [])
    G.GoTo(Nodo)
    G.setReduces()
    # G.printActions()
    strings = []
    if G.RR0:
        string = ""
        print("Ingrese las cadenas para verificar, finalice con una linea en blanco")
        while True:
            string = input()
            if len(string) == 0:
                break
            strings.append(string)
            
        for i in range(len(strings)):
            G.parsing_string(strings[i])
    else:
        print("Error. The grammar you provided is not LR(1)")
    


if __name__ == "__main__":
    main()
