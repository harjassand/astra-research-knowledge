"""Finite rank-two searches. Numerical probes, NOT a proof of positivity."""
import argparse, json, math, time
from pathlib import Path
import numpy as np
import torch

torch.set_num_threads(1)

def transform(C: torch.Tensor, dims: tuple[int, ...]) -> torch.Tensor:
    n = len(dims)
    X = C.reshape(dims+dims)
    for i, d in enumerate(dims):
        rest = [j for j in range(n) if j != i]
        p = [i]+rest+[n+i]+[n+j for j in rest]
        inv = np.argsort(p).tolist()
        D = math.prod(dims)//d
        Y = X.permute(p).reshape(d,D,d,D)
        tr = torch.einsum('aiaj->ij',Y)
        eye = torch.eye(d,dtype=C.dtype,device=C.device)
        Y = Y - eye[:,None,:,None]*tr[None,:,None,:]/2
        pdims = [dims[j] for j in [i]+rest]*2
        X = Y.reshape(pdims).permute(inv)
    return X.reshape(C.shape)

def objective(A, B, dims):
    C = A @ B.mH
    norm2 = torch.sum(torch.abs(C)**2)
    return torch.real(torch.sum(C.conj()*transform(C,dims)))/norm2.clamp_min(1e-300)

def run(d=3,n=3,starts=25,iterations=200,seed=1947):
    torch.manual_seed(seed)
    N=d**n; dims=(d,)*n
    outcomes=[]; best=1e100; bestAB=None
    begin=time.monotonic()
    for k in range(starts):
        A=torch.randn(N,2,dtype=torch.complex128)
        B=torch.randn(N,2,dtype=torch.complex128)
        if k % 3 == 1:
            A*=0.05; B*=0.05
            A[0,0]+=1; A[d**(n-1),1]+=1
            B[0,0]+=1; B[d**(n-1),1]+=1
        if k % 3 == 2:
            B=A.clone()
        A.requires_grad_(); B.requires_grad_()
        opt=torch.optim.LBFGS([A,B],lr=1,max_iter=iterations,
                             tolerance_grad=1e-11,tolerance_change=1e-13,
                             line_search_fn='strong_wolfe')
        def closure():
            opt.zero_grad()
            loss=objective(A,B,dims)
            if not torch.isfinite(loss):
                raise FloatingPointError('Nonfinite objective')
            loss.backward()
            A.grad = A.grad.resolve_conj().contiguous()
            B.grad = B.grad.resolve_conj().contiguous()
            return loss
        opt.step(closure)
        val=objective(A,B,dims).item()
        outcomes.append(val)
        if val<best:
            best=val; bestAB=(A.detach().numpy(),B.detach().numpy())
        print(f'{k+1}/{starts}: {val:.12g}',flush=True)
    out={'dimensions':dims,'rank_bound':2,'random_seed':seed,
         'starts':starts,'max_lbfgs_iterations':iterations,
         'objectives':outcomes,'minimum':best,'elapsed_seconds':time.monotonic()-begin,
         'status':'floating-point finite local-search diagnostic; no universal inference'}
    root=Path(__file__).parent
    (root/f'probe_d{d}_n{n}.json').write_text(json.dumps(out,indent=2))
    np.savez(root/f'best_d{d}_n{n}.npz',A=bestAB[0],B=bestAB[1])
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--d',type=int,default=3)
    p.add_argument('--n',type=int,default=3); p.add_argument('--starts',type=int,default=25)
    p.add_argument('--iterations',type=int,default=200);p.add_argument('--seed',type=int,default=1947)
    a=p.parse_args(); print(json.dumps(run(**vars(a)),indent=2))
