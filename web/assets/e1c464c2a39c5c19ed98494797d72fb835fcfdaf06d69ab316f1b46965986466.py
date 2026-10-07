"""Exact rational partition-base extension of rounding_sparse_compiler.py."""
from fractions import Fraction as F
from math import comb
import json,time
from itertools import product
from rounding_sparse_compiler import compress,check


def floor(v):return v.numerator//v.denominator

def moment_sign(D,s,counter):
    m=len(D);t=len(D[0]) if m else 0;r=(2*m-1).bit_length();degree=2*r
    if not t:return []
    suffix=[]
    for d in D:
        moments=[[F(0)]*(degree+1) for _ in range(t+1)];moments[-1][0]=F(1)
        for j in range(t-1,-1,-1):
            for ell in range(0,degree+1,2):
                moments[j][ell]=sum(F(comb(ell,v))*d[j]**v*moments[j+1][ell-v]
                                   for v in range(0,ell+1,2))
        suffix.append(moments)
    prefix=[F(0)]*m;eta=[]
    for j in range(t):
        costs=[]
        for sign in (-1,1):
            costs.append(sum(sum(F(comb(degree,ell))*(prefix[i]+sign*D[i][j])**(degree-ell)*suffix[i][j+1][ell]
                                 for ell in range(0,degree+1,2)) for i in range(m)))
        sign=-1 if costs[0]<=costs[1] else 1;eta.append(sign)
        for i in range(m):prefix[i]+=sign*D[i][j]
    assert all(sum(d*d for d in row)<=4*s for row in D)
    assert all(sum(d*x for d,x in zip(row,eta))**2<16*r*s for row in D)
    counter['signing_calls']+=1
    counter['max_signing_size']=max(counter['max_signing_size'],s)
    return eta


def partition_law(A,p,blocks):
    A=[[F(v) for v in row] for row in A];p=[F(v) for v in p]
    n=len(p);m=len(A);J=(n-1).bit_length();g=F(1,2**J)
    assert sorted(j for b in blocks for j in b)==list(range(n))
    targets=[sum(p[j] for j in b) for b in blocks]
    assert all(x.denominator==1 for x in targets)
    assert all(0<=v<=1 for v in p) and all(abs(v)<=1 for row in A for v in row)
    baseline=[int(v>F(1,2)) for v in p];defect=[1-2*b for b in baseline]
    mu=sum(min(v,1-v) for v in p)
    counter={'signing_calls':0,'max_signing_size':0,'compression_deletions':0,'max_precompression_support':0}
    if mu<1:
        law=[(tuple(F(v) for v in baseline),1-mu/2)]
        for block in blocks:
            neg=[[j,1-p[j]] for j in block if baseline[j] and p[j]<1]
            pos=[[j,p[j]] for j in block if not baseline[j] and p[j]>0]
            assert sum(v for j,v in neg)==sum(v for j,v in pos)
            i=j=0
            while i<len(neg) and j<len(pos):
                take=min(neg[i][1],pos[j][1]);atom=list(baseline)
                atom[neg[i][0]]=0;atom[pos[j][0]]=1
                law.append((tuple(F(v) for v in atom),take))
                neg[i][1]-=take;pos[j][1]-=take
                if not neg[i][1]:i+=1
                if not pos[j][1]:j+=1
        law=compress(law,counter)
    else:
        lower=[floor(v/g) for v in p];ranges={};cuts={F(0),F(1)}
        for block in blocks:
            cumulative=F(0)
            for j in block:
                alpha=p[j]/g-lower[j];ranges[j]=(cumulative,cumulative+alpha)
                cuts.add(cumulative-floor(cumulative));cumulative+=alpha
                cuts.add(cumulative-floor(cumulative))
            assert cumulative.denominator==1
        cuts=sorted(cuts);law=[]
        for left,right in zip(cuts,cuts[1:]):
            u=(left+right)/2;atom=[]
            for j in range(n):
                a,b=ranges[j];up=floor(b-u)-floor(a-u);assert up in (0,1)
                atom.append(g*(lower[j]+up))
            law.append((tuple(atom),right-left))
        law=compress(law,counter)
        for h in range(J,0,-1):
            branches=[];step=F(1,2**h)
            for atom,weight in law:
                S=[j for j,v in enumerate(atom) if int(v*2**h)%2]
                if not S:branches.append((atom,weight));continue
                Sset=set(S);directions=[];mixed=[]
                for block in blocks:
                    active=[j for j in block if j in Sset];assert len(active)%2==0
                    groups=[[j for j in active if baseline[j]==b] for b in (0,1)]
                    for group in groups:
                        for i in range(0,len(group)-1,2):directions.append({group[i]:1,group[i+1]:-1})
                    if len(groups[0])%2:
                        assert len(groups[1])%2
                        mixed.append({groups[0][-1]:1,groups[1][-1]:-1})
                for i in range(0,len(mixed)-1,2):
                    d=dict(mixed[i]);d.update({j:-v for j,v in mixed[i+1].items()});directions.append(d)
                if len(mixed)%2:directions.append(mixed[-1])
                D=[[sum(row[j]*v for j,v in d.items()) for d in directions] for row in A]
                eta=moment_sign(D,len(S),counter)
                xi={j:sum(sign*d.get(j,0) for sign,d in zip(eta,directions)) for j in S}
                assert all(abs(v)==1 for v in xi.values())
                assert all(sum(xi.get(j,0) for j in block)==0 for block in blocks)
                assert abs(sum(defect[j]*v for j,v in xi.items()))<=2
                for orient in (-1,1):
                    new=list(atom)
                    for j,v in xi.items():new[j]+=orient*step*v
                    assert all(0<=v<=1 for v in new)
                    branches.append((tuple(new),weight/2))
            law=compress(branches,counter)
            assert sum(w for a,w in law)==1
            assert all(sum(w*a[j] for a,w in law)==p[j] for j in range(n))
            assert all(all(sum(a[j] for j in block)==target for block,target in zip(blocks,targets)) for a,w in law)
            assert all(sum(abs(v-b) for v,b in zip(a,baseline))<=mu+3 for a,w in law)
    maxerr=max(abs(sum(x*(z-v) for x,z,v in zip(row,a,p))) for row in A for a,w in law)
    r=(2*m-1).bit_length()
    assert all(sum(w*a[j] for a,w in law)==p[j] for j in range(n))
    assert all(all(sum(a[j] for j in block)==target for block,target in zip(blocks,targets)) for a,w in law)
    assert all(all(v in (0,1) for v in a) and w>0 for a,w in law)
    assert all(all(a[j]==p[j] for j in range(n) if p[j] in (0,1)) for a,w in law)
    assert len(law)<=n+1
    if mu<1:assert maxerr<=2+mu
    else:assert max(F(0),maxerr-1)**2<=400*r*mu
    return law,counter,str(maxerr)


