#!/usr/bin/env python3
"""Independent numerical/symbolic fixtures, not the all-N contour proof."""
import hashlib,json,math,time
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
mp.mp.dps=90
OWN=Path(__file__).parent
def legendre_bernstein(N,l):
    return [sum((F(math.comb(l,j)*math.comb(N-l,k-j),math.comb(N,k))
                 *(-1)**(l-j)*math.comb(l,j)
                 for j in range(max(0,k-(N-l)),min(l,k)+1)),F(0))
            for k in range(N+1)]
def population_error(N,k,delta):
    z=mp.mpf(k)-mp.mpf(N)/2;b=mp.mpf(N)/(4*delta)
    return mp.exp(-z*z/(4*b))*mp.re(mp.erfc(mp.mpf('1.5')*mp.sqrt(b)+1j*z/(2*mp.sqrt(b))))
def p_trunc(N,delta,s):
    L=N+2;b=mp.mpf(N)/(4*delta);a=mp.mpf('1.5')
    v=mp.findroot(lambda v:v-delta*L/N*mp.tanh((s+v)/2),(-delta*L/N,delta*L/N))
    # Numerical fixture computes the original real contour, independently of
    # the proof's main/vertical contour lower estimate.
    value=2*mp.sqrt(b/mp.pi)*mp.quad(lambda u:mp.re(mp.exp(-b*u*u)*(mp.cosh((s+1j*u)/2)/mp.cosh(s/2))**(-L)),[0,a/2,a])
    return (N+1)*value,v
def p_correct(N,delta,s):
    x=1/(1+mp.exp(-s));errors=[population_error(N,k,delta) for k in range(N+1)]
    terms=[]
    for l in range(N+1):
        coeff=legendre_bernstein(N,l)
        ell=sum(mp.mpf(c.numerator)/c.denominator*e for c,e in zip(coeff,errors))
        terms.append((2*l+1)*ell*mp.legendre(l,2*x-1))
    return sum(terms)
def exact_duality(N):
    # Check the Legendre Gram rows vs Bernstein polynomials using the explicit
    # monomial formula. This is exact Fraction arithmetic.
    rows=[]
    for l in range(N+1):
        r=[F((-1)**(l+j)*math.comb(l,j)*math.comb(l+j,j)) for j in range(l+1)]
        row=[]
        for k in range(N+1):
            value=sum((c*F(math.comb(N,k))*F(math.factorial(k+j)*math.factorial(N-k),math.factorial(N+j+1)) for j,c in enumerate(r)),F(0))
            row.append(value)
        rows.append(row)
    # Raising any population delta-vector to its Legendre dual polynomial and
    # integrating against each Bernstein basis must return that vector.
    Bs=[legendre_bernstein(N,l) for l in range(N+1)]
    for i in range(N+1):
        for k in range(N+1):
            value=sum((F(2*l+1)*Bs[l][i]*rows[l][k] for l in range(N+1)),F(0))
            assert value==int(i==k),(N,i,k,value)
    assert all(abs(c)<=2**l for l,row in enumerate(Bs) for c in row)
    return {'N':N,'matrix_identity':'exact Fraction identity','coefficient_bound':'exact Fraction PASS'}
def main():
    start=time.perf_counter();delta=mp.mpf(1)/4;density=[]
    for N in [2,3,4,16,32]:
        low=(N+1)*mp.mpf(27)/32*mp.exp(-delta*(N+2)**2/(4*N))
        for s0 in [-20,-5,-1,0,1,5,20]:
            s=mp.mpf(s0);pt,v=p_trunc(N,delta,s);pc=p_correct(N,delta,s)
            assert pt>=low and pt+pc>=low/2
            density.append({'N':N,'s':s0,'P_truncated':str(pt),'P_correction':str(pc),'P_exact':str(pt+pc),'proved_lower':str(low/2),'saddle_v':str(v)})
    beta=[]
    for N,k,u0 in [(2,0,'1.5'),(2,1,'1.5'),(4,2,'.7'),(16,3,'1.2')]:
        L=N+2;z=mp.mpf(k)-mp.mpf(N)/2;u=mp.mpf(u0)
        value=mp.quad(lambda s:mp.exp(z*s)/(2*mp.cosh((s+1j*u)/2))**L,[-mp.inf,-10,-2,0,2,10,mp.inf])
        expected=mp.exp(-1j*z*u)/((N+1)*math.comb(N,k))
        assert abs(value-expected)<mp.mpf('1e-80')
        beta.append({'N':N,'k':k,'u':u0,'relative_residual':str(abs(value-expected)/abs(expected))})
    constants={'phase_cube':str(F(256,7935)),'phase_cube_leq_1_30':F(256,7935)<=F(1,30),
               'g0_fourth_gt_2_15':F(15,23)**4>F(2,15),'N2_correction_ratio_upper':str(F(40,81)),
               'N2_upper_lt_one_half':F(40,81)<F(1,2),
               'exp_7_3_first_four_terms_gt8':sum((F(7,3)**j/F(math.factorial(j)) for j in range(4)),F(0))>8,
               'exp4_first_six_terms_gt32':sum((F(4)**j/F(math.factorial(j)) for j in range(6)),F(0))>32}
    assert all(v for k,v in constants.items() if isinstance(v,bool))
    proof=OWN/'AXIAL_UNIFORM_SEPARABILITY.txt'
    out={'scope':'Numerical contour and exact finite duality fixtures only; the all-N theorem is the separate analytic proof','dps':mp.mp.dps,
         'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'density':density,'complex_beta':beta,
         'duality':[exact_duality(N) for N in [2,3,4,8,16]],'rational_constants':constants,'wall_seconds':time.perf_counter()-start}
    path=OWN/'evidence'/'axial_density_fixtures.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS bounded fixtures','records':len(density),'proof_sha256':out['proof_sha256'],'wall_seconds':out['wall_seconds']}))
if __name__=='__main__':main()
