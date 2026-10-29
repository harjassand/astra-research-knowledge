"""Globally correlated proposal, native noncommuting rank-one propagation.

Floating diagnostic consumer; exact rational setup is in INPUT.json.
The theorem concerns ideal fair bits and its specified high-precision version.
This run uses 52-bit midpoint inverse-normal variates and binary64 algebra.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,math,time
import numpy as np
from scipy.special import ndtri,logsumexp

HERE=Path(__file__).resolve().parent
N_PROPOSALS=32768  # Fixed before the first execution; no outcome-based stop.
SEED=202610290701

def frac(x):return F(int(x['numerator']),int(x['denominator']))
def fl(x):return float(frac(x))

class Bits:
    def __init__(self,seed):self.bg=np.random.PCG64(seed);self.words=0;self.normals=0
    def uniform(self,shape):
        n=math.prod(shape) if isinstance(shape,tuple) else shape
        self.words+=n
        raw=self.bg.random_raw(n)
        u=((raw>>12).astype(np.float64)+.5)*2.0**-52
        assert np.all((u>0)&(u<1))
        return u.reshape(shape) if isinstance(shape,tuple) else u
    def normal(self,shape):
        self.normals+=math.prod(shape) if isinstance(shape,tuple) else shape
        return ndtri(self.uniform(shape))

class Receiver:
    def __init__(self,x):
        self.x=x;self.M=x['M'];self.K=x['K_each_flavor'];self.L=x['slices']
        self.r=fl(x['r']);self.J=fl(x['J']);self.u=x['beta']*x['U']
        self.w=np.array(x['w'],float);self.w/=np.linalg.norm(self.w)
        self.a=np.expm1(-self.J/self.L)
        self.env=fl(x['determinant_envelope_upper'])
        self.Q=x['G0_trapezoid_points']
        self.circle=np.exp(2j*np.pi*np.arange(self.Q)/self.Q)
        self.d=np.arange(1,5)
        self.coeff=self.r**self.d*np.exp(-self.u*self.d**2)
        self.A0=1+2*np.sum(self.coeff)
        self.rng=Bits(SEED)
        self.phi_proposals=self.theta_proposals=0
        self.max_phase_sum_error=0.;self.max_trace_recurrence_disagreement=0.
        self.max_filter_violation=0.;self.max_operator_norm=0.
    def proposal(self,n):
        phi=[]
        while sum(len(x) for x in phi)<n:
            k=max(16,2*(n-sum(len(x) for x in phi)))
            p=2*np.pi*self.rng.uniform(k)-np.pi
            A=1+2*np.cos(p[:,None]*self.d)@self.coeff
            accept=np.exp(self.M*np.log(A/self.A0))
            good=self.rng.uniform(k)<accept
            phi.append(p[good]);self.phi_proposals+=k
        phi=np.concatenate(phi)[:n]  # All batch overruns were charged.
        theta=np.empty((n,self.M));left=np.arange(n*self.M)
        while len(left):
            z=math.sqrt(2*self.u)*self.rng.normal(len(left))
            pp=phi[left//self.M]
            a=(1-self.r)**2/(1+self.r**2-2*self.r*np.cos(pp+z))
            good=self.rng.uniform(len(left))<a
            theta.ravel()[left[good]]=z[good]
            self.theta_proposals+=len(left);left=left[~good]
        noise=math.sqrt(2*self.u/self.L)*self.rng.normal((n,self.M,self.L))
        histories=theta[:,:,None]/self.L+noise-noise.mean(axis=2)[:,:,None]
        self.max_phase_sum_error=max(self.max_phase_sum_error,float(np.max(abs(histories.sum(axis=2)-theta))))
        return theta,histories
    def propagate(self,hist):
        n=len(hist);B=np.broadcast_to(np.eye(self.M,dtype=complex),(n,self.M,self.M)).copy()
        for l in range(self.L):
            B*=np.exp(1j*hist[:,:,l])[:,:,None]
            row=np.einsum('i,bij->bj',self.w,B,optimize=False)
            B+=self.a*self.w[None,:,None]*row[:,None,:]
        return B
    def character(self,values):
        n=len(values);h=np.zeros((n,self.K+1),complex);h[:,0]=1
        powers=np.ones_like(values);p=np.zeros((n,self.K+1),complex)
        for j in range(1,self.K+1):powers*=self.r*values;p[:,j]=powers.sum(axis=1)
        for j in range(1,self.K+1):h[:,j]=np.sum(p[:,1:j+1]*h[:,j-1::-1],axis=1)/j
        return h[:,-1]
    def log_G0(self,theta):
        out=np.empty(len(theta))
        for k,row in enumerate(np.exp(1j*theta)):
            denom=1+self.r**2-2*self.r*(row[:,None]*self.circle[None,:]).real
            logf=-np.log(denom).sum(axis=0)
            out[k]=logsumexp(logf)-math.log(self.Q)
        return out

def free_ratio(M,K,J):
    D=math.comb(M+K-1,K)
    z=sum(math.exp(-J*n)*math.comb(M+K-n-2,K-n) for n in range(K+1))
    return (z/D)**2

def main():
    x=json.loads((HERE/'INPUT.json').read_text());r=Receiver(x)
    p0lo,p0hi=fl(x['pK_zero_lower']),fl(x['pK_zero_upper']);p0=(p0lo+p0hi)/2
    c=math.exp(-2*r.J*r.K/r.M)
    batch=32;f=[],[]
    vals=[];bases=[];cv=[];accepted=[];checks=[]
    rng_accepts=0;timing={'proposal':0.,'propagation_character':0.,'G0':0.}
    start=time.perf_counter()
    for b in range(0,N_PROPOSALS,batch):
        n=min(batch,N_PROPOSALS-b);z=time.perf_counter();theta,hist=r.proposal(n);timing['proposal']+=time.perf_counter()-z
        z=time.perf_counter();B=r.propagate(hist)
        ev=np.linalg.eigvals(B);hc=r.character(ev);h0=r.character(np.exp(1j*theta))
        if b==0:
            for j in range(3):
                tracep=[0j];power=np.eye(r.M,dtype=complex)
                for k in range(1,r.K+1):power=power@(r.r*B[j]);tracep.append(np.trace(power))
                hh=[1+0j]
                for k in range(1,r.K+1):hh.append(sum(tracep[t]*hh[k-t] for t in range(1,k+1))/k)
                err=abs(hh[-1]-hc[j])/max(1,abs(hh[-1]))
                r.max_trace_recurrence_disagreement=max(r.max_trace_recurrence_disagreement,float(err))
                r.max_operator_norm=max(r.max_operator_norm,float(np.linalg.norm(B[j],2)))
        timing['propagation_character']+=time.perf_counter()-z
        z=time.perf_counter();lg=r.log_G0(theta);timing['G0']+=time.perf_counter()-z
        v=np.exp(2*np.log(abs(hc))-lg);v0=np.exp(2*np.log(abs(h0))-lg)
        r.max_filter_violation=max(r.max_filter_violation,float(np.max(v/r.env-1)),float(np.max(v0-1)))
        assert np.all(v>=0) and np.max(v)<=r.env*(1+1e-10)
        assert np.all(v0>=0) and np.max(v0)<=1+1e-10
        vals.extend(v.tolist());bases.extend(v0.tolist());cv.extend(((v-c*v0+c)/(r.env+c)).tolist())
        mask=r.rng.uniform(n)<v/r.env
        rng_accepts+=int(mask.sum());accepted.extend(hist[mask])
        if b%4096==0:print(json.dumps({'completed':b+n,'seconds':time.perf_counter()-start,'accepts':rng_accepts}),flush=True)
    elapsed=time.perf_counter()-start
    vals=np.array(vals);bases=np.array(bases);cv=np.array(cv)
    variance=float(np.var(cv,ddof=1));log=math.log(4/.05)
    rad=math.sqrt(2*variance*log/N_PROPOSALS)+7*log/(3*(N_PROPOSALS-1))
    low=(r.env+c)*(float(cv.mean())-rad)-c+c*p0lo
    high=(r.env+c)*(float(cv.mean())+rad)-c+c*p0hi
    lower_ratio=max(0,low/p0hi);upper_ratio=high/p0lo
    est=(float(vals.mean())-c*(float(bases.mean())-p0))/p0
    control=free_ratio(r.M,r.K,r.J)
    np.savez_compressed(HERE/'ACCEPTED_HISTORIES.npz',histories=np.array(accepted),r=r.r,w=r.w,J=r.J)
    out={'source_sha256':hashlib.sha256((HERE/'INPUT.json').read_bytes()).hexdigest(),
      'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'predeclared_proposals':N_PROPOSALS,'seed':SEED,'M':r.M,'K_each':r.K,'slices':r.L,
      'mean_target_grand_filter':float(vals.mean()),'mean_base_grand_filter':float(bases.mean()),
      'base_filter_exact_interval':[p0lo,p0hi],'raw_partition_ratio':float(vals.mean()/p0),
      'fixed_CV_coefficient':c,'CV_partition_ratio':est,'CV_free_energy_shift':-math.log(est),
      'CV_unit_interval_sample_variance':variance,'ideal_95_EB_unit_radius':rad,
      'ideal_95_partition_ratio_interval':[lower_ratio,upper_ratio],
      'ideal_95_free_energy_shift_interval':[-math.log(upper_ratio),-math.log(lower_ratio)] if lower_ratio>0 else None,
      'same_T_noninteracting_canonical_ratio':control,'same_T_noninteracting_free_energy_shift':-math.log(control),
      'accepted_iid_histories':rng_accepts,'observed_acceptance':rng_accepts/N_PROPOSALS,
      'certified_ideal_acceptance_lower':fl(x['final_acceptance_lower']),
      'common_phase_proposals_including_batch_overrun':r.phi_proposals,
      'total_phase_Gaussian_proposals':r.theta_proposals,'normal_quantiles':r.rng.normals,
      'raw64_words':r.rng.words,'random_bits_from_seeded_PCG64':64*r.rng.words,
      'M_by_M_matrices_per_proposal':1,'native_state_dimension_not_stored':x.get('full_sector_state_count','D64^2~1.434e74'),
      'G0_points':r.Q,'ideal_uniform_trapezoid_absolute_error':2**-40,
      'max_Gaussian_bridge_sum_roundoff':r.max_phase_sum_error,
      'independent_trace_recurrence_relative_disagreement':r.max_trace_recurrence_disagreement,
      'sampled_operator_norm':r.max_operator_norm,'max_filter_bound_violation':r.max_filter_violation,
      'seconds_after_imports':elapsed,'timing':timing,
      'scope':'Finite seeded binary64 / 52-bit midpoint inverse-normal diagnostic. The EB interval concerns the ideal iid variable, not a certified bound on this floating/RNG implementation. No continuum bias, microscopic material, MCMC speed advantage, or generic extensive-band efficiency is asserted.'}
    (HERE/'EXECUTION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
