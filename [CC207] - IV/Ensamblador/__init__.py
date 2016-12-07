# -*- encoding: utf-8 -*-

import re
import os
import shutil

# ------------------------------
#         CONSTANTES
# ------------------------------
A_MAYUSCULA = 65
Z_MAYUSCULA = 90
A_MINUSCULA = 97
Z_MINUSCULA = 122
PUNTO = '.'
NUMERO_1 = 48
NUMERO_9 = 57
GUION_BAJO = 95
LONGITUD_MAX_ETIQUETA = 8
LONGITUD_MAX_CODOP = 5
PUNTOS_MAXIMOS = 1
NO_REPETIR_MENSAJE = 1
SALTO_LINEA = '\n'
PUNTO_COMA = ';'
ESPACIO    = ' '
TABULADOR = '\t'
ANADIR_FINAL = 'w+'
MODO_LECTURA   = 'r'
nombre_archivo_tabsim = 'tabsim.txt'
# ------------------------------
#         BANDERAS
# ------------------------------
EXISTE_END = False
EXISTE_END = False
EXISTE_ORG = False
ASM_LEIDO_EXITOSAMENTE = False
INSTRUCCION_END_REPETIDA = False
ARCHIVO_LISTADO_LEIDO = False
# ------------------------------
#         LISTAS
# ------------------------------
archivoEnsamblador = []      #Almacena las lineas que lee del archivo 'ASM'
archivoTabop = []            #Almacena las lineas que lee del archivo 'tabop'
lineasTabop = []             #Almacena elementos separados de cada linea de archivoTabop
listaCodop = []              #Almacena los codigos de operacion de cada linea de 'lineasTabop'
lista_direccionamientos = []
archivo_listado = []         #Almacena las linas que lee del archivo 'LST'
informacion_tabla_simbolos  = []         #Almacena las lineas que lee del archivo 'tabsim'
lista_etiquetas = []

archivo_listado = []    #Almacena las lineas que se leen del archivo de listado
tabla_simbolos  = []    #Almacena las lineas que se leen de la tabla de simbolos

temporal_archivo_listado = []   #Almacena las lineas que se van a escribir en el archivo de listado
temporal_archivo_tabsim  = []   #Almacena las lineas que se van a escribir en el archivo de tabla de simbolos
# ------------------------------
#        DICCIONARIOS
# ------------------------------
diccionario_direccionamientos = {'INH':'Inherente', 'DIR':'Directo','INM':'Inmediato','EXT':'Extendido',
                                 'REL':'Relativo','IDX':'Indizado de 5 bits','IDX1':'Indizado de 9 bits',
                                 'IDX2':'Indizado de 16 bits','[IDX2]':'Indizado indirecto de 16 bits',
                                 '[D,IDX]':'Indizado indirecto aculumador'}
diccionario_codop = {}      #Almacena el contenido de la lista 'archivoTabop' ordenada en clave (instruccion) y contenido (direccionamiento)
# ------------------------------
#            CADENAS
# ------------------------------
totalDireccionamiento = ''
nombre_archivo_asm = ''
nombre_archivo_temporal = ''
resultado_evaluacion = ''
nombre_directorio = ''
nombre_archivo_objeto = ''
# ------------------------------
#           CONTADORES
# ------------------------------
DIR_INIC = 0
CONTLOC  = 0
codigoMaquina = 0
contador   = 0

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#                        T        A        B        O        P
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


#----------------------------------------------------------------------------------
#    Esta funcion consiste en leer linea a linea el archivo de texto 'tabop.txt'
#    y cada linea leida la guarada en la lista 'archivoTapob' 
#----------------------------------------------------------------------------------
def leer_archivo_tabop():
    nombre_archivo = 'tabop.txt'
    try:
        with open(nombre_archivo, MODO_LECTURA) as archivo:
            for linea in archivo:
                longitud_linea = len(linea)
                if(longitud_linea > 1):
                    if(linea[-1] == SALTO_LINEA):
                        linea = linea[:-1]
                    archivoTabop.append(linea)
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
def direccionamiento_particular_tabop(codop):
    global lista_direccionamientos
    
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


#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#                                    A        S        M
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#----------------------------------------------------------------------------------
#    Esta funcion consiste en leer linea a linea el archivo de texto que contiene
#    las instrucciones en lenguaje ensabmlador, 
#    y cada linea leida la guarada en la lista 'archivoEnsamblador' 
#----------------------------------------------------------------------------------
def leer_archivo_ensamblador(nombre_archivo):
    global ASM_LEIDO_EXITOSAMENTE
    global nombre_archivo_asm
    global nombre_directorio
    
    nombre_archivo_asm = nombre_archivo
    nombre_directorio = nombre_archivo_asm.split('.')[0].upper()
    try:
        with open(nombre_archivo, MODO_LECTURA) as archivo:
            for linea in archivo:
                estaVacia = evaluar_lineas_sin_contenido(linea)
                if(not estaVacia):
                    archivoEnsamblador.append(linea)
                    
        ASM_LEIDO_EXITOSAMENTE = True
    except:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo)
        
#-----------------------------------------------------------------------------------------
#    Esta funcion consiste en pasar a evaluar cada linea de la lista 'archivoEnsamblador' 
#    las instrucciones en lenguaje ensamblador, saltandose las lineas vacias 
#-----------------------------------------------------------------------------------------
def evaluar_contenido_archivo_ensamblador():
    global EXISTE_END
    global nombre_archivo_temporal
    global nombre_archivo_tabsim
    global nombre_archivo_objeto
    
    etiqueta   = ''
    codop      = ''
    operando   = ''
    
    nombre_archivo_temporal = nombre_archivo_asm.split('.')[0].upper()+'tmp.txt'
    
    if re.search('asm', nombre_archivo_temporal, re.IGNORECASE):
        nombre_archivo_temporal = re.compile("asm").sub('',nombre_archivo_temporal)

    ##
    for linea in archivoEnsamblador:
        estaVacia = evaluar_lineas_sin_contenido(linea)
        if(not estaVacia):
            if(INSTRUCCION_END_REPETIDA):
                print('\n\n:::::::::::::::::::::: ADVERTENCIA :::::::::::::::::::::::\n    ~  Las siguientes lineas no seran evaluadas  ~\n\n')
            resultado_evaluacion = identificando_partes_linea_ensamblador(linea)
            
            etiqueta     = resultado_evaluacion[0]
            codop        = resultado_evaluacion[1]
            operando     = resultado_evaluacion[2]
            esComentario = resultado_evaluacion[3]
            
            if(not EXISTE_END):
                if(not esComentario):
                    evaluando_partes_linea_ensamblador(etiqueta,codop,operando)
            elif(not esComentario):
                print('ETIQUETA         =  '+etiqueta)  
                print('CODOP            =  '+codop)
                print('OPERANDO         =  '+operando)
                print('-'*100)
    ##
    
    # Al finalizar, si el 'END' no se encontro en el archivo, se marca error
    if(not EXISTE_END):
        print('ERROR DE CODIGO DE OPERACION: No se encontro el END')
    print('\nDIR_INIC = %d ::: CONTLOC = %d\nLongitud en bytes = %d' %(DIR_INIC, CONTLOC, (CONTLOC-DIR_INIC)))
    
    
    if(not os.path.exists(nombre_directorio)): 
        os.mkdir(nombre_directorio)
    else: 
        for root, dirs, files in os.walk(nombre_directorio):
            for archivo in files:
                os.remove(os.path.join(root,archivo))
            for directorios in dirs:
                os.remove(os.path.join(root,directorios))
        os.removedirs(nombre_directorio)
        os.mkdir(nombre_directorio)
        
    nuevo_archivo_temporal = os.path.abspath(nombre_directorio)+'\\'+nombre_archivo_temporal
    nuevo_archivo_tabsim   = os.path.abspath(nombre_directorio)+'\\'+nombre_archivo_tabsim
    
    nombre_archivo_objeto  = os.path.abspath(nombre_directorio)+'\\'+nombre_archivo_asm.split('.')[0].upper()+'.obj'
    nombre_archivo_temporal = nuevo_archivo_temporal
    nombre_archivo_tabsim   = nuevo_archivo_tabsim
    
    #    Con esta forma sólo se abre una vez el archivo
    
    try:
        archivo_temporal = open(nombre_archivo_temporal, 'w+')
        contador_lineas = 0
        for linea in temporal_archivo_listado:
            if(contador_lineas+1 == len(temporal_archivo_listado)):
                archivo_temporal.write(linea)
            else:
                linea += '\n'
                archivo_temporal.write(linea)
            contador_lineas += 1
        archivo_temporal.close()
    except: print('ERROR: Hubo un problema con el archivo de listado')
    
    try:
        archivo_tabsim = open(nombre_archivo_tabsim,   'w+')
        
        contador_lineas = 0
        for linea in temporal_archivo_tabsim:
            if(contador_lineas+1 == len(temporal_archivo_tabsim)):
                archivo_tabsim.write(linea)
            else:
                linea += '\n'
                archivo_tabsim.write(linea)
            contador_lineas += 1
        archivo_tabsim.close()
    except: print('ERROR: Hubo un problema con el archivo tabsim')
    
    #os.system('mkdir '+nombre_directorio)
    #shutil.copy(nombre_archivo_temporal, nombre_directorio)
    #shutil.copy(nombre_archivo_tabsim, nombre_directorio)
    
    
