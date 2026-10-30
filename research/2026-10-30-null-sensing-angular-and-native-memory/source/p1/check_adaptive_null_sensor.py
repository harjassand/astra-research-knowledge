#!/usr/bin/env python3
"""Population-model checks; persistent conditional clock/environment, not iid.

No experimental acquisition or apparatus validation is claimed.
Run: OPENBLAS_NUM_THREADS=1 python check_adaptive_null_sensor.py
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from threadpoolctl import threadpool_limits

HERE = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], complex)
Y = np.array([[0,-1j],[1j,0]], complex)
Z = np.diag([1,-1]).astype(complex)
LOWER = np.array([[0,1],[0,0]], complex)
N = np.diag([0,1]).astype(complex)
PLUS = np.array([[.5,.5],[.5,.5]], complex)
I4 = np.eye(4, dtype=complex)
I8 = np.eye(8, dtype=complex)

def vec(a):
    return np.asarray(a).reshape(-1, order="F")

def unvec(a, dim):
    return np.asarray(a).reshape((dim,dim), order="F")

def dissipator(j):
    ident = np.eye(j.shape[0]); jj = j.conj().T @ j
    return np.kron(j.conj(),j)-(np.kron(ident,jj)+np.kron(jj.T,ident))/2

def generator(h, jumps):
    ident = np.eye(h.shape[0])
    out = -1j*(np.kron(ident,h)-np.kron(h.T,ident))
    for j in jumps:
        out += dissipator(j)
    return out

def storage(g, gamma):
    v = np.diag([0,1/gamma,1/gamma+gamma/(4*g*g),2/gamma+gamma/(4*g*g)]).astype(complex)
    v[1,2] = 1j/(2*g); v[2,1] = -1j/(2*g)
    return v

def adjoint_generator(a,h,jumps):
    out = 1j*(h@a-a@h)
    for j in jumps:
        jj=j.conj().T@j
        out += j.conj().T@a@j-(jj@a+a@jj)/2
    return out

def random_density(dim,rng):
    a=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
    rho=a@a.conj().T
    return rho/np.trace(rho)

def physical_identities():
    def op(a,b,c):
        return np.kron(np.kron(a,b),c)
    transform=np.zeros((8,8),complex)
    for s in range(2):
        for a in range(2):
            for r in range(2):
                transform[4*a+2*(s^a)+r,4*s+2*a+r]=1
    zs=op(Z,I2,I2); xs=op(X,I2,I2); parity=op(Z,Z,I2)
    f=xs@(I8-parity)/2
    hc=f@op(I2,I2,LOWER.conj().T)+f.conj().T@op(I2,I2,LOWER)
    h_pauli=(op(X,I2,X)+op(Y,Z,Y))/2
    target=np.kron(I2,np.kron(LOWER,LOWER.conj().T)+np.kron(LOWER.conj().T,LOWER))
    checks={
        "correction_pauli_formula":np.linalg.norm(hc-h_pauli),
        "encoded_signal":np.linalg.norm(transform@zs@transform.conj().T-op(Z,Z,I2)),
        "encoded_noise":np.linalg.norm(transform@xs@transform.conj().T-op(I2,X,I2)),
        "encoded_correction":np.linalg.norm(transform@hc@transform.conj().T-target),
        "logical_x":np.linalg.norm(transform@op(X,X,I2)@transform.conj().T-op(X,I2,I2)),
        "logical_y":np.linalg.norm(transform@op(X,Y,I2)@transform.conj().T-op(Y,I2,I2))}
    assert max(checks.values())<1e-12
    return {k:float(v) for k,v in checks.items()}

def storage_checks():
    rows=[]
    for g,gamma in [(.7,2.3),(1,1),(3.2,.6),(25.2,25.2)]:
        v=storage(g,gamma)
        h=g*(np.kron(LOWER,LOWER.conj().T)+np.kron(LOWER.conj().T,LOWER))
        j=np.sqrt(gamma)*np.kron(I2,LOWER)
        residual=np.linalg.norm(adjoint_generator(v,h,[j])+np.kron(N,I2))
        eigs=np.linalg.eigvalsh(v); c=2/gamma+gamma/(4*g*g)
        up=adjoint_generator(v,np.zeros((4,4)),[np.kron(I2,LOWER.conj().T)])
        up_max=np.linalg.eigvalsh(up)[-1]
        flip=np.kron(X,I2)@v@np.kron(X,I2)-v
        flip_max=np.linalg.eigvalsh(flip)[-1]
        assert residual<1e-11 and eigs[0]>-1e-12
        assert abs(eigs[-1]-c)<1e-12
        assert up_max<=2*c+1e-12 and flip_max<=c+1e-12
        rows.append(dict(g=g,gamma=gamma,poisson_residual=float(residual),eigenvalues=eigs.tolist(),
                         norm=c,upward_drift_max=float(up_max),unit_flip_drift_max=float(flip_max)))
    return rows

def clock_generator(g,gamma,lam,nu):
    h=g*(np.kron(LOWER,LOWER.conj().T)+np.kron(LOWER.conj().T,LOWER))
    return generator(h,[np.sqrt(gamma)*np.kron(I2,LOWER),
                        np.sqrt(nu*gamma)*np.kron(I2,LOWER.conj().T),
                        np.sqrt(lam)*np.kron(X,I2)])

def full_generator(delta,g,gamma,lam,nu,logical_dephasing=0):
    hc=g*(np.kron(LOWER,LOWER.conj().T)+np.kron(LOWER.conj().T,LOWER))
    h=np.kron(I2,hc)+delta/2*np.kron(Z,np.kron(Z,I2))
    jumps=[np.sqrt(gamma)*np.kron(I2,np.kron(I2,LOWER)),
           np.sqrt(nu*gamma)*np.kron(I2,np.kron(I2,LOWER.conj().T)),
           np.sqrt(lam)*np.kron(I2,np.kron(X,I2))]
    if logical_dephasing:
        jumps.append(np.sqrt(logical_dephasing)*np.kron(Z,I4))
    return generator(h,jumps)

def response_checks(rng):
    rows=[]; g=gamma=25.2; cap=.4; nu=.02; vstore=9/(4*g)
    s_op=np.kron(Z,I2); y_op=np.kron(Y,I4)
    for idx in range(18):
        tau=random_density(4,rng)
        total_t=[1.,2.3,8.,31.,120.,512.][idx%6]
        rates=rng.uniform(0,cap,size=3); durations=total_t*np.array([.17,.31,.52])
        rho0=vec(tau); exposure=0.
        for lam,dt in zip(rates,durations):
            a=clock_generator(g,gamma,float(lam),nu)
            aug=np.zeros((17,17),complex); aug[:16,:16]=a; aug[16,:16]=vec(s_op.T)
            state=expm(aug*dt)@np.r_[rho0,0.]
            rho0=state[:16]; exposure+=float(state[-1].real)
        lower=(1-2*cap*vstore-4*nu*gamma*vstore)*total_t-2*vstore
        phase=[.09,.25,.5][idx%3]; delta=phase/total_t; means=[]
        for signed_delta in [delta,-delta]:
            state=vec(np.kron(PLUS,tau))
            for lam,dt in zip(rates,durations):
                state=expm(full_generator(signed_delta,g,gamma,float(lam),nu)*dt)@state
            means.append(float(np.trace(y_op@unvec(state,8)).real))
        remainder=abs(means[0]-delta*exposure)
        assert exposure>=lower-2e-8
        assert abs(means[0]+means[1])<2e-9
        assert remainder<=phase**3/6+2e-9
        assert means[0]>=(.5-1/24)*phase-2e-9
        rows.append(dict(T=total_t,rates=rates.tolist(),phase=phase,null_exposure=exposure,
                         exposure_lower=lower,signed_means=means,oddness_residual=abs(sum(means)),
                         cubic_remainder=remainder,cubic_bound=phase**3/6))
    return rows

def persistent_generator(delta,g,gamma,rates,nu,hidden_rates):
    blocks=[full_generator(delta,g,gamma,lam,nu) for lam in rates]
    out=np.zeros((128,128),complex); a,b=hidden_rates
    out[:64,:64]=blocks[0]-a*np.eye(64); out[64:,64:]=blocks[1]-b*np.eye(64)
    out[64:,:64]=a*np.eye(64); out[:64,64:]=b*np.eye(64)
    return out

def endpoint_maps(prep_error=.0005,plus_to_minus=.002,minus_to_plus=.006):
    logical=(1-prep_error)*PLUS+prep_error*(I2-PLUS)
    p=np.zeros((128,32),complex); ideal=[]
    for sign in [1,-1]:
        effect=(I2+sign*Y)/2; read=np.zeros((32,128),complex)
        for h in range(2):
            for col in range(64):
                basis=np.zeros((8,8),complex); basis[col%8,col//8]=1
                reduced=np.einsum("ji,iajb->ab",effect,basis.reshape(2,4,2,4))
                read[h*16:(h+1)*16,h*64+col]=vec(reduced)
        ideal.append(read)
    for h in range(2):
        for col in range(16):
            basis=np.zeros((4,4),complex); basis[col%4,col//4]=1
            p[h*64:(h+1)*64,h*16+col]=vec(np.kron(logical,basis))
    rplus=(1-plus_to_minus)*ideal[0]+minus_to_plus*ideal[1]
    rminus=plus_to_minus*ideal[0]+(1-minus_to_plus)*ideal[1]
    return p,rplus,rminus

TRACE32=np.r_[vec(I4),vec(I4)]

def persistent_trial_maps(delta,duration,g,gamma,rates,nu,hidden_rates,maps):
    prepare,readplus,readminus=maps
    evolve=expm(persistent_generator(delta,g,gamma,rates,nu,hidden_rates)*duration)
    plus=readplus@evolve@prepare; minus=readminus@evolve@prepare
    residual=float(np.linalg.norm(TRACE32@(plus+minus)-TRACE32))
    assert residual<2e-8
    return plus,minus,residual

def run_adaptive(seed,theta,hidden_rates,epsilon=1/128,alpha=.05):
    rng=np.random.default_rng(seed); width0=1.; left,right=-.5,.5
    cap=.4; g=gamma=18*(cap+width0); nu=.02; slope=.5-1/24
    eta=slope/16; beta=slope/32; threshold=eta+beta
    levels=math.ceil(math.log2(width0/(2*epsilon)))
    state=np.r_[.73*vec(random_density(4,rng)),.27*vec(random_density(4,rng))]
    maps=endpoint_maps(); raw=[]; records=[]; time_total=0.; calls_total=0; worst_trace=0.
    for j in range(levels):
        width=right-left; command=(left+right)/2; duration=1/width
        budget=alpha*2**(j-levels)
        count=math.ceil(2/(eta*eta)*math.log(2/budget))
        # Actual unknown command-dependent kinetics used only by the simulator.
        rates=[.05+.35*math.sin(3*command+.31)**2,.10+.30*math.cos(2*command-.17)**2]
        mplus,mminus,tr_res=persistent_trial_maps(theta-command,duration,g,gamma,rates,
                                                 nu,hidden_rates,maps)
        worst_trace=max(worst_trace,tr_res)
        h_start=float(np.trace(unvec(state[16:],4)).real)
        reports=np.zeros(count,dtype=np.uint8); conditional_sum=0.
        for i in range(count):
            nxt_plus=mplus@state; probability=float((TRACE32@nxt_plus).real)
            assert -1e-10<probability<1+1e-10
            probability=min(1.,max(0.,probability)); conditional_sum+=2*probability-1
            if rng.random()<probability:
                reports[i]=1; state=nxt_plus/probability
            else:
                state=(mminus@state)/(1-probability)
            state/=float((TRACE32@state).real)  # floating trace repair, no physical K reset
        mean=2*float(reports.mean())-1; before=[left,right]
        if mean>threshold:
            left=command; branch="upper"
        elif mean<-threshold:
            right=command; branch="lower"
        else:
            left,right=command-width/4,command+width/4; branch="central"
        h_end=float(np.trace(unvec(state[16:],4)).real)
        mineig=min(float(np.linalg.eigvalsh((unvec(state[k:k+16],4)
                        +unvec(state[k:k+16],4).conj().T)/2)[0]) for k in [0,16])
        assert mineig>-1e-8
        time_total+=count*duration; calls_total+=count; raw.append(reports)
        records.append(dict(level=j,interval_before=before,command=command,T=duration,trials=count,
                            conditional_failure_budget=budget,mean=mean,
                            mean_conditional_expectation=conditional_sum/count,
                            martingale_error=abs(mean-conditional_sum/count),threshold=threshold,
                            branch=branch,interval_after=[left,right],contains_truth=bool(left<=theta<=right),
                            hidden_one_probability_start=h_start,hidden_one_probability_end=h_end,
                            hidden_rates=list(hidden_rates),actual_native_rates=rates,
                            min_conditional_density_eigenvalue=mineig))
    estimate=(left+right)/2; c=2/(eta*eta)
    time_bound=(c*(math.log(2/alpha)+2*math.log(2))+1)/epsilon
    assert time_total<time_bound
    result=dict(seed=seed,theta=theta,epsilon=epsilon,alpha=alpha,estimate=estimate,
                absolute_error=abs(estimate-theta),all_brackets_contain_truth=all(r["contains_truth"] for r in records),
                passes=abs(estimate-theta)<=epsilon,total_interrogation_time=time_total,
                time_upper_bound=time_bound,trials=calls_total,correction_g=g,reset_down=gamma,
                reset_up=gamma*nu,beta=beta,endpoint_mean_error_bound=.013,
                max_instrument_trace_residual=worst_trace,levels=records,
                provenance="Numerical population model, persistent conditional clock/hidden state, not experimental acquisition.")
    return result,np.concatenate(raw)

def finite_residual_failure():
    g=gamma=36.; lam,nu=1.,.02; clock=clock_generator(g,gamma,lam,nu)
    a=clock.copy(); rhs=np.zeros(16,complex); a[-1,:]=vec(I4); rhs[-1]=1
    tau=unvec(np.linalg.solve(a,rhs),4); rows=[]
    for duration in [1.,8.,64.,512.,4096.,16384.]:
        entry=dict(T=duration)
        for label,delta in [("fixed",.4),("null_scaled",.5/duration)]:
            state=unvec(expm(full_generator(delta,g,gamma,lam,nu)*duration)@vec(np.kron(PLUS,tau)),8)
            xx=float(np.trace(np.kron(X,I4)@state).real); yy=float(np.trace(np.kron(Y,I4)@state).real)
            entry[label]=dict(delta=delta,x=xx,y=yy,contrast=math.hypot(xx,yy))
        logical_noise=1e-3
        state=unvec(expm(full_generator(.5/duration,g,gamma,lam,nu,logical_noise)*duration)
                    @vec(np.kron(PLUS,tau)),8)
        noisy_y=float(np.trace(np.kron(Y,I4)@state).real)
        target=entry["null_scaled"]["y"]*math.exp(-2*logical_noise*duration)
        entry["logical_dephasing_y"]=noisy_y
        entry["logical_dephasing_factor_residual"]=abs(noisy_y-target)
        assert abs(noisy_y-target)<3e-8
        rows.append(entry)
    return rows

def main():
    rng=np.random.default_rng(20261030)
    out={"scope":"Executed mathematical population checks, not acquired hardware data.",
         "physical_identities":physical_identities(),"storage_checks":storage_checks(),
         "warm_time_varying_response_checks":response_checks(rng),
         "fixed_residual_and_logical_noise_failures":finite_residual_failure()}
    adaptive=[]; raw={}
    cases=[(1030,.317,(0.,0.)),(1031,-.273,(.0002,.0001)),
           (1032,0.,(.00005,.0004)),(1033,.499,(0.,0.))]
    for seed,theta,hidden_rates in cases:
        result,reports=run_adaptive(seed,theta,hidden_rates)
        adaptive.append(result); raw[f"reports_seed_{seed}"]=reports
        print(json.dumps({"seed":seed,"epsilon":result["epsilon"],"error":result["absolute_error"],
                          "trials":result["trials"],"time":result["total_interrogation_time"],
                          "passes":result["passes"]}),flush=True)
    out["persistent_adaptive_runs"]=adaptive
    out["totals"]=dict(specimens=len(cases),trials=sum(r["trials"] for r in adaptive),
                       total_interrogation_time=sum(r["total_interrogation_time"] for r in adaptive),
                       passes=sum(r["passes"] for r in adaptive),
                       max_physical_identity_residual=max(out["physical_identities"].values()),
                       max_poisson_residual=max(r["poisson_residual"] for r in out["storage_checks"]),
                       max_instrument_trace_residual=max(r["max_instrument_trace_residual"] for r in adaptive))
    out["code_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/"ADAPTIVE_NULL_SENSOR_CHECK_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
    np.savez_compressed(HERE/"ADAPTIVE_NULL_SENSOR_BINARY_RECORDS.npz",**raw)
    print(json.dumps(out["totals"],indent=2),flush=True)

if __name__=="__main__":
    with threadpool_limits(limits=1):
        main()
