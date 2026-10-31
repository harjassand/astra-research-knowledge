"""Finite cold-carrier model: full unitary, source-uniform effects, ST Choi.

All numbers are dimensionless.  No material/device units are invented.
The finite contact Hamiltonian is exact here.  Bias changes between contacts
are instantaneous in this numerical model; physical ramps need their own
duration and error estimate.  Helper Kraus operators compute probabilities,
not an assumption that the emitted helpers have been measured.  The short
full-cycle comparison explicitly retains them coherently.
"""
from pathlib import Path
import itertools
import json
import numpy as np
from scipy.linalg import expm, norm, eigvalsh

ROOT=Path(__file__).resolve().parent
X=np.array([[0.,1.],[1.,0.]])
Z=np.diag([1.,-1.])
I2=np.eye(2)
PARAMETERS={"lambda":1.,"t0":.12,"density_coupling_b":.07,
            "helper_flip":.025,"charge_shift":.06,
            "source_transverse_J":.08,"source_neighbor_XX":.055,
            "charging_sum_over_delta":4.}


def opnorm(a):
    return float(norm(a,2))


def source(spins,omega):
    j=PARAMETERS["source_transverse_J"]
    if spins==1:
        z1=Z; he=omega*Z+j*X
    elif spins==2:
        z1=np.kron(Z,I2)
        he=(omega*z1+.63*omega*np.kron(I2,Z)
            +j*np.kron(X,I2)+PARAMETERS["source_neighbor_XX"]*np.kron(X,X))
    else: raise ValueError("only one or two source spins are used")
    return he,z1