def fixtures():
    start=time.monotonic();summaries=[]
    cases=[([F(1,3),F(2,3),F(1,7),F(6,7)],[[0,1],[2,3]]),
           ([F(1,2)]*8,[[0,1],[2,3],[4,5],[6,7]]),
           ([F(1,3),F(2,5),F(4,15),F(4,7),F(3,7),F(1),F(0)],[[0,1,2],[3,4],[5,6]]),
           ([F(1,3),F(2,3),F(2,5),F(3,5),F(1,7),F(6,7),F(3,8),F(5,8)],[[0,1],[2,3],[4,5],[6,7]]),
           ([F(1,20),F(19,20),F(1,30),F(29,30)],[[0,1],[2,3]]),
           ([F(1,13),F(2,13),F(3,13),F(4,13),F(3,13),F(3,7),F(4,7),F(1),F(0)],
            [list(range(5)),[5,6],[7,8]])]
    for p,blocks in cases:
        n=len(p);A=[[F(1 if (i*j+j*j+i)%3 else -1) for j in range(n)] for i in range(n)]
        law,counter,err=partition_law(A,p,blocks)
        summaries.append({'n':n,'blocks':len(blocks),'support':len(law),'error':err,**counter})
    count=0;values=[F(0),F(1,5),F(1,3),F(1,2),F(2,3),F(4,5),F(1)]
    A=[[F((-1)**((i+1)*j+j*j)) for j in range(6)] for i in range(6)]
    for v in product(values,repeat=3):
        p=[x for a in v for x in (a,1-a)]
        partition_law(A,p,[[0,1],[2,3],[4,5]]);count+=1
    return {'status':'exact_partition_fixture_checks_passed','rational_pair_laws':count,'fixtures':summaries,'elapsed_seconds':time.monotonic()-start,
            'scope':'Finite exact partition-base checks, not a general-matroid test or priority certificate.'}

if __name__=='__main__':
    report=fixtures();print(json.dumps(report,indent=2))
    with open('work/scouts/rounding_partition_compiler_checks.json','w') as f:json.dump(report,f,indent=2)
