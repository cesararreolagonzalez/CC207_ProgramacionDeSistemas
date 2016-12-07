import re

from f02_Variables import archivoEnsamblador, totalDireccionamiento
from f02_Variables import SALTO_LINEA, PUNTO_COMA, ESPACIO, TABULADOR
from Ensamblador.f01_Tabop import direccionamiento_particular_tabop
from Ensamblador.f04_Evaluacion import evaluar_codop, evaluar_etiqueta, existe_codop_en_tabop, codopTieneOperando
from Ensamblador.f05_Direccionamientos import direccionamiento_correspondiente
from Ensamblador.f06Evaluar_Direccionamientos import validar_operando_directo_o_extendido

existe_end = False
existe_org = False
lista_etiquetas = []
name_archivo = ''
DIR_INIC = 0
temp = ''
CONTLOC  = 0
ASM_LEIDO_EXITOSAMENTE = False
#----------------------------------------------------------------------------------
#    Esta funcion consiste en leer linea a linea el archivo de texto que contiene
#    las instrucciones en lenguaje ensabmlador, 
#    y cada linea leida la guarada en la lista 'archivoEnsamblador' 
#----------------------------------------------------------------------------------
def leer_archivo_ensamblador(nombre_archivo):
    global name_archivo
    name_archivo = nombre_archivo
    
    LECTURA   = 'r'
    try:
        with open(nombre_archivo, LECTURA) as archivo:
            for linea in archivo:
                if(len(linea) > 1):
                    archivoEnsamblador.append(linea)
        ASM_LEIDO_EXITOSAMENTE = True
    except:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo)
        

#-----------------------------------------------------------------------------------------
#    Esta funcion consiste en pasar a evaluar cada linea de la lista 'archivoEnsamblador' 
#    las instrucciones en lenguaje ensamblador, saltandose las lineas vacias 
#-----------------------------------------------------------------------------------------
def evaluar_lineas_ensamblador(diccionario_codop):
    global existe_end
    global archivo
    global temp
    contador = 0
    
    ANADIR_FINAL = 'w+'
    temp = name_archivo.split('.')[0].upper()+'tmp.txt'
    archivo_temporal = open(temp, ANADIR_FINAL)
    tabsim = open('tabsim.txt', ANADIR_FINAL)
    
    for linea in archivoEnsamblador:
        estaVacia = evaluar_lineas_sin_contenido(linea)
        if(not estaVacia):
                if(existe_end and contador == 0):
                    print('\n\n:::::::::::::::::::::: ADVERTENCIA :::::::::::::::::::::::\n    ~  Las siguientes lineas no seran evaluadas  ~\n\n') 
                    contador = 1
                evaluar_linea_ensamblador(linea, diccionario_codop, archivo_temporal, tabsim)
    # Al finalizar, si el 'END' no se encontro en el archivo, se marca error
    if(not existe_end):
        print('ERROR DE CODIGO DE OPERACION: No se encontro el END')
    print('\nDIR_INIC = %d ::: CONTLOC = %d\nLongitud en bytes = %d' %(DIR_INIC, CONTLOC, (CONTLOC-DIR_INIC)))
    archivo_temporal.close()
    tabsim.close()
        
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

