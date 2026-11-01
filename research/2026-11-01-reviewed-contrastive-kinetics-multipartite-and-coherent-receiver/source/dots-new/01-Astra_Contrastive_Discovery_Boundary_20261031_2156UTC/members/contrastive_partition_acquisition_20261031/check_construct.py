#!/usr/bin/env python3
"""Exact deterministic tests only; no new source sampling experiment."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,random,time
import sympy as s
import construct as c
ROOT=Path(__file__).resolve().parent

def canonical(parts):return sorted(tuple(sorted(x)) for x in parts)
def projector(parts,n):
    P=s.zeros(n)
    for part in parts:
        for i in part:
            for j in part:P[i,j]=s.Rational(1,len(part))
    return P

def run():
    start=time.perf_counter();checks=0;cases=[]
    def ck(v):
        nonlocal checks
        assert v;checks+=1
    for n,r in ((4,2),(8,2),(12,3),(16,4)):
        order=list(range(n));random.Random(910+n).shuffle(order);parts=[sorted(order[j*n//r:(j+1)*n//r]) for j in range(r)];P=projector(parts,n);J=s.ones(n)/n;Q=s.eye(n)-J
        beta=F(1,4096);Delta=s.Rational(3,4);C0=Delta*(P-J)
        # A centered full-rank perturbation on 1^perp, not exact low-rank data.
        E=s.Rational(1,4096*8*n)*Q;C=C0+E
        ck((C* s.ones(n,1))==s.zeros(n,1) and C.rank()==n-1)
        ck(sum(x*x for x in E)<=s.Rational(beta.numerator,beta.denominator)**2)
        rec=c.filter_projector(C,beta);ck(rec['rank']==r);ck(F(rec['roundoff_upper'])<=F(rec['nu'])/8)
        Fmat=s.Matrix(rec['numerators'])/rec['denominator'];nu=s.Rational(rec['nu']);beta_s=s.Rational(beta.numerator,beta.denominator)
        # Avoid irrational comparisons by weakening Delta-beta denominator bound
        # with exact supplied Delta, valid for this chosen C0.
        frob=sum(x*x for x in Fmat-P);bound=4*r*beta_s**2/(Delta-beta_s)**2+2*n*nu**2;ck(frob<=bound)
        proposal=c.greedy_partition(rec);ck(canonical(proposal['parts'])==canonical(parts))
        cases.append({'n':n,'r':r,'centered_contrast_rank':C.rank(),'iterations':rec['iterations'],'fraction_bits':rec['dyadic_fraction_bits'],'intermediate_bits':rec['max_observed_intermediate_integer_bits'],'filter_products':rec['matrix_scalar_products_filter'],'distance_products':proposal['distance_scalar_products'],'Frobenius_error_squared':str(frob),'success_ledger_not_executed':c.observation_ledger(n,r,beta)})
    # Cleanup really corrects a bad initial label, not just exact input labels.
    n=128;r=4;parts=[list(range(g*32,(g+1)*32)) for g in range(r)];P=projector(parts,n);Fmat=P.copy();Fmat[0,:]=P[32,:]
    D=32;rec={'status':'PROJECTOR_PROPOSAL','n':n,'rank':r,'denominator':D,'numerators':[[int(x*D) for x in Fmat.row(i)] for i in range(n)]}
    proposal=c.greedy_partition(rec);ck(canonical(proposal['parts'])!=canonical(parts));W=s.zeros(r,n)
    for g,part in enumerate(parts):
        for i in part:W[g,i]=s.Rational(1,32)
    Zh=s.zeros(n,r)
    for h,part in enumerate(proposal['parts']):
        for i in part:Zh[i,h]=1
    T=W*Zh;Dmacro=s.Rational(3,4)*(s.eye(r)-s.ones(r)/r);features=[]
    for i in range(n):
        row=list((Dmacro*T).row(i//32));row[0]+=s.Rational((i%3)-1,2**20);features.append(row)
    fixed=c.refine(features,F(1,4096),r);ck(fixed['status']=='REFINED_PARTITION_PROPOSAL');ck(canonical(fixed['parts'])==canonical(parts))
    # Contrast discovery alone does not validate useful model reduction.
    n=4;parts=[[0,1],[2,3]];P=projector(parts,n);J=s.ones(n)/n;S=s.zeros(n)
    for i,j in enumerate([0,2,1,3]):S[i,j]=1
    A0=s.Rational(9,10)*S+s.Rational(1,10)*J;A1=s.Rational(9,10)*S+s.Rational(1,10)*P
    ck(A1-A0==s.Rational(1,10)*(P-J))
    mu=s.Matrix([[s.Rational(1,2),s.Rational(1,2),0,0]]);b=s.Matrix([1,1,0,0]);true=(mu*A1*A1*b)[0];coarse=(mu*P*A1*P*A1*P*b)[0]
    ck(abs(true-coarse)==s.Rational(81,200))
    bad_rec=c.filter_projector(A1-A0,F(1,4096));bad_proposal=c.greedy_partition(bad_rec);ck(canonical(bad_proposal['parts'])==canonical(parts))
    # Zero contrast cannot justify a desired nontrivial partition; proposal is r1.
    zero=c.filter_projector(s.zeros(4),F(1,4096));ck(zero['rank']==1)
    rejects=0
    for x in (True,.1,s.Float('.1'),0,-1):
        try:c.filter_projector(s.zeros(2),x)
        except (AssertionError,ValueError,TypeError):rejects+=1
        else:raise AssertionError('accepted bad beta')
    # Receiver refusal is executable on small insufficient counts; no fake
    # huge observation experiment is manufactured for a sufficient ledger.
    refusal=c.proposal_from_counts([[1,1],[1,1]],[[[1,0],[0,1]],[[0,1],[1,0]]],expected_n=2,expected_beta=F(1,4096),expected_column_confidence=F(1,100),expected_spectral_confidence=F(1,100));ck(refusal['status']=='REFUSED_INSUFFICIENT_SPECTRAL_DATA')
    toy={'status':'PARTITION_PROPOSAL','parts':[[0],[1]],'which':[0,1]};digest=hashlib.sha256(json.dumps(toy,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    refused_cleanup=c.cleanup_from_counts([[1,0],[0,1]],[[0,1],[1,0]],toy,expected_beta=F(1,4096),expected_confidence=F(1,100),expected_proposal_sha256=digest);ck(refused_cleanup['status']=='REFUSED_INSUFFICIENT_CLEANUP_DATA')
    # Fabricated deterministic integer-count UNIT FIXTURE, NOT observations.
    # It checks the successful full count frontend without pretending to have
    # performed its enormous implied acquisition bill.
    n=4;beta=F(1,4096);Nc=10**9;columns=[[Nc//n]*n for _ in range(2)]
    N=10**13;P=projector([[0,1],[2,3]],n);M0=s.ones(n)/n;M1=s.Rational(3,4)*P+s.ones(n)/16
    rows=[[[int(x*N) for x in M.row(i)] for i in range(n)] for M in (M0,M1)]
    got=c.proposal_from_counts(columns,rows,expected_n=n,expected_beta=beta,expected_column_confidence=F(1,100),expected_spectral_confidence=F(1,100))
    ck(got['status']=='BUDGETED_PARTITION_PROPOSAL_ONLY');pp=got['proposal'];ck(canonical(pp['parts'])==canonical([[0,1],[2,3]]))
    rowblocks=[[[sum(mat[i][j] for j in part) for part in pp['parts']] for i in range(n)] for mat in rows]
    pd=hashlib.sha256(json.dumps(pp,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    cleaned=c.cleanup_from_counts(*rowblocks,pp,expected_beta=beta,expected_confidence=F(1,100),expected_proposal_sha256=pd)
    ck(cleaned['status']=='REFINED_PARTITION_PROPOSAL');ck(canonical(cleaned['parts'])==canonical([[0,1],[2,3]]))
    return {'status':'PASS_EXACT_DISCOVERY_BACKEND_CHECKS','checks':checks,'interface_rejections':rejects,'cases':cases,'cleanup_corrected_bad_initial_label':True,'nonreducing_common_background_true_two_step_value':str(true),'nonreducing_common_background_coarse_value':str(coarse),'nonreducing_background_error':str(abs(true-coarse)),'new_source_observations_executed':0,'successful_count_frontend_test_is_fabricated_deterministic_unit_fixture':True,'scope':'Deterministic exact finite-bit backend tests, not a statistical acquisition experiment, independent review or novel clustering claim. The sufficient sample ledger is huge and remains a limitation; practical spectral methods receive identical data.','seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256((ROOT/'construct.py').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
if __name__=='__main__':
    out=run();(ROOT/'construct_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2));print([{k:v for k,v in x.items() if k!='Frobenius_error_squared'} for x in out['cases']])
