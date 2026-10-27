"""Exact rational reconstruction of a known PPT activation obstruction.
This is NOT a witness for tensor powers of the qutrit Werner candidate.
"""
from fractions import Fraction as Q
from itertools import product
import json

D=3

def delta(a,b):return int(a==b)

def eye_pair(a,b,c,d):return delta(a,c)*delta(b,d)

def flip(a,b,c,d):return delta(a,d)*delta(b,c)

def pomega(a,b,c,d):return Q(delta(a,b)*delta(c,d),3)

def sigma_elem(a1,a2,b1,b2,c1,c2,d1,d2):
    # sigma = (I+F)_1 tensor I_2 /120 + (3I-5F)_1 tensor P_2 /120.
    i1=eye_pair(a1,b1,c1,d1);f1=flip(a1,b1,c1,d1)
    i2=eye_pair(a2,b2,c2,d2);p2=pomega(a2,b2,c2,d2)
    return ((i1+f1)*i2+(3*i1-5*f1)*p2)/120

def sigmag_elem(a1,a2,b1,b2,c1,c2,d1,d2):
    return sigma_elem(a1,a2,d1,d2,c1,c2,b1,b2)

def sigma_mix_g(a1,a2,b1,b2,c1,c2,d1,d2):
    ident=delta(a1,c1)*delta(a2,c2)*delta(b1,d1)*delta(b2,d2)
    return Q(9,10)*sigmag_elem(a1,a2,b1,b2,c1,c2,d1,d2)+Q(1,810)*ident

def k_elem(a,b,c,d):return eye_pair(a,b,c,d)-Q(delta(a,b)*delta(c,d),2)

def witness_entries():
    # Integer vec(D): Bell(A0,A1) tensor Bell(B0,B1) tensor antisymmetric(A2,B2),
    # all three unnormalized. Norm square = 18, matrix rank = 2.
    return {(i,i,a,j,j,b):Q(sgn) for i,j in product(range(3),repeat=2)
            for a,b,sgn in ((0,1,1),(1,0,-1))}

def expectation(entries,base):
    total=Q(0)
    for r,vr in entries.items():
      for s,vs in entries.items():
        a0,a1,a2,b0,b1,b2=r;c0,c1,c2,d0,d1,d2=s
        total+=vr*vs*k_elem(a0,b0,c0,d0)*base(a1,a2,b1,b2,c1,c2,d1,d2)
    return total

def main():
    # Independently check the PPT decomposition of sigma^Gamma entry by entry:
    # on P_1: (I-F)_2/30; on I-P_1: (I+F)_2/120.
    maxerr=Q(0);tr=Q(0);traceg=Q(0)
    for a1,a2,b1,b2,c1,c2,d1,d2 in product(range(3),repeat=8):
        actual=sigmag_elem(a1,a2,b1,b2,c1,c2,d1,d2)
        i1=eye_pair(a1,b1,c1,d1);p1=pomega(a1,b1,c1,d1)
        i2=eye_pair(a2,b2,c2,d2);f2=flip(a2,b2,c2,d2)
        rhs=p1*Q(i2-f2,30)+(i1-p1)*Q(i2+f2,120)
        maxerr=max(maxerr,abs(actual-rhs))
        if (a1,a2,b1,b2)==(c1,c2,d1,d2):
            tr+=sigma_elem(a1,a2,b1,b2,c1,c2,d1,d2);traceg+=actual
    if maxerr or tr!=1 or traceg!=1:raise AssertionError((maxerr,tr,traceg))
    w=witness_entries();norm=sum(v*v for v in w.values())
    e=expectation(w,sigmag_elem);em=expectation(w,sigma_mix_g)
    if norm!=18 or e!=Q(-1,15) or em!=Q(-28,675):raise AssertionError((norm,e,em))
    out={'known_primary_source':'Vollbrecht-Wolf quant-ph/0201103v2, tau^(5), d=3',
         'sigma_trace':str(tr),'sigma_PPT_decomposition_max_error':str(maxerr),
         'integer_witness_norm_squared':str(norm),'integer_witness_rank':2,
         'K_tensor_sigmaGamma_expectation':str(e),
         'normalized_K_tensor_sigmaGamma_expectation':str(e/norm),
         'normalized_rhoGamma_tensor_sigmaGamma_expectation':str(Q(2,15)*e/norm),
         'epsilon':'1/10','sigma_mix_and_partial_transpose_minimum_lower_bound':'1/810',
         'integer_K_tensor_sigmaMixGamma_expectation':str(em),
         'normalized_K_tensor_sigmaMixGamma_expectation':str(em/norm),
         'normalized_rhoGamma_tensor_sigmaMixGamma_expectation':str(Q(2,15)*em/norm),
         'scope':'Exact obstruction to a general PPT/positive-crossed induction. sigma_mix is not a Werner tensor power.'}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
