#!/usr/bin/env python3
"""New internal finite checks; rational interlacing identities and tensor counterexample.
Not a formal proof, independent reviewer, interval certificate, or complexity claim.
"""
from fractions import Fraction as F
from pathlib import Path
from random import Random
from collections import Counter
import json
import math
import numpy as np

COUNTS=Counter()
METRICS={}
def check(cond, name):
    if not cond:
        raise AssertionError(name)
    COUNTS[name]+=1

def mul(p,q):
    r=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):
            r[i+j]+=x*y
    return r

def polynomial(roots):
    p=[F(1)]
    for t in roots:
        p=mul(p,[-t,F(1)])
    return p

def add(p,q):
    r=[F(0)]*max(len(p),len(q))
    for i,x in enumerate(p):r[i]+=x
    for i,x in enumerate(q):r[i]+=x
    return r

def max_window(xi,a):
    # Definition-first exhaustive closed-left/open-right test, not source's two-pointer code.
    return max((sum(x<=y<x+a for y in xi) for x in xi), default=0)

def chain_residues(c,a):
    d=[x/(1-a*x) for x in c]
    weights=[]
    for j,dj in enumerate(d):
        numerator=math.prod((dj-x for x in c),start=F(1))
        denominator=math.prod((dj-x for k,x in enumerate(d) if k!=j),start=F(1))
        weights.append(numerator/denominator)
    check(all(w>=0 for w in weights),'exact_nonnegative_residues')
    check(sum(weights)==sum(d)-sum(c),'exact_minimum_energy_trace')
    # det(zI-(D-vv*)) via determinant lemma, with v_j^2=weights_j.
    lhs=polynomial(d)
    for j,w in enumerate(weights):
        lhs=add(lhs,[w*x for x in polynomial(d[:j]+d[j+1:])])
    check(lhs==polynomial(c),'exact_characteristic_polynomial_match')
    return d,weights

