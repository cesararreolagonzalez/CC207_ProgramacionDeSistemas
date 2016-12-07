from Ensamblador.f06Evaluar_Direccionamientos import validar_operando_inmediato, validar_operando_directo_o_extendido, identificar_indizado
from Ensamblador.f03_Ensamblador import evaluar_etiqueta

def direccionamiento_correspondiente(lista_direccionamientos, operando, CONTLOC):
    print()
    resultado_evaluacion = ''
    totalBytes = ''
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
                resultado_evaluacion = 'Directo, %s bytes' %totalBytes
            elif('EXT' in direccionamientos_disponibles and rango >= 256 and rango <= 65535):
                informacion = lista_direccionamientos[2]
                totalBytes = informacion[4]
                print('\t\t    Modo Extendido, %s bytes' %totalBytes) 
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
                        resultado_evaluacion = 'Relativo de 8 bits, %s bytes' %totalBytes
                    elif(informacion[3] == '2'):
                        print('\t\t    Modo Relativo de 16 bits, %s bytes' %totalBytes)
                        resultado_evaluacion = 'Relativo de 16 bits, %s bytes' %totalBytes
                elif('EXT' in direccionamientos_disponibles):
                    informacion = lista_direccionamientos[2]
                    totalBytes = informacion[4]
                    print('\t\t    Extendido, %s bytes' %totalBytes)
                    resultado_evaluacion = 'Extendido, %s bytes' %totalBytes
                 
    print()
    return totalBytes, resultado_evaluacion

def busca_etiqueta_tabop(etiqueta):
    valor = 0
    LECTURA   = 'r'
    try:
        with open("tabsim.txt", LECTURA) as archivo:
            for linea in archivo:
                if(len(linea) > 1):
                    print(linea)
                    lista = linea.split('|')
                    if(etiqueta == lista[1]):
                        valor = lista[2]
    except:
        print('%s (El sistema no puede encontrar el archivo especificado)' %nombre_archivo)
    return valor
            