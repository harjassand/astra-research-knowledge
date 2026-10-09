from itertools import product
import random


def partmat(n, labels):
    blocks=[[] for _ in range(max(labels)+1)]
    for e,b in enumerate(labels): blocks[b].append(e)
    def indep(S):
        return all(sum((e in S) for e in B)<=1 for B in blocks)
    return indep


def feasible_masks(mats,n):
    out=[]
    for mask in range(1<<n):
        S={i for i in range(n) if mask>>i&1}
        if all(M(S) for M in mats): out.append(mask)
    return out


def sumw(mask,weights):
    return sum(weights[i] for i in range(len(weights)) if mask>>i&1)


def best_sub(feas, support, weights):
    best=0; bestv=0
    for mask in feas:
        if mask & ~support: continue
        v=sumw(mask,weights)
        if v>bestv or (v==bestv and mask<best): best,bestv=mask,v
    return best,bestv


def greedy_mask(M, weights, support):
    picked=set()
    for e in sorted((i for i in range(len(weights)) if support>>i&1 and weights[i]>0),key=lambda i:(-weights[i],i)):
        if M(picked|{e}): picked.add(e)
    return sum(1<<i for i in picked)


def ratio(mats, weights, p=0.5):
    n=len(weights); feas=feasible_masks(mats,n)
    optv=max(sumw(x,weights) for x in feas)
    expected=0.0
    for P in range(1<<n):
        prob=p**P.bit_count()*(1-p)**(n-P.bit_count())
        if prob==0: continue
        a=[0]*n
        for e in range(n):
            bit=1<<e
            if P&bit: continue
            best,_=best_sub(feas,P|bit,weights)
            if best&bit: a[e]=weights[e]
        supports=sum(1<<e for e,x in enumerate(a) if x>0)
        gs=[greedy_mask(M,a,supports) for M in mats]
        B=gs[0]
        for g in gs[1:]: B &=g
        expected += prob*sumw(B,a)
    return expected/optv if optv else 1.0


def random_partition(n,rng):
    num_blocks=rng.randint(max(2,n//3),n)
    labels=[rng.randrange(num_blocks) for _ in range(n)]
    # compact labels
    remap={x:i for i,x in enumerate(sorted(set(labels)))}
    return [remap[x] for x in labels]


def main():
    rng=random.Random(20261009)
    for k in (2,3,4,5,6,8):
        best=(1.0,None)
        for trial in range(30):
            n=10
            mats=[partmat(n,random_partition(n,rng)) for _ in range(k)]
            weights=rng.sample(range(1,1000),n)
            r=ratio(mats,weights,0.5)
            if r<best[0]: best=(r,weights)
        print(f'k={k} n=10 trials=30 min_ratio={best[0]:.6f} weights={best[1]}')

if __name__=='__main__': main()
