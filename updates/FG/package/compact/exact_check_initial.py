"""Export a dyadic tensor witness and validate all-state energy and residual exactly."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json, math, subprocess, sys, time
import numpy as np
BASE=Path(__file__).resolve().parent
sys.set_int_max_str_digits(0)

def exact_validate(prefix:str,eps:str|None=None,degree:int=-1,bits:int=48):
    p=Path(prefix); meta=json.loads(p.with_suffix('.json').read_text()); n=meta['n'];k=int(meta['k'])
    ef=F(eps if eps is not None else str(meta['eps']));q=F(1,k*k+1)
    f=np.load(p.with_suffix('.npz')); cores=[f['a'+str(i)] for i in range(n)]
    lines=[f'{n} {k} {ef.numerator} {ef.denominator}']; ps=[]
    for a in cores:
        maximum=float(np.max(np.abs(a)))
        exponent=bits-max(0,math.ceil(math.log2(maximum))) if maximum else bits
        scale=2.0**exponent
        z=np.rint(a*scale).astype(np.int64)
        assert np.max(np.abs(z))<2**62
        ps.append(exponent)
        lines.append(f'{a.shape[0]} {a.shape[2]} {exponent}')
        lines.append(' '.join(str(int(v)) for v in z.flat))
    text=p.with_suffix('.dyadic.txt');text.write_text('\n'.join(lines)+'\n')
    start=time.perf_counter()
    result=subprocess.run([str(BASE/'exact_contract'),str(text),str(degree)],text=True,capture_output=True,check=True)
    p.with_suffix('.exact_raw.txt').write_text(result.stdout)
    ints={key:int(value) for key,value in (line.split() for line in result.stdout.splitlines())}
    S=2**ints['p'];D=ints['D']
    bv=F(ints['source'],S);bHv=F(ints['Hsource'],D*S);ev=F(ints['energy'],D*S*S);hn=F(ints['Hnorm'],D*D*S*S)
    lower=2*bv-ev; r0=1-bHv; rr=1-2*bHv+hn
    assert rr>=r0*r0>=0
    if degree>=0:
        ws=[F(ints['sector'+str(j)],D*D*S*S) for j in range(degree+1)]
        assert ws[0]==bHv*bHv
        ws[0]=r0*r0
        assert all(x>=0 for x in ws)
        tail=rr-sum(ws);assert tail>=0
        gap=sum(w/(q+j) for j,w in enumerate(ws))/ef
        if degree<n:gap+=tail/(ef*(q+degree+1))
        else:assert tail==0
    else:
        ws=[r0*r0];tail=rr-ws[0];gap=ws[0]/(ef*q)+tail/(ef*(q+1))
    upper=lower+gap
    assert lower>0 and upper>=lower
    def out(fr,places=12,upper=False):
        sc=10**places;num=fr.numerator*sc;den=fr.denominator
        v=(num+den-1)//den if upper else num//den
        return f'{v//sc}.{v%sc:0{places}d}'
    res={'n':n,'states':str(2**n),'k':k,'q':str(q),'eps':str(ef),'core_parameters':sum(a.size for a in cores),'max_rank':max(a.shape[2] for a in cores),'dyadic_bits':bits,'total_dyadic_exponent':ints['p'],'validation_seconds':time.perf_counter()-start,'lower':out(lower),'upper':out(upper,upper=True),'ratio_upper':out(upper/lower,upper=True),'residual_sq':str(float(rr)),'source_residual':str(float(r0)),'degree':degree,'sector_weights':[str(float(w)) for w in ws], 'coarse_gap_upper':out(rr/(ef*q),upper=True),'sector_gap_upper':out(gap,upper=True),'exact_integer_contractions':True}
    p.with_suffix('.certificate.json').write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2),flush=True)
    return res

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('prefix');p.add_argument('--degree',type=int,default=-1);p.add_argument('--bits',type=int,default=48)
    a=p.parse_args();exact_validate(a.prefix,degree=a.degree,bits=a.bits)
