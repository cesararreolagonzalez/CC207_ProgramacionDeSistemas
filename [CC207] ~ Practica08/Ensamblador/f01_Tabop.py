from Ensamblador.f02_Variables import archivoTabop, lineasTabop, listaCodop, diccionario_codop, lista_direccionamientos,SALTO_LINEA, diccionario_direccionamientos

#----------------------------------------------------------------------------------
#    Esta funcion consiste en leer linea a linea el archivo de texto 'tabop.txt'
#    y cada linea leida la guarada en la lista 'archivoTapob' 
#----------------------------------------------------------------------------------
def leer_archivo_tabop():
    #archivoTabop = []
    nombre_archivo = 'tabop.txt'
    modo_lectura   = 'r'
    try:
        with open(nombre_archivo, modo_lectura) as archivo:
            for linea in archivo:
                if(linea != ""):
                    if(linea[-1] == SALTO_LINEA):
                        linea = linea[:-1]
                    archivoTabop.append(linea)
            archivo.close()
    except:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo)

#-----------------------------------------------------------------------------------
#    Esta funcion consiste en crear el diccionario de codigos de operacion a partir
#    de la lista 'archivoTapob' y relacionar sus direccionamientos correspondientes.
#-----------------------------------------------------------------------------------
def leer_lineas_tabop():
    # Cada linea de texto se divide en elementos individuales
    for linea in archivoTabop:
        lineasTabop.append(linea.split('|'))
        
    #Todos el contenido de 'lista_codop' se pasan a un diccionario
    # para eliminar valores repetidos
    for linea in lineasTabop:
        listaCodop.append(linea[0])
    diccionario_codop = dict.fromkeys(listaCodop)
    
    #Se relaciona cada lista de listas con su llave correspondiente
    for llave in diccionario_codop:
        relacionar_direccionamiento(llave)
        
        
#----------------------------------------------------------------------------------
#    Esta funcion consiste en agregarle una lista de listas de los direccionamientos
#    disponibles para cada codigo de operacion
#----------------------------------------------------------------------------------
def relacionar_direccionamiento(llave):
    lista = []
    for linea in lineasTabop:
        if(linea[0] == llave):
            lista.append(linea)
    diccionario_codop[llave] = lista
    
#----------------------------------------------------------------------------------
#    Esta funcion busca si el codigo de operacion existe en el tabop y devuelve 
#    una cadena con sus correspondientes direccionamientos. 
#    Si no existe no devuelve nada.
#----------------------------------------------------------------------------------
def direccionamiento_particular_tabop(codop, diccionario_codop, lista_direccionamientos):
    #print(diccionario_codop)
    direccionamientos = []
    lista_informacion = []
    totalDireccionamiento = ''
    contador = 0
    try:
        for lista in (diccionario_codop[codop.upper()]):
            direccionamientos.append(lista[2])
            lista_informacion.append(lista[3:7])
            lista_direccionamientos.append(lista[2:7])
        try:
            direccionamientos.reverse()  
            while(direccionamientos != IndexError):   
                direccionamiento = ''
                direccionamiento += diccionario_direccionamientos[direccionamientos.pop()] + '\t'
                if(len(direccionamientos) > 1):
                    if(len(direccionamiento) > 15 and len(direccionamiento) < 30):
                        direccionamiento += '\t\t'
                    elif(len(direccionamiento) > 5 and len(direccionamiento) < 15):
                        direccionamiento += '\t\t\t'
                for elemento in (lista_informacion[contador]):
                    direccionamiento += elemento + '\t'
                contador +=1
                totalDireccionamiento += direccionamiento + '\n' + '\t\t    '
        except: None
    except: None
    return totalDireccionamiento