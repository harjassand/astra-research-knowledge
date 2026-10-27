#!/usr/local/bin/python3
"""Independent local second-sheet pole diagnostic, importing no endpoint code.

Builds the perturbed one-body memory matrix measure, its complete symmetric
two-body convolution, the actual two hard-core constraints, and the continued
physical |LR> resolvent. This is numerical corroboration, not the continuation
proof or an interval pole enclosure.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, root
from scipy.special import roots_legendre

SQ2=math.sqrt(2)
B=np.array([[1,0,0],[0,1/SQ2,0],[0,1/SQ2,0],[0,0,1.]])
T=np.array([[1/SQ2,0,1/SQ2],[0,1,0],[1/SQ2,0,-1/SQ2]])
ISO=B@T  # columns q_e, q_o, physical |LR>


def bath(z,c):
    u=np.asarray(z,dtype=complex)-c
    r=np.sqrt(u-1)*np.sqrt(u+1)
    return 2/(u+r)


def tkron(a,b):
    return np.einsum('nac,nbd->nabcd',a,b).reshape((-1,4,4))


class Local:
    def __init__(self,g,delta,epsilon=0,n=100):
        self.g,self.delta,self.epsilon,self.n=g,delta,epsilon,n
        self.C=np.diag([SQ2*g,g])
        t,w=roots_legendre(n)
        self.th=(t+1)*math.pi/2;self.tw=w*math.pi/2
        self.atoms=[]
        for a,b in [(2.8,3.),(3.,3.1)]:
            e=brentq(lambda x:np.linalg.det(self.memory_D(x)).real,a,b,xtol=5e-15)
            vals,U=np.linalg.eigh(self.memory_D(e).real)
            u=U[:,np.argmin(abs(vals))]
            tails=np.array([bath(e,5),bath(e,1)]).real
            roots=np.array([math.copysign(math.sqrt((e-c)**2-1),e-c) for c in [5,1]])
            tail_derivatives=-tails/roots
            Bprime=np.diag(1-.25*tail_derivatives)
            Binv=np.linalg.inv(self.bath_D(e))
            derivative=np.eye(2)+self.C@Binv@Bprime@Binv@self.C
            residue=np.outer(u,u)/(u@derivative.real@u)
            self.atoms.append((e,residue))

    def bath_D(self,z,m5=None,m1=None):
        z=np.asarray(z,dtype=complex)
        if m5 is None:m5=bath(z,5)
        if m1 is None:m1=bath(z,1)
        out=np.zeros(z.shape+(2,2),complex)
        out[...,0,0]=z-5-.25*m5
        out[...,1,1]=z-1-.25*m1
        out[...,0,1]=out[...,1,0]=-self.epsilon
        return out

    def memory_D(self,z,m5=None,m1=None):
        z=np.asarray(z,dtype=complex)
        out=np.zeros(z.shape+(2,2),complex)
        out[...,0,0]=out[...,1,1]=z-3
        out[...,0,1]=out[...,1,0]=-self.delta
        return out-self.C@np.linalg.inv(self.bath_D(z,m5,m1))@self.C

    def G(self,z,m5=None,m1=None):return np.linalg.inv(self.memory_D(z,m5,m1))

    def density(self,x,center):
        # Holomorphic complexification of the real matrix band density.
        x=np.asarray(x,dtype=complex)
        u=x-center
        rad=np.sqrt(1-u*u)
        upper=2*(u-1j*rad);lower=2*(u+1j*rad)
        if center==5:
            gu=self.G(x,upper,bath(x,1));gl=self.G(x,lower,bath(x,1))
        else:
            gu=self.G(x,bath(x,5),upper);gl=self.G(x,bath(x,5),lower)
        return (gl-gu)/(2j*math.pi)

    def raw_two(self,z):
        out=np.zeros((4,4),complex)
        for e,residue in self.atoms:
            out-=np.kron(residue,self.G(z-e))
        for c in [1,5]:
            cuts=[c-1.,c+1.]
            cuts += [z.real-edge for edge in [0,2,4,6] if c-1<z.real-edge<c+1]
            cuts=sorted(set(cuts))
            for a,b in zip(cuts[:-1],cuts[1:]):
                x=(a+b)/2-(b-a)*np.cos(self.th)/2
                w=self.tw*(b-a)*np.sin(self.th)/2
                integrand=tkron(self.density(x,c),-self.G(z-x))
                out+=np.einsum('n,nij->ij',w,integrand)
        return ISO.T@out@ISO

    def shell_two(self,z):
        # Opposite-band convolution, analytically continued from 4<E<6.
        theta=self.th/2;weights=self.tw/2
        t=np.sin(theta)**2
        x=4+(z-4)*t;y=(z-4)*(1-t)
        integrand=tkron(self.density(x,5),self.density(y,1))
        w=weights*2*(z-4)*np.sin(theta)*np.cos(theta)
        out=2*np.einsum('n,nij->ij',w,integrand)
        return ISO.T@out@ISO

    def continued(self,z):
        raw=self.raw_two(z)
        # h-z convention: upper minus lower boundary is +2 pi i density.
        return raw+(2j*math.pi*self.shell_two(z) if z.imag<0 else 0)

    def F(self,z):
        M=self.continued(z)
        return M[0,0]-M[0,1]*M[1,0]/M[1,1]

    def pole(self,guess):
        def objective(v):
            f=self.F(complex(v[0],v[1]))
            return [f.real,f.imag]
        sol=root(objective,[guess.real,guess.imag],tol=1e-11)
        z=complex(*sol.x)
        M=self.continued(z)
        h=1e-7
        dF=(self.F(z+h)-self.F(z-h))/(2*h)
        coupling=M[2,0]-M[2,1]*M[1,0]/M[1,1]
        residue=-coupling**2/dF
        return {'delta':self.delta,'epsilon':self.epsilon,'n':self.n,
                'success':bool(sol.success),'pole_real':z.real,'pole_imag':z.imag,
                'width_per_delta_squared':-2*z.imag/self.delta**2,
                'schur_zero_residual':float(abs(self.F(z))),
                'continued_physical_LR_residue':[residue.real,residue.imag],
                'harmonic_mixed_atom_distance':float(abs(sum(e for e,_ in self.atoms)-z))}


if __name__=='__main__':
    E=5.9785793151665785452365388939752013
    records=[]
    for n in [80,160]:
        for delta in [.001,.003,.006]:
            model=Local(.2,delta,n=n)
            records.append(model.pole(complex(E-.00708*delta**2,-6.68376e-8*delta**2)))
        delta=.003;epsilon=-.87110445*delta
        model=Local(.2,delta,epsilon,n=n)
        records.append(model.pole(complex(E-.00708*delta**2,-1.03e-9*delta**2)))
    Path(__file__).with_suffix('.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))
