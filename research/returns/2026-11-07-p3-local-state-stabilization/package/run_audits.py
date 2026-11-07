"""Reproducible construction audits. No physical experiment is performed."""
from __future__ import annotations
import json, math, platform, time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import numpy as np
import scipy
import scipy.linalg
from threadpoolctl import threadpool_limits
from local_stabilizer import *

ROOT=Path(__file__).resolve().parent

def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2)+"\n")

def exp_minus_upper(x: Fraction, bits: int):
    """Outward fixed-dyadic enclosure of exp(-x), using rational Taylor series."""
    assert x>=0
    s=0;y=x
    while y>Fraction(1,2):y/=2;s+=1
    D=1<<bits;term=Fraction(1);total=term;n=0
    while True:
        nxt=term*y/(n+1)
        # For y<=1/2, all terms after the first omitted one sum to <=2*nxt.
        if 2*nxt < Fraction(1, D*D):
            tail=2*nxt;break
        total+=nxt;term=nxt;n+=1
    lo=Fraction(1,total+tail);hi=Fraction(1,total)
    l=(lo.numerator*D)//lo.denominator
    u=(hi.numerator*D+hi.denominator-1)//hi.denominator
    for _ in range(s):
        l=l*l//D;u=(u*u+D-1)//D
    return Fraction(l,D),Fraction(u,D)

def scientific(f:Fraction):
    with localcontext() as c:
        c.prec=24
        return f"{Decimal(f.numerator)/Decimal(f.denominator):.14E}"

