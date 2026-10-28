"""Convert a candidate numerical SOS support into an exact certificate."""
from fractions import Fraction as F
import hashlib,json,time
from pathlib import Path
from poly_support import build

def ldl(matrix):
    n=len(matrix);L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        d=matrix[j][j]-sum(L[j][k]**2*D[k] for k in range(j))
        if d<=0:raise ValueError(('nonpositive exact pivot',j,str(d)))
        D.append(d)
        for i in range(j+1,n):
            L[i][j]=(matrix[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/d
    assert all(sum(L[i][k]*D[k]*L[j][k] for k in range(n))==matrix[i][j]
               for i in range(n) for j in range(n))
    return L,D

def main():
    start=time.monotonic()
    M,b,terms,monoms,P,lambdas,z=build()
    source=json.loads(Path('poly_support_search.json').read_text());n=len(z)
    theta=[F(round(c*10000),10000) for c in source['alpha_delta']]
    alpha,delta=theta
    Q=[[F(round(c*1_000_000),1_000_000) for c in row] for row in source['gram']]
    grouped={e:[] for e in monoms}
    for i,j,polynomial in terms:
        [(e,c)]=polynomial.terms();assert c==1
        grouped[e].append((i,j,1 if i==j else 2))
    target={e:F(int(c.p),int(c.q)) for e,c in P.terms()}
    for t,polynomial in zip(theta,lambdas):
        for e,c in polynomial.terms():target[e]=target.get(e,F(0))-t*F(int(c.p),int(c.q))
    for e,group in grouped.items():
        residual=target.get(e,F(0))-sum(w*Q[i][j] for i,j,w in group)
        change=residual/sum(w for i,j,w in group)
        for i,j,w in group:Q[i][j]=Q[j][i]=Q[i][j]+change
    assert all(sum(w*Q[i][j] for i,j,w in group)==target.get(e,F(0)) for e,group in grouped.items())
    rho=F(1,200)
    shifted=[[Q[i][j]-(rho if i==j else 0) for j in range(n)] for i in range(n)]
    L,D=ldl(shifted)
    record={
        'status':'EXACT_GLOBAL_SOS_POLYCONVEX_SUPPORT',
        'input_nine_vector':['1','1','16','-13','0','0','4','-4','0'],
        'feature_order':'16 A_i X_j row-major, then10 X_i X_j lex i<=j',
        'matrix_entry_order':['a','b','c','d'],
        'lambda':'alpha*(u-v)+delta*q',
        'alpha':str(alpha),'delta':str(delta),'gram_margin':str(rho),
        'gram':[[str(c) for c in row] for row in Q],
        'shifted_LDL_pivots':[str(c) for c in D],
        'polynomial_constraints':len(monoms),'exact_zero_residual':True,
        'numerical_search_sha256':hashlib.sha256(Path('poly_support_search.json').read_bytes()).hexdigest(),
        'QC_gap_constant':str(rho/2),
        'physical_capability':'NOT_CLAIMED',
        'novelty':'UNKNOWN; SOS polyconvexity is established prior machinery',
        'wall_seconds':time.monotonic()-start,
    }
    Path('EXACT_POLYCONVEX_SUPPORT.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ['gram','shifted_LDL_pivots']},indent=2))
    print('positive_pivots',len(D),'max_pivot_bits',max(max(abs(v.numerator).bit_length(),v.denominator.bit_length()) for v in D))

if __name__=='__main__':main()
