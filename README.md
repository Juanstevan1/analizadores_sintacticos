# analizadores_sintacticos

Este repositorio contiene implementaciones de dos tipos de analizadores sintácticos ampliamente utilizados en el campo de la compilación y el procesamiento de lenguajes de programación: Bottom-Up y Top-Down.

----
#Analizador Bottom-Up
-
El analizador Bottom-Up, también conocido como analizador ascendente, construye un árbol de análisis comenzando desde los símbolos terminales y aplicando reglas gramaticales para llegar a la raíz del árbol. Este tipo de analizador sigue una estrategia de reducción o desplazamiento para construir el árbol de análisis.

En el proceso de análisis bottom-up, los símbolos terminales se combinan gradualmente en símbolos no terminales hasta llegar a la raíz del árbol. Se utiliza una pila para realizar el seguimiento de los símbolos en proceso de análisis y una tabla de análisis para determinar qué acción tomar en cada paso. El analizador bottom-up puede utilizar diferentes algoritmos, como el algoritmo LR(0), LR(1) o LALR(1).

#Analizador Top-Down
El analizador Top-Down, también conocido como analizador descendente, construye un árbol de análisis comenzando desde la raíz y utilizando reglas gramaticales para llegar a los símbolos terminales. Este tipo de analizador sigue una estrategia de análisis predictivo o análisis descendente recursivo para construir el árbol de análisis.

En el proceso de análisis top-down, se parte de la raíz del árbol y se desciende hacia los símbolos terminales siguiendo las reglas gramaticales. Cada no terminal en el camino se expande utilizando reglas de producción hasta que se alcancen los símbolos terminales correspondientes. El analizador top-down puede utilizar diferentes algoritmos, como el algoritmo LL(1).

