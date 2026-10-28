"""Use the actual Euler-Lagrange residual to add compatible Fourier modes."""
import json,time,numpy as np
from scipy.optimize import minimize
from compatible_core import FourierProblem,TENSOR,gradient,half_square,ROOT

def force_candidates(record,count=4):
 freq=record['frequencies'];cutoff=max(abs(k)for f in freq for k in f);p=FourierProblem(freq,grid=6*cutoff+1)
 q=np.array(record['normalized_gradient_amplitudes']).ravel();x=np.einsum('npi,p->ni',p.design,q);B=np.array(record['background'])
 obj=record['objective_scaled'];square=np.sum(x*x,axis=1)
 g=gradient(x)+12*np.einsum('ijkl,j,nk,nl->ni',TENSOR,B,x,x,optimize=True)
 g+=x@(12*np.einsum('ijkl,j,k->il',TENSOR,B,B)).T;g-=obj*4*square[:,None]*x
 ft=np.fft.fftn(g.reshape(p.grid,p.grid,4),axes=(0,1))/p.grid**2;available=[]
 for k in half_square(3*cutoff):
    if list(k)in freq:continue
    unit=np.array(k)/np.linalg.norm(k);f=ft[k[0]%p.grid,k[1]%p.grid].reshape(2,2)@unit
    available.append((float(np.linalg.norm(f)),k,np.stack([-f.real,f.imag])))
 available.sort(key=lambda t:t[0],reverse=True)
 return available[:count]

def run(generations=8):
 source=json.loads((ROOT/'data/fourier_cutoff3.json').read_text());current=source['runs'][source['best_start']]
 out={'status':'COMPATIBLE_EULER_RESIDUAL_MODE_GROWTH_NOT_QC_PROOF','initial':current,'steps':[]}
 for generation in range(generations):
    start=time.monotonic();new=force_candidates(current)
    freq=current['frequencies']+[list(t[1])for t in new];p=FourierProblem(freq)
    old=np.array(current['normalized_gradient_amplitudes']).ravel();extra=np.array([t[2]for t in new]).ravel();extra/=max(np.linalg.norm(extra),1e-30)
    seed=np.r_[old,.02*extra];initial=p.evaluate(seed,True)
    opt=minimize(p.evaluate,seed,jac=True,method='L-BFGS-B',options=dict(maxiter=1500,ftol=1e-14,gtol=2e-10,maxls=50,maxcor=20))
    final=p.evaluate(opt.x,True)
    rec=dict(generation=generation,force_modes=[{'frequency':list(k),'force_norm':s,'negative_force_amplitudes':a.tolist()}for s,k,a in new],before=current,small_step=initial,after=final,iterations=int(opt.nit),seconds=time.monotonic()-start)
    out['steps'].append(rec);(ROOT/'data/mode_growth.json').write_text(json.dumps(out,indent=2));current=final
    print(generation,len(freq),final['grid'],final['objective_scaled'],new[0][0],rec['seconds'],flush=True)
 return out
if __name__=='__main__':run()
