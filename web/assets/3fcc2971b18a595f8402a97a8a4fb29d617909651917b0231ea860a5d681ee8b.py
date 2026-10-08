"""Exact Spin(13), d=64 full-star highest-weight extractor.

The resulting star blocks are exact. Support vertices in this file are *not*
claimed to be canonical-EB attainable; the script computes swap-resolved
isotypic blocks and an all-positive-dual outer-bound diagnostic separately.
It never forms a dense 262144-by-262144 star matrix.
"""
import sympy as sp
from itertools import combinations
from math import comb
import json
from pathlib import Path
import time

I=sp.I; NQ=6; DIM=1<<NQ; FULL=DIM**3
START=time.perf_counter()

def pmul(a,b):
    phase=0; out=[]
    tab={('I','I'):(0,'I'),('I','X'):(0,'X'),('I','Y'):(0,'Y'),('I','Z'):(0,'Z'),
    ('X','I'):(0,'X'),('Y','I'):(0,'Y'),('Z','I'):(0,'Z'),('X','X'):(0,'I'),('Y','Y'):(0,'I'),('Z','Z'):(0,'I'),
    ('X','Y'):(1,'Z'),('Y','X'):(3,'Z'),('Y','Z'):(1,'X'),('Z','Y'):(3,'X'),('Z','X'):(1,'Y'),('X','Z'):(3,'Y')}
    for x,y in zip(a,b):
        p,z=tab[x,y]; phase=(phase+p)%4; out.append(z)
    return phase,tuple(out)

def gamma_words():
    out=[]
    for k in range(NQ):
        pre=('Z',)*k; suf=('I',)*(NQ-k-1)
        out.extend((pre+('X',)+suf,pre+('Y',)+suf))
    out.append(('Z',)*NQ)
    return out
GAM=gamma_words()