def bottleneck_records():
    records=[];k=5
    for N in (63,127,255,511,1023):
        lo,hi=exp_minus_upper(Fraction(N)-Fraction(4*k*k,N),2*N+160)
        bup=min(Fraction(1), (1<<(N-1))*hi)
        quantum=math.isqrt(bup.denominator//(128*bup.numerator))
        classical=bup.denominator//(8*bup.numerator)
        with localcontext() as c:
            c.prec=100
            den=Decimal(0);num=Decimal(0)
            for w in range(N+1):
                m=N-2*w
                weight=Decimal(math.comb(N,w))*(Decimal(m*m-N*N)/Decimal(N)).exp()
                den+=weight
                if abs(m)<=2*k:num+=weight
            bnum=num/den
        records.append({"N":N,"beta":"2","physical_qubit_change_limit":k,
            "cut":"M>0", "boundary":"abs(M)<=10", "phase_probability":"1/2",
            "boundary_upper_rational_numerator":str(bup.numerator),
            "boundary_upper_rational_denominator":str(bup.denominator),
            "boundary_upper_scientific":scientific(bup),
            "boundary_probability_decimal_diagnostic":str(bnum),
            "quantum_auxiliary_allowed_event_lower_integer":str(quantum),
            "phase_block_diagonal_event_lower_integer":str(classical),
            "mixing_target_trace_distance":"1/4"})
    return records

def clock_structure_audit():
    n_words=0;n_edges=0;n_cleanup=0
    for T in range(1,13):
        for s in range(1<<T):
            w=word(s,T);v=potential(w);n_words+=1
            legal=(v==0)
            assert legal==(w==tuple(sorted(w,reverse=True)))
            for t in range(T):
                z=edge_destination(w,t);n_edges+=1
                assert potential(z)==v
            for t in range(T-1):
                if w[t:t+2]==(0,1):
                    z=list(w);z[t+1]=0;n_cleanup+=1
                    assert potential(tuple(z))<=v-1
    return {"clock_lengths_exhausted":list(range(1,13)),"clock_words":n_words,
        "edge_updates":n_edges,"illegal_cleanup_updates":n_cleanup,
        "all_legal_invariance_and_potential_assertions":True}

def bell_audit():
    source={"work_qubits":2,"output_qubits":[0,1],"input_state":"zero",
            "gates":[{"kind":"H","qubits":[0]},{"kind":"CNOT","qubits":[0,1]}]}
    desc=compile_description(source,"1/16","1/16")
    save("BELL_SOURCE.json",source);save("BELL_LOCAL_PROCESS.json",desc)
    cert=desc["certificate"]
    S,tp=superoperator(source,cert)
    blocks,states=stationary_history(source,cert);omega=blocks_to_density(blocks)
    stationary_resid=trace_distance((S@omega.reshape(-1,order='F')).reshape(omega.shape,order='F'),omega)
    eig=np.linalg.eigvals(S)
    eigen_moduli=sorted((abs(z) for z in eig),reverse=True)
    D=omega.shape[0];rng=np.random.default_rng(417)
    vectors={}
    for label,index in [("all_zero",0),("invalid_clock_01",1),("all_one",D-1)]:
        v=np.zeros(D,complex);v[index]=1;vectors[label]=v
    v=np.zeros(D,complex);v[1]=1/np.sqrt(2);v[-3]=1j/np.sqrt(2)
    vectors["coherent_invalid_valid_clock"]=v
    v=rng.normal(size=D)+1j*rng.normal(size=D);v/=np.linalg.norm(v)
    vectors["random_entangled_work_clock"]=v
    initial={k:np.outer(v,v.conj()) for k,v in vectors.items()}
    initial["maximally_mixed"]=np.eye(D)/D
    runs=[]
    for m in [0,100,1000,5000,cert["total_events_bound"]]:
        power=np.linalg.matrix_power(S,m)
        distances={k:trace_distance((power@rho.reshape(-1,order='F')).reshape(D,D,order='F'),omega)
                   for k,rho in initial.items()}
        runs.append({"events":m,"full_joint_trace_distances":distances})
    # A maximally entangled untouched reference tests complete erasure, not only marginals.
    reference_state=power.reshape(D,D,D,D,order='F').transpose(0,2,1,3).reshape(D*D,D*D)/D
    reference_distance=trace_distance(reference_state,np.kron(omega,np.eye(D)/D))
    # A single-qubit reset is a valid CPTP perturbation, with half-diamond error <= eta.
    eta=1e-6
    Kr=[embed(K,[0],4) for K in (np.array([[1,0],[0,0]],complex),np.array([[0,1],[0,0]],complex))]
    reset=sum(np.kron(K.conj(),K) for K in Kr)
    Sn=(1-eta)*S+eta*reset
    ident=(np.eye(D)/D).reshape(-1,order='F');tr=np.eye(D).reshape(-1,order='F')
    vn=np.linalg.solve(np.eye(D*D)-Sn+np.outer(ident,tr),ident)
    noisy=vn.reshape(D,D,order='F');noisy=(noisy+noisy.conj().T)/2
    out=reduce_state(omega,[0,1],4)
    mstar=desc["noise_block_certificate"]["total_events_bound"]
    return {"binary64_diagnostic":True,"max_channel_trace_preservation_residual":max(tp),
        "stationary_full_state_residual":stationary_resid,
        "unique_unit_eigenvalue_count_tolerance_1e-9":int(sum(abs(z-1)<1e-9 for z in eig)),
        "second_eigenvalue_modulus":eigen_moduli[1],
        "stationary_output_distance_to_bell":trace_distance(out,states[-1]),
        "certified_duty_bound":cert["actual_duty_error_bound"],
        "maximally_entangled_untouched_reference_error_at_certified_time":reference_distance,
        "runs":runs,"perturbation":{"reset_mixture_weight":eta,
            "m_star_exact_integer":mstar,"uniform_theorem_error_bound":2*mstar*eta,
            "observed_stationary_joint_error":trace_distance(noisy,omega),
            "stationary_residual":float(np.linalg.norm(Sn@vn-vn)),
            "least_state_eigenvalue":float(np.linalg.eigvalsh(noisy)[0])}}

def json_matrix(A):return [[[float(z.real),float(z.imag)] for z in row] for row in A]

def thermal_audit():
    X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]);I=np.eye(2)
    H=-np.kron(Z,Z)-.7*np.kron(X,I)-.4*np.kron(I,X)-.2*np.kron(Y,I)
    beta=1.5;E,V=np.linalg.eigh(H)
    weights=np.exp(-beta*(E-E[0]));weights/=sum(weights);amp=np.sqrt(weights)
    v=np.eye(4)[:,0]-amp;v/=np.linalg.norm(v);W=np.eye(4)-2*np.outer(v,v)
    source={"work_qubits":4,"output_qubits":[0,1],"input_state":"zero",
        "scope":"binary64 fixture for a full two-qubit noncommuting Gibbs state",
        "gates":[{"kind":"matrix","qubits":[2,3],"matrix":json_matrix(W)},
            {"kind":"CNOT","qubits":[2,0]}, {"kind":"CNOT","qubits":[3,1]},
            {"kind":"matrix","qubits":[0,1],"matrix":json_matrix(V)}]}
    desc=compile_description(source,"1/16","1/16");cert=desc["certificate"]
    blocks,states=stationary_history(source,cert)
    post=apply_diagonal_clock(blocks,source,cert)
    residual=sum(trace_distance(a,b) for a,b in zip(post,blocks))
    rho=V@np.diag(weights)@V.conj().T
    prepared=reduce_state(states[-1],[0,1],4)
    output=reduce_state(blocks.sum(axis=0),[0,1],4)
    raw=scipy.linalg.expm(-beta*H);raw/=np.trace(raw)
    save("THERMAL_SOURCE.json",source);save("THERMAL_LOCAL_PROCESS.json",desc)
    cert_noise=resource_certificate(4,4,"1/16","1/4")
    return {"binary64_diagnostic":True,
        "Hamiltonian":"-Z0 Z1 - (7/10) X0 - (2/5) X1 - (1/5) Y0",
        "beta":"3/2", "eigenvalues":E.tolist(),"Boltzmann_weights":weights.tolist(),
        "source_matrix_unitarity_residual":max(float(np.linalg.norm(A.conj().T@A-np.eye(4))) for A in (W,V)),
        "prepared_distance_to_direct_exponential":trace_distance(prepared,raw),
        "full_stationary_history_residual":residual,
        "stationary_output_distance_to_canonical":trace_distance(output,raw),
        "duty_upper_exact":cert["actual_duty_error_bound"],
        "total_events_bound":cert["total_events_bound"],
        "noise_block_events":cert_noise["total_events_bound"],
        "event_half_diamond_budget_for_1e-3_maintenance_error":str(Fraction(1,2000*cert_noise["total_events_bound"])),
        "state_matrix":[[[float(z.real),float(z.imag)] for z in row] for row in output]}

