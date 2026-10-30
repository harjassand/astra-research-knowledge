"""High-precision diagnostic; theorem must come from analytic bounds."""
import mpmath as mp,json
mp.mp.dps=100
C=[(0,72),(3,60),(5,36),(6,0)]
K=[2,1,1,1]; H=mp.log(2)/14
def f(r):
    if r<=20:return H
    if r>=30:return mp.mpf(0)
    t=(r-20)/10
    return H*(1-3*t*t+2*t*t*t)
def fall(n,k):
    if n<k:return mp.mpf(0)
    return mp.fprod(mp.mpf(n-i) for i in range(k))
def defect(A,B):
    a,b=mp.mpf(A),mp.mpf(B)
    Lb=mp.log(b+2);r=mp.log(a+2)/Lb;fr=f(r)
    incoming=[];out=[]
    for i,y in enumerate(C):
        z=C[(i+1)%4]; da=z[0]-y[0];db=z[1]-y[1]
        o=K[i]*fall(A,y[0])*fall(B,y[1]);out.append(o)
        if A<z[0] or B<z[1]:incoming.append(mp.mpf(0));continue
        rp=(mp.log(a+2)+mp.log1p(-mp.mpf(da)/(a+2)))/(Lb+mp.log1p(-mp.mpf(db)/(b+2)))
        df=-da*mp.log(2)-db*fr+(b-db)*(f(rp)-fr)
        incoming.append(K[i]*fall(A,z[0])*fall(B,z[1])*mp.exp(df))
    scale=max(out+[mp.mpf(1)])
    return float((sum(incoming)-sum(out))/scale)
rows=[]
for B in [100,1000,1000000]:
    for r in [1,4,8,12,19,20,21,25,29,30,31,36,40]:
        A=B**r
        rows.append({'B':B,'power_A_over_B':r,'normalized_defect':defect(A,B)})
for A,B in [(0,1000),(0,1000000),(1000,0),(1000000,0),(1,1000000),(1000000,1),(2,1000000),(1000000,2),(10**60,0),(10**60,1),(10**60,2),(0,10**20),(1,10**20)]:
    rows.append({'A':A,'B':B,'normalized_defect':defect(A,B)})
print(json.dumps({'precision_digits':mp.mp.dps,'tested':len(rows),'positive_count':sum(r['normalized_defect']>0 for r in rows),'rows':rows,'scope':'Numerical sign diagnostic, not a replacement for all-size proof or novelty review.'},indent=2))