def e_basis(k):
    for A in combinations(range(2*NQ+1),k):
        ph=0; w=('I',)*NQ
        for a in A:
            p,w=pmul(w,GAM[a]); ph=(ph+p)%4
        ph=(ph+k*(k-1)//2)%4
        yield A,ph,w

def apply_word(w,bits):
    out=bits; phase=0
    for q,p in enumerate(w):
        bit=(bits>>q)&1
        if p=='X': out ^= 1<<q
        elif p=='Y': out ^= 1<<q; phase += 1 if bit==0 else 3
        elif p=='Z' and bit: phase += 2
    return out,phase%4

def triple_apply(term,idx):
    coeff,words=term; out=idx; phase=(0 if coeff==1 else 2)
    for f,(flip,phases) in enumerate(words):
        b=(idx>>(NQ*f))&(DIM-1)
        phase+=phases[b]
        out ^= flip << (NQ*f)
    phase%=4
    if phase not in (0,2): raise AssertionError(('nonreal star action',term,idx,phase))
    return out,(1 if phase==0 else -1)

def h_terms():
    out={k:[] for k in range(1,NQ+1)}
    for k in out:
        for A,ph,w in e_basis(k):
            pt=(ph+2*(w.count('Y')%2))%4
            c=I**(pt+ph)
            c=sp.simplify(c)
            if c not in (1,-1): raise AssertionError(('bad transpose coefficient',A,c))
            c=int(c)
            out[k].append((c,(w,w,('I',)*NQ)))
            out[k].append((c,(w,('I',)*NQ,w)))
    return out
HT=h_terms()

def encode_word(w):
    flip=0; yz=0; ny=0
    for q,p in enumerate(w):
        if p in ('X','Y'): flip |= 1<<q
        if p in ('Y','Z'): yz |= 1<<q
        if p=='Y': ny += 1
    phases=tuple((ny+2*(yz & bits).bit_count())%4 for bits in range(DIM))
    return flip,phases

HT={k:[(c,tuple(encode_word(w) for w in words)) for c,words in terms]
    for k,terms in HT.items()}

def c_action(q,bits,create=True):
    bit=(bits>>q)&1
    if create and bit: return None
    if not create and not bit: return None
    sign=(-1)**sum((bits>>j)&1 for j in range(q))
    return bits^(1<<q),sign

def simple_action(alpha,bits,dual=False):
    if alpha==NQ-1:
        bit=(bits>>(NQ-1))&1
        if not dual: return None if bit else (bits^(1<<(NQ-1)),1)
        return None if not bit else (bits^(1<<(NQ-1)),-1)
    i=alpha
    if not dual:
        a=c_action(i+1,bits,False)
        if a is None:return None
        b=c_action(i,a[0],True)
        if b is None:return None
        return b[0],a[1]*b[1]
    if ((bits>>i)&1)==0 or ((bits>>(i+1))&1)==1:return None
    src=bits^(1<<i)^(1<<(i+1))
    fwd=simple_action(alpha,src,False)
    assert fwd is not None and fwd[0]==bits
    return src,-fwd[1]

def weight2(idx):
    ans=[]
    for q in range(NQ):
        br=(idx>>(NQ*0+q))&1; b1=(idx>>(NQ+q))&1; b2=(idx>>(2*NQ+q))&1
        ans.append((1-2*br)+(2*b1-1)+(2*b2-1))
    return tuple(ans)

def target(r): return tuple(3 if i<r else 1 for i in range(NQ))

def make_highest(r):
    wt=target(r); states=[x for x in range(FULL) if weight2(x)==wt]
    rows=[]
    for a in range(NQ):
        destwt=list(wt)
        if a<NQ-1: destwt[a]+=2; destwt[a+1]-=2
        else: destwt[a]+=2
        destwt=tuple(destwt)
        dest=[x for x in range(FULL) if weight2(x)==destwt]
        dpos={x:i for i,x in enumerate(dest)}
        M=sp.zeros(len(dest),len(states))
        for col,x in enumerate(states):
            for f in range(3):
                b=(x>>(NQ*f))&(DIM-1)
                ans=simple_action(a,b,dual=(f==0))
                if ans is not None:
                    y,p=ans; z=(x&~((DIM-1)<<(NQ*f))) | (y<<(NQ*f))
                    if z in dpos: M[dpos[z],col]+=p
        rows.append(M)
    stacked=sp.Matrix.vstack(*rows)
    ker=stacked.nullspace()
    return states,sp.Matrix.hstack(*ker),stacked

def act_h(k,states,vec):
    out={}
    for col,x in enumerate(states):
        cv=vec[col]
        if cv==0: continue
        for term in HT[k]:
            y,p=triple_apply(term,x)
            out[y]=out.get(y,0)+cv*p
    return {x:sp.simplify(v) for x,v in out.items() if sp.simplify(v)!=0}

def act_swap(states,vec):
    out={}
    for col,x in enumerate(states):
        cv=vec[col]
        if cv==0: continue
        y=(x&((DIM-1)))|(((x>>(2*NQ))&(DIM-1))<<NQ)|(((x>>NQ)&(DIM-1))<<(2*NQ))
        out[y]=out.get(y,0)+cv
    return out

def pivot_rows(N):
    piv=[]
    for rr in range(N.rows):
        if N[piv+[rr],:].rank()>len(piv): piv.append(rr)
        if len(piv)==N.cols: break
    if len(piv)!=N.cols: raise AssertionError('failed pivot rows')
    return piv

def coeff_matrix(states,N,act):
    piv=pivot_rows(N); Pinv=N[piv,:].inv(); pos={x:i for i,x in enumerate(states)}
    A=sp.zeros(N.cols,N.cols)
    for j in range(N.cols):
        out=act([N[i,j] for i in range(N.rows)])
        for x,v in out.items():
            if x not in pos: raise AssertionError(('outside HW states',x,v))
        vals=sp.Matrix([out.get(states[i],0) for i in piv])
        A[:,j]=Pinv*vals
        if N*A[:,j] != sp.Matrix([out.get(x,0) for x in states]):
            raise AssertionError(('invariant subspace failure',j))
    return A

def restrict_subspace(A,T):
    piv=pivot_rows(T)
    return T[piv,:].inv()*(A*T)[piv,:]

def gram_psd_minors(M):
    out=[]
    for sz in range(1,M.rows+1):
        for inds in combinations(range(M.rows),sz):
            det=sp.factor(M.extract(inds,inds).det())
            out.append((inds,det))
    return out

def irreducible_dim(r): return DIM*(comb(2*NQ+1,r)-comb(2*NQ+1,r-1) if r else 1)

def main():
    blocks={}; grams={}; swap_dims={}; dims=[]
    for r in range(NQ+1):
        t0=time.perf_counter()
        states,N,_=make_highest(r); expected=NQ+1-r
        if N.cols!=expected: raise AssertionError(('HW multiplicity',r,len(states),N.cols,expected))
        print(f'r={r} source_states={len(states)} kernel={N.cols} highest_seconds={time.perf_counter()-t0:.3f} elapsed={time.perf_counter()-START:.3f}',flush=True)
        H=[]
        for k in range(1,NQ+1):
            tk=time.perf_counter()
            H.append(coeff_matrix(states,N,lambda v,k=k:act_h(k,states,v)))
            print(f'  r={r} grade={k} words={comb(2*NQ+1,k)} seconds={time.perf_counter()-tk:.3f} elapsed={time.perf_counter()-START:.3f}',flush=True)
        S=coeff_matrix(states,N,lambda v:act_swap(states,v)); G=N.T*N
        if S*S!=sp.eye(N.cols): raise AssertionError(('swap involution',r,S))
        dim=irreducible_dim(r); dims.append(dim)
        for eps in (1,-1):
            vv=(S-eps*sp.eye(N.cols)).nullspace()
            if not vv: continue
            T=sp.Matrix.hstack(*vv); At=[restrict_subspace(a,T) for a in H]; Gt=T.T*G*T
            # Hermiticity is expressed in the exact Gram form.
            Bs=[sp.simplify(Gt*a) for a in At]
            if any(B!=B.T for B in Bs): raise AssertionError(('non-Hermitian Gram block',r,eps,Bs))
            blocks[(r,eps)]=Bs; grams[(r,eps)]=Gt; swap_dims[(r,eps)]=T.cols
        print(f'r={r} dim(T_r)={dim} m={expected} swap(+/-)=({swap_dims.get((r,1),0)}/{swap_dims.get((r,-1),0)})',flush=True)
        for eps in (1,-1):
            if (r,eps) in blocks: print(' ',eps,'H gram blocks=',blocks[(r,eps)],'G=',grams[(r,eps)],flush=True)
    total=sum((NQ+1-r)*dims[r] for r in range(NQ+1))
    if total!=FULL: raise AssertionError(('dimension sum',total,FULL))
    swap_total={eps:sum(dims[r]*swap_dims.get((r,eps),0) for r in range(NQ+1)) for eps in (1,-1)}
    if sum(swap_total.values())!=FULL: raise AssertionError(('swap dimension total',swap_total))
    # Rigorous pure-state outer support: s1<=1 by Clifford-vector anticommutation;
    # s2<=6 by SO(13) skew-normal form and ||(sigma_i)||_1<=sqrt(6)||(sigma_i)||_2;
    # s3,...,s6<=63 by Parseval. All moments are nonnegative and sum to 63.
    # Vertices of this capped-simplex outer polytope are listed below; not claimed attainable.
    support_vertices=[]
    for j in range(2,6):
        for rem,pre in ((63,[]),(62,[(0,1)]),(57,[(1,6)]),(56,[(0,1),(1,6)])):
            v=[0]*6
            for i,x in pre:v[i]=x
            v[j]=rem; support_vertices.append(v)
    trace=[comb(13,k) for k in range(1,7)]
    data={'status':'EXTRACTION_PASS','scope':'Spin(13) d=64 exact full ordinary-tensor star; no pure-orbit support asserted',
          'normalization':'tau=Tr/64; T_A=i^(k(k-1)/2) Gamma_A, grades k=0..6',
          'highest_weight_coordinates':'lambda_r=(3/2 repeated r, 1/2 repeated 6-r), r=0..6',
          'irreducible_dimensions':dims,'multiplicities':[NQ+1-r for r in range(NQ+1)],
          'swap_multiplicities':{f'{r},{eps:+d}':n for (r,eps),n in swap_dims.items()},
          'swap_sector_dimensions':{str(eps):swap_total[eps] for eps in (1,-1)},'full_dimension':total,
          'full_triple_dimension_charged':FULL,'elapsed_seconds':round(time.perf_counter()-START,3),
          'trace_coefficients':trace,'pure_moment_outer_vertices_not_claimed_attainable':support_vertices,
          'blocks':{f'{r},{eps:+d}':{'gram':[[str(grams[(r,eps)][i,j]) for j in range(grams[(r,eps)].cols)] for i in range(grams[(r,eps)].rows)],
                    'bilinear_H':[ [[str(B[i,j]) for j in range(B.cols)] for i in range(B.rows)] for B in mats]}
                    for (r,eps),mats in blocks.items()}}
    Path(__file__).with_name('spin13_fullstar_blocks.json').write_text(json.dumps(data,indent=2)+'\n')
    print('TOTAL',total,'swap',swap_total,'trace',trace,flush=True)
    print('CERTIFICATE EXTRACTION PASS elapsed_seconds',round(time.perf_counter()-START,3),flush=True)

if __name__=='__main__':main()
