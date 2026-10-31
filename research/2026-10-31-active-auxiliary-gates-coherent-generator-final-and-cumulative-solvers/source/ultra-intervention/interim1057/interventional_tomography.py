#!/usr/bin/env python3
"""Exact probability-table -> observable operators -> physical generator.

The compiler receives a promised complete rank bound. Probabilities are
analytically computed fixture inputs, not acquired sample frequencies.
Hidden source matrices stay in the oracle/validation side of the program.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time
import sympy as sp

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/interventional_generator'
sys.path.insert(0,str(ROOT/'work'));sys.path.insert(0,str(ROOT/'outputs/coherent_generator'))
from coherent_generator_control import identity,mm,inverse,mv
from ctmc_reflection_control import dyadic_enclose
from kinetic import log_bounds


def add(*As):return [[sum(xs,F(0)) for xs in zip(*rows)] for rows in zip(*As)]
def scale(a,A):return [[a*x for x in row] for row in A]
def rmv(v,A):return [sum(v[i]*A[i][j] for i in range(len(v))) for j in range(len(A[0]))]
def diagonal(v):return [[x*F(i==j) for j in range(len(v))] for i,x in enumerate(v)]
def decode(A):return [[F(x) for x in row] for row in A]
def encode(A):return [[str(x) for x in row] for row in A]


def controlled(q,f,t):
    n=len(q);out=[[F(0)]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i!=j:out[i][j]=q[i][j]*t**((f[j]-f[i])//2)
        out[i][i]=-sum(out[i])
    return out


def resolvent(q,nu):
    n=len(q);I=identity(n)
    return scale(nu,inverse(add(scale(nu,I),scale(-1,q))))


class ProbabilityOracle:
    """Mathematical input source, deliberately separate from recover()."""
    def __init__(self,q,pi,f,nu=F(1),t=F(2)):
        self.pi=pi;self.T=[];self.rows={():pi};self.queries={};self.row_updates=0
        for z in (q,controlled(q,f,t)):
            B=resolvent(z,nu)
            for bit in (-1,1):self.T.append(mm(B,diagonal([F(x==bit) for x in f])))
    def row(self,w):
        if w not in self.rows:
            self.rows[w]=rmv(self.row(w[:-1]),self.T[w[-1]]);self.row_updates+=1
        return self.rows[w]
    def p(self,w):
        w=tuple(w)
        if w not in self.queries:self.queries[w]=sum(self.row(w))
        return self.queries[w]


def choose_bases(oracle,rank_bound):
    # Ordinary exact cross approximation uses only queried probabilities.
    # rank_bound is an explicit promise, not inferred from a finite prefix.
    candidates=[()]+[(c,)*k for k in range(1,rank_bound+1) for c in range(4)]
    U=[];V=[];Hi=[]
    while len(U)<rank_bound:
        found=None
        for u in candidates:
            if u in U:continue
            row=[oracle.p(u+v) for v in V];right=rmv(row,Hi) if U else []
            for v in candidates:
                if v in V:continue
                col=[oracle.p(a+v) for a in U];left=mv(Hi,col) if U else []
                pivot=oracle.p(u+v)-sum(a*b for a,b in zip(right,col))
                if pivot:found=(u,v,right,left,pivot);break
            if found:break
        if not found:raise RuntimeError('candidate basis menu exhausted; no completeness claim')
        u,v,right,left,pivot=found;r=len(U)
        Hi=[[Hi[i][j]+left[i]*right[j]/pivot for j in range(r)]+[-left[i]/pivot] for i in range(r)]+[
            [-x/pivot for x in right]+[1/pivot]]
        U.append(u);V.append(v)
    H=[[oracle.p(u+v) for v in V] for u in U]
    assert mm(H,Hi)==identity(rank_bound)
    return U,V


def make_table(oracle,rank_bound,nu=F(1),t=F(2)):
    U,V=choose_bases(oracle,rank_bound)
    H=[[oracle.p(u+v) for v in V] for u in U]
    shifted=[[[oracle.p(u+(c,)+v) for v in V] for u in U] for c in range(4)]
    return {'complete_Hankel_rank_upper_promise':rank_bound,'inspection_rate':str(nu),'field_multiplier':str(t),
            'prefixes':[list(w) for w in U],'suffixes':[list(w) for w in V],
            'H':encode(H),'H_shifted':[encode(A) for A in shifted],
            'prefix_probabilities':[str(oracle.p(u)) for u in U],
            'suffix_probabilities':[str(oracle.p(v)) for v in V],
            'source':'exact analytical probability oracle; no independent sample preparations',
            'source_unique_probability_queries':len(oracle.queries),'source_cached_row_updates':oracle.row_updates,
            'source_max_queried_word_length':max(map(len,oracle.queries)),
            'source_query_rational_bits':sum(x.numerator.bit_length()+x.denominator.bit_length() for x in oracle.queries.values())}


def entropy(q,pi):
    lo=hi=F(0)
    for i in range(len(q)):
        for j in range(i+1,len(q)):
            x,y=pi[i]*q[i][j],pi[j]*q[j][i]
            if x==y:continue
            assert x>0 and y>0
            if x<y:x,y=y,x
            a,b=log_bounds(x/y,64);lo+=(x-y)*a;hi+=(x-y)*b
    return dyadic_enclose(lo,hi,96)


def observable(table):
    """Common observable algebra; no physical eigenbasis needed."""
    r=table['complete_Hankel_rank_upper_promise'];I=identity(r)
    H=decode(table['H']);Hi=inverse(H);T=[mm(Hi,decode(A)) for A in table['H_shifted']]
    one=mv(Hi,list(map(F,table['prefix_probabilities'])));rho=list(map(F,table['suffix_probabilities']))
    nu=F(table['inspection_rate'])
    B0=add(T[0],T[1]);B1=add(T[2],T[3]);B0i=inverse(B0);B1i=inverse(B1)
    Dm=mm(B0i,T[0]);Dp=mm(B0i,T[1])
    assert add(Dm,Dp)==I and mm(Dm,Dm)==Dm and mm(Dp,Dp)==Dp
    assert mm(inverse(B1),T[2])==Dm and mm(inverse(B1),T[3])==Dp
    Q0=scale(nu,add(I,scale(-1,B0i)));Q1=scale(nu,add(I,scale(-1,B1i)))
    if table.get('actuation_model')=='uniform_label_crossing_scaling':
        def proportional_factor(A,B):
            ratios=[y/x for rowa,rowb in zip(A,B) for x,y in zip(rowa,rowb) if x]
            if not ratios:raise RuntimeError('uninformative crossing block')
            factor=ratios[0]
            assert factor>0 and scale(factor,A)==B
            return factor
        mp=proportional_factor(mm(mm(Dp,Q0),Dm),mm(mm(Dp,Q1),Dm))
        mn=proportional_factor(mm(mm(Dm,Q0),Dp),mm(mm(Dm,Q1),Dp))
    else:
        t=F(table['field_multiplier']);mp,mn=1/t,t
    if mp==1 or mn==1:raise RuntimeError('both crossing multipliers must change for this hazard formula')
    Rt=add(mm(mm(Dp,Q0),Dp),mm(mm(Dm,Q0),Dm),
           scale(mp,mm(mm(Dp,Q0),Dm)),scale(mn,mm(mm(Dm,Q0),Dp)))
    Ft_i=add(scale(1/(1-mp),Dp),scale(1/(1-mn),Dm))
    C=mm(Ft_i,add(Q1,scale(-1,Rt)))
    assert mm(C,Dp)==mm(Dp,C)
    return {'T':T,'one':one,'rho':rho,'Q0':Q0,'Q1':Q1,'C':C,'Dp':Dp,'Dm':Dm,
            'plus_crossing_multiplier':mp,'minus_crossing_multiplier':mn}


def predict_generator(operators,t):
    return predict_scaled_generator(operators,1/t,t)


def predict_scaled_generator(operators,mp,mn):
    q,Dp,Dm,C=operators['Q0'],operators['Dp'],operators['Dm'],operators['C']
    Rt=add(mm(mm(Dp,q),Dp),mm(mm(Dm,q),Dm),
           scale(mp,mm(mm(Dp,q),Dm)),scale(mn,mm(mm(Dm,q),Dp)))
    return add(Rt,mm(add(scale(1-mp,Dp),scale(1-mn,Dm)),C))


def scaled_crossings(q,labels,mp,mn):
    n=len(q);out=[[F(0)]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i!=j:out[i][j]=q[i][j]*(mp if labels[i]==1 else mn) if labels[i]!=labels[j] else q[i][j]
        out[i][i]=-sum(out[i])
    return out


def recover(table):
    """Only the probability table and its explicit promises enter here."""
    start=time.perf_counter();r=table['complete_Hankel_rank_upper_promise'];I=identity(r)
    operators=observable(table);T=operators['T'];one=operators['one'];rho=operators['rho']
    Q0,Q1,C,Dp=[operators[k] for k in ['Q0','Q1','C','Dp']]
    nu=F(table['inspection_rate'])
    symbolic=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in row] for row in C])
    roots=symbolic.charpoly().as_poly().ground_roots()
    if sum(roots.values())!=r:
        raise RuntimeError('prototype needs rational hazard eigenvalues; algebraic spectral extension not implemented')
    distinct=sorted(F(int(x.p),int(x.q)) for x in roots)
    columns=[];hazards=[];joint_labels=[]
    for c in distinct:
        v=list(one)
        for d in distinct:
            if c==d:continue
            v=[(x-d*y)/(c-d) for x,y in zip(mv(C,v),v)]
        for label,D in ((-1,operators['Dm']),(1,Dp)):
            col=mv(D,v)
            if any(col):columns.append(col);hazards.append(c);joint_labels.append(label)
    if len(columns)!=r:
        raise RuntimeError('observable joint hazard spectrum is not simple')
    E=[list(row) for row in zip(*columns)];Ei=inverse(E)
    q=mm(mm(Ei,Q0),E);qh=mm(mm(Ei,Q1),E);dplus=mm(mm(Ei,Dp),E);pic=rmv(rho,E)
    labels=[]
    for i in range(r):
        assert all(dplus[i][j]==0 for j in range(r) if i!=j) and dplus[i][i] in (0,1)
        labels.append(1 if dplus[i][i] else -1)
    assert labels==joint_labels
    assert all(sum(row)==0 for row in q) and all(q[i][j]>=0 for i in range(r) for j in range(r) if i!=j)
    assert all(x>0 for x in pic) and sum(pic)==1 and all(x==0 for x in rmv(pic,q))
    mp,mn=operators['plus_crossing_multiplier'],operators['minus_crossing_multiplier']
    assert qh==scaled_crossings(q,labels,mp,mn)
    assert [sum(q[i][j] for j in range(r) if labels[i]!=labels[j]) for i in range(r)]==hazards
    canonicalT=[]
    for z in (q,qh):
        B=resolvent(z,nu)
        for bit in (-1,1):canonicalT.append(mm(B,diagonal([F(x==bit) for x in labels])))
    assert all(mm(mm(Ei,A),E)==B for A,B in zip(T,canonicalT))
    assert mv(E,[F(1)]*r)==one
    ep=entropy(q,pic)
    return {'Q':encode(q),'pi':list(map(str,pic)),'labels':labels,'cross_label_hazards':list(map(str,hazards)),
            'entropy_rate_interval':list(map(str,ep)),'entropy_rate_preview':[float(x) for x in ep],
            'all_four_observable_operator_identities_exact':True,'rank_promise_required_for_finite_completion':True,
            'identified_plus_crossing_multiplier':str(mp),'identified_minus_crossing_multiplier':str(mn),
            'elapsed_wall_seconds':time.perf_counter()-start}


def fixture4():
    n=4;q=[[F(0)]*n for _ in range(n)]
    for i,j,w in [(0,1,1),(0,2,2),(0,3,3),(1,2,4),(1,3,5),(2,3,6)]:q[i][j]=q[j][i]=F(w)
    for i in range(n):q[i][(i+1)%n]+=3
    for i in range(n):q[i][i]=-sum(q[i])
    return q,[F(1,4)]*4,[1,1,-1,-1]


def main():
    OUT.mkdir(parents=True,exist_ok=True);start=time.perf_counter();base=json.loads((OUT/'retuned_receipt.json').read_text())
    fixtures=[('four_state',*fixture4()),('work_source',decode(base['Q']),list(map(F,base['stationary_pi'])),base['labels']),
              ('work_gauge',decode(base['Q_gauge']),list(map(F,base['stationary_pi'])),base['labels'])]
    results=[]
    for name,q,pi,f in fixtures:
        begin=time.perf_counter();oracle=ProbabilityOracle(q,pi,f);table=make_table(oracle,len(q));tablepath=OUT/(name+'_table.json')
        tablepath.write_text(json.dumps(table,indent=2)+'\n')
        print(json.dumps({'stage':'exact_table_ready','name':name,'queries':table['source_unique_probability_queries'],
                          'table_seconds':time.perf_counter()-begin}),flush=True)
        result=recover(json.loads(tablepath.read_text()))
        hazards=[sum(q[i][j] for j in range(len(q)) if f[i]!=f[j]) for i in range(len(q))]
        order=sorted(range(len(q)),key=lambda i:(hazards[i],f[i]))
        assert decode(result['Q'])==[[q[i][j] for j in order] for i in order]
        assert list(map(F,result['pi']))==[pi[i] for i in order]
        result.update(name=name,physical_source_recovered_up_to_permutation=True,
                      complete_Hankel_rank_upper_promise=len(q),source_query_cost={k:v for k,v in table.items() if k.startswith('source_')},
                      table_SHA256=hashlib.sha256(tablepath.read_bytes()).hexdigest(),
                      total_fixture_elapsed_wall_seconds=time.perf_counter()-begin)
        results.append(result)
        print(json.dumps({'stage':'exact_reconstruction_passed','name':name,'entropy':result['entropy_rate_preview'],
                          'seconds':result['total_fixture_elapsed_wall_seconds']}),flush=True)
    data={'status':'CALIBRATED_BINARY_GENERATOR_RECONSTRUCTION_CONTROLS_PASSED','fixtures':results,
          'new_acquisitions':0,'physical_experiments':0,'elapsed_wall_seconds':time.perf_counter()-start,
          'input_contract':'exact mathematical probabilities plus finite rank upper promise; not learned from a finite record',
          'ordinary_incumbent':'same Hankel observable-operator realization supplies all protocol predictions',
          'extra_step':'calibrated finite-field hazard operator fixes physical coordinates and generator entropy',
          'sample_or_runtime_advantage_established':False}
    (OUT/'tomography_receipt.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='fixtures'},indent=2))


if __name__=='__main__':main()