def contact(delta,omega,spins,kind,full_triplet=False,perfect=False):
    """Return exact data/source Kraus operators and operator certificates.

    Hamiltonian order is data, helper, source.  Kraus output/input order is
    data, source, after contracting the fresh input helper |0>.
    """
    he,z1=source(spins,omega)
    ds=he.shape[0]; nd=6 if full_triplet else 3
    eye_s=np.eye(ds)
    charging=PARAMETERS["charging_sum_over_delta"]*delta
    if kind=="capture_R": energies=[0.,charging+delta,-delta]
    elif kind=="return_R": energies=[0.,charging-delta,delta]
    elif kind=="return_L": energies=[0.,delta,charging-delta]
    else: raise ValueError(kind)
    if full_triplet: energies+= [0.,0.,0.]
    energies=np.array(energies)
    hopping=np.zeros((nd,nd))
    hopping[0,1]=hopping[1,0]=np.sqrt(2)
    hopping[0,2]=hopping[2,0]=np.sqrt(2)
    ec=(energies[:,None]+delta*np.array([0.,1.])[None,:]).reshape(-1)
    hc=np.kron(np.diag(ec),eye_s)
    common_source=np.kron(np.eye(nd*2),he)
    coupling=PARAMETERS["lambda"]*np.kron(np.kron(hopping,X),eye_s)
    shift=0. if perfect else PARAMETERS["charge_shift"]
    source_charge=np.array([0.,shift,-shift]+([0.,0.,0.] if full_triplet else []))
    conditional=np.kron(np.kron(np.diag(source_charge),I2),z1)
    if perfect:
        nuisance=np.zeros_like(coupling)
    else:
        gain=PARAMETERS["t0"]*eye_s+PARAMETERS["density_coupling_b"]*z1
        nuisance=(np.kron(np.kron(hopping,I2),gain)
                  +PARAMETERS["helper_flip"]*np.kron(np.kron(np.eye(nd),X),eye_s))
    residual=coupling+conditional+nuisance
    ee=np.repeat(ec,ds)
    differences=ee[:,None]-ee[None,:]
    same=np.isclose(differences,0.,atol=1e-12,rtol=0.)
    wmat=np.where(same,residual,0.)
    vmat=residual-wmat
    smat=np.zeros_like(vmat)
    np.divide(vmat,differences,out=smat,where=~same)
    s=opnorm(smat)
    comm=smat@common_source-common_source@smat
    c=opnorm(comm); w=opnorm(wmat); v=opnorm(vmat)
    amp=np.sqrt(2)*abs(PARAMETERS["lambda"])
    tau=np.pi/(2*amp)
    remainder_bound=np.exp(2*s)*(c+2*s*w+s*v)
    e_bound=2*s+tau*remainder_bound
    actual_h=hc+common_source+residual
    ref_h=hc+common_source+wmat
    actual=expm(-1j*actual_h*tau)
    reference=expm(-1j*ref_h*tau)
    rot=expm(smat)
    remainder=rot@actual_h@rot.conj().T-ref_h
    # Fresh helper input embedding.
    embed=np.zeros((nd*2*ds,nd*ds),complex)
    for d,e in itertools.product(range(nd),range(ds)):
        embed[(2*d)*ds+e,d*ds+e]=1
    ua=actual@embed; ur=reference@embed
    def make_kraus(u):
        return [u.reshape(nd,2,ds,nd*ds)[:,h,:,:].reshape(nd*ds,nd*ds) for h in range(2)]
    ka=make_kraus(ua); kr=make_kraus(ur)
    target=2 if kind in ("capture_R","return_R") else 1
    # Removing the mean source shift in the active block leaves d=|xiS-xij|/2.
    d_active=abs(source_charge[0]-source_charge[target])/2
    survival_bound=min(1.,d_active*tau)
    if kind=="capture_R":
        transient=[0]; sink=[1,2]
    else:
        transient=[target]; sink=[0]
    def block_indices(charges):
        return [d*ds+e for d in charges for e in range(ds)]
    ib=block_indices(transient); iff=block_indices(sink)
    surv=np.vstack([k[np.ix_(ib,ib)] for k in kr])
    sink_back=np.vstack([k[np.ix_(ib,iff)] for k in kr])
    stats={"kind":kind,"s":s,"c":c,"w":w,"v":v,
           "source_hamiltonian_norm":opnorm(he),"duration":tau,
           "resonant_amplitude":amp,"active_residual_d":d_active,
           "analytic_reference_survival_amplitude_bound":survival_bound,
           "exact_reference_survival_amplitude":opnorm(surv),
           "reference_sink_to_transient_amplitude":opnorm(sink_back),
           "contact_isometry_error_bound":e_bound,
           "actual_full_unitary_error":opnorm(actual-reference),
           "actual_fresh_helper_isometry_error":opnorm(ua-ur),
           "transformed_remainder_bound":remainder_bound,
           "actual_transformed_remainder_norm":opnorm(remainder),
           "S_antihermitian_residual":opnorm(smat+smat.conj().T),
           "commutator_cancellation_residual":opnorm(smat@hc-hc@smat+vmat),
           "kraus_completeness_residual":opnorm(sum(k.conj().T@k for k in ka)-np.eye(nd*ds)),
           "known_energy_blocks":sorted(set(ec.tolist()))}
    if full_triplet:
        triplet_errors=[]
        for k in ka:
            fine_source=k[3*ds:4*ds,3*ds:4*ds]
            target=np.zeros((nd*ds,3*ds),complex)
            target[3*ds:,:]=np.kron(np.eye(3),fine_source)
            triplet_errors.append(opnorm(k[:,3*ds:]-target))
        stats["full_triplet_fine_operator_factorization_residual"]=max(triplet_errors)
    assert stats["actual_full_unitary_error"]<=e_bound+1e-9
    assert stats["actual_transformed_remainder_norm"]<=remainder_bound+1e-8
    assert stats["exact_reference_survival_amplitude"]<=survival_bound+1e-9
    return ka,kr,stats,ds


def compose_kraus(after,before):
    return [a@b for b in before for a in after]


def survival_effects(kraus,ds,transient,counts):
    nd=kraus[0].shape[0]//ds
    p=np.zeros((nd*ds,nd*ds),complex)
    indices=[d*ds+e for d in transient for e in range(ds)]
    p[indices,indices]=1
    effect=p.copy(); out={}
    for n in range(1,max(counts)+1):
        effect=sum(k.conj().T@effect@k for k in kraus)
        effect=(effect+effect.conj().T)/2
        if n in counts:
            out[n]=float(eigvalsh(effect[np.ix_(indices,indices)])[-1])
    return out


def recurrence_bound(a,e,n):
    if a>=1: return 1.
    return min(1.,(a**n+e*(1-a**n)/(1-a))**2)


