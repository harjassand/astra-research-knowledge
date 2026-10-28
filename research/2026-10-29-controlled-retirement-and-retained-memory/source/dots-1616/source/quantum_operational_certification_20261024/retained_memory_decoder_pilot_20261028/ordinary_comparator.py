"""Record-only ordinary random-Pauli tomography/Procrustes baseline.
Not the theorem's learner. It imports no plant. The source has no knowledge of
this decoder or current independently sampled output measurement axis.
"""
import numpy as np
from scipy.spatial.transform import Rotation
from quantum_math import I,X,Y,Z,unitary_choi

class OrdinaryComparator:
    def __init__(self):
        self.total=np.zeros((3,3));self.n=0
    def decoder(self):
        if self.n==0: return unitary_choi(I), {'singular_values':[0.,0.,0.]}
        left,sv,right=np.linalg.svd(self.total/self.n)
        correction=np.diag([1.,1.,np.linalg.det(left@right)])
        r=left@correction@right
        x,y,z,w=Rotation.from_matrix(r).as_quat()
        u=w*I-1j*(x*X+y*Y+z*Z)
        return unitary_choi(u.conj().T),{'singular_values':sv.tolist()}
    def observe(self,j,s,m,b):
        if j not in (0,1,2) or m not in (0,1,2) or s not in (-1,1) or b not in (-1,1):
            raise ValueError('invalid ordinary record')
        self.total[m,j]+=9*s*b
        self.n+=1
