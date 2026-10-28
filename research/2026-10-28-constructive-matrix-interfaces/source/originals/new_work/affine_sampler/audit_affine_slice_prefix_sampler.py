#!/usr/bin/env python3
"""Independent exact prefix, uniformity, and original-gate audits."""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction
import argparse,json,random,sys,time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from affine_slice_prefix_sampler import *

class PolynomialField:
    def __init__(self,modulus):
        self.modulus=modulus;self.a=modulus.bit_length()-1;self.q=1<<self.a;self.one=1
    def mul(self,x,y):
        out=0
        while y:
            if y&1:out^=x
            y>>=1;x<<=1
            if x&self.q:x^=self.modulus
        return out
    def inv(self,x):
        if not x:raise ValueError('zero inverse')
        out=1
        for _ in range(self.q-2):out=self.mul(out,x)
        return out

def matrix(F,w,h,r):
    return [[(w>>(F.a*(i*r+j)))&(F.q-1) for j in range(r)] for i in range(h)]

def literal_product(F,x,y,p,d,r):
    X=matrix(F,x,p,d);Y=matrix(F,y,d,r);out=0
    for i in range(p):
        for j in range(r):
            value=0
            for k in range(d):value^=F.mul(X[i][k],Y[k][j])
            out|=value<<(F.a*(i*r+j))
    return out

def parts(F,w,used,r):
    t,b=divmod(used,F.a*r)
    return matrix(F,w,t,r),(w>>(t*F.a*r))&((1<<b)-1),b

def literal_controls():
    records=[];rng=random.Random(281301)
    for mod,p,d,r in ((3,1,2,2),(3,2,2,2),(3,2,2,3),(7,1,2,2),(7,2,2,2),(11,1,1,2)):
        F=PolynomialField(mod);width=F.a*d*r;pop=defaultdict(Counter)
        for x in range(1<<(F.a*p*d)):
            for y in range(1<<width):pop[literal_product(F,x,y,p,d,r)][y]+=1
        targets=list(dict.fromkeys([0,1,rng.randrange(1<<(F.a*p*r))]))
        sets=[[],[(1,1)],[(1,1),(1<<min(width-1,F.a*(r+1)),1)]]
        if F.a>1:sets.append([(1,1),(2,0),(1<<(width-1),1)])
        checks=leaves=samples=0
        for z in targets:
            Z=matrix(F,z,p,r)
            for eqs in sets:
                S=AffineMatrixSliceSampler(F,Z,d,eqs,rng)
                expected={y:v for y,v in pop[z].items() if all(((mask&y).bit_count()&1)==b for mask,b in eqs)}
                assert S.population==sum(expected.values())
                counts={}
                for used in range(width+1):
                    sums=Counter()
                    for y,v in expected.items():sums[y&((1<<used)-1)]+=v
                    for word in range(1<<used):
                        got=S.count_prefix(*parts(F,word,used,r))
                        assert got==sums[word],(mod,p,d,r,z,eqs,used,word,got,sums[word])
                        counts[used,word]=got;checks+=1
                for y,left in expected.items():
                    probability=Fraction(1,1)
                    for used in range(width):
                        probability*=Fraction(counts[used+1,y&((1<<(used+1))-1)],counts[used,y&((1<<used)-1)])
                    assert probability/left==Fraction(1,S.population);leaves+=1
                if S.population:
                    for _ in range(4):
                        X,Y=S.sample();y=pack_vector(F,[v for row in Y for v in row])
                        assert y in expected and matmul(F,X,Y,r)==Z;samples+=1
        rec=dict(field_order=F.q,p=p,d=d,r=r,literal_factor_pairs=1<<(F.a*(p*d+d*r)),
                 prefix_count_checks=checks,exact_uniform_leaf_probability_checks=leaves,sampled_pair_checks=samples)
        records.append(rec);print(json.dumps(dict(event='literal_prefix_passed',**rec)),flush=True)
    bad=AffineMatrixSliceSampler(PolynomialField(3),[[0,0]],2,[(0,1)])
    assert bad.population==0
    try:bad.sample()
    except ValueError:pass
    else:raise AssertionError('empty slice sampled')
    return records

def signed_controls():
    F=PolynomialField(3);checks=0
    for z in (0,1,9,15):
        Z=matrix(F,z,2,2);weights=Counter()
        for x in range(16):
            for y in range(16):
                if literal_product(F,x,y,2,2,2)==z:weights[y]+=1
        S=AffineMatrixSliceSampler(F,Z,2)
        for dw in range(16):
            D=matrix(F,dw,2,2)
            for used in range(4):
                for word in range(1<<used):
                    rows,bits,b=parts(F,word,used,2);a0=rank_field(F,rows,2);k=rank_field(F,rows+Z,2)-a0
                    got=S._partial_signed(D,rows,bits,b,a0,k)
                    want=sum((-v if (dw&y).bit_count()&1 else v) for y,v in weights.items() if y&((1<<used)-1)==word)
                    assert got==want,(z,dw,used,word,got,want);checks+=1
    return dict(signed_prefix_checks=checks)

