def validar_operando_inmediato(operando, bytesPorCalcular, totalBytes):
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
                                        else:
                                            print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (%d > 255)' %valor)
                                            esValido = False
                                    elif(bytesPorCalcular == '2'):
                                        if(valor >= 0 and valor <= 65535):
                                            print('\t\t    Modo Inmediato de 16 bits, %s bytes' %totalBytes)
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
                        else:
                            print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (%d > 255)' %valor)
                            esValido = False
                    elif(bytesPorCalcular == '2'):
                        if(valor >= 0 and valor <= 65535):
                            print('\t\t    Modo Inmediato de 16 bits, %s bytes' %totalBytes)
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
                        else:
                            print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (255 > %d)' %valor)
                            esValido = False
                    elif(bytesPorCalcular == '2'):
                        if(valor >= 0 and valor <= 65535):
                            print('\t\t    Modo Inmediato de 16 bits, %s bytes' %totalBytes)
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
                                    print('\t\t    Modo  Inmediato de 8 bits, %s bytes' %totalBytes)
                                else:
                                    print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (%d > 255)' %valor)
                                    esValido = False
                            elif(bytesPorCalcular == '2'):
                                if(valor >= 0 and valor <= 65535):
                                    print('\t\t    Modo Inmediato 16 bits, %s bytes' %totalBytes)
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
                                else:
                                    print('\t\t    ERROR DE RANGO: El operando para Modo Inmediato de 8 bits esta fuera de rango (%d > 255)' %valor)
                                    esValido = False
                            elif(bytesPorCalcular == '2'):
                                if(valor >= 0 and valor <= 65535):
                                    print('\t\t    Modo Inmediato de 16 bits, %s bytes' %totalBytes)
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
    return esValido

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
        #print('Valor = ',valor,'Registro = ',registro, 'Longitud = ',len(lista_operando))
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
        #print('Valor=',valor,valor_valido,'::: Registro=',registro,registro_valido,'::: Error=',error_sintaxis)
        
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
                            print('\t\t    Modo Indizado de Pre Incremento, %s bytes' %totalBytes)
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
                            print('\t\t    Modo Indizado de Post Incremento, %s bytes' %totalBytes)
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
                            print('\t\t    Modo Indizado de Pre Decremento, %s bytes' %totalBytes)
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
                            print('\t\t    Modo Indizado de Post Decremento, %s bytes' %totalBytes)
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
                        bytesTotales = int(totalBytes)
  
    return bytesTotales
        
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