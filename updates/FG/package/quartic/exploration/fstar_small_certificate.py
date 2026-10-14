import numpy as np,sympy as sp,scipy.linalg as la,scipy.optimize as opt,pickle,os,itertools,json
BASE=os.path.dirname(__file__)
with open(BASE+'/c4_heat_symbolic.pkl','rb') as f:z=pickle.load(f)
S=z['S'];tau=sorted([x for x in S.free_symbols if str(x).startswith('tau')],key=str);a,c,e,L,d=z['param'];SP=S.subs({a:1,c:sp.Rational(7,2),e:sp.Rational(1,2),L:-sp.Rational(29,10),d:0});sf=sp.lambdify([tau],SP,'numpy')
Sd=np.array([np.array(SP.diff(t)).astype(float) for t in tau])
def fun(x):return -x[-1]
def con(x):return la.eigvalsh(sf(x[:6]))-x[-1]
def jac(x):
 val,V=la.eigh(sf(x[:6]));r=np.einsum('ik,pij,jk->kp',V,Sd,V);return np.c_[r,-np.ones(6)]
x0=np.array([8,0,0,0,1,1,0.]);sol=opt.minimize(fun,x0,jac=lambda x:np.r_[np.zeros(6),-1],constraints=[dict(type='ineq',fun=con,jac=jac)],method='SLSQP',options=dict(maxiter=2000,ftol=1e-12))
print(sol.success,sol.message,sol.x,con(sol.x),flush=True)
for den in [10,20,50,100,200,1000]:
 ts=[sp.Rational(round(float(x)*den),den) for x in sol.x[:6]];SS=SP.subs(dict(zip(tau,ts)));ev=la.eigvalsh(np.array(SS).astype(float))[0]
 print('den',den,'tau',ts,'eigen',ev)
 if ev>0:
  print('S=',SS)
  print('LDLdiags',[sp.factor(v) for v in SS.LDLdecomposition(hermitian=False)[1].diagonal()])
  # N coefficient solve for exact primitive; sparse solution through rref
  zz=np.load(BASE+'/heat_matrices.npz');N=sp.Matrix(zz['N'].astype(int).tolist());EA=z['EA'];p=sp.Matrix([1,sp.Rational(7,2),sp.Rational(1,2),-sp.Rational(29,10)])
  sv=sp.Matrix([SS[i,j] for i,j in z['ij']]);rhs=z['T']*sv-EA*p
  solc=next(iter(sp.linsolve((N,rhs))));free=set().union(*(v.free_symbols for v in solc));solc=sp.Matrix([v.subs({t:0 for t in free}) for v in solc])
  A=sp.symbols('a b c d');alph=[0]*4
  for co,inds in zip(solc,zz['alphas']):alph[inds[-1]]+=co*sp.prod(A[int(i)] for i in inds[:3])
  print('alpha raw',alph)
  with open(BASE+'/fstar_exact_small.pkl','wb') as f:pickle.dump(dict(S=SS,tau=ts,alpha=alph,c=solc,margin=sp.Rational(1,100)),f)
  break
