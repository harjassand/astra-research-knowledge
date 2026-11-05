"""Pure-frame and readout alternation in the rigorously fixed-k slow limit.

Uses the channel constructor's derived generator. These are local numerical
optima of a restricted physical cascade, not global receiver bounds. The
source is never accessed by the physical policy; it appears offline only.
"""
import sys,json,argparse
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import expm_multiply
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'joint_channel'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'joint_operational'))
import cascade_effective as ce
from control_search import SDPSolver,choi_cost,adjoint_local,trace_pair,herm
P=ce.PAULI
bell=np.array([1.,0.,0.,1.])/np.sqrt(2);phi=np.outer(bell,bell)

def backward_effect(B,block_effects):
    x={j:np.zeros((B['mult'][j],B['mult'][j]),complex) for j in B['js']}
    for (j,k),ids in B['parent'].items():
        x[j][np.ix_(ids,ids)]=block_effects[k]
    return B['pack']({j:B['rec'][j].T@x[j]@B['rec'][j] for j in B['js']})

def physical(B,v):
    x=B['unpack'](v);d=B['Q'].shape[0]
    out=np.zeros((d,d),complex)
    for j in B['js']:
        for mm in range(-j,j+1,2):
            ids=B['groups'][j,mm]
            q=B['Q'][:,ids]
            out+=q@x[j]@q.conj().T
    return herm(out)

def run(k,t,starts,sweeps,solver='CLARABEL',tol=3e-9):
    B=ce.build(k+1);m=2**k;rng=np.random.default_rng(72614+k)
    solvers={};best=None
    for trial in range(starts):
        if trial==0:psi=ce.frame(k,'triad')
        else:
            psi=rng.normal(size=m)+1j*rng.normal(size=m);psi/=np.linalg.norm(psi)
        decoders={};hist=[]
        for iteration in range(sweeps+1):
            v0=ce.initial(B,psi)
            value=expm_multiply(t*B['G'],v0,traceA=t*B['traceG'])
            blocks=ce.output_blocks(B,value)
            fidelity=0.;be=[{} for _ in range(4)]
            for j,images in blocks.items():
                r=images[0].shape[0]
                rho=herm(sum(np.kron(p.T,x) for p,x in zip(P,images))/2)
                cost=choi_cost(rho,phi,2,r)
                solvers.setdefault(j,SDPSolver(r,2,solver=solver,tol=tol))
                decoder,_=solvers[j].solve(cost,decoders.get(j));decoders[j]=decoder
                fidelity+=trace_pair(cost,decoder)
                for mu,p in enumerate(P):be[mu][j]=adjoint_local(p,decoder,2,r)
            hist.append(fidelity)
            if iteration==sweeps or (iteration>2 and abs(hist[-1]-hist[-2])<2e-8):break
            backwards=np.stack([backward_effect(B,be[mu]) for mu in range(4)],axis=1)
            backwards=expm_multiply(t*B['G'].H,backwards,traceA=t*B['traceG'])
            cost0=np.zeros((m,m),complex)
            for mu,p in enumerate(P):
                a=physical(B,backwards[:,mu]).reshape(2,m,2,m)
                cost0+=np.einsum('ba,aibj->ij',p,a)/8
            cost0=herm(cost0)
            current=float(np.vdot(psi,cost0@psi).real)
            if abs(current-fidelity)>1e-7:raise ValueError(('forward/backward mismatch',current,fidelity))
            vals,vecs=np.linalg.eigh(cost0);psi=vecs[:,-1]
        rec={'k':k,'t':t,'trial':trial,'Fe':float(fidelity),'history':hist,'limiting_Petz_visibility':ce.evaluate(B,value,False)['a'],'solver':solver,'solver_tolerance':tol,
             'scope':'fixed-k theta-to-zero matched cascade; initialization/readout local alternation, not a uniform-k result'}
        print(json.dumps(rec),flush=True)
        if best is None or fidelity>best[0]:best=(fidelity,psi,decoders.copy(),rec)
    tag=f'effective_frame_k{k}_t{t:g}'
    Path('joint_root/results').mkdir(exist_ok=True)
    np.savez_compressed(f'joint_root/results/{tag}.npz',initial_vector=best[1],**{f'decoder_j{j}':v for j,v in best[2].items()})
    Path(f'joint_root/results/{tag}.json').write_text(json.dumps(best[3],indent=2)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--k',nargs='+',type=int,default=[3,4,5,6]);ap.add_argument('--t',nargs='+',type=float,default=[1.]);ap.add_argument('--starts',type=int,default=3);ap.add_argument('--sweeps',type=int,default=18);ap.add_argument('--solver',default='CLARABEL');ap.add_argument('--tol',type=float,default=3e-9)
    a=ap.parse_args()
    for k in a.k:
        for t in a.t:run(k,t,a.starts,a.sweeps,a.solver,a.tol)