#-----------------------------------------------------------------------------------------
#    Esta funcion consiste en identificar si la linea es comentario o por el contrario,
#    identificar su ETIQUETA, CODIGO DE OPERACION y OPERANDO
#-----------------------------------------------------------------------------------------
def identificando_partes_linea_ensamblador(linea):
    global CONTLOC
    global DIR_INIC
    global lista_etiquetas
    
    etiqueta   = ''
    codop      = ''
    operando   = ''
    esComentario = False
    
    posicion     = 0
    
    etiquetaCompletada = False
    codopCompletado    = False
    
    if(linea[0] != SALTO_LINEA):
        if(linea[0] == PUNTO_COMA):
            print('COMENTARIO')
            print('-'*100)
            esComentario = True
        else:
            while(len(linea) > posicion and not etiquetaCompletada):
                caracter = linea[posicion]
                if(caracter != SALTO_LINEA and caracter != ESPACIO and caracter != TABULADOR):
                    etiqueta += caracter
                    posicion += 1
                    if(posicion >= len(linea)):
                        codop = 'NULL'
                        codopCompletado = True
                        operando = 'NULL'
                else:
                    etiquetaCompletada = True
                    while(linea[posicion] == ESPACIO or linea[posicion] == TABULADOR): 
                        posicion +=1 
                    if(caracter == '\n'):
                        codop = 'NULL'
                        codopCompletado = True
                        operando = 'NULL'
                    if(len(etiqueta) == 0):
                        etiqueta = 'NULL'
            while(len(linea) > posicion and not codopCompletado):
                caracter = linea[posicion]
                if(caracter != SALTO_LINEA and caracter != ESPACIO and caracter != TABULADOR):
                    codop += caracter
                    posicion += 1
                    if(posicion >= len(linea)):
                        operando = 'NULL'
                else:
                    codopCompletado = True
                    while(linea[posicion] == ESPACIO or linea[posicion] == TABULADOR):  
                        posicion +=1 
                    caracter = linea[posicion]
                    if(caracter == SALTO_LINEA):
                        operando = 'NULL'
                    if(len(codop) == 0):
                        codop = 'NULL'
            while(len(linea) > posicion):
                caracter = linea[posicion]
                if(caracter != SALTO_LINEA):
                    operando += caracter
                posicion += 1
                
    return etiqueta,codop,operando,esComentario

    
def evaluando_partes_linea_ensamblador(etiqueta,codop,operando):
    global EXISTE_END
    global EXISTE_ORG  
    global DIR_INIC
    global CONTLOC
    global INSTRUCCION_END_REPETIDA
    global temporal_archivo_listado
    global temporal_archivo_tabsim
    
    resultado_evaluacion = ''
    ERROR_ETIQUETA = False
    codopValido    = False
     
    bytesTotales = 0
    
    ##########################################
    print('ETIQUETA         =  '+etiqueta)
    ##########################################
    #--------------------------------------------------------------------------------------------------------------
    if(re.match('ORG|END', codop, re.IGNORECASE) and etiqueta != 'NULL'):
        print('\t\t    ERROR: La directiva %s no debe tener etiqueta\n' %codop.upper())
        ERROR_ETIQUETA = True
        resultado_evaluacion = 'X'
    elif(codop.upper() == 'EQU' and etiqueta == 'NULL'):
        print('\t\t    ERROR: La directiva %s debe tener etiqueta\n' %codop.upper())
        resultado_evaluacion = 'X'
    else: 
        evaluar_etiqueta(etiqueta)
    #--------------------------------------------------------------------------------------------------------------
    
    ##########################################
    print('CODOP            =  '+codop)
    ##########################################
    
    #--------------------------------------------------------------------------------------------------------------
    
    if(codop.upper() == 'ORG' and EXISTE_ORG):
        print('\t\t    ERROR DE DIRECTIVA: La directiva %s solo debe existir una vez' %codop.upper())
    
    #Si etiqueta_existente END en CODOP
    if(codop.upper() == 'END'):
        if(EXISTE_END):
            INSTRUCCION_END_REPETIDA = True
        else:
            EXISTE_END = True
            if(resultado_evaluacion == ''):
                resultado_evaluacion = 'END'
    #Se evalua el CODOP para encontrar errores
    codopTieneErrores = evaluar_codop(codop)
    
    #Si ni tiene errores, se busca si etiqueta_existente el codop en el tabop
    if(not codopTieneErrores):
        codopValido = existe_codop_en_tabop(codop.upper(), diccionario_codop)  
        
    #--------------------------------------------------------------------------------------------------------------
    
    ##########################################
    print('OPERANDO         =  '+operando)
    ##########################################
    
    #--------------------------------------------------------------------------------------------------------------
    
    #    La directiva ORG solo debe existir una vez y el valor_operando de su operando es la direccion inicial
    
    if(re.match(codop, 'ORG', re.IGNORECASE) and not EXISTE_ORG):
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            DIR_INIC = validar_operando_directo_o_extendido(operando)
            if(DIR_INIC == -1): 
                DIR_INIC = 0
            elif(DIR_INIC > 65535):
                print('\t\t    ERROR DE RANGO: El rango valido para ORG es de 0 a 65535')
                DIR_INIC = 0
        else:
            DIR_INIC = 0
            print('\t\t    ERROR DE OPERANDO: El valor_operando de la directiva ORG debe estar representado en Decimal, Hexadecimal, Octal o Binario y tener un rango de 0 a 65535',DIR_INIC)
        CONTLOC = DIR_INIC
        print('\t\t    La direccion inicial es: ',DIR_INIC)
        EXISTE_ORG = True
        resultado_evaluacion = 'ORG'
    
    #    La directiva END NO debe tener operando
    
    elif(re.match(codop, 'END', re.IGNORECASE) and operando != 'NULL'):
        print('\t\t    ERROR DE OPERANDO: La directiva END no debe tener operando')
        if(resultado_evaluacion == ''):
            resultado_evaluacion = 'X'
    #    DIRECTIVA EQUATE para darle valor a etiquetas
    
    elif(re.match('EQU', codop, re.IGNORECASE)):
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor_operando = validar_operando_directo_o_extendido(operando)
            if(valor_operando >= 0 and valor_operando <= 65535):
                bytesTotales = valor_operando
                if(resultado_evaluacion != 'X'):
                    resultado_evaluacion = 'EQU'
            else:
                ERROR_ETIQUETA = True
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            ERROR_ETIQUETA = True
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper()) 
               
    #    DIRECTIVAS CONSTANTES de 1 byte
     
    elif(re.match('DB|DC.B|FCB', codop, re.IGNORECASE)):
        #---------- 0 a 255 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor_operando = validar_operando_directo_o_extendido(operando)
            if(valor_operando >= 0 and valor_operando <= 255):
                resultado_evaluacion = 'Directiva'
                bytesTotales = 1
            else:
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 255' %codop.upper())
        else:
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())
        
    #    DIRECTIVAS CONSTANTES de 2 byte
            
    elif(re.match('DW|DC.W|FDB', codop, re.IGNORECASE)):
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor_operando = validar_operando_directo_o_extendido(operando)
            if(valor_operando >= 0 and valor_operando <= 65535):
                resultado_evaluacion = 'Directiva'
                bytesTotales = 2
            else:
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())
           
    #    DIRECTIVAS CONSTANTES de caracteres
    
    elif(codop.upper() == 'FCC'):
        if(operando == 'NULL'):
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe ser representado en cualquier caracter ASCII'%codop.upper())
        else:
            if(chr(34) not in operando):
                print('\t\t    ERROR DE SINTAXIS: El operando debe estar representado entre las comillas de apertura y cierre')
            else:
                if(chr(34) == operando[0]):
                    if(chr(34) == (operando[len(operando)-1])):
                        bytesTotales = int(len(operando) )- 2
                        resultado_evaluacion = 'Directiva'
                    else:
                        print('\t\t    ERROR DE SINTAXIS: Falta la comilla de cierre')
                else:
                    print('\t\t    ERROR DE SINTAXIS: Falta la comilla de apertura')
                    
    #    DIRECTIVAS DE RESERVA DE ESPACIO EN MEMORIA de 1 byte en 1 byte
    
    elif(re.match('DS.B|RMB', codop, re.IGNORECASE) or codop.upper() == 'DS'): 
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor_operando = validar_operando_directo_o_extendido(operando)
            if(valor_operando >= 0 and valor_operando <= 65535):
                bytesTotales = valor_operando * 1
                resultado_evaluacion = 'Directiva'
            else:
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper()) 
            
    #    DIRECTIVAS DE RESERVA DE ESPACIO EN MEMORIA de 2 bytes en 2 bytes
    
    elif(re.match('DS.W|RMW', codop, re.IGNORECASE)):
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor_operando = validar_operando_directo_o_extendido(operando)
            if(valor_operando >= 0 and valor_operando <= 65535):
                bytesTotales = (valor_operando * 2)
                resultado_evaluacion = 'Directiva'
            else:
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())     
    
    # El CODOP no es directiva
    
    else:
        if(codop.upper() != 'END' and codopValido):
            totalDireccionamiento = direccionamiento_particular_tabop(codop)
            lista = direccionamiento_correspondiente(operando)
            bytesTotales = lista[0]
            resultado_evaluacion = lista[1]
            if(codopValido):
                codopTieneOperando(codop.upper(), operando)
                print('DIRECCIONAMIENTO = ', totalDireccionamiento)
    #--------------------------------------------------------------------------------------------------------------
    #---------------------------------------------
    # Se muestran los resultados de la evaluacion
    #---------------------------------------------  
    
    valor = ''
    #    Se verifica que no exista la etiqueta en la tabla de simbolos
     
    if(codop.upper() == 'EQU'):
        if(bytesTotales > 65535):
            valor = format(bytesTotales, '05X')
        else:
            valor = format(bytesTotales, '04X')
    else:
        if(CONTLOC > 65535):
            valor = format(CONTLOC, '05X')
        else:
            valor = format(CONTLOC, '04X')
    
    if(etiqueta != 'NULL'):
        etiqueta_existente = False
        for etiqueta_tabsim in lista_etiquetas:
            if(etiqueta.upper() == etiqueta_tabsim.upper()):
                etiqueta_existente = True
                print('\t\t    ERROR DE ETIQUETA: La etiqueta ya existe')
                break
     
        #    Si la etiqueta no existe en la tabla de simbolos se anade
        if(not etiqueta_existente and not ERROR_ETIQUETA):
            lista_etiquetas.append(etiqueta)
             
            #    Etiqueta absoluta
             
            if(re.match(codop,'EQU',re.IGNORECASE)):
                informacion_tabla_simbolos = '%s|%s' %(etiqueta, valor)
             
            #    Etiqueta relativa
             
            else:
                informacion_tabla_simbolos = '%s|%s' %(etiqueta, valor)

            temporal_archivo_tabsim.append(informacion_tabla_simbolos)
             
             
    #    Archivo de Listado
    if(len(resultado_evaluacion) == 0):
        resultado_evaluacion = 'X'
    if(resultado_evaluacion != 'X'):
        informacion_archivo_listado = '%s|%s|%s|%s|%s' %(valor,etiqueta,codop,operando, resultado_evaluacion) #DIR_INIC
        temporal_archivo_listado.append(informacion_archivo_listado)
            
    # Aumenta el contador de localidades
     
    if(bytesTotales > 0 and codop.upper() != 'EQU' and EXISTE_ORG):
        valor_contloc_antes_de_aumentar = CONTLOC
        CONTLOC += bytesTotales
        print('CONTLOC          =  %d + %d = %d' %(valor_contloc_antes_de_aumentar, bytesTotales, CONTLOC))
         
        if(CONTLOC > 65535):
            print('\t\t    ERROR DE CONTLOC: El rango valido es de 0 a 65535')
             
    else:
        print('CONTLOC          =  %d' %CONTLOC)

    print('-'*100)
    
    
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#                                    L        S        T
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def archivo_de_listado():
    global archivo_listado
    global ARCHIVO_LISTADO_LEIDO
    
    try:
        with open(nombre_archivo_temporal, MODO_LECTURA) as archivo:
            for linea in archivo:
                if(len(linea) > 1):
                    archivo_listado.append(linea.split('|'))
        ARCHIVO_LISTADO_LEIDO = True
    except:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo_temporal)

