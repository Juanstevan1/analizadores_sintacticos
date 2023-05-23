# Analizadores_sintacticos

Este repositorio contiene implementaciones de dos tipos de analizadores sintácticos ampliamente utilizados en el campo de la compilación y el procesamiento de lenguajes de programación: Bottom-Up y Top-Down.

----
Analizador Top-Down
--
Se tomaron las siguientes condicones para hacer el analizador Top-Down: 
  - Verificar si la gramatica es LL(1). Si la gramatica no es LL(1), retornar el mensaje “error” y detener
     la ejecucion, no es necesario procesar las cadenas.
  - Calcular los conjuntos First y Follow. Tambi´en se debe implementar la funci´on para calcular el conjunto
     Fisrt de una cadena.
  - Calcular la tabla de an´alisis sintactico.
  - Implementar algoritmo de an´alisis de cadenas.
---
Analizador Buttom-Up
--
Se tomaron las siguientes condicones para hacer el analizador Top-Down: 
  - Implementar funcion para calcular Closure(I) donde I es un conjunto de ıtems.
  - Calcular LR(0) canocico, utilizando la funcion GoTo(I, X) donde I es un conjunto de ıtems y X es
     un sımbolo de la gram´atica.
  - Calcular la tabla de an´alisis sintactico utilizando las funciones Action(I, a) y GoTo(I, X) donde
     a ∈ Σ, I es un conjunto de ıtems y X es un sımbolo de la gram´atica.
  - Implementar algoritmo de analisis de cadenas.
 
---
Input
--
Se ingresa desde consola, tanto la gramatica como para verificar las cadenas:
 - Gramatica:
       Cada produccion de un no terminal se ingresa en una sola linea, por ejemplo (S-> aS|ε) y termina con $. 
 - Cadenas:
       Se ingresa en lineas independientes y termina cuando lee una linea vacia.
      
---
Output
--
Cuando no es LL(1) o LR(1), sale por pantalla indicando que no lo es y no se analisan las cadenas. En cambio, si es
cumple las condiciones, leera la cadenas y nos dira si cumple o no. 

---
Requisitos
--
El proyecto se realizo en python 3.11, por lo tanto se necesita:
  - Importor las libreria (numpy y deque)
  - Ejecutar el programa (Main.py) teniendo encuenta que los 3 archivos esten en el mismo directorio.
  
---
Contacto
--
David Grisales Posada
dgrisalesp@eafit.edu.co

Juan Esteban Garcia Galvis
jegarciag1@eafit.edu.co

---
