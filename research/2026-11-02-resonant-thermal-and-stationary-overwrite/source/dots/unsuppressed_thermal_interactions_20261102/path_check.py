import numpy as np
from scipy.special import logsumexp

def mat(K,eta,s,t=1.):
    g=eta*t/K
    H=np.zeros((K,K)); H[1:,1:]=2*t*np.eye(K-1)
    for j in range(1,K-1): H[j,j+1]=H[j+1,j]=-t
    H[0,1]=H[1,0]=-g
    H[0,K-1]=H[K-1,0]=-s*g
    return H
print('K,eta,ground_syndrome_gap_over_2J0,full_DeltaF_over_2J0_at_betaJ0_5,excited_path_gap,J0')
for K in [4,8,16,64,180]:
 for eta in [.1,.3,.5]:
    ep=np.linalg.eigvalsh(mat(K,eta,1)); em=np.linalg.eigvalsh(mat(K,eta,-1))
    J=2*eta**2/K**3; beta=5/J
    F=(logsumexp(-beta*ep)-logsumexp(-beta*em))/beta
    print(K,eta,(em[0]-ep[0])/(2*J),F/(2*J),2*(1-np.cos(np.pi/K)),J,sep=',')
