import numpy as np
import matplotlib.pyplot as plot


class carga:
    def __init__(self, tipo):
        #tipo = 0 Carga puntual
        #tipo = 1 Carga distribuida
        #tipo = 2 Momento concentrado
        self.tipo = tipo
    def Tipo(self):
        if self.tipo == 0:
            print('Carga Puntual')
        elif self.tipo == 1:
            print('Carga Distribuida')
        elif self.tipo == 2:
            print('Momento Concentrado')
        else:
            print('No Definido')

class CargaPuntual(carga):
    def __init__(self, P=0, a=0):
        #P: valor de la carga. Positivo hacia abajo.
        #a: posicion de la carga respecto al extremo izquierdo del tramo.
        Carga._init_(self, 0)
        self.P = P
        self.a = a
    def __str__(self):
        return 'Carga puntual\n Valor=' + str(self.p) + 'g' \
               + '\n Posicion, x= ' + str(self.a) + 'a'

    #Reacciones nodales equivalentes
    def Qf(self, L):
        #L: longitud de la viga.
        a = self.a
        return self.P / L**2 * np.array([
            [b**2 / L * (3*a+b)],
            [a*b**2],
            [-a**2 * b],
        ])
    #Fuerza cortante en una seccion (viga sin apoyo)
    def FQ(self, x, L):
        #x: posicion de la seccion debido a la cargaa puntual
        #L: longitud del tramo
        if self.a < x < L:
            return -self.P
        else:
            return 0

    #Momento flector en una seccion (viga simplemente apoyada)
    def MF(self, x, L):
         #x: posicion de la seccion considerada respecto al extremo izquierdo
         #L: longitud del tramo
        if 0 <= x < self.a:
            return (l-self.a/L) * self.P * x
        elif x <= L:
            return self.a * self.P * (l - x/L)
        else:
            return 0
class CargaDistribuida(carga):
    def __init__(self, q=0, a=0, l=0):
        #P: valor de la carga. Posicion hacia abajo.
        #a: distancia entre el extremo izquierdo del tramo y el inicio de la carga.
        #l: longitud de la carga distribuida'''
        Carga.__init__(self, l)
        self.q = q
        self.a = a
        self.l = l
    def __str__(self):
        return 'Carga distribuida\n Valor=  ' + str(self.q) + 'N/m'
    ', ' + '\n Inicio= ' + str(self.a) + 'a' + '\n Longitud= ' + str(self.l) + 'm'

    def Qf(self, L):
        #L: longitud de la viga.
        q = self.q
        a = self.a
        b = L - self.a - self.l
        return q*L/2* np.array([
        [1 - a / L ** 4 * (2 * L ** 3 - 2 * a ** 2 * L + a ** 3) - b ** 3 / L ** 4 * (2 * L - b)],
        [L/6*(1 - a**2/L**4*(6*L**2 - 8*a*L + 3*a**2) - b**3/L**4*(4*L - 3*b))],
        [1 - a**3/L**4*(2*L - a) - b/L**4*(2*L**3 - 2*b**2*L + a**3)],
        [-L/6*(1 - a**3/L**4*(4*L - 3*a) - b**2/L**4*(6*L**2 - 8*b*L + 3*b**2))]
    ])

    #Fuerza cortante en una sección (viga sin apoyos).
    def FQ(self, x, L):
        #L: Longitud del tramo.
        if self.a <= x < self.a + self.l:
            return -self.q * (x - self.a)
        elif x <= L:
            return -self.q * self.l
        else:
            return 0

    #Momento flector en una sección (viga simplemente apoyada).

    def MF(self, x, L):
        #L: Longitud del tramo.
        #V1 = self.q * self.l / L * (L - self.a - self.l / 2)
        #V2 = self.q * self.l - V1
        if 0 <= x < self.a:
            return V1 * x
        elif x <= self.a + self.l:
            return V1 * x - 0.5 * self.q * (x - self.a) ** 2
        elif x <= L:
            return V2 * (L - x)
        else:
            return 0

