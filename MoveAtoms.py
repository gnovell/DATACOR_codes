import sys
import numpy as np
#from math import pi, sin, cos

def read_file(arxiu):
    Mcell=[]
    Mxyz=[]
    selective=0
    counter=0
    lin=0
    archivo=open(arxiu,'rt')
    for linea in archivo :
        if counter == 0 :
            comment=linea
        elif counter == 1 :
            modulo=float(linea)
        elif counter > 1 and counter < 5 :
            Mcell.append(linea.split())
        elif counter == 5 :
            at_type=linea.split()
        elif counter == 6 :
            at_num=linea.split()
        elif linea[0] == 'S' and counter > 0 :
            selective = 1
            lin=1
        elif counter == 7 and lin == 0 :
            coordenadas = linea
        elif counter == 8 and lin == 1 :
            coordenadas = linea
        elif not linea.split():
            break
        elif counter > 7+lin :
            Mxyz.append(linea.split()[0:3])
 #           Mxyz.append([float(x) for x in linea.split()[0:3]])
        counter += 1
    Matriz_celda=np.array(Mcell,float)
    Matriz_XYZ=np.array(Mxyz,float)
    return(Matriz_XYZ,Matriz_celda,modulo,at_type,at_num,coordenadas)

def CenterMolecule(Mcell,Matriz_xyz):
    Tamanho=len(Matriz_xyz)
    CentroCelda=np.sum(Mcell,axis=0)/2
    CentroMol=np.sum(Matriz_xyz,axis=0)/Tamanho
    Vector=CentroCelda-CentroMol
    Traslacion=np.eye(4,4)
    Traslacion[3,0:-1]=Vector
#    columna=np.zero(Tamanho)
    Matriz_xyz2=np.c_[Matriz_xyz,np.ones(Tamanho)]
    NuevasCocordenadas=np.dot(Matriz_xyz2,Traslacion)[:,0:-1]
    return(NuevasCocordenadas)

def FormatoGEN(Mcell,Mxyz,at_type,at_num):
    print(len(Mxyz),'S')
    #    print('Converted by gnovell')
    print(*at_type)
    limiter = int(at_num[0])
    j = 1
    for i in range(len(Mxyz)):
        if i == limiter:
            limiter += int(at_num[j])
            j += 1
        print(i + 1, j, *Mxyz[i])
    # print(New_coordinates)
    print('0.00   0.00   0.00')
    for i in range(len(Mcell)):
        print(*Mcell[i])


##########################
##########################
#########################

# archivo=sys.argv[1]
archivo1 = './SLAB'
archivo2 = './POSCAR'

Mxyzslab, Mcellslab, moduloslab, at_typeslab, at_numslab, coordenadasslab = read_file(archivo1)
Mxyz, Mcell, modulo, at_type, at_num, coordenadas = read_file(archivo2)

if coordenadasslab[0] == 'D' :
    Matriz_XYZslab=np.dot(Mxyzslab,Mcellslab*moduloslab)
else:
    Matriz_XYZslab=Mxyzslab
if coordenadas[0] == 'D' :
    Matriz_XYZ=np.dot(Mxyz,Mcell*modulo)
else :
    Matriz_XYZ=Mxyz

CoordenadasMOL=CenterMolecule(Mcellslab,Matriz_XYZ)

Matriz_coordenadas=np.concatenate((Matriz_XYZslab,CoordenadasMOL))
FormatoGEN(Mcellslab,Matriz_coordenadas,at_typeslab+at_type,at_numslab+at_num)

