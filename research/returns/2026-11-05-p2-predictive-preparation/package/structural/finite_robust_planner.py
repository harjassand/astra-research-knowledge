"""Construct and exactly certify a finite smooth-input robust planner.

Only acquired_step_response.json and declared budgets are consumed. HiGHS is
a proposal, followed by rational vertex reconstruction and primal/dual checks.
An explicit finite vertex-enumeration fallback is implemented; its worst-case
cost is exponential and is reported rather than called a polynomial solver.
"""
from __future__ import annotations
from fractions import Fraction as F
from bisect import bisect_right
from itertools import combinations
from pathlib import Path
from math import comb
import argparse
import hashlib
import importlib.util
import json
import time
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
BRIDGE=HERE.parent/"bridge"


def fs(x):
    x=F(x)
    return str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"


def bitlen(x):
    x=F(x)
    return abs(x.numerator).bit_length()+x.denominator.bit_length()


def dot(a,b):
    return sum((x*y for x,y in zip(a,b)),F(0))


class Moments:
    def __init__(self,ts,ys):
        assert ts[0]==0 and ys[0]==0
        assert all(t1>t0 for t0,t1 in zip(ts,ts[1:]))
        self.ts,self.ys=ts,ys
        self.slopes=[(b-a)/(v-u) for u,v,a,b in zip(ts,ts[1:],ys,ys[1:])]
        self.intercepts=[ys[i]-self.slopes[i]*ts[i] for i in range(len(self.slopes))]
        self.prefix=[[F(0)]*5]
        for i,(u,v) in enumerate(zip(ts,ts[1:])):
            self.prefix.append([self.prefix[-1][r]+self.integral(i,r,u,v) for r in range(5)])

    def integral(self,i,r,u,v):
        return (self.intercepts[i]*(v**(r+1)-u**(r+1))/(r+1)
                +self.slopes[i]*(v**(r+2)-u**(r+2))/(r+2))

    def at(self,t):
        if t<=0:return [F(0)]*5
        if t>=self.ts[-1]:return list(self.prefix[-1])
        i=bisect_right(self.ts,t)-1
        return [self.prefix[i][r]+self.integral(i,r,self.ts[i],t) for r in range(5)]

    def filtered(self,t,start,h):
        tau=t-start
        if tau<=0:return F(0)
        assert tau<=self.ts[-1]
        hi=self.at(tau);lo=self.at(tau-h)
        moments=[a-b for a,b in zip(hi,lo)]
        ans=F(0)
        for r,coeff in [(2,F(30)/h**3),(3,-F(60)/h**4),(4,F(30)/h**5)]:
            ans+=coeff*sum((F(comb(r,k))*(-1)**k*tau**(r-k)*moments[k]
                            for k in range(r+1)),F(0))
        return ans


