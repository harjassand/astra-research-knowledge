#!/usr/bin/env python3
"""Finite-bit contrast spectral filter and oracle-free block acquisition.

Input: rational noisy contrast records, not a true partition/eigenbasis.
This is a deterministic backend for the statistical success theorem. No source
observations are generated or claimed by this module's exact test harness.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math,time
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parent

def rational(x):
    assert not isinstance(x,(bool,float,np.bool_,np.floating,s.Float))
    return F(str(x))

def ceil_log2(x):
    x=F(x);assert x>0
    k=max(0,x.numerator.bit_length()-x.denominator.bit_length())
    while F(1<<k)<x:k+=1
    return k

def filter_projector(contrast,beta):
    start=time.perf_counter();beta=rational(beta);assert beta>0
    C=s.Matrix(contrast);n=C.rows;assert n>=2 and C.cols==n
    assert all(x.is_Rational for x in C)
    J=s.eye(n)-s.ones(n)/n;C=J*C*J;S=C*C.T
    R=F(str(sum(x*x for x in C)+4*s.Rational(beta.numerator,beta.denominator)**2));nu=F(1,1024*n)
    a=min(F(1,2),3*beta*beta/R);h=0;grow=a
    while grow<F(1,2):grow*=F(11,8);h+=1
    q=F(3,4);j=0
    while F(2,3)*q>nu/8:q=q*q;j+=1
    T=h+j;b=ceil_log2(8*n*4**(T+1)/nu);scale=1<<b
    X0=(S-4*s.Rational(beta.numerator,beta.denominator)**2*s.eye(n))/s.Rational(R.numerator,R.denominator)
    Y=np.array([[int(s.floor(X0[i,k]*scale)) for k in range(n)] for i in range(n)],dtype=object)
    peak=max(abs(int(x)).bit_length() for x in Y.flat);rounds=[]
    for t in range(T):
        Y2=Y@Y;Y3=Y2@Y
        numer=3*Y*(1<<(2*b))-Y3;peak=max(peak,max(abs(int(x)).bit_length() for x in Y3.flat),max(abs(int(x)).bit_length() for x in numer.flat))
        Y=numer//(1<<(2*b+1));assert np.array_equal(Y,Y.T)
        rounds.append(max(abs(int(x)).bit_length() for x in Y.flat))
    D=n*(1<<(b+1));nums=n*(Y+scale*np.eye(n,dtype=object))+(1<<(b+1))*np.ones((n,n),dtype=object)
    nums=[[int(x) for x in row] for row in nums];trace=sum(nums[i][i] for i in range(n));r=(2*trace+D)//(2*D)
    valid=1<=r<=n and n%r==0 and abs(F(trace,D)-r)<=F(1,4)
    return {'status':'PROJECTOR_PROPOSAL' if valid else 'REFUSED_RANK_PROPOSAL','n':n,'rank':r if valid else None,'numerators':nums,'denominator':D,'beta':str(beta),'nu':str(nu),'R':str(R),'initial_spectral_gap_lower_if_success_class':str(a),'iterations':T,'dyadic_fraction_bits':b,'max_observed_intermediate_integer_bits':peak,'matrix_scalar_products_filter':2*T*n**3,'matrix_scalar_products_form_S':n**3,'round_entry_bits':rounds,'roundoff_upper':str(F(n*4**(T+1),1<<b)),'scope':'Deterministic finite-bit proposal; an inferred rank is not a statistical or reuse certificate. Class assumptions belong to success theorem only.','seconds':time.perf_counter()-start}

def greedy_partition(record):
    assert record['status']=='PROJECTOR_PROPOSAL';n=record['n'];r=record['rank'];D=record['denominator'];rows=record['numerators']
    assert type(n) is int and type(r) is int and n%r==0 and len(rows)==n and all(len(row)==n for row in rows)
    distances=[[sum((rows[i][q]-rows[j][q])**2 for q in range(n)) for j in range(n)] for i in range(n)]
    remaining=set(range(n));parts=[];centers=[]
    for _ in range(r):
        if not remaining:return {'status':'REFUSED_EMPTY_CLUSTER'}
        center=max(sorted(remaining),key=lambda i:(sum(8*n*distances[i][j]<=r*D*D for j in remaining),-i))
        part=sorted(j for j in remaining if 2*n*distances[center][j]<=r*D*D)
        assert part;parts.append(part);centers.append(center);remaining.difference_update(part)
    leftovers=sorted(remaining);parts[0]+=leftovers;parts[0].sort();which=[None]*n
    for g,part in enumerate(parts):
        for i in part:assert which[i] is None;which[i]=g
    assert all(x is not None for x in which)
    return {'status':'PARTITION_PROPOSAL','parts':parts,'which':which,'centers':centers,'leftover_rows':leftovers,'distance_scalar_products':n**3,'distance_storage_entries':n*n,'scope':'All pair distances/densest balls paid; no k-means/prototype oracle.'}

def refine(features,beta,expected_rank):
    beta=rational(beta);assert beta>0 and type(expected_rank) is int and expected_rank>0
    rows=[[rational(x) for x in row] for row in features];n=len(rows);assert n>0 and all(len(row)==expected_rank for row in rows)
    remaining=set(range(n));parts=[];comparisons=0
    while remaining:
        i=min(remaining);part=[]
        for j in sorted(remaining):
            comparisons+=1
            if sum((x-y)**2 for x,y in zip(rows[i],rows[j]))<beta*beta/16:part.append(j)
        assert part;parts.append(part);remaining.difference_update(part)
    valid=len(parts)==expected_rank and n%expected_rank==0 and all(len(part)==n//expected_rank for part in parts)
    return {'status':'REFINED_PARTITION_PROPOSAL' if valid else 'REFUSED_REFINEMENT','parts':parts,'pair_comparisons':comparisons,'feature_scalar_products':comparisons*expected_rank,'scope':'Exact threshold cleanup; still requires independent task/reuse validation.'}

def observation_ledger(n,r,beta,B=1,delta_s=F(1,100),delta_f=F(1,100)):
    # Conservative closed sufficient N: sqrt term and linear term each <=beta/16;
    # receive with outward-root error <=beta/64, so two-action error<beta/2. No outcomes are generated here.
    beta=rational(beta);B=rational(B);ks=ceil_log2(F(4*n,1)/delta_s);kf=ceil_log2(F(4*n*r,1)/delta_f)
    N=max(math.ceil(512*B*ks/(beta*beta)),math.ceil(F(64*ks,3)/beta))
    Nf=math.ceil(2048*r*kf/(beta*beta))
    return {'spectral_per_row_action_samples':N,'cleanup_per_row_action_samples':Nf,'total_named_forward_calls_sufficient':2*n*(N+Nf),'spectral_log_upper':ks,'cleanup_log_upper':kf,'preliminary_column_acquisition_calls':'ADDITIONAL; B is an acquired confidence cap, not gratis','reuse_validation_calls':'ADDITIONAL; not supplied by contrast recovery','scope':'Sufficient theorem ledger, NOT executed observations or a necessary sample lower bound. Very conservative constants.'}


def proposal_from_counts(columns,rows,*,expected_n,expected_beta,expected_column_confidence,expected_spectral_confidence):
    """Receive ordinary count arrays and BUILD the contrast; no supplied basis.

    Complete iid/fresh/nonanticipating provenance remains external. Status only
    means a statistically budgeted proposal, never a valid reusable abstraction.
    """
    n=expected_n;beta=rational(expected_beta);dc=rational(expected_column_confidence);ds=rational(expected_spectral_confidence)
    assert type(n) is int and n>=2 and beta>0 and 0<dc<1 and 0<ds<1
    assert len(columns)==len(rows)==2
    Nc=None;N=None
    for cs in columns:
        assert len(cs)==n and all(type(x) is int and x>=0 for x in cs)
        if Nc is None:Nc=sum(cs)
        assert sum(cs)==Nc and Nc>0
    Kc=ceil_log2(F(2*n,1)/dc);B=max(F(1),max(F(n*(2*x+8*Kc),Nc) for cs in columns for x in cs));B=min(F(n),B)
    for mat in rows:
        assert len(mat)==n
        for cs in mat:
            assert len(cs)==n and all(type(x) is int and x>=0 for x in cs)
            if N is None:N=sum(cs)
            assert sum(cs)==N and N>0
    Ks=ceil_log2(F(4*n,1)/ds)
    # Exact rational upper square root, local to avoid a library accuracy oracle.
    value=2*B*Ks/N;bits=max(64,ceil_log2(64/beta));scale=1<<bits;z=math.isqrt(value.numerator*scale*scale//value.denominator)
    if F(z*z,scale*scale)<value:z+=1
    tau=F(z,scale)+F(4*Ks,3*N)
    ledger={'column_calls':2*Nc,'spectral_calls':2*n*N,'source_calls_total':2*Nc+2*n*N,'column_cap':str(B),'column_K':Kc,'spectral_K':Ks,'tau':str(tau),'class_perturbation_not_checked':True,'reuse_validated':False}
    if 2*tau>beta/2:return {'status':'REFUSED_INSUFFICIENT_SPECTRAL_DATA','ledger':ledger}
    contrast=s.Matrix([[s.Rational(rows[1][i][j]-rows[0][i][j],N) for j in range(n)] for i in range(n)])
    filtered=filter_projector(contrast,beta)
    if filtered['status']!='PROJECTOR_PROPOSAL':return {'status':'REFUSED_FILTER_PROPOSAL','ledger':ledger,'filter':filtered}
    proposal=greedy_partition(filtered)
    return {'status':'BUDGETED_PARTITION_PROPOSAL_ONLY','ledger':ledger,'filter':filtered,'proposal':proposal,'scope':'Source counts generate the representation. Fresh cleanup and independent reuse validation are still required; no class-membership test or iid authentication is implied.'}


def cleanup_from_counts(rows0,rows1,proposal,*,expected_beta,expected_confidence,expected_proposal_sha256):
    beta=rational(expected_beta);delta=rational(expected_confidence)
    assert beta>0 and 0<delta<1 and type(expected_proposal_sha256) is str
    actual=hashlib.sha256(json.dumps(proposal,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert actual==expected_proposal_sha256 and proposal['status']=='PARTITION_PROPOSAL'
    n=len(proposal['which']);r=len(proposal['parts']);assert sorted(i for part in proposal['parts'] for i in part)==list(range(n))
    assert all(proposal['which'][i]==g for g,part in enumerate(proposal['parts']) for i in part)
    N=None
    for mat in (rows0,rows1):
        assert len(mat)==n
        for row in mat:
            assert len(row)==r and all(type(x) is int and x>=0 for x in row)
            if N is None:N=sum(row)
            assert N>0 and sum(row)==N
    K=ceil_log2(F(4*n*r,1)/delta);required=math.ceil(2048*r*K/(beta*beta))
    ledger={'fresh_cleanup_calls':2*n*N,'required_per_row_samples':required,'actual_per_row_samples':N,'confidence':str(delta),'old_proposal_sha256':actual}
    if N<required:return {'status':'REFUSED_INSUFFICIENT_CLEANUP_DATA','ledger':ledger}
    features=[[F(rows1[i][h]-rows0[i][h],N) for h in range(r)] for i in range(n)]
    out=refine(features,beta,r);out['ledger']=ledger
    out['scope']='Fresh outcome-independent fixed row counts relative to the bound proposal are external protocol premises. Output remains a partition proposal; independent reuse validation is not executed by this helper.'
    return out