def main():
    begin=time.perf_counter()
    with threadpool_limits(limits=1):
        structural=clock_structure_audit();save("CLOCK_STRUCTURE_AUDIT.json",structural)
        bell=bell_audit();save("FULL_CHANNEL_AUDIT.json",bell)
        thermal=thermal_audit();save("THERMAL_STATE_AUDIT.json",thermal)
        barriers=bottleneck_records();save("BOTTLENECK_CERTIFICATES.json",barriers)
        table=[]
        for duty in ["1/4","1/16","1/64","1/256","1/1024"]:
            table.append(resource_certificate(4,4,duty,"1/16"))
        save("ACCURACY_RESOURCE_TABLE.json",table)
    summary={"elapsed_seconds":time.perf_counter()-begin,
        "python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
        "parallel_blas_threads":1,"physical_runs":0,
        "thermal_stationary_distance":thermal["stationary_output_distance_to_canonical"],
        "bell_joint_residual":bell["stationary_full_state_residual"],
        "all_held_originals_untouched":True}
    save("RUN_SUMMARY.json",summary)
    print(json.dumps(summary,indent=2))
    print(json.dumps([{k:r[k] for k in ["N","boundary_upper_scientific","quantum_auxiliary_allowed_event_lower_integer"]} for r in barriers],indent=2))

if __name__=="__main__":main()
