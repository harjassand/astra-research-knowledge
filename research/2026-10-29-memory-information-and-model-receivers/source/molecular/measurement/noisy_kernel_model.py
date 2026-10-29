"""UNEXECUTED exploratory Lindblad scenario library; NOT a noise acquisition.
Computational adjoint evolution is not a physical reversed Hamiltonian.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.linalg import eigh
from scipy.integrate import solve_ivp
from scipy.sparse import csr_matrix
from scipy.special import eval_genlaguerre
from parking_preview import model,sequence
from history_kernel_consumer import enc,bound
HERE=Path(__file__).resolve().parent

class NativeModel:
    def __init__(self,magnetic_fraction,extra_ground_rate,N=100,rtol=1e-7):
        assert 0<=magnetic_fraction<=1 and extra_ground_rate>=0
        self.scenario={'magnetic_fraction':magnetic_fraction,'extra_ground_rate':extra_ground_rate,
          'status':'EXPLICIT_ASSUMPTION_NOT_IDENTIFIED_BY_PUBLISHED_OPTICAL_T2'}
        self.N=N;self.rtol=rtol
        self.w,self.eta,self.g,self.D,self.packets,self.code=model(N)
        n=np.arange(N-1)
        c=np.exp(-self.eta**2/2)/np.sqrt(n+1)*eval_genlaguerre(n,1,self.eta**2)
        ad=np.diag(c,-1);self.p=csr_matrix(1j*(ad-ad.T))
        rows,cols=np.indices((N,N));Db=np.where(abs(rows-cols)<=14,self.D,0)
        self.Dcut_fro=float(np.linalg.norm(Db-self.D,'fro'));self.ds=[]
        for a in [Db,Db.conj().T]:
            c=csr_matrix(a);rr=np.repeat(np.arange(N),np.diff(c.indptr))
            self.ds.append((c.data,c.indices,c.indptr,self.w*(rr-c.indices)))
        self.Tspin=2.84821251e-3;self.Tmotion=83009.6233e-6
        spin=np.repeat(np.array([-1.,1.,-3.]),N);num=np.tile(np.arange(N),3)
        laser=np.repeat(np.array([1.,1.,-1.]),N);tag=np.repeat([0.,1.,0.],N)
        self.deph=-magnetic_fraction*(spin[:,None]-spin[None,:])**2/(4*self.Tspin)
        self.deph-=(1-magnetic_fraction)*(laser[:,None]-laser[None,:])**2/(4*self.Tspin)
        self.deph-=extra_ground_rate*(tag[:,None]-tag[None,:])**2
        self.deph-=(num[:,None]-num[None,:])**2/self.Tmotion
        self.evals=0;self.segments=[]

    def optical_segments(self,start,theta,inverse=False,phase0=0.,gref=None,bb1=True):
        if gref is None:gref=self.g[42]
        seq=sequence(theta,bb1)
        if inverse:seq=[(a,p+np.pi) for a,p in seq[::-1]]
        out=[]
        for angle,phase in seq:
            dur=2*angle/(2*np.pi*85e3*gref)
            out.append(dict(kind='opt',start=start,duration=dur,phase=phase+phase0))
            start+=dur
        return out,start

    def phased_D(self,t,which):
        data,indices,indptr,freq=self.ds[which]
        return csr_matrix((data*np.exp(1j*freq*t),indices,indptr),shape=(self.N,self.N))

    def propagate(self,rho,seg,adjoint=False):
        N=self.N;duration=seg['duration'];start=time.perf_counter()
        if seg['kind']=='idle':
            return rho*np.exp(duration*self.deph)
        def rhs(u,flat):
            rr=flat.reshape(3*N,3*N)
            t=duration-u if adjoint else u
            left=np.zeros_like(rr)
            if seg['kind']=='opt':
                amp=np.pi*85e3*np.sin(np.pi*t/duration)**2
                D=self.phased_D(seg['start']+t,0);Dc=self.phased_D(seg['start']+t,1)
                left[:N]=amp*np.exp(1j*seg['phase'])*(D@rr[2*N:])
                left[2*N:]=amp*np.exp(-1j*seg['phase'])*(Dc@rr[:N])
            elif seg['kind']=='cat':
                amp=seg['sign']*2*np.pi*.145e6*self.eta/2
                left[:N]=amp*(self.p@rr[2*N:]);left[2*N:]=amp*(self.p@rr[:N])
            elif seg['kind']=='rf':
                amp=np.pi/(2*duration)*seg['sign']
                left[:N]=amp*rr[N:2*N];left[N:2*N]=amp*rr[:N]
            else:raise ValueError(seg)
            # rho/O remain Hermitian, so (H*rho)^dagger=rho*H.
            comm=left-left.conj().T
            return ((1j if adjoint else -1j)*comm+self.deph*rr).reshape(-1)
        sol=solve_ivp(rhs,(0,duration),rho.reshape(-1),method='DOP853',
          rtol=self.rtol,atol=self.rtol/100,t_eval=[duration],
          max_step=(2*np.pi/self.w/6 if seg['kind']=='opt' else duration/20))
        assert sol.success
        ans=sol.y[:,-1].reshape(3*N,3*N);ans=(ans+ans.conj().T)/2
        self.evals+=sol.nfev
        self.segments.append({'kind':seg['kind'],'adjoint':adjoint,'duration_s':duration,
          'rhs_evaluations':sol.nfev,'wall_seconds':time.perf_counter()-start})
        return ans