def archivo_tabsim():
    global tabla_simbolos
    try:
        with open(nombre_archivo_tabsim, MODO_LECTURA) as archivo:
            for linea in archivo:
                if(len(linea) > 1):
                    tabla_simbolos.append(linea.split('|'))
    except:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo_tabsim)
        
def evaluar_lineas_de_listado():
    lineas_archivo_objeto = []
    codigo_maquina = ''
    
    contador_codigos_maquina = 0
    contador = 0
    S0 = '0000'
    S1 = ''
    S1completado = False
    existeORG = False
    codigo_maquina_registro = ''
    direccion = ''
    longitud = 3
    checksum = ''
    for linea in archivo_listado: 
        valor = linea[0]
        etiqueta = linea[1]
        codop = linea[2]
        operando = linea[3]
        direccionamiento = linea[4]
        
        if(direccionamiento[len(direccionamiento)-1:] == '\n'):
            direccionamiento = direccionamiento[:-1]
        
        print('VALOR            =   '+valor)
        print('ETIQUETA         =   '+etiqueta)
        print('CODOP            =   '+codop)
        print('OPERANDO         =   '+operando)
        
        if(direccionamiento.upper() == 'X' and existeORG):
            S1completado = True
        elif(direccionamiento.upper() == 'ORG'):
            existeORG = True
            caracteres_s0 = os.path.abspath(nombre_archivo_asm)[0:2]+os.path.basename(nombre_archivo_asm)
            codigo_ascii_archivo = ''
            for caracter in caracteres_s0:
                codigo_ascii_archivo += hex(ord(caracter))[2:].upper()
                
            direccionS0 = '0000'
            codigo_ascii_archivo += '0A'
            
            checksum = suma_hexadecimal_s1(codigo_ascii_archivo)
            longitudS0 = format(int(len(direccionS0 + codigo_ascii_archivo + checksum)/2),'02X')
            
            S0 = 'S0' + longitudS0 + direccionS0 + codigo_ascii_archivo + checksum
            direccion = valor
            lineas_archivo_objeto.append(S0)
        elif(direccionamiento.upper() == 'END'):
            if(len(codigo_maquina_registro) > 0):
                if(longitud > 0):
                    longitud += int(len(codigo_maquina_registro)/2)
                longitud_hexadecimal = format(longitud,'02X')
                calcular = longitud_hexadecimal + direccion + codigo_maquina_registro
                checksum = suma_hexadecimal_s1(calcular)
                S1 = 'S1%s%s%s%s' %(str(longitud_hexadecimal),direccion,codigo_maquina_registro,checksum)
            
                lineas_archivo_objeto.append(S1)
        elif(direccionamiento.upper() != 'X' and direccionamiento.upper() != 'EQU'):
            codigo_maquina = calcular_codigo_maquina(direccionamiento, codop, operando, contador)
            print('\nCODIGO MAQUINA   =   '+codigo_maquina)
        
        if(direccion == '' and direccionamiento.upper() != 'EQU'):
            direccion = valor        
       
        if(existeORG and direccionamiento.upper() != 'EQU'):
            posicion_anterior = 0
            nueva_posicion = 2
            bytes_para_recalcular_direccion = ''
            while(len(codigo_maquina) > posicion_anterior and not S1completado):
                codigo_maquina_registro += codigo_maquina[posicion_anterior:nueva_posicion]
                posicion_anterior += 2
                nueva_posicion += 2
                contador_codigos_maquina += 1
                
                bytes_para_recalcular_direccion = codigo_maquina[posicion_anterior:]
                if(contador_codigos_maquina >= 16):
                    S1completado = True
            #    #    #    #    #    #    #    #    #    #    #    #
            if(S1completado):
                if(len(codigo_maquina_registro) > 0):
                    if(longitud > 0):
                        longitud += int(len(codigo_maquina_registro)/2)
                    longitud_hexadecimal = format(longitud,'02X')
                    calcular = longitud_hexadecimal + direccion + codigo_maquina_registro
                    checksum = suma_hexadecimal_s1(calcular)
                    S1 = 'S1%s%s%s%s' %(str(longitud_hexadecimal),direccion,codigo_maquina_registro,checksum)
                    lineas_archivo_objeto.append(S1)
                #    #    #    #    #    #    #    #    #    #    #    #
                codigo_maquina_registro = ''
                direccion = ''
                checksum = ''
                longitud = 3
                contador_codigos_maquina = 0
                S1completado = False
                #    #    #    #    #    #    #    #    #    #    #    #
                if(len(bytes_para_recalcular_direccion)>0):
                    codigos_pendientes = 0
                    codigo_hexadecimal_utilizado = 0
                    lista_codigos_pendientes = []
                    while(len(codigo_maquina) > posicion_anterior):
                        lista_codigos_pendientes.append(codigo_maquina[posicion_anterior:nueva_posicion])
                        codigos_pendientes += 1
                        posicion_anterior += 2
                        nueva_posicion += 2
                    codigo_hexadecimal_utilizado = int(len(codigo_maquina)/2)-codigos_pendientes
                    valor = hex(int(valor, 16) + int(str(codigo_hexadecimal_utilizado), 16))[2:].upper()
                    direccion = valor
                    
                    lista_codigos_pendientes.reverse()
                    while(len(lista_codigos_pendientes) > 0 and contador_codigos_maquina < 16):
                        codigo_maquina_registro += lista_codigos_pendientes.pop()
                        contador_codigos_maquina += 1
        print()
        print('-'*50)
        print()
        contador += 1
        
    S9 = 'S9030000FC'
    lineas_archivo_objeto.append(S9)
        
    #    Se escribe el contenido en el archivo
    try:
        archivo_objeto = open(nombre_archivo_objeto, ANADIR_FINAL)
        contador_lineas = 0
        for linea in lineas_archivo_objeto:
            if(contador_lineas+1 == len(lineas_archivo_objeto)):
                archivo_objeto.write(linea)
            else:
                linea += '\n'
                archivo_objeto.write(linea)
            contador_lineas += 1
        archivo_objeto.close()
    except IOError:
        print('ERROR: No se pudo escribir el archivo objeto')  