def independent_kernel():
    spec=importlib.util.spec_from_file_location("planner_independent_prediction",BRIDGE/"exact_step_prediction.py")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(table,settings,direct=False):
    ts=[F(x) for x in table["times_exact"]]
    ys=[F(x) for x in table["values_exact"]]
    T=F(table["horizon_exact"]);baseline=F(table["deployment_baseline_exact"])
    assert ts[-1]==T and T==1
    starts=[F(x) for x in settings["starts_exact"]]
    h=F(settings["ramp_exact"]);J=len(starts);n=2*J
    assert all(a+h<=b for a,b in zip(starts,starts[1:])) and starts[-1]+h<=T
    Fcap=F(settings["force_cap_exact"]);V=F(settings["variation_cap_exact"])
    Ccap=F(settings["increment_cap_exact"])
    low=F(settings["path_lower_exact"]);high=F(settings["path_upper_exact"])
    P=int(settings["planning_intervals"])
    grid=[T*i/P for i in range(P+1)]
    slopes=[(b-a)/(v-u) for u,v,a,b in zip(ts,ts[1:],ys,ys[1:])]
    L=max(abs(x) for x in slopes)
    physical=(F(table["readiness_error_exact"])+V*F(table["response_error_exact"])
              +F(table.get("delivery_error_exact","0")))
    margin=physical+V*L*T/(2*P)
    if direct:
        f=independent_kernel().filtered_value
        coeffs=[[f(ts,ys,t,s,h) for s in starts] for t in grid]
    else:
        obj=Moments(ts,ys)
        coeffs=[[obj.filtered(t,s,h) for s in starts] for t in grid]
    rows=[];bounds=[];labels=[]
    def add(row,b,name):
        assert len(row)==n
        rows.append([F(x) for x in row]);bounds.append(F(b));labels.append(name)
    lo_rows=[];hi_rows=[];var_lo=[];var_hi=[]
    for i in range(n):
        lo,hi=(-Ccap,Ccap) if i<J else (F(0),V)
        row=[F(0)]*n;row[i]=-1
        lo_rows.append(len(rows));add(row,-lo,f"lower_bound_{i}")
        row=[F(0)]*n;row[i]=1
        hi_rows.append(len(rows));add(row,hi,f"upper_bound_{i}")
        var_lo.append(lo);var_hi.append(hi)
    for j in range(J):
        row=[F(0)]*n;row[j]=1;row[J+j]=-1;add(row,0,f"abs_plus_{j}")
        row=[F(0)]*n;row[j]=-1;row[J+j]=-1;add(row,0,f"abs_minus_{j}")
    add([F(0)]*J+[F(1)]*J,V,"total_variation")
    for j in range(J):
        row=[F(1) if i<=j else F(0) for i in range(J)]+[F(0)]*J
        add(row,Fcap,f"prefix_upper_{j}")
        add([-x for x in row],Fcap,f"prefix_lower_{j}")
    for l,c in enumerate(coeffs):
        row=c+[F(0)]*J
        add(row,high-margin-baseline,f"trajectory_upper_{l}")
        add([-x for x in row],baseline-low-margin,f"trajectory_lower_{l}")
    objective=[-x for x in coeffs[-1]]+[F(0)]*J
    return {"A":rows,"b":bounds,"labels":labels,"d":objective,
            "lower_rows":lo_rows,"upper_rows":hi_rows,"lower":var_lo,"upper":var_hi,
            "coefficients":coeffs,"grid":grid,"L":L,"physical":physical,
            "margin":margin,"baseline":baseline,"J":J,"n":n,"P":P,
            "starts":starts,"h":h,"V":V,"Ccap":Ccap,"Fcap":Fcap}


def solve_equalities(A,b):
    n=len(b);q=[[F(x) for x in row]+[F(rhs)] for row,rhs in zip(A,b)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if q[i][j]),None)
        if pivot is None:return None
        q[j],q[pivot]=q[pivot],q[j]
        v=q[j][j];q[j]=[x/v for x in q[j]]
        for i in range(n):
            if i!=j and q[i][j]:
                v=q[i][j];q[i]=[a-v*c for a,c in zip(q[i],q[j])]
    return [row[-1] for row in q]


def feasible(lp,x):
    return all(dot(row,x)<=rhs for row,rhs in zip(lp["A"],lp["b"]))


def greedy_basis(A,indices,n):
    echelon=[];chosen=[]
    for i in indices:
        v=[F(x) for x in A[i]]
        for pivot,row in echelon:
            if v[pivot]:
                k=v[pivot];v=[a-k*b for a,b in zip(v,row)]
        p=next((j for j,x in enumerate(v) if x),None)
        if p is not None:
            z=v[p];v=[x/z for x in v]
            echelon.append((p,v));chosen.append(i)
            if len(chosen)==n:return chosen
    return None


def exact_vertex(lp,proposal):
    A,b,n=lp["A"],lp["b"],lp["n"]
    slacks=np.array([float(rhs)-sum(float(a)*float(z) for a,z in zip(row,proposal))
                     for row,rhs in zip(A,b)])
    order=sorted(range(len(A)),key=lambda i:abs(slacks[i]))
    active=[i for i in order if abs(slacks[i])<=1e-7*(1+abs(float(b[i])))]
    chosen=greedy_basis(A,active,n)
    tried=0
    if chosen is not None:
        tried+=1;x=solve_equalities([A[i] for i in chosen],[b[i] for i in chosen])
        if x is not None and feasible(lp,x):return x,chosen,tried,"active-basis reconstruction"
    # Guaranteed finite fallback. No arbitrary early cutoff is hidden here.
    best=None;best_basis=None
    for subset in combinations(range(len(A)),n):
        tried+=1;x=solve_equalities([A[i] for i in subset],[b[i] for i in subset])
        if x is not None and feasible(lp,x):
            if best is None or dot(lp["d"],x)<dot(lp["d"],best):
                best,best_basis=x,list(subset)
    if best is None:raise RuntimeError("Complete rational vertex enumeration found no feasible plan in this bounded polytope")
    return best,best_basis,tried,"complete finite vertex enumeration"


def repaired_dual(lp,marginals,p=52):
    den=1<<p
    lam=[F(max(0,round(-float(x)*den)),den) for x in marginals]
    for i in range(lp["n"]):
        residual=lp["d"][i]+sum((row[i]*v for row,v in zip(lp["A"],lam)),F(0))
        if residual>0:lam[lp["lower_rows"][i]]+=residual
        elif residual<0:lam[lp["upper_rows"][i]]-=residual
    return lam


