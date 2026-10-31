"""Joint finite-time Gaussian cat/parity-meter instrument with faulty CD.

Six quantum modes, all three physical output channels, hot independent helper
noise, desired nu=.2 quadratic H3, ALL six lower-weight annihilation drives,
16 physical counterrotations, proportional and optional branch-dependent CD.
Cross blocks include covariance changes, residual gauge and emitted field.
One integrated homodyne record yields an actual noisy binary instrument.
"""
from pathlib import Path
import argparse,itertools,json,time
import numpy as np
from scipy.special import erfc
from gaussian_cross_engine import symplectic,cross_rhs


def enc(x):
    a=np.asarray(x)
    if np.iscomplexobj(a):return {'real':a.real.tolist(),'imag':a.imag.tolist()}
    return a.tolist()


class Model:
    def __init__(self,modulated=True,odd=0.,phase_kind='common',cycles=16,steps_per_segment=32):
        self.modulated=modulated;self.odd=odd;self.phase_kind=phase_kind
        self.n=16.;self.alpha=4.;self.G=1.;self.gamma=10.;self.heat=.01;self.nu=.2
        self.g2=self.G/(2*self.alpha);self.g3=self.nu*self.G**2/(self.gamma*self.alpha)
        self.kappa2=4*self.g2**2/self.gamma;self.kconf=2*self.G**2/self.gamma
        self.delta=50*self.kconf;self.eps_common=.01;self.u=.01;self.eta=.5
        self.segment=np.pi/self.delta;self.cycle=16*self.segment
        self.cycles=cycles;self.drive_time=cycles*self.cycle;self.ringdown=60.
        self.dt=self.segment/steps_per_segment;self.steps_per_segment=steps_per_segment
        self.z=np.array(list(itertools.product((1.,-1.),repeat=3)))
        self.S=np.prod(self.z,axis=1)
        self.Rs=[(0,),(1,),(2,),(0,1),(0,2),(1,2)]
        self.phases=np.zeros(6) if phase_kind=='common' else np.array([.3,1.7,-2.2,.9,-.6,2.6])
        self.labels=list('ABABBABA')+list('ABABBABA')[::-1]
        self.signs=np.r_[np.ones(8),-np.ones(8)]
        dirs={'A':np.array([1.,-1.,0.]),'B':np.array([1.,0.,-1.])}
        self.dirs=np.array([s*dirs[l] for l,s in zip(self.labels,self.signs)])
        self.starts=np.vstack((np.zeros(3),np.cumsum(np.pi*self.dirs,axis=0)))[:-1]
        self.pairs=list(itertools.combinations_with_replacement(range(8),2))
        self.il=np.array([i for i,j in self.pairs]);self.ir=np.array([j for i,j in self.pairs])
        self.diag=np.array([self.pairs.index((i,i)) for i in range(8)])
        self.np=len(self.pairs);self.dim=13
        self.O=np.zeros((13,13));self.O[:12,:12]=symplectic(6)
        self.baseG=np.zeros((13,13))
        for j in range(3):
            for q in (0,1):self.baseG[2*j+q,6+2*j+q]=self.baseG[6+2*j+q,2*j+q]=self.G
        self.Q=np.zeros((2*self.np,13,13));self.qc=np.zeros(2*self.np)
        for j in range(6,12):self.Q[self.np:,j,j]=self.gamma
        self.qc[self.np:]=-3*self.gamma/2

    def phases_at(self,t):
        if not self.modulated or t>=self.drive_time:return np.zeros(3),np.zeros(3)
        pos=(t%self.cycle)/self.segment
        j=min(int(pos),15); frac=pos-j
        return self.starts[j]+frac*np.pi*self.dirs[j],self.delta*self.dirs[j]

    def matrices(self,t):
        on=t<self.drive_time
        th,dth=self.phases_at(t)
        G=np.broadcast_to(self.baseG,(8,13,13)).copy()
        d=np.zeros((8,13));h=np.zeros(8)
        if on:
            # State-dependent error is an explicit odd, phase-tracking actuator
            # contamination. It is NOT ordinary physical number-detuning noise.
            deterr=dth[None,:]*(self.eps_common+self.odd*self.z)
            for j in range(3):
                G[:,2*j,2*j]+=deterr[:,j];G[:,2*j+1,2*j+1]+=deterr[:,j]
                d[:,2*j]+=np.sqrt(2)*self.alpha*deterr[:,j]
                h+=deterr[:,j]*(self.n-.5)
            for j in range(3):d[:,2*j]+=np.sqrt(2)*self.g3*self.n*self.S
            h+=2*self.g3*self.alpha**3*self.S
            for j,k in itertools.combinations(range(3),2):
                f=self.g3*self.alpha*self.S
                G[:,2*j,2*k]+=f;G[:,2*k,2*j]+=f
                G[:,2*j+1,2*k+1]-=f;G[:,2*k+1,2*j+1]-=f
            for R,phi in zip(self.Rs,self.phases):
                r=len(R);zr=np.prod(self.z[:,R],axis=1)
                eps=self.u*self.g3*self.alpha**(3-r)
                angle=np.sum(th[list(R)])-phi
                co,si=np.cos(angle),np.sin(angle)
                h+=2*eps*self.alpha**r*co*zr
                for j in R:
                    d[:,2*j]+=np.sqrt(2)*eps*self.alpha**(r-1)*co*zr
                    d[:,2*j+1]+=np.sqrt(2)*eps*self.alpha**(r-1)*si*zr
                if r==2:
                    j,k=R
                    for a,b,val in [(2*j,2*k,co),(2*j+1,2*k+1,-co),
                                    (2*j,2*k+1,si),(2*j+1,2*k,si)]:
                        G[:,a,b]+=eps*val*zr;G[:,b,a]+=eps*val*zr
        A=np.zeros((2*self.np,13,13));D=np.zeros_like(A)
        for j in range(6,12):
            A[:self.np,j,j]=(-self.gamma+self.heat)/2
            D[:self.np,j,j]=(self.gamma+self.heat)/2
            A[self.np:,j,j]=self.heat/2
            D[self.np:,j,j]=self.heat/2
        # Sum homodyne, with a decaying post-pulse collection weight. All other
        # output modes remain in the Lindbladian and are traced, not discarded.
        # The real buffer displacement is negative for S=+1; choose homodyne
        # phase pi so a positive collected record reports positive parity.
        weight=-1. if on else -np.exp(-self.kconf*(t-self.drive_time))
        for j in range(3):
            c=weight*np.sqrt(2*self.eta*self.gamma/3)
            cross=-weight*np.sqrt(self.eta*self.gamma/6)
            A[:self.np,12,6+2*j]=c
            D[:self.np,12,6+2*j]=cross;D[:self.np,6+2*j,12]=cross
        D[:self.np,12,12]=weight*weight
        il=np.r_[self.il,self.il];ir=np.r_[self.ir,self.ir]
        return G[il],G[ir],d[il],d[ir],h[il],h[ir],A,D

    def rhs(self,t,V,m,l):
        G1,G2,d1,d2,h1,h2,A,D=self.matrices(t)
        return cross_rhs(V,m,l,G1,G2,d1,d2,h1,h2,self.O,A,D,self.Q,self.qc)


