"""Exact exchange controlled-phase revival in four-spin singlet blocks."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh, expm
from scipy.optimize import brentq

def tensor(xs):
    z=np.array([[1]],complex)
    for x in xs:z=np.kron(z,x)
    return z
spin=[np.array([[0,1,0],[1,0,1],[0,1,0]],complex)/np.sqrt(2),
      np.array([[0,-1j,0],[1j,0,-1j],[0,1j,0]],complex)/np.sqrt(2),
      np.diag([1,0,-1])]
S=[[tensor([spin[a] if j==i else np.eye(3) for j in range(4)])
    for a in range(3)] for i in range(4)]
def dot(x,y):return sum(a@b for a,b in zip(x,y))
def add(ids):return [sum(S[i][a] for i in ids) for a in range(3)]
A=add([0,1]);B=add([2,3]);T=add(range(4))
Hpen=(dot(A,A)+dot(B,B))/2
Cross=dot(S[0],S[2])
ev,U=eigh(dot(T,T));P=U[:,abs(ev)<1e-8]
en,W=eigh(P.conj().T@Hpen@P);Z=P@W
assert np.max(abs(en-[0,2,6]))<1e-9
V=np.real_if_close(Z.conj().T@Cross@Z)
for j in [1,2]:
    if V[j-1,j]<0: Z[:,j]*=-1;V=np.real_if_close(Z.conj().T@Cross@Z)
D=np.diag([0.,2.,6.])
def ratio(g):
    e=np.linalg.eigvalsh(D+g*V)
    return (e[2]-e[0])/(e[1]-e[0])

def main():
    rows=[]
    # Rational spectral gap ratios imply an EXACT recurrence of logical |11>.
    for num,den in [(2,1),(5,2),(7,3),(8,3),(11,4),(13,5),(3,1),(7,2),(4,1)]:
        target=num/den
        grid=np.linspace(.00001,20,2001)
        for l,r in zip(grid[:-1],grid[1:]):
            if (ratio(l)-target)*(ratio(r)-target)<0:
                g=brentq(lambda x:ratio(x)-target,l,r,xtol=2e-14)
                e=np.linalg.eigvalsh(D+g*V)
                t=2*np.pi*den/(e[1]-e[0])
                phase=np.angle(np.exp(-1j*e[0]*t))
                u=expm(-1j*(D+g*V)*t)
                rows.append({'ratio':[num,den],'g_over_Delta':g,'T_Delta':t,
                             'phase':phase,'phase_over_pi':phase/np.pi,
                             'return_error':float(np.linalg.norm(u[:,0]-np.exp(1j*phase)*np.eye(3)[:,0]))})
    result={'V':V.round(12).tolist(),'revivals':rows}
    Path(__file__).with_name('singlet_entangler_exploration.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
