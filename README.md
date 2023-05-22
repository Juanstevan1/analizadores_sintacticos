# analizadores_sintacticos

Este repositorio contiene implementaciones de dos tipos de analizadores sintácticos ampliamente utilizados en el campo de la compilación y el procesamiento de lenguajes de programación: Bottom-Up y Top-Down.

----
Analizador Top-Down
-
Al realizar el proyecto se tomaron las siguientes condicones: 
  1. Verificar si la gramatica es LL(1). Si la gramatica no es LL(1), retornar el mensaje “error” y detener
     la ejecucion, no es necesario procesar las cadenas.
  2. Calcular los conjuntos First y Follow. Tambi´en se debe implementar la funci´on para calcular el conjunto
     Fisrt de una cadena.
  3. Calcular la tabla de an´alisis sintactico.
  4. Implementar algoritmo de an´alisis de cadenas.
 
 
En el proceso de análisis top-down, se parte de la raíz del árbol y se desciende hacia los símbolos terminales siguiendo las reglas gramaticales. Cada no terminal en el camino se expande utilizando reglas de producción hasta que se alcancen los símbolos terminales correspondientes. El analizador top-down puede utilizar diferentes algoritmos, como el algoritmo LL(1).

