"""Finite, reversible kinetic construction for a removable RNA assembly gate.

This is NOT a fitted ribosome model or a molecular validation. It tests the
proposed control mechanism without instantaneous capture/release, free reset,
infinite antidote, or an irreversible molecular helper. Rates are illustrative.
Concentrations and time are dimensionless. scipy/numpy/matplotlib only.
"""
from pathlib import Path
import os
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

OUT = Path(__file__).resolve().parent / "results"
OUT.mkdir(exist_ok=True)
# RNA states: unfolded, locally ready, misdocked, native, and three gate-bound
# versions. Additional species: free guide, antidote, spent duplex; native-time.
U,C,M,N,UG,CG,MG,G,A,W,SERVICE,RESETS = range(12)
E = np.array([0., -3., -4., -12., -8., -11., -12.])

def rhs(t,y, selective=0.002, local_fold=1., release=50.,
        affinity=22., native_energy_shift=0., reset=0.):
    z=np.maximum(y,0.)
    d=np.zeros(12)
    energies=E.copy();energies[N]+=native_energy_shift
    def rx(i,j,k):
        # Two-state thermal edge. k is forward rate, reverse fixed by energies.
        v=k*z[i]-k*np.exp(energies[j]-energies[i])*z[j]
        d[i]-=v; d[j]+=v
    rx(U,C,1.); rx(U,M,3.); rx(C,N,2.); rx(C,M,0.02)
    rx(UG,CG,local_fold); rx(UG,MG,3.*selective); rx(CG,MG,0.02)
    # Equal binding free energies for U,C,M. This makes all chemical cycles
    # obey local detailed balance. Native RNA is assumed inaccessible to G.
    kb=np.exp(8.)
    for free,bound in [(U,UG),(C,CG),(M,MG)]:
        v=50.*z[free]*z[G]-(50./kb)*z[bound]
        d[free]-=v;d[G]-=v;d[bound]+=v
        # RNAG + A <-> RNA + W, with W binding free energy -affinity.
        v=release*z[bound]*z[A]-release*np.exp(8.-affinity)*z[free]*z[W]
        d[bound]-=v;d[A]-=v;d[free]+=v;d[W]+=v
    v=100.*z[G]*z[A]-100.*np.exp(-affinity)*z[W]
    d[G]-=v;d[A]-=v;d[W]+=v
    # Optional, explicitly supplied nonthermal services/lesions for stress tests.
    v=reset*z[M]
    d[M]-=v;d[U]+=v
    d[RESETS]=v
    d[SERVICE]=z[N]
    return d

def simulate(guide=0.,pulse=None,antidote_ratio=2.,horizon=15.,
             premixed=False,dense=False,**kw):
    y=np.zeros(12);y[U]=1.;y[G]=guide
    if premixed:
        # Exact prehybridization control: no RNA has yet seen free gate.
        y[G]=0.;y[W]=guide;y[A]=(antidote_ratio-1.)*guide
        pulse=None
    times=[0.,horizon] if pulse is None else [0.,float(pulse),horizon]
    curves=[]
    for k,(ta,tb) in enumerate(zip(times[:-1],times[1:])):
        if k: y[A]+=antidote_ratio*guide
        if tb==ta: continue
        sol=solve_ivp(lambda t,z:rhs(t,z,**kw),(ta,tb),y,method="LSODA",
                      rtol=2e-8,atol=2e-10,
                      t_eval=np.linspace(ta,tb,151) if dense else None)
        assert sol.success
        y=sol.y[:,-1]
        if dense:curves.append((sol.t,sol.y))
    rna=float(y[:7].sum()); gate=float(y[[UG,CG,MG,G,W]].sum())
    assert abs(rna-1)<1e-7 and abs(gate-guide)<1e-7
    supplied=antidote_ratio*guide if pulse is not None or premixed else 0.
    assert abs(y[A]+y[W]-supplied)<1e-7
    return {"native_fraction":float(y[N]),"integrated_native_time":float(y[SERVICE]),
            "rna_total":rna,"guide_total":gate,"antidote_supplied":supplied,
            "spent_duplex":float(y[W]),"free_antidote":float(y[A]),
            "residual_bound_gate":float(y[[UG,CG,MG]].sum()),
            "supplied_selective_reset_events":float(y[RESETS]),
            "final_state":y.tolist()},curves

def optimize_pulse(guide=1.2,**kw):
    horizon=kw.get("horizon",15.)
    # Coarse grid brackets possible nonunimodal behavior; then refine locally.
    ts=np.linspace(0.,horizon,51)
    vs=[simulate(guide=guide,pulse=t,**kw)[0]["integrated_native_time"] for t in ts]
    i=int(np.argmax(vs));lo=ts[max(0,i-1)];hi=ts[min(len(ts)-1,i+1)]
    o=minimize_scalar(lambda t:-simulate(guide=guide,pulse=t,**kw)[0]["integrated_native_time"],
                      bounds=(lo,hi),method="bounded",options={"xatol":2e-4})
    result=simulate(guide=guide,pulse=o.x,**kw)[0]
    return {"release_time":float(o.x),**result}