def verify(lp,x,lam):
    assert len(x)==lp["n"] and len(lam)==len(lp["A"])
    assert feasible(lp,x)
    assert all(v>=0 for v in lam)
    assert all(lp["d"][i]+sum((r[i]*v for r,v in zip(lp["A"],lam)),F(0))==0
               for i in range(lp["n"]))
    primal=dot(lp["d"],x);dual=-dot(lp["b"],lam)
    gap=primal-dual
    assert gap>=0
    return primal,dual,gap


def baseline_region(lp,basis,lam):
    """An exact parametric LP region; online evaluation needs no new solve."""
    slope=[F(-1) if name.startswith("trajectory_upper_") else
           F(1) if name.startswith("trajectory_lower_") else F(0)
           for name in lp["labels"]]
    intercept=[b-s*lp["baseline"] for b,s in zip(lp["b"],slope)]
    B=[lp["A"][i] for i in basis]
    x0=solve_equalities(B,[intercept[i] for i in basis])
    x1=solve_equalities(B,[slope[i] for i in basis])
    lower=upper=None
    for row,b,s in zip(lp["A"],intercept,slope):
        rhs=b-dot(row,x0);coef=dot(row,x1)-s
        if coef>0:
            v=rhs/coef;upper=v if upper is None else min(upper,v)
        elif coef<0:
            v=rhs/coef;lower=v if lower is None else max(lower,v)
        else:assert rhs>=0
    assert lower is not None and upper is not None and lower<=lp["baseline"]<=upper
    gap0=dot(lp["d"],x0)+dot(intercept,lam)
    gap1=dot(lp["d"],x1)+dot(slope,lam)
    return {"baseline_interval_exact":[fs(lower),fs(upper)],
            "primal_affine_intercept_exact":[fs(v) for v in x0],
            "primal_affine_slope_exact":[fs(v) for v in x1],
            "duality_gap_affine_intercept_exact":fs(gap0),
            "duality_gap_affine_slope_exact":fs(gap1),
            "online_rational_multiplications":lp["n"],"online_rational_additions":lp["n"],
            "online_interval_comparisons":2,
            "scope":"Precompute before a fresh readiness draw. For a measured baseline inside this interval the same dual and affine primal give a certified plan, with the stated objective gap. Outside it this one-region plan abstains; it does not assert physical infeasibility. No conditional-on-acceptance confidence amplification is asserted."}


