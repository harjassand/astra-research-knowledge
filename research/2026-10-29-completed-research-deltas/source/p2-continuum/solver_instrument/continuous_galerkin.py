#!/usr/bin/env python3
"""Finite-duration qubit/continuum sine dynamics with full-space residual.

This is an a posteriori diagnostic, not interval-certified numerics. The bath
kernel is analytic and positive-frequency. No Fock or frequency grid is used.
"""
import hashlib,itertools,json,math,time
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eigh

OUT=Path(__file__).parent
X=np.array([[0,1],[1,0]],complex)
YPAULI=np.array([[0,-1j],[1j,0]],complex)

def herm(a):return (a+a.conj().T)/2

def corr(t,u,v=2.1):
    return v/(1-1j*(np.asarray(u)-np.asarray(t)))

class Basis:
    def __init__(self,nodes,K,eig_cut=1e-10,v=2.1):
        self.nodes=np.array(nodes,float);self.v=v;self.K=K
        self.labels=np.array(list(itertools.product(range(-K,K+1),repeat=len(nodes))),float)
        self.C=corr(self.nodes[:,None],self.nodes[None,:],v)
        inner=self.labels@self.C@self.labels.T
        norm=inner.diagonal().real
        self.G=np.exp(-.5*(norm[:,None]+norm[None,:])+inner)
        zero=int(np.flatnonzero(np.all(self.labels==0,axis=1))[0])
        other=np.delete(np.arange(len(norm)),zero)
        g0=self.G[zero,other]
        reduced=herm(self.G[np.ix_(other,other)]-np.outer(g0.conj(),g0))
        val,vec=eigh(reduced)
        keep=val>eig_cut*max(1.,val[-1]);w=vec[:,keep]/np.sqrt(val[keep])
        self.R=np.zeros((len(norm),1+sum(keep)),complex);self.R[zero,0]=1
        self.R[other,1:]=w;self.R[zero,1:]=-g0@w
        self.rank=self.R.shape[1]
        self.stats={'packets':len(norm),'rank':self.rank,'nodes':list(nodes),'K':K,
            'eig_cut':eig_cut,'minimum_retained_residual_gram_eigenvalue':float(val[keep][0]),
            'retained_residual_gram_condition':float(val[keep][-1]/val[keep][0]),
            'raw_gram_min_eigenvalue_float':float(np.linalg.eigvalsh(herm(self.G))[0]),
            'basis_orthonormality_defect':float(np.linalg.norm(self.R.conj().T@self.G@self.R-np.eye(self.rank),2)),
            'initial_vacuum_retained_exactly_in_symbolic_construction':True}
    def vertex(self,t,power):
        c=corr(self.nodes,t,self.v)
        l=self.labels@c
        return self.G*np.exp(-.5*power*power*self.v+power*(l[:,None]-l.conj()[None,:]))
    def moments(self,t):
        # W(+q)=D(i q f_t). Sine and sine squared are evaluated in the full bath.
        wp=self.vertex(t,1);wm=self.vertex(t,-1)
        sine=(wp-wm)/(2j)
        square=.5*self.G-.25*(self.vertex(t,2)+self.vertex(t,-2))
        b=self.R.conj().T@sine@self.R
        b2=self.R.conj().T@square@self.R
        return herm(b),herm(b2)
    def cross(self,other):
        C=corr(self.nodes[:,None],other.nodes[None,:],self.v)
        ab=self.labels@C@other.labels.T
        aa=(self.labels@self.C*self.labels).sum(axis=1).real
        bb=(other.labels@other.C*other.labels).sum(axis=1).real
        g=np.exp(-.5*(aa[:,None]+bb[None,:])+ab)
        return self.R.conj().T@g@other.R

def amplitude(t,T,Apeak):return Apeak*np.sin(np.pi*t/T)**2

def source(t):return np.cos(t)*X+np.sin(t)*YPAULI

def apply_product(S,B,state):
    shaped=state.reshape(2,B.shape[0],-1)
    return np.einsum('ab,ij,bjk->aik',S,B,shaped,optimize=True).reshape(state.shape)

