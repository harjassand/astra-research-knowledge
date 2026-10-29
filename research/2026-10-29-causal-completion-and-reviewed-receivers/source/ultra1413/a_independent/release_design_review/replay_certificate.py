"""Independent exact same-input release certificate intake; no optimization.

Only stdlib/Fraction; reads producer SOURCE/CERTIFICATE/INTEGER_RELEASE and
writes only this review directory. No producer function imports, conic/LP
solver, state/reference queries, random draw or new model case. The all-size
proof is challenged analytically in REVIEW; this checks the exact operational
receiver and its costs on the supplied single design.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import math
import platform
import resource
import time

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent.parent/'c_independent_opening'


def read_matrix(M):return [[F(x) for x in row] for row in M]
def transpose(A):return list(map(list,zip(*A)))
def multiply(A,B):
    cols=transpose(B)
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in cols] for row in A]
def inv(A):
    n=len(A)
    C=[row[:]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if C[i][j])
        C[j],C[pivot]=C[pivot],C[j]
        fac=C[j][j]
        C[j]=[x/fac for x in C[j]]
        for i in range(n):
            if i!=j:
                fac=C[i][j]
                C[i]=[x-fac*y for x,y in zip(C[i],C[j])]
    return [row[n:] for row in C]


def strictly_positive(A):
    """Successive exact symmetric Schur pivots, no spectral proposal."""
    assert A==transpose(A)
    B=[row[:] for row in A]
    pivots=[]
    for j in range(len(B)):
        pivot=B[j][j]
        assert pivot>0
        pivots.append(pivot)
        for i in range(j+1,len(B)):
            for k in range(i,len(B)):
                B[i][k]-=B[i][j]*B[j][k]/pivot
                B[k][i]=B[i][k]
    return min(pivots)


def main():
    start=time.perf_counter()
    raw={name:(SOURCE/name).read_bytes() for name in ('SOURCE.json','CERTIFICATE.json','INTEGER_RELEASE.json','RECEIVER.json')}
    src=json.loads(raw['SOURCE.json']);cert=json.loads(raw['CERTIFICATE.json'])
    tickets=json.loads(raw['INTEGER_RELEASE.json']);saved=json.loads(raw['RECEIVER.json'])
    L=read_matrix(src['reference_L']);C=read_matrix(src['cost_C'])
    K=read_matrix(cert['release_K']);a=[F(row[0]) for row in cert['center_a']]
    m,n=src['m'],src['n'];q,p=m-1,n-1
    c=F(src['budget']);t=1-c;kappa=F(src['entry_floor'])
    assert 0<c<1 and 0<kappa<F(1,m)
    assert all(x>0 for row in L for x in row)
    assert all(sum(col)==1 for col in transpose(L))
    assert all(sum(col)==1 for col in transpose(K))
    assert all(x>=kappa for row in K for x in row)
    assert all(abs(x)<=2 for x in a)
    R=inv(L)[:p]
    H=[];Hinv=[];h_pivots=[]
    for i in range(n):
        mean=[sum((R[h][y]*L[y][i] for y in range(n)),F(0)) for h in range(p)]
        assert mean==[F(h==i) for h in range(p)]
        hh=[[sum((L[y][i]*R[h][y]*R[j][y] for y in range(n)),F(0))-mean[h]*mean[j]
             for j in range(p)] for h in range(p)]
        h_pivots.append(strictly_positive(hh));H.append(hh);Hinv.append(inv(hh))
    D=[[K[h][j]-K[h][n-1] for j in range(p)] for h in range(q)]
    Dt=transpose(D)
    primal=[]
    for i in range(n):
        x=[K[h][i] for h in range(q)]
        S=multiply(multiply(D,H[i]),Dt)
        b=[[c*x[h]*F(h==j)-S[h][j]-c*x[h]*x[j]
             -(a[h]-t*x[h])*(a[j]-t*x[j])/t
             for j in range(q)] for h in range(q)]
        primal.append(strictly_positive(b))
    upper=sum((C[y][i]*K[y][i] for y in range(m) for i in range(n)),F(0))
    Y=[read_matrix(M) for M in cert['dual_Y']]
    assert len(Y)==n and all(len(M)==m+n and all(len(row)==m+n for row in M) for M in Y)
    dual_pivots=[strictly_positive(y) for y in Y]
    r=[row[:] for row in C];ba=[F(0)]*q;constant=F(0)
    alpha=q+p;beta=alpha+1
    for i,y in enumerate(Y):
        constant-=sum((y[q+h][q+j]*Hinv[i][j][h] for h in range(p) for j in range(p)),F(0))
        constant-=c*y[alpha][alpha]+t*y[beta][beta]
        for h in range(q):
            r[h][i]-=c*y[h][h]+2*c*y[h][alpha]-2*t*y[h][beta]
            ba[h]-=2*y[h][beta]
            for j in range(p):
                r[h][j]-=2*y[h][q+j]
                r[h][n-1]+=2*y[h][q+j]
    lower=constant-2*sum(abs(x) for x in ba)
    lower+=sum((kappa*sum(col)+(1-m*kappa)*min(col) for col in transpose(r)),F(0))
    assert [lower,upper]==[F(x) for x in cert['cost_interval_exact']]

    P=read_matrix(cert['ordinary_SAME_FLOOR_P'])
    rr=[F(row[0]) for row in cert['ordinary_SAME_FLOOR_r']]
    assert all(x>=0 for row in P for x in row)
    assert all(sum(col)==1 for col in transpose(P))
    assert min(rr)>=0 and sum(rr)==1
    PL=multiply(P,L)
    KO=[[c*PL[y][i]+t*rr[y] for i in range(n)] for y in range(m)]
    assert all(x>=kappa for row in KO for x in row)
    ordinary_upper=sum((C[y][i]*KO[y][i] for y in range(m) for i in range(n)),F(0))
    lam=read_matrix(cert['ordinary_SAME_FLOOR_dual'])
    assert all(x>=0 for row in lam for x in row)
    residual=[[C[y][i]-lam[y][i] for i in range(n)] for y in range(m)]
    losses=multiply(residual,transpose(L))
    ordinary_lower=kappa*sum(x for row in lam for x in row)
    ordinary_lower+=c*sum(min(col) for col in transpose(losses))+t*min(sum(row) for row in residual)
    assert [ordinary_lower,ordinary_upper]==[F(x) for x in cert['ordinary_SAME_FLOOR_family_interval']]
    relaxed=c*sum(min(col) for col in transpose(multiply(C,transpose(L))))+t*min(sum(row) for row in C)
    assert relaxed==F(cert['ordinary_sufficient_family_exact_optimum'])
    assert relaxed<upper<ordinary_lower

    endpoint_checks=0;table_rows=[]
    for i,column in enumerate(tickets['columns']):
        den=column['denominator'];counts=column['ticket_counts']
        assert len(counts)==m and sum(counts)==den and min(counts)>0
        assert all(F(counts[y],den)==K[y][i] for y in range(m))
        cum=[];cur=0
        for count in counts:cur+=count;cum.append(cur)
        assert cum==column['cumulative_ends']
        previous=0
        for y,count in enumerate(counts):
            # A disjoint half-open integer interval has exactly count tickets.
            assert previous<previous+count<=den
            for ticket in (previous,previous+count-1):
                output=next(j for j,end in enumerate(cum) if ticket<end)
                assert output==y;endpoint_checks+=1
            previous+=count
        bits=(den-1).bit_length()
        mean=F(bits*2**bits,den)
        assert bits==column['fresh_word_bits'] and mean==F(column['mean_fair_bits_exact'])
        assert mean<2*bits
        table_rows.append({'input':i,'denominator':str(den),'word_bits':bits,
                           'mean_fair_bits':str(mean),'word_acceptance':str(F(den,2**bits))})
    assert endpoint_checks==saved['integer_ticket_endpoint_checks']==2*m*n
    htrace=max(sum(h[i][i] for i in range(p)) for h in H)
    mu0=F(1,4)*min(c/F(m*m),t,1/htrace)
    rin=min(F(1,2),(F(1,m)-kappa)/(2*m),mu0/(8*(m+n)))
    assert rin>0
    assert all((SOURCE/name).read_bytes()==body for name,body in raw.items())
    result={'scope':'Independent exact SAME saved design/certificate/ticket replay, no solver/producer imports or added case.',
      'input_hashes':{name:hashlib.sha256(body).hexdigest() for name,body in raw.items()},
      'n':n,'m':m,'H_positive':len(h_pivots),'common_center_B_positive':len(primal),
      'lifted_dual_Y_positive':len(dual_pivots),'cost_interval_exact':[str(lower),str(upper)],
      'global_gap_exact':str(upper-lower),'ordinary_same_floor_interval':[str(ordinary_lower),str(ordinary_upper)],
      'ordinary_relaxed_exact':str(relaxed),'relaxed_family_beaten':False,
      'ticket_endpoint_checks':endpoint_checks,'ticket_rows':table_rows,
      'explicit_rational_Slater_mu0':str(mu0),'explicit_rational_inner_radius':str(rin),
      'minimum_H_schur_pivot':str(min(h_pivots)),
      'minimum_primal_B_schur_pivot':str(min(primal)),
      'minimum_dual_Y_schur_pivot':str(min(dual_pivots)),
      'seconds_after_stdlib_imports':time.perf_counter()-start,
      'ru_maxrss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'ru_maxrss_platform':platform.system(),
      'new_random_samples':0,'new_reference_queries':0,'new_solver_calls':0,
      'producer_source_unchanged_during_replay':True}
    (HERE/'EXACT_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('n','m','H_positive','common_center_B_positive',
       'lifted_dual_Y_positive','ticket_endpoint_checks','seconds_after_stdlib_imports',
       'new_solver_calls','producer_source_unchanged_during_replay')},indent=2))


if __name__=='__main__':main()
