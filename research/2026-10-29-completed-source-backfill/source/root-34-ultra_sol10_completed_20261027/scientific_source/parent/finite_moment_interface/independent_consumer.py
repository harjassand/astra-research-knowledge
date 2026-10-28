"""Root: literal symbolic coefficients, integer Bareiss positive-definiteness.
No producer imports or optimization solver; all22 rational certificates.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr
import math,json,time
import sympy as s
OUT=Path(__file__).resolve().parent;SRC=OUT.parents[1]/'explicit_convex_interface'
def e(ii):return tuple(ii.count(j) for j in range(4))
mom=[e(ii) for d in range(5) for ii in cwr(range(4),d)];feat=mom[:15];ix={v:i for i,v in enumerate(mom)}
def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def pd(mat):
    n=len(mat);assert all(len(r)==n for r in mat)
    assert all(mat[i][j]==mat[j][i] for i in range(n) for j in range(n))
    den=math.lcm(*(v.denominator for row in mat for v in row))
    a=[[v.numerator*(den//v.denominator) for v in row] for row in mat];prev=1
    for k in range(n-1):
        pivot=a[k][k];assert pivot>0
        for i in range(k+1,n):
            for j in range(k+1,n):
                val,rem=divmod(pivot*a[i][j]-a[i][k]*a[k][j],prev);assert rem==0;a[i][j]=val
        prev=pivot
    assert a[-1][-1]>0
a,b,c,d=s.symbols('a b c d');var=(a,b,c,d)
T=a*a+b*b+c*c+d*d;q=a*d-b*c;u=a*a+c*c;v=b*b+d*d;w=a*b+c*d
p=s.Rational(55220381,10**10)*(u*u+v*v)+s.Rational(114430029,625000000)*u*v-s.Rational(801761987,5000000000)*w*w+s.Rational(118849817,4000000000)*q*(u-v)
def coeff(p):return {e:F(int(z.p),int(z.q)) for e,z in s.Poly(p,*var).terms()}
fc,nc,tc,qc=map(coeff,[p,T*T,T,q])
def value(p,x):return sum(z*math.prod(t**i for t,i in zip(x,e)) for e,z in p.items())
start=time.monotonic();raw=json.loads((SRC/'MOMENT_EVALUATIONS.json').read_text());rows=[]
slices={F(r['s']):(F(r['value_lower']),F(r['value_upper'])) for r in json.loads((OUT/'SLICE_CERTIFICATE.json').read_text())['rows']}
for row in raw['rows']:
    z=json.loads((SRC/row['certificate_path']).read_text())
    y=list(map(F,z['primal_moments']));lam=list(map(F,z['dual_lambda']));gram=[list(map(F,r)) for r in z['dual_gram']]
    mean=list(map(F,z['mean_scaled']));ss,eps,scale=map(F,[z['det_scaled'],z['eps_scaled'],z['scale']])
    assert len(y)==70 and len(lam)==6 and len(gram)==15 and y[0]==1
    assert [y[ix[e((i,))]] for i in range(4)]==mean
    assert sum(v*y[ix[k]] for k,v in qc.items())==ss
    pd([[y[ix[plus(x,t)]] for t in feat] for x in feat]);pd(gram)
    assert row['model'] in ['old_F','norm4_control']
    obj=(fc if row['model']=='old_F' else nc).copy()
    for k,v in tc.items():obj[k]=obj.get(k,F(0))+eps*v
    target=obj.copy();zero=(0,0,0,0);target[zero]=target.get(zero,F(0))-lam[0]
    for i in range(4):
        k=e((i,));target[k]=target.get(k,F(0))-lam[i+1]
    for k,v in qc.items():target[k]=target.get(k,F(0))-lam[5]*v
    got={}
    for i,x in enumerate(feat):
        for j,t in enumerate(feat):
            k=plus(x,t);got[k]=got.get(k,F(0))+gram[i][j]
    assert all(got.get(k,F(0))==target.get(k,F(0)) for k in mom)
    lo=(lam[0]+sum(v*x for v,x in zip(lam[1:5],mean))+lam[5]*ss)*scale**4
    hi=sum(v*y[ix[k]] for k,v in obj.items())*scale**4
    assert lo==F(row['lower']) and hi==F(row['upper']) and lo<=hi
    bm=list(map(F,row['B']));ps,pe=map(F,[row['s'],row['epsilon']])
    assert bm==[scale*x for x in mean] and ps==scale*scale*ss and pe==scale*scale*eps
    control=None
    if row['model']=='norm4_control':
        tau=value(tc,bm)+2*abs(ps-value(qc,bm));assert lo<=tau*tau+pe*tau<=hi;control='closed norm4'
    elif ps==value(qc,bm):
        assert lo<=value(fc,bm)+pe*value(tc,bm)<=hi;control='literal graph'
    elif bm==[F(0)]*4 and abs(ps) in slices:
        left,right=slices[abs(ps)];assert pe==F(1,100) and lo<=left<=right<=hi;control='root exact slice'
    rows.append({'model':row['model'],'label':row['label'],'status':'EXACT_PASS','control':control,'width_display_only':float(hi-lo)})
result={'status':'ROOT_INDEPENDENT_ALL22_CERTIFICATES_PASS','method':'integer Bareiss Sylvester and literal symbolic coefficients',
        'rows':rows,'seconds':time.monotonic()-start,'scope':'70 coefficients, six constraints, exact primal/dual PSD and endpoints. No newer target QC or smoothness claim.'}
(OUT/'INDEPENDENT_CONSUMER.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'cases':len(rows),'formula_controls':sum(r['control'] is not None for r in rows),'seconds':result['seconds']},indent=2))