def source_rank_energy():
    rng=Random(28102026)
    spectra=[]
    for n in range(1,26):
        # Consecutive reciprocal endpoints, ties, and strict gaps.
        for repeats in (1,2,3):
            xi=[F(2+j//repeats) for j in range(n)]
            spectra.append((xi,F(1)))
    for _ in range(300):
        a=F(rng.randint(1,5),rng.randint(1,5))
        xi=sorted(a+F(rng.randint(1,50),rng.randint(1,7)) for j in range(rng.randint(1,25)))
        spectra.append((xi,a))
    energies=[]
    numeric_residual=0.0
    for xi,a in spectra:
        lam=[1/x for x in xi]
        r=max_window(xi,a)
        expected=sum(x/(1-a*x)-x for x in lam)
        actual=F(0)
        blocks=[]
        for offset in range(r):
            c=lam[offset::r]
            d,w=chain_residues(c,a)
            actual+=sum(w)
            check(sum(w)>0,'exact_nonzero_rank_one_chain')
            check(all(c[j]>=d[j+1] for j in range(len(c)-1)),'exact_chain_interlacing')
            blocks.append((c,d,w))
        check(actual==expected,'exact_simultaneous_rank_energy_optimum')
        check(len(blocks)==r,'exact_rank_equals_window_occupancy')
        energies.append(float(expected))
        # Numerical reconstruction of the polar factor on the first 40 small examples only.
        if len(lam)<=12 and COUNTS['numeric_polar_curvature_equality']<40:
            for c,d,w in blocks:
                aa=np.diag([float(x) for x in c])
                dd=np.diag([float(x) for x in d])
                v=np.sqrt(np.array([float(x) for x in w]))
                pp=np.outer(v,v)
                cc=dd-pp
                eig,u=np.linalg.eigh(cc)
                # Sorted eigenbasis realizes C=U A U^T, reverse ascending eigh order.
                u=u[:,::-1]
                check(np.max(np.abs(eig[::-1]-np.diag(aa)))<2e-11,'numeric_prescribed_C_spectrum')
                tt=u@np.sqrt(aa)
                residual=max(np.linalg.norm(tt.T@tt-aa,2),np.linalg.norm(tt@tt.T+pp-dd,2))
                numeric_residual=max(numeric_residual,float(residual))
                check(residual<2e-11,'numeric_polar_curvature_equality')
    METRICS['spectra_tested']=len(spectra)
    METRICS['largest_polar_reconstruction_residual']=numeric_residual
    METRICS['example']=example_rank_energy()

def example_rank_energy():
    a=F(1)
    lam=[F(1,2),F(1,3),F(1,4)]
    d,w=chain_residues(lam,a)
    # lambda half-open reciprocal occupancy=1. Source padded shift energy=1.
    # Exact equality construction energy=1-(1/4)=3/4.
    return {'a':'1','lambda':[str(x) for x in lam], 'minimum_source_rank':1,
        'residue_squared_coordinates':[str(x) for x in w],
        'minimum_HS_source_squared':str(sum(w)),
        'padded_shift_HS_source_squared':'1'}

def bell_unitary(m):
    d=2**m
    unitary=np.zeros((d*d,d*d))
    # H on every left qubit then paired CNOTs: U|(l,r)> = d^-1/2 sum_x (-1)^(l dot x)|x,r xor x>.
    for l in range(d):
        for r in range(d):
            col=l*d+r
            for x in range(d):
                parity=(l & x).bit_count()%2
                unitary[x*d+(r^x),col]=(-1 if parity else 1)/math.sqrt(d)
    return unitary

def tensor_counterexample():
    for m in (1,2,3):
        d=2**m
        u=bell_unitary(m)
        check(np.linalg.norm(u.T@u-np.eye(d*d),2)<2e-12,'numeric_Bell_circuit_unitary')
        v=np.kron(np.array([[0.,0.],[1.,0.]]),u)
        s=np.zeros(2*d*d); s[0]=1
        e=v@s
        ps=np.outer(s,s); pe=np.outer(e,e)
        fixed=ps/2+pe/3
        check(np.linalg.norm(v@fixed@v.T-pe/2,2)<2e-12,'numeric_nilpotent_recursion_support')
        check(np.linalg.norm(v@e)<2e-12,'numeric_second_source_word_zero')
        # Operator realignment across (clock,left) | right.
        realignment=fixed.reshape(2*d,d,2*d,d).transpose(0,2,1,3).reshape((2*d)**2,d*d)
        singular=np.linalg.svd(realignment,compute_uv=False)
        expected=np.array([math.sqrt(.25+(1/(3*d))**2)]+[1/(3*d)]*(d*d-1))
        check(np.max(np.abs(singular-expected))<2e-12,'numeric_exact_operator_Schmidt_spectrum')
        check(np.count_nonzero(singular>1e-10)==d*d,'numeric_operator_tensor_rank_exponential')
    rows=[]
    for m in range(1,65):
        d=2**m
        required=3*d*d//4
        # For a rank R approximation with HS error <=1/6, 1/9*(1-R/d^2)<=1/36.
        check(F(1,9)*(1-F(required,d*d))==F(1,36),'exact_tensor_error_rank_threshold')
        rows.append({'m':m,'word_dimension':2,'ordinary_fixed_point_rank':2,'operator_Schmidt_rank':d*d,'rank_needed_for_HS_error_at_most_1_over_6':required})
    METRICS['tensor_counterexample_m20']=rows[19]

def commutator_transfer():
    rng=np.random.default_rng(20261013)
    smallest_residual=0.0
    largest_ratio=0.0
    for n in (2,3,5,8):
        for _ in range(12):
            a=float(rng.uniform(.2,2.))
            t=rng.standard_normal((n,n))+1j*rng.standard_normal((n,n))
            t*=math.sqrt(.7/a)/np.linalg.norm(t,2)
            aa=t.conj().T@t
            cc=t@t.conj().T
            def positive(x):
                w,u=np.linalg.eigh((x+x.conj().T)/2)
                return (u*np.maximum(w,0))@u.conj().T
            lam,u=np.linalg.eigh(aa)
            fa=(u*(lam/(1-a*lam)))@u.conj().T
            pp=positive(fa-cc)
            qq=positive(cc-aa)
            residual=(pp+qq-a*aa@aa)
            residmin=float(np.linalg.eigvalsh((residual+residual.conj().T)/2)[0])
            smallest_residual=min(smallest_residual,residmin)
            check(residmin>=-2e-10,'numeric_commutator_positive_majorant')
            bp=np.maximum(np.linalg.eigvalsh(pp),0)
            qp=np.maximum(np.linalg.eigvalsh(qq),0)
            for p in (.25,.5,1.,1.5,2.,3.,6.):
                if p<=2:
                    lhs=float(np.sum(lam**p))
                    rhs=a**(-p/2)*(np.sum(bp**(p/2))+np.sum(qp**(p/2)))
                else:
                    lhs=float(np.sum(lam**p)**(2/p))
                    rhs=a**-1*(np.sum(bp**(p/2))**(2/p)+np.sum(qp**(p/2))**(2/p))
                largest_ratio=max(largest_ratio,lhs/rhs)
                check(lhs<=rhs+2e-9*max(1.,rhs),'numeric_commutator_Schatten_transfer')
    METRICS['commutator_instances']=48
    METRICS['smallest_commutator_majorant_eigenvalue']=smallest_residual
    METRICS['largest_commutator_Schatten_lhs_over_rhs']=largest_ratio

def main():
    source_rank_energy()
    tensor_counterexample()
    commutator_transfer()
    report={'status':'PASS_INTERNAL_FINITE_CHECKS_ONLY','scope':'Exact rational identities plus floating diagnostics; no formal or external validation, no novelty clearance.',
        'assertions_total':sum(COUNTS.values()),'exact_assertions_total':sum(v for k,v in COUNTS.items() if k.startswith('exact_')),'floating_diagnostic_assertions_total':sum(v for k,v in COUNTS.items() if k.startswith('numeric_')),'assertions_by_category':dict(COUNTS),'metrics':METRICS}
    Path(__file__).with_name('synthesis_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
