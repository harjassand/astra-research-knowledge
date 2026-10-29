"""Exact tall-reference obstruction to a single signed output extension.

Two physical input letters make the true all-reference coefficient scalar.
A positive rational Fisher gap has four interior equality priors. They force
inconsistent kernel equations for any constant signed output extension S.
No stochastic samples, fitted coefficient, hierarchy, or SDP status.
"""
from pathlib import Path
import hashlib
import json
import time
import sympy as s

ROOT=Path(__file__).resolve().parent


def serial(M):return [[str(x) for x in row] for row in M.tolist()]


def experiment(weights,radii):
    rows=[]
    for w,r in zip(weights,radii):
        rows.extend([[w*(1+r)/2,w*(1-r)/2],
                     [w*(1-r)/2,w*(1+r)/2]])
    rows.append([1-sum(weights),1-sum(weights)])
    A=s.Matrix(rows)
    assert all(z>0 for z in A)
    assert list(s.ones(1,A.rows)*A)==[1,1]
    return A


def fisher(A,t):
    d=A[:,0]-A[:,1]
    w=t*A[:,0]+(1-t)*A[:,1]
    return sum(d[j]**2/w[j] for j in range(A.rows))


def main():
    tick=time.perf_counter()
    x=s.symbols('x')
    radii=[s.Rational(1,5),s.Rational(2,5),s.Rational(3,5),
           s.Rational(4,5),s.Rational(9,10)]
    nodes=[r*r for r in radii]
    numerator=(x-s.Rational(1,9))**2*(x-s.Rational(4,9))**2
    denominator=s.prod(1-a*x for a in nodes)
    gap=numerator/denominator
    coefficients=[]
    for j,a in enumerate(nodes):
        # delta_j a_j/(1-a_j x) is the partial-fraction term.
        coeff=s.cancel(numerator.subs(x,1/a)
              /s.prod(1-b/a for k,b in enumerate(nodes) if k!=j)/a)
        coefficients.append(coeff)
    assert s.cancel(gap-sum(coeff*a/(1-a*x)
                      for coeff,a in zip(coefficients,nodes)))==0
    scale=1/(4*(1+sum(abs(z) for z in coefficients)))
    budget=s.Rational(1,2)
    positive=[j for j,z in enumerate(coefficients) if z>0]
    negative=[j for j,z in enumerate(coefficients) if z<0]
    L=experiment([scale*coefficients[j]/budget for j in positive],
                 [radii[j] for j in positive])
    K=experiment([-scale*coefficients[j] for j in negative],
                 [radii[j] for j in negative])
    assert L.cols==K.cols==2 and L.rank()==2
    t=s.symbols('t')
    truegap=s.factor(budget*fisher(L,t)-fisher(K,t))
    intended=4*scale*gap.subs(x,(2*t-1)**2)
    assert s.cancel(truegap-intended)==0
    priors=[s.Rational(1,6),s.Rational(1,3),s.Rational(2,3),s.Rational(5,6)]
    for prior in priors:
        assert fisher(L,prior)>0 and s.cancel(truegap.subs(t,prior))==0
    assert all(0<a<1 for a in nodes)
    # Positive squared numerator and denominators1-a*(2t-1)^2>0 prove
    # the TRUE inequality for every t in[0,1]. Binary input implies the
    # same inequality for every reference by spectral calculus of Q1.
    ell,m=L.rows,K.rows
    names=s.symbols('S0:'+str(m*ell))
    S=s.Matrix(m,ell,names)
    equations=list(S*L-K)+list(s.ones(1,m)*S-s.ones(1,ell))
    labels=[f'factor:{y}:{i}' for y in range(m) for i in range(2)]
    labels+=[f'stochastic-column:{z}' for z in range(ell)]
    B=s.eye(ell)[:,:ell-1]
    B[ell-1,:]=-s.ones(1,ell-1)
    v=L[:,0]-L[:,1];d=K[:,0]-K[:,1]
    for prior in priors:
        wl=prior*L[:,0]+(1-prior)*L[:,1]
        wk=prior*K[:,0]+(1-prior)*K[:,1]
        residual=S.T*s.diag(*[1/z for z in wk])*d-budget*s.diag(*[1/z for z in wl])*v
        equations+=list(B.T*residual)
        labels.extend([f'equality-kernel:{prior}:{j}' for j in range(ell-1)])
    A,b=s.linear_eq_to_matrix(equations,names)
    rank=A.rank();augmented_rank=A.row_join(b).rank()
    assert augmented_rank==rank+1
    witness=None
    for y in A.T.nullspace():
        z=(y.T*b)[0]
        if z:
            witness=y/z;break
    assert witness is not None
    assert witness.T*A==s.zeros(1,A.cols) and (witness.T*b)[0]==1
    costs={'seconds_after_sympy_import':time.perf_counter()-tick,
           'numeric_SDP_or_optimizer_or_reference_queries':0}
    out={'status':'EXACT_TRUE_BUDGET_BUT_NO_CONSTANT_SIGNED_OUTPUT_EXTENSION',
         'budget':str(budget),'L':serial(L),'K':serial(K),
         'input_letters':2,'reference_outputs':ell,'release_outputs':m,
         'all_entries_strictly_positive':True,
         'reference_rank':L.rank(),
         'radii':[str(z) for z in radii],
         'partial_fraction_coefficients':[str(z) for z in coefficients],
         'scale':str(scale),'gap_factored':str(truegap),
         'gap_positive_argument':'square factors divided by positive1-r_j²(2t-1)² on[0,1]',
         'equality_priors':[str(z) for z in priors],
         'true_all_reference_coefficient':str(budget),
         'extension_linear_constraint_matrix':serial(A),
         'extension_linear_constraint_rhs':serial(b),
         'equation_labels':labels,
         'rank':rank,'augmented_rank':augmented_rank,
         'exact_inconsistency_witness':serial(witness),
         'contradiction':'y^T A=0 and y^T b=1',
         'max_source_rational_bits':max(max(int(z.p).bit_length(),int(z.q).bit_length()) for z in list(L)+list(K)),
         'scope':'rejects SAME constant signed-S full-output-tangent/common-center lift, not all finite SDP representations',
         'costs':costs}
    (ROOT/'TALL_OBSTRUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in
        ['extension_linear_constraint_matrix','extension_linear_constraint_rhs',
         'equation_labels','exact_inconsistency_witness','L','K']},indent=2))


if __name__=='__main__':main()