#-----------------------------------------------------------------------------------------
#    Esta funcion consiste en identificar si la linea es comentario o por el contrario,
#    identificar su ETIQUETA, CODIGO DE OPERACION y OPERANDO
#-----------------------------------------------------------------------------------------
def evaluar_linea_ensamblador(linea, diccionario_codop, archivo_temporal,tabsim):
    global CONTLOC
    global DIR_INIC
    global lista_etiquetas
    
    etiqueta   = ''
    codop      = ''
    operando   = ''
    comentario = ''
    aux = 0
    posicion = 0
    bytesTotales = 0
    valor_equ = 0
    etiquetaCompletada = False
    codopCompletado    = False
    
    lista_direccionamientos = []

    if(linea[0] != SALTO_LINEA):
        if(linea[0] == PUNTO_COMA):
            comentario += linea
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
           
    #---------------------------------------------
    # Se muestran los resultados de la evaluacion
    #---------------------------------------------  
    if(not existe_end):
        if(len(comentario) > 0):
            print('COMENTARIO')
        else:  
            if(re.match(codop,'EQU',re.IGNORECASE)):
                valor_equ = resultados(etiqueta, codop, operando, diccionario_codop, lista_direccionamientos)
            else:
                bytesTotales = resultados(etiqueta, codop, operando, diccionario_codop, lista_direccionamientos)
             
        if(codop.upper() == 'EQU'):
            if(valor_equ > 65535):
                valor = format(valor_equ, '05X')
            else:
                valor = format(valor_equ, '04X')
        else:
            if(CONTLOC > 65535):
                valor = format(CONTLOC, '05X')
            else:
                valor = format(CONTLOC, '04X')
        while(4 > len(valor)):
            valor = '0'+valor
        if(etiqueta != 'NULL' and len(comentario) == 0):
            existe = False
            for etq in lista_etiquetas:
                if(etiqueta.upper() == etq.upper()):
                    existe = True
                    print('\t\t    ERROR DE ETIQUETA: La etiqueta ya existe')
                    break
            if(not existe):
                lista_etiquetas.append(etiqueta)
                if(re.match(codop,'EQU',re.IGNORECASE)):
                    tabla_simbolos = 'EQU (ETIQUETA ABSOLUTA)|%s|%s\n' %(etiqueta, valor)
                else:
                    tabla_simbolos = 'CONTLOC (ETIQUETA RELATIVA)|%s|%s\n' %(etiqueta,valor)
                tabsim.write(tabla_simbolos)
        if(len(comentario) == 0):
            if(re.match(codop,'EQU',re.IGNORECASE) and valor_equ > 0):
                cadena = 'VALOR EQU|%s|%s|%s|%s\n' %(valor,etiqueta,codop,operando)
            elif(archivo_temporal.tell() > 0):
                cadena = 'CONTLOC|%s|%s|%s|%s\n' %(valor,etiqueta,codop,operando)
            else:
                cadena = 'DIR_INIC|%s|%s|%s|%s\n' %(valor,etiqueta,codop,operando)
            archivo_temporal.write(cadena)
        
        if(CONTLOC >= 0 and len(comentario) == 0):
            if(int(bytesTotales) > 0 and codop.upper() != 'EQU'):
                aux = CONTLOC
                CONTLOC += int(bytesTotales)
                print('CONTLOC          =  %d + %d = %d' %(aux, int(bytesTotales),CONTLOC))
                if(CONTLOC > 65535):
                    print('\t\t    ERROR DE CONTLOC: El rango valido es de 0 a 65535')
            elif(int(valor_equ) > 0 and codop.upper() != 'EQU'):
                aux = CONTLOC
                CONTLOC += int(valor_equ)
                print('CONTLOC          =  %d + %d = %d' %(aux, int(valor_equ),CONTLOC))
                if(CONTLOC > 65535):
                    print('\t\t    ERROR DE CONTLOC: El rango valido es de 0 a 65535')
            else:
                print('CONTLOC          =  %d' %CONTLOC)
    else:
        if(len(comentario) > 0):
            print('COMENTARIO')
        else:
            print('ETIQUETA         =  '+etiqueta)  
            print('CODOP            =  '+codop)
            print('OPERANDO         =  '+operando)
    #if(CONTLOC > 65535):
        #print('\t\t    ERROR DE CONTLOC: El rango valido es de 0 a 65535')
        #CONTLOC = 0
    print('-'*100)
    lista_direccionamientos.clear()
    
