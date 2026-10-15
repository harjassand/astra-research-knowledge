"""Exploratory compatible Fourier search; numerical output is not a proof.

Quartic trig averages use at least 4K+1 nodes in each direction, so the
quadrature itself integrates the represented polynomial exactly up to float
roundoff.  The affine background is minimized analytically as a PSD quadratic.
Only this worker's output directory is written.
"""
import argparse, json, time
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import minimize

ap = argparse.ArgumentParser()
ap.add_argument('--r', type=float, default=-2.5)
ap.add_argument('--k', type=int, default=2)
ap.add_argument('--restarts', type=int, default=4)
ap.add_argument('--maxiter', type=int, default=500)
ap.add_argument('--seed', type=int, default=20261015)
ap.add_argument('--aspect', type=float, default=1.)
args = ap.parse_args()
r = args.r
assert r < -2

x = sp.symbols('a b c d')
a,b,c,d = x
F = (3*r/(8*(r+2))*((a-d)**2+(b+c)**2)**2
     +r*(r-1)*(a*a+c*c)**2/6+(a*d-b*c)**2
     +r*(a*a+c*c)*(a*d-b*c))
ff = sp.lambdify(x, F, 'numpy', cse=True)
gg = [sp.lambdify(x, sp.diff(F,t), 'numpy', cse=True) for t in x]
hh = [[sp.lambdify(x, sp.diff(F,t,s), 'numpy', cse=True)
       for s in x] for t in x]

N = 4*args.k+1
XX,YY = np.meshgrid(2*np.pi*np.arange(N)/N,
                    2*np.pi*np.arange(N)/N, indexing='ij')
modes = [(i,j) for i in range(-args.k,args.k+1)
         for j in range(-args.k,args.k+1)
         if i>0 or (i==0 and j>0)]
bas=[]
for i,j in modes:
    phase = i*XX+j*YY
    for trig in [np.cos(phase), -np.sin(phase)]:
        for target in range(2):
            v=np.zeros((N*N,4))
            v[:,2*target]=i*args.aspect*trig.ravel()
            v[:,2*target+1]=j*trig.ravel()
            bas.append(v)
bas=np.array(bas)
nb=len(bas)

def grad(q):
    return np.array([g(*q.T)+np.zeros(len(q)) for g in gg]).T

def objective(co, details=False):
    q=np.einsum('k,knc->nc',co,bas)
    q2=(q*q).sum(axis=1)
    den=np.mean(q2*q2)
    vals=[np.mean(g(*q.T)) for g in gg]
    lin=np.array(vals)
    mat=np.array([[np.mean(h(*q.T)) for h in row] for row in hh])/2
    eig,U=np.linalg.eigh(mat)
    tol=max(eig[-1],1)*1e-13
    inv=np.where(eig>tol,1/np.maximum(eig,tol),0)
    B=-.5*U@(inv*(U.T@lin))
    const=np.mean(ff(*q.T))
    gap=const+.5*lin@B
    ans=gap/den
    gq=grad(q+B)-grad(np.broadcast_to(B,q.shape))
    numg=np.einsum('knc,nc->k',bas,gq)/len(q)
    deng=np.einsum('knc,nc->k',bas,4*q2[:,None]*q)/len(q)
    jac=(numg-ans*deng)/den
    if details:
        return {'ratio':float(ans),'B':B.tolist(),
                'affine_quadratic_eigenvalues':eig.tolist(),
                'q_fourth_average':float(den),'zero_B_ratio':float(const/den),
                'affine_linear_kernel_residual':float(np.linalg.norm(
                    lin-2*mat@(-B))), 'gradient_norm':float(np.linalg.norm(jac))}
    return ans,jac

rng=np.random.default_rng(args.seed)
record={'scope':'Exploratory finite Fourier optimization, no global theorem',
        'r':r,'K':args.k,'aspect':args.aspect,'grid_nodes_per_axis':N,
        'modes':modes,'runs':[]}
best=None
start=time.monotonic()
for seed in range(args.restarts):
    co=rng.normal(size=nb)
    co/=np.linalg.norm(co)
    opt=minimize(objective,co,jac=True,method='L-BFGS-B',
                 options={'maxiter':args.maxiter,'gtol':1e-9,'ftol':1e-12,
                          'maxls':30})
    item=objective(opt.x,True)
    item.update(seed=seed,success=bool(opt.success),iterations=int(opt.nit),
                message=str(opt.message))
    record['runs'].append(item)
    if best is None or item['ratio']<best['ratio']:
        best=dict(item,coefficients=opt.x.tolist())
    print(json.dumps(item),flush=True)
record['best']=best
record['elapsed_seconds']=time.monotonic()-start
out=Path(__file__).with_name(f'fourier_r{r:g}_k{args.k}_aspect{args.aspect:g}.json')
out.write_text(json.dumps(record,indent=2)+'\n')
print('saved',out,flush=True)
