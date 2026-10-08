"""Bounded diagnostic only. Floating-point optima are NOT certificates.

For a real or complex Hermitian frame, compare the least Dirichlet cost
of an HS-self-adjoint bistochastic self-compatible channel with the least
cost of a PPT bistochastic channel. The real mode restricts the Choi
variables to real matrices. The PPT minimum is a LOWER bound on all EB
costs, so a certified PPT_gap > C * compat_gap could refute C. Also probe
the Bose-supported PPT relaxation containing all pure canonical maps.
We enforce positive HS spectrum on the compatible channel. No floating
solver output certifies feasibility, separability, or optimality.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
import cvxpy as cp


def swap(d):
    s = np.zeros((d*d, d*d))
    for a in range(d):
        for b in range(d):
            s[a*d+b, b*d+a] = 1
    return s


def swap_bc(d):
    s = np.zeros((d**3,d**3))
    for a in range(d):
        for b in range(d):
            for c in range(d):
                s[(a*d+b)*d+c,(a*d+c)*d+b]=1
    return s


def basis(d):
    mats=[]
    for a in range(d):
        for b in range(a+1,d):
            h=np.zeros((d,d),complex)
            h[a,b]=h[b,a]=np.sqrt(d/2)
            mats.append(h)
            h=np.zeros((d,d),complex)
            h[a,b]=-1j*np.sqrt(d/2)
            h[b,a]=1j*np.sqrt(d/2)
            mats.append(h)
    for k in range(1,d):
        h=np.zeros((d,d),complex)
        h[:k,:k]=np.eye(k)
        h[k,k]=-k
        mats.append(h*np.sqrt(d/(k*(k+1))))
    return mats


class Probe:
    def __init__(self,d,complex_model=False):
        self.d=d
        self.complex_model=complex_model
        self.cost=cp.Parameter((d*d,d*d),hermitian=True) if complex_model else cp.Parameter((d*d,d*d),symmetric=True)
        self.costW=cp.Parameter((d*d,d*d),hermitian=True) if complex_model else cp.Parameter((d*d,d*d),symmetric=True)
        R=cp.Variable((d**3,d**3),hermitian=True) if complex_model else cp.Variable((d**3,d**3),symmetric=True)
        J=cp.partial_trace(R,(d,d,d),axis=2)
        S=swap(d); U=swap_bc(d)
        cons=[R>>0, R==U@R@U.T, J==S@J.T@S.T,
              cp.partial_trace(J,(d,d),axis=0)==np.eye(d)/d,
              cp.partial_trace(J,(d,d),axis=1)==np.eye(d)/d]
        bs=basis(d)
        trows=[]
        for a in bs:
            trows.append(cp.hstack([cp.real(cp.trace(np.kron(a.T,b)@J))
                                   for b in bs]))
        T=cp.vstack(trows)
        cons.append(T>>0)
        self.compat=cp.Problem(cp.Maximize(cp.real(cp.trace(self.cost@J))),cons)
        self.R=R; self.J=J; self.T=T
        E=cp.Variable((d*d,d*d),hermitian=True) if complex_model else cp.Variable((d*d,d*d),symmetric=True)
        self.ppt=cp.Problem(cp.Maximize(cp.real(cp.trace(self.cost@E))),[
            E>>0, cp.partial_transpose(E,(d,d),axis=0)>>0,
            E==S@E.T@S.T,
            cp.partial_trace(E,(d,d),axis=0)==np.eye(d)/d,
            cp.partial_trace(E,(d,d),axis=1)==np.eye(d)/d])
        self.E=E
        W=cp.Variable((d*d,d*d),hermitian=True) if complex_model else cp.Variable((d*d,d*d),symmetric=True)
        Ps=(np.eye(d*d)+S)/2
        # Pure canonical maps have J^{T_A} supported on the Bose space.
        self.canonical_ppt=cp.Problem(cp.Maximize(cp.real(cp.trace(self.costW@W))),[
            W>>0, cp.partial_transpose(W,(d,d),axis=0)>>0,
            W==Ps@W@Ps,
            cp.partial_trace(W,(d,d),axis=0)==np.eye(d)/d])
        self.W=W

    def solve(self,frame,name,out):
        d=self.d
        V=sum(np.trace(a@a).real/d for a in frame)
        cost=sum(np.kron(a.T,a) for a in frame)/V
        costW=sum(np.kron(a,a) for a in frame)/V
        self.cost.value=cost if self.complex_model else np.real(cost)
        self.costW.value=costW if self.complex_model else np.real(costW)
        start=time.time()
        v1=self.compat.solve(solver='SCS',eps=2e-6,max_iters=15000,
                             warm_start=False,verbose=False)
        v2=self.ppt.solve(solver='SCS',eps=2e-6,max_iters=15000,
                          warm_start=False,verbose=False)
        v3=self.canonical_ppt.solve(solver='SCS',eps=2e-6,max_iters=15000,
                                    warm_start=False,verbose=False)
        J=self.J.value; R=self.R.value; E=self.E.value
        row={'name':name,'d':d,'rank_bound':len(frame),'V':float(V),
             'compat_score':float(v1),'ppt_score_upper_EB':float(v2),
             'compat_gap':float(1-v1),'ppt_gap_lower_EB':float(1-v2),
             'gap_ratio':float((1-v2)/(1-v1)),
             'canonical_ppt_score_upper_EB':float(v3),
             'canonical_ppt_gap_lower_EB':float(1-v3),
             'canonical_ppt_ratio':float((1-v3)/(1-v1)),
             'compat_status':self.compat.status,'ppt_status':self.ppt.status,
             'canonical_ppt_status':self.canonical_ppt.status,
             'min_R_eig':float(np.linalg.eigvalsh(R)[0]),
             'min_T_eig':float(np.linalg.eigvalsh(self.T.value)[0]),
             'min_E_eig':float(np.linalg.eigvalsh(E)[0]),
             'min_W_eig':float(np.linalg.eigvalsh(self.W.value)[0]),
             'seconds':time.time()-start,'status':'FINITE_DIAGNOSTIC_ONLY'}
        np.savez(out/(name+'.npz'),frame=np.array(frame),R=R,J=J,E=E,W=self.W.value,
                 T=self.T.value,cost=self.cost.value)
        with (out/'sdp_results.jsonl').open('a') as f:
            f.write(json.dumps(row)+'\n')
        print(json.dumps(row),flush=True)


def random_frame(d,r,rng,near_diag=False,delta=.1,complex_frame=False):
    result=[]
    for _ in range(r):
        a=rng.standard_normal((d,d))
        if complex_frame:
            a=a+1j*rng.standard_normal((d,d))
        a=(a+a.conj().T)/2
        if near_diag:
            a=np.diag(np.diag(a))+delta*(a-np.diag(np.diag(a)))
        a-=np.trace(a)/d*np.eye(d)
        a/=np.sqrt(np.trace(a@a)/d)
        result.append(a)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--d',type=int,default=3)
    p.add_argument('--count',type=int,default=3)
    p.add_argument('--seed',type=int,default=20261009)
    p.add_argument('--near-diag',action='store_true')
    p.add_argument('--delta',type=float,default=.1)
    p.add_argument('--complex',action='store_true')
    p.add_argument('--rank',type=int,default=3)
    p.add_argument('--isotropic',action='store_true')
    args=p.parse_args()
    out=Path(__file__).parent
    probe=Probe(args.d,args.complex)
    rng=np.random.default_rng(args.seed)
    for k in range(args.count):
        f=basis(args.d) if args.isotropic else random_frame(args.d,args.rank,rng,args.near_diag,args.delta,args.complex)
        name=f'd{args.d}_s{args.seed}_{k}_r{args.rank}'
        name+=f'_delta{args.delta}' if args.near_diag else '_random'
        name+='_complex' if args.complex else '_real'
        name+='_isotropic' if args.isotropic else ''
        probe.solve(f,name,out)