def parameter_case(delta,omega,spins):
    cap,cap_ref,sc,ds=contact(delta,omega,spins,"capture_R")
    rr,rr_ref,sr,_=contact(delta,omega,spins,"return_R")
    rl,rl_ref,sl,_=contact(delta,omega,spins,"return_L")
    macro=compose_kraus(rl,rr)
    macro_ref=compose_kraus(rl_ref,rr_ref)
    a_cap=sc["analytic_reference_survival_amplitude_bound"]
    a_ret=max(sr["analytic_reference_survival_amplitude_bound"],sl["analytic_reference_survival_amplitude_bound"])
    e_cap=sc["contact_isometry_error_bound"]
    e_ret=sr["contact_isometry_error_bound"]+sl["contact_isometry_error_bound"]
    counts=[1,2,4,8]
    pc=survival_effects(cap,ds,[0],counts)
    pr=survival_effects(macro,ds,[1,2],counts)
    ref_r=survival_effects(macro_ref,ds,[1,2],[1])[1]
    table=[]
    for n in counts:
        bc=recurrence_bound(a_cap,e_cap,n); br=recurrence_bound(a_ret,e_ret,n)
        assert pc[n]<=bc+1e-9
        assert pr[n]<=br+1e-9
        table.append({"capture_contacts":n,"return_macrosteps":n,
                      "return_contacts":2*n,
                      "worst_source_capture_miss":pc[n],
                      "analytic_capture_miss_bound":bc,
                      "worst_double_charge_source_return_failure":pr[n],
                      "analytic_return_failure_bound":br})
    assert ref_r<=a_ret*a_ret+1e-9
    return {"delta":delta,"omega":omega,"source_spins":spins,
            "capture":sc,"return_R":sr,"return_L":sl,
            "macro_reference_survival_amplitude":float(np.sqrt(max(0.,ref_r))),
            "macro_analytic_survival_amplitude_bound":a_ret,
            "macro_isometry_error_bound":e_ret,"pumping_table":table}


def common_outlet_trap():
    ds=1; amp=np.sqrt(2)*PARAMETERS["lambda"]; tau=np.pi/(2*amp)
    h=np.zeros((6,6),complex)
    # Data 0=S,1=DL,2=DR; helper index is the least-significant index.
    for d in [1,2]: h[1,2*d]=h[2*d,1]=amp
    u=expm(-1j*h*tau)
    embed=np.zeros((6,3),complex)
    embed[0,0]=embed[2,1]=embed[4,2]=1
    v=u@embed
    common=[v.reshape(3,2,3)[:,k,:] for k in range(2)]
    worst=survival_effects(common,1,[1,2],[1,2,4,8])
    minus=np.array([0.,1.,-1.])/np.sqrt(2)
    minus_survival=float(sum(np.vdot((k@minus)[1:],(k@minus)[1:]).real for k in common))
    # Exact separated resonant contacts with distinct fresh outgoing helpers.
    kr=[]
    for target in [2,1]:
        hh=np.zeros((6,6),complex)
        hh[1,2*target]=hh[2*target,1]=amp
        vv=expm(-1j*hh*tau)@embed
        kr.append([vv.reshape(3,2,3)[:,j,:] for j in range(2)])
    separated=compose_kraus(kr[1],kr[0])
    separated_worst=survival_effects(separated,1,[1,2],[1])[1]
    return {"common_outlet_worst_transient_survival_by_contacts":worst,
            "common_outlet_D_minus_survival":minus_survival,
            "separate_two_helper_macro_worst_transient_survival":separated_worst,
            "outgoing_helpers_retained_as_distinct_routes":True}


def append_helper(v,kraus):
    d,h,r=v.shape
    out=np.zeros((d,2*h,r),complex)
    for old,k in itertools.product(range(h),range(2)):
        out[:,2*old+k,:]=kraus[k]@v[:,old,:]
    return out


def low_rank_trace_norm(terms):
    nonzero=[(sign,v) for sign,v in terms if np.vdot(v,v).real>1e-28]
    if not nonzero: return 0.
    b=np.column_stack([v for _,v in nonzero])
    gram=b.conj().T@b
    es,vs=np.linalg.eigh((gram+gram.conj().T)/2)
    sqrtgram=(vs*np.sqrt(np.maximum(es,0.)))@vs.conj().T
    signs=np.diag([sign for sign,_ in nonzero])
    small=sqrtgram@signs@sqrtgram
    return float(np.sum(np.abs(eigvalsh((small+small.conj().T)/2))))


