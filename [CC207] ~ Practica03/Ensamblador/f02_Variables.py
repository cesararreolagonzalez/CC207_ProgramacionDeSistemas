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
archivoEnsamblador = []      #Almacena las lineas que lee del archivo 'P1ASM.txt'
archivoTabop = []            #Almacena las lineas que lee del archivo 'tabop.txt'
lineasTabop = []             #Almacena elementos separados de cada linea de archivoTabop
listaCodop = []             #Almacena los codigos de operacion de cada linea de 'lineasTabop'
lista_direccionamientos = []

# ------------------------------
#        DICCIONARIOS
# ------------------------------
diccionario_direccionamientos = {'INH':'Inherente', 'DIR':'Directo','INM':'Inmediato','EXT':'Extendido',
                                 'REL':'Relativo','IDX':'Indizado de 5 bits','IDX1':'Indizado de 9 bits',
                                 'IDX2':'Indizado de 16 bits','[IDX2]':'Indizado indirecto de 16 bits',
                                 '[D,IDX]':'Indizado indirecto aculumador'}
diccionario_codop = {}
# ------------------------------
#        CADENAS
# ------------------------------
totalDireccionamiento = ''