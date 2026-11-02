import numpy as np
from itertools import product
U=1.;t=.375;J=.09
h=np.diag([-U if i%4==0 else 0 for i in range(8)]).astype(float)
for i in range(8):h[(i+1)%8,i]-=t;h[i,(i+1)%8]-=t
m=np.arange(8)%4
T=[1-2*(m==2),2*(m==0)-1,1-2*(m==1),1-2*(m==3)]
e0=np.linalg.eigvalsh(h)[0]
shifts=[]
for a in product([0,1],repeat=4):
 if sum(a)==0:continue
 v=2*J*(a[0]*(T[0]-.75)+a[1]*(T[1]-.25)+a[2]*(T[2]-.5)+a[3]*(T[3]-.5))
 sh=np.linalg.eigvalsh(h+np.diag(v))[0]-e0;shifts.append((sh,a))
print('E0',e0,'minimum local penalty',min(shifts),'maximum',max(shifts))
print('all',sorted(shifts))