class MomentoConcentrado(Carga):
    def __init__(self, M=0, a=0):
        #M: valor del momento concentrado. Antihorario positivo.
        #a: posición del momento respecto al extremo izquiero del tramo.
        Carga.__init__(self, 2)
        self.M = M
        self.a = a

    def __str__(self):
        return 'Momento concentrado\\n Valor= ' + str(self.M) + 'Nm'
                ',' + '\n Posición, x= ' + str(self.a) + 'm'

     def Qf(self, L):
    #L: longitud de la viga.
        a = self.a
        b = L - a
        return self.M / L ** 2 * np.array([
            [-6 * a * b / L],
            [b * (b - 2 * a)],
            [6 * a * b / L],
            [a * (a - 2 * b)]
        ])
    #Fuerza cortante en una sección (viga sin apoyos).

    def FQ(self, x, L):
        #x: posición de la sección considerada respecto al extremo izquierdo.
        return 0

    #Momento flector en una sección (viga simplemente apoyada).

    def MF(self, x, L):
        #x: posición de la sección considerada respecto al extremo izquierdo.
        #L: Longitud del tramo.
        if 0 <= x < self.a:
            return self.M / L * x
        elif self.a < x <= L:
            return self.M * (x/L - 1)
        else:
            return 0
    #Cargas en cada tramo.
    #q = CargaDistribuida(valor, inicio, longitud), el inicio es respecto al nudo izq. del tramo
    #P = CargaPuntual(valor, posición), la posición es respecto al nudo izq. del tramo.
    #M = MomentoConcentrado(valor, posición), la posición es respecto al nudo izq. del tramo.

        q = CargaDistribuida(8000,0,6)
        P = CargaPuntual(12000, 4)
         cargas = [
             [q],  # carga en tramo 1
             [P]  # carga en tramo 2
        ]


    #Los grados de libertad restringidos son:
        gdlRest = []
    #En general.
        for i in range(b):
            gdlRest.append(2*i)
    #Extremo izquierdo.
        if apoyoIzq == 0: #empotramiento
            gdlRest.insert(1, 1)
        elif apoyoIzq == 1: #restricción al giro
            gdlRest[0] = 1
        elif apoyoIzq == 3: #voladizo
            del gdlRest[0]
        else: #apoyo de segundo grado
            pass
    #Extremo derecho.
        if apoyoDer == 0: #empotramiento
            gdlRest.append(2*b)
            gdlRest.append(2*b + 1)
        elif apoyoDer == 1: #restricción al giro
            gdlRest.append(2*b + 1)
        elif apoyoDer == 2: #apoyo de segundo género
            gdlRest.append(2*b)
        else: #voladizo
            pass

    Cortantes = []
    for i in range(b): #para cada tramo

    #Cortantes como vigas sin apoyo
        Q0 = np.zeros(numS)
    for j in range(len(cargas[i])): #considera todas las cargas de cada tramo
        m = 0 #para enumerar las secciones
    for x in Xt[i]: #recorre las secciones
        Q0[m] += cargas[i][j].FQ(x, Tramo[i].L)
        m += 1
    #Cortantes en el extremo, obtenidos del cálculo
        Q1 = F[i][0]

    #Momento total
    Cortantes.append(Q0 + Q1)

    Flectores = []
        for i in range(b): #para cada tramo

    #Momentos como tramos simplemente apoyado
            M0 = np.zeros(numS)
        for j in range(len(cargas[i])): #considera todas las cargas de cada tramo
            m = 0 #para enumerar las secciones
        for x in Xt[i]: #recorre las secciones
            M0[m] += cargas[i][j].MF(x, Tramo[i].L)
            m += 1

    #Momentos debidos a los empotramientos o a la continuidad de la viga
            M1 = -F[i][1] + (F[i][3] + F[i][1]) / Tramo[i].L * Xt[i]

    #Momento total
    Flectores.append(M0 + M1)