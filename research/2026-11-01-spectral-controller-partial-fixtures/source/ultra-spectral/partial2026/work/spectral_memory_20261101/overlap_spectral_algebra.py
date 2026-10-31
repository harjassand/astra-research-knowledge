"""Two overlapping spectral controllers, including finite flag weights."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/spectral_memory_20261101'
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
down=s.Matrix([[0,1],[0,0]]);up=down.T;num=up*down
def ten(*a):return s.kronecker_product(*a)
def com(a,b):return a*b-b*a
def adj(a):return a.conjugate().T
def diss(j,x):
    a=adj(j)*j;return adj(j)*x*j-(a*x+x*a)/2
def unit(d,i,j):
    a=s.zeros(d);a[i,j]=1;return a


def main():
    hd=-2*ten(Z,Z);omega=s.Integer(4)
    h0=ten(hd,I,I)+omega*ten(s.eye(4),num,I)+omega*ten(s.eye(4),I,num)
    vs=[];gs=[];ls=[];desired=[]
    for i in range(2):
        xi=ten(X,I) if i==0 else ten(I,X)
        delta=xi*hd*xi-hd
        flag=ten(up,I) if i==0 else ten(I,up)
        vi=ten(xi,flag+adj(flag));gi=s.zeros(16);terms=[]
        for d in (-4,4):
            p=s.diag(*(int(delta[j,j]==d) for j in range(4)))
            j=xi*p;c=1/(s.Rational(1,2)-s.I*(omega+d))
            a=c*ten(j,flag);gi+=a+adj(a)
            terms.append((s.simplify(1/(s.Rational(1,4)+(omega+d)**2)),j))
        vs.append(vi);gs.append(gi);ls.append(ten(s.eye(4),adj(flag)));desired.append(terms)
    vv=sum(vs,s.zeros(16))
    def fast(x):return s.I*com(h0,x)+sum((diss(j,x) for j in ls),s.zeros(16))
    def aa(i,x):return s.I*com(gs[i],x)
    def atotal(x):return aa(0,x)+aa(1,x)
    def asecond(x):return aa(0,aa(0,x))/2+aa(0,aa(1,x))+aa(1,aa(1,x))/2
    def invsecond(x):return aa(0,aa(0,x))/2+aa(1,aa(0,x))+aa(1,aa(1,x))/2
    def hv(x):return s.I*com(vv,x)
    iso=ten(s.eye(4),s.Matrix([1,0,0,0]))
    charge=[ten(Z,I,Z,I),ten(I,Z,I,Z)]
    assert all(com(a,h0)==s.zeros(16) and com(a,vv)==s.zeros(16) for a in charge)
    assert all(com(a,g)==s.zeros(16) for a in charge for g in gs)
    assert com(gs[0],gs[1])!=s.zeros(16)
    for a in range(4):
        for b in range(4):
            xx=ten(unit(4,a,b),s.eye(4))
            assert s.simplify(fast(atotal(xx))-atotal(fast(xx))+hv(xx))==s.zeros(16)
    checked=0
    for weight in (1,2,3):
        fc=s.diag(1,weight,weight,weight**2)
        for a in range(4):
            x=unit(4,a,a);xx=ten(x,fc)
            # Full second coefficient e^-A (D+eps H) e^A for the
            # ordered two-center frame, including nonzero D(xx).
            coeff=fast(asecond(xx))-atotal(fast(atotal(xx)))+invsecond(fast(xx))
            coeff+=hv(atotal(xx))-atotal(hv(xx))
            wanted=sum((rate*diss(j,x) for terms in desired for rate,j in terms),s.zeros(4))
            assert s.simplify(adj(iso)*coeff*iso-wanted)==s.zeros(4)
            checked+=1
    # All normal-frame ground-to-ground Hamiltonian terms must be
    # diagonal in the data basis, and a dressed loss can flip only its
    # own center in that block, because these charges are exact.
    out={'full_data_first_order_basis':16,'weighted_ground_second_order_checks':checked,
         'record_weight_values':[1,2,3],'overlapping_centers_noncommute':True,
         'second_ground_block_independent_of_record_weight':True,
         'local_spin_record_charges_exact':True,'ordered_two_layer_frame':True,
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Exact two-site finite algebra; not an expanding family or a global quantum-memory simulation'}
    OUT.mkdir(parents=True,exist_ok=True);p=OUT/'overlap_spectral_algebra.json';p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(p),'passed':True,'weighted_ground_checks':checked}))


if __name__=='__main__':main()
