"""Native recursive rejection on an extensive frustrated triangular ladder.

Executes the CONDITIONAL-common-phase operation only. It does not execute
the phase-normalizer FPRAS or claim canonical count conditioning here.
RNG backend is explicitly reused from sampler.py in this package.
"""
from pathlib import Path
import hashlib,json,math,time
import numpy as np
from scipy.linalg import eigh
from sampler import Bits

HERE=Path(__file__).resolve().parent
M=64;L=16;U=4.;BETA=1.;J=.01;R=.7048643671236743
PHASES=(0.,math.pi/2);SAMPLES_PER_PHASE=32

class Node:
    def __init__(self,lo,hi,edges):
        self.lo=lo;self.hi=hi;self.n=hi-lo
        self.T=np.zeros((self.n,self.n))
        for i,j in edges:
            if lo<=i<j<hi:
                self.T[i-lo,i-lo]+=J;self.T[j-lo,j-lo]+=J
                self.T[i-lo,j-lo]+=J;self.T[j-lo,i-lo]+=J
        ev,V=eigh(self.T)
        assert ev.min()>-1e-14
        self.E=(V*np.exp(-BETA*ev/L))@V.T
        self.left=self.right=None;self.calls=self.attempts=0
        self.min_log_ratio=math.inf;self.max_log_ratio=-math.inf
        if self.n>1:
            mid=(lo+hi)//2
            self.left=Node(lo,mid,edges);self.right=Node(mid,hi,edges)
            cross=[(i,j) for i,j in edges if lo<=i<mid<=j<hi]
            self.cut_edges=cross;self.cut_trace=2*J*len(cross)
            cut=np.zeros_like(self.T)
            for i,j in cross:
                a=i-lo;b=j-lo
                cut[a,a]+=J;cut[b,b]+=J;cut[a,b]+=J;cut[b,a]+=J
            base=np.zeros_like(self.T);nl=self.left.n
            base[:nl,:nl]=self.left.T;base[nl:,nl:]=self.right.T
            assert np.max(abs(self.T-base-cut))<1e-14
            self.logC=2*R*BETA*self.cut_trace/(1-R)
        else:self.cut_edges=[];self.cut_trace=0.;self.logC=0.

def nodes(root):
    yield root
    if root.left:
        yield from nodes(root.left);yield from nodes(root.right)

class Conditional:
    def __init__(self,root,seed):
        self.root=root;self.rng=Bits(seed);self.leaf_proposals=0
        self.max_B_norm=0.;self.max_bridge_error=0.;self.max_bound_excess=0.
    def logg(self,B,phi):
        A=np.eye(len(B))-R*np.exp(1j*phi)*B
        if len(B)==1:return -2*math.log(abs(A[0,0]))
        # Uniformly SPD Gram; avoids spurious complex-slogdet FPE warnings
        # observed in the initial run, which is preserved separately.
        G=A.conj().T@A;C=np.linalg.cholesky((G+G.conj().T)/2)
        return -2*float(np.log(C.diagonal().real).sum())
    def sample(self,node,phi):
        node.calls+=1
        if node.n==1:
            while True:
                theta=math.sqrt(2*BETA*U)*self.rng.normal(1)[0]
                p=(1-R)**2/(1+R**2-2*R*math.cos(theta+phi))
                self.leaf_proposals+=1
                if self.rng.uniform(1)[0]<p:break
            xi=math.sqrt(2*BETA*U/L)*self.rng.normal(L)
            hist=(theta/L+xi-xi.mean()).reshape(1,L)
            self.max_bridge_error=max(self.max_bridge_error,abs(hist.sum()-theta))
            B=np.array([[np.exp(1j*hist.sum())]])
            return hist,B,self.logg(B,phi)
        while True:
            node.attempts+=1
            lh,lB,lg=self.sample(node.left,phi);rh,rB,rg=self.sample(node.right,phi)
            hist=np.concatenate((lh,rh));B=np.eye(node.n,dtype=complex)
            for l in range(L):B=node.E@(np.exp(1j*hist[:,l])[:,None]*B)
            log=self.logg(B,phi);ratio=log-lg-rg
            node.min_log_ratio=min(node.min_log_ratio,ratio);node.max_log_ratio=max(node.max_log_ratio,ratio)
            excess=max(abs(ratio)-node.logC,0.)
            self.max_bound_excess=max(self.max_bound_excess,excess)
            assert excess<1e-10
            if math.log(self.rng.uniform(1)[0])<ratio-node.logC:
                return hist,B,log

def main():
    start=time.perf_counter();edges=[(i,i+d) for i in range(M) for d in (1,2) if i+d<M]
    root=Node(0,M,edges);ns=list(nodes(root));setup=time.perf_counter()-start
    backend=Conditional(root,202610290802);saved=[];reports=[];sampling_start=time.perf_counter()
    for phi in PHASES:
        phase_start=time.perf_counter();diags=[];total_log=[]
        for _ in range(SAMPLES_PER_PHASE):
            hist,B,log=backend.sample(root,phi)
            saved.append(hist);diags.append(float(np.linalg.norm(B,2)));total_log.append(log)
        reports.append({'phi':phi,'samples':SAMPLES_PER_PHASE,'seconds':time.perf_counter()-phase_start,
             'max_operator_norm':max(diags),'mean_log_determinant_kernel_diagnostic':float(np.mean(total_log))})
    sampling=time.perf_counter()-sampling_start
    np.savez_compressed(HERE/'BOUNDED_CUT_HISTORIES.npz',histories=np.array(saved),phases=np.repeat(PHASES,SAMPLES_PER_PHASE))
    b=max(n.cut_trace for n in ns);C=math.exp(2*R*BETA*b/(1-R))
    whole_tau=float(np.trace(root.T));wholeC=math.exp(2*R*BETA*whole_tau/(1-R))
    out={'M':M,'K':'NOT_CONDITIONED','slices':L,'beta':BETA,'U':U,'bond_j':J,
       'edges':edges,'T_definition':'Sum j(|i>+|j>)(<i|+<j|), nearest+next-nearest open chain.',
       'total_trace':whole_tau,'max_cut_trace':b,'max_merge_envelope':C,
       'guaranteed_merge_acceptance_lower':C**-2,'binary_recurrence_exponent_bound':1+2*math.log(C)/math.log(2),
       'whole_system_envelope':wholeC,'whole_system_generic_acceptance_floor':wholeC**-2,
       'setup_seconds_after_imports':setup,'sampling_seconds_after_setup':sampling,
       'reports':reports,'native_recursion_calls':sum(n.calls for n in ns),'native_merge_attempts':sum(n.attempts for n in ns),
       'leaf_normal_proposals':backend.leaf_proposals,'normal_quantiles':backend.rng.normals,
       'raw64_words':backend.rng.words,'random_bits_from_seeded_PCG64':64*backend.rng.words,
       'max_bridge_sum_roundoff':backend.max_bridge_error,'max_determinant_bound_excess':backend.max_bound_excess,
       'nodes':[{'interval':[n.lo,n.hi],'calls':n.calls,'attempts':n.attempts,'cut_trace':n.cut_trace,
          'log_envelope':n.logC,'minimum_log_ratio':n.min_log_ratio if n.attempts else None,
          'maximum_log_ratio':n.max_log_ratio if n.attempts else None} for n in ns],
       'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'scope':'Seeded binary64 conditional-phi execution. No complete phase-normalizer FPRAS, canonical count, continuum bias, certified arithmetic, or practical advantage is acquired by this run.'}
    (HERE/'BOUNDED_CUT_EXECUTION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('nodes','edges')},indent=2))

if __name__=='__main__':main()
