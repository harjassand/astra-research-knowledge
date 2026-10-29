"""Standalone stdlib exact receiver and integer-only randomized release.

Reads only SOURCE.json/CERTIFICATE.json. No producer import, SDP, eigenvalue
proposal, symbolic package or reference-state model is required to qualify
the returned mechanism. Private fair-word sampling is an explicit interface;
the default run checks the integer law without obtaining any random samples.
"""
from bisect import bisect_right
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import resource
import time

ROOT=Path(__file__).resolve().parent


def zeros(r,c):return [[F(0) for _ in range(c)] for _ in range(r)]
def parse(M):return [[F(x) for x in row] for row in M]
def trans(A):return list(map(list,zip(*A)))
def mm(A,B):
    BT=trans(B)
    return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in BT] for row in A]
def sub(A,B):return [[a-b for a,b in zip(x,y)] for x,y in zip(A,B)]


def inverse(A):
    n=len(A)
    aug=[row[:]+[F(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next(k for k in range(j,n) if aug[k][j])
        aug[j],aug[k]=aug[k],aug[j]
        d=aug[j][j];aug[j]=[x/d for x in aug[j]]
        for i in range(n):
            if i!=j:
                d=aug[i][j];aug[i]=[x-d*y for x,y in zip(aug[i],aug[j])]
    return [row[n:] for row in aug]


def positive(A):
    n=len(A)
    assert A==trans(A)
    ll=zeros(n,n);diag=[]
    for j in range(n):
        d=A[j][j]-sum((ll[j][k]**2*diag[k] for k in range(j)),F(0))
        assert d>0
        diag.append(d);ll[j][j]=F(1)
        for i in range(j+1,n):
            ll[i][j]=(A[i][j]-sum((ll[i][k]*ll[j][k]*diag[k] for k in range(j)),F(0)))/d
    return min(diag)


def trace(A,B):
    return sum((A[i][j]*B[j][i] for i in range(len(A)) for j in range(len(A))),F(0))


def literal_blocks(K,aa,Hinv,c):
    """Directly materialize (10), also off the stochastic affine subspace."""
    m,n=len(K),len(K[0]);q,p=m-1,n-1;t=1-c
    blocks=[]
    for i in range(n):
        block=zeros(m+n,m+n)
        for h in range(q):
            x=K[h][i]
            block[h][h]=c*x
            for j in range(p):
                d=K[h][j]-K[h][n-1]
                block[h][q+j]=block[q+j][h]=d
            block[h][q+p]=block[q+p][h]=c*x
            block[h][q+p+1]=block[q+p+1][h]=aa[h]-t*x
        for h in range(p):
            for j in range(p):block[q+h][q+j]=Hinv[i][h][j]
        block[q+p][q+p]=c;block[q+p+1][q+p+1]=t
        blocks.append(block)
    return blocks


class IntegerRelease:
    def __init__(self,K):
        self.n=len(K[0]);self.m=len(K);self.columns=[]
        for i in range(self.n):
            den=math.lcm(*(K[y][i].denominator for y in range(self.m)))
            counts=[int(K[y][i]*den) for y in range(self.m)]
            assert all(x>0 for x in counts) and sum(counts)==den
            ends=[];total=0
            for count in counts:total+=count;ends.append(total)
            self.columns.append((den,counts,ends))

    def ticket(self,symbol,ticket):
        den,counts,ends=self.columns[symbol]
        assert 0<=ticket<den
        return bisect_right(ends,ticket)

    def draw(self,symbol,fair_word):
        """fair_word(k) must return fresh private uniform k-bit words."""
        den,_,_=self.columns[symbol]
        bits=(den-1).bit_length()
        while True:
            u=fair_word(bits)
            assert isinstance(u,int) and 0<=u<2**bits
            if u<den:return self.ticket(symbol,u)


def main():
    start=time.perf_counter()
    source_bytes=(ROOT/'SOURCE.json').read_bytes()
    cert_bytes=(ROOT/'CERTIFICATE.json').read_bytes()
    source=json.loads(source_bytes);cert=json.loads(cert_bytes)
    L=parse(source['reference_L']);C=parse(source['cost_C'])
    K=parse(cert['release_K']);aa=[row[0] for row in parse(cert['center_a'])]
    n,m=source['n'],source['m'];p,q=n-1,m-1
    c,kappa=F(source['budget']),F(source['entry_floor'])
    assert len(L)==n and all(len(row)==n for row in L)
    assert len(K)==m and all(len(row)==n for row in K)
    assert all(sum(col)==1 for col in trans(L)) and all(x>0 for row in L for x in row)
    assert all(sum(col)==1 for col in trans(K)) and all(x>=kappa for row in K for x in row)
    assert all(abs(x)<=2 for x in aa)
    R=inverse(L)[:p]
    H=[];Hi=[]
    for i in range(n):
        hh=[[sum((L[y][i]*R[a][y]*R[b][y] for y in range(n)),F(0))
             -F(int(a==i and b==i)) for b in range(p)] for a in range(p)]
        positive(hh);H.append(hh);Hi.append(inverse(hh))
    # Entire lifted primal, rather than importing the producer's Schur checker.
    blocks=literal_blocks(K,aa,Hi,c)
    primal_pivots=[positive(b) for b in blocks]
    upper=sum((C[y][i]*K[y][i] for y in range(m) for i in range(n)),F(0))
    Y=[parse(z) for z in cert['dual_Y']]
    assert len(Y)==n
    dual_pivots=[positive(y) for y in Y]
    zeroK=zeros(m,n);zeroA=[F(0)]*q
    base=literal_blocks(zeroK,zeroA,Hi,c)
    constant=-sum((trace(y,b) for y,b in zip(Y,base)),F(0))
    rc=zeros(m,n);ba=[]
    # Exact affine finite differences of the literal full matrix construction.
    # This does not reuse the producer's residual-coefficient formula.
    for y in range(m):
        for i in range(n):
            basis=zeros(m,n);basis[y][i]=F(1)
            delta=[sub(b,b0) for b,b0 in zip(literal_blocks(basis,zeroA,Hi,c),base)]
            rc[y][i]=C[y][i]-sum((trace(yy,b) for yy,b in zip(Y,delta)),F(0))
    for h in range(q):
        basis=[F(int(j==h)) for j in range(q)]
        delta=[sub(b,b0) for b,b0 in zip(literal_blocks(zeroK,basis,Hi,c),base)]
        ba.append(-sum((trace(yy,b) for yy,b in zip(Y,delta)),F(0)))
    lower=constant-2*sum(abs(x) for x in ba)
    for col in trans(rc):lower+=kappa*sum(col)+(1-m*kappa)*min(col)
    assert [lower,upper]==[F(x) for x in cert['cost_interval_exact']]

    # Reconstruct the full same-floor ordinary positive-replacer comparator.
    P=parse(cert['ordinary_SAME_FLOOR_P']);rr=parse(cert['ordinary_SAME_FLOOR_r'])
    assert all(x>=0 for row in P for x in row) and all(sum(z)==1 for z in trans(P))
    assert all(row[0]>=0 for row in rr) and sum(row[0] for row in rr)==1
    PL=mm(P,L)
    KO=[[c*PL[y][i]+(1-c)*rr[y][0] for i in range(n)] for y in range(m)]
    assert all(x>=kappa for row in KO for x in row)
    ordinary_upper=sum((C[y][i]*KO[y][i] for y in range(m) for i in range(n)),F(0))
    lam=parse(cert['ordinary_SAME_FLOOR_dual'])
    assert all(x>=0 for row in lam for x in row)
    cc=sub(C,lam);post=mm(cc,trans(L))
    ordinary_lower=kappa*sum(x for row in lam for x in row)
    ordinary_lower+=c*sum(min(col) for col in trans(post))
    ordinary_lower+=(1-c)*min(sum(row) for row in cc)
    assert [ordinary_lower,ordinary_upper]==[F(x) for x in cert['ordinary_SAME_FLOOR_family_interval']]
    relaxed=c*sum(min(col) for col in trans(mm(C,trans(L))))+(1-c)*min(sum(row) for row in C)
    assert relaxed==F(cert['ordinary_sufficient_family_exact_optimum'])
    assert upper<ordinary_lower and relaxed<upper

    release=IntegerRelease(K)
    boundary_checks=0;catalogue=[]
    for i,(den,counts,ends) in enumerate(release.columns):
        previous=0
        for y,count in enumerate(counts):
            assert release.ticket(i,previous)==y
            assert release.ticket(i,previous+count-1)==y
            boundary_checks+=2;previous+=count
        bits=(den-1).bit_length()
        catalogue.append({'input':i,'denominator':den,'ticket_counts':counts,
                          'cumulative_ends':ends,'fresh_word_bits':bits,
                          'mean_fair_bits_exact':str(F(bits*2**bits,den))})
    (ROOT/'INTEGER_RELEASE.json').write_text(json.dumps({'columns':catalogue,
        'contract':'fresh private ideal fair bits; no actual random samples acquired',
        'law':'exact rational K, proved by disjoint integer ticket multiplicities'},indent=2)+'\n')
    out={'status':'PASS_STANDALONE_EXACT_GLOBAL_DESIGN_AND_INTEGER_LAW',
         'source_sha256':hashlib.sha256(source_bytes).hexdigest(),
         'certificate_sha256':hashlib.sha256(cert_bytes).hexdigest(),
         'input_alphabet':n,'output_alphabet':m,'budget':str(c),
         'complete_primal_PSD_blocks':len(primal_pivots),'lifted_block_order':m+n,
         'complete_dual_PSD_blocks':len(dual_pivots),
         'global_optimum_interval_display':[float(lower),float(upper)],
         'certified_gap_display':float(upper-lower),
         'ordinary_same_floor_interval_display':[float(ordinary_lower),float(ordinary_upper)],
         'ordinary_relaxed_cost_display':float(relaxed),
         'ordinary_relaxed_beaten':False,'same_floor_sufficient_family_beaten':True,
         'integer_ticket_endpoint_checks':boundary_checks,
         'maximum_integer_word_bits':max(z['fresh_word_bits'] for z in catalogue),
         'maximum_mean_fair_bits':float(max(F(z['mean_fair_bits_exact']) for z in catalogue)),
         'new_random_samples_or_reference_queries':0,
         'seconds_after_stdlib_imports':time.perf_counter()-start,
         'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'imports_producer_or_solver_or_symbolic_library':False}
    (ROOT/'RECEIVER.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
