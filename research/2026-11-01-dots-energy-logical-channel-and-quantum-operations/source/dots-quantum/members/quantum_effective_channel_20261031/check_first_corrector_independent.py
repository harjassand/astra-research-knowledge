import numpy as np, json
rng=np.random.default_rng(193)
I=np.eye(2); P=np.diag([1.,0,0]); Q=np.eye(3)-P
Ls=[]
for a,b in [(0,1),(0,2),(1,2)]:
 L=np.zeros((3,3),complex);L[a,b]=2**.5;Ls.append(L)
H=sum(L.conj().T@L for L in Ls)/2
Hi=np.diag([0,1,0.5]);Hih=np.diag([0,1,1/2**.5])
pp=np.kron(P,I);qq=np.kron(Q,I);hh=np.kron(H,I);hi=np.kron(Hi,I)
ls=[np.kron(L,I) for L in Ls]
def comm(a,b):return a@b-b@a
def G(o):return sum(L.conj().T@o@L for L in ls)-hh@o-o@hh
errs=[]
for _ in range(30):
 K=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6));K=(K+K.conj().T)/2;K-=pp@K@pp
 S=hi@K@pp+pp@K@hi
 o=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));o=(o+o.conj().T)/2
 O=np.kron(np.eye(3),o); F=1j*comm(S,O)
 B=qq@(1j*comm(K,O))@qq+sum(L.conj().T@F@L for L in ls)
 err=np.linalg.norm(G(F)+1j*comm(K,O)-B)
 E=2**.5*np.kron(Hih,I)@K[:,:2]
 rec=sum(E[2*j:2*j+2].conj().T@o@E[2*j:2*j+2] for j in range(3))
 gram=E.conj().T@E;D=rec-(gram@o+o@gram)/2
 derr=np.linalg.norm((1j*comm(K,F))[:2,:2]-D)
 errs.append((err,derr))
print(json.dumps({'cases':30,'source_H':np.diag(H).real.tolist(),'Gadj_H':np.diag(sum(L.conj().T@H@L for L in Ls)-2*H@H).real.tolist(),'max_identity_error':max(x[0] for x in errs),'max_CP_orientation_error':max(x[1] for x in errs),'diagnostic_only':True},indent=2))
