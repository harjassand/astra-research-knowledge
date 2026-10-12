"""Exact-integer checks of weighted basis-peeling parity-cut sensitivity."""
import random

def independent_add(basis,v):
    while v:
        k=v.bit_length()-1
        if k in basis: v^=basis[k]
        else:
            basis[k]=v
            return True
    return False

def peel(vectors,weights):
    remaining=set(range(len(vectors)))
    rounds=[None]*len(vectors)
    k=0
    while remaining:
        k+=1; basis={}; selected=[]
        for i in sorted(remaining,key=lambda i:(-weights[i],i)):
            if independent_add(basis,vectors[i]): selected.append(i)
        assert selected
        for i in selected: rounds[i]=k;remaining.remove(i)
    return rounds

def main():
    rng=random.Random(310512)
    checked=0
    for D in range(1,8):
        for trial in range(25):
            m=60
            vectors=[rng.randrange(1,1<<D) for _ in range(m)]
            weights=[rng.randrange(1,8)*(1<<rng.randrange(40)) for _ in range(m)]
            rounds=peel(vectors,weights)
            for ell in range(1,1<<D):
                cut=sum(w for v,w in zip(vectors,weights) if (ell&v).bit_count()%2)
                for v,w,k in zip(vectors,weights,rounds):
                    if (ell&v).bit_count()%2:
                        assert cut>=k*w
                        checked+=1
    print(f'weighted maximum-basis peeling: {checked} exact active-cut sensitivity inequalities passed')

if __name__=='__main__': main()
