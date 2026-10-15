from geometry import *
from pathlib import Path
import pickle
base=Path(__file__).parent
with open(base/'quarter_turn_face.pkl','rb') as ff:data=pickle.load(ff)
C=data['C'];S=data['S'];h=(2*r+1)/3
Tx=s.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
Tz=s.Matrix.vstack(s.Matrix.hstack(s.zeros(3),-s.eye(3)),s.Matrix.hstack(s.eye(3),s.zeros(3)))
U=s.kronecker_product(Tx,Tz)
T=(C.T*U)[:,12:24]
assert all(s.cancel(vv)==0 for vv in C.T*U-T*C.T)
even=[0,2,4,7,9,11];odd=[1,3,5,6,8,10]
blocks=[];V=[]
for sig in [1,-1]:
    for inds in [even,odd]:
        E=s.eye(12)[:,inds]
        NN=s.Matrix.hstack(*((T-sig*s.eye(12))*E).nullspace())
        VV=E*NN;V.extend([VV[:,ii] for ii in range(VV.cols)])
        block=(VV.T*S*VV).applyfunc(s.factor)
        blocks.append({'sign':sig,'parity':'even' if inds==even else 'odd','V':VV,'S':block})
        print('sign/parity/dim',sig,inds==even,VV.cols,flush=True)
        print(block,flush=True)
VV=s.Matrix.hstack(*V)
assert VV.shape==(12,12) and s.factor(VV.det())!=0
SS=(VV.T*S*VV).applyfunc(s.cancel)
with open(base/'representation_blocks.pkl','wb') as ff:pickle.dump({'r':r,'y':data['y'],'V':VV,'S':SS,'blocks':blocks,'data':data},ff)
