"""Exact rational simultaneous consumer: no private_source import or access."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from math import isqrt
import json,time

ROOT=Path(__file__).resolve().parent

def sqrt_up(x,scale=2**48):
    x=F(x); v=(x.numerator*scale*scale+x.denominator-1)//x.denominator
    a=isqrt(v)
    if a*a<v: a+=1
    z=F(a,scale)
    assert z*z>=x
    return z

def solve(A,b):
    n=len(b)
    if not n:return []
    M=[list(map(F,A[i]))+[F(b[i])] for i in range(n)]
    for j in range(n):
        k=next((k for k in range(j,n) if M[k][j]),None)
        if k is None: raise ValueError('singular lower conductance: upper mean unavailable')
        M[j],M[k]=M[k],M[j]
        d=M[j][j];M[j]=[v/d for v in M[j]]
        for i in range(n):
            if i!=j:
                d=M[i][j]
                M[i]=[M[i][k]-d*M[j][k] for k in range(n+1)]
    return [row[-1] for row in M]

def laplacian(edges):
    n=len(edges)
    return [[sum(edges[i]) if i==j else -edges[i][j] for j in range(n)] for i in range(n)]

def tree_weights(P):
    n=len(P); out=[]
    for root in range(n):
        rest=[i for i in range(n) if i!=root]; total=F(0)
        for par in product(range(n),repeat=n-1):
            parents=dict(zip(rest,par)); ok=True
            for i in rest:
                seen=set(); j=i
                while j!=root:
                    if j in seen:ok=False;break
                    seen.add(j);j=parents[j]
                if not ok:break
            if ok:
                w=F(1)
                for i,j in parents.items():w*=P[i][j]
                total+=w
        out.append(total)
    return out

def stringify(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,list):return [stringify(y) for y in x]
    if isinstance(x,dict):return {k:stringify(v) for k,v in x.items()}
    return x

def consume(record):
    started=time.perf_counter()
    nports=record['port_count']; H=F(record['horizon']); ticks=record['tick_scale']
    assert nports==4 and H==24 and record['contracts']['port_holding_rate']=='1'
    assert record['contracts']['hidden_excursion_tail']=='Pr(sigma>t) <= exp(-t/2), every prepared port'
    allowance=F(record['contracts']['timestamp_absolute_allowance'])
    # e^3 > 20 by its degree-eight Taylor polynomial; hence e^-12<1/160000.
    exp3=sum(F(3**k,__import__('math').factorial(k)) for k in range(9))
    assert exp3>20
    tail=F(1,160000); logbudget=F(12); gamma=F(1,2)
    Plo=[];Phi=[];ulo=[];uhi=[];vlo=[];vhi=[]; observation_bounds=[]
    for row in record['rows']:
        n=row['n']; assert sum(row['endpoint_counts'])+row['pending_count']==n
        p_error=sqrt_up(logbudget/(2*n))
        lo=[max(F(0),F(c,n)-p_error) for c in row['endpoint_counts']]
        hi=[min(F(1),F(c,n)+p_error+tail) for c in row['endpoint_counts']]
        # All improvements preserve the true row simplex.
        for j in range(nports):
            lo[j]=max(lo[j],1-sum(hi[k] for k in range(nports) if k!=j))
            hi[j]=min(hi[j],1-sum(lo[k] for k in range(nports) if k!=j))
        Plo.append(lo);Phi.append(hi)
        first=F(int(row['sum_ticks']),n*ticks)
        second=F(int(row['sum_squared_ticks']),n*ticks*ticks)
        r1=sqrt_up(2*F(8)*logbudget/n)+2*H*logbudget/(3*n)+allowance
        r2=sqrt_up(2*F(384)*logbudget/n)+2*H*H*logbudget/(3*n)+2*H*allowance+allowance*allowance
        ulo.append(max(F(0),first-r1)); uhi.append(first+r1+tail/gamma)
        vlo.append(max(F(0),second-r2)); vhi.append(second+r2+2*tail*(H/gamma+1/(gamma*gamma)))
        observation_bounds.append({'endpoint_error':p_error,'first_error':r1,'second_error':r2,
            'first_truncated_mean':first,'second_truncated_mean':second})
    tlo=tree_weights(Plo);thi=tree_weights(Phi)
    assert min(tlo)>0
    slo=[tlo[i]/(tlo[i]+sum(thi[j] for j in range(nports) if j!=i)) for i in range(nports)]
    shi=[thi[i]/(thi[i]+sum(tlo[j] for j in range(nports) if j!=i)) for i in range(nports)]
    elo=[[F(0)]*nports for _ in range(nports)];ehi=[[F(0)]*nports for _ in range(nports)]
    for i,j in combinations(range(nports),2):
        l=max(slo[i]*Plo[i][j],slo[j]*Plo[j][i])
        u=min(shi[i]*Phi[i][j],shi[j]*Phi[j][i])
        assert 0<=l<=u
        elo[i][j]=elo[j][i]=l;ehi[i][j]=ehi[j][i]=u
    Slo=laplacian(elo);Shi=laplacian(ehi)
    blo=[slo[i]*(1+ulo[i]) for i in range(nports)]
    bhi=[shi[i]*(1+uhi[i]) for i in range(nports)]
    clo=sum(slo[i]*vlo[i] for i in range(nports))/2
    chi=sum(shi[i]*vhi[i] for i in range(nports))/2
    queries=[]
    for mask in range(1,1<<nports):
        A=[i for i in range(nports) if mask>>i&1];R=[i for i in range(nports) if i not in A]
        dl=sum(slo[i] for i in R)+sum(slo[i]*ulo[i] for i in range(nports))
        du=sum(shi[i] for i in R)+sum(shi[i]*uhi[i] for i in range(nports))
        lowmat=[[Shi[i][j] for j in R] for i in R]
        himat=[[Slo[i][j] for j in R] for i in R]
        vl=solve(lowmat,[blo[i] for i in R]);vu=solve(himat,[bhi[i] for i in R])
        tl=(clo+sum(blo[i]*vl[k] for k,i in enumerate(R)))/du
        tu=(chi+sum(bhi[i]*vu[k] for k,i in enumerate(R)))/dl
        assert 0<tl<=tu
        queries.append({'target_ports':A,'lower':tl,'upper':tu,'factor':tu/tl,
            'display':[float(tl),float(tu)],'factor_display':float(tu/tl)})
    out={'schema':'astra.native_boundary_mean_certificate.v1',
        'failure_probability_upper':F(48,160000),
        'all_nonempty_port_target_sets':True,'query_count':len(queries),
        'new_source_queries':0,'source_generator_reads':0,
        'input_contracts':record['contracts'],
        'observation_bounds':observation_bounds,
        'P_lower':Plo,'P_upper':Phi,'stationary_event_lower':slo,'stationary_event_upper':shi,
        'u_lower':ulo,'u_upper':uhi,'v_lower':vlo,'v_upper':vhi,
        'S_lower':Slo,'S_upper':Shi,'b_lower':blo,'b_upper':bhi,'c_lower':clo,'c_upper':chi,
        'queries':queries,'wall_seconds':time.perf_counter()-started,
        'max_factor_display':max(q['factor_display'] for q in queries),
        'comparison':'same complete record permits ordinary positive killed/Schur solve; no exclusive speed advantage',
    }
    return out

def main():
    record=json.loads((ROOT/'NATIVE_EXCURSION_RECORD.json').read_text())
    out=consume(record)
    (ROOT/'NATIVE_EXCURSION_CERTIFICATE.json').write_text(json.dumps(stringify(out),indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['query_count','max_factor_display','wall_seconds','new_source_queries','source_generator_reads']},indent=2))

if __name__=='__main__':main()
