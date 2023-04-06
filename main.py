import dearpygui.dearpygui as dpg
import math
import numpy as np
dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()


class Application():
    """"VARIABLES DE CLASE"""
    #CARACTERES MODULO 38
    caracter = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9',' ')
    numeros =  (21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 19, 29, 39, 49, 59, 18)
    texto_ingresado = ""
    code = []
    matrizC = []
    key = np.array([[1,0,1], [0,2,1], [0,1,3]])
    def __init__(self) -> None:
        pass

    def button_callback(sender, app_data, user_data):
        if user_data == "":
            dpg.configure_item(encriptar, enabled=False)
        else:
            dpg.configure_item(encriptar, enabled=True)

    def call_back(sender, app_data, user_data):
        print('hola')

    def get_texto_ingresado(self, sender, app_data, user_data):
        if len(self.matrizC) == 0:
            self.texto_ingresado = dpg.get_value(input)
            for letra in self.texto_ingresado:
                for i in range(0, len(self.caracter)):
                    if letra == self.caracter[i]:
                        self.code.append(self.numeros[i])
            self.multiplicar_llave_mensaje()

    def multiplicar_llave_mensaje(self):
        if len(self.texto_ingresado) < 3*math.ceil(len(self.texto_ingresado)/3):
            for missing in range((3*math.ceil(len(self.texto_ingresado)/3))-len(self.texto_ingresado)):
                self.code.append(18)

        print('LETRAS CAMBIADAS POR SU EQUIVALENTE: ', self.code)
        self.matrizC = np.asarray(self.code)
        print('Shape: ', self.matrizC.shape)
        self.matrizC = np.reshape(self.matrizC, (math.ceil(len(self.texto_ingresado)/3),3))
        self.matrizC = np.transpose(self.matrizC)
        # print(self.matrizC)
        print(self.key.shape)
        self.matrizC = np.dot(self.key,self.matrizC)
    
        print("PRODUCTO MATRICIAL MENSAJE PUNTO LLAVE: \n",self.matrizC)
        self.matrizC = np.mod(self.matrizC, 38)
        print('MATRIZ CIFRADA CON MODULO 38: \n', self.matrizC)

with dpg.window(label='Proyecto', width=430, height=400):
    dpg.add_text("INGRESE EL TEXTO A ENCRIPTAR")
    input = dpg.add_input_text(multiline=True, height=150, width=400, uppercase=True, callback=Application().button_callback)
    with dpg.group():
        encriptar = dpg.add_button(label="Encriptar", width=400, enabled=False, id='encriptar', callback=Application().get_texto_ingresado)

dpg.create_viewport(title='Inicio', width=430, height=400, resizable=False)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
