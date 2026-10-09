#!/usr/bin/env python3
"""Finite checks for QUANTUM_ORBIT_EXTENSION.md; no formal certification.
Requirements: numpy and sympy. No network access. Works under Python -O.
"""
from __future__ import annotations
import argparse, json, platform, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp

checks=[]
def require(ok, name, kind, **data):
    if not ok: raise RuntimeError(f'{name}: {data}')
    checks.append(dict(name=name,status='PASS',kind=kind,**data))

def unitary(rng,D):
    Z=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D))
    Q,R=np.linalg.qr(Z)
    phase=np.diag(R)/np.abs(np.diag(R))
    return Q*phase.conj()

def run():
    for D in range(2,21):
        r2=F(D-1,D)
        variance=(F(2,D*(D+1))-F(1,D*D))/(r2*r2)
        require(variance==F(1,D*D-1),f'Haar overlap variance D={D}',
                'exact rational arithmetic')
    R=sp.Matrix([[sp.Rational(3,5),-sp.Rational(4,5),0],
                 [sp.Rational(4,5),sp.Rational(3,5),0],[0,0,1]])
    S=sp.Matrix([[1,0,0],[0,sp.Rational(5,13),-sp.Rational(12,13)],
                 [0,sp.Rational(12,13),sp.Rational(5,13)]])
    U=R*S
    for eigen in [(3,1,-4),(2,2,-4),(4,-2,-2),(5,-1,-4)]:
        A=sp.diag(*eigen); Ap=U*A*U.T
        lhs=sp.trace((A-Ap)**2)
        rhs=sum((eigen[i]-eigen[j])**2*U[i,j]**2 for i in range(3) for j in range(3))
        require(sp.simplify(lhs-rhs)==0,f'spectral distance identity {eigen}',
                'exact symbolic algebra')
        gaps=[eigen[i]-eigen[i+1] for i in range(2)];k=1+int(np.argmax(gaps));gap=gaps[k-1]
        P=sp.diag(*([1]*k+[0]*(3-k))); Pp=U*P*U.T
        rhs_bound=gap**2*sp.trace((P-Pp)**2)
        require(bool(lhs>=rhs_bound),f'spectral projection bound {eigen}',
                'exact symbolic algebra')
    rng=np.random.default_rng(20261010)
    for D in range(2,8):
        for rep in range(12):
            lam=np.sort(rng.normal(size=D))[::-1];lam-=lam.mean();lam/=np.linalg.norm(lam)
            k=1+int(np.argmax(lam[:-1]-lam[1:]));gap=lam[k-1]-lam[k]
            require(gap>=1/(np.sqrt(D)*(D-1))-1e-13,
                    f'uniform gap D={D},run={rep}','seeded numerical diagnostic')
            U=unitary(rng,D);A=np.diag(lam);Ap=U@A@U.conj().T
            P=np.diag([1.]*k+[0.]*(D-k));Pp=U@P@U.conj().T
            lhs=np.linalg.norm(A-Ap,'fro')**2;rhs=gap**2*np.linalg.norm(P-Pp,'fro')**2
            require(lhs+1e-12>=rhs,f'projection stability D={D},run={rep}',
                    'seeded numerical diagnostic',lhs=float(lhs),rhs=float(rhs))
            r0=np.sqrt((D-1)/D);psi=U[:,0];rho=np.outer(psi,psi.conj());X=(rho-np.eye(D)/D)/r0
            B=np.diag(lam);delta=1/(D*D-1)
            effect=(np.eye(D)+delta*B/r0)/2
            p=float(np.trace(rho@effect).real);p2=(1+delta*np.trace(B@X).real)/2
            require(abs(p-p2)<2e-13 and np.linalg.eigvalsh(effect).min()>=-1e-13
                    and np.linalg.eigvalsh(effect).max()<=1+1e-13,
                    f'quantum response D={D},run={rep}','seeded numerical diagnostic')
            r2=0.01
            phi=np.zeros(D);phi[0]=np.sqrt(1-r2);phi[-1]=np.sqrt(r2)
            expectation=float(phi@A@phi);lower=(1-D*r2)*lam[0]
            require(expectation+1e-13>=lower,
                    f'quadratic support loss D={D},run={rep}','seeded numerical diagnostic')
    # Matrix graph charts: projection formula, norm and rank for exact complex Z.
    Z=sp.Matrix([[sp.Rational(1,7),sp.I/11],[sp.Rational(-2,13),sp.Rational(1,17)]])
    W=sp.eye(2).col_join(Z);Q=W*(sp.eye(2)+Z.conjugate().T*Z).inv()*W.conjugate().T
    require(sp.simplify(Q*Q-Q)==sp.zeros(4) and Q==Q.conjugate().T and sp.trace(Q)==2,
            'complex Grassmann graph projection','exact symbolic algebra')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,default=Path('quantum_verification_receipt.json'))
    args=ap.parse_args();run()
    result={'status':'PASS','check_count':len(checks),'optimization_flag':sys.flags.optimize,
      'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__,
      'scope':'Finite algebraic and numerical checks only. The uniform volume bounds, Haar integrals, all-horizon theorem, external correctness and novelty are not computationally certified.',
      'checks':checks}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','check_count','optimization_flag','scope']},indent=2))
if __name__=='__main__':main()
