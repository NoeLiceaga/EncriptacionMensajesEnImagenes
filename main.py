import math
import tkinter as tk
from tkinter.ttk import Style
from tkinter import filedialog
import numpy as np
import cv2 as cv2

listaLetras = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q',
               'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ')

# Números equivalentes a los caracteres usados MODULO 38
listaNum = (65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 143, 79, 80, 81, 82,
            83, 84, 85, 86, 87, 88, 89, 90, 159, 123, 163, 176, 116, 169, 139, 180, 167, 189, 43)
llave = np.array([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
code = []
cod2 = []
ar = []
matriz_cifrada = []
coordenadas = []
bitsExtra = 0
filasMI = 0
columnasMI = 0
longuitudBits = ""

class redimensionamiento:#Esta calse la usamos para poder saber de que tamaño vamos a extraer la matriz de imagen, siempre sera de 5xN o 3xN
    matriz = []
    filas = 0
    columnas = 0
    dim = 0
    ar = []
    def __init__(self,matriz,dim):
        self.matriz = matriz
        self.dim = dim
        
    def redimensionaMatrizImagenObtenida(self):
        self.ar = np.empty((self.dim, 0), int)
        aux = []
        self.matriz.reverse()
        bandera = 1
        inicio = len(self.matriz)
        fin = len(self.matriz)-self.dim
        while bandera == 1:
            for i in range(inicio, fin, -1):
                aux.append(int(self.matriz[i-1]))
                self.matriz.pop(i-1)
            if(self.dim==5):
                a = aux[0]
                b = aux[1]
                c = aux[2]
                d = aux[3]
                e = aux[4]
                self.ar = np.append(self.ar, np.array([[a], [b], [c], [d], [e]]), axis=1)
            else:
                a = aux[0]
                b = aux[1]
                c = aux[2]
                self.ar = np.append(self.ar, np.array([[a], [b], [c]]), axis=1)

            if(len(self.matriz) == 0):
                bandera = 0

            inicio = len(self.matriz)
            fin = len(self.matriz)-self.dim
            aux.clear()
            
        self.filas,self.columnas = self.ar.shape
        print("Los numeros esta acomodados en columnas, pero aqui solo hacemos esto para obtener las dimensiones necesarias para la matriz imagen"+
              " por lo que nunca usamos esta matriz")
        print("Dimension fila:", self.dim)
        print("Matriz redim: ",self.ar)
        print("Filas: ",self.filas)
        print("Columnas: ",self.columnas)

    
        
def cifrar():
    global filasMI,columnasMI,longuitudBits,bitsExtra
    longuitudBits = ""
    code.remove
    valores = entry.get().lower()
    for chr in valores:
        for i in range(0, len(listaLetras)):
            if chr == listaLetras[i]:
                code.append(listaNum[i])

    if len(valores) < 3*math.ceil(len(valores)/3):
        for missing in range(3*math.ceil(len(valores)/3)-len(valores)):
            code.append(43)
    print(code)
    matrizMensaje = redimensionamiento(code,3)
    matrizMensaje.redimensionaMatrizImagenObtenida()
    mensaje = matrizMensaje.ar
    cifrarMensaje(mensaje)


def crearMatrizMensaje():
    ar = np.empty((3, 0), int)
    code.reverse()
    bandera = 1
    inicio = len(code)
    fin = len(code)-3
    while bandera == 1:
        for i in range(inicio, fin, -1):
            cod2.append(code[i-1])
            code.pop(i-1)

        a = cod2[0]
        b = cod2[1]
        c = cod2[2]
        ar = np.append(ar, np.array([[a], [b], [c]]), axis=1)

        if(len(code) == 0):
            bandera = 0

        inicio = len(code)
        fin = len(code)-3
        cod2.clear()
    print("Matriz a cifrar: ")
    print(ar)
    return ar


def cifrarMensaje(mensaje):
    arr = []
    aux = []
    lista_binario = []
    
    global matriz_cifrada
    matriz_cifrada = np.dot(llave, mensaje)
    print("PRODUCTO MATRICIAL")
    print(matriz_cifrada)
    matriz_cifrada = np.mod(matriz_cifrada, 38)
    print("MATRIZ CIFRADA")
    print(matriz_cifrada)
    
    #CONVERTIMOS LA MATRIZ CIFRADA A BINARIO
    arr = np.asarray(matriz_cifrada)
    filas,columnas = arr.shape
    for x in range(filas):
        for y in range(columnas):
            aux.append(str(int(format(arr[x][y],"b"))))
        lista_binario.append(aux.copy())
        aux.clear()
        
    print(lista_binario)
    obtenDimensionMatrizImagen( np.asarray(lista_binario))
    
def obtenDimensionMatrizImagen(listBinario):
    filas,columnas = listBinario.shape
    pruebaTM = []
    global longuitudBits
    global bitsExtra,filasMI,columnasMI
    print(filas,columnas)
    for x in range(filas):
        for y in range(columnas):
            longuitudBits += listBinario[x][y]
    print(longuitudBits)
    
    for x in range(len(longuitudBits)):
        pruebaTM.append(longuitudBits[x])
                
    if len(longuitudBits) <5*math.ceil(len(longuitudBits)/5):
        for missing in range(5*math.ceil(len(longuitudBits)/5)-len(longuitudBits)):
            bitsExtra +=1
            pruebaTM.append('0')
    print(pruebaTM)
    
    matriz = redimensionamiento(pruebaTM,5)
    matriz.redimensionaMatrizImagenObtenida()
    filasMI,columnasMI = matriz.filas,matriz.columnas
    
    
def abreSeleccionImg():
    array = []
    if filasMI !=0:
        filename = filedialog.askopenfilename(
            initialdir="/imgs", title="Selecciona una imagen", filetypes=(
                ("png files", "*.png"),
                ("jpg files", "*.jpg"),
                ("svg files", "*.svg"),
                ("jpeg files","*.jpeg")
            ))
        img = cv2.imread(filename,1)
        cv2.imshow("Imagen",img)
        cv2.setMouseCallback("Imagen", obtenCoordenadas)
        cv2.waitKey(0)
        texto = "Coordenadas" + str(coordenadas) 
        label = tk.Label(text=texto,
                         justify="center", font=fuente)
        label.place(y=20, x=250)
        
        region = img[coordenadas[0]:coordenadas[0]+filasMI,coordenadas[1]:coordenadas[1]+columnasMI,2]
        array = bitMenosSignificativo(region)
        array = np.asarray(array)
        x,y = array.shape
        array = array.tolist()
        for x1 in range(x):
            for y1 in range(y):
                img[coordenadas[0]+x1,coordenadas[1]+y1,2] = array[x1][y1]
                
        bol = cv2.imwrite(filename,img)
        if bol:
            print("si")
        print("Matriz Cifrada y Guardada")
    else:
        print("Cifre antes el mensaje")
    
def bitMenosSignificativo(region):
    aux = []
    regionBinario = []
    arr = np.asarray(region)
    contador =0
    filas,columnas = region.shape
    print("Matriz Region: ",arr)
    for x in range(filas):
        for y in range(columnas):
            aux.append(str(int(format(arr[x][y],"b"))))
        regionBinario.append(aux.copy())
        aux.clear()
    print(regionBinario)
    print("BitsExtra:", bitsExtra)
    filas,columnas = np.asarray(regionBinario).shape
    for s in range(filas):
        for d in range(columnas):
            cifra = regionBinario[s][d]
            ultimo = cifra[-1]
            if(contador == len(longuitudBits)):
                break
            else:
                reemplazo = list(regionBinario[s][d])
                reemplazo[-1] = longuitudBits[contador]
                nuevo = "".join(reemplazo)
            print("Cifra: ",cifra,
                "UltimoBit: ",ultimo,
                "Bit de Reemplazo: ",longuitudBits[contador],
                "Reemplazo: ",nuevo)
            regionBinario[s][d] = nuevo
            reemplazo.clear()
            contador+=1
    
    print("Matriz Modificada: ")
    print(regionBinario)
    array = deBinarioABase10(regionBinario)
    
    return array
    
    
def deBinarioABase10(M):
    arr = np.asarray(M)
    filas, columnas = arr.shape
    for x in range(filas):
        for y in range(columnas):
            arr[x][y] = int(str(arr[x][y]),2)
    print(bitsExtra)
    print("Matriz Modificada Base10: ")
    print(arr)
    return arr
    
    
def obtenCoordenadas(event,x,y,flags,*userdata):
    global coordenadas
    if event == cv2.EVENT_LBUTTONDOWN:
        coordenadas= (x,y)
        cv2.destroyAllWindows()

        
        
    
root = tk.Tk()
s = Style()
s.configure('TButton', font=(20, 'bold'), borderwidht='4')
fuente = ('Roboto', 10)
root.title("Proyecto Encriptacion")
root.config(height=300, width=400)

entry = tk.Entry(root)
entry.place(height=100, width=300, y=100, x=10)

label = tk.Label(text="Ingresa el texto",
                 justify="center", font=fuente)
label.place(y=70, x=10)
boton = tk.Button(root, text="Cifrar", font=fuente,
                  command=cifrar)
boton.place(width=50, y=220, x=10)

botonImg = tk.Button(root,text="Seleccion Imagen",font=fuente, command=abreSeleccionImg)
botonImg.place(width=150, y=20, x=10)

root.mainloop()
