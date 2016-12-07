# -*- coding: utf-8 -*-
import re
import os

from f02_Variables import archivoEnsamblador, totalDireccionamiento, archivo_listado, tabla_simbolos
from f02_Variables import SALTO_LINEA, PUNTO_COMA, ESPACIO, TABULADOR
from Ensamblador.f01_Tabop import direccionamiento_particular_tabop
from Ensamblador.f04_Evaluacion import evaluar_codop, evaluar_etiqueta, existe_codop_en_tabop, codopTieneOperando
from Ensamblador.f05_Direccionamientos import direccionamiento_correspondiente
from Ensamblador.f06Evaluar_Direccionamientos import validar_operando_directo_o_extendido
from Ensamblador.f02_Variables import diccionario_codop

existe_end = False
existe_org = False
lista_etiquetas = []
name_archivo = ''
DIR_INIC = 0
temp = ''
CONTLOC  = 0
codigoMaquina = 0
ANADIR_FINAL = 'w+'
LECTURA   = 'r'
resultado_evaluacion = ''
ASM_LEIDO_EXITOSAMENTE = False
#----------------------------------------------------------------------------------
#    Esta funcion consiste en leer linea a linea el archivo de texto que contiene
#    las instrucciones en lenguaje ensabmlador, 
#    y cada linea leida la guarada en la lista 'archivoEnsamblador' 
#----------------------------------------------------------------------------------
def leer_archivo_ensamblador(nombre_archivo):
    global name_archivo
    name_archivo = nombre_archivo
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
    temp = name_archivo.split('.')[0]+'tmp.txt'
    archivo_temporal = open(temp, ANADIR_FINAL)
    tabsim = open('tabsim.txt', ANADIR_FINAL)
    for linea in archivoEnsamblador:
        estaVacia = evaluar_lineas_sin_contenido(linea)
        if(not estaVacia):
                if(existe_end and contador == 0):
                    #print('\n\n:::::::::::::::::::::: ADVERTENCIA :::::::::::::::::::::::\n    ~  Las siguientes lineas no seran evaluadas  ~\n\n') 
                    contador = 1
                evaluar_linea_ensamblador(linea, diccionario_codop, archivo_temporal, tabsim)
    # Al finalizar, si el 'END' no se encontro en el archivo, se marca error
    if(not existe_end):None
        #print('ERROR DE CODIGO DE OPERACION: No se encontro el END')
    #print('\nDIR_INIC = %d ::: CONTLOC = %d\nLongitud en bytes = %d' %(DIR_INIC, CONTLOC, (CONTLOC-DIR_INIC)))
    
    archivo_temporal.close()
    tabsim.close()
    archivo_de_listado()
    archivo_tabsim()
    evaluar_lineas_de_listado()
    
def archivo_de_listado():
    try:
        with open(temp, LECTURA) as archivo:
            for linea in archivo:
                if(len(linea) > 1):
                    archivo_listado.append(linea.split('|'))
    except:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo)

def archivo_tabsim():
    try:
        with open('tabsim.txt', LECTURA) as archivo:
            for linea in archivo:
                if(len(linea) > 1):
                    tabla_simbolos.append(linea.split('|'))
    except:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo)
        