def gate_value(P,x):
    v=[(x>>j)&1 for j in range(P['inputs'])]
    for g in P['gates']:
        op=g['op'];a=[v[j] for j in g.get('args',[])]
        if op=='const':z=g['value']
        elif op=='not':z=1^a[0]
        elif op=='xor':z=a[0]^a[1]
        elif op=='and':z=a[0]&a[1]
        elif op=='or':z=a[0]|a[1]
        else:raise ValueError(op)
        v.append(z)
    return v[P['output']]

def native_controls(large=False):
    data=json.loads((SOURCE/'work_trace_frontier/affine_unsaturated_bilinear_audit_results.json').read_text())
    cases=data['small_cases']+data['native_cases'];records=[]
    if large:cases=[dict(fixture='matrix_affine_diamond_native_n72.json',result={'ones':71210970084540416})]
    for i,case in enumerate(cases):
        folder='work_phase_diamond' if large else 'work_trace_frontier'
        path=SOURCE/folder/case['fixture'];P=json.loads(path.read_text());begun=time.perf_counter()
        S,result=compile_native(P,random.Random(281501+i));assert S.population==case['result']['ones']
        failures=0;draws=[]
        for _ in range(1 if large else 8):
            draw=S.sample();assert gate_value(P,draw['assignment'])==1;draws.append(draw['assignment'])
            old=S.split['affine_offset']^apply_binary(S.split['coordinate_columns'],draw['local_assignment'])
            failures+=int(gate_value(P,old)!=1)
        witness=S.witness();assert gate_value(P,witness['assignment'])==1
        Q=S.coords
        yword=apply_binary(Q.hom_columns,witness['full_hom_coordinates'])
        used=min(Q.a*Q.d*Q.r, max(1,Q.a*Q.r+1))
        rows,bits,b=parts(Q.F,yword,used,Q.r)
        equations=S.prefix_constraints_on_original(rows,bits,b)
        assert all(((mask&witness['assignment']).bit_count()&1)==rhs for mask,rhs in equations)
        prefix_count=S.engine.count_prefix(rows,bits,b)
        original_prefix_checks=0
        if P['inputs']<=13:
            literal=sum(gate_value(P,x) for x in range(1<<P['inputs'])
                        if all(((mask&x).bit_count()&1)==rhs for mask,rhs in equations))
            assert literal==prefix_count,(case['fixture'],literal,prefix_count)
            original_prefix_checks=1<<P['inputs']
        from rank_one_dual_counter import acquire_rank_one_dual
        try:acquire_rank_one_dual(S.C);rank_one=True
        except ValueError:rank_one=False
        result.update(fixture=case['fixture'],old_rank_one_admission=rank_one,old_offset_failed_samples=failures,
                      samples=draws,all_original_gate_checks_passed=True,coordinate_acquisition=S.coords.stats,
                      witness=witness['assignment'],witness_original_gate_passed=True,
                      exported_original_prefix_equations=equations,exported_prefix_population=prefix_count,
                      original_assignments_in_prefix_crosscheck=original_prefix_checks,
                      prefix_stats=S.engine.stats,total_seconds=time.perf_counter()-begun)
        records.append(result)
        print(json.dumps(dict(event='native_slice_passed',n=P['inputs'],rank_one_admitted=rank_one,
                              population=S.population,seconds=result['total_seconds'])),flush=True)
    return records

def rejection_control():
    F=PolynomialField(3);p=64;records=[]
    full=(1<<(2*p))+9*(1<<p)+6
    for eqs,pop in (([(9,1)],6*(1<<p)+2), ([(1,1),(8,1)],(1<<p)+3)):
        S=AffineMatrixSliceSampler(F,[[0,0] for _ in range(p)],2,eqs,random.Random(281901))
        assert S.population==pop
        for _ in range(4):
            X,Y=S.sample();word=pack_vector(F,[v for row in Y for v in row])
            assert all(((mask&word).bit_count()&1)==rhs for mask,rhs in eqs)
            assert matmul(F,X,Y,2)==S.Z
        dual_ranks=sorted(set(rank_field(F,matrix(F,apply_binary([e[0] for e in eqs],word),2,2),2)
                             for word in range(1<<len(eqs))))
        assert 2 in dual_ranks
        records.append(dict(p=p,original_matrix_bits=2*p+4-len(eqs),binary_codimension=len(eqs),
                equations=eqs,dual_natural_ranks=dual_ranks,population=S.population,full_population=full,
                exact_rejection_acceptance=str(Fraction(S.population,full)),direct_samples=4,
                formula_stage_only=True,raw_acquisition_performed=False,stats=S.stats))
    return records

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--part',choices=['all','literal','native','large'],default='all');args=parser.parse_args()
    begun=time.perf_counter();out={'scope':args.part}
    if args.part in ('all','literal'):
        out['signed_controls']=signed_controls();out['literal_controls']=literal_controls();out['rejection_failure']=rejection_control()
    if args.part in ('all','native','large'):out['native_controls']=native_controls(args.part=='large')
    out.update(all_assertions_passed=True,seconds=time.perf_counter()-begun)
    path=HERE/('affine_slice_prefix_'+args.part+'_results.json');path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(event='audit_complete',part=args.part,seconds=out['seconds'],output=str(path))),flush=True)

if __name__=='__main__':main()
