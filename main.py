import math
import tkinter as tk
from tkinter.ttk import Style
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import cv2 as cv2
import customtkinter
from customtkinter import StringVar

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

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    gapx=20
    gapy=20
    label_font_size = 16
    font_family = 'Roboto'
    #Variables that i use as a global variables, it works for cipher tasks
    mensaje = ""
    region = ""
    regionBinario = []
    def __init__(self):
        super().__init__()
        coor_sting = StringVar(master=self,value="Coordenadas: (Imagen sin seleccionar)")
        entry_label = StringVar(master=self)
        #Configure Window
        self.title('Proyecto')
        self.geometry(f"{500}x{500}")
        self.maxsize(500,500)
        self.minsize(500,500)
        self.iconbitmap('icons8-python-16.ico')
        #self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        #Create the GUI
        self.main_frame = customtkinter.CTkFrame(self, width=400)
        self.main_frame.grid(row=0, column=0, padx=self.gapx, pady=self.gapy, sticky='nsew')
        self.main_label = customtkinter.CTkLabel(self.main_frame, text="Ingresa el texto", font=customtkinter.CTkFont(size=self.label_font_size, weight="bold", family=self.font_family))
        self.main_label.grid(row=0, column=0, sticky='nsew', padx=self.gapx, pady=self.gapy, columnspan=3)
        self.main_entry = customtkinter.CTkEntry(self.main_frame, width=400, height=100,font=customtkinter.CTkFont(size=self.label_font_size, family=self.font_family), textvariable=entry_label)
        self.main_entry.grid(row=1, column=0,padx=self.gapx, pady=self.gapy,sticky='nsew', rowspan=2, columnspan=3)
        self.main_button_cipher = customtkinter.CTkButton(self.main_frame, text='Cifrar', font=customtkinter.CTkFont(size=self.label_font_size, weight="bold", family=self.font_family), fg_color='red', state='disabled', command=self.press_button, hover_color='#790001')
        self.main_button_cipher.grid(row=3 , column=0,padx=self.gapx,sticky='nsew', columnspan=3)
        self.main_button_image = customtkinter.CTkButton(self.main_frame, text='Selecciona Imagen', font=customtkinter.CTkFont(size=self.label_font_size, weight="bold", family=self.font_family), fg_color='green', state='disabled', command=self.imageSelection, hover_color='#2b472b')
        self.main_button_image.grid(row=4 , column=0, padx=self.gapx, pady=self.gapy,sticky='nsew', columnspan=3)
        #Label that contains the coordinates where the message was encripted
        self.main_label_coordinates = customtkinter.CTkLabel(self.main_frame, text="Coordenadas: (Imagen sin Seleccionar)", font=customtkinter.CTkFont(size=self.label_font_size, family=self.font_family))
        self.main_label_coordinates.grid(row=5, column=1, padx=self.gapx, pady=self.gapy,sticky='nsew')
        self.main_button_clear = customtkinter.CTkButton(self.main_frame, text='LIMPIAR', font=customtkinter.CTkFont(size=self.label_font_size, weight="bold", family=self.font_family), state='disabled',command=self.clean)
        self.main_button_clear.grid(row=6 , column=0,padx=self.gapx, pady=(0,self.gapy), sticky='nsew', columnspan=3)
        
        
        entry_label.trace("w", lambda name, index, mode, sv=entry_label: self.check_entry())

    def press_button(self):
        self.cifrar()
        self.check_cipher()
        
    def imageSelection(self):
        self.abreSeleccionImg()
        self.main_button_clear.configure(state='normal')

    def check_entry(self):
        if self.main_entry.get() != "":
            self.main_button_cipher.configure(state="normal")
        else:
            self.main_button_cipher.configure(state="disabled")

    def clean(self):
        self.main_entry.delete(0,'end')
        self.main_button_cipher.configure(state='disabled')
        self.main_button_image.configure(state='disabled')
        self.main_button_clear.configure(state='disabled')
        self.main_label_coordinates.configure(text = "Coordenadas: (Imagen sin Seleccionar)")
        self.mensaje = ""
        self.region = ""
        self.regionBinario = []

        global code, cod2, ar, matriz_cifrada, coordenadas, bitsExtra, filasMI, columnasMI,longuitudBits
        code = []
        cod2 = []
        ar = []
        matriz_cifrada = []
        coordenadas = []
        bitsExtra = 0
        filasMI = 0
        columnasMI = 0
        longuitudBits = ""
        

    def check_cipher(self):
        if(len(matriz_cifrada)>0):
            self.main_button_image.configure(state='normal')
        else:
            self.main_button_image.configure(state='disabled')

    def cifrar(self):
        global filasMI,columnasMI,longuitudBits,bitsExtra
        longuitudBits = ""
        code.remove
        valores = self.main_entry.get().lower()

        for x in valores:
            try:
                valor = listaLetras.index(x)
            except:
                messagebox.showinfo("Error","Ingresaste un caracter no permitido")
                self.clean()
                return

        for chr in valores:
            for i in range(0, len(listaLetras)):
                if chr == listaLetras[i]:
                    code.append(listaNum[i])

        if len(valores) < 3*math.ceil(len(valores)/3):
            for missing in range(3*math.ceil(len(valores)/3)-len(valores)):
                code.append(43)
        print(code)
        matrizMensaje = Redimensionamiento(code,3)
        matrizMensaje.redimensionaMatrizImagenObtenida()
        self.mensaje = matrizMensaje.ar
        self.cifrarMensaje()


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


    def cifrarMensaje(self):
        arr = []
        aux = []
        lista_binario = []
        print("dad", self.mensaje)
        global matriz_cifrada
        matriz_cifrada = np.dot(llave, self.mensaje)
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
        App.obtenDimensionMatrizImagen( np.asarray(lista_binario))
        
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
        
        matriz = Redimensionamiento(pruebaTM,5)
        matriz.redimensionaMatrizImagenObtenida()
        filasMI,columnasMI = matriz.filas,matriz.columnas
        
        
    def abreSeleccionImg(self):
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
            if not img.any():
                messagebox.showerror("Error", "Imagen no seleccionada")
                return
            cv2.setMouseCallback("Imagen", obtenCoordenadas)
            cv2.waitKey(0)
            texto = "Coordenadas" + str(coordenadas)
            self.main_label_coordinates.configure(text=texto)
            self.region = img[coordenadas[0]:coordenadas[0]+filasMI,coordenadas[1]:coordenadas[1]+columnasMI,2]
            array = self.bitMenosSignificativo()
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
        
    def bitMenosSignificativo(self):
        aux = []
        arr = np.asarray(self.region)
        contador =0
        filas,columnas = self.region.shape
        print("Matriz Region: ",arr)
        for x in range(filas):
            for y in range(columnas):
                aux.append(str(int(format(arr[x][y],"b"))))
            self.regionBinario.append(aux.copy())
            aux.clear()
        print(self.regionBinario)
        print("BitsExtra:", bitsExtra)
        filas,columnas = np.asarray(self.regionBinario).shape
        for s in range(filas):
            for d in range(columnas):
                cifra = self.regionBinario[s][d]
                ultimo = cifra[-1]
                if(contador == len(longuitudBits)):
                    break
                else:
                    reemplazo = list(self.regionBinario[s][d])
                    reemplazo[-1] = longuitudBits[contador]
                    nuevo = "".join(reemplazo)
                print("Cifra: ",cifra,
                    "UltimoBit: ",ultimo,
                    "Bit de Reemplazo: ",longuitudBits[contador],
                    "Reemplazo: ",nuevo)
                self.regionBinario[s][d] = nuevo
                reemplazo.clear()
                contador+=1
        
        print("Matriz Modificada: ")
        print(self.regionBinario)
        array = self.deBinarioABase10()
        
        return array
        
        
    def deBinarioABase10(self):
        arr = np.asarray(self.regionBinario)
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


class Redimensionamiento:#Esta calse la usamos para poder saber de que tamaño vamos a extraer la matriz de imagen, siempre sera de 5xN o 3xN
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




if __name__ == "__main__":

    app = App()
    app.mainloop()