def evaluar_lineas_de_listado():
    archivo_s0 = os.path.basename(name_archivo)[0:2]+'.obj'
    archivo_objeto = open(archivo_s0, ANADIR_FINAL)
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
        direccionamiento = linea[4][:-1]
        
        print('VALOR            =   '+valor)
        print('ETIQUETA         =   '+etiqueta)
        print('CODOP            =   '+codop)
        print('OPERANDO         =   '+operando)
        
        if(direccionamiento.lower() == 'error' and existeORG):
            S1completado = True
        elif(direccionamiento.lower() == 'org'):
            existeORG = True
            caracteres_s0 = os.path.abspath(name_archivo)
            codigo_ascii_archivo = ''
            for caracter in caracteres_s0:
                codigo_ascii_archivo += hex(ord(caracter))[2:].upper()
                
            direccionS0 = '0000'
            codigo_ascii_archivo += '0A'
            
            checksum = suma_hexadecimal_s1(codigo_ascii_archivo)
            longitudS0 = format(int(len(direccionS0 + codigo_ascii_archivo + checksum)/2),'02X')
            
            S0 = 'S0' + longitudS0 + direccionS0 + codigo_ascii_archivo + checksum
            direccion = valor
            archivo_objeto.write(S0+'\n')
        elif(direccionamiento.lower() == 'end'):
            if(len(codigo_maquina_registro) > 0):
                if(longitud > 0):
                    longitud += int(len(codigo_maquina_registro)/2)
                longitud_hexadecimal = format(longitud,'02X')
                calcular = longitud_hexadecimal + direccion + codigo_maquina_registro
                checksum = suma_hexadecimal_s1(calcular)
                S1 = 'S1%s%s%s%s' %(str(longitud_hexadecimal),direccion,codigo_maquina_registro,checksum)
            
                archivo_objeto.write(S1+'\n')
            S9 = 'S9030000FC'
            archivo_objeto.write(S9)
        elif(direccionamiento.lower() != 'error'):
            codigo_maquina = calcular_codigo_maquina(direccionamiento, codop, operando, contador)
            print('CODIGO MAQUINA   =   '+codigo_maquina)
            print('\n     '+direccionamiento+'\n')
        
        if(direccion == '' and direccionamiento.upper() != 'EQU'):
            direccion = valor        
       
        if(existeORG and direccionamiento.upper() != 'EQU'):
            posicion_anterior = 0
            nueva_posicion = 2
            bytes_para_recalcular_direccion = ''
            while(len(codigo_maquina) > posicion_anterior and contador_codigos_maquina < 16 and not S1completado):
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
                    archivo_objeto.write(S1+'\n')
                
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
    archivo_objeto.close()

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
            codigoMaquinaCalculado = format(int(operando), '02X')
        elif(codop.upper() in directivas_2bytes):
            codigoMaquinaCalculado = format(int(operando), '04X')
    return codigoMaquinaCalculado

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
def evaluar_linea_ensamblador(linea, diccionario_codop, archivo_temporal, tabsim):
    global CONTLOC
    global DIR_INIC
    global lista_etiquetas
    global codigoMaquina
    global resultado_evaluacion
    
    etiqueta   = ''
    codop      = ''
    operando   = ''
    comentario = ''
    #aux = 0
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
            #print('COMENTARIO')
            None
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
                    None
                    #print('\t\t    ERROR DE ETIQUETA: La etiqueta ya existe')
                    break
            if(not existe):
                lista_etiquetas.append(etiqueta)
                if(re.match(codop,'EQU',re.IGNORECASE)):
                    tabla_simbolos = '%s|%s\n' %(etiqueta, valor) #ETIQUETA ABSOLUTA
                else:
                    tabla_simbolos = '%s|%s\n' %(etiqueta,valor) #ETIQUETA RELATIVA
                tabsim.write(tabla_simbolos)
        if(len(comentario) == 0):
            if(len(resultado_evaluacion) == 0):
                resultado_evaluacion = 'Error'
            if(re.match(codop,'EQU',re.IGNORECASE) and valor_equ > 0):
                if(codigoMaquina != 0):
                    cadena = '%s|%s|%s|%s|%s\n' %(valor,etiqueta,codop,operando, resultado_evaluacion) #VALOR EQU
                    codigoMaquina = 0
                else:
                    cadena = '%s|%s|%s|%s|%s\n' %(valor,etiqueta,codop,operando,resultado_evaluacion)#VALOR EQU
            elif(archivo_temporal.tell() > 0):
                if(codigoMaquina!= 0):
                    cadena = '%s|%s|%s|%s|%s\n' %(valor,etiqueta,codop,operando,resultado_evaluacion)#CONTLOC
                    codigoMaquina = 0
                else:
                    cadena = '%s|%s|%s|%s|%s\n' %(valor,etiqueta,codop,operando,resultado_evaluacion)#CONTLOC
            else:
                cadena = '%s|%s|%s|%s|%s\n' %(valor,etiqueta,codop,operando,resultado_evaluacion)#DIR_INIC
            archivo_temporal.write(cadena)
            resultado_evaluacion = ''
        
        if(CONTLOC >= 0 and len(comentario) == 0):
            if(int(bytesTotales) > 0 and codop.upper() != 'EQU'):
                #aux = CONTLOC
                CONTLOC += int(bytesTotales)
                #print('CONTLOC          =  %d + %d = %d' %(aux, int(bytesTotales),CONTLOC))
                if(CONTLOC > 65535):
                    #print('\t\t    ERROR DE CONTLOC: El rango valido es de 0 a 65535')
                    None
            elif(int(valor_equ) > 0 and codop.upper() != 'EQU'):
                #aux = CONTLOC
                CONTLOC += int(valor_equ)
                #print('CONTLOC          =  %d + %d = %d' %(aux, int(valor_equ),CONTLOC))
                if(CONTLOC > 65535):
                    None
                    #print('\t\t    ERROR DE CONTLOC: El rango valido es de 0 a 65535')
            else:
                None
                #print('CONTLOC          =  %d' %CONTLOC)
        codigoMaquina = 0
    #print('-'*100)
    lista_direccionamientos.clear()
    
