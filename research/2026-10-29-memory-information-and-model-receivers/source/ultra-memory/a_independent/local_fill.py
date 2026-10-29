"""Exact local-generation discriminant on supplied finite complexes.

Graph balls are explicitly NOT the BHM spatial cube contract.  A failing
stabilizer witness can be interpreted algebraically without a geometric oracle;
a passing finite collection proves only those literal inclusion checks.
"""
from pathlib import Path
from collections import defaultdict
import json,time,argparse
from compile_complex import load,basis,bits,reduce


def quotient_signatures(rows,n):
    b=basis(rows);pivots=sorted(b,reverse=True)
    residues=[]
    for i in range(n):
        x=1<<i
        for p in pivots:
            if (x>>p)&1:x^=b[p]
        residues.append(x)
    groups=defaultdict(list)
    for i,s in enumerate(residues):groups[s].append(i)
    return b,groups


def neighbours(c):
    out=[1<<i for i in range(c.n)]
    for s in c.xs+c.zs:
        for i in bits(s):out[i]|=s
    return out


def grow(A,adj):
    B=A
    for i in bits(A):B|=adj[i]
    return B


def local_basis(rows,B):return basis(x for x in rows if x&~B==0)


def local_dimension(rows,A,B):
    selected=[x for x in rows if x&~B==0]
    return len(basis(selected))-len(basis(x&~A for x in selected))


def query(c,A,guard,adj):
    B=A
    for _ in range(guard):B=grow(B,adj)
    out={'A_size':A.bit_count(),'B_size':B.bit_count(),'guard':guard}
    for name,rows in [('X',c.xs),('Z',c.zs)]:
        glob=len(basis(rows))-len(basis(x&~A for x in rows))
        loc=local_dimension(rows,A,B)
        out[name]={'global_supported_rank':glob,'locally_generated_supported_rank':loc,'deficit':glob-loc}
    return out


def main():
    p=Path(__file__).parent;parser=argparse.ArgumentParser()
    parser.add_argument('--level',type=int,default=2);parser.add_argument('--queries',type=int,default=32)
    args=parser.parse_args();t0=time.perf_counter();c=load(p/'complexes'/f'level_{args.level}.json')
    adj=neighbours(c);out={'level':args.level,'n':c.n,'small_stabilizers':{}}
    for name,rows in [('X',c.xs),('Z',c.zs)]:
        _,groups=quotient_signatures(rows,c.n)
        single=groups.get(0,[]);pairs=[(a,b) for g in groups.values() for j,a in enumerate(g) for b in g[j+1:]]
        # Literal minimum check-neighbourhood generation radius, not inferred
        # geometric proximity and not a quantum logical-distance calculation.
        witnesses=[]
        for a,b in pairs[:10000]:
            s=(1<<a)|(1<<b);B=s
            for radius in range(20):
                if reduce(s,local_basis(rows,B))==0:
                    witnesses.append({'a':a,'b':b,'radius':radius,'neighbourhood_size':B.bit_count()});break
                B=grow(B,adj)
            else:raise AssertionError('global stabilizer did not fill')
        out['small_stabilizers'][name]={'weight1':single,'weight2_count':len(pairs),
                                      'weight2_checked':len(witnesses),'max_radius':max((x['radius'] for x in witnesses),default=None),
                                      'largest_radius_examples':sorted(witnesses,key=lambda x:x['radius'],reverse=True)[:8]}
    # Predeclared deterministic equally spaced centers, no sign-conditioned
    # postselection.  Count distinct queried balls explicitly.
    centers=sorted({j*(c.n-1)//max(1,args.queries-1) for j in range(args.queries)})
    tests=[]
    for center in centers:
        A=adj[center]
        for guard in (0,1):
            tests.append({'center':center,**query(c,A,guard,adj)})
    out['ball_tests']=tests;out['wall_seconds']=time.perf_counter()-t0
    out['scope']='Literal finite graph-neighbourhood algebra only. No spatial TQO-2, perturbation theorem, all-level theorem or memory advantage inferred.'
    (p/f'LOCAL_FILL_{args.level}.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k!='ball_tests'},indent=2))
    print(json.dumps({'queries':len(tests),'deficit_counts':{str(g):sum(t[n]['deficit']>0 for t in tests if t['guard']==g for n in ('X','Z')) for g in (0,1)}}))


if __name__=='__main__':main()
