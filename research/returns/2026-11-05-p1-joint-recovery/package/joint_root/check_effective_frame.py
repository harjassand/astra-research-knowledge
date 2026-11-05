"""Replay saved physical frame/readout without reoptimizing any SDP.

Floating-point audit, not an interval-certified proof. The decoder is
specified by positive-part and marginal normalization of saved matrices.
Fidelities below use explicit Choi action, not the SDP objective formula.
"""
from pathlib import Path
import sys, json, argparse
import numpy as np
from scipy.linalg import eigh, norm
from scipy.sparse.linalg import expm_multiply
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'joint_channel'))
import cascade_effective as ce

def herm(x): return (x+x.conj().T)/2
def marginal(j,r): return np.einsum('aiaj->ij',j.reshape(2,r,2,r))
def repair(j,r):
    w,v=eigh(herm(j)); pos=(v*np.maximum(w,0))@v.conj().T
    a=herm(marginal(pos,r)); w,v=eigh(a)
    assert min(w)>1e-8
    root=(v*(w**-.5))@v.conj().T
    big=np.kron(np.eye(2),root)
    return herm(big@pos@big)
def apply(j,x):
    r=x.shape[0]
    return np.einsum('iajb,ab->ij',j.reshape(2,r,2,r),x)

def run(k,t):
    tag=f'effective_frame_k{k}_t{t:g}'
    z=np.load(Path(__file__).resolve().parent/'results'/f'{tag}.npz')
    psi=z['initial_vector']; psi=psi/norm(psi)
    B=ce.build(k+1); initial=ce.initial(B,psi)
    value=expm_multiply(t*B['G'],initial,traceA=t*B['traceG'])
    pieces=initial.copy()
    for _ in range(7):
        pieces=expm_multiply(t/7*B['G'],pieces,traceA=t/7*B['traceG'])
    out=ce.output_blocks(B,value); out2=ce.output_blocks(B,pieces)
    images=[np.zeros((2,2),complex) for _ in range(4)]
    images2=[np.zeros((2,2),complex) for _ in range(4)]
    blocks=[]
    for j,xs in out.items():
        r=xs[0].shape[0]; saved=z[f'decoder_j{j}']; dec=repair(saved,r)
        blocks.append(dict(j=j,multiplicity=r,
            probability=float(np.trace(xs[0]).real),
            saved_min_eigenvalue=float(eigh(herm(saved),eigvals_only=True)[0]),
            saved_tp_residual=float(norm(marginal(saved,r)-np.eye(r),2)),
            repaired_min_eigenvalue=float(eigh(dec,eigvals_only=True)[0]),
            repaired_tp_residual=float(norm(marginal(dec,r)-np.eye(r),2)),
            repair_distance_fro=float(norm(dec-saved,'fro'))))
        for mu,x in enumerate(xs):
            images[mu]+=apply(dec,x); images2[mu]+=apply(dec,out2[j][mu])
    choi=herm(sum(np.kron(p.T,x) for p,x in zip(ce.PAULI,images))/2)
    choi2=herm(sum(np.kron(p.T,x) for p,x in zip(ce.PAULI,images2))/2)
    bell=np.array([1.,0.,0.,1.])/np.sqrt(2)
    pt=choi.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
    Fe=float(np.vdot(bell,choi@bell).real)
    ans=dict(k=k,t=t,Fe_explicit_choi=Fe,
        twirled_half_diamond_error=1-Fe,bell_margin_above_separable=Fe-.5,
        output_choi_min_eigenvalue=float(eigh(choi,eigvals_only=True)[0]),
        output_partial_transpose_min_eigenvalue=float(eigh(herm(pt),eigvals_only=True)[0]),
        reference_marginal_residual=float(norm(np.einsum('aibi->ab',choi.reshape(2,2,2,2))-np.eye(2)/2,2)),
        independent_seven_piece_output_trace_distance=float(sum(abs(eigh(choi-choi2,eigvals_only=True)))/2),
        blocks=blocks,
        scope='Saved finite receiver; floating-point feasibility and semigroup replay. No interval certification, global optimum, high-fidelity scaling, or positive unassisted capacity is claimed.')
    path=Path(__file__).resolve().parent/'results'/f'{tag}_audit.json'
    path.write_text(json.dumps(ans,indent=2)+'\n')
    np.savez_compressed(path.with_suffix('.npz'),recovered_choi=choi,recovered_choi_seven_piece=choi2)
    print(json.dumps(ans),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--k',type=int,default=9);p.add_argument('--t',type=float,default=1.)
    a=p.parse_args();run(a.k,a.t)
