import math
import tkinter as tk
from tkinter.ttk import Style

listaLetras = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q',
               'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ')

# Números equivalentes a los caracteres usados
listaNum = (65,66,67,68,69,70,71,72,73,74,75,76,77,78,143,79,80,81,82,83,84,85,86,87,88,89,90,159,123,163,176,116,169,139,180,167,189,43)

code = []
cod2 = []

def cifrar():
    code.remove
    valores = entry.get()
    
    for chr in valores:
        for i in range(0, len(listaLetras)):
            if chr == listaLetras[i]:
                code.append(listaNum[i])


    if len(valores) < 3*math.ceil(len(valores)/3):
        for missing in range(3*math.ceil(len(valores)/3)-len(valores)):
            code.append(43)
    print(code)

root = tk.Tk()
s = Style()
s.configure('TButton', font=(20, 'bold'), borderwidht='4')
fuente = ('Verdana', 10)
root.title("Proyecto Encriptacion")
root.config(height=300, width=320)
entry = tk.Entry(root)
entry.place(height=100, width=300, y=50, x=10)
label = tk.Label(text="Ingresa el texto",
                 justify="center", font=fuente)
label.place(y=20, x=10)
boton = tk.Button(root, text="Cifrar", font=fuente, command=cifrar)
boton.place(width=50, y=200, x=130)
root.mainloop()
