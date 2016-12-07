from f02_Variables import archivoEnsamblador, totalDireccionamiento
from f02_Variables import SALTO_LINEA, PUNTO_COMA, ESPACIO, TABULADOR
from Ensamblador.f01_Tabop import direccionamiento_particular_tabop
from Ensamblador.f04_Evaluacion import evaluar_codop, evaluar_etiqueta, existe_codop_en_tabop, codopTieneOperando
from Ensamblador.f05_Direccionamientos import direccionamiento_correspondiente

existe_end = False
#----------------------------------------------------------------------------------
#    Esta funcion consiste en leer linea a linea el archivo de texto que contiene
#    las instrucciones en lenguaje ensabmlador, 
#    y cada linea leida la guarada en la lista 'archivoEnsamblador' 
#----------------------------------------------------------------------------------
def leer_archivo_ensamblador(nombre_archivo):
    LECTURA   = 'r'
    try:
        with open(nombre_archivo, LECTURA) as archivo:
            for linea in archivo:
                if(len(linea) > 1):
                    archivoEnsamblador.append(linea)
            archivo.close()
    except:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo)
        

#-----------------------------------------------------------------------------------------
#    Esta funcion consiste en pasar a evaluar cada linea de la lista 'archivoEnsamblador' 
#    las instrucciones en lenguaje ensamblador, saltandose las lineas vacias 
#-----------------------------------------------------------------------------------------
def evaluar_lineas_ensamblador(diccionario_codop):
    global existe_end
    for linea in archivoEnsamblador:
        estaVacia = evaluar_lineas_sin_contenido(linea)
        if(not estaVacia):
            evaluar_linea_ensamblador(linea, diccionario_codop)
    # Al finalizar, si el 'END' no se encontro en el archivo, se marca error
    if(not existe_end):
        print('Error: No se encontro el END')
        
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
def evaluar_linea_ensamblador(linea, diccionario_codop):
    etiqueta   = ''
    codop      = ''
    operando   = ''
    comentario = ''
    
    posicion = 0

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
    if(len(comentario) > 0):
        print('COMENTARIO')
    else:  
        resultados(etiqueta, codop, operando, diccionario_codop, lista_direccionamientos)
    print('-'*100)
    lista_direccionamientos.clear()
    
def resultados(etiqueta, codop, operando, diccionario_codop, lista_direccionamientos):
    global existe_end
    codopValido        = False
    print('ETIQUETA         =  '+etiqueta)
    evaluar_etiqueta(etiqueta)
    print('CODOP            =  '+codop)
    if(codop.lower() == 'end'): 
        existe_end = True
    codopTieneErrores = evaluar_codop(codop)
    
    if(not codopTieneErrores):
        codopValido = existe_codop_en_tabop(codop.upper(), diccionario_codop)  
        
    print('OPERANDO         =  '+operando)
    if(codop.upper() != 'END' and codopValido):
        totalDireccionamiento = direccionamiento_particular_tabop(codop, diccionario_codop, lista_direccionamientos)
        direccionamiento_correspondiente(lista_direccionamientos, operando)
        if(codopValido):
            codopTieneOperando(codop.upper(), operando, diccionario_codop)
            print('DIRECCIONAMIENTO = ', totalDireccionamiento)