import numpy as np,json
from scipy.linalg import sqrtm
rng=np.random.default_rng(20261030);dim=40
ix=lambda l,m,h,g:(((l*2+m)*2+h)*2+g)
def random_pos(n):
 x=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));a=x.conj().T@x+np.eye(n);return a/np.linalg.norm(a,2)
def coeff(owner):
 own=[1,2] if owner==0 else [3,4];a=random_pos(8);b=random_pos(2);out=np.zeros((dim,dim),complex)
 for l in range(5):
  for lp in range(5):
   for m in range(2):
    for mp in range(2):
     for h in range(2):
      for hp in range(2):
       for g in range(2):
        for gp in range(2):
         p,pp=(h,hp) if owner==0 else (g,gp);other,otherp=(g,gp) if owner==0 else (h,hp)
         if other!=otherp:continue
         v=0
         if l in own and lp in own:v=a[(own.index(l)*2+m)*2+p,(own.index(lp)*2+mp)*2+pp]
         elif l==lp and l not in own and m==mp:v=b[p,pp]
         out[ix(l,m,h,g),ix(lp,mp,hp,gp)]=v
 return out
def lift_lm(a):return np.kron(a,np.eye(4))
def monitor(label):
 a=np.zeros((10,10));a[2*label,2*label+1]=1;return lift_lm(a)
def cleanup(owner):
 x,y=(1,2) if owner==0 else (3,4);a=np.zeros((10,10));
 for m in range(2):a[2*x+m,2*y+m]=a[2*y+m,2*x+m]=1
 return lift_lm(a)
def zreset(owner):
 z=2 if owner==0 else 4;a=np.zeros((10,10));
 for m in range(2):a[m,2*z+m]=1
 return lift_lm(a)
def outside_acq():
 a=np.zeros((10,10))
 for m in range(2):a[m,6+m]=a[6+m,m]=1
 return lift_lm(a)
def erase(owner,s):
 out=np.zeros((dim,dim))
 for l in range(5):
  for m in range(2):
   for h in range(2):
    for g in range(2):
     if (h if owner==0 else g)==s:
      out[ix(l,m,0 if owner==0 else h,0 if owner==1 else g),ix(l,m,h,g)]=1
 return out
Rh,Rg=coeff(0),coeff(1);S_h=.6*np.eye(dim)+.2*Rh;S_g=.6*np.eye(dim)+.2*Rg
Kh=[np.array(sqrtm(S_h),complex)]+[erase(0,s)@np.array(sqrtm(np.eye(dim)-S_h),complex) for s in range(2)]
Kg=[np.array(sqrtm(S_g),complex)]+[erase(1,s)@np.array(sqrtm(np.eye(dim)-S_g),complex) for s in range(2)]
comm=lambda a,b:float(np.linalg.norm(a@b-b@a))
res={'dimension':dim,'coefficient_commutator':comm(Rh,Rg),'all_credit_kraus_commutator_max':max(comm(a,b) for a in Kh for b in Kg),'exterior_monitor_commutator_max':max(comm(Rh,monitor(l)) for l in [0,3,4]),'exterior_acquisition_commutator':comm(Rh,outside_acq()),'own_monitor_is_NOT_spectator':comm(Rh,monitor(1)),'credit_unitality_error':float(np.linalg.norm(sum(k.conj().T@k for k in Kh)-np.eye(dim)))}
# Closure: after own cleanup, z-reset, and actual owned monitor pieces,
# the result still commutes with a random exterior-owner algebra coefficient.
L=1j*(cleanup(0)@Rh-Rh@cleanup(0))
for j in [zreset(0),monitor(1),monitor(2)]:
 a=j.conj().T@j;L+=j.conj().T@Rh@j-(a@Rh+Rh@a)/2
res['enlarged_fast_adjoint_exterior_commutator']=comm(L,Rg)
assert res['coefficient_commutator']<1e-12
assert res['all_credit_kraus_commutator_max']<1e-12
assert res['exterior_monitor_commutator_max']<1e-12
assert res['exterior_acquisition_commutator']<1e-12
assert res['credit_unitality_error']<1e-12
assert res['enlarged_fast_adjoint_exterior_commutator']<1e-12
assert res['own_monitor_is_NOT_spectator']>1e-3
print(json.dumps(res,indent=2))
