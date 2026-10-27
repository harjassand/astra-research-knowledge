"""Pure exact receiving for the nonflat two-mode shared-clock one-crossing theorem.
The large integer weights are proof data; no optimizer or floating point is used.
"""
import sympy as S
from math import comb
from pathlib import Path
import json,hashlib
s,b,c,p,d=S.symbols('s b c p d');w=s+b;qc=p+(1-p)*c;rc=1-p+p*c
D=(s+1)*(s+c);Di=(3*s+1)*(3*s+c)
A=2*w*D-b*(qc*s+c)
B=4*w*w*D-2*b*w*(qc*s+c)+b*b*c*d
J=9*s*s+(9*b+3+3*c)*s+c+3*b*rc
R=w*w*(s+3)*(s+3*c)-b*w*(p*(s+3*c)+(1-p)*c*(s+3))+b*b*c*d
num=3**18*s**5*D*D*A*A*B*B;den=64*w*Di**6*J**3*R
N=S.Poly(S.expand(num-den),s);assert N.degree()==21
assert S.factor(N.LC()-49589822592*(c*c+1))==0
assert S.factor(N.nth(0)+64*b**3*c**7*(d+6)*(c+3*b*rc)**3)==0
assert N.nth(3).subs(b,0)==-576*c**10
assert all(N.nth(k).subs(b,0)==0 for k in range(3))
# Original actual rank-one determinant lemma heads.
x=1/s;beta=-b/(s*w)
def td(k):
 h1=1/(1+k*x);h2=c/(1+k*x*c)
 return p*h1+(1-p)*h2,d*h1*h2
to,do=td(1);ti,_=td(S.Rational(1,3));tr,dr=td(3)
base=((1+x)*(1+c*x))**6/(((1+x/3)*(1+c*x/3))**9*(1+3*x)*(1+3*c*x))
ratio=base*(1+beta*to/2)**2*(1+beta*to/2+beta*beta*do/4)**2/((1+beta*ti/3)**3*(1+beta*tr+beta*beta*dr))
assert S.factor(ratio-num/den)==0
print('Exact degree21 source ratio and endpoint signs PASS',flush=True)
# Homogeneous p,Gram determinant, and bounded c coordinates.
# p=P/(P+Q), d=PQ H1/[(P+Q)^2(H0+H1)], c=z/(1+z).
# Common multiplier:(P+Q)^6(H0+H1)^2(1+z)^10.
# Dictionary key(b degree,z degree,P degree,H1 degree); Q/H0 degrees are implicit.
co={}
for j in range(22):
 tmp={}
 for (bb,cc,ii,kk),val in S.Poly(N.nth(j),b,c,p,d).terms():
  nn=6-ii-2*kk;assert nn>=0 and kk<=2 and cc<=10
  for pp in range(nn+1):
   for hh in range(3-kk):
    for zz in range(cc,11):
     key=(bb,zz,ii+kk+pp,kk+hh)
     tmp[key]=tmp.get(key,0)+int(val)*comb(nn,pp)*comb(2-kk,hh)*comb(10-cc,zz-cc)
 co[j]={k:v for k,v in tmp.items() if v}
for j in range(6):assert all(v<0 for v in co[j].values())
for j in range(18,22):assert all(v>0 for v in co[j].values())
weights_path=Path(__file__).with_name('nonflat_two_mode_white_rank_one_reset_chain_weights.json')
weights=json.loads(weights_path.read_text())['weights'];mons=[(0,0),(1,0),(0,1),(1,1)];report=[]
for j in range(6,17):
 ww=weights[str(j)];assert len(ww)==8 and all(v>=0 for v in ww) and sum(ww[:4])>0 and sum(ww[4:])>0
 out={}
 for row,sg,part in [(co[j],-1,ww[:4]),(co[j+1],1,ww[4:])]:
  for mult,(db,dz) in zip(part,mons):
   for (bb,zz,pp,hh),val in row.items():
    key=(bb+db,zz+dz,pp,hh);out[key]=out.get(key,0)+sg*mult*val
 assert all(v>=0 for v in out.values())
 nonzero={k:v for k,v in out.items() if v};assert nonzero
 canonical='\n'.join(str(k)+':'+str(v) for k,v in sorted(nonzero.items()))
 report.append({'chain':j,'positive_coefficients':len(nonzero),'zero_coefficients':len(out)-len(nonzero),'sha256':hashlib.sha256(canonical.encode()).hexdigest()})
 print('chain',j,'PASS:',len(nonzero),'positive coefficients;',len(out)-len(nonzero),'zeros',flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps({'domain':'b>0,0<c<1,0<=p<=1,0<=d<=p(1-p)','degree':21,'coefficient_domain_transform':'(P+Q)^6(H0+H1)^2(1+z)^10','chains':report,'weight_file_sha256':hashlib.sha256(weights_path.read_bytes()).hexdigest()},indent=2))
print('PASS: all11 exact nonnegative coefficient chains; no numerical optimization used in receiving.')
