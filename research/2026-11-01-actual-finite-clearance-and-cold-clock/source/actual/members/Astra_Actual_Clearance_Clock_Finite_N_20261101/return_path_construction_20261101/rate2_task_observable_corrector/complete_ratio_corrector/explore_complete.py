import pickle,sympy as S,mpmath as mp
from pathlib import Path
P=Path(__file__).parent
ob=pickle.load(open(P/'complete_algebra.pkl','rb'));r,u,t,a,z,s=ob['vars']
hf=[S.lambdify((r,u,t,z,s),q,'mpmath',cse=True) for q in ob['chi_power'][1:]]
meanf=S.lambdify((r,u,t,z,s),ob['mean'],'mpmath',cse=True)
rf=[(name,S.lambdify((r,u,t,a,z,s),rate,'mpmath'),tuple(mp.mpf(str(v)) if not isinstance(v,S.Rational) else mp.mpf(int(v.p))/int(v.q) for v in j)) for name,rate,j in ob['rows']]
mp.mp.dps=100
def f2(rr,uu,tt,aa,zz,ss):
 h=[fn(rr,uu,tt,zz,ss) for fn in hf]
 return rr*(1-aa*uu)+sum(hh*aa**j for j,hh in enumerate(h,1))
def gen2(rr,uu,tt,aa,zz,ss):
 f=f2(rr,uu,tt,aa,zz,ss);total=0
 for name,rate,j in rf:
  da,dl,de,dz,dn=j;ch=1+de*uu*tt/rr;lh=1+dl*tt
  fp=f2(rr*ch*ch/lh,uu*ch,tt/lh,(aa+tt*da)/lh,(zz+tt*dz)/lh,ss+dn*uu*uu*tt/rr)
  total+=rate(rr,uu,tt,aa,zz,ss)*(fp-f)/(uu*tt)
 return total
for q in (3,4,6,8,10):
 for rr in (mp.mpf('.5'),mp.mpf('2')):
  for ss in (mp.mpf('.99'),mp.mpf('1'),mp.mpf('1.01')):
   uu=tt=mp.mpf(10)**(-q);aa=mp.mpf('.01');zz=mp.mpf(0)
   val=gen2(rr,uu,tt,aa,zz,ss);mean=meanf(rr,uu,tt,zz,ss);change=f2(rr,uu,tt,aa,zz,ss)-rr
   print('q',q,'r',rr,'s',ss,'GF2/(uL)',mp.nstr(val,18),'mean',mp.nstr(mean,12),'F2-R',mp.nstr(change,8),flush=True)
