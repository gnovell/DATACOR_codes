import sys
import numpy as np
from math import pi, sin, cos

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
    Matriz_xyz2=np.c_[Matriz_xyz,np.ones(Tamanho)]
    NuevasCocordenadas=np.dot(Matriz_xyz2,Traslacion)[:,0:-1]
    return(NuevasCocordenadas)

def RotacionMolecula(Matriz_XYZ,type,ang):
    Angulo=45*pi/180*ang
    Rotacion=np.eye(3,3)
    if type == 'Z':
        Rotacion[0, 0] = cos(Angulo)
        Rotacion[1, 1] = cos(Angulo)
        Rotacion[0, 1] = -sin(Angulo)
        Rotacion[1, 0] = sin(Angulo)
    if type == 'X':
        Rotacion[1, 1] = cos(Angulo)
        Rotacion[2, 2] = cos(Angulo)
        Rotacion[1, 2] = -sin(Angulo)
        Rotacion[2, 1] = sin(Angulo)
    if type == 'Y':
        Rotacion[1, 1] = cos(Angulo)
        Rotacion[2, 2] = cos(Angulo)
        Rotacion[1, 2] = -sin(Angulo)
        Rotacion[2, 1] = sin(Angulo)
    Matriz_rotada=np.dot(Matriz_XYZ,Rotacion)
    return(Matriz_rotada)

def FormatoGEN(arxiu,Mcell,Mxyz,at_type,at_num):
    archivo=open(arxiu,'w')
    archivo.write(' {}   S \n'.format(len(Mxyz)))
    #    print('Converted by gnovell')
    archivo.write('  '.join(at_type)+'\n')
    limiter = int(at_num[0])
    j = 1
    for i in range(len(Mxyz)):
        if i == limiter:
            limiter += int(at_num[j])
            j += 1
        archivo.write('{:>4}   {}   {:>12f}   {:>12f}   {:>12f} \n'.format(i+1,j,*Mxyz[i]))
    archivo.write('  0.0000000000   0.0000000000   0.0000000000 \n')
    for i in range(len(Mcell)):
        archivo.write(' {:>12f}  {:>12f}  {:>12f}  \n'.format(*Mcell[i]))


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

for i in range(7):
    Matriz_coorRot = RotacionMolecula(CoordenadasMOL,'Z',i)
    Matriz_centerRot = CenterMolecule(Mcellslab, Matriz_coorRot)
    for j in range(7):
        Matriz_coorRot = RotacionMolecula(Matriz_centerRot, 'X',j)
        Matriz_centerRot = CenterMolecule(Mcellslab, Matriz_coorRot)
        for k in range(7):
            Matriz_coorRot = RotacionMolecula(Matriz_centerRot, 'Y',k)
            Matriz_centerRot = CenterMolecule(Mcellslab, Matriz_coorRot)
            Matriz_coordenadas = np.concatenate((Matriz_XYZslab, Matriz_centerRot))
            FormatoGEN('geom_rZ'+str(i)+'_X'+str(j)+'_Y'+str(k)+'.gen', Mcellslab, Matriz_coordenadas,at_typeslab + at_type, at_numslab + at_num)

