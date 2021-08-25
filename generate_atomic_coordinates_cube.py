import numpy as np
import sys
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-a", required=True, type=str,choices=['V','E','111','110','E110','E111','V110','V111'],help="Arrangement of the cube")


# ap.add_argument("-l","--length", required=True, type=float,help="Cube size")

args = ap.parse_args()
case=args.a
L= 600/2 # args.length 500nm
#32e6 atoms


# atomsfilename=argv.sys[1]


# Lattice constant and vectors
a0 = 4.09
a1 = np.matrix([[.0],[.5],[.5]])*a0
a2 = np.matrix([[.5],[.0],[.5]])*a0
a3 = np.matrix([[.5],[.5],[.0]])*a0
# sft = np.matrix([[1.],[.0],[.0]])*a0


N=10

Lbox=L*1.2
##########################################################
# Functions
def rotationMatrixX(alpha):
    theta=alpha/180.*np.pi
    Rx=np.matrix([[1.,0.,0.],[0.,np.cos(theta),-np.sin(theta)],[0.,np.sin(theta),np.cos(theta)]])
    return Rx

def rotationMatrixY(alpha):
    theta=alpha/180.*np.pi
    Ry=np.matrix([[np.cos(theta),0.,np.sin(theta)],[0.,1.,0.],[-np.sin(theta),0.,np.cos(theta)]])
    return Ry

def rotationMatrixZ(alpha):
    theta=alpha/180.*np.pi
    Rz=np.matrix([[np.cos(theta),-np.sin(theta),0.],[np.sin(theta),np.cos(theta),0.],[0.,0.,1.]])
    return Rz

def inBox(atom,L):
    inside = 0
    if atom[0]<L:
        if atom[0]>-L:
            if atom[1]<L:
                if atom[1]>-L:
                    if atom[2]<L:
                        if atom[2]>-L:
                            inside=1
    return inside

########################################################


## Select type of rotation

## Rotate Lattice AND/OR Cube
if case=='V' :    # vertice
    Rzc=rotationMatrixZ(-35.2643897)
    Ryc=rotationMatrixY(45.)
    Rc=Ryc*Rzc
    rotateLatticeVector=0
    Rl = 1.0
    rotateCube=1
    atomsfilename='ag.fcc.vert.atoms'

elif case=='E' :    # edge
    Rzc=rotationMatrixZ(45.)
    Ryc=1.
    Rc=Ryc*Rzc
    rotateLatticeVector=0
    Rl = 1.0
    rotateCube=1
    atomsfilename='ag.fcc.edge.atoms'

elif case=='111' : # cube 111 to 100
    Rzl=rotationMatrixZ(-35.2643897) #54.7356103
    Ryl=rotationMatrixY(45.0)
    Rl=Ryl*Rzl
    rotateLatticeVector=1
    rotateCube=0
    Rc = 1.0
    atomsfilename='ag.fcc.111.atoms'

elif case=='110' : # cube 110 to 100
    Rzl=rotationMatrixZ(45.)
    Ryl=1.
    Rl=Ryl*Rzl
    rotateLatticeVector=1
    rotateCube=0
    Rc = 1.0
    atomsfilename='ag.fcc.110.atoms'

elif case=='V110' :    # vertice
    Rzc=rotationMatrixZ(-35.2643897)
    Ryc=rotationMatrixY(45.)
    Rc=Ryc*Rzc
    Rzl=rotationMatrixZ(45.)
    Ryl=1.
    Rl=Ryl*Rzl
    rotateLatticeVector=1
    rotateCube=1
    atomsfilename='ag.fcc.vert110.atoms'

elif case=='V111' :    # vertice
    Rzc=rotationMatrixZ(35.2643897)
    Ryc=rotationMatrixY(-45.)
    Rc=Ryc*Rzc
    Rzl=rotationMatrixZ(-35.2643897) #54.7356103
    Ryl=rotationMatrixY(+45.0)
    Rl=Ryl*Rzl
    rotateLatticeVector=1
    rotateCube=1
    atomsfilename='ag.fcc.vert111.atoms'