def resultados(etiqueta, codop, operando, diccionario_codop, lista_direccionamientos):
    global existe_end
    global existe_org  
    global DIR_INIC
    global CONTLOC
    global codigoMaquina
    global resultado_evaluacion
    
    bytesTotales = 0
    
    codopValido        = False
    #print('ETIQUETA         =  '+etiqueta)
    if(re.match(codop, 'ORG|END', re.IGNORECASE) and etiqueta != 'NULL'):
        #print('\t\t    ERROR DE DIRECTIVA: La directiva %s no debe tener etiqueta' %codop.upper())
        None
    elif(codop.upper() == 'EQU' and etiqueta == 'NULL'):
        #print('\t\t    ERROR DE DIRECTIVA: La directiva %s debe tener etiqueta' %codop.upper())
        None
    else: 
        evaluar_etiqueta(etiqueta)
    #print('CODOP            =  '+codop)
    #-------------------------------------------------------------
    
    if(re.match(codop, 'ORG', re.IGNORECASE) and existe_org):
        #print('\t\t    ERROR DE DIRECTIVA: La directiva %s solo debe existir una vez' %codop.upper())
        None
    #Si existe END en CODOP
    if(re.match(codop, 'END', re.IGNORECASE)):
        existe_end = True
        resultado_evaluacion = 'END'
    #Se evalua el CODOP para encontrar errores
    codopTieneErrores = evaluar_codop(codop)
    
    #Si ni tiene errores, se busca si existe el codop en el tabop
    if(not codopTieneErrores):
        codopValido = existe_codop_en_tabop(codop.upper(), diccionario_codop)  
        
    #-------------------------------------------------------------    
    #print('OPERANDO         =  '+operando)
    if(re.match(codop, 'ORG', re.IGNORECASE) and not existe_org):
        existe_org = True
        resultado_evaluacion = 'ORG'
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            DIR_INIC = validar_operando_directo_o_extendido(operando)
            if(DIR_INIC == -1): DIR_INIC = 0
        else:
            DIR_INIC = 0
            #print('\t\t    ERROR DE OPERANDO: El valor de la directiva ORG debe estar representado en Decimal, Hexadecimal, Octal o Binario y tener un rango de 0 a 65535',DIR_INIC)
        CONTLOC = DIR_INIC
        #print('\t\t    La direccion inicial es: ',DIR_INIC)
    elif(re.match(codop, 'END', re.IGNORECASE) and operando != 'NULL'):
        #print('\t\t    ERROR DE OPERANDOV: La directiva END no debe tener operando')
        None
    elif(re.match('DB|DC.B|FCB', codop, re.IGNORECASE)):
        #---------- 0 a 255 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 255):
                resultado_evaluacion = 'Directiva'
            else:
                None
                #print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 255'%codop.upper())
        else:
            None
            #print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())
        bytesTotales = 1
    elif(re.match('DW|DC.W|FDB', codop, re.IGNORECASE)):
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 65535):
                resultado_evaluacion = 'Directiva'
            else:
                None
                #print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            None
            #print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())
        bytesTotales = 2
    elif(re.match('FCC', codop, re.IGNORECASE)):
        if(operando == 'NULL'):
            None
            #print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe ser representado en cualquier caracter ASCII'%codop.upper())
        else:
            if(chr(34) not in operando):
                None
                #print('\t\t    ERROR DE SINTAXIS: La cadena debe estar representada entre las comillas de apertura y cierre')
            else:
                if(chr(34) == operando[0]):
                    if(chr(34) == (operando[len(operando)-1])):
                        bytesTotales = len(operando) - 2
                        resultado_evaluacion = 'Directiva'
                    else:
                        None
                        #print('\t\t    ERROR DE SINTAXIS: Falta la comilla de cierre')
                else:
                    None
                    #print('\t\t    ERROR DE SINTAXIS: Falta la comilla de apertura')
    elif(re.match('DS.B|RMB', codop, re.IGNORECASE) or codop.upper() == 'DS'): ##error con los re.match
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 65535):
                bytesTotales = valor * 1
            else:
                None
                #print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            None
            #print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper()) 
    elif(re.match('DS.W|RMW', codop, re.IGNORECASE)):
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 65535):
                bytesTotales = (valor * 2)
            else:
                None
                #print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            None
            #print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())  
    elif(re.match('EQU', codop, re.IGNORECASE)):
        #---------- 0 a 65535 ---------
        if(operando[0] == '$' or operando[0] == '%' or operando[0] == '@' or (operando[0] >= '0' and operando[0] <= '9')):
            valor = validar_operando_directo_o_extendido(operando)
            if(valor >= 0 and valor <= 65535):
                bytesTotales = valor
                resultado_evaluacion = 'EQU'
            else:
                None
                #print('\t\t    ERROR DE RANGO: El operando de la directiva %s debe tener un rango de 0 a 65535'%codop.upper())
        else:
            None
            #print('\t\t    ERROR DE OPERANDO: El operando de la directiva %s debe estar representado en Decimal, Hexadecimal, Octal o Binario'%codop.upper())      
    else:
        if(codop.upper() != 'END' and codopValido):
            totalDireccionamiento = direccionamiento_particular_tabop(codop, diccionario_codop, lista_direccionamientos)
            lista = direccionamiento_correspondiente(lista_direccionamientos, operando, CONTLOC)
            totalBytes = lista[0]
            bytesTotales = int(totalBytes)
            resultado_evaluacion = lista[1]
            if(codopValido):
                codopTieneOperando(codop.upper(), operando, diccionario_codop)
                #print('DIRECCIONAMIENTO = ', totalDireccionamiento)
    return bytesTotales