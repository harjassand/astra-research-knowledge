"""Equally informed conventional candidate extraction on the SAME raw DAG.

The raw benchmark visibly retains x_i+x_j^2 subgraphs. An ordinary symbolic
pattern/CSE pass can exploit them; hiding syntax would make an unfair comparator.
Candidate validation uses the same exact rational arithmetic/fresh PIT contract.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib,secrets,time
import sympy as s
from strong_decoder import DAG,strong_decoder,summary
from quadratic_circuit_acquisition import formal_degree,monomials,value_grad


def load_circuit(serialized):
    c=DAG(serialized['n'])
    for i,(op,*args) in enumerate(serialized['nodes']):
        if op=='const':args=[Q(args[0])]
        assert c.node(op,*args)==i
    return c,serialized['roots']


def extract(c,raw):
    candidates={i:[] for i in range(c.n)}
    for r in c.reachable(raw):
        op,*a=c.nodes[r]
        if op!='add':continue
        for left,right in [a,a[::-1]]:
            lo,*la=c.nodes[left];ro,*ra=c.nodes[right]
            if lo=='var' and ro=='mul' and ra[0]==ra[1] and c.nodes[ra[0]][0]=='var':
                candidates[la[0]].append(r)
    if any(len(v)>1 for v in candidates.values()):return None
    return [v[0] if v else c.variables[i] for i,v in candidates.items()]


def run(record):
    c,raw=load_circuit(record['raw_circuit']);n=c.n;start=time.perf_counter()
    candidate=extract(c,raw)
    if candidate is None:return {'status':'AMBIGUOUS_PATTERN'}
    extraction=time.perf_counter()-start
    x=s.symbols('x0:'+str(n));F=c.expand(candidate,x) # quadratic candidates only
    mons=monomials(n);coeff=[]
    for p in [s.Integer(1)]+list(F):
        poly=s.Poly(p,*x);coeff.append([Q(poly.coeff_monomial(s.prod(x[i] for i in m))) for m in mons])
    d=formal_degree(c,raw);q=c.manufacture_q(raw);roots=raw+[q]
    def point(a):
        vals,_=c.evaluate(roots,a);vg=[value_grad(p,mons,a) for p in coeff]
        return [v for v,g in vg],[vals[-1]*v+sum(f*b for f,b in zip(vals[:-1],g)) for v,g in vg]
    points=[[Q(0)]*n]
    for i in range(n):a=[Q(0)]*n;a[i]=1;points.append(a)
    phis=[];Ts=[]
    for a in points:v,t=point(a);phis.append(v);Ts.append(t)
    E=s.Matrix(phis).T
    if E.det()==0:return {'status':'SINGULAR_CANDIDATE_EVALUATIONS'}
    A=s.Matrix(Ts).T*E.inv();Qsize=2**32;r=3
    for _ in range(r):
        a=[Q(secrets.randbelow(Qsize)) for _ in range(n)];v,t=point(a)
        if s.Matrix(t)!=A*s.Matrix(v):return {'status':'PROJECTIVE_CANDIDATE_REJECTED'}
    t=time.perf_counter();dec=strong_decoder(F,x);dec_seconds=time.perf_counter()-t
    assert dec['status']=='EXACT_FLAG_CERTIFIED_INVERSE_DAG'
    assert A==s.Matrix(record['normalized_matrix'])
    acquired=s.Matrix([s.sympify(v) for v in record['chart']]);zero=dict.fromkeys(x,0)
    normalized=acquired.jacobian(x).subs(zero).inv()*(acquired-acquired.subs(zero))
    assert all(s.expand(v)==0 for v in F-normalized)
    return {'status':'SAME_SYNTAX_CONVENTIONAL_CANDIDATE_ACCEPTED','n':n,
       'candidate_extraction_seconds':extraction,'total_including_decoder_seconds':time.perf_counter()-start,
       'decoder_certificate_build_seconds':dec_seconds,'training_points':n+1,'fresh_verification_points':r,
       'false_acceptance_union_bound':str((n+1)*Q(d+1,Qsize)**r),
       'normalization_matches_independently_replayed_compiler_output':True,
       'candidate_gate_ids':candidate,'chart':[str(v) for v in F],
       'matrix':[[str(v) for v in row] for row in A.tolist()], 'decoder':summary(dec)}


def main():
    root=Path(__file__).parent;source=root/'quadratic_circuit_results.json'
    reports=[run(v) for v in json.loads(source.read_text())['runs']]
    assert all(v['status']=='SAME_SYNTAX_CONVENTIONAL_CANDIDATE_ACCEPTED' for v in reports)
    out={'verdict':'NO demonstrated algorithmic advantage: ordinary syntax/CSE recognition recovers the literal constructor chart.',
         'timing_warning':'Different operation mixes; times are evidence of tractability, not a general speed ratio.',
         'reports':reports,'source_hashes':{str(p.name):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,Path(__file__)]}}
    (root/'same_syntax_comparator_results.json').write_text(json.dumps(out,indent=2))
    for v in reports:print({k:z for k,z in v.items() if k not in ['chart','matrix','candidate_gate_ids']},flush=True)


if __name__=='__main__':main()