elif case=='E110' :    # edge
    Rzl=rotationMatrixZ(45.)
    Ryl=1.
    Rl=Ryl*Rzl
    Rzc=rotationMatrixZ(45.)
    Ryc=1.
    Rc=Ryc*Rzc
    rotateLatticeVector=1
    rotateCube=1
    atomsfilename='ag.fcc.edge110.atoms'


elif case=='E111' :    # edge
    Rzl=rotationMatrixZ(45.)
    Ryl=1.
    Rl=Ryl*Rzl
    Rzc=rotationMatrixZ(-35.2643897)
    Ryc=rotationMatrixY(45.0)
    Rc=Ryc*Rzc
    rotateLatticeVector=0
    rotateCube=1
    atomsfilename='ag.fcc.edge111.atoms'


else:
    rotateLatticeVector=0
    rotateCube=0
    atomsfilename='ag.fcc.atoms'





print('Generating: '+atomsfilename)



if rotateLatticeVector==1:
    R = Rl
    a1 = R*a1
    a2 = R*a2
    a3 = R*a3




###
#print(Rc*(N*a1+N*a2+N*a3))
#print(Rc*(N*a1+0*a2+0*a3))
#print(Rc*(0*a1+N*a2+0*a3))
#print(Rc*(0*a1+0*a2+N*a3))
######################################################################################################
## Compute atoms
def computeAtoms(I,case,interval,N,L,Rc,rotateCube):
    f = open('.atoms'+str(I)+case,'w')
    n = 0
    for i in interval:
        for j in range(-N,N):
            for k in range(-N,N):
                atom1 = (i*a1+j*a2+k*a3)

                if inBox(atom1,L)==1:
                    if rotateCube==1:
                        atom1 = Rc*atom1
                    else:
                        atom1 = atom1
                    n=n+1
                    f.write('%d \t 1 \t %f \t %f \t %f \n' % (n,atom1[0],atom1[1],atom1[2]))


    f.close()

from multiprocessing import Pool
pool = Pool(processes=4)
# for I in range(0,4):
int1=range(-N,-N//3)
int2=range(-N//3,0)
int3=range(0,N//3)
int4=range(N//3,N)

# pool.map(computeAtoms,[I,case,interval,N,L,Rc,rotateCube])
pool.map(computeAtoms,[(1,case,int1,N,L,Rc,rotateCube),(2,case,int2,N,L,Rc,rotateCube),(3,case,int3,N,L,Rc,rotateCube),(4,case,int4,N,L,Rc,rotateCube)])


cmd='cat .atoms1'+case+' .atoms2'+case+ ' > .atoms12'
os.system(cmd)
cmd='cat .atoms3'+case+' .atoms4'+case+ ' > .atoms34'
os.system(cmd)
cmd='cat .atoms12'+case+' .atoms34'+case+ ' > .atoms'+case
os.system(cmd)
###
######################################################################################################
# print('# atoms = %d' % n)

## Write to file
g = open('.header'+case,'w')
# File header
g.write('# Lammps input \n\n')

g.write('%d atoms \n' % n)
g.write('1 atom types \n\n')

g.write('%f \t %f \t xlo xhi \n' % (-Lbox,Lbox) )
g.write('%f \t %f \t ylo yhi \n' % (-Lbox,Lbox) )
g.write('%f \t %f \t zlo zhi \n\n' % (-Lbox,Lbox) )

g.write('0.0 0.0 0.0 xy xz yz \n\n')

g.write('Atoms \n\n')

g.close()

cmd='cat .header'+case+' .atoms'+case+ ' > ag.atoms'
# print(cmd)
os.system(cmd)
# os.system()
os.system('rm -f .atoms'+case+' .header'+case)
print('DONE!')
