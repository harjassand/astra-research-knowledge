"""Exact finite-bandwidth spin/auxiliary filter identities.

The graph here is a two-neighbor star, not the asymptotic expander.
First-order identities hold for a full data operator basis. The
second-order identity is checked on diagonal data weights only, which
is exactly the scope needed for the proposed positive moment.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/spectral_memory_20261101'
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
down=s.Matrix([[0,1],[0,0]]);up=down.T;num=up*down


def ten(*args):return s.kronecker_product(*args)
def comm(a,b):return a*b-b*a
def adj(a):return a.conjugate().T
def diss(j,a):
    b=adj(j)*j
    return adj(j)*a*j-(b*a+a*b)/2
def unit(n,i,j):
    a=s.zeros(n);a[i,j]=1;return a


def main():
    J=s.Integer(2);omega=4*J;Gamma=s.S(1)
    xi=ten(X,I,I)
    hd=-J*(ten(Z,Z,I)+ten(Z,I,Z))
    delta=xi*hd*xi-hd
    projectors={d:s.diag(*(int(delta[i,i]==d) for i in range(8))) for d in (-4*J,0,4*J)}
    assert sum(projectors.values(),s.zeros(8))==s.eye(8)
    hfast=ten(hd,I)+omega*ten(s.eye(8),num)
    v=ten(xi,X);loss=ten(s.eye(8),down)
    g=s.zeros(16);jumps={};rates={}
    for d,p in projectors.items():
        j=xi*p;jumps[d]=j
        assert comm(hd,j)==d*j
        c=1/(Gamma/2-s.I*(omega+d))
        a=c*ten(j,up);g+=a+adj(a)
        rates[d]=s.simplify(Gamma/((Gamma/2)**2+(omega+d)**2))
    def fast(a):return s.I*comm(hfast,a)+Gamma*diss(loss,a)
    def aa(a):return s.I*comm(g,a)
    def hh(a):return s.I*comm(v,a)
    assert s.simplify(fast(g)+v)==s.zeros(16)
    assert s.simplify(diss(loss,g)+g/2)==s.zeros(16)
    # This controls fast-Hamiltonian commutators without a factor J/Gamma.
    assert s.simplify(s.I*comm(hfast,g)+v-g/2)==s.zeros(16)
    # The ground-to-excited singular values are the source-resolvent
    # magnitudes, bounded by 2/Gamma independently of the detunings.
    sq=s.simplify(4*s.eye(16)-g*g)
    assert sq==s.diag(*sq.diagonal()) and all(a>=0 for a in sq.diagonal())
    iso=ten(s.eye(8),s.Matrix([1,0]))
    basis_checks=0;diag_checks=0
    for a in range(8):
        for b in range(8):
            xx=ten(unit(8,a,b),I)
            # [D_fast^*, A] + H_V^* =0 on ALL controller states.
            first=fast(aa(xx))-aa(fast(xx))+hh(xx)
            assert s.simplify(first)==s.zeros(16)
            basis_checks+=1
        x=unit(8,a,a);xx=ten(x,I)
        second=fast(aa(aa(xx)))/2+hh(aa(xx))
        wanted=sum((rates[d]*diss(j,x) for d,j in jumps.items()),s.zeros(8))
        assert s.simplify(adj(iso)*second*iso-wanted)==s.zeros(8)
        diag_checks+=1
    parity=ten(X,X,X,I)
    assert comm(parity,hfast)==s.zeros(16)
    assert comm(parity,v)==s.zeros(16) and comm(parity,g)==s.zeros(16)
    assert comm(parity,loss)==s.zeros(16)
    # An orientation-resolved version has the SAME classical transitions
    # but loses the coherent record between complementary error states.
    jup=jumps[4*J]
    split=[jup*(s.eye(8)+ten(Z,I,I))/2,jup*(s.eye(8)-ten(Z,I,I))/2]
    coherence=unit(8,0,7)
    whole=jup*coherence*adj(jup)
    resolved=sum((j*coherence*adj(j) for j in split),s.zeros(8))
    assert whole!=s.zeros(8) and resolved==s.zeros(8)
    assert comm(ten(X,X,X),jup)==s.zeros(8)
    assert all(comm(ten(X,X,X),j)!=s.zeros(8) for j in split)
    out={'data_qubits':3,'auxiliary_qubits':1,'star_degree':2,'J':str(J),'Gamma':str(Gamma),
         'omega':str(omega),'exact_full_data_operator_basis_checks':basis_checks,
         'exact_diagonal_second_order_checks':diag_checks,
         'Lorentzian_rates_per_g_squared':{str(d):str(r) for d,r in rates.items()},
         'Poisson_resolvent_identity':True,'G_norm_upper':'2/Gamma',
         'fast_commutator_bound_independent_of_J':True,'all_physical_primitives_strong_symmetry':True,
         'orientation_resolution_destroys_error_coherence':True,
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Exact finite algebra; the second-order moment identity is diagonal only; no classical-rate substitution for full quantum dynamics or asymptotic code verification'}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'spectral_filter_algebra.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'passed':True,'full_basis':basis_checks,'diagonal':diag_checks}))


if __name__=='__main__':main()
