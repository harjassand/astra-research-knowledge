"""Reproducible exact algebra audits and labeled finite matrix diagnostics."""
import json
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
from gain_certificate import certify
from thermal_controller import *
from resource_bounds import select_radii, schedule, noise_completion_error

OUT = Path(__file__).resolve().parent


def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2)+"\n")


def exact_gain_audits():
    e = [[Q(1,8),Q(1,16),0],[Q(1,16),Q(1,8),Q(1,16)],[0,Q(1,16),Q(1,8)]]
    b = [Q(3,10),Q(2,5),Q(1,2)]
    ok = certify(e,b,caps=[1,1,1],prices=[2,3,4])
    assert ok["feasible_balance"] and ok["within_caps"]
    unreachable = certify([[Q(1,2),0],[0,2]],[1,0])
    assert unreachable["x"] == ["2","0"]
    critical = certify([[1]],[1])
    assert not critical["feasible_balance"]
    unstable = certify([[2]],[1])
    assert not unstable["feasible_balance"]
    capped = certify(e,b,caps=[Q(1,100)]*3)
    assert not capped["within_caps"]
    # Nonstationary up/down noises cancel at a faithful target even though
    # a componentwise repair loop with E=2I cannot balance positive b.
    p = Q(3,4)
    bdown, bup = p, 1-p
    drift = bdown*(1-p)-bup*p
    assert drift == 0
    return {"subcritical":ok,"unreachable_unstable_mode":unreachable,
            "reachable_critical":critical,"reachable_supercritical":unstable,
            "capacity_failure":capped,
            "balance_failure_is_not_all_control_failure":{
                "target_ground_population":str(p),"noise_rates":[str(bdown),str(bup)],
                "gain_E":"2 I", "stationarity_drift_with_no_repairs":str(drift),
                "balance_test":certify([[2,0],[0,2]],[bdown,bup])}}


def finite_quantum_audit():
    n, beta = 3, 0.65
    d = 2**n
    h = (0.37*two_site(Z,0,Z,1,n)+0.29*two_site(X,1,Y,2,n)
         +0.23*onsite(X,0,n)-0.17*onsite(Z,1,n)+0.19*onsite(Y,2,n))
    assert np.linalg.norm(h-h.conj().T) < 1e-13
    sigma = gibbs(h,beta)
    sv = sigma.reshape(-1,order="F")
    base = np.zeros((d*d,d*d),complex)
    gram_records=[]
    for i in range(n):
        li,jumps,g,meta = ckg_site(h,[onsite(a/2,i,n) for a in (X,Y,Z)],beta)
        base += li
        gram_records.append(meta)
    fs = [onsite(DOWN,0,n),onsite(X,1,n),onsite((X+0.3j*Z)/1.3,2,n)]
    ds,cs,ps=[],[],[]
    for f in fs:
        j,g=complete_noise(h,f,beta)
        di=dissipator(f)
        ci=dissipator(j)+commutator(g)
        ds.append(di);cs.append(ci);ps.append(di+ci)
    e = np.array([[1/8,1/16,0],[1/16,1/8,1/16],[0,1/16,1/8]])
    b = np.array([.3,.4,.5])
    xx = np.linalg.solve(np.eye(3)-e,b)
    actual = base.copy()
    ideal_balanced = base.copy()
    for i in range(3):
        actual += (b+e@xx)[i]*ds[i]+xx[i]*cs[i]
        ideal_balanced += xx[i]*ps[i]
    identity = np.eye(d).reshape(-1,order="F")
    records={"status":"binary64 diagnostic, no physical data or certified CMLSI constant",
        "sites":n,"inverse_temperature":beta,"complex_noncommuting_H":True,
        "base_stationarity_residual":float(np.linalg.norm(base@sv)),
        "pair_stationarity_residuals":[float(np.linalg.norm(z@sv)) for z in ps],
        "actual_stationarity_residual":float(np.linalg.norm(actual@sv)),
        "native_identity_residual":float(np.linalg.norm(actual-ideal_balanced)),
        "trace_preservation_residual":float(np.linalg.norm(identity.conj()@actual)),
        "gram_records":gram_records}
    assert records["base_stationarity_residual"] < 1e-10
    assert records["actual_stationarity_residual"] < 1e-10
    assert records["native_identity_residual"] < 1e-10
    # A retained qubit reference, with a nontrivial faithful entangled input.
    rng=np.random.default_rng(20261107)
    z=rng.normal(size=2*d)+1j*rng.normal(size=2*d)
    z/=np.linalg.norm(z)
    rho=.83*np.outer(z,z.conj())+.17*np.eye(2*d)/(2*d)
    pt=rho.reshape(d,2,d,2).transpose(0,3,2,1).reshape(2*d,2*d)
    pt_min=float(np.linalg.eigvalsh(pt).min())
    assert pt_min < -1e-3
    records["initial_reference_partial_transpose_min_eigenvalue"] = pt_min
    omega=np.trace(rho.reshape(d,2,d,2),axis1=0,axis2=2)
    target=np.kron(sigma,omega)
    entropy0=entropy_relative(rho,target)
    # Independently test that a sigma-stationary repair addition cannot
    # produce positive relative-entropy drift at a generic joint state.
    kadd=sum(xx[i]*ps[i] for i in range(3))
    dt=1e-6
    rhoadd=apply_with_reference(expm(dt*kadd),rho,d,2)
    drift=(entropy_relative(rhoadd,target)-entropy0)/dt
    assert drift < 1e-7
    rows=[]
    for t in [0,.25,.5,1,2,4,8,12,20,30]:
        r=apply_with_reference(expm(t*actual),rho,d,2)
        rows.append({"time":t,"joint_trace_distance":trace_distance(r,target),
                     "joint_relative_entropy":entropy_relative(r,target)})
    assert rows[-1]["joint_trace_distance"] < rows[0]["joint_trace_distance"]*1e-3
    records["stationary_addition_joint_entropy_derivative"] = drift
    records["joint_reference_trajectory"] = rows
    records["spectral_gap_diagnostic_not_CMLSI"] = float(-np.sort(np.linalg.eigvals(actual).real)[-2])
    # Save an inspectable actual finite coefficient instance.
    np.savez_compressed(OUT/"FINITE_CONTROLLER_BINARY64.npz",H=h,beta=beta,
                        sigma=sigma,E=e,b=b,x=xx,base=base,actual=actual,
                        noise=np.array(ds),repairs=np.array(cs),rho_reference=rho)
    return records