def calcular_codigo_maquina(info_direccionamiento, codop, operando, contador):
    codigoMaquinaCalculado = ''
    codigoMaquinaTabop     = ''
    valor_hexadecimal      = ''
    registro_computadora = {'X':'00','Y':'01','SP':'10','PC':'11'}
    registro_valor = {'A':'00','B':'01','D':'10'}
    
    informacion = info_direccionamiento.split(', ')
    direccionamiento = informacion[0] 
    #bytes_correspondientes = informacion[1] 
    if(direccionamiento.lower() == 'inherente'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'inh'):
                codigoMaquinaTabop =  direccionamientos[3]
                codigoMaquinaCalculado = codigoMaquinaTabop
    elif(direccionamiento.lower() == 'directo'):
        for direccionamientos in diccionario_codop[codop]:
            if(direccionamientos[2].lower() == 'dir'):
                codigoMaquinaTabop =  direccionamientos[3]
                ###
                valor_decimal = convertir_operando_a_hexadecimal(operando)
                valor_hexadecimal = format(valor_decimal, '02X')
                codigoMaquinaCalculado = codigoMaquinaTabop + valor_hexadecimal
    elif(direccionamiento.lower() == 'extendido'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'ext'):
                codigoMaquinaTabop =  direccionamientos[3]
                ###
                if(es_numerico(operando[1:])):
                    valor_decimal = convertir_operando_a_hexadecimal(operando)
                    valor_hexadecimal = format(valor_decimal, '04X')
                else:
                    for etiqueta in tabla_simbolos:
                        if(operando == etiqueta[0]):
                            valor_hexadecimal = etiqueta[1][:-1]
                codigoMaquinaCalculado = codigoMaquinaTabop + valor_hexadecimal
    elif(direccionamiento.lower() == 'inmediato de 8 bits'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'inm'):
                codigoMaquinaTabop =  direccionamientos[3]
                ###
                valor_decimal = convertir_operando_a_hexadecimal(operando[1:])
                valor_hexadecimal = format(valor_decimal, '02X')
                codigoMaquinaCalculado = codigoMaquinaTabop + valor_hexadecimal
    elif(direccionamiento.lower() == 'inmediato de 16 bits'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'inm'):
                codigoMaquinaTabop =  direccionamientos[3]
                ###
                valor_decimal = convertir_operando_a_hexadecimal(operando[1:])
                valor_hexadecimal = format(valor_decimal, '04X')
                codigoMaquinaCalculado = codigoMaquinaTabop + valor_hexadecimal
    elif(direccionamiento.lower() == 'indizado de 5 bits'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'idx'):
                codigoMaquinaTabop =  direccionamientos[3]
                partes_operando = operando.split(',')
                valor = partes_operando[0]
                if(valor == ''): valor = '0'
                registro = partes_operando[1]
                
                bytesRegistro = registro_computadora[registro.upper()]
                #   
                if(int(valor) >= 0):
                    valor_en_binario = format(abs(int(valor)), '#07b')[2:]
                else:
                    valor_en_binario = format(abs(int(valor)), '#07b')[2:]
                    valor_complementoa2 = complementoados(valor_en_binario)
                    valor_en_binario = valor_complementoa2
                    
                postbyteCode = bytesRegistro+'0'+valor_en_binario
                
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                    
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte
    elif(direccionamiento.lower() == 'indizado de 9 bits'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'idx1'):
                codigoMaquinaTabop =  direccionamientos[3]
                partes_operando = operando.split(',')
                valor = partes_operando[0]
                if(valor == ''): valor = '0'
                registro = partes_operando[1]
                bytesRegistro = registro_computadora[registro.upper()]
                ##
                z ='0'
                if(int(valor) >= 0):
                    valor_hexadecimal = format(abs(int(valor)),'02X')
                    s = '0'
                else:
                    valor_resultante = int(valor) + 256
                    valor_hexadecimal = format(valor_resultante,'02X')
                    s = '1'
                    
                postbyteCode = '111'+bytesRegistro+'0' + z + s
                
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                    
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte + valor_hexadecimal
                
    elif(direccionamiento.lower() == 'indizado de 16 bits'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'idx2'):
                codigoMaquinaTabop =  direccionamientos[3]
                partes_operando = operando.split(',')
                valor = partes_operando[0]
                if(valor == ''): valor = '0'
                registro = partes_operando[1]
                bytesRegistro = registro_computadora[registro.upper()]
                ##
                z = '1'
                s = '0'
                                    
                postbyteCode = '111'+bytesRegistro+'0' + z + s
                
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                    
                valor_hexadecimal = format(abs(int(valor)),'04X')
                
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte + valor_hexadecimal
                
    elif(direccionamiento.lower() == 'indizado de pre decremento'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'idx'):
                codigoMaquinaTabop =  direccionamientos[3]
                partes_operando = operando.split(',')
                valor = partes_operando[0]
                registro = partes_operando[1][1:]
                bytesRegistro = registro_computadora[registro.upper()]
                ##
                p = '0'
                
                valor_resultante = (int(valor)*-1) + 16
                valor_en_binario = format(valor_resultante, '#06b')[2:]
                
                postbyteCode = bytesRegistro+ '1' + p + valor_en_binario
                
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                    
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte 
    
    elif(direccionamiento.lower() == 'indizado de post decremento'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'idx'):
                codigoMaquinaTabop =  direccionamientos[3]
                partes_operando = operando.split(',')
                valor = partes_operando[0]
                registro = partes_operando[1][:-1]
                bytesRegistro = registro_computadora[registro.upper()]
                ##
                p = '1'
                
                valor_resultante = (int(valor)*-1) + 16
                valor_en_binario = format(valor_resultante, '#06b')[2:]
                
                postbyteCode = bytesRegistro+ '1' + p + valor_en_binario
                
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                    
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte 
                
    elif(direccionamiento.lower() == 'indizado de pre incremento'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'idx'):
                codigoMaquinaTabop =  direccionamientos[3]
                partes_operando = operando.split(',')
                valor = partes_operando[0]
                registro = partes_operando[1][1:]
                bytesRegistro = registro_computadora[registro.upper()]
                ##
                p = '0'
                
                valor_en_binario = format(int(valor)-1, '#06b')[2:]
                    
                postbyteCode = bytesRegistro+ '1' + p + valor_en_binario
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                    
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte
                    
    elif(direccionamiento.lower() == 'indizado de post incremento'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'idx'):
                codigoMaquinaTabop =  direccionamientos[3]
                partes_operando = operando.split(',')
                valor = partes_operando[0]
                registro = partes_operando[1][:-1]
                bytesRegistro = registro_computadora[registro.upper()]
                ##
                p = '1'
                
                valor_en_binario = format(int(valor)-1, '#06b')[2:]
                    
                postbyteCode = bytesRegistro+ '1' + p + valor_en_binario
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                    
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte
               
    elif(direccionamiento.lower() == 'indizado de acumulador'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'idx'):
                codigoMaquinaTabop =  direccionamientos[3]
                
                partes_operando = operando.split(',')
                valor = partes_operando[0]
                registro = partes_operando[1]
                
                bytesRegistro = registro_computadora[registro.upper()]
                ##
                a = registro_valor[valor.upper()]
                postbyteCode = '111'+bytesRegistro+ '1' + a
                
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                    
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte   
    elif(direccionamiento.lower() == 'indizado indirecto de 16 bits'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == '[idx2]'):
                codigoMaquinaTabop =  direccionamientos[3]
                
                partes_operando = operando.split(',')
                valor = partes_operando[0][1:]
                registro = partes_operando[1][:-1]
                
                bytesRegistro = registro_computadora[registro.upper()]
                ##
                postbyteCode = '111'+bytesRegistro+ '011'
                
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                ##
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte + format(int(valor), '04X')
                
    elif(direccionamiento.lower() == 'indizado de acumulador indirecto'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == '[d,idx]'):
                codigoMaquinaTabop =  direccionamientos[3]
                
                partes_operando = operando.split(',')
                valor = partes_operando[0][1:]
                registro = partes_operando[1][:-1]
                
                bytesRegistro = registro_computadora[registro.upper()]
                ##
                postbyteCode = '111'+bytesRegistro+ '111'
                
                primerByte  = hex(int(postbyteCode[0:4],2))[2:].upper()
                segundoByte = hex(int(postbyteCode[4:8],2))[2:].upper()
                    
                codigoMaquinaCalculado = codigoMaquinaTabop + primerByte + segundoByte 
                
    elif(direccionamiento.lower() == 'relativo de 8 bits'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'rel'):
                codigoMaquinaTabop =  direccionamientos[3]
                #
                desplazamiento = 0
                valor_numerico = None
                valor_siguiente_localidad = 0
                
                for etiqueta in tabla_simbolos:
                    if(etiqueta[0] == operando):
                        valor_tabsim = etiqueta[1][:-1]
                        valor_numerico = int(valor_tabsim,16)
                        break
                valor_siguiente_localidad = int(archivo_listado[contador][0],16)
                
                if(valor_numerico != None):
                    desplazamiento = valor_numerico - valor_siguiente_localidad
                    if(desplazamiento >= -128 and desplazamiento <= 127):
                        # Complemento a 2 si el numero es negativo
                        if(desplazamiento < 0):
                            valor_resultante = desplazamiento + 256
                            valor_en_binario = format(valor_resultante, '#06b')[2:]
                            codigoMaquinaCalculado = codigoMaquinaTabop + format(int(valor_en_binario,2),'02X')
                        else:
                            codigoMaquinaCalculado = codigoMaquinaTabop + format(desplazamiento,'02X')
                    else: 
                        print('\t\t     ERROR DE DESPLAZAMIENTO: El rango valido es de -128 a 127')
                else:
                    codigoMaquinaCalculado = '-1'
                    
    elif(direccionamiento.lower() == 'relativo de 16 bits'):
        for direccionamientos in diccionario_codop[codop.upper()]:
            if(direccionamientos[2].lower() == 'rel'):
                codigoMaquinaTabop =  direccionamientos[3]
                
                codigoMaquinaCalculado = codigoMaquinaTabop 
                #
                desplazamiento = 0
                valor_numerico = None
                valor_siguiente_localidad = 0
                
                for etiqueta in tabla_simbolos:
                    if(etiqueta[0] == operando):
                        valor_tabsim = etiqueta[1][:-1]
                        valor_numerico = int(valor_tabsim,16)
                        break
                valor_siguiente_localidad = int(archivo_listado[contador][0],16)
                
                if(valor_numerico != None):
                    desplazamiento = valor_numerico - valor_siguiente_localidad
                    if(desplazamiento >= -32768 and desplazamiento <= 32767):
                        # Complemento a 2 si el numero es negativo
                        if(desplazamiento < 0):
                            valor_resultante = desplazamiento + 65536
                            valor_en_binario = format(valor_resultante, '#06b')[2:]
                            codigoMaquinaCalculado = codigoMaquinaTabop + format(int(valor_en_binario,2),'04X')
                        else:
                            codigoMaquinaCalculado = codigoMaquinaTabop + format(desplazamiento,'04X')
                    else: 
                        print('\t\t     ERROR DE DESPLAZAMIENTO: El rango valido es de -128 a 127')
                else:
                    codigoMaquinaCalculado = '-1'
                    
    elif(direccionamiento.lower() == 'directiva'):
        directivas_1byte = ['DB','DC.B','FCB']
        directivas_2bytes = ['DW', 'DC.W','FDB']
        codigoMaquina = ''
        if(codop.upper() == 'FCC'):
            for caracter in operando[1:len(operando)-1]:
                codigo_ascii = ord(caracter)
                codigoMaquinaCalculado += hex(codigo_ascii)[2:].upper()
        elif(codop.upper() in directivas_1byte):
            if(operando[0] == '$' or operando[0] == '@' or operando[0] == '%'):
                operando = operando[1:]
                if(len(operando) < 2):
                    operando = '0'+operando
            else:
                codigoMaquinaCalculado = format(int(operando), '02X')
        elif(codop.upper() in directivas_2bytes):
            if(operando[0] == '$' or operando[0] == '@' or operando[0] == '%'):
                operando = operando[1:]
                if(len(operando) < 4):
                    operando = '0'+operando
            else:
                codigoMaquinaCalculado = format(int(operando), '04X')
    return codigoMaquinaCalculado


#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#                E    V    A    L    U    A    C    I    O    N    E    S
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#------------------------------------------------------------------------------------------
#    Esta funcion evalua si la etiqueta tiene erores o no.
#------------------------------------------------------------------------------------------
def evaluar_etiqueta(etiqueta):
    longitud_etiqueta = len(etiqueta)
    posicion_errores = '                    '
    listaErrores = []
    
    if(longitud_etiqueta > LONGITUD_MAX_ETIQUETA):
        longitudExcedida = "\t\t    ERROR: La longitud maxima de una etiqueta es de 8 caracteres (%d > 8)" %longitud_etiqueta
        listaErrores.append(longitudExcedida)
        
    esValido = evaluar_caracter_inicio(etiqueta[0])
    if(not esValido):
        caracterInicioInvalido = '\t\t    ERROR:  El caracter de inicio de una etiqueta debe ser una letra A-Z o a-z'
        listaErrores.append(caracterInicioInvalido)
        posicion_errores += '^'
    else:
        for caracter in etiqueta:
            esValido = evaluar_caracter(caracter, 'etiqueta')
            if(esValido):
                posicion_errores += ' '
            else:
                posicion_errores += '^'
                caracterNoValido = ('\t\t    ERROR: Los caracteres validos en una etiqueta son A-Z,a-z, 0-9 y \'_\' ')
                listaErrores.append(caracterNoValido)
                
    if(evaluarPosicionErrores(posicion_errores)):
        print(posicion_errores)
        
    longitud_listaErrores = len(listaErrores)  
    if(longitud_listaErrores > 0):
        for error in listaErrores:
            print(error)
        esValido = False
    return esValido

