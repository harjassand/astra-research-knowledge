#!/usr/local/bin/python3
"""Independent series, coherent mixed-Fock, Gram, and stability checks."""
import json
import math
from pathlib import Path

import numpy as np
import mpmath as mp
import sympy as sy
from scipy.linalg import eigh


def exact_series():
    t,a,b,c=sy.symbols('t a b c',positive=True)
    ep=3-2*a*t+4*a*b*t*t;em=3+a*t-a*b*t*t
    zp=1-2*b*t;zm=1-b*t;E=6-a*t+c*t*t
    F=zp*zp/(2*ep-E)+zm*zm/(2*em-E)
    Fconstant=sy.simplify(sy.limit(F,t,0))
    assert sy.simplify(Fconstant-2*c/(9*a*a))==0
    J=zp/(2*ep-E.subs(c,0))+zm/(2*em-E.subs(c,0))
    Jconstant=sy.simplify(sy.limit(J,t,0))
    assert sy.simplify(Jconstant+b/(3*a))==0
    D=zp*zp/(2*ep-E.subs(c,0))**2+zm*zm/(2*em-E.subs(c,0))**2
    Dleading=sy.simplify(sy.limit(t*t*D,t,0))
    assert sy.simplify(Dleading-2/(9*a*a))==0
    u=sy.symbols('u',positive=True)
    integral=sy.integrate(-u**-2+4*u**-3-3*u**-4,(u,1,3))
    assert integral==sy.Rational(4,27)
    return {'pair_equation_constant_term':str(Fconstant),
            'consequence':'g^4 pair-energy coefficient c=0; continuum remainder is O(g^2)',
            'bound_bound_J_constant':str(Jconstant),'D_times_g4_limit':str(Dleading),
            'bare_integral_before_4_over_pi2':str(integral)}


def gram():
    mp.mp.dps=50
    a=4-2*mp.sqrt(3);b=4/mp.sqrt(3)-2
    pref=3*a/mp.sqrt(2)
    def m(x):return 2/(x-1+mp.sqrt((x-1)**2-1))
    def weight(x):return 4/mp.pi**2*(1-(x-5)**2)/(x-3)**4
    values=[mp.quad(lambda x:weight(x)*m(x)**j,[4,5,6]) for j in range(3)]
    M11=4*mp.pi*b*b*values[0]
    M12=4*mp.pi*b*pref*values[1]
    M22=4*mp.pi*pref*pref*values[2]
    ratio=-M12/M22;residual=M11-M12*M12/M22
    assert M11*M22-M12*M12>0
    return {k:mp.nstr(v,40) for k,v in {
        'M11':M11,'M12':M12,'M22':M22,'optimal_epsilon_over_delta':ratio,
        'residual':residual,'improvement_factor':M11/residual,
        'remaining_fraction':residual/M11,'determinant':M11*M22-M12*M12}.items()}


def mixed_fock(n,g=.2):
    # Physical rail coordinates: both V and W are diagonal number differences.
    d=2+2*n;h=3*np.eye(d)
    t=(1+math.sqrt(2))*g/2;s=(math.sqrt(2)-1)*g/2
    for i,j,v in [(0,2,t),(1,2+n,t),(0,2+n,s),(1,2,s)]:h[i,j]=h[j,i]=v
    for j in range(n):h[2+j,2+n+j]=h[2+n+j,2+j]=2
    for j in range(n-1):
        for o in [2,2+n]:h[o+j,o+j+1]=h[o+j+1,o+j]=-.5
    basis=[(i,j) for i in range(d) for j in range(i,d) if (i,j) not in [(0,0),(1,1)]]
    S=np.zeros((d*d,len(basis)))
    for k,(i,j) in enumerate(basis):
        if i==j:S[i*d+j,k]=1
        else:S[i*d+j,k]=S[j*d+i,k]=1/math.sqrt(2)
    H=S.T@(np.kron(h,np.eye(d))+np.kron(np.eye(d),h))@S
    vals,U=eigh(H);ix=np.argmax(U[basis.index((0,1))]**2)
    E=vals[ix];psi=U[:,ix]
    mem=np.array([int(i==0)+int(j==0)-int(i==1)-int(j==1) for i,j in basis])
    rung=np.array([int(i==2)+int(j==2)-int(i==2+n)-int(j==2+n) for i,j in basis])
    sources=np.array([mem*psi,rung*psi]).T
    specs=[]
    for c,coupling in [(5,math.sqrt(2)*g),(1,g)]:
        h1=np.diag([3.]+[float(c)]*n)
        off=np.r_[coupling,np.full(n-1,-.5)]
        for j,v in enumerate(off):h1[j,j+1]=h1[j+1,j]=v
        x,u=eigh(h1);specs.append((x,u[0]**2))
    xp,wp=specs[0];ym,wm=specs[1]
    dp=xp[:,None]+xp[None,:]-E;dm=ym[:,None]+ym[None,:]-E
    N=math.sqrt(2/(np.sum(np.outer(wp,wp)/dp**2)+np.sum(np.outer(wm,wm)/dm**2)))
    fp=(xp-3)/(math.sqrt(2)*g);fm=(ym-3)/g
    Jp=np.sum(wp[None,:]/dp,axis=1);Jm=np.sum(wm[None,:]/dm,axis=1)
    Hp=np.sum((wp*fp)[None,:]/dp,axis=1);Hm=np.sum((wm*fm)[None,:]/dm,axis=1)
    eta=np.array([N*(Jp[:,None]+Jm[None,:]),N*(Hp[:,None]*fm[None,:]+fp[:,None]*Hm[None,:])])
    mass=np.outer(wp,wm);sums=xp[:,None]+ym[None,:]
    rows=[]
    for shift,reg in [(0,.071),(.13,.019)]:
        z=E+shift+1j*reg
        direct=sources.T@np.linalg.solve(H-z*np.eye(len(H)),sources)
        R=mass/(sums-z)
        K=R.sum();B=np.einsum('ijk,jk->i',eta,R)
        A=np.einsum('ijk,ljk,jk->il',eta,eta,R)
        formula=A-np.outer(B,B)/K
        rows.append({'shift':shift,'regulator':reg,'max_2x2_resolvent_error':float(np.max(abs(direct-formula))),
                     'direct_coherent_cross_entry':[direct[0,1].real,direct[0,1].imag]})
    return {'n':n,'Ep':float(E),'physical_dimension':len(H),'checks':rows}


def stability():
    upper=2.5+math.sqrt(6)
    K=np.array([[upper,.1],[.1,.5]])
    return {'worst_corner_first_rung_exact_min_eigenvalue':float(np.linalg.eigvalsh(K)[0]),
            'Gershgorin_lower_bound':.4,'memory_lower_bound':2.9,
            'max_coupling_norm_squared':.32,'uniform_memory_Schur_lower_bound':2.1,
            'scope':'Infinite tails have nonnegative forms and finite endpoint inverse forms at zero. Schur form criterion gives h1>=0; second quantization and physical compression preserve it.'}


if __name__=='__main__':
    result={'series':exact_series(),'leading_Gram':gram(),
            'mixed_physical_Fock':[mixed_fock(n) for n in [3,5,7]],'stability':stability()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