def full_st_choi_check():
    """Complete two-charge-read instrument, with coherent helper fields.

    The comparison instrument pinches the INPUT S/T label, uses the actual
    source/helper backaction on each sector, corrects the coarse ST report,
    and completes every singlet output into charge S.  It is therefore an
    exact ST instrument on data, including its retained auxiliary output.
    Its auxiliary fine charge records need not all denote a successful
    physical charge conversion; those records are deliberately retained.
    """
    delta=64.; omega=32.; spins=1; ncap=2; nmacro=1
    kc,_,sc,ds=contact(delta,omega,spins,"capture_R",full_triplet=True)
    krr,_,sr,_=contact(delta,omega,spins,"return_R",full_triplet=True)
    krl,_,sl,_=contact(delta,omega,spins,"return_L",full_triplet=True)
    dim=6*ds; din=4*ds
    logical=[0,3,4,5]  # loaded S and the three complete triplet vectors
    embedding=np.zeros((dim,din),complex)
    for j,d in enumerate(logical):
        for e in range(ds): embedding[d*ds+e,j*ds+e]=1
    v=embedding[:,None,:]/np.sqrt(din)
    for _ in range(ncap): v=append_helper(v,kc)
    projectors=[]
    for charges in [[0,3,4,5],[1],[2]]:
        p=np.zeros((dim,dim))
        for d in charges:
            for e in range(ds): p[d*ds+e,d*ds+e]=1
        projectors.append(p)
    blocks={}; actual_trace=0.; ideal_trace=0.; failure_prob=0.
    def add(key,sign,vector):
        blocks.setdefault(key,[]).append((sign,vector.reshape(-1)))
    for qc,p in enumerate(projectors):
        vc=np.einsum('ab,bhr->ahr',p,v)
        # Applying return contacts on all charge outcomes keeps real elapsed
        # contact time explicit.  The full triplet is exactly dark to hopping.
        # Any missed-S outcome was already charged at the capture stage.
        for _ in range(nmacro):
            vc=append_helper(vc,krr); vc=append_helper(vc,krl)
        for qf,pf in enumerate(projectors):
            branch=np.einsum('ab,bhr->ahr',pf,vc)
            label="T" if qc==0 else "S"
            add((qc,qf,label),+1,branch)
            actual_trace+=float(np.vdot(branch,branch).real)
            if qc!=0 and qf!=0: failure_prob+=float(np.vdot(branch,branch).real)
            # Ideal T sector: preserve all three triplet vectors and full field.
            ideal_t=branch.copy(); ideal_t[:,:,:ds]=0
            add((qc,qf,"T"),-1,ideal_t)
            ideal_trace+=float(np.vdot(ideal_t,ideal_t).real)
            # Ideal S sector: preserve its actual auxiliary state, return charge.
            ideal_s=branch.copy(); ideal_s[:,:,ds:]=0
            if qf in [1,2]:
                fixed=np.zeros_like(ideal_s)
                fixed[:ds,:,:]=ideal_s[qf*ds:(qf+1)*ds,:,:]
                ideal_s=fixed
            add((qc,qf,"S"),-1,ideal_s)
            ideal_trace+=float(np.vdot(ideal_s,ideal_s).real)
    distance=.5*sum(low_rank_trace_norm(terms) for terms in blocks.values())
    # Independent worst-input probability effects from the three-charge model.
    kcap,_,_,_=contact(delta,omega,spins,"capture_R")
    kretR,_,_,_=contact(delta,omega,spins,"return_R")
    kretL,_,_,_=contact(delta,omega,spins,"return_L")
    pmiss=survival_effects(kcap,ds,[0],[ncap])[ncap]
    pret=survival_effects(compose_kraus(kretL,kretR),ds,[1,2],[nmacro])[nmacro]
    effect_bound=np.sqrt(pmiss)+pmiss+pret
    ac=sc["analytic_reference_survival_amplitude_bound"]
    ar=max(sr["analytic_reference_survival_amplitude_bound"],sl["analytic_reference_survival_amplitude_bound"])
    pc_bound=recurrence_bound(ac,sc["contact_isometry_error_bound"],ncap)
    pr_bound=recurrence_bound(ar,sr["contact_isometry_error_bound"]+sl["contact_isometry_error_bound"],nmacro)
    recurrence_instrument_bound=min(1.,np.sqrt(pc_bound)+pc_bound+pr_bound)
    assert abs(actual_trace-1)<1e-9 and abs(ideal_trace-1)<1e-9
    assert distance<=effect_bound+1e-8
    return {"delta":delta,"omega":omega,"source_spins":spins,
            "capture_contacts":ncap,"return_macrosteps":nmacro,
            "total_coherent_outgoing_helpers":ncap+2*nmacro,
            "choi_input_dimension_including_source":din,
            "quantum_output_times_reference_vector_dimension":dim*2**(ncap+2*nmacro)*din,
            "ideal_charge_reads":2,"charge_read_error_assumed_in_this_check":0.,
            "actual_instrument_choi_trace":actual_trace,
            "comparison_ST_instrument_choi_trace":ideal_trace,
            "complete_record_choi_half_trace_distance":distance,
            "worst_source_capture_miss":pmiss,
            "worst_double_charge_source_return_failure":pret,
            "sqrt_pmiss_plus_pmiss_plus_preturn_from_exact_effects":float(effect_bound),
            "instrument_bound_from_analytic_contact_recurrences":float(recurrence_instrument_bound),
            "actual_return_failure_probability_on_choi_input":failure_prob,
            "maximum_contact_triplet_fine_factorization_residual":max(s["full_triplet_fine_operator_factorization_residual"] for s in [sc,sr,sl]),
            "meaning":"One full source/reference-entangled input check; not a diamond-norm computation. All emitted helpers remain coherent; both charge records are classical.",
            "endpoint_failure_records_retained":True}