#------------------------------------------------------------------------------------------
#    Esta funcion evalua si el codigo de operacion tiene erores o no.
#------------------------------------------------------------------------------------------
def evaluar_codop(codop):
    global EXISTE_ORG
    
    elCodopTieneErrores = False
    puntosPermitidos = 0
    longitud_codop = len(codop)
    posicion_errores = '                    '
    listaErrores = []
    
    NO_EXISTEN_ERRORES = 0
    
    if(codop == 'NULL'):
        codopNULL = '\t\t    ERROR: Debe existir el codigo de operacion'
        listaErrores.append(codopNULL)
    esValido = evaluar_caracter_inicio(codop[0])
    if(not esValido):
        caracterInicioInvalido = '\t\t    ERROR: El caracter de inicio de un codigo de operaacion debe ser una letra A-Z o a-z'
        listaErrores.append(caracterInicioInvalido)
        posicion_errores += '^'
    else: 
        if(longitud_codop > LONGITUD_MAX_CODOP):
            excedeLongitud = "\t\t    ERROR: La longitud maxima de un codigo de operacion es de 5 caracteres (%d > 5)" %longitud_codop
            listaErrores.append(excedeLongitud)
        for caracter in codop:
            esValido = evaluar_caracter(caracter, 'codop')
            if(esValido):
                if(caracter == PUNTO):
                    puntosPermitidos += 1
                    if(puntosPermitidos > PUNTOS_MAXIMOS):
                        PuntoSobrante = '\t\t    ERROR: El codigo de operacion solo permite 1 punto (%d > 1)' %puntosPermitidos
                        listaErrores.append(PuntoSobrante)
                        posicion_errores += '^'
                posicion_errores += ' '
            else:
                caracterNoValido = ('\t\t    ERROR: Los caracteres validos en un codigo de operacion son A-Z,a-z y \'.\' ')
                listaErrores.append(caracterNoValido)
                posicion_errores += '^'
                        
    if(evaluarPosicionErrores(posicion_errores)):
        print(posicion_errores)
     
    if(len(listaErrores) > NO_EXISTEN_ERRORES):
        elCodopTieneErrores = True
        for error in listaErrores:
            print(error)
            
    return elCodopTieneErrores

def direccionamiento_correspondiente(operando):
    print()
    global resultado_evaluacion
    bytesTotales = 0
    resultado_evaluacion = ''
    # Se le quita el espacio en blanco al operando
    auxiliar = ''
    for caracter in operando:
        if(caracter != ' '):
            auxiliar += caracter
    operando = auxiliar
    
    # Nombre de los direccionamientos disponibles
    direccionamientos_disponibles = []
    for direccionamiento in lista_direccionamientos:
        direccionamientos_disponibles.append(direccionamiento[0])
        
    #-----------------------------------------------------------------------
    #                        INHERENTE
    #-----------------------------------------------------------------------

    if('INH' in direccionamientos_disponibles):
        if(operando == 'null' or operando == 'NULL'):
            informacion = lista_direccionamientos.pop()
            totalBytes = informacion[4]
            print('\t\t    Modo Inherente de %s bytes' %totalBytes)
            bytesTotales = int(totalBytes)
            
            resultado_evaluacion = 'Inherente, %s bytes' %totalBytes
    #-----------------------------------------------------------------------
    #                        INMEDIATO
    #-----------------------------------------------------------------------
    elif(operando[0] == '#'):
        if('INM' in direccionamientos_disponibles):
            informacion = lista_direccionamientos[0]
            
            lista = validar_operando_inmediato(operando, informacion[3], informacion[4])
            esValido = lista[0]
            resultado_evaluacion = lista[1]
            
            if(esValido): 
                totalBytes = informacion[4]
                bytesTotales = int(totalBytes)
        else:
            print('\t\t    ERROR DE CODIGO DE OPERACION: Este Codigo de Operacion no soporta el Modo Inmediato')
    #-----------------------------------------------------------------------
    #                        INDIZADOS
    #-----------------------------------------------------------------------
    elif(',' in operando or '[' in operando or ']' in operando ):
        if('IDX' in direccionamientos_disponibles or 'IDX1' in direccionamientos_disponibles or 'IDX2' in direccionamientos_disponibles 
           or '[IDX2]' in direccionamientos_disponibles or '[D,IDX]' in direccionamientos_disponibles):
            lista = identificar_indizado(operando, lista_direccionamientos)
            
            totalBytes = lista[0]
            bytesTotales = int(totalBytes)
            resultado_evaluacion = lista[1]
        #-----------------------------------------------------------------------
        #                      (2)RELATIVO
        #-----------------------------------------------------------------------
        elif('REL' in direccionamientos_disponibles):
            esValido = evaluar_etiqueta(operando)
    else:
        #-----------------------------------------------------------------------
        #                        DIRECTO & EXTENDIDO
        #-----------------------------------------------------------------------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9') or operando[0] == '-'):
            rango = validar_operando_directo_o_extendido(operando)
            if('DIR' in direccionamientos_disponibles and (rango >= 0 and rango <= 255)):
                informacion = lista_direccionamientos[1]
                totalBytes = informacion[4]
                print('\t\t    Modo Directo, %s bytes' %totalBytes) 
                bytesTotales = int(totalBytes)
                resultado_evaluacion = 'Directo, %s bytes' %totalBytes
            elif('EXT' in direccionamientos_disponibles and rango >= 256 and rango <= 65535):
                informacion = lista_direccionamientos[2]
                totalBytes = informacion[4]
                print('\t\t    Modo Extendido, %s bytes' %totalBytes) 
                bytesTotales = int(totalBytes)
                resultado_evaluacion = 'Extendido, %s bytes' %totalBytes
            elif(rango > 65535):
                print('\t\t    ERROR: El valor del operando esta fuera del rango de Modo Extendido (%d > 65535)' %rango)
            elif(rango < 0):
                print('\t\t    ERROR: El valor del operando esta fuera del rango de Modo Directo (0 > %d)' %rango)
                
        #-----------------------------------------------------------------------
        #                      RELATIVO & EXTENDIDO
        #-----------------------------------------------------------------------
        else:
            esValido = evaluar_etiqueta(operando)
            if(esValido):
                if('REL' in direccionamientos_disponibles):
                    informacion = lista_direccionamientos[0]
                    totalBytes = informacion[4]
                    
                    if(informacion[3] == '1'):
                        print('\t\t    Modo Relativo de 8 bits, %s bytes' %totalBytes)
                        bytesTotales = int(totalBytes)
                        resultado_evaluacion = 'Relativo de 8 bits, %s bytes' %totalBytes
                    elif(informacion[3] == '2'):
                        print('\t\t    Modo Relativo de 16 bits, %s bytes' %totalBytes)
                        bytesTotales = int(totalBytes)
                        resultado_evaluacion = 'Relativo de 16 bits, %s bytes' %totalBytes
                elif('EXT' in direccionamientos_disponibles):
                    informacion = lista_direccionamientos[2]
                    totalBytes = informacion[4]
                    bytesTotales = int(totalBytes)
                    print('\t\t    Modo Extendido, %s bytes' %totalBytes)
                    resultado_evaluacion = 'Extendido, %s bytes' %totalBytes
    print()
    return bytesTotales, resultado_evaluacion

