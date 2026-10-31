"""Exact finite-depth normal form for two overlapping CSS repair couplers."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/tanner_controller_20261101'
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Z=s.diag(1,-1)
down=s.Matrix([[0,1],[0,0]]); up=down.T; num=up*down


def adj(a):return a.conjugate().T
def ten(*args):return s.kronecker_product(*args)
def diss(j,x):
    a=adj(j)*j
    return adj(j)*x*j-(a*x+x*a)/2


def main():
    nu=s.Rational(1,2)
    pz=(s.eye(4)-ten(Z,Z))/2
    px=(s.eye(4)-ten(X,X))/2
    js=[ten(X,I)*pz,ten(Z,I)*px]
    assert pz*px==px*pz
    assert js[0]*js[1]!=js[1]*js[0]
    ts=[];gs=[];losses=[]
    for v,j in enumerate(js):
        flag=ten(up,I) if v==0 else ten(I,up)
        a=ten(j,flag)
        ts.append(a+adj(a))
        gs.append((1+s.I)*a+(1-s.I)*adj(a))
        losses.append(ten(s.eye(4),adj(flag)))
    number=ten(s.eye(4),ten(num,I)+ten(I,num))
    def fast(x):
        return sum((diss(a,x) for a in losses),s.zeros(16))+s.I*nu*(number*x-x*number)
    def fast_v(v,x):
        nv=ten(s.eye(4),ten(num,I) if v==0 else ten(I,num))
        return diss(losses[v],x)+s.I*nu*(nv*x-x*nv)
    def aa(v,x):return s.I*(gs[v]*x-x*gs[v])
    def hh(x):
        t=sum(ts,s.zeros(16))
        return s.I*(t*x-x*t)
    for v,g in enumerate(gs):assert s.simplify(fast(g)+ts[v])==s.zeros(16)
    iso=ten(s.eye(4),s.Matrix([1,0,0,0]))
    checked=0
    for u in range(4):
        for v in range(4):
            x=s.zeros(4);x[u,v]=1
            xx=ten(x,s.eye(4))
            first=aa(0,xx)+aa(1,xx)
            # W=exp(-i eps G_1)exp(-i eps G_0).
            second=aa(0,aa(0,xx))/2+aa(0,aa(1,xx))+aa(1,aa(1,xx))/2
            assert s.simplify(fast(first)+hh(xx))==s.zeros(16)
            coefficient=fast(second)+hh(first)
            wanted=2*sum((diss(j,x) for j in js),s.zeros(4))-s.I*(pz*x-x*pz+px*x-x*px)
            assert s.simplify(adj(iso)*coefficient*iso-wanted)==s.zeros(4)
            # The local Schur argument needs this for EACH primitive
            # center, rather than only after a possibly nonlocal sum.
            for center in range(2):
                hv=lambda y:s.I*(ts[center]*y-y*ts[center])
                assert s.simplify(fast_v(center,first)+hv(xx))==s.zeros(16)
                local_second=fast_v(center,second)+hv(first)
                pi=(pz,px)[center]
                local_wanted=2*diss(js[center],x)-s.I*(pi*x-x*pi)
                assert s.simplify(adj(iso)*local_second*iso-local_wanted)==s.zeros(4)
            checked+=1
    out={'exact_full_data_basis_checks':checked,'noncommuting_overlapping_css_writes':True,
         'finite_depth_order_included':True,'cross_controller_ground_terms_zero':True,
         'per_center_ground_identity_checks':2*checked,
         'first_order_full_controller_cancellation':True,
         'second_order':'2 sum_v D[J_v], plus syndrome Hamiltonian -sum_v Pi_v',
         'detuning':'1/2','program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Exact two-center symbolic algebra; not a Tanner family or a memory theorem'}
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/'overlap_algebra.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'passed':True,'basis_checks':checked}))


if __name__=='__main__':main()
