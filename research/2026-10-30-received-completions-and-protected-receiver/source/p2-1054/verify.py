"""Reproducible algebra, measurement, calibration and forward-bath checks.

Numerical residuals are floating point diagnostics. The operator identities and
uniform bounds are proved separately in DERIVATION.md. No external operations.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm, polar
from compiler import I,X,Y,Z,kron,spin,controls,target_rotation,cross_rotation,unitary,inspect

def memory_effect(U, rhoL, O):
    M=U.conj().T@kron(O,I)@U
    return np.einsum('ab,biaj->ij',rhoL,M.reshape(4,2,4,2))

def check_measurements(rng):
    worst=0.
    for _ in range(100):
        v=rng.normal(size=(3,3));v/=np.linalg.norm(v,axis=1)[:,None]
        gs=controls(v);angles=rng.uniform(-1.4,1.4,3)
        rhos=[kron((I+Z)/2,I/2),kron(I/2,(I+Z)/2),kron((I+Z)/2,I/2)]
        obs=[kron(Z,I),kron(I,Z),kron(Z,I)]
        for j in range(3):
            U=unitary([(j,angles[j])],gs)
            E=memory_effect(U,rhos[j],obs[j])
            worst=max(worst,np.linalg.norm(E-math.cos(2*angles[j])*I,2))
        U=unitary([(2,angles[2]),(1,angles[1])],gs)
        E=memory_effect(U,kron((I+Z)/2,(I+Z)/2),-kron(X,Y))
        q=v[1]@v[2]
        worst=max(worst,np.linalg.norm(E-q*math.sin(2*angles[1])*math.sin(2*angles[2])*I,2))
        U=unitary([(2,angles[2]),(1,angles[1]),(0,angles[0])],gs)
        E=memory_effect(U,(np.eye(4)+kron(Y,X))/4,kron(X,I))
        k=np.linalg.det(v)
        val=-k*np.prod(np.sin(2*angles))
        worst=max(worst,np.linalg.norm(E-val*I,2))
    return worst

def bath_model(n):
    def site(j,P): return kron(*[P if k==j else I for k in range(n)])
    H=.23*site(0,X)+.17*site(0,Z)
    for j in range(n-1):
        H+=.37*site(j,X)@site(j+1,X)+.29*site(j,Y)@site(j+1,Y)+.23*site(j,Z)@site(j+1,Z)
    for j in range(1,n):
        H+=(.19+.013*j)*site(j,Y)+(.11+.007*j)*site(j,Z)
    return H

def bath_checks(v,seq,theta):
    out=[]
    T=sum(abs(a) for j,a in seq)
    for n in [1,2,3,4]:
        H0=bath_model(n);dm=2**n
        spins=[kron(spin(vi),np.eye(2**(n-1))) for vi in v]
        gs=[kron(kron(X,I),spins[0]),kron(kron(I,X),spins[1]),kron(kron(Y,I),spins[2])]
        local_h=max(np.linalg.norm(H0@P-P@H0,2) for P in spins)
        for J in [.00001,.0001,.001,.01]:
            HM=J*H0
            U=np.eye(4*dm,dtype=complex)
            for j,a in seq:
                U=U@expm(-1j*(kron(np.eye(4),HM)+np.sign(a)*gs[j])*abs(a))
            targetL=expm(-1j*theta*kron(Z,X))
            target=kron(targetL,expm(-1j*HM*T))
            free_error=np.linalg.norm(U-target,2)
            W=kron(targetL.conj().T,np.eye(dm))@U
            partial=np.einsum('aiaj->ij',W.reshape(4,dm,4,dm))/4
            VM,_=polar(partial)
            fit_error=np.linalg.norm(U-kron(targetL,VM),2)
            out.append({'memory_spins':n,'J':J,'h_max':J*local_h,
                        'free_bath_error':free_error,'fitted_memory_error':fit_error,
                        'midpoint_bound':J*local_h*T*T/4})
    return out

def calibration_checks(v,seq,theta,rng):
    q=float(v[1]@v[2]);s=math.sqrt(1-q*q);k=float(np.linalg.det(v));gs=controls(v)
    target=expm(-1j*theta*kron(Z,X,I));worst=0.;worstbound=0.
    # Confidence radii of the finite illustration in DERIVATION.md.
    for _ in range(200):
        dq=rng.uniform(-.0006,.0006);dk=rng.uniform(-.0006,.0006)
        rel=rng.uniform(-.0002,.0002,3)
        estimated=target_rotation(theta,math.sqrt(1-(q+dq)**2),k+dk)
        # True rates are one, estimated rates 1/(1+rel): actual angles scale 1+rel.
        actual=[(j,a*(1+rel[j])) for j,a in estimated]
        err=np.linalg.norm(unitary(actual,gs)-target,2)
        bound=20*max(abs(rel))+1.8*abs(dq)+1.4*abs(dk)
        worst=max(worst,err);worstbound=max(worstbound,bound)
        assert err<=bound+1e-12
    return {'max_sampled_error':worst,'max_sampled_analytic_bound':worstbound,
            'whole_box_bound':20*.0002+(1.8+1.4)*.0006}

def same_kappa_other_q(k,q):
    s=math.sqrt(1-q*q);d=k/s
    return np.array([[math.sqrt(1-d*d),0,d],[1,0,0],[q,s,0]])

def main():
    rng=np.random.default_rng(270130)
    v=np.array([[1,0,0],[.3,math.sqrt(.91),0],[.2,.4,math.sqrt(.8)]])
    theta=-math.pi/4;r=inspect(v,theta);seq=r.pop('sequence')
    r['native_sequence_matrix_order']=seq
    r['chronological_sequence']=list(reversed(seq))
    random_results=[]
    for _ in range(300):
        w=rng.normal(size=(3,3));w/=np.linalg.norm(w,axis=1)[:,None]
        if abs(np.linalg.det(w))<.015:continue
        rr=inspect(w,rng.uniform(-math.pi/2,math.pi/2))
        random_results.append({x:rr[x] for x in ['kappa','pulses','action','error']})
    signflip=v.copy();signflip[0]*=-1
    wrongsign=np.linalg.norm(unitary(seq,controls(signflip))-expm(-1j*theta*kron(Z,X,I)),2)
    assumed=same_kappa_other_q(.8,.4);actual=same_kappa_other_q(.8,0.)
    wseq=target_rotation(theta,math.sqrt(1-.4**2),.8)
    missingq=np.linalg.norm(unitary(wseq,controls(actual))-expm(-1j*theta*kron(Z,X,I)),2)
    acquisition=[]
    for fail in [.01,.0001]:
        nl,nq,nk=[math.ceil(2*math.log(10/fail)/d**2) for d in [.0023,.0018,.00048]]
        acquisition.append({'calibration_failure_bound':fail,'strength_shots_each':nl,
                            'q_echo_shots':nq,'chirality_shots':nk,
                            'total_shots':3*nl+nq+nk,'native_segments':3*nl+5*nq+3*nk,
                            'nominal_source_action':3*nl*17*math.pi/4+nq*2*math.pi+nk*3*math.pi/4})
    data={'example':r,'measurement_effect_max_error':check_measurements(rng),
          'random_gate_checks':{'count':len(random_results),'max_error':max(x['error'] for x in random_results),
                                'max_segments':max(x['pulses'] for x in random_results),
                                'min_kappa':min(x['kappa'] for x in random_results)},
          'calibration':calibration_checks(v,seq,theta,rng),
          'acquisition_budgets':acquisition,
          'conditional_finite_gate_bound':.00592+1.01*3e-5*20.21**2/4+.0005,
          'bath_checks':bath_checks(v,seq,theta),
          'failures':{'wrong_chirality_sign_error':wrongsign,'same_kappa_wrong_q_error':missingq}}
    Path(__file__).with_name('results.json').write_text(json.dumps(data,indent=2,default=float)+'\n')
    brief=dict(data);brief['example']={k:v for k,v in r.items() if 'sequence' not in k}
    print(json.dumps(brief,indent=2,default=float))

if __name__=='__main__':main()