def resultados(etiqueta, codop, operando, diccionario_codop, lista_direccionamientos):
    global existe_end
    global existe_org  
    global DIR_INIC
    global CONTLOC
    
    bytesTotales = 0
    
    codopValido        = False
    print('ETIQUETA         =  '+etiqueta)
    if(re.match(codop, 'ORG|END', re.IGNORECASE) and etiqueta != 'NULL'):
        print('\t\t    ERROR DE DIRECTIVA: La directiva %s no debe tener etiqueta' %codop.upper())
    elif(re.match(codop, 'EQU', re.IGNORECASE) and etiqueta == 'NULL'):
        print('\t\t    ERROR DE DIRECTIVA: La directiva %s debe tener etiqueta' %codop.upper())
    else: 
        evaluar_etiqueta(etiqueta)
    print('CODOP            =  '+codop)
    #-------------------------------------------------------------
    
    if(re.match(codop, 'ORG', re.IGNORECASE) and existe_org):
        print('\t\t    ERROR DE DIRECTIVA: La directiva %s solo debe existir una vez' %codop.upper())
    #Si existe END en CODOP
    if(re.match(codop, 'END', re.IGNORECASE)):
        existe_end = True
    #Se evalua el CODOP para encontrar errores
    codopTieneErrores = evaluar_codop(codop)
    
    #Si ni tiene errores, se busca si existe el codop en el tabop
    if(not codopTieneErrores):
        codopValido = existe_codop_en_tabop(codop.upper(), diccionario_codop)  
        
    #-------------------------------------------------------------    
    print('OPERANDO         =  '+operando)
    if(re.match(codop, 'ORG', re.IGNORECASE) and not existe_org):
        existe_org = True
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            DIR_INIC = validar_operando_directo_o_extendido(operando)
            if(DIR_INIC == -1): DIR_INIC = 0
        else:
            DIR_INIC = 0
            print('\t\t    ERROR DE OPERANDO: El valor de la directiva ORG debe estar representado en Decimal, Hexadecimal, Octal o Binario y tener un rango de 0 a 65535',DIR_INIC)
        CONTLOC = DIR_INIC
        print('\t\t    La direccion inicial es: ',DIR_INIC)
    elif(re.match(codop, 'END', re.IGNORECASE) and operando != 'NULL'):
        print('\t\t    ERROR DE OPERANDOV: La directiva END no debe tener operando')
    elif(re.match('DB|DC.B|FCB', codop, re.IGNORECASE)):
        #---------- 0 a 255 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 255):
                bytesTotales = 1
            else:
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 255'%codop.upper())
        else:
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())
    elif(re.match('DW|DC.W|FDB', codop, re.IGNORECASE)):
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 65535):
                bytesTotales = 2
            else:
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())

    elif(re.match('FCC', codop, re.IGNORECASE)):
        if(operando == 'NULL'):
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe ser representado en cualquier caracter ASCII'%codop.upper())
        else:
            if(chr(34) not in operando):
                print('\t\t    ERROR DE SINTAXIS: La cadena debe estar representada entre las comillas de apertura y cierre')
            else:
                if(chr(34) == operando[0]):
                    if(chr(34) == (operando[len(operando)-1])):
                        bytesTotales = len(operando) - 2
                    else:
                        print('\t\t    ERROR DE SINTAXIS: Falta la comilla de cierre')
                else:
                    print('\t\t    ERROR DE SINTAXIS: Falta la comilla de apertura')
    elif(re.match('DS.B|RMB', codop, re.IGNORECASE) or codop.upper() == 'DS'): ##error con los re.match
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 65535):
                bytesTotales = valor * 1
            else:
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper()) 
    elif(re.match('DS.W|RMW', codop, re.IGNORECASE)):
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 65535):
                bytesTotales = (valor * 2)
            else:
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())  
    elif(re.match('EQU', codop, re.IGNORECASE)):
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 65535):
                bytesTotales = valor
            else:
                print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())      
    else:
        if(codop.upper() != 'END' and codopValido):
            totalDireccionamiento = direccionamiento_particular_tabop(codop, diccionario_codop, lista_direccionamientos)
            bytesTotales = direccionamiento_correspondiente(lista_direccionamientos, operando)
            if(codopValido):
                codopTieneOperando(codop.upper(), operando, diccionario_codop)
                print('DIRECCIONAMIENTO = ', totalDireccionamiento)
    return bytesTotales