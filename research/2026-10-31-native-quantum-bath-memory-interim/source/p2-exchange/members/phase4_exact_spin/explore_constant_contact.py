"""Explore constant exchange leakage-removal contacts; no device claim."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

I2 = np.eye(2)
pauli = [np.array([[0, 1], [1, 0]], complex)/2,
         np.array([[0, -1j], [1j, 0]], complex)/2,
         np.diag([1, -1])/2]
def tensor(xs):
    out=np.array([[1]],complex)
    for x in xs: out=np.kron(out,x)
    return out
S=[[tensor([pauli[a] if k==i else I2 for k in range(5)])
    for a in range(3)] for i in range(5)]
I=np.eye(32)
def dot(v,w): return sum(a@b for a,b in zip(v,w))
def add(ids): return [sum(S[i][a] for i in ids) for a in range(3)]
D=add(range(3)); A=add([3,4]); P=add([0,1]); T=add(range(5))
D2=dot(D,D); A2=dot(A,A); P2=dot(P,P); T2=dot(T,T)
Q=(D2-.75*I)/3
Pt=A2/2
F=[S[0][a]-S[1][a] for a in range(3)]
Da=[S[3][a]-S[4][a] for a in range(3)]
V=dot(F,Da); W=dot(D,A)

def state(j,jd,ja,jp):
    obs=[T2,T[2],D2,A2,P2]
    vals=[j*(j+1),j,jd*(jd+1),ja*(ja+1),jp*(jp+1)]
    M=sum((o-v*I)@(o-v*I) for o,v in zip(obs,vals))
    ev,vec=eigh(M)
    assert abs(ev[0])<1e-9 and ev[1]>1e-4,(ev[:3],vals)
    x=vec[:,0]
    idx=np.argmax(abs(x));x*=np.exp(-1j*np.angle(x[idx]))
    return np.real_if_close(x)

def sector(j,labels):
    B=np.column_stack([state(j,*t) for t in labels])
    return B, {n:np.real_if_close(B.conj().T@o@B).round(12).tolist()
               for n,o in [('Q',Q),('Pt',Pt),('V',V),('W',W)]}

def main():
    # jd,ja,jp; order distinguishes the two data logical basis states.
    B1,r1=sector(.5,[(.5,0,0),(.5,0,1),(.5,1,0),(.5,1,1),(1.5,1,1)])
    B3,r3=sector(1.5,[(1.5,0,1),(.5,1,0),(.5,1,1),(1.5,1,1)])
    results={'spin_half':r1,'spin_three_halves':r3}
    out=Path(__file__).with_name('constant_contact_algebra.json')
    out.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
