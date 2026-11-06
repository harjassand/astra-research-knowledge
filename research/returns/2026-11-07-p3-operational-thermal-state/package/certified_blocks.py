"""Exact-input all-sector compiler and certified dyadic thermal purifications.

The Newton/Schur representation is reused from the obtained collective-
thermodynamics result. Here its rational Dicke representation is executed,
followed by gap-free shifted, rounded scaling/squaring. No eigensolver or
physical Gibbs oracle is used in the certificate. NumPy object matmul performs
exact Python-integer arithmetic; the only floats returned are display values.
"""
from fractions import Fraction as Q
from decimal import Decimal as D, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from math import comb, factorial, isqrt, prod
from itertools import product
import numpy as np

ZERO=(Q(0),Q(0)); ONE=(Q(1),Q(0))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def conj(a): return (a[0],-a[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,c): return (a[0]*c,a[1]*c)
def nz(a): return bool(a[0] or a[1])

def sparse_add(dest,src,c=Q(1)):
    for ij,v in src.items():
        w=add(dest.get(ij,ZERO),scale(v,c))
        if nz(w): dest[ij]=w
        elif ij in dest: del dest[ij]

def sparse_mul(A,B):
    rows={}
    for (i,j),v in B.items(): rows.setdefault(i,[]).append((j,v))
    C={}
    for (i,k),v in A.items():
        for j,w in rows.get(k,[]):
            ij=(i,j); z=add(C.get(ij,ZERO),mul(v,w))
            if nz(z): C[ij]=z
            elif ij in C: del C[ij]
    return C

def matrix_polynomial_mul(P,R):
    C={}
    for a,A in P.items():
        for b,B in R.items():
            c=tuple(x+y for x,y in zip(a,b))
            sparse_add(C.setdefault(c,{}),sparse_mul(A,B))
    return C

def rational_block(N,L,coeffs):
    """Return H in unnormalized Dicke basis and its exact diagonal Gram G."""
    assert N>=max(map(sum,coeffs),default=0) and L%2==N%2 and 0<=L<=N
    K=max(map(sum,coeffs),default=0); I={(i,i):ONE for i in range(L+1)}
    Sx={}; Sy={}; Sz={}
    for k in range(L+1):
        Sz[k,k]=(Q(L,2)-k,Q(0))
        if k:
            Sx[k-1,k]=(Q(L-k+1,2),Q(0)); Sy[k-1,k]=(Q(0),-Q(L-k+1,2))
        if k<L:
            Sx[k+1,k]=(Q(k+1,2),Q(0)); Sy[k+1,k]=(Q(0),Q(k+1,2))
    S=[Sx,Sy,Sz]; powers=[None]
    for j in range(1,K+1):
        r=j//2; p={}
        for a in product(range(r+1),repeat=3):
            if sum(a)!=r: continue
            c=Q(factorial(r),prod(factorial(x) for x in a))
            alpha=tuple(2*x for x in a)
            if j%2==0:
                p[alpha]={ij:scale(v,N*c) for ij,v in I.items()}
            else:
                for t in range(3):
                    b=list(alpha); b[t]+=1; b=tuple(b)
                    sparse_add(p.setdefault(b,{}),S[t],2*c)
        powers.append(p)
    E=[{(0,0,0):I}]
    for k in range(1,K+1):
        out={}
        for j in range(1,k+1):
            C=matrix_polynomial_mul(E[k-j],powers[j])
            for a,A in C.items(): sparse_add(out.setdefault(a,{}),A,Q(1 if j%2 else -1,k))
        E.append(out)
    H={}
    for a,c in coeffs.items():
        k=sum(a)
        if not k: sparse_add(H,I,N*c); continue
        count=Q(factorial(N),factorial(N-k))
        for t in a: count/=factorial(t)
        sparse_add(H,E[k].get(a,{}),N*c/count)
    G=[Q(comb(L,k)) for k in range(L+1)]
    for (i,j),v in H.items():
        assert scale(v,G[i])==conj(scale(H.get((j,i),ZERO),G[j]))
    return H,G

def multiplicity(N,L):
    if L<0 or L>N or (N-L)%2: return 0
    k=(N-L)//2
    return comb(N,k)-(comb(N,k-1) if k else 0)

def compress(H,G,keep):
    ix={k:i for i,k in enumerate(keep)}
    return {(ix[i],ix[j]):v for (i,j),v in H.items() if i in ix and j in ix},[G[i] for i in keep]

def positive_definite(H,G,x):
    """Exact Sylvester/LDL test of G(H-xI), exploiting sparse band fill."""
    d=len(G); A={}
    for (i,j),v in H.items():
        if i<=j: A[i,j]=scale(v,G[i])
    for i in range(d): A[i,i]=add(A.get((i,i),ZERO),(-x*G[i],Q(0)))
    for k in range(d):
        p=A.get((k,k),ZERO); assert p[1]==0
        if p[0]<=0: return False
        row=[(j,A[k,j]) for j in range(k+1,d) if (k,j) in A and nz(A[k,j])]
        for t,(i,u) in enumerate(row):
            for j,v in row[t:]:
                z=add(A.get((i,j),ZERO),neg(scale(mul(conj(u),v),1/p[0])))
                if nz(z): A[i,j]=z
                elif (i,j) in A: del A[i,j]
    return True

def lowest_interval(H,G,bound,beta):
    lo=-bound-1; hi=bound+1; calls=0
    while hi-lo>Q(1,2)/beta:
        mid=(lo+hi)/2; calls+=1
        if positive_definite(H,G,mid): lo=mid
        else: hi=mid
    return lo,hi,calls

def sqrt_bounds(x,bits):
    assert x>=0; S=1<<bits
    k=isqrt((x.numerator*S*S)//x.denominator)
    lo=Q(k,S)
    return lo,lo if lo*lo==x else Q(k+1,S)

def round_q(x,S):
    y=x*S
    return (2*y.numerator+y.denominator)//(2*y.denominator)

def orthonormal_dyadic(H,G,bits):
    d=len(G); S=1<<bits
    re=np.zeros((d,d),dtype=object); im=np.zeros((d,d),dtype=object)
    radii=[[Q(0) for _ in range(d)] for _ in range(d)]
    for (i,j),v in H.items():
        if i>j: continue
        extra=max(abs(v[0].numerator).bit_length(),abs(v[1].numerator).bit_length())+8
        sl,sh=sqrt_bounds(G[i]/G[j],bits+extra)
        rad=Q(0)
        for part,mat in zip(v,(re,im)):
            lo,hi=sorted([part*sl,part*sh]); n=round_q((lo+hi)/2,S)
            mat[i,j]=n
            mat[j,i]=n if mat is re else -n
            rad+=max(abs(Q(n,S)-lo),abs(Q(n,S)-hi))
        if i==j: assert im[i,i]==0
        radii[i][j]=rad; radii[j][i]=rad
    delta=max(map(sum,radii),default=Q(0))
    return re,im,delta

def rounded_div(A,den):
    return np.frompyfunc(lambda x:(2*x+den)//(2*den),1,1)(A)

def cmul(A,B):
    ar,ai=A; br,bi=B
    if not np.any(ai) and not np.any(bi): return ar@br,np.zeros_like(ar)
    return ar@br-ai@bi,ar@bi+ai@br

def exponential_purification(H,G,bound,beta,bits=144,terms=64):
    """A dyadic matrix approximating exp[-beta(Htilde-aI)/2].
    Htilde differs from exact orthonormal H by <= delta_H in operator norm.
    A error E follows only from exact rounding and a Taylor remainder bound.
    """
    d=len(G); S=1<<bits
    lo,hi,calls=lowest_interval(H,G,bound,beta)
    hr,hi_im,delta=orthonormal_dyadic(H,G,bits)
    a=lo-delta
    assert hi+delta-a<=1/beta
    B=beta*(bound+delta+abs(a))/2; s=0
    while B>1: B/=2; s+=1
    xr=np.empty((d,d),dtype=object); xi=np.empty_like(xr)
    for i in range(d):
        for j in range(d):
            value=Q(hr[i,j],S)-(a if i==j else 0)
            xr[i,j]=round_q(beta*value/(1<<(s+1)),S)
            xi[i,j]=round_q(beta*Q(hi_im[i,j],S)/(1<<(s+1)),S)
    r=Q(d,S); delta_x=r
    assert delta_x<=Q(1,2)
    tail=Q(8*(1<<(terms+1)),factorial(terms+1))
    E=(1<<(2*s))*(2*delta_x+(8*terms+1)*r+tail)
    assert E<Q(1,100),"Increase bits/terms; fixed precision refused."
    identity=np.eye(d,dtype=object)*S
    T=(identity,np.zeros_like(identity)); A=(identity.copy(),np.zeros_like(identity))
    X=(-xr,-xi)
    for k in range(1,terms+1):
        raw=cmul(T,X); T=tuple(rounded_div(v,S*k) for v in raw)
        A=(A[0]+T[0],A[1]+T[1])
    for _ in range(s): A=tuple(rounded_div(v,S) for v in cmul(A,A))
    Tmid=Q(sum(int(x)*int(x) for mat in A for x in mat.flat),S*S)
    Trad=d*E*(2+E)
    Tl=max(Q(0),Tmid-Trad); Th=Tmid+Trad
    assert Tl>0
    return {'A_re':A[0],'A_im':A[1],'bits':bits,'d':d,'a':a,'T_lo':Tl,'T_hi':Th,
            'delta_H':delta,'A_operator_error':E,'purification_trace_error':4*d*E,
            'squarings':s,'Taylor_terms':terms,'PD_calls':calls,
            'minimum_lo':lo,'minimum_hi':hi}

NEAR=Context(prec=90,rounding=ROUND_HALF_EVEN)
DOWN=Context(prec=90,rounding=ROUND_FLOOR)
UP=Context(prec=90,rounding=ROUND_CEILING)
def decimal_bounds(x):
    return DOWN.divide(D(x.numerator),D(x.denominator)),UP.divide(D(x.numerator),D(x.denominator))
def exp_bounds(x,cutoff=10000):
    x=Q(x)
    if x<=-cutoff: return Q(0),Q(1,1<<cutoff)
    assert x<=0
    lo,hi=decimal_bounds(x)
    return Q(NEAR.next_minus(NEAR.exp(lo))),Q(NEAR.next_plus(NEAR.exp(hi)))
def log_bounds(x):
    lo,hi=decimal_bounds(Q(x)); assert lo>0
    return Q(NEAR.next_minus(NEAR.ln(lo))),Q(NEAR.next_plus(NEAR.ln(hi)))

def sector_distribution(blocks,beta,random_bits=96):
    shift=min(b['a'] for b in blocks); wlo=[]; whi=[]
    cutoff=max(b['N'] for b in blocks)+random_bits+32
    for b in blocks:
        el,eh=exp_bounds(-beta*(b['a']-shift),cutoff)
        wlo.append(b['multiplicity']*el*b['T_lo'])
        whi.append(b['multiplicity']*eh*b['T_hi'])
    Wl=sum(wlo); Wh=sum(whi); assert Wl>0
    mids=[(x+y)/2 for x,y in zip(wlo,whi)]; Wm=sum(mids)
    S=1<<random_bits; cumulative=Q(0); old=0; counts=[]
    for mid in mids:
        cumulative+=mid/Wm; new=(cumulative.numerator*S)//cumulative.denominator
        counts.append(new-old); old=new
    assert sum(counts)==S and min(counts)>=0
    tv=Q(0)
    for b,wl,wh,c in zip(blocks,wlo,whi,counts):
        ql=wl/Wh; qh=wh/Wl; qt=Q(c,S)
        tv+=max(abs(qt-ql),abs(qt-qh))/2
        b['probability_count']=c; b['probability_bits']=random_bits
        b['q_lo']=ql; b['q_hi']=qh
    logWlo=log_bounds(Wl)[0]; logWhi=log_bounds(Wh)[1]
    return {'sector_TV_bound':tv,'free_energy_lo':shift-logWhi/beta,
            'free_energy_hi':shift-logWlo/beta,'random_bits':random_bits,
            'delta_H':max(b['delta_H'] for b in blocks),
            'purification_trace_error':max(b['purification_trace_error'] for b in blocks)}

def compile_blocks(N,coeffs,beta,window=(-1,1),bits=144,terms=64,progress=None):
    coeffs={tuple(a):Q(c) for a,c in coeffs.items()}; beta=Q(beta)
    wl,wh=map(Q,window); assert beta>0 and -1<=wl<=wh<=1
    normbound=N*sum(abs(c) for c in coeffs.values()); blocks=[]
    for L in range(N%2,N+1,2):
        keep=[k for k in range(L+1) if wl<=Q(L-2*k,N)<=wh]
        if not keep: continue
        H,G=rational_block(N,L,coeffs); H,G=compress(H,G,keep)
        b=exponential_purification(H,G,normbound,beta,bits,terms)
        b.update(N=N,L=L,keep=keep,multiplicity=multiplicity(N,L))
        blocks.append(b)
        if progress: progress(L)
    if not blocks: raise ValueError('The supplied hard window contains no finite-N eigenvalue.')
    cert=sector_distribution(blocks,beta)
    cert.update(N=N,beta=str(beta),window=[str(wl),str(wh)],norm_bound=normbound,
                blocks=len(blocks),stored_entries=sum(b['d']**2 for b in blocks))
    return blocks,cert

def float_A(b):
    return (np.array(b['A_re'],dtype=float)+1j*np.array(b['A_im'],dtype=float))/(2.0**b['bits'])

def serializable(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,np.ndarray): return [[str(int(v)) for v in row] for row in x]
    if isinstance(x,dict): return {k:serializable(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serializable(v) for v in x]
    if isinstance(x,np.integer): return int(x)
    return x
