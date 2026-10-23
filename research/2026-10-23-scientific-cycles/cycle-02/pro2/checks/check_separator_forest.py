#!/usr/bin/env python3
"""Exact receiving fixtures for the actual separator/forest decoder."""
import argparse,json,resource,sys,time
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from separator_forest import design,seed,action,decode,selected_cells,frobenius_squared


def run():
    start=time.perf_counter(); cpu=time.process_time()
    cases=[]
    fixtures=[(0,[],[]),(1,[],[]),(5,[(0,1),(0,2),(2,3)],[]),
              (6,[(0,1),(0,2),(0,3),(1,2),(2,3),(3,4)], [0]),
              (7,[(0,1),(0,2),(1,2),(0,3),(1,4),(2,3),(3,4),(4,5)], [0,1]),
              (5,[(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(3,4)],[0,1]),
              (4,[(0,1),(0,2),(1,2),(2,3)],[0,1,2,3])]
    for case,(n,edges,S) in enumerate(fixtures):
        plan=design(n,edges,S)
        X=seed(plan,F(1),F(0))
        assert all(sum(a*a for a in x)==1 for x in X)
        coeff={(i,i):F((-1)**i*(i+1),7) for i in range(n)}
        coeff.update({(min(i,j),max(i,j)):F((-1)**k*(k+2),11) for k,(i,j) in enumerate(edges)})
        Y=action(plan,coeff)
        assert decode(plan,Y)==coeff
        E=[[F(((i+3)*(j+2)+case)%13-6,101) for j in range(plan.q)] for i in range(n)]
        noisy=[[a+b for a,b in zip(yr,er)] for yr,er in zip(Y,E)]
        got=decode(plan,noisy)
        error={key:got[key]-value for key,value in coeff.items()}
        e2=sum(a*a for row in E for a in row)
        assert frobenius_squared(error)<=2*e2
        chosen=[cell for cells in selected_cells(plan).values() for cell in cells]
        assert len(chosen)==len(set(chosen))
        # Exact dual coefficient inequality for nonnegative rational weights.
        w=[F(i+1, n*(n+1)//2) for i in range(n)] if n else []
        Sset=set(S)
        adj2=sum(a*a for a in w)+sum((2 if i in Sset and j in Sset else 4)*w[i]*w[j] for i,j in edges)
        assert adj2 <= (F(5,3) if S else F(3,2))
        cases.append({'n':n,'separator_size':len(S),'queries':plan.q,'edges':len(edges),
                      'error_frobenius_squared':str(frobenius_squared(error)),
                      'noise_frobenius_squared':str(e2),'distinct_selected_cells':len(chosen)})
    invalid=[(3,[(0,1),(1,2),(0,2)],[]),(2,[(0,1),(1,0)],[]),
             (2,[(0,0)],[]),(2,[(0,2)],[]),(2,[],[0,0]),(2,[],[2])]
    for args in invalid:
        try: design(*args)
        except ValueError: pass
        else: raise AssertionError('invalid input accepted')
    # Exact sharp operator example for the implemented decoder.
    p=design(3,[(0,1),(0,2),(1,2)],[0])
    E=[[F(0)]*p.q for _ in range(3)]
    for (i,j),cells in selected_cells(p).items():
        for a,b in cells: E[a][b]=F(1,3) if i==j else F(2,3)
    H=decode(p,E)
    assert all(H[(i,i)]==F(1,3) for i in range(3))
    assert all(H[e]==F(2,3) for e in p.edges)
    assert sum(a*a for row in E for a in row)==F(5,3)
    # H=(2/3)11^T-(1/3)I: exact operator norm5/3, ratio squared5/3.
    return {'status':'passed','cases':cases,'invalid_inputs_rejected':len(invalid),
            'sharp_operator_ratio_squared':'5/3','wall_seconds':time.perf_counter()-start,
            'cpu_seconds':time.process_time()-cpu,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();ans=run();text=json.dumps(ans,indent=2)+'\n'
    if args.output: args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    print(text,end='')
