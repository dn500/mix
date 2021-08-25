import numpy as np
import matplotlib.pyplot as plt
name='data2.dat'

data = np.loadtxt(name)
data[np.isnan(data)]=0

pick=(data[:,6]<100)
nx=data[pick,0]
ny=data[pick,1]
nz=data[pick,2]
xp=data[pick,3]
yp=data[pick,4]
me=data[pick,5]
st=data[pick,6]
nz=data[pick,7]

# for i in range(len(pick)):
# 	if ((data[i,4]>=0.000) and (data[i,4]<0.01) and (data[i,3]>0.23) and (data[i,3]<0.24)):
# 		print(data[i,:])

#sigma = st/st.max()
#z = (sigma-1)*nz
z=st

N = len(z)

#cmap=plt.get_cmap('viridis').colors
#j = np.round((N-1)/(z.max()-z.min())*z+(1-z.min()*(N-1)/(z.max()-z.min())))

#test_direntions = np.array([[1.0000, 0.0000,  0.0000],
#							[0.7071, 0.7071,  0.0000],
#							[0.5774, 0.5774, -0.5774], # =[0.5774, 0.5774,  0.5774]
#							[0.2525, 0.2525, -0.9341],
#							[0.4082, 0.4082, -0.8165],
#							[0.6865, 0.5694, -0.4523],
#							[0.6906, 0.4468, -0.5687],
#							[0.8165, 0.4082, -0.4082],
#							[0.9975, 0.0499, -0.0499],
#							[0.7071, 0.0000, -0.7071],
#							[0.8944, 0.4472,  0.0000],
#							[0.9330, 0.2545, -0.2545],
#							[0.9035, 0.0531, -0.4252],
#							[0.4472, 0.0000, -0.8944]])



test_direntions = np.array([[1.0000, 0.0000,  0.0000],
							[0.7071, 0.7071,  0.0000],
							[0.5774, 0.5774, -0.5774], # =[0.5774, 0.5774,  0.5774]
							[0.2525, 0.2525, -0.9341],
							[0.4082, 0.4082, -0.8165],
							[0.6865, 0.5694, -0.4523],
							[0.6906, 0.4468, -0.5687],
							[0.8165, 0.4082, -0.4082],
							[0.9975, 0.0499, -0.0499], 
							[0.7071, 0.0000, -0.7071],
							[0.8944, 0.4472,  0.0000],
							[0.9330, 0.2545, -0.2545],
							[0.9035, 0.0531, -0.4252],
							[0.4472, 0.0000, -0.8944]])

xp1 = np.divide(test_direntions[:,0],1-test_direntions[:,2])
yp1 = np.divide(test_direntions[:,1],1-test_direntions[:,2])




plt.scatter(xp,yp,c=z,s=1, marker='.')
plt.jet()
plt.plot(xp1,yp1,'o', markerfacecolor='none')

for i in range(len(xp1)):
	#plt.text(xp1[i],yp1[i],str("%d" % i),fontsize=6)
	plt.text(xp1[i],yp1[i],str("[%d %d %d]" % (test_direntions[i,0]*100,test_direntions[i,1]*100,test_direntions[i,2]*100)),fontsize=6)

plt.xlim([0,  1.1])
plt.ylim([-0.1,.8])
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')
plt.colorbar()
plt.savefig("stereo2_withbar.png", dpi=1200, bbox_inches='tight')
plt.close()
plt.show()