def short_scalar_transfer_check():
    """Scalar transfer with arbitrary switched common source and detuning.

    Here d is the FULL norm bound on H_D(t)-H_S(t), not the half-difference
    used by centering the perturbation in the resonant pi-swap calculation.
    """
    a=np.sqrt(2)*PARAMETERS["lambda"]
    y=np.array([[0.,-1j],[1j,0.]])
    results=[]
    for ratio,omega,segments in itertools.product([0.,.1,1.,10.,100.],[0.,1e2,1e4],[1,7,63]):
        d=ratio*a
        tau=1/(2*(a+d))
        dt=tau/segments
        u=np.eye(4,dtype=complex)
        for j in range(segments):
            # Rapid switches of the common source are not averaged away.
            phase=.73*j
            he=((-1)**j*omega*Z+.08*(np.cos(phase)*X+np.sin(phase)*y))
            relative=d*(np.cos(.41*j)*Z+np.sin(.41*j)*X)
            hh=np.block([[he,a*I2],[a*I2,he+relative]])
            u=expm(-1j*hh*dt)@u
        transfer=u[2:,:2]
        minimum=float(np.linalg.svd(transfer,compute_uv=False)[-1])
        x=a*tau
        odd_bound=x-a*d*tau*tau/2-(np.sinh(x)-x)
        simple=x/np.sqrt(2)
        prob_bound=a*a/(8*(a+d)**2)
        assert odd_bound>=simple-1e-14
        assert minimum>=odd_bound-1e-9
        assert minimum**2>=prob_bound-1e-9
        results.append({"d_over_a":ratio,"common_source_scale":omega,
                        "source_switch_segments":segments,"duration":tau,
                        "minimum_transfer_singular_value":minimum,
                        "first_odd_minus_higher_odd_bound":float(odd_bound),
                        "simple_amplitude_bound":float(simple),
                        "simple_probability_bound":float(prob_bound),
                        "actual_worst_input_transfer_probability":minimum**2})
    return {"number_of_cases":len(results),
            "detuning_definition":"d bounds the full conditional Hamiltonian difference, not half its difference.",
            "min_actual_amplitude_over_odd_bound":min(r["minimum_transfer_singular_value"]/r["first_odd_minus_higher_odd_bound"] for r in results),
            "min_odd_bound_over_simple_amplitude":min(r["first_odd_minus_higher_odd_bound"]/r["simple_amplitude_bound"] for r in results),
            "cases":results}


