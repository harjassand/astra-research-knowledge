"""Exact finite Lindblad spectral hierarchy, boundary counterexample, cat Gram.

The theorem is checked on non-Gaussian spin chains with a genuinely nonlinear
Hamiltonian, and separately on passive oscillator chains. The finite-window
example shows why a stationary fourth-order tail is not a gate error bound.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, norm
from scipy.integrate import quad
from scipy.special import eval_genlaguerre, gammaln
import itertools

ROOT=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)

def tensor(ops):
    out=np.array([[1.]],complex)
    for o in ops:out=np.kron(out,o)
    return out

def local(o,j,n):return tensor([o if k==j else I for k in range(n)])
def comm(a,b):return a@b-b@a

def spin_model(n):
    xs=[local(X,j,n) for j in range(n)]
    ys=[local(Y,j,n) for j in range(n)]
    zs=[local(Z,j,n) for j in range(n)]
    H=sum((.13+.07*j)*xs[j]+(.19-.03*j)*ys[j]+(.23+.02*j)*zs[j] for j in range(n))
    for j in range(n-1):
        H+=(.7-.11*j)*xs[j]@xs[j+1]+(.31+.09*j)*zs[j]@ys[j+1]
    jumps=[np.sqrt(.17)*xs[-1],np.sqrt(.23)*ys[-1],np.sqrt(.29)*zs[-1]]
    d=2**n;eye=np.eye(d);rho=eye/d
    def action(o):
        out=1j*comm(H,o)
        for l in jumps:
            q=l.conj().T@l
            out+=l.conj().T@o@l-(q@o+o@q)/2
        return out
    # Construct columns explicitly; reshape of the complete stack is ambiguous.
    columns=[]
    for k in range(d*d):
        e=np.zeros(d*d);e[k]=1
        columns.append(action(e.reshape((d,d),order='F')).reshape(-1,order='F'))
    L=np.column_stack(columns)
    return H,jumps,rho,zs[0],action,L

def ip(rho,a,b):return np.trace(rho@a.conj().T@b)

def spectrum(O,w,rho,L):
    d=len(O)
    R=np.linalg.solve(1j*w*np.eye(d*d)-L,O.reshape(-1,order='F')).reshape((d,d),order='F')
    return float(2*np.real(ip(rho,O,R))),R

def spin_checks():
    result=[]
    for n in (1,2,3):
        H,ls,rho,O,act,L=spin_model(n);d=len(O)
        ops=[O]
        for j in range(2*n+2):ops.append(act(ops[-1]))
        gam=[float(sum(ip(rho,comm(l,a),comm(l,a)).real for l in ls)) for a in ops]
        r=next(j for j,g in enumerate(gam) if g>1e-12)
        assert r==n-1
        moments=[float(ip(rho,O,a).real) for a in ops]
        for k in range(r):assert abs(moments[2*k+1])<2e-12
        leading=gam[r]
        assert abs(moments[2*r+1]-(-1)**(r+1)*leading/2)<5e-10
        rows=[]
        for w in (.4,1.3,3.,10.,30.,100.):
            s,R=spectrum(O,w,rho,L)
            sr,Rr=spectrum(ops[r],w,rho,L)
            diri=float(sum(ip(rho,comm(l,R),comm(l,R)).real for l in ls))
            rel=abs(s-sr/w**(2*r))/max(abs(s),1e-30)
            assert rel<2e-7
            assert abs(s-diri)<5e-12
            cres=max(norm(comm(l,R)-comm(l,Rr)/(1j*w)**r) for l in ls)
            rows.append(dict(omega=w,spectrum=s,derivative_spectrum=sr,
                             exact_identity_relative_error=rel,
                             Dirichlet_identity_error=abs(s-diri),
                             commutator_resolvent_error=float(cres),
                             scaled_tail_ratio=s*w**(2*r+2)/leading))
        result.append(dict(qubits=n,first_outlet_commutator_depth=r,
                           Gamma_by_depth=gam[:r+2],odd_moments=[moments[2*j+1] for j in range(r+1)],
                           predicted_tail_power=2*r+2,tail_coefficient=leading,frequency_checks=rows))
    return result

def passive_chain(n,gamma=1.7):
    # Annihilation drift: loss only on the final mode; vacuum stationary state.
    h=np.zeros((n,n),complex)
    gs=[]
    for j in range(n-1):
        g=.8+.13*j;h[j,j+1]=h[j+1,j]=g;gs.append(g)
    A=-1j*h;A[-1,-1]-=gamma/2
    coefficient=gamma*float(np.prod(np.array(gs)**2))
    rows=[]
    for w in (.3,1.,3.,10.,30.,100.):
        e=np.eye(n)[:,0]
        t=np.linalg.solve(1j*w*np.eye(n)-A,e)
        S=gamma*abs(t[-1])**2
        rows.append(dict(omega=w,spectrum=float(S),scaled_tail_ratio=float(S*w**(2*n)/coefficient)))
    return dict(modes=n,commutator_depth=n-1,tail_power=2*n,tail_coefficient=coefficient,frequency_checks=rows)

def finite_window():
    # A two-mode passive meter, driven by sin(omega t) for an integer number of
    # cycles, then turned off. All ringdown emission equals residual energy.
    gamma=10.;G=1.;T=8.
    A=np.array([[0.,-1j*G],[-1j*G,-gamma/2]],complex)
    rows=[]
    for cycles in (10,20,40,80,160):
        w=2*np.pi*cycles/T
        p=np.linalg.solve(1j*w*np.eye(2)-A,np.array([1.,0.]))
        m=np.linalg.solve(-1j*w*np.eye(2)-A,np.array([1.,0.]))
        vals,vecs=np.linalg.eig(A);co=np.linalg.solve(vecs,p-m)
        def amplitude(t):
            transient=vecs@(np.exp(vals*t)*co)
            return -.5*(np.exp(1j*w*t)*p-np.exp(-1j*w*t)*m-transient)
        emitted,quadrature_error=quad(lambda t:gamma*abs(amplitude(t)[-1])**2,0,T,
                                     epsabs=1e-13,epsrel=1e-10,limit=3000,
                                     points=np.linspace(0,T,4*cycles+1))
        yf=amplitude(T)
        residual=float(np.vdot(yf,yf).real)
        stationary=gamma*abs(np.linalg.solve(1j*w*np.eye(2)-A,np.array([1.,0.]))[-1])**2*T/2
        rows.append(dict(cycles=cycles,omega=w,emitted_during_drive=emitted,
                         final_meter_energy_equal_to_all_ringdown_emission=residual,
                         total_distinguishability_energy=emitted+residual,
                         stationary_bulk_prediction=stationary,
                         emitted_integral_error_estimate=float(quadrature_error),
                         total_times_omega_squared=(emitted+residual)*w*w,
                         bulk_times_omega_fourth=stationary*w**4))
    return rows

def displacement_block(alpha,cutoff):
    z=-2*complex(alpha);x=abs(z)**2
    M=np.empty((cutoff+1,cutoff+1),complex)
    for m in range(cutoff+1):
        for n in range(cutoff+1):
            if m>=n:
                M[m,n]=np.exp(-x/2+(gammaln(n+1)-gammaln(m+1))/2)*z**(m-n)*eval_genlaguerre(n,m-n,x)
            else:
                M[m,n]=np.exp(-x/2+(gammaln(m+1)-gammaln(n+1))/2)*(-z.conjugate())**(n-m)*eval_genlaguerre(m,n-m,x)
    return M

def localization():
    rows=[]
    for alpha in (4.,4*np.sqrt(1.04)):
        for cutoff in (0,2,3,4,6,8,10,12):
            s=float(norm(displacement_block(alpha,cutoff),2))
            rows.append(dict(center_magnitude=alpha,local_fluctuation_cutoff=cutoff,
                             opposite_well_overlap_operator_norm=s,
                             fixed_parity_four_well_Gram_defect_bound=3*s*s,
                             all_eight_well_Gram_defect_bound=(1+s)**3-1))
    return rows

def cycle_primitives(delta=10.,cycles=16,alternating=False):
    labels=list('ABABBABA')+list('ABABBABA')[::-1]
    signs=np.r_[np.ones(8),-np.ones(8)]
    dirs={'A':np.array([1.,-1.,0.]),'B':np.array([1.,0.,-1.])}
    base=np.array([s*dirs[l] for l,s in zip(labels,signs)])
    supports=[(0,),(1,),(2,),(0,1),(0,2),(1,2)]
    tseg=np.pi/delta
    F1=np.zeros(6,complex);F2=np.zeros(6,complex)
    C1=np.zeros(3);C2=np.zeros(3)
    mx=np.zeros(6);cmx=np.zeros(3)
    for cyc in range(cycles):
        orientation=(-1)**cyc if alternating else 1
        theta=np.zeros(3)
        for direction in orientation*base:
            omega=-delta*np.array([sum(direction[list(R)]) for R in supports])
            phase=np.exp(-1j*np.array([sum(theta[list(R)]) for R in supports]))
            for tau in np.linspace(0,tseg,21):
                AA=np.where(abs(omega)>1e-12,(np.exp(1j*omega*tau)-1)/np.where(abs(omega)>1e-12,1j*omega,1),tau)
                BB=np.where(abs(omega)>1e-12,(np.exp(1j*omega*tau)-1-1j*omega*tau)/np.where(abs(omega)>1e-12,(1j*omega)**2,1),tau*tau/2)
                mx=np.maximum(mx,abs(F2+F1*tau+phase*BB))
                cmx=np.maximum(cmx,abs(C2+C1*tau+delta*direction*tau*tau/2))
            AA=np.where(abs(omega)>1e-12,(np.exp(1j*omega*tseg)-1)/np.where(abs(omega)>1e-12,1j*omega,1),tseg)
            BB=np.where(abs(omega)>1e-12,(np.exp(1j*omega*tseg)-1-1j*omega*tseg)/np.where(abs(omega)>1e-12,(1j*omega)**2,1),tseg*tseg/2)
            F2+=F1*tseg+phase*BB;F1+=phase*AA
            C2+=C1*tseg+delta*direction*tseg*tseg/2;C1+=delta*direction*tseg
            theta+=delta*direction*tseg
    assert max(abs(F1))<2e-12 and max(abs(F2))<1e-10
    assert max(abs(C1))<1e-12
    if alternating:assert max(abs(C2))<1e-10
    return dict(delta=delta,cycles=cycles,alternating_complete_cycle_orientation=alternating,
                duration=cycles*16*tseg,
                parasitic_first_primitive_endpoint_norm=float(max(abs(F1))),
                parasitic_second_primitive_endpoint_norm=float(max(abs(F2))),
                parasitic_sampled_max_second_primitive_abs=mx.tolist(),
                proportional_CD_first_primitive_endpoint=C1.tolist(),
                proportional_CD_second_primitive_endpoint=C2.tolist(),
                proportional_CD_sampled_max_second_primitive_abs=cmx.tolist())

def main():
    result=dict(spin_chain_hierarchy=spin_checks(),
                passive_chain_hierarchy=[passive_chain(n) for n in (1,2,3)],
                finite_window_boundary_counterexample=finite_window(),
                displaced_Fock_localization=localization(),
                exact_cycle_primitive_checks=[cycle_primitives(alternating=x) for x in (False,True)],
                qualifications=[
                    'Stationary spectral identities do not certify finite-time logical instruments.',
                    'Frequency asymptotics require a physical band below Lindblad/RWA/control breakdown.',
                    'Finite-Fock Gram bounds require a separate true-state tail bound; cutoff convergence alone is not one.',
                    'The spin and passive-chain checks validate theorem factors, not a cat-device fidelity.'
                ])
    (ROOT/'spectral_hierarchy_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