def locality_and_integral_audit():
    n=6; beta=.3; strength=.5
    terms=[]
    for i in range(n):
        terms.append(({i},.15*onsite(X,i,n)))
    for i in range(n-1):
        terms.append(({i,i+1},.07*two_site(Z,i,Z,i+1,n)+.06*two_site(Y,i,Y,i+1,n)))
    h=sum(z for _,z in terms)
    center=2; f=onsite((X+.2j*Z)/1.2,center,n)
    j,g=complete_noise(h,f,beta)
    rows=[]
    for r,q in [(0,1),(0,2),(1,1),(1,2),(2,1)]:
        inner=set(range(max(0,center-r),min(n,center+r+1)))
        outer=set(range(max(0,center-r-q),min(n,center+r+q+1)))
        hi=sum((z for s,z in terms if s <= inner),start=np.zeros_like(h))
        ho=sum((z for s,z in terms if s <= outer),start=np.zeros_like(h))
        jr,_=complete_noise(hi,f,beta)
        kr=f.conj().T@f+jr.conj().T@jr
        gr=coherent(ho,kr,beta)
        je=float(np.linalg.norm(j-jr,2)); ge=float(np.linalg.norm(g-gr,2))
        bound=noise_completion_error(r,q,beta,strength)
        assert je <= bound["jump_error_upper"]+1e-12
        assert ge <= bound["coherent_error_upper"]+1e-12
        rows.append({"inner_radius":r,"extra_radius":q,"actual_jump_error":je,
                     "actual_coherent_error":ge,"analytic_bounds_binary64":bound})
    integrals=[]
    for u,v in [(-3.,1.),(.2,.7),(0.,0.),(4.,-2.)]:
        numeric,err=quad(lambda x: np.exp(-(x+1)**2/2-((x-u)**2+(x-v)**2)/4)/np.sqrt(2*np.pi),
                         -np.inf,np.inf,epsabs=1e-13,epsrel=1e-13)
        analytic=np.exp(-.5-(u*u+v*v)/4+(u+v-2)**2/16)/np.sqrt(2)
        assert abs(numeric-analytic) < 1e-12
        integrals.append({"u":u,"v":v,"quadrature":numeric,"closed_form":float(analytic),
                          "absolute_difference":float(abs(numeric-analytic))})
    return {"status":"binary64 operator and independent quadrature diagnostics",
            "locality_sites":n,"locality_cases":rows,"Gaussian_cross_frequency_integrals":integrals}


def finite_resources():
    # Supplied theoretical parameter scenarios. Not calibration, measured
    # throughput, or a numerical extraction of the source's MLSI constant.
    rows=[]
    for n in [100,10000,1000000]:
        beta=.2; strength=1.; eps=.01; alpha=.1; u=1.; gain=.25
        aa=max(1.,np.sqrt(n*(np.log(2)+beta*strength)))
        mem=(1+np.log(aa))/(u*alpha)
        eta=eps/(4*mem)
        percenter=eta/(n*(1+1/(1-gain)))
        nr=select_radii(percenter,beta,strength,"noise")
        sr=select_radii(percenter,beta,strength,"ckg")
        w=min(n,max(nr["window_sites_upper"],sr["window_sites_upper"]))
        rows.append({"N":n,"epsilon":eps,"beta":beta,"J":strength,
            "alpha":alpha,"alpha_status":"illustrative supplied parameter, not inferred",
            "gain_row_sum_bound":gain,"allowed_total_generator_half_diamond":eta,
            "percenter_tolerance":percenter,"noise_window":nr,"sampler_window":sr,
            "dense_compiler_log10_D6":float(6*w*np.log10(2)),
            "schedule":schedule(n,2,beta,strength,alpha,u,eps,eta)})
    return {"status":"conditional analytic-bound scenarios evaluated in binary64",
            "dense_cost_warning":"The sufficient windows can be enormous; polynomial does not mean economical.",
            "rows":rows}


if __name__ == "__main__":
    gain=exact_gain_audits();dump("EXACT_GAIN_CERTIFICATES.json",gain)
    q=finite_quantum_audit();dump("FINITE_QUANTUM_DIAGNOSTIC.json",q)
    loc=locality_and_integral_audit();dump("LOCALITY_DIAGNOSTIC.json",loc)
    res=finite_resources();dump("RESOURCE_SCENARIOS.json",res)
    summary={"exact_gain_cases":6,"finite_quantum_sites":q["sites"],
             "locality_operator_cases":len(loc["locality_cases"]),
             "independent_Gaussian_integrals":len(loc["Gaussian_cross_frequency_integrals"]),
             "base_stationarity_residual":q["base_stationarity_residual"],
             "actual_stationarity_residual":q["actual_stationarity_residual"],
             "joint_final_trace_distance":q["joint_reference_trajectory"][-1]["joint_trace_distance"],
             "physical_experiment":False,"all_assertions_passed":True}
    dump("RUN_SUMMARY.json",summary)
    print(json.dumps(summary,indent=2))