def validar_operando_inmediato(operando, bytesPorCalcular, totalBytes):
    resultado_evaluacion = ''
    esValido = False
    
    if(operando[0] == '#'):
        if(len(operando) > 1):
            if(operando[1] == '%'):
                if(len(operando) > 1):
                    try:
                        if(not esEspacioBlanco_o_Tabulador(operando[2:])):
                            esValido = validar_binario(operando[2:])
                            if(esValido):
                                try:
                                    valor = (int(operando[2:], 2))
                                    if(bytesPorCalcular == '1'):
                                        if(valor >= 0 and valor <= 255):
                                            print('\t\t    Modo Inmediato de 8 bits, %s bytes' %totalBytes)
                                            resultado_evaluacion = 'Inmediato de 8 bits, %s bytes'%totalBytes
                                        else:
                                            print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (%d > 255)' %valor)
                                            esValido = False
                                    elif(bytesPorCalcular == '2'):
                                        if(valor >= 0 and valor <= 65535):
                                            print('\t\t    Modo Inmediato de 16 bits, %s bytes' %totalBytes)
                                            resultado_evaluacion = 'Inmediato de 16 bits, %s bytes' %totalBytes
                                        else:
                                            print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 16 bits esta fuera de rango (%d > 65535)' %valor)
                                            esValido = False
                                except:
                                    print('\t\t    ERROR DE SINTAXIS: La sintaxis de un operando para Modo Inmediato es #<Base Numerica><Valor>')
                            else:
                                print('\t\t    ERROR DE OPERANDO: Los caracteres validos para binario son 0 y 1')
                        else:
                            print('\t\t    ERROR DE SINTAXIS: La sintaxis para Binario es %(0-1)<(0-1)>')
                    except:
                        print('\t\t    ERROR DE SINTAXIS: La sintaxis para Binario es %(0-1)<(0-1)>')
                else:
                    print('\t\t    ERROR DE SINTAXIS: La sintaxis de un operando para Modo Inmediato es #<Base Numerica><Valor>')
            elif(operando[1] >= '0' and operando[1] <= '9'):
                esValido = validar_decimal(operando[1:])
                if(esValido):
                    valor = (int(operando[1:]))
                    if(bytesPorCalcular == '1'):
                        if(valor >= 0 and valor <= 255):
                            print('\t\t    Modo Inmediato de 8 bits, %s bytes' %totalBytes)
                            resultado_evaluacion = 'Inmediato de 8 bits, %s bytes'%totalBytes
                        else:
                            print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (%d > 255)' %valor)
                            esValido = False
                    elif(bytesPorCalcular == '2'):
                        if(valor >= 0 and valor <= 65535):
                            print('\t\t    Modo Inmediato de 16 bits, %s bytes' %totalBytes)
                            resultado_evaluacion = 'Inmediato de 16 bits, %s bytes'%totalBytes
                        else:
                            print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 16 bits esta fuera de rango (%d > 65535)' %valor) 
                            esValido = False  
                else:
                    print('\t\t    ERROR DE OPERANDO: Los caracteres validos para decimal son 0-9')
            elif(operando[1] == '-'):
                try:
                    valor = (int(operando[1:]))
                    if(bytesPorCalcular == '1'):
                        if(valor >= 0 and valor <= 255):
                            print('\t\t    Modo Inmediato de 8 bits, %s bytes' %totalBytes)
                            resultado_evaluacion = 'Inmediato de 8 bits, %s bytes'%totalBytes
                        else:
                            print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (255 > %d)' %valor)
                            esValido = False
                    elif(bytesPorCalcular == '2'):
                        if(valor >= 0 and valor <= 65535):
                            print('\t\t    Modo Inmediato de 16 bits, %s bytes' %totalBytes)
                            resultado_evaluacion = 'Inmediato de 16 bits, %s bytes'%totalBytes
                        else:
                            print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 16 bits esta fuera de rango (65535 > %d)' %valor)
                            esValido = False
                except:
                    print('\t\t    ERROR DE OPERANDO: Los caracteres validos para decimal son 0-9')
            elif(operando[1] == '@'):
                if(len(operando) > 1):
                    try:
                        operando[2]
                        esValido = validar_octal(operando[2:])
                        if(esValido):
                            valor = (int(operando[2:], 8))
                            if(bytesPorCalcular == '1'):
                                if(valor >= 0 and valor <= 255):
                                    print('\t\t    Modo Inmediato de 8 bits, %s bytes' %totalBytes)
                                    resultado_evaluacion = 'Inmediato de 8 bits, %s bytes'%totalBytes
                                else:
                                    print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (%d > 255)' %valor)
                                    esValido = False
                            elif(bytesPorCalcular == '2'):
                                if(valor >= 0 and valor <= 65535):
                                    print('\t\t    Modo Inmediato 16 bits, %s bytes' %totalBytes)
                                    resultado_evaluacion = 'Inmediato de 16 bits, %s bytes'%totalBytes
                                else:
                                    print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 16 bits esta fuera de rango (%d > 65535)' %valor)
                                    esValido = False
                        else:
                            print('\t\t    ERROR DE OPERANDO: Los caracteres validos para octal son 0-7')
                    except:
                        print('\t\t    ERROR DE SINTAXIS: La sintaxis para Octal es @(0-7)<(0-7)>')
                else:
                    print('\t\t    ERROR DE SINTAXIS: La sintaxis de un operando para Modo Inmediato es #<Base Numerica><Valor>') 
            elif(operando[1] == '$'):
                if(len(operando) > 1):
                    try:
                        operando[2]
                        esValido = validar_hexadecimal(operando[2:])
                        if(esValido):
                            valor = (int(operando[2:], 16))
                            if(bytesPorCalcular == '1'):
                                if(valor >= 0 and valor <= 255):
                                    print('\t\t    Modo Inmediato de 8 bits, %s bytes' %totalBytes)
                                    resultado_evaluacion = 'Inmediato de 8 bits, %s bytes'%totalBytes
                                else:
                                    print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (%d > 255)' %valor)
                                    esValido = False
                            elif(bytesPorCalcular == '2'):
                                if(valor >= 0 and valor <= 65535):
                                    print('\t\t    Modo Inmediato de 16 bits, %s bytes' %totalBytes)
                                    resultado_evaluacion = 'Inmediato de 16 bits, %s bytes'%totalBytes
                                else:
                                    print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 16 bits esta fuera de rango (%d > 65535)' %valor)
                                    esValido = False 
                        else:
                            print('\t\t    ERROR DE OPERANDO: Los caracteres validos para hexadecimal son A-F, a-f y 0-9')
                    except:
                        print('\t\t    ERROR DE SINTAXIS: La sintaxis para Hexadecimal es $(A-F,a-f,0-9)<(A-F,a-f,0-9)>')
                else:
                    print('\t\t    ERROR DE SINTAXIS: La sintaxis de un operando para Modo Inmediato es #<Base Numerica><Valor>') 
            else:
                print('\t\t    ERROR DE SINTAXIS: La sintaxis de un operando para Modo Inmediato es #<Base Numerica><Valor>')
        else:
            print('\t\t    ERROR DE SINTAXIS: La sintaxis de un operando para Modo Inmediato es #<Base Numerica><Valor>')
    return esValido, resultado_evaluacion

def validar_binario(operando):
    esValido = False
    for caracter in operando:
        if(caracter >= '0' and caracter <= '1'):
            esValido = True
        else:
            esValido = False
            break
    return esValido

def validar_octal(operando):
    esValido = False
    for caracter in operando:
        if(caracter >= '0' and caracter <= '7'):
            esValido = True
        else:
            esValido = False
            break
    return esValido

def validar_decimal(operando):
    esValido = False
    for caracter in operando:
        if(caracter >= '0' and caracter <= '9'):
            esValido = True
        else:
            esValido = False
            break
    return esValido

def validar_hexadecimal(operando):
    esValido = False
    for caracter in operando:
        if((caracter >= '0' and caracter <= '9') or (caracter >= 'a' and caracter <= 'f') or (caracter >= 'A' and caracter <= 'F') ):
            esValido = True
        else:
            esValido = False
            break
    return esValido


def validar_operando_directo_o_extendido(operando):
    valor = -1
    esValido = False
    
    if(operando != 'NULL'):
        if(operando[0] == '%'):
            if(len(operando) > 1):
                esValido = validar_binario(operando[1:])
                if(esValido):
                    valor = (int(operando[1:], 2))  
                else:
                    print('\t\t    ERROR  DE OPERANDO: Los caracteres validos para Binario son 0 y 1')
            else:
                print('\t\t    ERROR DE SINTAXIS: La sintaxis de Binario es %(0,1)<(0,1)>')
        elif(operando[0] >= '0' and operando[0] <= '9'):
            esValido = validar_decimal(operando)
            if(esValido):
                valor = (int(operando)) 
            else:
                print('\t\t    ERROR DE OPERANDO: Los caracteres validos para Decimal son 0-9')
        elif(operando[0] == '@'):
            if(len(operando) > 1):
                esValido = validar_octal(operando[1:])
                if(esValido):
                    valor = (int(operando[1:], 8))
                else:
                    print('\t\t    ERROR DE OPERANDO: Los caracteres validos para Octal son 0-7')
            else:
                print('\t\t    ERROR DE SINTAXIS: La sintaxis de Octal es @(0-7)<(0-7)>')
        elif(operando[0] == '$'):
            if(len(operando) > 1):
                esValido = validar_hexadecimal(operando[1:])
                if(esValido):
                    valor = (int(operando[1:], 16))
                else:
                    print('\t\t    ERROR DE OPERANDO: Los caracteres validos para Hexadecimal son A-F, a-f y 0-9')
            else:
                print('\t\t    ERROR DE SINTAXIS: La sintaxis de Hexadecimal es $(A-F, a-f, 0-9)<(A-F, a-f, 0-9)>')
        elif(operando[0] == '-'):
            if(len(operando) > 1):
                esValido = validar_decimal(operando[1])
                if(esValido):
                    print('\t\t    ERROR DE RANGO: El rango valido para Decimal debe ser mayor o igual a 0')
                else:
                    print('\t\t    ERROR DE OPERANDO: Los caracteres validos para Decimal son 0-9')
            else:
                print('\t\t    ERROR DE SINTAXIS: La sintaxis de Decimal es <Signo>(0-9)<(0-9)>')
        else:
            print('\t\t    ERROR DE SINTAXIS: La sintaxis de un operando para Modo Directo es <Entero Positivo><Valor>')
    
    return valor

