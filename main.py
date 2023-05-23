import Top_down
import Buttom_up
import numpy
from collections import deque

def main():
    while True:
        print("------\nParser\n------")
        answer = int(input("1.Analizador sintactico descendente (Top-Down)\n2.Analizador sintactico ascendente (Bottom-Up)\n3.detener el programa\n"))
        if answer == 1:
            Top_down.main()
        elif answer == 2:
            Buttom_up.main()
        else:
            break
        
if __name__ == "__main__":
    main()
