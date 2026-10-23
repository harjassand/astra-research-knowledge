#!/usr/bin/env python3
"""Exact normal-form check of the anisotropic corrector, without bath truncation."""
import argparse
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import platform
import resource
import sys
import time

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--representation',type=Path,default=Path(__file__).resolve().parents[1]/'representation/exact_representation.py')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    wall,cpu=time.perf_counter(),time.process_time()
    spec=importlib.util.spec_from_file_location('inherited_fock_rep',args.representation)
    rep=importlib.util.module_from_spec(spec); sys.modules[spec.name]=rep; spec.loader.exec_module(rep)
    add,mul,scale,star=rep.add,rep.mul,rep.scale,rep.adjoint
    sub=lambda x,y:add(x,scale(y,-1))
    comm=lambda x,y:sub(mul(x,y),mul(y,x))
    C=lambda x:add(*(mul(mul(rep.S[a],x),star(rep.S[a])) for a in (1,2)))
    alpha,beta,q=F(12,13),F(5,13),F(2,5)
    a1,a2=F(1,5),F(2,5)
    g1,g2=F(1,10),F(-1,30)
    assert a1+a2==1-q and g1*g1/a1+g2*g2/a2<q
    f1,f2=g1/a2,g2/a1
    r=q/(1-q)
    Sg=add(scale(rep.S[1],g1),scale(rep.S[2],g2))
    Sf=add(scale(rep.S[1],f1),scale(rep.S[2],f2))
    Dg=sub(star(Sg),Sg)
    gf=g1*f1+g2*f2
    ig=rep.I_G
    rho=[[rep.G(q),ig*g1,ig*g2],[-ig*g1,rep.G(a1),rep.G()],[-ig*g2,rep.G(),rep.G(a2)]]
    V=rep.port_matrix(alpha,beta)
    def T(x):
        return add(*(scale(mul(mul(star(V[b][j]),x),V[b][i]),rho[i][j])
                     for i in range(3) for j in range(3) for b in range(3) if rho[i][j]))
    assert T(rep.ONE)==rep.ONE
    Fk=[Sf]
    for k in range(5):
        Fk.append(C(Fk[-1]))
    for k in range(1,5):
        delta=sub(Fk[k-1],Fk[k])
        expected=add(scale(Fk[k],beta*beta),scale(Fk[k+1],alpha*alpha*q),
                     scale(Fk[k-1],alpha*alpha*(1-q)),
                     scale(add(mul(delta,star(Sg)),mul(Sg,delta)),-alpha*beta))
        assert T(Fk[k])==expected
    for N in range(5):
        B=add(*(scale(Fk[k],r**k) for k in range(N+1)))
        expected=add(scale(Sg,alpha*alpha),scale(mul(Sf,rep.ROOT),ig*alpha*beta*q),
                     scale(rep.ROOT,-ig*alpha*alpha*gf),scale(comm(Dg,B),alpha*beta),
                     scale(sub(Fk[N],Fk[N+1]),alpha*alpha*q*r**N))
        assert sub(B,T(B))==expected
        comm_expected=add(scale(rep.ONE,gf),mul(Sf,Sg),
                          scale(add(mul(B,star(Sg)),mul(Sg,B)),-(1-r)),
                          scale(add(mul(Fk[N],star(Sg)),mul(Sg,Fk[N])),-r**(N+1)))
        assert comm(Dg,B)==comm_expected
    result={'scope':'Finite exact anisotropic operator identities in the infinite-bath algebra; analytic norm limit is in coherent_moments.md.',
            'parameters':dict(alpha=str(alpha),beta=str(beta),q=str(q),a1=str(a1),a2=str(a2),g1=str(g1),g2=str(g2),f1=str(f1),f2=str(f2)),
            'checks':{'unitality':'passed','hierarchy_k_1_to_4':'passed','corrector_N_0_to_4':'passed','commutator_N_0_to_4':'passed'},
            'resources':{'wall_seconds':time.perf_counter()-wall,'cpu_seconds':time.process_time()-cpu,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python':platform.python_version(),'discovery_cost':'not independently metered'}}
    out=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(out)
    print(out,end='')

if __name__=='__main__':
    main()

