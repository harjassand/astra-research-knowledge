#!/usr/bin/env python3
"""Synthetic ordinary-forward source for large sparse routing experiments.

Batch multinomials are simulation shortcuts. Every represented transition
and row/block lookup is charged as a logical ordinary generative query.
Only public labels/tasks/counts cross the learner interface, never neighbors,
true groups, transition probabilities or a useful basis.
"""
import numpy as np


class RoutingSource:
    def __init__(self,n=1024,seed=7281,degree=16):
        if n%4 or degree%2:raise ValueError('fixture dimensions')
        self.n=n;self.generators=2;self.rng=np.random.default_rng(seed)
        order=self.rng.permutation(n);self._groups=[list(map(int,x)) for x in np.split(order,4)]
        self._which=np.zeros(n,dtype=np.int64)
        for g,part in enumerate(self._groups):self._which[part]=g
        # Cycle and transposition do not commute: macro order matters too.
        self._actions=((1,2,3,0),(2,1,0,3));self._adj=[]
        for a in range(2):
            adj=[[] for _ in range(n)]
            for part in self._groups:
                k=len(part)
                for _ in range(degree//2):
                    p=self.rng.permutation(k);inverse=np.argsort(p)
                    for i,node in enumerate(part):adj[node].extend((part[int(p[i])],part[int(inverse[i])]))
            self._adj.append(adj)
        self._global=[list(map(int,self.rng.permutation(n))) for _ in range(2)]
        self._reset=[list(map(int,self.rng.choice(n,n//2,replace=False))) for _ in range(2)]
        self._tau=.02;self._noise=.00001;self._degree=degree;self.ledger=[]

    def public_task(self):
        b=[int(self._which[i]==1) for i in range(self.n)]
        # Return exact integer weights and their denominator, not hidden groups.
        ell_numer=[int(self._which[i]==0) for i in range(self.n)]
        return b,ell_numer,self.n//4

    def _uniform_destinations(self,dest,N,out):
        if not N:return
        if N<3*len(dest):
            indices=self.rng.integers(len(dest),size=N);keys,vals=np.unique(indices,return_counts=True)
            for k,v in zip(keys,vals):
                j=dest[int(k)];out[j]=out.get(j,0)+int(v)
        else:
            vals=self.rng.multinomial(N,np.full(len(dest),1/len(dest)))
            for j,v in zip(dest,vals):
                if v:out[j]=out.get(j,0)+int(v)

    def _row_counts(self,a,i,N):
        if not N:return {}
        branch=self.rng.multinomial(N,[1-self._tau-2*self._noise,self._tau,self._noise,self._noise])
        out={};self._uniform_destinations(self._adj[a][i],int(branch[0]),out)
        g=self._actions[a][int(self._which[i])]
        self._uniform_destinations(self._groups[g],int(branch[1]),out)
        if branch[2]:
            j=self._global[a][i];out[j]=out.get(j,0)+int(branch[2])
        self._uniform_destinations(self._reset[a],int(branch[3]),out)
        assert sum(out.values())==N
        return out

    def uniform_batch(self,a,N,label):
        sizes=self.rng.multinomial(N,np.full(self.n,1/self.n));rows=[];columns=[0]*self.n
        for i,ni in enumerate(sizes):
            row=self._row_counts(a,i,int(ni));rows.append(sorted(row.items()))
            for j,v in row.items():columns[j]+=v
        self.ledger.append({'phase':label,'generator':a,'logical_forward_calls':int(N),
                            'observed_nonzero_counts':sum(map(len,rows)),
                            'selection':'uniform named source row before each true transition'})
        return rows,columns

    def row_block_batch(self,a,N,which,r,label):
        """Synthetic compression of N ordinary transitions per named row."""
        # Computing mock probabilities is confined to this source adapter.
        hidden_to_observed=[np.bincount(np.asarray(which)[part],minlength=r)/len(part) for part in self._groups]
        reset=np.bincount(np.asarray(which)[self._reset[a]],minlength=r)/len(self._reset[a])
        out=[]
        for i in range(self.n):
            p=(1-self._tau-2*self._noise)*np.bincount([which[j] for j in self._adj[a][i]],minlength=r)/self._degree
            p=p+self._tau*hidden_to_observed[self._actions[a][int(self._which[i])]]+self._noise*reset
            p[which[self._global[a][i]]]+=self._noise
            out.append(list(map(int,self.rng.multinomial(N,p/p.sum()))))
        self.ledger.append({'phase':label,'generator':a,'logical_forward_calls':self.n*int(N),
                            'observed_block_count_entries':self.n*r,
                            'selection':'fixed N ordinary transitions per named row; public block-label lookup'})
        return out

    def pooled_batch(self,a,part,N,label,which=None,r=None):
        """Synthetic marginal of uniform-within-public-block row sampling."""
        p=np.zeros(self.n);weight=1/len(part)
        sourcegroups=np.zeros(4)
        for i in part:
            for j in self._adj[a][i]:p[j]+=weight*(1-self._tau-2*self._noise)/self._degree
            p[self._global[a][i]]+=weight*self._noise
            sourcegroups[self._actions[a][int(self._which[i])]]+=weight
        for g,mass in enumerate(sourcegroups):p[self._groups[g]]+=mass*self._tau/len(self._groups[g])
        p[self._reset[a]]+=self._noise/len(self._reset[a])
        if which is not None:p=np.bincount(which,weights=p,minlength=r)
        counts=list(map(int,self.rng.multinomial(N,p/p.sum())))
        self.ledger.append({'phase':label,'generator':a,'logical_forward_calls':int(N),
                            'observed_count_entries':len(counts),
                            'selection':'uniform row in a public acquired block, then true forward transition'})
        return counts

    def apply_truth(self,a,x):
        """Evaluation only; never available to the acquisition functions."""
        x=np.asarray(x,dtype=float);means=[float(np.mean(x[g])) for g in self._groups]
        reset=float(np.mean(x[self._reset[a]]));out=np.empty(self.n)
        for i in range(self.n):
            out[i]=(1-self._tau-2*self._noise)*sum(x[j] for j in self._adj[a][i])/self._degree
            out[i]+=self._tau*means[self._actions[a][int(self._which[i])]]
            out[i]+=self._noise*x[self._global[a][i]]+self._noise*reset
        return out


def acquire_partition(rows_by_generator,b,ell_numer):
    """Ordinary threshold-community proposal; no hidden partition argument."""
    n=len(b);tables=[dict(row) for row in rows_by_generator[0]]
    if len(rows_by_generator)>1:
        for rows in rows_by_generator[1:]:
            for i,row in enumerate(rows):
                for j,v in row:tables[i][j]=tables[i].get(j,0)+v
    edges=[]
    for i,row in enumerate(tables):
        for j,v in row.items():
            if j>=i or (b[i],ell_numer[i])!=(b[j],ell_numer[j]):continue
            weight=min(v,tables[j].get(i,0))
            if weight>0:edges.append((weight,i,j))
    values=sorted({e[0] for e in edges})
    if len(values)<2:raise ValueError('no acquired threshold gap')
    low,threshold=max(zip(values,values[1:]),key=lambda pair:(pair[1]+1)/(pair[0]+1))
    parent=list(range(n))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for weight,i,j in edges:
        if weight>=threshold:
            u,v=find(i),find(j)
            if u!=v:parent[max(u,v)]=min(u,v)
    parts={}
    for i in range(n):parts.setdefault(find(i),[]).append(i)
    parts=sorted(parts.values());which=[0]*n
    for g,part in enumerate(parts):
        for i in part:which[i]=g
    return parts,which,{'edge_count':len(edges),'observed_threshold_gap':[low,threshold],
                        'candidate_rank':len(parts),'block_sizes':list(map(len,parts)),
                        'scope':'Data-only proposal; correctness comes from later certificates, not this clustering heuristic.'}
