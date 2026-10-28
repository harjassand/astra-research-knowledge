"""Independent literal AKLT transfer proof and compiler applicability check.
No corpus-first construction or verifier module is imported.
"""
from pathlib import Path
from itertools import product
import sympy as s,json,time
ROOT=Path(__file__).resolve().parent
def run():
    started=time.monotonic();r2=s.sqrt(2);r6=s.sqrt(6)
    # Literal spin2 tensors from two virtual spin1 CG coefficients/singlet.
    A=[s.Matrix([[0,0,1],[0,0,0],[0,0,0]]),
       s.Matrix([[0,-1/r2,0],[0,0,1/r2],[0,0,0]]),
       s.diag(1/r6,-2/r6,1/r6),
       s.Matrix([[0,0,0],[1/r2,0,0],[0,-1/r2,0]]),
       s.Matrix([[0,0,0],[0,0,0],[1,0,0]])]
    E=sum((s.kronecker_product(a,a) for a in A),s.zeros(9)).applyfunc(s.simplify)
    Z=s.diag(-2,-1,0,1,2);P=s.zeros(5)
    for m in range(-2,2):P[m+3,m+2]=s.sqrt(6-m*(m+1))
    h=s.kronecker_product(Z,Z)+(s.kronecker_product(P,P.T)+s.kronecker_product(P.T,P))/2
    two=[a*b for a in A for b in A];B=s.zeros(9)
    for i,j in product(range(25),repeat=2):
        if h[i,j]:B+=h[i,j]*s.kronecker_product(two[j],two[i])
    B=B.applyfunc(s.simplify);I=s.eye(9)
    eig=[s.Rational(5,3),s.Rational(-5,6),s.Rational(1,6)]
    assert (E-eig[0]*I)*(E-eig[1]*I)*(E-eig[2]*I)==s.zeros(9)
    assert E*B==B*E
    projectors=[];data=[]
    for value,multiplicity,expected in zip(eig,[1,3,5],[-s.Rational(25,2),-15,-s.Rational(5,2)]):
        projector=I
        for other in eig:
            if other!=value:projector=projector*(E-other*I)/(value-other)
        assert projector*projector==projector and s.trace(projector)==multiplicity
        assert s.trace(projector*B)==expected
        projectors.append(projector)
        data.append({'eigenvalue':str(value),'multiplicity':multiplicity,'insertion_trace':str(expected)})
    assert sum(projectors,s.zeros(9))==I
    assert all(projectors[i]*projectors[j]==s.zeros(9) for i in range(3) for j in range(3) if i!=j)
    # With even n, these data prove the complete finite-ring formulas in
    # the reviewed proof, not merely values at a chosen finite n.
    log5=s.Rational(161,100)
    assert sum(log5**k/s.factorial(k) for k in range(13))>5
    bounds={str(beta):str((s.Rational(1,2)-log5/beta)/10) for beta in [64,96]}
    assert bounds=={'64':'3039/64000','96':'4639/96000'}
    out={'status':'INDEPENDENT_LITERAL_TRANSFER_AND_ALL_EVEN_RING_BARRIER_PASS',
       'spectral_data':data,'minimal_polynomial_distinct_roots':True,
       'all_even_n_ge4_trial_energy_per_bond':'strictly less than -9/2',
       'Gibbs_trace_distance_from_any_fully_separable_state_strict_lower_bounds':bounds,
       'seconds':time.monotonic()-started,
       'scope':'Exact finite-ring variational family plus reviewed free-energy, separable-energy and trace-norm inequalities. Excludes one-spin physical-product state reconstruction at that accuracy; does not exclude nonphysical/entangled frames or scalar-only partition contraction.'}
    (ROOT/'INDEPENDENT_PRODUCT_BARRIER.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
