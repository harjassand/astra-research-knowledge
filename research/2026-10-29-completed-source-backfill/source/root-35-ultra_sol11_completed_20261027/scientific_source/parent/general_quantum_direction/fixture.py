from fractions import Fraction as Q
from pathlib import Path
import json,time
OUT=Path(__file__).resolve().parent
def zero(n):return [[Q(0) for _ in range(n)] for _ in range(n)]
def mm(a,b):return [[sum((x*y for x,y in zip(row,col)),Q(0)) for col in zip(*b)] for row in a]
def ceilq(x):return (x.numerator+x.denominator-1)//x.denominator
def ceil2(x):
    n=0
    while Q(2)**n<x:n+=1
    return n
def ldl(a):
    n=len(a);l=zero(n);p=[]
    for i in range(n):
        t=a[i][i]-sum((l[i][j]**2*p[j] for j in range(i)),Q(0));assert t>0;p.append(t)
        for j in range(i+1,n):l[j][i]=(a[j][i]-sum((l[j][k]*l[i][k]*p[k] for k in range(i)),Q(0)))/t
    return min(p)
def main():
    start=time.perf_counter();h=zero(9);pomega=zero(9)
    for i in range(9):h[i][i]=Q(1,9)
    for b,d in enumerate([1,-1,0]):h[b][3+b]=h[3+b][b]=Q(d,36)
    for i in range(3):
        for j in range(3):pomega[3*i+i][3*j+j]=1
    assert sum(h[i][i] for i in range(9))==1
    reduced=[[sum((h[3*i+b][3*j+b] for b in range(3)),Q(0)) for j in range(3)] for i in range(3)]
    assert reduced==[[Q(i==j,3) for j in range(3)] for i in range(3)]
    # Prove a strict convenient PD floor (actual smallest eigenvalue is1/12).
    shifted=[[h[i][j]-(Q(1,13) if i==j else 0) for j in range(9)] for i in range(9)]
    pivot=ldl(shifted)
    ph=mm(pomega,h);ell=1-sum(ph[i][i] for i in range(9))/3;assert ell==Q(8,9)
    L,K=ceil2(24/ell),ceil2(Q(4));k=2*L+ceilq(4*K/ell)+1;assert (L,K,k)==(5,2,20)
    epsilon=Q(1,2**k);x=[[pomega[i][j]+epsilon*h[i][j] for j in range(9)] for i in range(9)]
    off=[[x[b][3+c] for c in range(3)] for b in range(3)];squared=mm(off,off)
    expected=[[epsilon**2*Q(1,1296) if i==j and i<2 else Q(0) for j in range(3)] for i in range(3)]
    assert squared==expected and any(v for row in squared for v in row)
    trace=3+epsilon;rawbound=epsilon*ell/3;normalized=rawbound/trace;assert normalized==Q(8,84934683)
    out={'status':'EXACT_GENERAL_DIRECTION_FIXTURE_PASSED','r':1,'m':'1','kappa':'1','H_trace':'1','H_PD_floor':'1/13','shifted_LDL_min_pivot':str(pivot),'leakage':str(ell),'L':L,'K':K,'k':k,'epsilon':str(epsilon),'Delta_lower_raw':str(rawbound),'CMI_excess_lower':str(normalized),'CMI_excess_lower_display':float(normalized),'offdiagonal_block_square':[[str(v) for v in row] for row in squared],'square_nonzero':True,'seconds':time.perf_counter()-start,'scope':'Exact synthetic source and finite theorem receiver; no certified dense entropy evaluation, physical instrument, unrestricted inequality or novelty claim.'}
    (OUT/'FIXTURE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
