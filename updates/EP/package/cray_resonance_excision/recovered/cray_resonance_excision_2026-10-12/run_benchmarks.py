import json, math, time, sys
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import inv
from resonance_compiler import make_grid, Compiler, wick_two_orders, Model
ROOT=Path(__file__).parent

def transfer(model,q,radius=5.):
    n=model.n
    x,w=leggauss(q); x*=radius; w*=radius
    onsite=np.exp(-.5*np.diag(model.A)[:,None]*x*x-model.g*x**4/4
                  +.5j*np.diag(model.C)[:,None]*x*x)
    v=w*onsite[0]; logscale=0.
    for k in range(n-1):
        E=np.exp((-model.A[k,k+1]+1j*model.C[k,k+1])*np.outer(x,x))
        v=(v@E)*(w*onsite[k+1])
        scale=np.max(np.abs(v)); v/=scale; logscale+=np.log(scale)
    logZ=np.log(np.sum(v))+logscale
    c=Compiler(model); logG=.5*n*np.log(2*np.pi)+c.F0
    return np.log(np.exp(logZ-logG))

def main():
    results={'status':'floating research prototype; ideal-arithmetic certificate not interval-implemented',
      'seed_policy':'explicit rational independent seeded grid inputs; same inputs and output log(Z/Z_G) for all methods',
      'numpy':np.__version__,'benchmarks':[]}
    for L,k,N in [(4,35,25000),(8,50,25000),(16,70,4000)]:
        m=make_grid(L,k,seed=20261012+L)
        np.savez(ROOT/f'grid_{L}_{int(k)}.npz',A=m.A,C=m.C,g=m.g,kappa=m.kappa,
                 amin=m.amin,amax=m.amax,cmax=m.cmax)
        c=Compiler(m)
        out=c.iid(N,seed=603001+L)
        wick=wick_two_orders(m)
        direct=c.iid(2000,seed=604001+L,center=False,clipped=False)
        out['ideal_relative_error_at_95pct']=math.sqrt(out['certificate']['relative_variance_bound']/(.05*N))
        diff=np.array(out['log_ratio'])-np.array(wick['two_order_log_ratio'])
        results['benchmarks'].append(dict(grid_side=L,kappa=k,compiler=out,wick=wick,
                                         plain_intermediate_field=direct,
                                         stochastic_minus_wick_log_difference=diff.tolist()))
        print('grid',L,'completed',out['sample_seconds'],flush=True)
    chain=make_grid(16,35,seed=71236,chain=True); c=Compiler(chain)
    tr=[]
    for q in (192,320,512):
        tic=time.perf_counter(); value=transfer(chain,q); elapsed=time.perf_counter()-tic
        tr.append(dict(nodes=q,log_ratio=[value.real,value.imag],seconds=elapsed))
    results['chain_matched_comparison']={'input':'heterogeneous 16-site chain, same coefficient generator',
        'transfer':tr,'compiler':c.iid(25000,seed=651),'wick':wick_two_orders(chain)}
    gates=[]
    for k in [4,6,8,12,16,20,25,30,35,50]:
        m=make_grid(4,k); c=Compiler(m)
        gates.append(c.certificate())
    results['fixed_size_gate_sweep']=gates
    with open(ROOT/'benchmark_results.json','w') as f: json.dump(results,f,indent=2)
    print(json.dumps(results['chain_matched_comparison'],indent=2),flush=True)

if __name__=='__main__':main()