def full_matrix(vals,pairs):
    W=np.zeros((8,8),complex)
    for a,(i,j) in zip(vals,pairs):W[i,j]=a;W[j,i]=np.conj(a)
    return W


def gate_choi(instruments,qx=0.,qprep=0.,return_branches=False):
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1])
    plus=np.array([1,1])/np.sqrt(2);minus=np.array([1,-1])/np.sqrt(2)
    prep=np.kron(np.eye(4),plus[:,None])
    out=np.zeros((16,16),complex)
    branch_out={(s,m):np.zeros((16,16),complex) for s in (1,-1) for m in (1,-1)}
    ancilla_z=np.tile([1.,-1.],4)
    prep_noise=(1-qprep)+qprep*ancilla_z[:,None]*ancilla_z[None,:]
    for i,j in itertools.product(range(4),repeat=2):
        rho=np.outer(prep[:,i],prep[:,j].conj())*prep_noise
        rout=np.zeros((4,4),complex)
        for s,W in zip((1,-1),instruments):
            r=rho*W
            for m,bra in ((1,plus),(-1,minus)):
                B=np.kron(np.kron(I,bra[None,:]),I)
                rr=B@r@B.conj().T
                for reported,prob in ((m,1-qx),(-m,qx)):
                    correction=np.kron(Z if reported==-1 else I,Z if reported==-1 else I)@\
                               np.kron(I,X if s==-1 else I)
                    piece=prob*correction@rr@correction.conj().T
                    rout+=piece
                    branch_out[s,reported][i*4:(i+1)*4,j*4:(j+1)*4]+=piece/4
        out[i*4:(i+1)*4,j*4:(j+1)*4]=rout/4
    U=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    ideal=U.reshape(-1,order='F')/2
    result=(out,float(1-np.real(ideal.conj()@out@ideal)))
    return (*result,branch_out) if return_branches else result


