"""Exact damped-subdivision algebra for overlapping noncommuting terms.

No effective-channel or asymptotic memory conclusion follows from these
finite identities alone. The companion proof treats all excited sectors.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/arity_transfer_20261101'
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
down=s.Matrix([[0,1],[0,0]]);num=down.T*down


def ten(*args):return s.kronecker_product(*args)
def comm(a,b):return a*b-b*a
def diss(j,x):
    a=j.conjugate().T*j
    return j.conjugate().T*x*j-(a*x+x*a)/2


def main():
    # Two anticommuting weight-four target Paulis, each split into disjoint
    # weight-two pieces. h_0=+2, h_1=-2, so t=sqrt(|h|/2)=1 exactly.
    aa=[ten(X,X,I,I),ten(Z,X,I,I)]
    bb=ten(I,I,X,X)
    pp=[a*bb for a in aa]
    assert pp[0]*pp[1]==-pp[1]*pp[0]
    signs=[-1,1]
    kk=[aa[v]+signs[v]*bb for v in range(2)]
    vv=[ten(kk[0],X,I),ten(kk[1],I,X)]
    gg=[ten(kk[0],Y,I),ten(kk[1],I,Y)]
    nn=ten(s.eye(16),num,I)+ten(s.eye(16),I,num)
    vs=sum(vv,s.zeros(64))
    first=vs-s.I*comm(sum(gg,s.zeros(64)),nn)
    assert first==s.zeros(64)
    # R=exp(-i eps G_1)exp(-i eps G_0), H=eps^-2 N+eps^-1 V.
    second=-s.I*comm(sum(gg,s.zeros(64)),vs)
    second-=comm(gg[0],comm(gg[0],nn))/2
    second-=comm(gg[1],comm(gg[0],nn))
    second-=comm(gg[1],comm(gg[1],nn))/2
    iso=ten(s.eye(16),s.Matrix([1,0,0,0]))
    target=2*pp[0]-2*pp[1]
    assert iso.T*second*iso==target-4*s.eye(16)
    # The cross-center term is zero in the record-ground block, but is
    # not a negligible operator on all controller states.
    cross=-s.I*comm(gg[0],vv[1])
    assert cross!=s.zeros(64) and iso.T*cross*iso==s.zeros(16)
    residual=second-ten(target-4*s.eye(16),s.eye(4))
    assert iso.T*residual*iso==s.zeros(16)
    # First-order conjugated damping has zero ground block for a genuinely
    # noncommuting data weight and finite record excitation weight.
    fdata=s.diag(*(s.Integer(2)**j.bit_count() for j in range(16)))
    fflag=s.diag(1,3,3,9)
    ff=ten(fdata,fflag)
    checked=0
    for v in range(2):
        loss=ten(s.eye(16),down,I) if v==0 else ten(s.eye(16),I,down)
        action=lambda a:s.I*comm(gg[v],a)
        dfirst=diss(loss,action(ff))-action(diss(loss,ff))
        assert dfirst!=s.zeros(64)
        assert iso.T*dfirst*iso==s.zeros(16)
        checked+=1
    # The degree-reducing fork needs a counterterm. Omitting it leaves an
    # unwanted old-port interaction, even in the controller ground block.
    p=ten(Y,I,I);q=ten(I,X,I);r=ten(I,I,X)
    left=s.Integer(2);right=s.Integer(-3)
    k=(p-left*q-right*r)/s.sqrt(2)
    counter=left*right*q*r
    wanted=left*p*q+right*p*r
    assert s.simplify(-k*k+counter-wanted)==-7*s.eye(8)
    assert s.simplify(-k*k-wanted)!=-7*s.eye(8)
    out={'first_H_order_cancels_on_full_controller_space':True,
         'target_terms_noncommute':True,'exact_ground_second_order_target':'2 XXXX - 2 ZXXX, minus scalar 4 I',
         'cross_controller_residual_is_nonzero':True,'cross_residual_ground_block_zero':True,
         'conjugated_damping_first_order_ground_checks':checked,
         'target_max_arity':4,'physical_coupler_max_arity':3,
         'fork_counterterm_exact':True,'fork_coupler_arity':2,
         'scope':'Exact two-gadget algebra; not an all-size transfer theorem or hardware validation',
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'subdivision_algebra.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'passed':True}))


if __name__=='__main__':main()