def identificar_indizado(operando, lista_direccionamientos):
    resultado_evaluacion = ''
    registro = ''
    valor = ''
    error = ''
    
    registros = ['A','B','D']
    registros_computadora = ['X','Y', 'PC', 'SP']
    
    error_sintaxis = False
    valor_valido = False
    registro_valido = False
    
    bytesTotales = 0
    #-------------------------------------
    
    
    #-----------------------------------------------------------------------
    #     Si tiene corchete, entonces se evalua como [IDX2] o [D,IDX]
    #-----------------------------------------------------------------------
    if('[' in operando or ']' in operando):
        #
        lista_operando = operando.split(',')
        if(len(lista_operando) == 2):
            valor    = lista_operando[0]
            registro = lista_operando[1]
        elif(len(lista_operando) > 2):
            error_sintaxis = True
            valor    = lista_operando[0]
            for lista in lista_operando:
                lista = lista.upper()
                if(']' in lista and 'X' in lista or 'Y' in lista or 'SP' in lista or 'PC' in lista):
                    registro = lista
                    break
                elif(']' in lista):
                    registro = lista
                    break
            if(registro == ''):
                for lista in lista_operando:
                    lista = lista.lower()
                    for caracter in lista:
                        if(caracter >= 'a' and caracter <= 'z'):
                            registro = lista
                            break
            if(registro == ''):
                registro = lista_operando[1]
        else:
            error_sintaxis = True
            valor    = operando
            registro = operando
        #
        if('[' in valor and ']' in registro):
            valor = valor[1:]
            registro = registro[:len(registro)-1]
        elif('[' in valor and ']' not in registro):
            valor = valor[1:]
            error_sintaxis = True
            error = ']'
        elif('[' not in valor and ']' in registro):
            registro = registro[:len(registro)-1]
            error_sintaxis = True
            error = '['
            
        if(valor != '' ):
            valor_valido = True
        if(registro != ''):
            if(registro.upper() in registros_computadora):
                registro_valido = True
        
        if(valor_valido and valor == 'D' or valor == 'd'):
                if(registro_valido):
                    if(error_sintaxis):
                        print('\t\t    ERROR DE SINTAXIS: La sintaxis de Modo Indizado de Acumulador Indirecto es [D,<Registro>]')
                        
                        if('[' in error):
                            print('\t\t\t\t       Falta el corchete de apertura')
                        elif(']' in error):
                            print('\t\t\t\t       Falta el corchete de cierre')
                
                    else:
                        informacion = lista_direccionamientos[6]
                        totalBytes  = informacion[4]
                        print('\t\t    Modo Indizado de Acumulador Indirecto, %s bytes' %totalBytes)
                        resultado_evaluacion = 'Indizado de Acumulador Indirecto, %s bytes' %totalBytes
                        bytesTotales = totalBytes
                else:
                    print('\t\t    ERROR DE REGISTRO: Los Registros validos para Modo Indizado de Acumulador Indirecto son X, Y, PC y SP')
                    if(error_sintaxis):
                        print('\t\t    ERROR DE SINTAXIS: La sintaxis de Modo Indizado de Acumulador Indirecto es [D,<Registro>]')
                        if('[' in error):
                            print('\t\t\t\t       Falta el corchete de apertura')
                        elif(']' in error):
                            print('\t\t\t\t       Falta el corchete de cierre')
                
        elif(valor_valido and valor.isdigit()):
            numero = int(valor)
            if(numero >= 0 and numero <= 65535):
                valor_valido = True
            else:
                valor_valido = False

            if(valor_valido and registro_valido and not error_sintaxis):
                informacion = lista_direccionamientos[7]
                totalBytes  = informacion[4]
                print('\t\t    Modo Indizado Indirecto de 16 Bits, %s bytes' %totalBytes)
                resultado_evaluacion = 'Indizado Indirecto de 16 Bits, %s bytes' %totalBytes
                bytesTotales = int(totalBytes)
            if(not valor_valido):
                print('\t\t    ERROR DE VALOR: El rango de <Valor> para Modo Indizado de 16 Bits es de 0 a 65,535')
            if(not registro_valido):
                print('\t\t    ERROR DE REGISTRO: Los Registros validos para Modo Indizado de 16 Bits son X, Y, PC y SP')
                if(error_sintaxis):
                    print('\t\t    ERROR DE SINTAXIS: La sintaxis de Modo Indizado de 16 Bits  es [<Valor Decimal>,<Registro>]')
                    if('[' in error):
                        print('\t\t\t\t      Falta el corchete de apertura')
                    elif(']' in error):
                        print('\t\t\t\t       Falta el corchete de cierre')
                        
            if(registro_valido and error_sintaxis):
                print('\t\t    ERROR DE SINTAXIS: La sintaxis de Modo Indizado de 16 Bits  es [<Valor Decimal>,<Registro>]')
                if('[' in error):
                    print('\t\t\t\t      Falta el corchete de apertura')
                elif(']' in error):
                    print('\t\t\t\t       Falta el corchete de cierre')
            
        else:
            valor_valido = False
            if(isLetter(valor)):
                print('\t\t    ERROR DE VALOR: El caracter valido en <Valor> para Modo Indizado de Acumulador Indirecto es D')
            else:
                if(error_sintaxis):
                    print('\t\t    ERROR DE SINTAXIS: La sintaxis de Modo Indizado de 16 Bits  es [<Valor Decimal>,<Registro>]')
                    
                    if('[' in error):
                            print('\t\t\t\t      Falta el corchete de apertura')
                    elif(']' in error):
                        print('\t\t\t\t       Falta el corchete de cierre')
                    print('\t\t    ERROR DE SINTAXIS: La sintaxis de Modo Indizado de Acumulador Indirecto es [D,<Registro>]')
                    
                    if('[' in error):
                            print('\t\t\t\t      Falta el corchete de apertura')
                    elif(']' in error):
                        print('\t\t\t\t       Falta el corchete de cierre')
                if(len(lista_operando) > 1):
                    if(not valor_valido):
                        print()
                        print('\t\t    ERROR DE VALOR: Los caracteres validos en <Valor> para Modo Indizado de 16 Bits son 0-9') 
                        print('\t\t    ERROR DE VALOR: El caracter valido en <Valor> para Modo Indizado de Acumulador Indirecto es D')
                    if(not registro_valido):
                        print()
                        print('\t\t    ERROR DE REGISTRO: Los Registros validos para  Modo Indizado de 16 Bits son X, Y, PC y SP')
                        print('\t\t    ERROR DE REGISTRO: Los Registros validos para Modo Indizado de Acumulador Indirecto son X, Y, PC y SP')
    else:
        #-----------------------------------------------------------------------
        #    No exite el corchete, entonces se evalua como IDX o IDX1 o IDX2
        #-----------------------------------------------------------------------  
        error_sintaxis = False
        registro_valido = False
        valor_valido = False
        
        contador_signos = 0
        errores = []
        
        lista_operando = operando.split(',')
        #-----------------------------------------------------------
        # CASO BASE: IDX - Cuando solo existe una coma
        #-----------------------------------------------------------
        if(len(lista_operando) == 2):
            if(lista_operando[0] == ''):      
                valor = '0'
            else:
                valor = lista_operando[0]
                
            if(lista_operando[1] == ''):
                registro = 'NULL'
                registro_valido = False
            else:
                registro = lista_operando[1]
                registro = registro.upper()
                
        elif(len(lista_operando) > 2):
            error_sintaxis = True
            valor    = lista_operando[0]
            for lista in lista_operando:
                lista = lista.upper()
                if('X' in lista or 'Y' in lista or 'SP' in lista or 'PC' in lista):
                    registro = lista
                    break
            if(registro == ''):
                for lista in lista_operando:
                    lista = lista.lower()
                    for caracter in lista:
                        if(caracter >= 'a' and caracter <= 'z'):
                            registro = lista
                            break
            if(registro == ''):
                registro = lista_operando[1]
        else:
            error_sintaxis = True
            valor    = operando
            registro = operando
                
        try:
            numero = int(valor)
            valor_valido = True
        except:
            numero = None
            
        if('+' in registro or '-' in registro):
            if(numero >= 1 and numero <= 8):
                valor_valido = True
            else:
                valor_valido = False
            if('X' in registro or 'Y' in registro or 'SP' in registro):
                auxiliar = ''
                for caracter in registro:
                    if(caracter == '+' or caracter == '-'):
                        contador_signos += 1
                    elif(caracter >= 'a' and caracter <= 'z' or caracter >= 'A' and caracter <= 'Z'):
                        auxiliar += caracter
                    else:
                        errores.append(caracter)
                
                if(len(errores)== 0 and contador_signos == 1):
                    if(auxiliar in registros_computadora):
                        registro_valido = True
                else:
                    error_sintaxis = True
            else:
                registro_valido = False
            
            if(not error_sintaxis):
                informacion = lista_direccionamientos[3]
                totalBytes = informacion[4]
                if('+' in registro):
                    posicion_signo = registro.split('+')
                    if(posicion_signo[0] == ''):
                        if(valor_valido and registro_valido):
                            #print('\t\t    Modo Indizado de Pre Incremento, %s bytes' %totalBytes)
                            resultado_evaluacion = 'Indizado de Pre Incremento, %s bytes' %totalBytes
                            bytesTotales = int(totalBytes)
                        else:
                            if(not valor_valido):
                                if(numero == None):
                                    print('\t\t    ERROR DE VALOR: Los caracteres validos de <Valor> para Modo Indizado de Pre Incremento son 1-8')
                                else:
                                    print('\t\t    ERROR DE RANGO: El rango valido de <Valor> para Modo Indizado de Pre Incremento es 1-8')
                            if(not registro_valido):
                                print('\t\t    ERROR DE REGISTRO: Los <Registro> validos para Modo Indizado de Pre Incremento son X, Y y SP')
                            
                    elif(posicion_signo[1] == ''):
                        if(valor_valido and registro_valido):
                            #print('\t\t    Modo Indizado de Post Incremento, %s bytes' %totalBytes)
                            resultado_evaluacion = 'Indizado de Post Incremento, %s bytes' %totalBytes
                            bytesTotales = int(totalBytes)
                        else:
                            if(not valor_valido):
                                if(numero == None):
                                    print('\t\t    ERROR DE VALOR: Los caracteres validos de <Valor> para Modo Indizado de Post Incremento son 1-8')
                                else:
                                    print('\t\t    ERROR DE RANGO: El rango valido de <Valor> para Modo Indizado de Post Incremento es 1-8')
                            if(not registro_valido):
                                print('\t\t    ERROR DE REGISTRO: Los <Registro> validos para Modo Indizado de Post Incremento son X, Y y SP')
                            
                elif('-' in registro):
                    posicion_signo = registro.split('-')
                    if(posicion_signo[0] == ''):
                        if(valor_valido and registro_valido):
                            #print('\t\t    Modo Indizado de Pre Decremento, %s bytes' %totalBytes)
                            resultado_evaluacion = 'Indizado de Pre Decremento, %s bytes' %totalBytes
                            bytesTotales = int(totalBytes)
                        else:
                            if(not valor_valido):
                                if(numero == None):
                                    print('\t\t    ERROR DE VALOR: Los caracteres validos de <Valor> para Modo Indizado de Pre Decremento son 1-8')
                                else:
                                    print('\t\t    ERROR DE RANGO: El rango valido de <Valor> para Modo Indizado de Pre Decremento es 1-8')
                            if(not registro_valido):
                                print('\t\t    ERROR DE REGISTRO: Los <Registro> validos para Modo Indizado de Pre Decremento son X, Y y SP')
                    
                    elif(posicion_signo[1] == ''):
                        if(valor_valido and registro_valido):
                            #print('\t\t    Modo Indizado de Post Decremento, %s bytes' %totalBytes)
                            resultado_evaluacion = 'Indizado de Post Decremento, %s bytes' %totalBytes
                            bytesTotales = int(totalBytes)
                        else:
                            if(not valor_valido):
                                if(numero == None):
                                    print('\t\t    ERROR DE VALOR: Los caracteres validos de <Valor> para Modo Indizado de Post Decremento son 1-8')
                                else:
                                    print('\t\t    ERROR DE RANGO: El rango valido de <Valor> para Modo Indizado de Post Decremento es 1-8')
                            if(not registro_valido):
                                print('\t\t    ERROR DE REGISTRO: Los <Registro> validos para Modo Indizado de Post Decremento son X, Y y SP')
                       
            else:
                print('\t\t    ERROR DE SINTAXIS: La sintaxis para Modo Indizado de Pre/Post Incremento/Decremento es: <Entero(1-8), (Signo)Registro> o <Entero(1-8), Registro(Signo)>')
        else:
            if(numero != None):
                ##
                if(registro in registros_computadora):
                    registro_valido = True
                    
                if(valor_valido):
                    if(numero >= -256 and numero <= -17):
                        if(registro_valido):
                            if(error_sintaxis):
                                print('\t\t    ERROR DE SINTAXIS: La sintaxis valida para Modo Indizado de 9 Bits es <Numero con/sin signo>,<Registro>')
                            else:
                                informacion = lista_direccionamientos[4]
                                totalBytes = informacion[4]
                                print('\t\t    Modo Indizado de 9 Bits, %s bytes' %totalBytes)
                                resultado_evaluacion = 'Indizado de 9 Bits, %s bytes' %totalBytes
                                bytesTotales = int(totalBytes)
                        else:
                            print('\t\t    ERROR DE REGISTRO: Los Registros validos para Modo Indizado de 9 Bits son X, Y, PC y SP')
                    elif(numero >= -16 and numero <= 15):
                        if(registro_valido):
                            if(error_sintaxis):
                                print('\t\t    ERROR DE SINTAXIS: La sintaxis valida para Modo Indizado de 5 Bits es <Numero con/sin signo>,<Registro>')
                            else:
                                informacion = lista_direccionamientos[3]
                                totalBytes = informacion[4]
                                print('\t\t    Modo Indizado de 5 Bits, %s bytes' %totalBytes)
                                resultado_evaluacion = 'Indizado de 5 Bits, %s bytes' %totalBytes
                                bytesTotales = int(totalBytes)
                        else:
                            print('\t\t    ERROR DE REGISTRO: Los Registros validos para Modo Indizado de 5 Bits son X, Y, PC y SP')
                    elif(numero >= 16 and numero <= 255):
                        if(registro_valido):
                            if(error_sintaxis):
                                print('\t\t    ERROR DE SINTAXIS: La sintaxis valida para Modo Indizado de 9 Bits es <Numero con/sin signo>,<Registro>')
                            else:
                                informacion = lista_direccionamientos[4]
                                totalBytes = informacion[4]
                                print('\t\t    Modo Indizado de 9 Bits, %s bytes' %totalBytes)
                                resultado_evaluacion = 'Indizado de 9 Bits, %s bytes' %totalBytes
                                bytesTotales = int(totalBytes)
                        else:
                            print('\t\t    ERROR DE REGISTRO: Los Registros validos para Modo Indizado de 9 Bits son X, Y, PC y SP')
                    elif(numero >= 256 and numero <= 65535):
                        if(registro_valido):
                            if(error_sintaxis):
                                print('\t\t    ERROR DE SINTAXIS: La sintaxis valida para Modo Indizado de 16 Bits es <Numero con/sin signo>,<Registro>')
                            else:
                                informacion = lista_direccionamientos[5]
                                totalBytes = informacion[4]
                                print('\t\t    Modo Indizado de 16 Bits, %s bytes' %totalBytes)
                                resultado_evaluacion = 'Indizado de 16 Bits, %s bytes' %totalBytes
                                bytesTotales = int(totalBytes)
                        else:
                            print('\t\t    ERROR DE REGISTRO: Los Registros validos para Modo Indizado de 16 Bits son X, Y, PC y SP')
                    
                    elif(numero < -256 ):
                        print('\t\t    ERROR DE VALOR: El valor numerico excede el rango valido de Modo Indizado de 9 Bits (-256 > %d)' %numero)
                    elif(numero > 65535 ):
                        print('\t\t    ERROR DE VALOR: El valor numerico excede el rango valido de Modo Indizado de 16 Bits (%d > 65535)' %numero)
                    
            else:
                if(valor[0] == '@' or valor[0] == '$' or valor[0] == '%' or valor[0] == '-'):
                    print('\t\t    ERROR DE VALOR: El valor numerico de Modo Indizado de 5, 9 o 16 Bits no esta en base DECIMAL')
                else:
                    valor = valor.upper()
                    if(valor in registros):
                        valor_valido = True
                    if(registro in registros_computadora):
                        registro_valido = True
                    if(not valor_valido):
                        print('\t\t    ERROR: Los registros validos en Modo Indizado de Acumulador son A, B, D') 
                    if(not registro_valido):
                        print('\t\t    ERROR: Los registros validos en Modo Indizado de Acumulador son X, Y, SP o PC')
                    
                    if(valor_valido and registro_valido):
                        informacion = lista_direccionamientos[3]
                        totalBytes = informacion[4]
                        print('\t\t    Modo Indizado de Acumulador, %s bytes' %totalBytes)
                        resultado_evaluacion = 'Indizado de Acumulador, %s bytes' %totalBytes
                        bytesTotales = int(totalBytes)
    return bytesTotales,resultado_evaluacion

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-----------------------------------------------------------------------------------------
#    Esta funcion consiste en evaluar si una linea contiene caracteres distintos a 
#    los vacios como: Tabulador y Espacio en Blanco, antes del Salto de Linea
#-----------------------------------------------------------------------------------------
def evaluar_lineas_sin_contenido(linea):
    posicion = 0
    if(linea[0] == '\n'):
        estaVacia = True
    else:
        while( linea[posicion] != '\n' ):
            if(linea[posicion] == ' ' or linea[posicion] == '\t'):
                estaVacia = True
            else:
                estaVacia = False
                break
            posicion += 1
    return estaVacia

