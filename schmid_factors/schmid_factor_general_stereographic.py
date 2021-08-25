import numpy as np
import sys
import os




# FCC

slip_planes = np.array([[ 1, 1, 1],
			[-1, 1, 1],
			[ 1,-1, 1],
			[ 1, 1,-1]])

burger_vectors = np.array([[[ 0, 1,-1] ,[-1, 0, 1] ,[-1, 1, 0]],
			  [[ 0,-1, 1] ,[ 1, 0, 1] ,[ 1, 1, 0]],
			  [[ 0, 1, 1] ,[-1, 0, 1] ,[ 1, 1, 0]],
			  [[ 0, 1, 1] ,[ 1, 0, 1] ,[ 1,-1, 0]]])

####
n_slip_planes = len(slip_planes)
n_burger_vectors = len(burger_vectors[0])
n_slip_systems = n_slip_planes*n_burger_vectors


def nonzero(a):
	count = 0
	nz = []
	for ai in a:
		if ai < 0.0001:
			count = count+1
		else:
			nz.append(ai)
	return nz

def print_column(Sf):
	print('=========')
	for i in Sf:
		print('%6.3f' % i)
	print('__________ \n')
# DX=np.linspace(0,1,50)
# DY=np.linspace(0,1,50)
# DZ=np.linspace(0,-1,50)

DX=[1]
DY=[1]
DZ=[-1]
for dx in DX:
	for dy in DY:
		for dz in DZ:

			d = np.array([ dx, dy, dz])/np.linalg.norm(np.array([ dx, dy, dz]))

			d[np.isnan(d)]=0

			Sf = []

			for i in range(0,n_slip_planes):
				si  = slip_planes[i]/np.linalg.norm(slip_planes[i])
				cos_phi_i = np.dot(si,d)

				for j in range(0,n_burger_vectors):
					bij = burger_vectors[i][j]/np.linalg.norm(burger_vectors[i][j])
					cos_lambda_ij = np.dot(bij,d)

					sfij = cos_phi_i*cos_lambda_ij

					Sf.append(sfij)
			print_column(Sf)
					#print('%6.6f \t %6.6f \t %6.6f' % (dp[0],dp[1],sfij))

			nz = np.array(nonzero(np.round(np.abs(Sf)*1000)/1000))

			dp = np.array([d[0]/(1-d[2]),d[1]/(1-d[2])])
			dp[np.isnan(dp)]=0
			if (d[0]>=0) and (d[1]>=0) and (d[0]>=d[1]) and (d[0]*d[0]+d[1]*d[1]<=1):
				print('%6.6f\t%6.6f\t%6.6f\t%6.6f\t%6.6f\t%6.6f\t%6.6f\t %6.6f'  % (d[0],d[1],d[2],dp[0],dp[1],nz.mean(),nz.std(),len(nz)))
