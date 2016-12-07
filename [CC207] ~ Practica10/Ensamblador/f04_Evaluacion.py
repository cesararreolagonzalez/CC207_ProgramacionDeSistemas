from f02_Variables import existe_end
from f02_Variables import LONGITUD_MAX_CODOP, LONGITUD_MAX_ETIQUETA, PUNTO, PUNTOS_MAXIMOS

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
#    Esta funcion evalua si la etiqueta tiene erores o no.
#------------------------------------------------------------------------------------------
def evaluar_etiqueta(etiqueta):
    longitud_etiqueta = len(etiqueta)
    posicion_errores = '                    '
    listaErrores = []
    
    if(longitud_etiqueta > LONGITUD_MAX_ETIQUETA):
        #longitudExcedida = "\t\t    ERROR: La longitud maxima de una etiqueta es de 8 caracteres (%d > 8)" %longitud_etiqueta
        listaErrores.append(longitudExcedida)
        
    esValido = evaluar_caracter_inicio(etiqueta[0])
    if(not esValido):
        #caracterInicioInvalido = '\t\t    ERROR:  El caracter de inicio de una etiqueta debe ser una letra A-Z o a-z'
        listaErrores.append(caracterInicioInvalido)
        posicion_errores += '^'
    else:
        for caracter in etiqueta:
            esValido = evaluar_caracter(caracter, 'etiqueta')
            if(esValido):
                posicion_errores += ' '
            else:
                posicion_errores += '^'
                #caracterNoValido = ('\t\t    ERROR: Los caracteres validos en una etiqueta son A-Z,a-z, 0-9 y \'_\' ')
                listaErrores.append(caracterNoValido)
                
    if(evaluarPosicionErrores(posicion_errores)):
        print(posicion_errores)
        
    longitud_listaErrores = len(listaErrores)  
    if(longitud_listaErrores > 0):
        for error in listaErrores:
            #print(error)
            None
        esValido = False
    return esValido
    
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
#    Esta funcion evalua si el codigo de operacion tiene erores o no.
#------------------------------------------------------------------------------------------
def evaluar_codop(codop):
    elCodopTieneErrores = False
    puntosPermitidos = 0
    longitud_codop = len(codop)
    posicion_errores = '                    '
    listaErrores = []
    
    NO_EXISTEN_ERRORES = 0
    
    if(codop.lower() == 'end'):
        existe_end = True
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
            #print(error)
            None
    return elCodopTieneErrores

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
        #print('\t\t    INVALIDO: El codigo de operacion no se encuentra en el TABOP')
        None
    return False  


#------------------------------------------------------------------------------------------
#    Esta funcion evalua si el codigo de operacion debe tener operando
#------------------------------------------------------------------------------------------
def codopTieneOperando(codop, operando, diccionario_codop):
    debeExisteOperando = False
    try:
        for lista in (diccionario_codop[codop]):
            debeExisteOperando = (lista[1] == '1')
            break
    except:
        #print('No existe el codigo de operacion')
        None
    if(operando == 'NULL' and debeExisteOperando):
        #print('\t\t    ERROR: Este codigo de operacion debe tener operando')
        return False
    elif(operando != 'NULL' and not debeExisteOperando):
        #print('\t\t    ERROR: Este codigo de operacion no debe tener operando')
        return False
    return True