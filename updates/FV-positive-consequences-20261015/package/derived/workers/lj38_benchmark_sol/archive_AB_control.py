"""Exact classical GT control for the archive's A=1..5, B=6..400 sets.

The sets are used only as archived terminal lists, without funnel labels.
MFPT initial distributions are original equilibrium weights conditioned on A
or B. They are not the exact capacity-related exit distribution.
"""
from pathlib import Path
import json,math,os,resource,sys,time
sys.dont_write_bytecode=True
import numpy as np
from scipy import linalg
from scipy.linalg.blas import dsyr
from run_classical import load_model
from positive_elimination import eliminate

HERE=Path(__file__).resolve().parent
def main():
    st=time.perf_counter();u0=resource.getrusage(resource.RUSAGE_SELF)
    p,c,w,ids,load=load_model(.2);z=math.fsum(w)
    ta=np.flatnonzero((ids>=1)&(ids<=5));tb=np.flatnonzero((ids>=6)&(ids<=400));keep=np.r_[ta,tb]
    ia=w[ta]/math.fsum(w[ta]);ib=w[tb]/math.fsum(w[tb])
    ss,core=eliminate(p,c,w,int(ta[0]),int(tb[0]),seconds=50.,edge_cap=500000,return_core=True,keep_extra=keep)
    n=len(core["w"]);assert n<5000
    mapping={int(old):i for i,old in enumerate(core["component_indices"])}
    retained=np.array([mapping[int(i)] for i in keep]);order=np.r_[[i for i in range(n) if i not in set(retained)],retained]
    remap=np.empty(n,dtype=np.int64);remap[order]=np.arange(n)
    q=np.sort(remap[core["pairs"]],axis=1);a=np.zeros((n,n),order="F");a[q[:,0],q[:,1]]=core["c"]
    mass=core["w"][order].copy();loc=0;dense_st=time.perf_counter()
    while len(mass)-loc>len(keep):
        if time.perf_counter()-st>52:raise TimeoutError("52s overall budget")
        v=np.r_[a[:loc,loc],0.,a[loc,loc+1:]];den=math.fsum(v)
        mass+=mass[loc]*(v/den);mass[loc]=0
        a=dsyr(1/den,v,a=a,lower=0,overwrite_a=1);a[:loc,loc]=0;a[loc,loc:]=0;np.fill_diagonal(a,0)
        loc+=1
        if loc>=64 and len(mass)-loc>len(keep):
            a=np.array(a[loc:,loc:],order="F");mass=mass[loc:];loc=0
    a=a[-len(keep):,-len(keep):];a=np.triu(a,1);a=a+a.T;mass=mass[-len(keep):]
    ll=np.diag(a.sum(axis=0))-a;na=len(ta)
    ma=linalg.solve(ll[:na,:na],mass[:na],assume_a="pos");mb=linalg.solve(ll[na:,na:],mass[na:],assume_a="pos")
    cap=float(a[:na,na:].sum())
    out={"status":"complete","temperature":.2,"A_archive_ids":[1,2,3,4,5],"B_archive_id_range":[6,400],
         "A_count":len(ta),"B_count":len(tb),"component_nodes":len(w),"component_Z":z,
         "terminal_sets_label":"as supplied by archive, no FCC/ICO basin interpretation",
         "initial_distribution":"original HTST equilibrium weights conditioned separately within A and B",
         "capacity_AB_omitting_1_over_2pi":cap,"reactive_equilibrium_flux_AB_HTST":cap/z/(2*math.pi),
         "equilibrium_weighted_MFPT_A_to_B_HTST":float(ia@ma*2*math.pi),
         "equilibrium_weighted_MFPT_B_to_A_HTST":float(ib@mb*2*math.pi),
         "MFPT_A_state_values_HTST":(ma*2*math.pi).tolist(),
         "mass_drift_relative":float(math.fsum(mass)/z-1),"total_from_raw_tables_seconds":time.perf_counter()-st,
         "model_phase":load,"sparse_phase":ss,"dense_and_terminal_solve_seconds":time.perf_counter()-dense_st,
         "terminal_linear_relative_residual_A":float(np.max(np.abs(ll[:na,:na]@ma-mass[:na]))/np.max(mass[:na])),
         "terminal_linear_relative_residual_B":float(np.max(np.abs(ll[na:,na:]@mb-mass[na:]))/np.max(mass[na:])),
         "peak_rss_bytes_macos":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         "thread_environment":{k:os.environ.get(k) for k in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","VECLIB_MAXIMUM_THREADS")},
         "arithmetic":"float64 positive exact-elimination baseline plus small positive-definite terminal solves; no rounding certificate"}
    u1=resource.getrusage(resource.RUSAGE_SELF);out["process_cpu_seconds_in_timed_pipeline"]=(u1.ru_utime+u1.ru_stime)-(u0.ru_utime+u0.ru_stime)
    (HERE/"ARCHIVE_AB_CONTROL.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
