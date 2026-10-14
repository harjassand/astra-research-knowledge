"""Exact continuum (not lattice) certificate using local Jacobi polynomials.
All tensor contractions and beta moments are rational. Trial degree leakage is charged.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from functools import reduce
import json, math, subprocess, sys, time
import numpy as np
from jacobi_gate import local_basis
sys.set_int_max_str_digits(0);BASE=Path(__file__).resolve().parent

def lcm_den(xs):
    return reduce(math.lcm,(F(x).denominator for x in xs),1)

def validate(prefix,degree_sector=2,bits=48):
    p=Path(prefix);meta=json.loads(p.with_suffix('.json').read_text());n=meta['n'];q=F(meta['q']);rho=F(meta['rho']);eps=F(meta['eps']);kappa=q*rho
    degree=meta['degree'];d=degree+2;info=local_basis(q,rho,degree+1);X=info['X'];lam=info['lambda'];norms=info['norms'];L=lcm_den(lam)
    I=np.eye(d,dtype=int).astype(object);h=np.diag([x*L for x in lam]);C=(1-eps)*X/F(L)
    O=[]
    for i in range(n):
        o=(F(1) if i==0 else eps)*np.diag(lam)
        if i==0:o=o+kappa*eps*I
        if i==n-1:o=o+kappa*(1-eps)*X
        O.append(o)
    D=lcm_den(list(C.flat)+[x for o in O for x in o.flat]);G=lcm_den(norms)
    grams=[int(x*G) for x in norms]
    lines=[f'{n} {d} {D} {G}', ' '.join(map(str,grams))]
    for i in range(n):
        w=np.zeros((3,3,d,d),dtype=object);w[0,0]=I;w[1,0]=h;w[2,2]=I;w[2,1]=C*D;w[2,0]=O[i]*D
        assert all(F(x).denominator==1 for x in w.flat)
        lines.append(' '.join(str(int(x)) for x in w.flat))
    f=np.load(p.with_suffix('.npz'));params=0
    for i in range(n):
        a=f['a'+str(i)];params+=a.size
        a=a/np.sqrt(np.array([float(x) for x in norms[:degree+1]]))[None,:,None]
        aa=np.zeros((a.shape[0],d,a.shape[2]));aa[:,:degree+1,:]=a
        maximum=float(np.max(np.abs(aa))); exponent=bits-max(0,math.ceil(math.log2(maximum))) if maximum else bits
        z=np.rint(aa*(2.0**exponent)).astype(np.int64);assert np.max(np.abs(z))<2**62
        lines.append(f'{a.shape[0]} {a.shape[2]} {exponent}');lines.append(' '.join(str(int(v)) for v in z.flat))
    text=p.with_suffix('.continuum.txt');text.write_text('\n'.join(lines)+'\n');t=time.perf_counter()
    result=subprocess.run([str(BASE/'exact_continuum'),str(text),str(degree_sector)],text=True,capture_output=True,check=True)
    p.with_suffix('.continuum_raw.txt').write_text(result.stdout)
    ints={key:int(value) for key,value in (line.split() for line in result.stdout.splitlines())}
    S=2**ints['p'];GN=G**n
    bv=F(ints['source'],S);hy=F(ints['Hsource'],D*S);energy=F(ints['energy'],D*S*S*GN)
    yn=F(ints['Hnorm'],D*D*S*S*GN);ynlow=F(ints['Hnorm_low'],D*D*S*S*GN)
    rr=1-2*hy+yn;rrlow=1-2*hy+ynlow;r0=1-hy
    assert rr>=rrlow>=r0*r0>=0
    ws=[F(ints['sector'+str(j)],D*D*S*S*GN) for j in range(degree_sector+1)]
    assert ws[0]==hy*hy
    ws[0]=r0*r0;tail=rrlow-sum(ws);assert tail>=0 and all(w>=0 for w in ws)
    gap=sum(w/(eps*(kappa+rho*j)) for j,w in enumerate(ws))
    gap+=tail/(eps*(kappa+rho*(degree_sector+1)))
    gap+=(rr-rrlow)/(eps*(kappa+2*(1+rho)))
    lower=2*bv-energy;upper=lower+gap;assert lower>0
    def out(fr,places=10,up=False):
        sc=10**places;num=fr.numerator*sc;den=fr.denominator;v=(num+den-1)//den if up else num//den
        return f'{v//sc}.{v%sc:0{places}d}'
    res={'continuous':True,'n':n,'q':str(q),'rho':str(rho),'eps':str(eps),'trial_degree':degree,'residual_local_degree':degree+1,'core_parameters':params,'max_rank':max(f['a'+str(i)].shape[2] for i in range(n)),'lower':out(lower),'upper':out(upper,up=True),'ratio_upper':out(upper/lower,up=True),'residual_sq':float(rr),'residual_binary_sector_sq':float(rrlow),'residual_higher_modes_sq':float(rr-rrlow),'gap':out(gap,up=True),'crude_gap':out(rr/(eps*kappa),up=True),'validation_seconds':time.perf_counter()-t,'exact_integer_contractions':True,'equilibrium_samples':0,'lattice_discretization':False,'bits':bits}
    p.with_suffix('.certificate.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2),flush=True);return res
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('prefix');p.add_argument('--degree-sector',type=int,default=2);p.add_argument('--bits',type=int,default=48);a=p.parse_args();validate(a.prefix,a.degree_sector,a.bits)
