#-------------------------------
# 1. El CODOP es valido si sus caracteres son mayusculas, minusculas o combinacion
# 2. Imprimir toda la informacion de los modos de direccionamiento
# 3. Aunque un CODOP tenga un error en su operando, debe imprimirse su informacion
# 4. END no aparece en el tabop
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

# ------------------------------
#         BANDERAS
# ------------------------------
existe_end = False
contador   = 0

# ------------------------------
#         LISTAS
# ------------------------------
archivoEnsamblador = [] #Almacena las lineas que lee del archivo 'P1ASM.txt'
archivoTabop = []            #
lineasTabop = []             #Almacena las lineas que lee del archivo 'tabop.txt'
lista_codop = []             #Almacena los codigos de operacion de cada linea de 'lineasTabop'
lista_direccionamientos = []

# ------------------------------
#        DICCIONARIOS
# ------------------------------
diccionario_direccionamientos = {'INH':'Inherente', 'DIR':'Directo','INM':'Inmediato','EXT':'Extendido',
                                 'REL':'Relativo','IDX':'Indizado de 5 bits','IDX1':'Indizado de 9 bits',
                                 'IDX2':'Indizado de 16 bits','[IDX2]':'Indizado indirecto de 16 bits',
                                 '[D,IDX]':'Indizado indirecto aculumador'}
diccionario_codop = {}

# -------------------------------------------------------------------
# -------------------------------------------------------------------
#                        F  U  N  C  I  O  N  E  S
#                              T  A  B  O  P
# -------------------------------------------------------------------
# -------------------------------------------------------------------
def leer_archivo_tabop():
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
    except IOError:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo)

def leer_lineas_tabop():
    global diccionario_codop
    global lista_direccionamientos
    global diccionario_direccionamientos
    global lineasTabop
    
    # Cada linea de texto se divide en elementos individuales
    for linea in archivoTabop:
        lineasTabop.append(linea.split('|'))
        
    #Todos los elementos de 'lista_codop' se pasan a un diccionario
    # para eliminar valores repetidos
    for linea in lineasTabop:
        lista_codop.append(linea[0])
    diccionario_codop = dict.fromkeys(lista_codop)
    
    #Se relaciona cada lista de listas con su llave correspondiente
    for llave in diccionario_codop:
        relacionar_llave(llave)

        
def relacionar_llave(llave):
    global diccionario_codop
    lista = []
    for linea in lineasTabop:
        if(linea[0] == llave):
            lista.append(linea)
    diccionario_codop[llave] = lista


# -------------------------------------------------------------------
# -------------------------------------------------------------------
#                        F  U  N  C  I  O  N  E  S
#                             P  1  A  S  M
# -------------------------------------------------------------------
# -------------------------------------------------------------------

def leer_archivo_ensamblador():
    nombre_archivo = 'PRA2BB.txt'
    modo_lectura   = 'r'
    
    try:
        with open(nombre_archivo, modo_lectura) as archivo:
            for linea in archivo:
                if(linea != ""):
                    archivoEnsamblador.append(linea)
            archivo.close()
    except IOError:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo)
        
def leer_lineas_ensamblador():
    for linea in archivoEnsamblador:
        evaluar_linea_ensamblador(linea)
    if(not existe_end):
        print('Error: No se encontro el END')

def evaluar_linea_ensamblador(linea):
    global contador
    etiqueta = ''
    codop    = ''
    operando = ''
    
    posicion = 0
    longitudLinea = len(linea)
    
    etiquetaCompletada = False
    codopCompletado    = False
    operandoCompletado = False
    esComentario       = False
    lineaVacia         = False
    
    if(linea[0] != SALTO_LINEA):
        if(linea[0] == PUNTO_COMA):
            esComentario = True
        else:
            if(linea[0] == ESPACIO or linea[0] == TABULADOR):
                etiqueta = 'NULL'
                etiquetaCompletada = True
                
                while(linea[posicion] == ESPACIO or linea[posicion] == TABULADOR and linea[posicion] != SALTO_LINEA):
                    posicion = posicion + 1
                    if(linea[posicion] == SALTO_LINEA):
                        lineaVacia = True  
                           
            while(not etiquetaCompletada and longitudLinea > posicion):
                if(linea[posicion] == SALTO_LINEA): 
                    codop    = 'NULL'
                    operando = 'NULL'
                    codopCompletado = True
                    operandoCompletado = True
                elif(linea[posicion] == ESPACIO or linea[posicion] == TABULADOR):
                    etiquetaCompletada = True
                    while(linea[posicion] == ESPACIO or linea[posicion] == TABULADOR):
                        if(linea[posicion] == SALTO_LINEA):
                            codop    = 'NULL'
                            operando = 'NULL'
                            codopCompletado = True
                            operandoCompletado = True
                        posicion = posicion + 1
                else:
                    etiqueta = etiqueta + linea[posicion]
                #Si la etiqueta no ha sido completada sigue leyendo posiciones
                if(not etiquetaCompletada):
                    posicion = posicion + 1
                       
            while(not codopCompletado and longitudLinea > posicion):
                if(linea[posicion] == SALTO_LINEA): 
                    operando = 'NULL'
                    operandoCompletado = True
                elif(linea[posicion] == ESPACIO or linea[posicion] == TABULADOR):
                    codopCompletado = True
                    while(linea[posicion] == ESPACIO or linea[posicion] == TABULADOR):
                        posicion = posicion + 1
                else:
                    codop = codop + linea[posicion]
                #Si el codop no ha sido completado sigue leyendo posiciones
                if(not codopCompletado): 
                    posicion = posicion + 1
                
                if(posicion == longitudLinea or linea[posicion] == SALTO_LINEA):
                    operando = 'NULL'
                    operandoCompletado = True
                    
            while(not operandoCompletado and longitudLinea > posicion):
                if(linea[posicion] == SALTO_LINEA or (posicion >= longitudLinea)):
                    operandoCompletado = True
                else:
                    operando = operando + linea[posicion]
                posicion = posicion + 1
           
        codopValido = False
        if(not lineaVacia):
            if(esComentario):
                print('COMENTARIO')
            else:
                if(not existe_end):
                    print('ETIQUETA         =  '+etiqueta)
                    evaluar_etiqueta(etiqueta)
                    
                    print('CODOP            =  '+codop)
                    elCodopTieneErrores = evaluar_codop(codop.upper())
                    
                    if(not elCodopTieneErrores):
                        codopValido = existe_codop_en_tabop(codop.upper())  
                        
                    print('OPERANDO         =  '+operando)
                    if(codopValido):
                        validar_operando(codop.upper(), operando)
                    
                    if(codopValido):
                        print('DIRECCIONAMIENTO = ', direccionamiento_codop(codop.upper()))
                else:
                    contador = contador + 1
                    if(contador == NO_REPETIR_MENSAJE):
                        print('** Las siguientes lineas no seran analizadas')
                        print('   porque ya se encontro el END **')
                    print('-'*90)
                    print('ETIQUETA = '+etiqueta)
                    print('CODOP    = '+codop)
                    print('OPERANDO = '+operando)
    
            print('-'*90)
            
