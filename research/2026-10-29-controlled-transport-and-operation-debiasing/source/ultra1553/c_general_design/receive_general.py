"""Stdlib exact receiver: SOURCE+CERTIFICATE only, no solver imports.

Rebuilds ALL symmetric and imaginary/skew coefficient identities, checks
the full Choi/R signs, and reconstructs a global utility lower bound.
The analytic same-source ordinary comparator is a separate exact route.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math,resource,time
from fisher_pencils import (decode,encode,zeros,source_coefficients,target_coefficients,
    phi,minus,linear_system,pack,upper_coords,quadratic_matrix,ldl_positive,
    matvec,trace_product,min_floor_columns)
ROOT=Path(__file__).resolve().parent


def shape(M,n,m):
    return len(M)==n and all(len(row)==m for row in M)


class IntegerRelease:
    """Private exact tickets, conditional on fresh independent fair words.

    randbits(b) must return an exact uniform integer on [0,2^b).
    No PRNG, shared randomness or device acquisition is silently supplied.
    """
    def __init__(self,catalogue):
        self.catalogue=catalogue

    def draw(self,i,randbits):
        row=self.catalogue[i];den=int(row['denominator'])
        end=list(map(int,row['endpoints']));bits=row['fair_bits_per_attempt']
        while True:
            ticket=randbits(bits)
            assert 0<=ticket<(1<<bits)
            if ticket<den:return next(y for y in range(len(end)-1) if ticket<end[y+1])


def bounds_root():
    """The unique real root r^3+r-1=0, exact rational isolation."""
    lo,hi=F(1,2),F(1)
    for _ in range(100):
        r=(lo+hi)/2
        if r**3+r-1<0:lo=r
        else:hi=r
    assert lo**3+lo-1<0<hi**3+hi-1
    return lo,hi


def interval_product(A,B):
    a=[x*y for x in A for y in B]
    return min(a),max(a)


def ordinary():
    tick=time.perf_counter();lo,hi=bounds_root()
    # Positive factors (1-r^2)(r-1/2)/r^2 /15.
    improvement=interval_product((1-hi**2,1-lo**2),(lo-F(1,2),hi-F(1,2)))
    improvement=(improvement[0]/(15*hi**2),improvement[1]/(15*lo**2))
    optimum=(F(1,4)-improvement[1],F(1,4)-improvement[0])
    tau=(F(2,15)*(1-hi**2)/hi**2,F(2,15)*(1-lo**2)/lo**2)
    # The full 0.001 entry floor is inactive at this exact optimizer.
    assert tau[0]*(1-hi)/2>F(1,1000) and 1-tau[1]>F(1,1000)
    return {'method':'binary functional calculus, symmetry and one cubic root; same L/raw input/floor/budget/cost',
        'root_polynomial':'r^3+r-1','root_interval':list(map(str,(lo,hi))),
        'utility_interval':list(map(str,optimum)),'tau_interval':list(map(str,tau)),
        'postprocess_L_best_cost':'1/4','entry_floor_inactive_exactly':True,
        'seconds':time.perf_counter()-tick}


def main():
    tick=time.perf_counter()
    source_path=ROOT/'SOURCE.json';cert_path=ROOT/'CERTIFICATE.json'
    s=json.loads(source_path.read_text());cert=json.loads(cert_path.read_text())
    L=decode(s['L']);cost=decode(s['cost']);c=F(s['budget']);kappa=F(s['entry_floor'])
    n,ell,m=s['n'],s['ell'],s['m'];f=m+1
    assert isinstance(n,int) and isinstance(ell,int) and isinstance(m,int)
    assert n>=2 and ell>=1 and m>=1 and 0<=kappa<F(1,m) and c>=0
    assert shape(L,ell,n) and shape(cost,m,n)
    coefficients=source_coefficients(L);e=len(coefficients[0][1]);d=e*f
    C,K,R=decode(cert['C']),decode(cert['K']),decode(cert['R'])
    assert shape(C,d,d) and shape(R,f,f) and shape(K,m,n)
    assert all(sum(K[y][i] for y in range(m))==1 for i in range(n))
    assert all(x>=kappa for row in K for x in row)
    target=target_coefficients(K,c);checks=[]
    for j,((tag,A),(_,B)) in enumerate(zip(coefficients,target)):
        P=phi(C,A,f)
        if j==0:P=[[v+R[p][q] for q,v in enumerate(row)] for p,row in enumerate(P)]
        assert P==B,(j,tag)
        checks.append({'coefficient':tag,'full_matrix_exact':True,'order':f})
    cp,cpiv=ldl_positive(C);rp,rpiv=ldl_positive(R)
    assert cp and rp
    upper=sum(cost[y][i]*K[y][i] for y in range(m) for i in range(n))
    assert upper==F(cert['global_upper'])
    _,Ar,br,_=linear_system(L,m);v=pack(C,K)
    assert matvec(Ar,v)==br
    nc=len(upper_coords(d));lam=list(map(F,cert['dual_lambda']));Y=decode(cert['dual_Y'])
    assert len(lam)==len(Ar) and shape(Y,f,f)
    yp,ypiv=ldl_positive(Y);assert yp
    gc=[sum(lam[h]*Ar[h][j] for h in range(len(Ar))) for j in range(nc)]
    A0=coefficients[0][1]
    # Build the exact derivative from the Choi convention, independently
    # of the producer's diagonal optimization of this same expression.
    for h,(u,w) in enumerate(upper_coords(d)):
        a,p=divmod(u,f);b,q=divmod(w,f)
        gc[h]+=A0[a][b]*Y[q][p]
        if u!=w:gc[h]+=A0[b][a]*Y[p][q]
    M=quadratic_matrix(gc,d);delta=F(cert['dual_C_shift'])
    assert delta>=0, 'trace upper bound cannot be used with a negative shift'
    for j in range(d):M[j][j]+=delta
    mp,mpiv=ldl_positive(M);assert mp
    WK=zeros(m,n)
    for y in range(m):
        for i in range(n):
            WK[y][i]=cost[y][i]+sum(lam[h]*Ar[h][nc+y*n+i] for h in range(len(Ar)))-Y[y][y]/n
    constant=-sum(lam[h]*br[h] for h in range(len(Ar)))-c*Y[-1][-1]
    traceC=(1+c)/min(A0[j][j] for j in range(e))
    assert traceC==F(cert['dual_trace_C_bound'])
    lower=constant+min_floor_columns(WK,kappa)-delta*traceC
    assert lower==F(cert['global_lower']) and lower<=upper
    rational_seconds=time.perf_counter()-tick

    # The exact qualifier above compiles arbitrary admitted dimensions;
    # this particular conventional closed form is ONLY for this source.
    assert (n,ell,m)==(2,3,3) and c==F(1,2) and kappa==F(1,1000)
    assert L==decode([['3/5','1/5'],['1/5','3/5'],['1/5','1/5']])
    assert cost==[[(y-F(i))**2/n for i in range(n)] for y in (F(0),F(1,2),F(1))]
    cmp=ordinary();ol,ou=map(F,cmp['utility_interval'])
    assert lower<=ou and ol<=upper
    # Exact integer-ticket realization of the returned channel. No draws.
    tickets=[];edgechecks=0
    for i in range(n):
        den=math.lcm(*(K[y][i].denominator for y in range(m)))
        endpoints=[0]
        for y in range(m):endpoints.append(endpoints[-1]+int(K[y][i]*den))
        assert endpoints[-1]==den and all(endpoints[j]<endpoints[j+1] for j in range(m))
        for y in range(m):
            assert F(endpoints[y+1]-endpoints[y],den)==K[y][i]
            for z in (endpoints[y],endpoints[y+1]-1):
                assert next(a for a in range(m) if z<endpoints[a+1])==y
                edgechecks+=1
        b=(den-1).bit_length();expected=F(b*(1<<b),den)
        tickets.append({'input':i,'denominator':str(den),'endpoints':list(map(str,endpoints)),
            'fair_bits_per_attempt':b,'expected_fair_bits':str(expected)})
    record={'status':'ACCEPTED_EXACT_FINITE_DESIGN_RECEIVER',
        'source_SHA256':hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'certificate_SHA256':hashlib.sha256(cert_path.read_bytes()).hexdigest(),
        'scope':'one-use conditional/subtracted comparison at all finite complex references; raw classical X supplied',
        'orders':{'source':e,'target':f,'Choi':d},'coefficient_checks':checks,
        'PD_checks':{'C':cpiv,'R':rpiv,'dual_Y':ypiv,'dual_shifted_C':mpiv},
        'cost_lower':str(lower),'cost_upper':str(upper),'cost_gap':str(upper-lower),
        'cost_decimal_diagnostic':[float(lower),float(upper)],
        'same_source_ordinary':cmp,'ticket_catalogue':tickets,'ticket_boundary_checks':edgechecks,
        'random_draws':0,'reference_queries':0,'solver_calls':0,
        'receiver_rational_seconds':rational_seconds,'seconds':time.perf_counter()-tick,
        'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/'RECEIVER.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'status':record['status'],'bounds':[float(lower),float(upper)],
        'ordinary_bounds':[float(ol),float(ou)],'seconds':record['seconds'],
        'ordinary_seconds':cmp['seconds'],'peak_RSS_bytes':record['peak_RSS_bytes']},indent=2))


if __name__=='__main__':main()
