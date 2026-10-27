"""Exact acquisition of a locally exact, paid raw-record replacement module.

Compilation, runtime and independent checking use only the standard library.
The exact simplex backend has no polynomial runtime guarantee here. Every returned
answer has a rational primal/dual certificate; checks fail closed.
"""
from __future__ import annotations
import json, sys, time, platform
from pathlib import Path
from fractions import Fraction as F


def matrix(raw):
    out=[[F(x) for x in row] for row in raw]
    if not out or not out[0] or any(len(row)!=len(out[0]) for row in out):
        raise ValueError('empty/ragged channel')
    if any(x<0 for row in out for x in row): raise ValueError('negative channel entry')
    if any(sum(row[x] for row in out)!=1 for x in range(len(out[0]))):
        raise ValueError('columns must sum to one')
    return out


def constraints(K,L):
    ny,nx,nz=len(K),len(K[0]),len(L)
    if len(L[0])!=nx: raise ValueError('channels have different input alphabets')
    A=[];b=[];names=[]
    def add(a,rhs,name): A.append(a); b.append(F(rhs)); names.append(name)
    for z in range(nz):
        a=[F(0)]*(ny*nz+1)
        for y in range(ny):a[y*nz+z]=F(1)
        add(a,1,f'column_{z}')
    for y in range(ny):
        for x in range(nx):
            a=[F(0)]*(ny*nz+1)
            for z in range(nz):a[y*nz+z]=L[z][x]
            add(a,K[y][x],f'output_{y}_{x}')
    for x in range(nx):
        add([-L[z][x] for y in range(ny) for z in range(nz)]+[F(-1)],-1,f'query_{x}')
    return A,b,names


def compile_channels(data):
    started=time.perf_counter();cpu=time.process_time()
    from exact_simplex import solve
    K=matrix(data['K']);L=matrix(data['L']);ny,nx,nz=len(K),len(K[0]),len(L)
    A,b,names=constraints(K,L)
    # Set v=1-q, maximize v. All transformed RHS are nonnegative,
    # so U=0,v=0 is a supplied feasible basis, even at zero entries.
    Av=[row[:-1]+[-row[-1]] for row in A]
    bv=[rhs-row[-1] for row,rhs in zip(A,b)]
    Av.append([F(0)]*(ny*nz)+[F(1)]);bv.append(F(1))
    obj,p,lam,stats=solve(Av,bv,[F(0)]*(ny*nz)+[F(1)])
    q=1-p[-1];primal=p[:-1]+[q]
    if q:
        totalpi=sum(lam[-nx-1:-1])
        if lam[-1] or totalpi<=0:raise ArithmeticError('dual conversion failed')
        dual=[v/totalpi for v in lam[:-1]]
    else:dual=[F(0)]*len(b)
    cert={
      'schema':'charged-classical-replacement-v1','input_id':data.get('id','unnamed'),
      'K':[[str(v) for v in row] for row in K],
      'L':[[str(v) for v in row] for row in L],
      'U':[[str(primal[y*nz+z]) for z in range(nz)] for y in range(ny)],
      'q':str(q),
      'dual':[{'constraint':name,'weight':str(weight)} for name,weight in zip(names,dual) if weight],
      'acquisition':{'backend':'standard-library rational simplex with Bland rule',
                     'python':platform.python_version(),**stats},
      'contract':'Already classical raw X, one supplied L record per round, charged raw reads; local exactness before every fresh round; cost flags private to controller.'}
    # Separate standard-library verifier is part of the output acceptance gate.
    from verify_certificate import verify
    cert['checked']=verify(cert)
    if obj!=1-q:raise ArithmeticError('invalid transformed objective')
    cert['acquisition']['construction_and_check_wall_s']=time.perf_counter()-started
    cert['acquisition']['construction_and_check_cpu_s']=time.process_time()-cpu
    return cert


if __name__=='__main__':
    raw=json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv)>1 else json.load(sys.stdin)
    answer=compile_channels(raw)
    out=json.dumps(answer,indent=2)+'\n'
    if len(sys.argv)>2:Path(sys.argv[2]).write_text(out)
    else:sys.stdout.write(out)