def existe_codop_en_tabop(codop):
    if(codop in diccionario_codop):
        return True
    elif(codop != 'NULL'):
        print('** Invalido: El codigo de operacion no se encuentra en el TABOP **')
    return False  
            
def evaluar_codop(codop):
    global existe_end
    diccionario_codop = dict.fromkeys(lista_codop)
    elCodopTieneErrores = False
    contador_puntos = 0
    longitud_codop = len(codop)
    
    if(codop == 'NULL'):
        print('Error: Debe existir el codigo de operacion')
    elif(codop.lower() == 'end'):
            existe_end = True
    else: 
        if(longitud_codop > LONGITUD_MAX_CODOP):
            elCodopTieneErrores  = True
            print('Error: La longitud maxima de un codigo de operacion es de cinco caracteres y este tiene',longitud_codop)
        for caracter in codop:
            if(caracter == PUNTO):
                contador_puntos += 1
            esValido = evaluar_caracter(caracter, 'codop')
            if(not esValido):
                elCodopTieneErrores = True
                print("Error: El caracter %s no es valido en un codigo de operacion" %caracter)
        if(contador_puntos > PUNTOS_MAXIMOS):
            print('Error: El codigo de operacion tiene', contador_puntos, 'puntos y solo se permite uno')
            elCodopTieneErrores = True
    return elCodopTieneErrores  
            
def validar_operando(codop, operando):
    debeExisteOperando = False
    try:
        for lista in (diccionario_codop[codop]):
            debeExisteOperando = (lista[1] == '1')
            break
    except:
        print('No existe el codigo de operacion')
    if(operando == 'NULL' and debeExisteOperando):
        print('* Error: Este codigo de operacion debe tener operando *')
    elif(operando != 'NULL' and not debeExisteOperando):
        print('* Error: Este codigo de operacion no debe tener operando *')
        
def direccionamiento_codop(codop):
    lista_direccionamientos = []
    lista_informacion = []
    totalDireccionamiento = ''
    contador = 0
    try:
        for lista in (diccionario_codop[codop]):
            lista_direccionamientos.append(lista[2])
            lista_informacion.append(lista[3:7])
        try:
            lista_direccionamientos.reverse()  
            while(lista_direccionamientos != IndexError):   
                direccionamiento = ''
                direccionamiento += diccionario_direccionamientos[lista_direccionamientos.pop()] + '\t'
                if(len(lista_direccionamientos) > 1):
                    if(len(direccionamiento) > 15 and len(direccionamiento) < 30):
                        direccionamiento += '\t\t'
                    elif(len(direccionamiento) > 5 and len(direccionamiento) < 15):
                        direccionamiento += '\t\t\t'
                for elemento in (lista_informacion[contador]):
                    direccionamiento += elemento + '\t'
                contador +=1
                totalDireccionamiento += direccionamiento + '\n' + '\t\t    '
            print(totalDireccionamiento)
        except: None
    except:
        print('No existe el codigo de operacion')
    return totalDireccionamiento
        
def evaluar_etiqueta(etiqueta):
    longitud_etiqueta = len(etiqueta)
    if(longitud_etiqueta > LONGITUD_MAX_ETIQUETA):
        print("Error: La longitud maxima de una etiqueta es de ocho caracteres, y esta tiene",longitud_etiqueta)
            
    for caracter in etiqueta:
        esValido = evaluar_caracter(caracter, 'etiqueta')
        if(not esValido):
            print("Error: El caracter %s no es valido en una etiqueta" %caracter)
    
def evaluar_caracter(caracterAEvaluar, tipo_evaluacion):
    tipo_evaluacion = tipo_evaluacion.lower()    
    caracter = ord(caracterAEvaluar)
    
    if( (caracter >= A_MAYUSCULA and caracter <= Z_MAYUSCULA)):
        return True
    elif(caracter >= A_MINUSCULA and caracter <= Z_MINUSCULA):
        return True
    elif(caracter >= NUMERO_1 and caracter <= NUMERO_9):
        return True
    elif(tipo_evaluacion == 'etiqueta' and caracter == GUION_BAJO):
        return True
    elif(tipo_evaluacion == 'codop' and caracter == ord(PUNTO)):
        return True
    return False      
        
        
if __name__ == '__main__':
    leer_archivo_tabop()
    leer_lineas_tabop()
    leer_archivo_ensamblador()
    leer_lineas_ensamblador()