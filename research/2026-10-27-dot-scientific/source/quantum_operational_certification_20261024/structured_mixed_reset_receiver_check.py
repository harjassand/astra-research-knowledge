import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(20261027)
def state(d):
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); a=z@z.conj().T; return a/np.trace(a)
def norm(a):return np.linalg.norm(a,ord=2)
def pos(a):
 w,v=np.linalg.eigh(a);return (v*np.maximum(w,0))@v.conj().T
phi=np.zeros(9,complex);phi[[0,4,8]]=1/np.sqrt(3);Phi=np.outer(phi,phi.conj())
mins=[];bayes=[];count=0
for d in [1,2,3,5]:
 for p in [.001,.1,.5,.9,1.]:
  s,t=state(d),state(d);q=1-p
  js=np.kron(Phi,s);om=np.kron(np.eye(9)/9,p*s+q*t);J=p*js+q*np.kron(np.eye(9)/9,t)
  T=(J+3*om)/4;D=np.kron(np.eye(9),(5*p*s+4*q*t)/9);H=J-5*om
  assert norm(H-(p*js-D))<1e-13
  assert min(np.linalg.eigvalsh(D-T))>-1e-12
  assert min(np.linalg.eigvalsh(D/4-om))>-1e-12
  assert min(np.linalg.eigvalsh(8*D-H@H))>-1e-12
  assert abs(np.trace(D).real-(4+p))<1e-12
  assert np.trace(pos(H)).real<=p+1e-12
  for delta in [-.1,-.003,.003,.1]:
   a,b=4*delta,-8*delta;c=np.cos(a)*np.cos(b)
   L=(np.cos(b)*np.eye(9*d)-1j*np.sin(b)*om)@(np.cos(a)*np.eye(9*d)-1j*np.sin(a)*T)
   E=L-c*expm(-1j*delta*H)
   val=min(np.linalg.eigvalsh(8192*delta**4*D-E@E.conj().T));mins.append(val)
   assert val>-1e-11
  K=p*s-q*t;w,v=np.linalg.eigh(K);cut=p/(16*d)
  f=np.clip(w/cut,0,1);F=(v*f)@v.conj().T;M=(v*(w>0))@v.conj().T
  e=(1-np.linalg.norm(K,ord='nuc'))/2
  ef=(p*np.trace((np.eye(d)-F)@s)+q*np.trace(F@t)).real
  excess=np.trace((M-F)@K).real
  assert abs(ef-e-excess)<1e-12
  assert -1e-12<=excess<=d*cut+1e-12
  # The reference accepted/rejected Kraus sqrt(F) on matching Bell sector.
  # H positive modes only; define smooth effect by H eigenvalue converted to K.
  h,u=np.linalg.eigh(H);g=np.clip((9*h/4)/cut,0,1)
  AF=(u*np.sqrt(g))@u.conj().T;BF=(u*np.sqrt(1-g))@u.conj().T
  assert np.linalg.norm(BF@D@BF-D,ord='nuc')<=3*p+1e-11
  assert np.trace(AF@D@AF).real<=p+1e-11
  count+=1;bayes.append(excess)
print('PASS',count,'noncommuting source/soft-effect cases;',len(mins),'principal pair cases; min square slack',min(mins),'max Bayes excess',max(bayes))
# scalar budgets, including worst precision and small p0
for nu in [1,.1,.001]:
 for p0 in [1,.1,1e-6]:
  xi=nu/100;L=int(np.ceil(np.log(1000/(p0*xi))/np.log(16)));eta=(xi/(100*L))**2
  h=xi/(9*1e10*L);eh=lambda x:4e5*x*np.exp(2e5*x)
  beta=eta+eh(h);u=L*(4*np.sqrt(eta)+512*h)
  assert u<=xi/20 and beta<=1/16 and beta**L<=p0*xi/1000
  assert 5*beta**L+p0*eh(h)/(1-beta)+2*p0*u<=p0*xi/9
  k=eh(L*h)+eta**L
  assert k<=xi/4000 and k+eh(L*h)+2*u<=xi/9
print('PASS 9 parameter-budget cases')
