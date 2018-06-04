from enum import Enum
import random
import string

class Direccion(Enum):
    normal             = 0
    inversa            = 1

class Inclinacion(Enum):
    horizontal = 0
    vertical   = 1
    diagonal   = 2

class Sopa:
    def __init__(self, alto, ancho):
        self.alto  = alto
        self.ancho = ancho
        self.palabras = []
    def palabra_rnd(self, string):
        nletras = len(string)
        if nletras > self.alto or nletras > self.ancho: return None
        direccion = random.randint(0,1)
        inclinacion = random.randint(0,2)
        ubicacion = (0,0)
        if inclinacion == Inclinacion.horizontal.value:
            ubicacion = (random.randint(1, self.alto),
                         random.randint(1, self.ancho - nletras))
        elif inclinacion == Inclinacion.vertical.value:
            ubicacion = (random.randint(1, self.alto - nletras),
                         random.randint(1, self.ancho))
        elif inclinacion == Inclinacion.diagonal.value:
            ubicacion = (random.randint(1, self.alto - nletras),
                         random.randint(1, self.ancho - nletras))

        p = Palabra(string, direccion, inclinacion, ubicacion)
        return p

    def hay_conflicto_con(self, pal):
        for p in self.palabras:
            if p.hay_conflicto(pal): return True
        return False
    def add_palabras(self, str_lst):
        for s in str_lst:
            p = None
            while p is None or self.hay_conflicto_con(p):
                p = self.palabra_rnd(s)
            self.palabras.append(p)

    def at(self, fila, col):
        res = None
        for p in self.palabras:
            res = p.at(fila, col)
            if res is not None: break
        return res

    def mostrar(self):
        for i in range(1, self.ancho + 1):
            line = [str(i)+ "\t"]
            for j in range (1, self.alto + 1):
                at = self.at(i,j)
                if at is None: line.append("_")
                else: line.append(at)
            print (" ".join(line))

    def mostrar_rnd(self, ayuda = False):
        letras = string.ascii_uppercase
        #letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        npals = len(self.palabras)
        #i = 0
        for i in range(1, self.ancho + 1):
            line = []##[str(i)+ "\t"]
            for j in range (1, self.alto + 1):
                at = self.at(i,j)
                l = random.randint(0,len(letras))
                if at is None: line.append(letras[l - 1])
                else: line.append(at)
            if ayuda and i <= npals:
                line.append("\t" + self.palabras[i-1].string)
            print (" ".join(line))

        if ayuda and npals > self.ancho:
            for i in range (self.ancho, npals):
                print(self.palabras[i].string)

            
class Palabra:
    def __init__(self, string, direccion, inclinacion, ubicacion):
        "Parametros: string, direccion, inclinacion, ubicacion"
        self.string = string
        self.direccion = direccion
        self.inclinacion = inclinacion
        self.ubicacion = ubicacion # (fila, col)
    def len(self):
        return len(self.string)
    def rectangulo(self):
        if self.inclinacion == Inclinacion.horizontal.value:
            return (1, len(self.string))
        elif self.inclinacion == Inclinacion.vertical.value:
            return (len(self.string), 1)
        elif self.inclinacion == Inclinacion.diagonal.value:
            return (len(self.string), len(self.string))
    def imprimir(self):
        ##esto igual no tiene utilidad
        if self.inclinacion == Inclinacion.horizontal.value:
            if self.direccion == Direccion.normal.value:
                print(self.string)
            elif self.direccion == Direccion.inversa.value:
                print(self.string.reverse[::-1])
        if self.inclinacion == Inclinacion.vertical.value:
            if self.direccion == Direccion.normal.value:
                print(["%s\n" %  x for x in self.string])
            elif self.direccion == Direccion.inversa.value:
                print(self.string.reverse[::-1])
                
    def ocupap(self, fila, col):
        """val: bool, que expresa si la palabra ocupa o no
        la posicion, en funcio'n de su ubicacio'n, inclinacio'n"""
        _fila = self.ubicacion[0]
        _col = self.ubicacion[1]

        if fila < _fila or col < _col: return False

        # centro la palabra en (0, 0)
        fila = fila - _fila
        col = col - _col

        if fila > self.len() or col > self.len(): return False
        if self.inclinacion == Inclinacion.horizontal.value:
            return fila == 1
        if self.inclinacion == Inclinacion.vertical.value:
            return col == 1
        if self.inclinacion == Inclinacion.diagonal.value:
            return fila == col
        return True

    def at(self, fila , col):
        _fila = self.ubicacion[0]
        _col = self.ubicacion[1]

        if fila < _fila or col < _col: return None

        # centro la palabra en (0, 0)
        fila = fila - _fila
        col = col - _col
        
        if fila >= self.len() or col >= self.len(): return None
        if self.inclinacion == Inclinacion.horizontal.value and fila == 0:
            if self.direccion == Direccion.normal.value:
                return self.string[col]
            else:
                return self.string[self.len() - 1 - col]
        if self.inclinacion == Inclinacion.vertical.value and col == 0:
            if self.direccion == Direccion.normal.value:
                return self.string[fila]
            else:
                return self.string[self.len() - 1 - fila]
        if self.inclinacion == Inclinacion.diagonal.value and fila == col:
            if self.direccion == Direccion.normal.value:
                return self.string[fila]
            else:
                return self.string[self.len() - 1 - fila]
        return None
            
    def ocupados(self):
        fila = self.ubicacion[0]
        col  = self.ubicacion[1]
        l    = self.len()
        if self.inclinacion == Inclinacion.horizontal.value:
            # fila es fija
            return [(fila, x) for x in range (col, col + l) ]
        if self.inclinacion == Inclinacion.vertical.value:
            # col es fija
            return [(x, col) for x in range (fila, fila + l) ]
        if self.inclinacion == Inclinacion.diagonal.value:
            return [(x, y) for x, y in zip (range(fila, fila + l),
                                            range(col, col + l))]
    def hay_conflicto(self, pal):
        o1 = self.ocupados()
        o2 = pal.ocupados()
        for pt in o2:
            if pt in o1:
                x, y = pt[0], pt[1]
                if self.at(x, y) != pal.at(x, y): return True
        return False