def run():
    base=simulate()[0]
    controls=np.r_[0.,np.geomspace(1e-4,2.,50)]
    static=[(g,simulate(guide=g)[0]) for g in controls]
    gs,bs=max(static,key=lambda x:x[1]["integrated_native_time"])
    best=optimize_pulse()
    pre=simulate(guide=1.2,premixed=True)[0]
    slow=optimize_pulse(release=.02)
    noselect=optimize_pulse(selective=1.,local_fold=1.)
    blockall=optimize_pulse(selective=.002,local_fold=.002)
    thermal=simulate(reset=1.)[0]
    weakdrive=optimize_pulse(affinity=9.)
    unstable=optimize_pulse(native_energy_shift=9.)
    unstable_base=simulate(native_energy_shift=9.)[0]
    broad_opt=minimize_scalar(lambda logr:-simulate(guide=1.2,pulse=.1,release=np.exp(logr))[0]["integrated_native_time"],
                             bounds=(-6.,4.),method="bounded")
    broad={"pulse_time":.1,"release_rate":float(np.exp(broad_opt.x)),
           **simulate(guide=1.2,pulse=.1,release=np.exp(broad_opt.x))[0]}
    srows=[]
    for leak in [0.001,.01,.1,.5,1.]:
        rr=optimize_pulse(selective=leak)
        srows.append({"relative_misdocking_rate":leak,"release_time":rr["release_time"],
                      "native_time":rr["integrated_native_time"],
                      "native_fraction":rr["native_fraction"]})
    res={"scope":"Unfitted, dimensionless mass-action existence and failure test; no ribosome rate or yield is inferred.",
         "normalization":"one newly supplied RNA; no internal-state feedback; fixed timed antidote pulse",
         "local_detailed_balance":{"RNA_state_energies_kBT":E.tolist(),
             "guide_binding_free_energy_kBT":-8.,"duplex_binding_free_energy_kBT":-22.,
             "release_standard_free_energy_kBT":-14.,
             "chemical_cycle_log_residual":float(np.log(np.exp(8.))+np.log(np.exp(14.))-np.log(np.exp(22.)))},
         "unassisted":base,"best_static_guide_on_grid":{"guide":float(gs),**bs},
         "timed_finite_gate":{"guide":1.2,**best},"prehybridized_control":pre,
         "slow_release":slow,"nonselective_gate":noselect,"blocks_all_folding":blockall,
         "weak_antidote_drive":weakdrive,"postrelease_instability":unstable,
         "matched_unassisted_instability":unstable_base,
         "broad_finite_release_after_early_pulse":broad,
         "supplied_ideal_selective_reset_comparator":thermal,
         "selectivity_sweep":srows,
         "critical_unearned_transfer":"Existing RNA-bound splint release has not demonstrated release from a protein-coated ribosome assembly intermediate. Supplied favorable properties are capture/access before wrong folding, wrong-path suppression while useful local folding continues, fast postbinding release, and native-state exclusion from guide binding. All numeric rates need measurement; no resource superiority follows."}
    (OUT/"assembly_gate_results.json").write_text(json.dumps(res,indent=2)+"\n")
    os.environ.setdefault("MPLCONFIGDIR",str(OUT/".mplcache"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(1,2,figsize=(10.2,3.7),layout="constrained")
    for label,kwargs in [("No guide",{}),("Best static guide",{"guide":float(gs)}),
                         ("Timed guide + finite release",{"guide":1.2,"pulse":best["release_time"]}),
                         ("Slow release",{"guide":1.2,"pulse":slow["release_time"],"release":.02})]:
        _,curves=simulate(dense=True,**kwargs)
        axs[0].plot(np.concatenate([x[0] for x in curves]),np.concatenate([x[1][N] for x in curves]),label=label)
    axs[0].set(xlabel="Dimensionless time",ylabel="Native fraction",title="Finite capture and release")
    axs[0].legend(fontsize=8,frameon=False)
    axs[1].semilogx([r["relative_misdocking_rate"] for r in srows],
                   [r["native_time"] for r in srows],"o-",label="Optimized release time")
    axs[1].axhline(base["integrated_native_time"],color="k",linestyle="--",label="No guide")
    axs[1].set(xlabel="Misdocking rate under guide / without guide",ylabel="Integrated native time",title="A selective kinetic gate is essential")
    axs[1].legend(fontsize=8,frameon=False)
    fig.suptitle("Mechanism test only — rates are not fitted to ribosome data",fontsize=11)
    fig.savefig(OUT/"assembly_gate.png",dpi=180)
    print(json.dumps({k:v for k,v in res.items() if k not in ["selectivity_sweep"]},indent=2))

if __name__=="__main__":run()
