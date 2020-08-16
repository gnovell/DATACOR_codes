import sys
import os

# Leer archivo POSCAR
def vasp_file(arxiu):
    at_type=[]
    counter = 0
    archivo = open(arxiu, 'rt')
    for linea in archivo:
        if counter == 5:
            at_type = (linea.split())
        counter += 1
    return(at_type)

##########################
##########################
#########################

#archivo=sys.argv[1]
archivo = './POSCAR'
dirPOTCAR = '~/DATACOR/POTCARS/'

at_type = vasp_file(archivo)
linea='cat '

for i in range(len(at_type)):
    linea = linea+dirPOTCAR+at_type[i]+'.pot  '
linea = linea+'  > POTCAR'

os.system(linea)
