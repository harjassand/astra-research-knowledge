"""Meaningful finite-dimensional checks of the new algebra and scope boundaries."""
import json, math, time
from pathlib import Path
import numpy as np
from scipy.linalg import expm, eigh
from threadpoolctl import threadpool_limits
from noise_absorption import *
from native_menu import solve_menu, sparse_generator
from rational_certificates import certificates

ROOT=Path(__file__).resolve().parent


def dump(name, obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2)+"\n")


def td(a,b): return .5*float(np.linalg.norm(a-b,ord="nuc"))


def circuit_matrix(n,gates):
    u=np.eye(2**n,dtype=complex)
    for g in gates:
        if g[0]=="H": local=np.array([[1,1],[1,-1]])/np.sqrt(2)
        elif g[0]=="CZ": local=np.diag([1,1,1,-1])
        else: raise ValueError(g)
        u=embed(local,g[1:],n)@u
    return u


def main():
    began=time.time()
    rng=np.random.default_rng(117031)
    # General complex KMS test: omitted Hamiltonian has a genuine defect.
    kms=[]
    for d in [2,3,4,8]:
        a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
        om=a@a.conj().T+np.eye(d)
        om/=np.trace(om)
        f=(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))/math.sqrt(d)
        rec=kms_complete(om,f)
        kms.append({"dimension":d,**{k:v for k,v in rec.items() if not isinstance(v,np.ndarray)}})
        assert rec["with_h_residual"]<1e-10
    dump("KMS_COMPLETION_AUDIT.json",kms)

    # A commuting interacting model checks the modular support cancellation.
    nint=4
    hfull=sum(embed(-.4*np.kron(Z,Z),[i,i+1],nint) for i in range(nint-1))
    hfull+=sum(embed(-.2*X*0-.2*Z,[i],nint) for i in range(nint))
    omfull=expm(-1.1*hfull);omfull/=np.trace(omfull)
    fp=.3*X+.2j*Z
    ffull=embed(fp,[1],nint)
    relevant=[0,1,2]
    hnear=embed(-.4*np.kron(Z,Z),[0,1],3)+embed(-.4*np.kron(Z,Z),[1,2],3)+embed(-.2*Z,[1],3)
    omnear=expm(-1.1*hnear);omnear/=np.trace(omnear)
    kfull=kms_complete(omfull,ffull)
    knear=kms_complete(omnear,embed(fp,[1],3))
    locality={"n":nint,"local_block_sites":relevant,
              "jump_locality_residual":float(np.linalg.norm(kfull["jump"]-embed(knear["jump"],relevant,nint))),
              "h_locality_residual":float(np.linalg.norm(kfull["h_correction"]-embed(knear["h_correction"],relevant,nint))),
              "full_stationarity_residual":kfull["with_h_residual"]}
    assert max(locality[k] for k in locality if k.endswith("residual"))<1e-10
    dump("COMMUTING_LOCALITY_AUDIT.json",locality)

    # Four physical qubits, finite-depth entangled target, local amplitude damping,
    # dephasing, and coherent drift. Every term is transformed using its light cone.
    n=4; probs=[.2,.2,.2,.2]
    gates=[("H",i) for i in range(n)]+[("CZ",0,1),("CZ",2,3),("CZ",1,2)]
    u=circuit_matrix(n,gates);tau=product_state(probs);sigma=u@tau@u.conj().T
    blocks=[]
    for i in range(n):
        def word(c): return "I"*i+c+"I"*(n-i-1)
        comp=compile_physical_block(n,probs,gates,{word("X"):.02},
              [{word("X"):.1,word("Y"):.1j},{word("Z"):.06}],margin=.05)
        blocks.append(comp)
    # Add gamma=1 single-bit reset to cover every logical factor independently.
    gamma=1.
    allh=np.zeros((2**n,2**n),complex);allf=[]
    expected=np.zeros((4**n,4**n),complex)
    coverage=np.full(n,gamma)
    for b in blocks:
        ss=b["support"]
        allh+=embed(b["h_noise"]+b["h_controller"],ss,n)
        allf.extend(embed(f,ss,n) for f in b["jumps_noise"]+b["jumps_controller"])
        coverage[ss]+=b["kappa"]
        for a in range(2**len(ss)):
            for c in range(2**len(ss)):
                mat=np.zeros((2**len(ss),2**len(ss)),complex)
                mat[a,c]=math.sqrt(b["kappa"]*b["omega"][a,a].real)
                expected+=noise_super(np.zeros_like(allh),[embed(mat,ss,n)])
    for i,p in enumerate(probs):
        for a,pr in enumerate([1-p,p]):
            for c in range(2):
                mat=np.zeros((2,2),complex);mat[a,c]=math.sqrt(gamma*pr)
                f=embed(mat,[i],n);allf.append(f)
                expected+=noise_super(np.zeros_like(allh),[f])
    total=noise_super(allh,allf)
    assert np.linalg.norm(total-expected,2)<1e-9
    d=2**n
    eigen=np.linalg.eigvals(total)
    gap=-max(x.real for x in eigen if abs(x)>1e-8)
    t=mixing_time(n,float(min(coverage)),.01)
    evol=expm(t*total)
    cpmin=float(np.linalg.eigvalsh((choi_from_super(evol,d)+choi_from_super(evol,d).conj().T)/2)[0])
    replacement=reset_super(tau)
    # Normalised Choi trace distance is an attained maximally entangled-reference test,
    # not an upper bound on diamond distance.
    ref_error=td(choi_from_super(evol,d)/d,choi_from_super(replacement,d)/d)
    tested=[]
    for _ in range(20):
        v=rng.normal(size=d)+1j*rng.normal(size=d);v/=np.linalg.norm(v)
        rho=np.outer(v,v.conj())
        final=(evol@rho.reshape(-1,order="F")).reshape(d,d,order="F")
        tested.append(td(final,tau))
    # Partial transpose across first two physical qubits: verifies nonproduct entanglement.
    pt=sigma.reshape(4,4,4,4).transpose(2,1,0,3).reshape(d,d)
    negativity=(np.linalg.norm(pt,ord="nuc")-1)/2
    audit={"n":n,"probabilities":probs,"gates":gates,"native_execution":"not performed",
           "largest_logical_block":max(len(b["support"]) for b in blocks),
           "coverage_rates":coverage.tolist(),"mixing_time_for_0.01":t,
           "complete_analytic_error_bound":sum(math.exp(-x*t) for x in coverage),
           "superoperator_reconstruction_residual":float(np.linalg.norm(total-expected,2)),
           "stationarity_residual":float(np.linalg.norm(total@tau.reshape(-1,order="F"))),
           "trace_preservation_residual":float(np.linalg.norm(np.eye(d).reshape(-1,order="F")@total)),
           "spectral_gap_numeric":float(gap),"stationary_eigenvalue_count":int(sum(abs(eigen)<1e-8)),
           "minimum_choi_eigenvalue_at_test_time":cpmin,
           "maximally_entangled_reference_error":ref_error,"max_20_pure_initial_state_error":max(tested),
           "target_physical_cut_negativity":float(negativity),
           "local_controller_activity_sum":sum(b["controller_activity"] for b in blocks),
           "local_controller_activity_upper_sum":sum(b["controller_activity_upper"] for b in blocks),
           "baseline_reset_jump_activity_upper":2*n*gamma,
           "blocks":[public_record(b,False) for b in blocks]}
    assert negativity>0 and max(tested)<=audit["complete_analytic_error_bound"]+1e-9
    assert ref_error<=audit["complete_analytic_error_bound"]+1e-9
    dump("GRAPH_STATE_AUDIT.json",audit)
    dump("GRAPH_STATE_CONTROLLER_BINARY64.json",{"status":"binary64 logical generator data, not certified physical implementation", "n":n,"probabilities":probs,"gates":gates,"baseline_reset_rate":gamma,"blocks":[public_record(b) for b in blocks]})

    # Native-menu LP: exact rational certificates supply the interpretation.
    z2=np.zeros((2,2),complex)
    down=np.array([[0,1],[0,0]],complex);up=down.T
    noise=[{"support":[0],"super":noise_super(z2,[X])}]
    records=[]
    for cap in [7,5,2]:
        controls=[{"name":name,"support":[0],"super":noise_super(z2,[jump]),"cap":c,"cost":1.}
                  for name,jump,c in [("Y",Y,1.2),("Z",Z,3.),("down",down,cap),("up",up,1.)]]
        for mode in ["reset","stationarity"]:
            rec=solve_menu(1,[.2],noise,controls,coverage_rate=1.,mode=mode)
            rec["downward_cap"]=cap;records.append(rec)
    expected_status=[True,True,False,True,False,False]
    assert [x["success"] for x in records]==expected_status
    dump("NATIVE_MENU_AUDIT.json",records)
    dump("EXACT_RATIONAL_CERTIFICATES.json",certificates())

    # Two overlapping local blocks test sparse FULL-generator assembly, not only
    # the one-site population fixture. Dense matrices are used only to audit n=3.
    small_probs=[.3,.25,.35]; nb=3
    nc=[]; cc=[]; bc=[]
    for ss in [[0,1],[1,2]]:
        hs=.03*np.kron(X,Z)
        fs=[.2*np.kron(down,I),.11*np.kron(Z,X)]
        om=product_state([small_probs[i] for i in ss])
        comp=complete_to_reset(om,hs,fs)
        bc.append((ss,comp,hs,fs,om))
        nc.append({"support":ss,"super":comp["noise_super"]})
        cc.append({"support":ss,"super":comp["controller_super"],"cap":1.,"cost":1.,"name":str(ss)})
    overlap=solve_menu(nb,small_probs,nc,cc,reset_blocks=[[0,1],[1,2]],coverage_rate=.1,mode="reset")
    assert overlap["success"]
    lhs=np.zeros((64,64),complex);rhs=np.zeros_like(lhs)
    for j,(ss,comp,hs,fs,om) in enumerate(bc):
        rate=overlap["control_rates"][str(ss)]
        lhs+=noise_super(embed(hs,ss,nb),[embed(f,ss,nb) for f in fs])
        lhs+=rate*noise_super(embed(comp["h_controller"],ss,nb),[embed(f,ss,nb) for f in comp["jumps_controller"]])
        for a in range(4):
            for c in range(4):
                mat=np.zeros((4,4),complex);mat[a,c]=np.sqrt(overlap["reset_rates"][j]*om[a,a].real)
                rhs+=noise_super(np.zeros((8,8)),[embed(mat,ss,nb)])
    overlap["independent_dense_equality_residual"]=float(np.linalg.norm(lhs-rhs,2))
    assert overlap["independent_dense_equality_residual"]<1e-9
    dump("OVERLAPPING_MENU_AUDIT.json",overlap)

    # Random complex local blocks independently audit the CCP-vs-CP rate and sum.
    randoms=[]
    for d in [2,3,4]:
        a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));om=a@a.conj().T+np.eye(d);om/=np.trace(om)
        h=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));h=(h+h.conj().T)/10
        fs=[(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))/10 for _ in range(2)]
        c=complete_to_reset(om,h,fs)
        assert c["kappa_ccp"]<=c["kappa_cp"]+1e-10 and c["reconstruction_residual"]<1e-10
        test_cp=superoperator(lambda x:fs[0]@x@fs[0].conj().T,d)
        choi_check=np.linalg.norm(choi_from_super(test_cp,d)-np.outer(fs[0].reshape(-1),fs[0].reshape(-1).conj()))
        assert choi_check<1e-12
        c["independent_choi_convention_residual"]=float(choi_check)
        randoms.append({"dimension":d,**public_record(c,False)})
    dump("GENERAL_COMPLEX_AUDIT.json",randoms)
    summary={"elapsed_seconds":time.time()-began,"all_assertions_passed":True,
             "no_physical_experiment":True,"no_unknown_noise_acquired":True,
             "numerics":"Python/NumPy/SciPy binary64; exact Fraction certificates separately labelled",
             "graph_mix_time":t,"graph_complete_bound":audit["complete_analytic_error_bound"],
             "graph_ref_error":ref_error,"graph_negativity":float(negativity),
             "native_status_sequence":[x["success"] for x in records]}
    dump("RUN_SUMMARY.json",summary)
    print(json.dumps(summary,indent=2))


if __name__=="__main__":
    with threadpool_limits(limits=1): main()
