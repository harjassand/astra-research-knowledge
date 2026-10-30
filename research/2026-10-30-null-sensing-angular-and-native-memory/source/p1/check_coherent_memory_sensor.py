#!/usr/bin/env python3
"""Full quantum-bath continuation; conditional state retained between all trials.

Population mathematics only. Endpoint CP instruments and finite Markov reservoir
remain the explicit operation interfaces in the proof, not verified hardware.
"""
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from threadpoolctl import threadpool_limits
from check_adaptive_null_sensor import (I2, I4, X, Y, Z, LOWER, PLUS, vec,
    unvec, generator, storage, clock_generator)

HERE=Path(__file__).resolve().parent
IK=np.eye(8,dtype=complex)
S=np.kron(np.kron(Z,I2),I2)
TRACE=vec(IK)

def clock_hamiltonian(g,j,omega):
    exchange=g*(np.kron(LOWER,LOWER.conj().T)+np.kron(LOWER.conj().T,LOWER))
    return np.kron(exchange,I2)+j*np.kron(np.kron(X,I2),X)+omega/2*np.kron(I4,Z)

def clock_jumps(gamma,nu,lam):
    return [np.sqrt(gamma)*np.kron(np.kron(I2,LOWER),I2),
            np.sqrt(gamma*nu)*np.kron(np.kron(I2,LOWER.conj().T),I2),
            np.sqrt(lam)*np.kron(np.kron(X,I2),I2)]

def full(delta,g,gamma,j,omega,nu,lam):
    h=np.kron(I2,clock_hamiltonian(g,j,omega))+delta/2*np.kron(Z,S)
    return generator(h,[np.kron(I2,jump) for jump in clock_jumps(gamma,nu,lam)])