def final_charge_measurement_cost():
    """A return-coherence counterexample with the helper fully retained."""
    p=1e-4
    # Basis |S,0>, |S,1>, |D,0>, |D,1>.
    ideal=np.zeros(4,complex); ideal[0]=1
    actual=np.sqrt(1-p)*ideal; actual[3]=np.sqrt(p)
    coherent=.5*low_rank_trace_norm([(1,actual),(-1,ideal)])
    # The measured success and failure records are distinct classical blocks.
    measured=.5*(abs((1-p)-1)+p)
    return {"return_failure_probability":p,
            "half_trace_distance_before_final_charge_read":coherent,
            "half_trace_distance_after_final_charge_read":measured,
            "square_root_probability":float(np.sqrt(p)),
            "helper_retained":True}


def source_resonance_counterexample():
    """Bare gaps fail if the source can supply that energy through G."""
    strength=.2; duration=np.pi/(2*strength)
    output=[]
    for gap in [16.,64.,256.]:
        hc=np.kron(np.diag([0.,gap]),I2)
        he=np.kron(I2,(gap/2)*Z)
        initial=np.array([1.,0.,0.,0.])
        row={"carrier_gap":gap,"source_level_splitting":gap,"duration":duration}
        for label,gain in [("density",strength*Z),("transition",strength*X)]:
            coupling=np.kron(X,gain)
            final=expm(-1j*(hc+he+coupling)*duration)@initial
            row[label+"_carrier_excitation_probability"]=float(np.vdot(final[2:],final[2:]).real)
            row[label+"_source_commutator_norm"]=opnorm(((gap/2)*Z)@gain-gain@((gap/2)*Z))
        row["density_uniform_excitation_bound"]=4*strength**2/(gap**2+4*strength**2)
        assert row["density_carrier_excitation_probability"]<=row["density_uniform_excitation_bound"]+1e-10
        assert row["transition_carrier_excitation_probability"]>1-1e-9
        output.append(row)
    return output


def main():
    cases=[]
    for delta in [16.,32.,64.,128.]:
        for omega in [0.,delta/2,20*delta,1e4]:
            cases.append(parameter_case(delta,omega,1))
    for delta,omega in [(32.,0.),(32.,1e4),(128.,0.),(128.,1e4)]:
        cases.append(parameter_case(delta,omega,2))
    trap=common_outlet_trap()
    choi=full_st_choi_check()
    short=short_scalar_transfer_check()
    summary=[]
    for case in cases:
        row=case["pumping_table"][2]
        summary.append({"delta":case["delta"],"omega":case["omega"],"source_spins":case["source_spins"],
                        "c_capture":case["capture"]["c"],
                        "e_capture_bound":case["capture"]["contact_isometry_error_bound"],
                        "capture_miss_after_4":row["worst_source_capture_miss"],
                        "capture_bound_after_4":row["analytic_capture_miss_bound"],
                        "return_failure_after_4_macros":row["worst_double_charge_source_return_failure"],
                        "return_bound_after_4_macros":row["analytic_return_failure_bound"]})
    result={"status":"All asserted finite-model inequalities passed.",
            "scope":{"dimensionless":True,"fresh_helpers_prepared_in_0":True,
                     "source_state_not_prepared_or_sampled":True,
                     "probability_bounds_use_maximum_eigenvalues":True,
                     "ramps_implemented":False,"physical_charge_detector_implemented":False,
                     "note":"Probability effects are exact finite-model operator checks; analytic inequalities are proved separately. Ideal charge reads in the Choi check do not certify a detector or a device."},
            "parameters":PARAMETERS,"cases":cases,"summary_table":summary,
            "common_outlet_counterexample":trap,"full_ST_instrument_choi":choi,
            "short_scalar_transfer":short,
            "final_charge_measurement_cost":final_charge_measurement_cost(),
            "source_resonance_counterexample":source_resonance_counterexample()}
    (ROOT/"cold_carrier_cycle_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"number_of_full_contact_parameter_cases":len(cases),
                      "representative_rows_at_source_scale_10000":[row for row in summary if row["omega"]==1e4 and row["source_spins"]==1],
                      "common_outlet_counterexample":trap,"full_ST_instrument_choi":choi,
                      "short_scalar_transfer_summary":{k:v for k,v in short.items() if k!="cases"},
                      "final_charge_measurement_cost":result["final_charge_measurement_cost"],
                      "source_resonance_counterexample":result["source_resonance_counterexample"]},indent=2))

if __name__=="__main__": main()
