"""Numerical tests of a stronger positive-rank-two conjecture; not a certificate."""
from werner_probe import transform
from pathlib import Path
import torch,json,time,argparse

def run(n=4,d=3,starts=10,iterations=150,seed=811):
    torch.manual_seed(seed);vals=[];N=d**n;dims=(d,)*n;t=time.monotonic()
    for k in range(starts):
        A=torch.randn(N,2,dtype=torch.complex128)
        if k%2:
            A*=.02;A[0,0]+=1;A[N-1,1]+=1
        A.requires_grad_()
        def objective():
            C=A@A.mH;norm2=torch.sum(abs(C)**2)
            q=torch.real(torch.sum(C.conj()*transform(C,dims)))
            return (2**n*q-2*norm2+torch.real(torch.trace(C))**2)/norm2
        opt=torch.optim.LBFGS([A],lr=1,max_iter=iterations,
                       tolerance_grad=1e-10,tolerance_change=1e-12,line_search_fn='strong_wolfe')
        def closure():
            opt.zero_grad();f=objective();f.backward();A.grad=A.grad.resolve_conj().contiguous();return f
        opt.step(closure);v=objective().item();vals.append(v)
        print(k,v,flush=True)
    out={'n':n,'d':d,'seed':seed,'starts':starts,'iterations':iterations,
         'normalized_strengthened_deficits':vals,'elapsed_seconds':time.monotonic()-t,
         'status':'finite floating-point local search, not an all-input statement'}
    (Path(__file__).parent/f'positive_deficit_d{d}_n{n}.json').write_text(json.dumps(out,indent=2))
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=4);p.add_argument('--d',type=int,default=3)
    p.add_argument('--starts',type=int,default=10);p.add_argument('--iterations',type=int,default=150)
    args=p.parse_args();print(json.dumps(run(**vars(args)),indent=2))