def maps():
    logical=.9995*PLUS+.0005*(I2-PLUS)
    prep=np.zeros((256,64),complex); reads=[]
    for k in range(64):
        basis=np.zeros((8,8),complex); basis[k%8,k//8]=1
        prep[:,k]=vec(np.kron(logical,basis))
    for sign in [1,-1]:
        effect=(I2+sign*Y)/2; read=np.zeros((64,256),complex)
        for k in range(256):
            basis=np.zeros((16,16),complex); basis[k%16,k//16]=1
            read[:,k]=vec(np.einsum("ji,iajb->ab",effect,basis.reshape(2,8,2,8)))
        reads.append(read)
    return prep,.998*reads[0]+.006*reads[1],.002*reads[0]+.994*reads[1]

def initial_state():
    psi=np.zeros(8,complex); psi[2]=1/np.sqrt(2); psi[7]=1j/np.sqrt(2)
    return np.outer(psi,psi.conj())

def hidden_bloch(state):
    rho=unvec(state,8)
    hidden=np.einsum("aiaj->ij",rho.reshape(4,2,4,2))
    return [float(np.trace(p@hidden).real) for p in [X,Y,Z]]

def coherent_response_checks():
    g=gamma=50.4; j=.53; nu=.02; lam=.31; cap=.4; jcap=.7
    c=9/(4*g); tau=initial_state(); rows=[]
    for omega,duration in [(0.,1.),(.7,8.),(53.,16.),(5000.,1.)]:
        h=clock_hamiltonian(g,j,omega)
        a=generator(h,clock_jumps(gamma,nu,lam))
        aug=np.zeros((65,65),complex); aug[:64,:64]=a; aug[64,:64]=vec(S.T)
        out=expm(aug*duration)@np.r_[vec(tau),0.]
        exposure=float(out[-1].real)
        lower=(1-2*c*cap-4*c*jcap-4*c*nu*gamma)*duration-2*c
        delta=.5/duration
        final=unvec(expm(full(delta,g,gamma,j,omega,nu,lam)*duration)@vec(np.kron(PLUS,tau)),16)
        mean=float(np.trace(np.kron(Y,IK)@final).real)
        assert exposure>=lower-2e-8 and mean>=(.5-1/24)*.5-2e-8
        assert abs(mean-delta*exposure)<=.5**3/6+2e-8
        # Internal bath Hamiltonian cancels from the storage drift exactly.
        vb=np.kron(storage(g,gamma),I2)
        comm=np.linalg.norm(np.kron(I4,Z)@vb-vb@np.kron(I4,Z))
        rows.append(dict(omega=omega,T=duration,null_exposure=exposure,
                         lower_exposure=lower,actual_terminal_mean=mean,
                         bath_internal_commutator=comm))
    return rows

def peripheral_spectrum_check():
    a=clock_generator(36.,36.,1.,.02); s=np.kron(Z,I2); rows=[]
    for delta in [0.,.01,.1,.4]:
        off=a-1j*delta/2*(np.kron(I4,s)+np.kron(s.T,I4))
        values=np.linalg.eigvals(off)
        rightmost=values[np.argmax(values.real)]
        if delta:
            assert rightmost.real<0
        rows.append(dict(delta=delta,rightmost_real=float(rightmost.real),
                         rightmost_imag=float(rightmost.imag)))
    return rows

def adaptive():
    rng=np.random.default_rng(20261031)
    theta=.193; epsilon=1/128; alpha=.05; W=1.; cap=.4; jcap=.7
    g=gamma=18*(cap+2*jcap+W); jactual=.53; omega=17.13; nu=.02
    slope=.5-1/24; eta=slope/16; beta=slope/32; threshold=eta+beta
    levels=math.ceil(math.log2(W/(2*epsilon))); left,right=-.5,.5
    prep,rplus,rminus=maps(); state=vec(initial_state()); reports=[]; records=[]
    total_t=0.; total_n=0; max_trace=0.
    for level in range(levels):
        command=(left+right)/2; width=right-left; duration=1/width
        failure=alpha*2**(level-levels)
        count=math.ceil(2/(eta*eta)*math.log(2/failure))
        lam=.23+.08*math.cos(3*command)**2
        evolved=expm(full(theta-command,g,gamma,jactual,omega,nu,lam)*duration)@prep
        mp=rplus@evolved; mm=rminus@evolved
        trace_error=float(np.linalg.norm(TRACE@(mp+mm)-TRACE)); max_trace=max(max_trace,trace_error)
        assert trace_error<3e-8
        before=[left,right]; hbefore=hidden_bloch(state); ys=np.zeros(count,dtype=np.uint8); condsum=0.
        for i in range(count):
            plus=mp@state; probability=float((TRACE@plus).real)
            assert 0<probability<1
            condsum+=2*probability-1
            if rng.random()<probability:
                ys[i]=1; state=plus/probability
            else:
                state=(mm@state)/(1-probability)
            state/=float((TRACE@state).real)
        mean=2*float(ys.mean())-1
        if mean>threshold:
            left=command; branch="upper"
        elif mean<-threshold:
            right=command; branch="lower"
        else:
            left,right=command-width/4,command+width/4; branch="central"
        minimum=float(np.linalg.eigvalsh((unvec(state,8)+unvec(state,8).conj().T)/2)[0])
        assert minimum>-3e-8
        records.append(dict(level=level,interval_before=before,interval_after=[left,right],command=command,
                            T=duration,trials=count,mean=mean,conditional_mean=condsum/count,
                            martingale_deviation=abs(mean-condsum/count),branch=branch,
                            contains_truth=bool(left<=theta<=right),hidden_bloch_before=hbefore,
                            hidden_bloch_after=hidden_bloch(state),min_joint_density_eigenvalue=minimum))
        reports.append(ys); total_t+=count*duration; total_n+=count
    estimate=(left+right)/2
    out=dict(theta=theta,epsilon=epsilon,alpha=alpha,estimate=estimate,error=abs(theta-estimate),
             passes=abs(theta-estimate)<=epsilon,trials=total_n,total_interrogation_time=total_t,
             g=g,gamma=gamma,upward_ratio=nu,native_rate_cap=cap,coherent_coupling_cap=jcap,
             actual_coherent_coupling=jactual,actual_hidden_frequency=omega,
             max_instrument_trace_residual=max_trace,levels=records,
             interpretation="One conditional full-quantum population-model run; no hidden bath reset or iid replacement.")
    np.savez_compressed(HERE/"COHERENT_MEMORY_BINARY_RECORD.npz",reports=np.concatenate(reports))
    return out

def main():
    out=dict(scope="Mathematical population checks, not acquired device confidence.",
             response_checks=coherent_response_checks(),peripheral_spectrum=peripheral_spectrum_check(),
             persistent_quantum_run=adaptive(),
             code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             imported_checker_sha256=hashlib.sha256((HERE/"check_adaptive_null_sensor.py").read_bytes()).hexdigest())
    (HERE/"COHERENT_MEMORY_CHECK_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
    run=out["persistent_quantum_run"]
    print(json.dumps({k:run[k] for k in ["error","epsilon","trials","total_interrogation_time","passes",
                                       "max_instrument_trace_residual"]},indent=2),flush=True)

if __name__=="__main__":
    with threadpool_limits(limits=1):
        main()
