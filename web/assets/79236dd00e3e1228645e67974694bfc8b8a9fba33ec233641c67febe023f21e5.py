"""Exact support-cone checks for the Spin(13) extracted star blocks.

Checks the five attained seed lower support, and separately uses a valid
full-domain canonical-EB moment outer bound to search for a strict obstruction.
All calculations are in the reduced ordinary-tensor blocks from the extractor.
"""
from itertools import combinations, product
from functools import reduce
from math import gcd, comb
from pathlib import Path
import json
import sympy as sp

HERE=Path(__file__).parent
STAR=json.loads((HERE/'spin13_fullstar_blocks.json').read_text())
SEEDS=json.loads((HERE/'spin13_pair_support_certificate.json').read_text())['attained_seed_moments_grades1_to6']
SEED_NAMES=list(SEEDS)
SEED_V=[sp.Matrix(SEEDS[name]) for name in SEED_NAMES]
D=64
N=6
TRACE=sp.Matrix(STAR['trace_coefficients'])


def mat(obj):
    return sp.Matrix([[sp.Rational(x) for x in row] for row in obj])


def primitive(q):
    den=sp.ilcm(*[x.q for x in q])
    vals=[int(x*den) for x in q]
    g=reduce(gcd,(abs(x) for x in vals),0)
    return tuple(x//g for x in vals)


def extreme_rays(rows):
    rays=set()
    for inds in combinations(range(len(rows)),N-1):
        M=sp.Matrix.vstack(*(rows[i] for i in inds))
        if M.rank()!=N-1:
            continue
        ker=M.nullspace()
        if len(ker)!=1:
            continue
        q=ker[0]
        for sign in (1,-1):
            v=sign*q
            if all((row*v)[0]>=0 for row in rows):
                rays.add(primitive(list(v)))
                break
    return rays


def support_cones(vertices):
    out=[]
    for i,v in enumerate(vertices):
        rows=[sp.eye(N).row(j) for j in range(N)]
        rows += [(v-w).T for j,w in enumerate(vertices) if j!=i]
        out.append((i,extreme_rays(rows)))
    return out


def principal_minors_psd(G):
    undec=[]; negative=[]; checked=0; cert=[]
    for size in range(1,G.rows+1):
        for inds in combinations(range(G.rows),size):
            det=sp.factor(G.extract(inds,inds).det()); checked+=1
            cert.append({'indices':list(inds),'determinant':str(det)})
            if det.is_negative is True:
                negative.append((inds,det))
            elif det.is_nonnegative is not True:
                undec.append((inds,det))
    return not negative and not undec,checked,negative,undec,cert


def witness(G,H,bound):
    """Find a small integer direction with x^T(H-bound*G)x>0."""
    for radius in (1,2,3,4):
        for vals in product(range(-radius,radius+1),repeat=G.rows):
            if not any(vals):
                continue
            x=sp.Matrix(vals)
            den=(x.T*G*x)[0]
            num=(x.T*(H-bound*G)*x)[0]
            if den>0 and num>0:
                return {'x':list(vals),'rayleigh':str(sp.factor(num/den)),
                        'numerator_over_gram':str(sp.factor(num)),'gram_norm':str(sp.factor(den))}
    return None


def seed_lower_test():
    cones=support_cones(SEED_V)
    union=set().union(*(r for _,r in cones))
    records=[]; failures=[]; undecided=[]; minors=0
    for ray in sorted(union):
        a=sp.Matrix(ray)
        vals=[(v.T*a)[0] for v in SEED_V]
        sup=max(vals); winners=[SEED_NAMES[i] for i,x in enumerate(vals) if x==sup]
        bound=(TRACE.T*a)[0]+sup
        blocks=[]
        for key,obj in STAR['blocks'].items():
            G=mat(obj['gram']); Bs=[mat(x) for x in obj['bilinear_H']]
            H=sum((a[k]*Bs[k] for k in range(N)),sp.zeros(G.rows))
            gap=sp.simplify(bound*G-H)
            ok,n,bad,unk,cert=principal_minors_psd(gap); minors+=n
            blocks.append({'block':key,'order':G.rows,'psd':ok,'principal_minors':cert})
            if bad: failures.append({'ray':list(ray),'winners':winners,'block':key,
                                     'negative_minors':[(list(ix),str(v)) for ix,v in bad]})
            if unk: undecided.append({'ray':list(ray),'winners':winners,'block':key,
                                      'undecided_minors':[(list(ix),str(v)) for ix,v in unk]})
        records.append({'ray':list(ray),'seed_support':str(sup),'winner_seeds':winners,
                        'trace':str((TRACE.T*a)[0]),'support_bound':str(bound),'blocks':blocks})
    return {'cone_ray_counts':[len(r) for _,r in cones],'distinct_rays':len(union),
            'rays':records,'minor_checks':minors,'failures':failures,'undecided':undecided}


def outer_vertices():
    # s1<=1, s2<=6, nonnegative s3..s6, total sum=63.
    vs=[]
    for j in range(2,6):
        for rem,s1,s2 in ((63,0,0),(62,1,0),(57,0,6),(56,1,6)):
            v=[0]*6; v[0]=s1; v[1]=s2; v[j]=rem; vs.append(sp.Matrix(v))
    return vs


def upper_test_on_seed_rays(seed_result):
    # A single strict violation of this valid outer support is decisive. Search
    # every attained-support ray from the preceding complete cone enumeration.
    uv=outer_vertices(); rays=sorted({tuple(x['ray']) for x in seed_result['rays']})
    checked=[]; violations=[]; minors=0
    for ray in rays:
        a=sp.Matrix(ray); scores=[(v.T*a)[0] for v in uv]; sup=max(scores)
        bound=(TRACE.T*a)[0]+sup
        for key,obj in STAR['blocks'].items():
            G=mat(obj['gram']); Bs=[mat(x) for x in obj['bilinear_H']]
            H=sum((a[k]*Bs[k] for k in range(N)),sp.zeros(G.rows))
            gap=sp.simplify(bound*G-H)
            ok,n,bad,unk,_=principal_minors_psd(gap); minors+=n
            if not ok:
                xw=witness(G,H,bound)
                rec={'ray':list(ray),'outer_support':str(sup),'trace':str((TRACE.T*a)[0]),
                     'support_bound':str(bound),'block':key,'gap_psd':False,
                     'negative_minors':[(list(ix),str(v)) for ix,v in bad],
                     'undecided_minors':[(list(ix),str(v)) for ix,v in unk],
                     'positive_rayleigh_witness':xw}
                violations.append(rec)
            checked.append({'ray':list(ray),'block':key,'gap_psd':ok})
    return {'candidate_ray_count':len(rays),'block_ray_checks':len(checked),
            'principal_minor_checks':minors,'violations':violations,'checks':checked}


def exact_axis_checks():
    # Grade-1 exact support is 1 by Clifford anticommutation. Isotropic support
    # is 63 by Parseval. These checks anchor the normalization of the star.
    out={}
    for name,a in (('grade1',[1,0,0,0,0,0]),('isotropic',[1]*6)):
        a=sp.Matrix(a)
        sup=sp.Integer(1) if name=='grade1' else sp.Integer(63)
        bound=(TRACE.T*a)[0]+sup
        bad=[]; unknown=[]; count=0
        for key,obj in STAR['blocks'].items():
            G=mat(obj['gram']); Bs=[mat(x) for x in obj['bilinear_H']]
            H=sum((a[k]*Bs[k] for k in range(N)),sp.zeros(G.rows))
            ok,n,neg,unk,_=principal_minors_psd(sp.simplify(bound*G-H)); count+=n
            if neg: bad.append({'block':key,'negative':[(list(ix),str(v)) for ix,v in neg]})
            if unk: unknown.append({'block':key,'undecided':[(list(ix),str(v)) for ix,v in unk]})
        out[name]={'support':str(sup),'trace':str((TRACE.T*a)[0]),'bound':str(bound),
                   'all_blocks_psd':not bad and not unknown,'principal_minor_checks':count,
                   'failures':bad,'undecided':unknown}
    return out


def gram_checks():
    records=[]
    for key,obj in STAR['blocks'].items():
        G=mat(obj['gram'])
        leading=[sp.factor(G[:j,:j].det()) for j in range(1,G.rows+1)]
        if not all(x.is_positive is True for x in leading):
            raise AssertionError(('non-positive Gram metric',key,leading))
        records.append({'block':key,'order':G.rows,'leading_principal_minors':[str(x) for x in leading]})
    return records


def main():
    lower=seed_lower_test()
    upper=upper_test_on_seed_rays(lower)
    axes=exact_axis_checks()
    gram=gram_checks()
    result={'seed_support_test':lower,'valid_outer_support_search_on_seed_cone_rays':upper,
            'axis_normalization_checks':axes,'positive_gram_metric_checks':gram,
            'status':('STRICT_GLOBAL_OBSTRUCTION_FOUND' if upper['violations'] else
                      'SEED_LOWER_BOUND_PASSES' if not lower['failures'] and not lower['undecided'] else
                      'NO_DECISIVE_COUNTEREXAMPLE')}
    out=HERE/'spin13_seed_star_check.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('seed rays',lower['cone_ray_counts'],'distinct',lower['distinct_rays'],
          'lower failures',len(lower['failures']),'undecided',len(lower['undecided']),
          'principal minors',lower['minor_checks'])
    print('outer search rays',upper['candidate_ray_count'],'block checks',upper['block_ray_checks'],
          'strict violations',len(upper['violations']))
    print('axis checks',axes)
    print('STATUS',result['status'])


if __name__=='__main__':main()