#------------------------------------------------------------------------------------------
#    Esta funcion evalua si el caracter de inicio de una Etiqueta y Codigo de Operacion
#    inician con letra (para ser validas) o no.
#------------------------------------------------------------------------------------------
def evaluar_caracter_inicio(caracter):
    if( (caracter >= 'A' and caracter <= 'Z')):
        return True
    elif(caracter >= 'a' and caracter <= 'z'):
        return True
    return False

#------------------------------------------------------------------------------------------
#    Esta funcion evalua si el codigo de operacion existe en el tabop
#------------------------------------------------------------------------------------------
def existe_codop_en_tabop(codop, diccionario_codop):
    if(codop in diccionario_codop):
        return True
    elif(codop != 'NULL'):
        print()
        print('\t\t    INVALIDO: El codigo de operacion no se encuentra en el TABOP')
        print()
    return False  

#------------------------------------------------------------------------------------------
#    Esta funcion simplemente establece si la cadena de posicion de errores tiene algun 
#    caracter diferente de espacio en blanco
#------------------------------------------------------------------------------------------
def evaluarPosicionErrores(posicion_errores):
    for caracter in posicion_errores:
        if(caracter == '^'):
            return True
    return False
#------------------------------------------------------------------------------------------
#    Esta funcion evalua si el caracter es valido o no para etiqueta o codigo de operacion
#------------------------------------------------------------------------------------------
def evaluar_caracter(caracter, tipo_evaluacion):
    tipo_evaluacion = tipo_evaluacion.lower()  
    
    if((caracter >= 'A' and caracter <= 'Z') or (caracter >= 'a' and caracter <= 'z') or (caracter >= '0' and caracter <= '9') 
       and (tipo_evaluacion == 'codop' or tipo_evaluacion == 'etiqueta')):
        return True
    elif(tipo_evaluacion == 'etiqueta' and caracter == '_'):
        return True
    elif(tipo_evaluacion == 'codop' and caracter == '.'):
        return True
    return False 
#------------------------------------------------------------------------------------------
#    Esta funcion evalua si el codigo de operacion debe tener operando
#------------------------------------------------------------------------------------------
def codopTieneOperando(codop, operando):
    debeExisteOperando = False
    try:
        for lista in (diccionario_codop[codop]):
            debeExisteOperando = (lista[1] == '1')
            break
    except:
        print('No existe el codigo de operacion')
    if(operando == 'NULL' and debeExisteOperando):
        print('\t\t    ERROR: Este codigo de operacion debe tener operando')
        return False
    elif(operando != 'NULL' and not debeExisteOperando):
        print('\t\t    ERROR: Este codigo de operacion no debe tener operando')
        return False
    return True
        
def isLetter(cadena):
    cadena = cadena.lower()
    esValido = False
    for caracter in cadena:
        if(caracter >= 'a' and caracter <= 'z'):
            esValido = True
            break
    return esValido
            
def esEspacioBlanco_o_Tabulador(cadena):
    esValido = False
    for caracter in cadena:
        if(caracter == ' ' or caracter == '\t'):
            esValido = True
        else:
            esValido = False
    return esValido

def suma_hexadecimal_s1(calcular):
    posicion_anterior = 0
    nueva_posicion = 2
    suma = 0
    while(len(calcular) > posicion_anterior):
        suma += int(calcular[posicion_anterior:nueva_posicion],16)
        posicion_anterior += 2
        nueva_posicion += 2
    complemento = complementoauno(format(suma,'#010b'))
    hexa = hex(int(complemento,2))[2:].upper()
    return hexa[1:]
    
def complementoauno(operando):
    complemento = ''
    for caracter in operando:
        if(caracter == '1'):
            complemento += '0'
        elif(caracter == '0'):
            complemento += '1'
    return complemento

def convertir_operando_a_hexadecimal(operando):
    valor_decimal = 0
    if(operando[0] == '@'):
        valor_decimal = (int(operando[1:], 8))
    elif(operando[0] == '%'):
        valor_decimal = (int(operando[1:], 2))
    elif(operando[0] == '$'):
        valor_decimal = (int(operando[1:], 16))
    elif((operando[0] >= '0' and operando[0] <= '9')):
        valor_decimal = int(operando)
    return valor_decimal

def es_numerico(operando):
    operando = operando.upper()
    esNumerico = False
    for caracter in operando:
        if(caracter >= '0' and caracter <= '9' or caracter >='A' and caracter <= 'F'):
            esNumerico = True
        else:
            return False
    return esNumerico

def complementoados(numero):
    i = len(numero)-1
    complemento = ''
    
    while(i >= 0):
        bit = numero[i]
        if(bit == '1'):
            i = i - 1
            complemento = bit + complemento
            break
        complemento = bit + complemento
        i = i - 1
        
    while(i >= 0):
        bit = numero[i]
        if(bit == '1'):
            bit = '0'
        elif(bit == '0'):
            bit = '1' 
        complemento = bit + complemento
        i = i - 1
    return(complemento)

#************************************************************************************************
#************************************************************************************************
#                            P    R    I    N    C    I    P    A    L                          #
#************************************************************************************************
#************************************************************************************************


if __name__ == '__main__':
    
    leer_archivo_tabop()
    leer_lineas_tabop()
    
    nombre_archivo_asm = input('Nombre del archivo: ')
    nombre_archivo_asm += '.txt'
    leer_archivo_ensamblador(nombre_archivo_asm)
    
    if(ASM_LEIDO_EXITOSAMENTE):
        print('='*150)
        print('='*150)
        print('                                                        PASO UNO')
        print('='*150)
        print('='*150)
        print('\n')
        evaluar_contenido_archivo_ensamblador()
        archivo_de_listado()
        archivo_tabsim()
        if(ARCHIVO_LISTADO_LEIDO):
            print('\n')
            print('='*150)
            print('='*150)
            print('                                                        PASO DOS')
            print('='*150)
            print('='*150)
            print('\n')
            evaluar_lineas_de_listado()