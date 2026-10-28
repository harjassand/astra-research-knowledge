"""Exact rational reconstruction of the 60-feature multiplied support."""
from fractions import Fraction as F
import json,time
from pathlib import Path
from multiplier_support import compile_map

def ldl(Q):
    n=len(Q);L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        d=Q[j][j]-sum(L[j][k]**2*D[k] for k in range(j));assert d>0,(j,d)
        D.append(d)
        for i in range(j+1,n):L[i][j]=(Q[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/d
    assert all(Q[i][j]==sum(L[i][k]*D[k]*L[j][k] for k in range(n)) for i in range(n) for j in range(n))
    return D

def main():
    start=time.monotonic();_,_,terms,monoms,P,multipliers,z=compile_map()
    source=json.loads(Path('multiplier_support_search.json').read_text());n=len(z)
    theta=[F(round(c*10000),10000) for c in source['selector']]
    Q=[[F(round(c*1_000_000),1_000_000) for c in row] for row in source['gram']]
    groups={e:[] for e in monoms}
    for i,j,p in terms:
        [(e,c)]=p.terms();assert c==1;groups[e].append((i,j,1 if i==j else 2))
    target={e:F(int(c.p),int(c.q)) for e,c in P.terms()}
    for t,p in zip(theta,multipliers):
        for e,c in p.terms():target[e]=target.get(e,F(0))-t*F(int(c.p),int(c.q))
    for e,group in groups.items():
        residual=target.get(e,F(0))-sum(w*Q[i][j] for i,j,w in group)
        change=residual/sum(w for i,j,w in group)
        for i,j,w in group:Q[i][j]=Q[j][i]=Q[i][j]+change
    assert all(sum(w*Q[i][j] for i,j,w in group)==target.get(e,F(0)) for e,group in groups.items())
    rho=F(1,200);D=ldl([[Q[i][j]-(rho if i==j else 0) for j in range(n)] for i in range(n)])
    out={'status':'EXACT_GLOBAL_POLYCONVEX_SUPPORT_WITH_NORM_MULTIPLIER',
         'coefficient_vector':['1','1','113/10','-83/10','0','0','4','-4','0'],
         'tau':'113/10','alpha':str(theta[0]),'delta':str(theta[1]),
         'multiplier':'sum_j X_j^2','feature_order':'40 A_i X_j X_k (i then j<=k),20 X_i X_j X_k (i<=j<=k)',
         'gram_margin':str(rho),'gram':[[str(c) for c in row] for row in Q],
         'shifted_LDL_pivots':[str(c) for c in D],'exact_polynomial_equations':len(groups),
         'strict_QC_gap':str(rho/6),'background_quadratic_coefficient':str(rho/2),
         'wall_seconds':time.monotonic()-start,
         'max_pivot_bits':max(max(abs(d.numerator).bit_length(),d.denominator.bit_length()) for d in D),
         'method':'Ordinary SOS multiplier, then exact rational coefficient projection and LDL'}
    Path('EXACT_MULTIPLIER_SUPPORT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['gram','shifted_LDL_pivots']},indent=2))

if __name__=='__main__':main()
