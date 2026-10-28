"""Private quantum retained-memory plant. Never imported by learner or replay.
The source returns only an ordinary bit. Internal audit is written separately.
No branch is sampled or revealed: the retained memory is a conditional density
operator updated by summing the CP branches weighted by the actual instrument.
"""
import numpy as np
from quantum_math import I,X,Y,Z,PAULIS,rotation,apply_kraus,trace_distance

def positive_sqrt(a):
    v,w=np.linalg.eigh(a)
    if v.min() < -1e-12: raise ValueError('not positive')
    return (w*np.sqrt(np.maximum(v,0)))@w.conj().T

class RetainedSource:
    def __init__(self,seed):
        self.rng=np.random.default_rng(seed)
        self.u=rotation([.31,-.72,.62],1.17)
        self.a=.045*(I+.65*Z)
        self.b=.055*(I+.60*X)
        self.kx=rotation([0,0,1],.63)@positive_sqrt(self.a)
        self.kz=rotation([1,0,0],.83)@positive_sqrt(self.b)
        self.h=positive_sqrt(I-2*self.a-2*self.b)
        self.maps=((self.kx,self.kz,self.h),(self.kx,),(),(self.kz,))
        psi=np.array([np.sqrt(.63),np.exp(.47j)*np.sqrt(.37)])
        self.sigma=np.outer(psi,psi.conj())
        self.calls=0;self.audit=[]

    def branches(self):
        return [sum((k@self.sigma@k.conj().T for k in ks),np.zeros((2,2),complex)) for ks in self.maps]

    def probe(self,ks,j,s):
        rho=(I+s*PAULIS[j+1])/2
        mismatch=(I-s*PAULIS[j+1])/2
        return self._instrument(ks,rho,mismatch)

    def probe_pauli(self,j,s,m):
        rho=(I+s*PAULIS[j+1])/2
        negative=(I-PAULIS[m+1])/2
        y=self._instrument([I],rho,negative)
        return 1-2*y

    def _instrument(self,ks,rho,mismatch):
        # ks frozen before this complete source call; not exposed to the source map.
        blocks=self.branches()
        masses=np.array([np.trace(x).real for x in blocks])
        probs=np.array([np.trace(mismatch@apply_kraus(ks,self.u@p@rho@p@self.u.conj().T)).real for p in PAULIS])
        p=float(masses@probs)
        if not -1e-12<=p<=1+1e-12: raise ValueError('invalid Born probability')
        coin=float(self.rng.random()); y=int(coin<p)
        weights=probs if y else 1-probs
        post=sum((q*b for q,b in zip(weights,blocks)),np.zeros((2,2),complex))
        normalization=float(np.trace(post).real)
        post=post/normalization
        unconditional=sum(blocks)
        prior=self.sigma.copy()
        self.sigma=(post+post.conj().T)/2
        self.calls+=1
        self.audit.append({'call':self.calls,'branch_masses':masses.tolist(),
            'born_mismatch_probability':p,'private_bernoulli_uniform':coin,
            'conditional_vs_unobserved_trace_distance':trace_distance(post,unconditional),
            'memory_prior_real':prior.real.tolist(),'memory_prior_imag':prior.imag.tolist(),
            'memory_post_real':post.real.tolist(),'memory_post_imag':post.imag.tolist(),
            'memory_post_min_eigen':float(np.linalg.eigvalsh(post).min()),
            'memory_post_purity':float(np.trace(post@post).real),
            'memory_post_offdiagonal_abs':float(abs(post[0,1]))})
        return y

    def metadata(self):
        to_json=lambda a:{'real':a.real.tolist(),'imag':a.imag.tolist()}
        tp=2*self.kx.conj().T@self.kx+2*self.kz.conj().T@self.kz+self.h.conj().T@self.h
        return {'unitary':to_json(self.u),'KX':to_json(self.kx),'KZ':to_json(self.kz),'H':to_json(self.h),
            'source_tp_residual':float(np.linalg.norm(tp-I)),
            'H_effect_min_eigen':float(np.linalg.eigvalsh(I-2*self.a-2*self.b).min()),
            'noncommuting_effect_commutator_frobenius':float(np.linalg.norm(self.a@self.b-self.b@self.a)),
            'source_memory_dimension':2,'physical_output_dimension':2,
            'CP_dominance_witness':'GI-GX=GZ+H_map; GI-GZ=GX+H_map; GI-GY=GI; each explicitly CP',
            'source_calls':self.calls}
