#!/usr/bin/env python3
"""Exact exhaustive small policy-tree falsification tests for the new proof."""
from pathlib import Path
import itertools,json,hashlib,sys
import sympy as s
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent
sys.path.insert(0,str(PARENT.parent/'robust_operator_reuse_20261031'/'finite_observation'))
from robust_replay import norm_up,sqrt_up
R=s.Rational


def run():
    checks=0;cases=[]
    for n,parts in [(4,[[0,1],[2,3]]),(5,[[0,1],[2,3,4]])]:
        r=2;Z=s.zeros(n,r);W=s.zeros(r,n)
        for g,p in enumerate(parts):
            for i in p:Z[i,g]=1;W[g,i]=R(1,len(p))
        P=Z*W;Q=s.eye(n)-P;matrices=[]
        for a in range(2):
            E=s.Matrix(n,n,lambda i,j:((i+2*j+3*a)%5)-2)
            for i in range(n):E[i,n-1]-=sum(E.row(i))
            A=s.ones(n)/n+R(1,100)*E
            assert min(A)>=0 and A*s.ones(n,1)==s.ones(n,1);checks+=1;matrices.append(A)
        B=[W*A*Z for A in matrices];ein=max(norm_up(Q*A*P,s.eye(n)) for A in matrices)
        eout=max(sqrt_up(n*sum(x*x for x in (W*A*Q).row(g))) for A in matrices for g in range(r))
        U=s.zeros(r)
        for g,pg in enumerate(parts):
            for h,ph in enumerate(parts):
                U[g,h]=max(sqrt_up(sum(x*x for x in (Q*A*Q).extract(pg,ph))) for A in matrices)
        c=max(ein*sqrt_up(R(n,len(pg))) for pg in parts)
        k=max(sum(sqrt_up(R(len(ph),len(pg)))*U[g,h] for h,ph in enumerate(parts)) for g,pg in enumerate(parts))
        z=R(0);err=R(0);b=Z*s.Matrix([1,0])
        # Each option retains (true function on current block, same-tree coarse
        # scalar). Child options may differ independently for every block.
        options=[[(b.extract(pg,[0]),R(1-g))] for g,pg in enumerate(parts)]
        coarse=s.Matrix([1,0]);chosen=b;counts=[]
        for depth in range(1,4):
            error_next=err+eout*z;z_next=min(R(1),c+k*z);new=[]
            candidate_coarse=[M*coarse for M in B]
            policy=[max(range(2),key=lambda a:(candidate_coarse[a][g],-a)) for g in range(r)]
            newchosen=s.zeros(n,1)
            for g,pg in enumerate(parts):
                values=[]
                for children in itertools.product(*options):
                    full=s.zeros(n,1)
                    for h,ph in enumerate(parts):
                        for j,i in enumerate(ph):full[i]=children[h][0][j]
                    cv=s.Matrix([x[1] for x in children])
                    for a,A in enumerate(matrices):
                        fv=(A*full).extract(pg,[0]);coarsev=(B[a]*cv)[g];mean=sum(fv)/len(pg)
                        assert abs(mean-coarsev)<=error_next;checks+=1
                        residual=fv-s.ones(len(pg),1)*mean
                        assert residual.dot(residual)/len(pg)<=z_next*z_next;checks+=1
                        values.append((fv,coarsev))
                assert max(x[1] for x in values)==candidate_coarse[policy[g]][g];checks+=1
                got=(matrices[policy[g]]*chosen).extract(pg,[0]);mean=sum(got)/len(pg)
                assert max(sum(x[0])/len(pg) for x in values)-mean<=2*error_next;checks+=1
                for j,i in enumerate(pg):newchosen[i]=got[j]
                new.append(values)
            options=new;coarse=s.Matrix([candidate_coarse[policy[g]][g] for g in range(r)])
            chosen=newchosen;z=z_next;err=error_next;counts.append([len(x) for x in options])
        cases.append({'n':n,'blocks':parts,'history_tree_counts_per_initial_block':counts,'incoming':str(ein),
          'outgoing':str(eout),'kappa':str(k),'history_error_depth3':str(err)})
    return {'status':'PASS_EXACT_SMALL_HISTORY_TREES','checks':checks,'cases':cases,
      'scope':'Exhaustive deterministic block-observation history trees through horizon3; fixed true rational fixtures, not sampled acquisition or proof of large-world truth. New unreviewed extension.',
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    out=run();(ROOT/'history_tree_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
