"""Exact rational reconstruction and modular rank certificates for family272.

U0,V0 are unnormalized integer sym/wedge embeddings. D^2=diag(1,2).
K_r=(V0^T(Q_p kron Q_q)U0)D^-1/sqrt(2), exactly.
"""
import json
from pathlib import Path
import numpy as np
from diagnostics import B,C,syms,weds,choi

def modular_elimination(a,p):
    a=[[int(x)%p for x in row] for row in a]
    rank=0; determinant=1; pivots=[]
    for col in range(len(a[0])):
        pivot=next((r for r in range(rank,len(a)) if a[r][col]),None)
        if pivot is None:continue
        if pivot!=rank:a[pivot],a[rank]=a[rank],a[pivot];determinant=-determinant
        val=a[rank][col];determinant=determinant*val%p;pivots.append(val)
        inv=pow(val,-1,p)
        a[rank]=[x*inv%p for x in a[rank]]
        for r in range(rank+1,len(a)):
            z=a[r][col]
            if z:a[r]=[(x-z*y)%p for x,y in zip(a[r],a[rank])]
        rank+=1
        if rank==len(a):break
    if rank<len(a):determinant=0
    return dict(rank=rank,determinant_mod_p=determinant%p,pivots=pivots)

def rational_model():
    q=B.astype(np.int64).astype(object).transpose(1,2,0)
    u=np.zeros((16,10),dtype=object);v=np.zeros((16,6),dtype=object)
    for a,(i,j) in enumerate(syms):
        u[4*i+j,a]=1;u[4*j+i,a]=1
    for a,(i,j) in enumerate(weds):v[4*i+j,a]=1;v[4*j+i,a]=-1
    ks=np.array([v.T@np.kron(x,y)@u for x in q for y in q],dtype=object)
    s=sum(np.kron(x,x) for x in ks)
    c0=C.astype(np.int64).astype(object)
    c=np.kron(c0,c0)
    d=np.diag([2 if i==j else 1 for i,j in syms]).astype(object)
    dd=np.kron(d,d)
    # M=s Ad_(2 D^-2) s* Ad_K s; ABA=(1/32) M Ad_D^-1.
    m=s@dd@s.T@c@s
    j=choi(m,10,6)
    assert all(isinstance(x,int) for x in j.flat)
    assert np.array_equal(j,j.T)
    assert np.array_equal(j.reshape(10,6,10,6),
                          j.reshape(10,6,10,6).transpose(0,3,2,1))
    return ks,s,m,j

def main():
    ks,s,m,j=rational_model()
    out={'arithmetic':'exact Python integers and prime-field elimination',
         'conclusion':'Choi(ABA) has rank 60 by invertible local congruence',
         'certificates':{str(p):modular_elimination(j,p) for p in (101,131,139)},
         'kraus_count':len(ks),
         'choi_integer_trace':str(np.trace(j)),
         'max_entry_bitlength':max(abs(int(x)).bit_length() for x in j.flat)}
    assert all(o['rank']==60 for o in out['certificates'].values())
    outpath=Path(__file__).with_name('exact_rank.json')
    outpath.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
