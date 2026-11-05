"""Finite-angle checks of the boundary-charge compression theorem.

Run from any directory. This checks physical channels, not a spectral search.
"""
from pathlib import Path
import json, math
import numpy as np
HERE = Path(__file__).resolve().parent
PAULI = [np.array([[0,1],[1,0]],complex), np.array([[0,-1j],[1j,0]]), np.diag([1.,-1.])]

def swap(n,i,j):
    out=np.zeros((2**n,2**n),complex)
    for a in range(2**n):
        f=((a>>(n-1-i))^(a>>(n-1-j)))&1
        b=a^(f<<(n-1-i))^(f<<(n-1-j)); out[b,a]=1
    return out

def energy(n):
    return sum((swap(n,j,j+1) for j in range(n-1)),np.zeros((2**n,2**n),complex))

def monodromy(n,theta):
    d=2**(n+1); out=np.eye(d,dtype=complex)
    for j in range(1,n+1):
        out=(np.cos(theta)*np.eye(d)+1j*np.sin(theta)*swap(n+1,0,j))@out
    return out

def source_identity_part(x,d):
    z=x.reshape(2,d,2,d)
    return np.kron(np.eye(2),(z[0,:,0,:]+z[1,:,1,:])/2)

def norm2(x): return float(np.vdot(x,x).real/x.shape[0])

def grid_effects(h,w):
    e,v=np.linalg.eigh(h); effects=[]; ranks=[]
    for j in range(math.floor(float(e[0])/w)-1,math.ceil(float(e[-1])/w)+2):
        z=(e-j*w)/w
        f=np.where(np.abs(z)<1-1e-12,np.cos(np.pi*z/2),0.)
        if np.max(np.abs(f))<1e-12: continue
        effects.append((v*f)@v.conj().T)
        ranks.append(int(np.count_nonzero(f>1e-12)))
    return effects,ranks

def binary_effects(h):
    n=round(math.log2(h.shape[0])); ell=n-1
    z=2*h-ell*np.eye(2**n); e,v=np.linalg.eigh(z); w=np.sqrt(ell)/4
    angle=np.clip((e+w)/(2*w),0,1)*np.pi/2
    fs=[np.cos(angle),np.sin(angle)]
    for f in fs: f[np.abs(f)<1e-12]=0.
    return [(v*f)@v.conj().T for f in fs],[int(np.count_nonzero(f>1e-12)) for f in fs]

def luders(x,effects):
    return sum((a@x@a for a in effects),np.zeros_like(x))

def physical_coefficients(n,theta,effects):
    d=2**n; u=monodromy(n,theta)
    w=u@np.kron(PAULI[2],np.eye(d))@u.conj().T
    p=source_identity_part(w,d); q=w-p
    aa=[np.kron(np.eye(2),a) for a in effects]
    return float(np.vdot(p,luders(p,aa)).real/(2*d)),float(np.vdot(q,luders(q,aa)).real/(2*d))

def run():
    records=[]
    for n in range(2,8):
        d=2**n; h=energy(n); ell=n-1; z=2*h-ell*np.eye(d); z2=z@z
        binary,ranks=binary_effects(h)
        records.append(dict(kind='moments',n=n,m2=float(np.trace(z2).real/d),m4=float(np.trace(z2@z2).real/d),m2_target=3*ell,m4_target=27*ell**2-30*ell+24,binary_ranks=ranks,rank_fraction_bound=47/48,rank_fraction=max(ranks)/d))
        if n>5: continue
        hh=np.kron(np.eye(2),h); p1,pn=swap(n+1,0,1),swap(n+1,0,n)
        for theta in [.07,.37,.9]:
            s4=np.sin(theta)**4; r=1-s4; u=monodromy(n,theta); comm=hh@u-u@hh
            heis=u.conj().T@hh@u; qheis=heis-source_identity_part(heis,d)
            records.append(dict(kind='boundary',n=n,theta=theta,train_residual=float(np.linalg.norm(comm-s4**.5*(u@p1-pn@u))),comm_norm2=norm2(comm),comm_target=1.5*s4,charge_loss=4*norm2(qheis)/3,charge_loss_target=s4*(1+r**(n-1))))
            for mode,width in [('grid',.7),('grid',1.3),('binary',None)]:
                if mode=='grid':
                    effects,eranks=grid_effects(h,width); bound=np.pi**2*s4*(1+r**(n-1))/(4*width**2)
                else:
                    effects,eranks=binary,ranks; bound=4*np.pi**2*s4*(1+r**(n-1))/(n-1)
                b,rem=physical_coefficients(n,theta,effects); delta=1-b-rem
                records.append(dict(kind='instrument',n=n,theta=theta,mode=mode,width=width,outcomes=len(effects),ranks=eranks,completeness_residual=float(np.linalg.norm(sum(a@a for a in effects)-np.eye(d))),b=b,h=rem,delta=delta,delta_bound=float(bound),slack=float(bound-delta)))
    for n in [2,3]:
        effects,_=grid_effects(energy(n),.7)
        for theta in [.13,.53]:
            b,h=physical_coefficients(n,theta,effects); dn=2**n; db=dn*dn; u=monodromy(2*n,theta)
            w=u@np.kron(PAULI[2],np.eye(db))@u.conj().T; p=source_identity_part(w,db); q=w-p
            left=[np.kron(np.eye(2),np.kron(a,np.eye(dn))) for a in effects]
            right=[np.kron(np.eye(2),np.kron(np.eye(dn),a)) for a in effects]
            direct_a=float(np.vdot(p,luders(luders(p,left),right)).real/(2*db))
            direct_q=float(np.vdot(q,luders(luders(q,left),right)).real/(2*db))
            records.append(dict(kind='two_blocks',n=n,theta=theta,direct_a=direct_a,recursion_a=b*(1+h),direct_q=direct_q,recursion_q=h*h,max_residual=max(abs(direct_a-b*(1+h)),abs(direct_q-h*h))))
    (HERE/'train_energy_checks.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in records))
    print(json.dumps(dict(records=len(records),max_train_residual=max(x['train_residual'] for x in records if x['kind']=='boundary'),max_charge_residual=max(abs(x['charge_loss']-x['charge_loss_target']) for x in records if x['kind']=='boundary'),min_instrument_slack=min(x['slack'] for x in records if x['kind']=='instrument'),max_recursion_residual=max(x['max_residual'] for x in records if x['kind']=='two_blocks'),elementary_packing_factor=(47/48)**33)),flush=True)

if __name__=='__main__': run()