def run(model,label):
    npair=2*model.np;d=model.dim
    V=np.zeros((npair,d,d),complex)
    V[:,:12,:12]=(.5+.001)*np.eye(12)
    m=np.zeros((npair,d),complex);l=np.zeros(npair,complex)
    exposure=np.zeros((8,3));maxg=np.zeros((8,3));maxvar=0.
    snapshots=[];t=0.;count=0
    stop=model.drive_time+model.ringdown
    start=time.monotonic()
    while t<stop-1e-11:
        # Every winding boundary is an integration boundary.
        if t<model.drive_time-1e-10:
            boundary=min(model.drive_time,(np.floor((t+1e-9)/model.segment)+1)*model.segment)
        else:boundary=stop
        dt=min(model.dt,boundary-t,stop-t)
        if dt<1e-10:t=boundary;continue
        # Endpoint values stay on the current side of a piecewise control jump.
        k1=model.rhs(t+1e-10,V,m,l)
        k2=model.rhs(t+dt/2,V+dt*k1[0]/2,m+dt*k1[1]/2,l+dt*k1[2]/2)
        k3=model.rhs(t+dt/2,V+dt*k2[0]/2,m+dt*k2[1]/2,l+dt*k2[2]/2)
        k4=model.rhs(t+dt-1e-10,V+dt*k3[0],m+dt*k3[1],l+dt*k3[2])
        V+=dt*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6
        m+=dt*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6
        l+=dt*(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6
        V=(V+V.swapaxes(-1,-2))/2
        t+=dt;count+=1
        md=m[model.diag,:12].real;vd=V[model.diag,:12,:12].real
        gp=np.array([.5*(vd[:,2*j,2*j]+vd[:,2*j+1,2*j+1]+md[:,2*j]**2+md[:,2*j+1]**2-1)
                     for j in range(3)]).T
        maxg=np.maximum(maxg,gp)
        actual=model.n+np.sqrt(2)*model.alpha*md[:,::2][:,:3]+gp
        exposure+=dt*actual
        if count%max(model.steps_per_segment*4,1)==0 or t>=stop-1e-10:
            snapshots.append({'time':t,'mean':md.tolist(),'covariance':vd.tolist()})
    w=np.exp(l[:model.np]);w0=np.exp(l[model.np:])
    yp=m[:model.np,12];yv=V[:model.np,12,12]
    plus=w*.5*erfc(-yp/np.sqrt(2*yv));minus=w-plus
    W=full_matrix(w,model.pairs);Wp=full_matrix(plus,model.pairs);Wm=full_matrix(minus,model.pairs)
    W0=full_matrix(w0,model.pairs)
    J,infid=gate_choi([Wp,Wm]);_,infid_x=gate_choi([Wp,Wm],qx=.001)
    q=np.array([Wm[i,i].real if model.S[i]>0 else Wp[i,i].real for i in range(8)])
    sectors={}
    for S in (-1,1):
        ix=np.flatnonzero(model.S==S);s=W[np.ix_(ix,ix)]
        sectors[str(S)]={'raw_entanglement_infidelity':float(1-np.real(np.sum(s))/16),
                        'max_pair_visibility_loss':float(np.max(1-abs(s))),
                        'minimum_pair_visibility':float(np.min(abs(s)))}
    out={'label':label,'scope':'Exact quadratic Gaussian instrument; nonlinear oscillator remainders not certified.',
         'parameters':{k:getattr(model,k) for k in ('n','G','gamma','heat','nu','g2','g3','kappa2','kconf','delta','eps_common','odd','u','eta','cycles','drive_time','ringdown','dt','modulated','phase_kind')},
         'runtime_seconds':time.monotonic()-start,'steps':count,
         'logical_Gram':enc(W),'reported_plus_instrument':enc(Wp),'reported_minus_instrument':enc(Wm),
         'no_click_Gram':enc(W0),'gate_Choi':enc(J),
         'CNOT_entanglement_infidelity':infid,'CNOT_entanglement_infidelity_with_0p1percent_X_readout_error':infid_x,
         'parity_assignment_error_by_branch':q.tolist(),'max_parity_assignment_error':float(np.max(q)),
         'within_parity_sectors':sectors,
         'instrument_min_eigenvalue':float(min(np.linalg.eigvalsh(Wp).min(),np.linalg.eigvalsh(Wm).min())),
         'no_click_min_eigenvalue':float(np.linalg.eigvalsh(W0).min()),
         'Choi_trace':float(np.real(np.trace(J))),'Choi_min_eigenvalue':float(np.linalg.eigvalsh(J).min()),
         'final_diagonal_logical_weights':np.diag(W).real.tolist(),
         'no_click_probabilities':np.diag(W0).real.tolist(),
         'final_gauge_means':m[model.diag,:12].real.tolist(),
         'final_gauge_covariances':V[model.diag,:12,:12].real.tolist(),
         'final_cross_gauge_means':enc(m[:model.np,:12]),
         'final_cross_gauge_covariances':enc(V[:model.np,:12,:12]),
         'cross_pair_order':model.pairs,
         'final_record_means':m[model.diag,12].real.tolist(),'final_record_variances':V[model.diag,12,12].real.tolist(),
         'max_single_storage_gauge_population_by_branch':maxg.tolist(),
         'photon_exposure_by_branch_and_storage':exposure.tolist(),
         'max_total_photon_exposure':float(exposure.sum(axis=1).max()),
         'storage_loss_probability_bound_for_kappa1_over_kappa2_1e_minus4':float(exposure.sum(axis=1).max()*model.kappa2*1e-4),
         'snapshot_count':len(snapshots)}
    folder=Path(__file__).parent
    (folder/f'joint_{label}_results.json').write_text(json.dumps(out,indent=2)+'\n')
    (folder/f'joint_{label}_moments.json').write_text(json.dumps({'snapshots':snapshots})+'\n')
    print(json.dumps({k:out[k] for k in ('label','runtime_seconds','steps','CNOT_entanglement_infidelity','CNOT_entanglement_infidelity_with_0p1percent_X_readout_error','max_parity_assignment_error','within_parity_sectors','instrument_min_eigenvalue','Choi_trace','Choi_min_eigenvalue','max_total_photon_exposure','storage_loss_probability_bound_for_kappa1_over_kappa2_1e_minus4')},indent=2),flush=True)
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',default='mod_odd',choices=['unmod','mod','mod_odd','mod_independent'])
    p.add_argument('--cycles',type=int,default=16);p.add_argument('--steps',type=int,default=32)
    p.add_argument('--odd',type=float,default=None);p.add_argument('--label',default=None)
    p.add_argument('--phase-kind',choices=['common','independent'],default=None)
    a=p.parse_args()
    odd=(.001 if a.case in ('mod_odd','mod_independent') else 0.) if a.odd is None else a.odd
    model=Model(modulated=a.case!='unmod',odd=odd,
                phase_kind=a.phase_kind or ('independent' if a.case=='mod_independent' else 'common'),cycles=a.cycles,steps_per_segment=a.steps)
    run(model,a.label or a.case)
