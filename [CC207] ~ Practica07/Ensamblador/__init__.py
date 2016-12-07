#------------------------------------------------------------------------------------------------
# Taller de Programacion de Sistemas
#------------------------------------------------------------------------------------------------
from Ensamblador.f01_Tabop import *
from Ensamblador.f02_Variables import *
from Ensamblador.f03_Ensamblador import *

if __name__ == '__main__':
    #--------------------------------------------------------------------------------------------
    # Se lee el archivo tabop linea a linea y se guarda su contenido en la lista 'archivoTapob'.
    #--------------------------------------------------------------------------------------------
    leer_archivo_tabop()
    #--------------------------------------------------------------------------------------------
    # Se crea el diccionadio de codigos de operacion (llave), cuyo valor consiste 
    # en una lista de listas de sus direccionamientos correspondientes.
    #--------------------------------------------------------------------------------------------
    leer_lineas_tabop()
    #--------------------------------------------------------------------------------------------
    # Se lee el archivo que contiene las instrucciones en lenguaje ensamblador linea a linea 
    # y se guarda su contenido en la lista 'archivoEnsamblador'.
    #--------------------------------------------------------------------------------------------
    leer_archivo_ensamblador('IDXC.txt')
    #-------------------------------------------------------------------------------------------
    # Finalmente se evalua una a una las lineas de instrucciones en ensamblador
    #--------------------------------------------------------------------------------------------
    evaluar_lineas_ensamblador(diccionario_codop)