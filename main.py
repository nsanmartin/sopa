#!/usr/bin/env python3

import sys
import getopt

from sopa import Sopa, Palabra, Direccion, Inclinacion

def main(argv):
    ayuda = False
    diagonal = 16
    try:
        opts, args = getopt.getopt(argv, "had:",
                                   ["help", "ayuda", "diagonal"])
    except:
        print("Se produjo un erro al leer las opciones")
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif o in ("-a", "--ayuda"):
            ayuda = True
        elif o in ("-d", "--diagonal"):
            diagonal = int(a)
        else:
            assert False, "unhandled option"

    s = Sopa(diagonal, diagonal)
    if len(args) == 0:
        for line in sys.stdin:
            pals = line.split()
            if max([ len(x) for x in pals ]) > diagonal:
                print("Tabla muy chica para palabras dadas")
                continue
            #print("\n\n\n")
            s.add_palabras(pals)

        s.mostrar_rnd(ayuda)
    else:
        with open(args[0], 'r') as f:
            for line in f:
                pals = line.split()
                if max([ len(x) for x in pals ]) > diagonal:
                    print("Tabla muy chica para palabras dadas")
                    continue
                #print("\n\n")
                s.add_palabras(pals)
                
        s.mostrar_rnd(ayuda)

def usage():
    msg = "uso: main [-a] [-d NUMERO] [ARCHIVO]\n\n" \
          + "\t-a Muestra como ayuda las palabras que estan en la sopa\n" \
          + "\t-d Es el taman~o de la diagonal. El valor por defecto es 16\n" \
          + "\tEl ARCHIVO es el lugar donde se buscan las palabras. Si no hay\n"\
          + "\tningu'n archivo se buscan en stdin."
    print(msg)
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    else :
        main(sys.argv[1:])