def run(table_path,settings,compile_all=False):
    begin=time.perf_counter();raw=table_path.read_bytes();table=json.loads(raw)
    lp=build(table,settings)
    coefficient_time=time.perf_counter()-begin
    Aa=np.array([[float(x) for x in r] for r in lp["A"]])
    bb=np.array([float(x) for x in lp["b"]]);dd=np.array([float(x) for x in lp["d"]])
    began_lp=time.perf_counter()
    res=linprog(dd,A_ub=Aa,b_ub=bb,bounds=[(None,None)]*lp["n"],method="highs")
    if not res.success:raise RuntimeError("No floating proposal; no certificate of global physical infeasibility is asserted: "+res.message)
    proposal_time=time.perf_counter()-began_lp
    x,basis,tried,route=exact_vertex(lp,res.x)
    lam=repaired_dual(lp,res.ineqlin.marginals)
    primal,dual,gap=verify(lp,x,lam)
    region=baseline_region(lp,basis,lam)
    J=lp["J"];c=x[:J];variation=sum(abs(v) for v in c)
    program=[{"start_exact":fs(start),"ramp_exact":fs(lp["h"]),"increment_exact":fs(inc)}
             for start,inc in zip(lp["starts"],c) if inc]
    predicted=[lp["baseline"]+dot(r,c) for r in lp["coefficients"]]
    maxinc=max(abs(v) for v in c);k=F(table["stiffness_exact"])
    terminal_force=sum(c,F(0))
    return_count=0 if terminal_force==0 else (abs(terminal_force)/lp["Ccap"]).__ceil__()
    return_program=[{"start_exact":fs(F(table["horizon_exact"])+i*lp["h"]),
                     "ramp_exact":fs(lp["h"]),"increment_exact":fs(-terminal_force/return_count)}
                    for i in range(return_count)]
    cert={"schema":"finite_robust_step_planner_v1","acquired_table_sha256":hashlib.sha256(raw).hexdigest(),
          "settings":settings,"primal_exact":[fs(v) for v in x],"dual_exact":[fs(v) for v in lam],
          "precomputed_baseline_region":region,
          "active_basis":basis,"force_program":program,"post_horizon_return_program":return_program,
          "objective":"maximize endpoint coordinate in the declared robust finite basis",
          "primal_minimization_value_exact":fs(primal),"dual_lower_bound_exact":fs(dual),
          "optimization_gap_exact":fs(gap),"optimization_gap":float(gap),
          "predicted_endpoint_exact":fs(predicted[-1]),"predicted_endpoint":float(predicted[-1]),
          "endpoint_physical_interval_exact":[fs(predicted[-1]-lp["physical"]),fs(predicted[-1]+lp["physical"])],
          "uniform_physical_radius_for_all_candidates_exact":fs(lp["physical"]),
          "intergrid_radius_exact":fs(lp["V"]*lp["L"]/(2*lp["P"])),
          "complete_grid_tightening_exact":fs(lp["margin"]),
          "acquired_table_lipschitz_exact":fs(lp["L"]),"actual_variation_exact":fs(variation),
          "predicted_grid_range_exact":[fs(min(predicted)),fs(max(predicted))],
          "certified_whole_path_band_exact":[settings["path_lower_exact"],settings["path_upper_exact"]],
          "hardware":{"trap_stiffness_exact":fs(k),"center_travel_exact":fs(variation/k),
                      "center_speed_bound_exact":fs(F(15)*maxinc/(8*k*lp["h"])),
                      "center_acceleration_rational_bound_exact":fs(6*maxinc/(k*lp["h"]**2)),
                      "terminal_force_exact":fs(terminal_force),
                      "additional_return_duration_exact":fs(return_count*lp["h"]),
                      "additional_return_center_travel_exact":fs(abs(terminal_force)/k)},
          "execution":{"variables":lp["n"],"inequalities":len(lp["A"]),
                       "table_intervals":len(table["times_exact"])-1,"planning_intervals":lp["P"],
                       "coefficient_build_seconds":coefficient_time,"floating_proposal_seconds":proposal_time,
                       "rational_vertex_route":route,"rational_vertex_systems_tried":tried,
                       "maximum_constraint_coefficient_integer_bits":max(bitlen(a) for row in lp["A"] for a in row),
                       "primal_integer_payload_bits":sum(bitlen(v) for v in x),
                       "dual_integer_payload_bits":sum(bitlen(v) for v in lam),
                       "worst_case_enumeration_systems":str(comb(len(lp["A"]),lp["n"]))},
          "scope":{"plant_access":"Only acquired table and declared budgets; no microscopic source import.",
                   "demonstration":"Counterfactual optimization using a recorded readiness baseline. A new physical deployment requires a fresh readiness draw and compatible planning latency.",
                   "optimization_comparison":"Declared tightened quintic-basis polytope only.",
                   "path_guarantee":"Conditional on the acquired-table physical confidence event and finite command-delivery contract."}}
    cert["execution"]["total_construct_seconds"]=time.perf_counter()-begin
    target=HERE/"robust_planner_certificate.json"
    target.write_text(json.dumps(cert,indent=2)+"\n")
    (HERE/"robust_planner_program.json").write_text(json.dumps(program,indent=2)+"\n")
    if compile_all:
        compiled=independent_kernel().compile_path(table,program)
        compiled["acquired_table_sha256"]=cert["acquired_table_sha256"]
        compiled["planner_certificate_sha256"]=hashlib.sha256(target.read_bytes()).hexdigest()
        (HERE/"robust_planner_prediction_path.json").write_text(json.dumps(compiled,indent=2)+"\n")
    return cert


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--table",type=Path,default=BRIDGE/"acquired_step_response.json")
    parser.add_argument("--grid",type=int,default=64)
    parser.add_argument("--upper",default="3/10")
    parser.add_argument("--lower",default="-3/10")
    parser.add_argument("--compile-path",action="store_true")
    args=parser.parse_args()
    settings={"starts_exact":["0","1/5","2/5","3/5","4/5"],"ramp_exact":"1/20",
              "force_cap_exact":"1","variation_cap_exact":"1","increment_cap_exact":"2/5",
              "path_lower_exact":fs(F(args.lower)),"path_upper_exact":fs(F(args.upper)),
              "planning_intervals":args.grid}
    cert=run(args.table,settings,args.compile_path)
    print(json.dumps({k:cert[k] for k in ["predicted_endpoint","optimization_gap",
                     "uniform_physical_radius_for_all_candidates_exact","actual_variation_exact",
                     "force_program","hardware","execution","scope"]},indent=2))


if __name__=="__main__":main()