def run(nodes,K,T=.6,Apeak=12.,steps=80,quad_order=4,eig_cut=1e-10,label=None):
    start=time.time();basis=Basis(nodes,K,eig_cut);r=basis.rank
    state=np.zeros((2*r,2),complex);state[0,0]=1;state[r,1]=1
    x,w=leggauss(quad_order);dt=T/steps
    integral=0.;basis_integral=0.;freeze_integral=0.
    min_res=0.;min_basis_res=0.;max_res=0.;isometry_drift=0.
    samples=[]
    for step in range(steps):
        left=step*dt;mid=left+dt/2
        bm,_=basis.moments(mid);am=amplitude(mid,T,Apeak)
        hmid=am*np.kron(source(mid),bm)
        lam,vec=eigh(hmid);co=vec.conj().T@state
        for xx,ww in zip(x,w):
            tm=left+dt*(xx+1)/2
            sy=vec@(np.exp(-1j*(tm-left)*lam)[:,None]*co)
            b,b2=basis.moments(tm);aa=amplitude(tm,T,Apeak)
            hy=aa*apply_product(source(tm),b,sy)
            my=vec@(lam[:,None]*np.exp(-1j*(tm-left)*lam)[:,None]*co)
            h2y=aa*aa*apply_product(np.eye(2),b2,sy)
            # ||(H_full Q-Q Hmid)Y||² on the complete input code.
            residual=herm(sy.conj().T@h2y-hy.conj().T@my-my.conj().T@hy+my.conj().T@my)
            ev=np.linalg.eigvalsh(residual);min_res=min(min_res,float(ev[0]))
            rn=float(np.sqrt(max(0.,ev[-1])));max_res=max(max_res,rn)
            br=herm(sy.conj().T@h2y-hy.conj().T@hy)
            bev=np.linalg.eigvalsh(br);min_basis_res=min(min_basis_res,float(bev[0]))
            bn=float(np.sqrt(max(0.,bev[-1])))
            diff=hy-my;fn=float(np.sqrt(max(0.,np.linalg.eigvalsh(herm(diff.conj().T@diff))[-1])))
            integral+=dt*ww*rn/2;basis_integral+=dt*ww*bn/2;freeze_integral+=dt*ww*fn/2
            samples.append([float(tm),rn,bn,fn,float(ev[0])])
        state=vec@(np.exp(-1j*dt*lam)[:,None]*co)
        isometry_drift=max(isometry_drift,float(np.linalg.norm(state.conj().T@state-np.eye(2),2)))
    # Explicit positivity checks of the full projected exterior-basis form.
    exterior=[]
    for tm in np.linspace(0,T,9):
        b,b2=basis.moments(tm);ex=herm(b2-b@b)
        exterior.append([float(tm),float(np.linalg.eigvalsh(ex)[0]),float(np.linalg.eigvalsh(ex)[-1])])
    rec={'label':label,'model':{'rho':'2.1 exp(-omega), omega>=0','T':T,'Apeak':Apeak,
           'A':'Apeak sin²(pi t/T)','action':Apeak*T/2,'S':'cos(t) X + sin(t) Y'},
         'basis':basis.stats,'steps':steps,'quadrature_order':quad_order,
         'residual_integral_diagnostic':integral,
         'basis_residual_integral_diagnostic':basis_integral,
         'time_freeze_residual_integral_diagnostic':freeze_integral,
         'residual_squared_min_input_eigenvalue':min_res,
         'basis_residual_squared_min_input_eigenvalue':min_basis_res,
         'maximum_residual_norm':max_res,'finite_coordinate_isometry_drift':isometry_drift,
         'full_basis_exterior_eigenvalue_checks':exterior,
         'runtime_seconds':time.time()-start,
         'scope':'Actual finite smooth waveform and all-bath residual; floating arithmetic and time quadrature remain uncertified.',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if label:
        np.savez_compressed(OUT/(label+'.npz'),state=state,R=basis.R,labels=basis.labels,nodes=basis.nodes,G=basis.G,samples=np.array(samples))
    return rec,basis,state

def compare(b1,y1,b2,y2):
    cross=np.kron(np.eye(2),b1.cross(b2))
    z=y1.conj().T@cross@y2
    ev=np.linalg.eigvalsh(herm(2*np.eye(2)-z-z.conj().T))
    return {'complete_input_endpoint_distance_float':float(np.sqrt(max(0.,ev[-1]))),
            'squared_distance_eigenvalues_float':ev.tolist()}

if __name__=='__main__':
    configs=[('continuous_two_K1', [0.,.6],1,80),('continuous_two_K2',[0.,.6],2,80),
             ('continuous_two_K3',[0.,.6],3,80),('continuous_two_K4',[0.,.6],4,80),
             ('continuous_three_K1',[0.,.3,.6],1,80),('continuous_three_K2',[0.,.3,.6],2,80)]
    runs=[]
    for label,nodes,K,steps in configs:
        rec,b,y=run(nodes,K,steps=steps,label=label);runs.append((rec,b,y))
        print(label,'rank',b.rank,'integral',rec['residual_integral_diagnostic'],'basis',rec['basis_residual_integral_diagnostic'],'time',rec['time_freeze_residual_integral_diagnostic'],flush=True)
        (OUT/(label+'_receipt.json')).write_text(json.dumps(rec,indent=2)+'\n')
    comparisons=[]
    for i in range(len(runs)):
        for j in range(i+1,len(runs)):
            comparisons.append({'a':runs[i][0]['label'],'b':runs[j][0]['label'],**compare(runs[i][1],runs[i][2],runs[j][1],runs[j][2])})
    summary={'runs':[r[0] for r in runs],'comparisons':comparisons}
    (OUT/'continuous_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
