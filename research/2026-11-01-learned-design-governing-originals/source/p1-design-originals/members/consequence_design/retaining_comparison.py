"""Same acquired full energy, ordinary retaining MILP, task-matched accuracy.

The MILP gets all acquired coefficients, not the hidden generating parameters.
Its tolerance is an ABSOLUTE objective gap after reserving the identical source
uncertainty. Exactness is not imposed to manufacture an advantage. These runs
are computational comparisons, not an interval verification of HiGHS bounds.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import argparse
import json
import sys
import time
import warnings

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_array

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/"consequence_mechanism"))
from latent_design import compile_acquired


class RetainingMILP:
    def __init__(self, full):
        self.A = np.asarray(full["A_units"], dtype=float)/full["denominator"]
        self.b = np.asarray(full["b_units"], dtype=float)/full["denominator"]
        self.n = len(self.b)
        self.pairs = [(i,j) for i in range(self.n) for j in range(i+1,self.n)]
        self.dimension = self.n+len(self.pairs)
        rows, cols, values, lower, upper = [], [], [], [], []
        for e,(i,j) in enumerate(self.pairs):
            # z_ij<=y_i; z_ij<=y_j; z_ij>=y_i+y_j-1.
            for coefficients, lo, hi in (
                ({self.n+e:1.,i:-1.}, -np.inf, 0.),
                ({self.n+e:1.,j:-1.}, -np.inf, 0.),
                ({self.n+e:1.,i:-1.,j:-1.}, -1., np.inf)):
                row = len(lower)
                for col, value in coefficients.items():
                    rows.append(row); cols.append(col); values.append(value)
                lower.append(lo); upper.append(hi)
        matrix = coo_array((values,(rows,cols)), shape=(len(lower),self.dimension)).tocsc()
        self.constraints = LinearConstraint(matrix, np.array(lower), np.array(upper))
        self.bounds = Bounds(np.zeros(self.dimension), np.ones(self.dimension))
        self.integrality = np.r_[np.ones(self.n),np.zeros(len(self.pairs))]
        self.base = np.zeros(self.dimension)
        off = self.A.copy()
        np.fill_diagonal(off, 0.)
        self.base[:self.n] = 2*self.b-2*off.sum(axis=1)
        self.base[self.n:] = [4*self.A[i,j] for i,j in self.pairs]

    def solve(self, h, absolute_gap, time_limit=20., relaxation=False):
        c = self.base.copy()
        c[:self.n] += 2*np.asarray(h)
        options = {"presolve":True,"time_limit":time_limit,"mip_rel_gap":0.,
                   "mip_abs_gap":absolute_gap,"threads":1}
        start = time.perf_counter()
        with warnings.catch_warnings(record=True) as issued:
            warnings.simplefilter("always")
            result = milp(c, integrality=np.zeros(self.dimension) if relaxation else self.integrality,
                          bounds=self.bounds,constraints=self.constraints,options=options)
        elapsed = time.perf_counter()-start
        record = {"seconds":elapsed,"solver_status":int(result.status),
                  "message":result.message,"requested_absolute_gap":absolute_gap,
                  "reported_nodes":getattr(result,"mip_node_count",None),
                  "passed_HiGHS_options":[str(w.message) for w in issued],
                  "relaxation_only":relaxation}
        if result.x is None:
            return None, record
        record["relaxed_fractional_physical_variables"] = int(np.sum(
            (result.x[:self.n]>1.e-6)&(result.x[:self.n]<1.-1.e-6)))
        dual = getattr(result,"mip_dual_bound",None)
        if dual is not None:
            gap = max(0.,float(result.fun-dual))
            record.update({"reported_absolute_gap":gap,
                           "within_requested_gap":gap<=absolute_gap+1.e-7})
        constant = .5*np.sum(self.A)+float(-np.sum(self.b+np.asarray(h)))
        record["objective_with_energy_constant"] = float(result.fun+constant)
        x = 2*(result.x[:self.n]>=.5).astype(np.int8)-1
        return x,record

    def objective(self,x,h):
        return float(.5*x@self.A@x+(self.b+np.asarray(h))@x)


def compare(name,full,seed,queries=6):
    source_error = full.get("source_regret_bound")
    if source_error is None:
        source_error = str(2*len(full["b_units"])**2*Fraction(full["coefficient_radius"]))
    service,compiled = compile_acquired(full,source_regret_bound=source_error)
    if service is None:
        return {"fixture":name,"status":"No compiled service for comparison","compilation":compiled}
    start = time.perf_counter()
    retaining = RetainingMILP(full)
    setup_time = time.perf_counter()-start
    target = .02*service.n-float(Fraction(source_error))
    if target<=0:
        raise ValueError("Source uncertainty already consumes task budget")
    rng = np.random.default_rng(seed)
    previous = np.ones(service.n)
    records = []
    for t in range(queries):
        h = .16*rng.uniform(-1,1,service.n)+.03*previous*((-1)**t)
        start = time.perf_counter()
        compact,work = service.solve(h)
        compact_seconds = time.perf_counter()-start
        ordinary,record = retaining.solve(h,target)
        record.update({"query":t,"compact_seconds":compact_seconds,
                       "compact_arithmetic":work,
                       "compact_surrogate_objective":retaining.objective(compact,h)})
        if ordinary is not None:
            record["ordinary_surrogate_objective"] = retaining.objective(ordinary,h)
            record["compact_minus_ordinary_objective"] = (
                record["compact_surrogate_objective"]-record["ordinary_surrogate_objective"])
        if t==0:
            _,record["ordinary_LP_relaxation"] = retaining.solve(h,target,relaxation=True)
        records.append(record)
        previous = compact
    return {"fixture":name,"n":service.n,"learned_logical_variables":service.r,
            "source_information":"identical full acquired quadratic and same source confidence event",
            "source_regret_bound":source_error,"physical_regret_budget":.02*service.n,
            "MILP_extra_source_samples":0,"compact_extra_source_samples":0,
            "MILP_setup_seconds":setup_time,"MILP_binary_variables":service.n,
            "MILP_continuous_product_variables":len(retaining.pairs),
            "MILP_constraints":3*len(retaining.pairs),
            "compact_retained_labels":service.n,
            "compact_retained_scalar_coefficients":service.r+len(service.forest),
            "uniform_compact_certificate":str(service.regret_bound),
            "queries":records,
            "all_MILP_queries_met_requested_gap":all(q.get("within_requested_gap",False) for q in records),
            "MILP_total_query_seconds":sum(q["seconds"] for q in records),
            "compact_total_query_seconds":sum(q["compact_seconds"] for q in records),
            "caveats":["Small synthetic benchmarks, not a scaling or lower-bound result",
                       "MILP reports floating numerical bounds; not an exact rational certificate",
                       "HiGHS preprocessing and cuts enabled; no true partition given to either learner",
                       "Specialized relational/SDP preprocessing could also acquire a reusable contraction",
                       "No superiority claimed over every strong ordinary retaining method"]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--model-files",nargs="*")
    parser.add_argument("--queries",type=int,default=6)
    parser.add_argument("--output",default="retaining_comparison_results.json")
    args=parser.parse_args()
    if args.model_files:
        models={Path(path).stem:json.loads(Path(path).read_text()) for path in args.model_files}
    else:
        path=HERE.parent/"consequence_mechanism/latent_design_acquired_models.json"
        models=json.loads(path.read_text())
    results=[]
    for index,(name,full) in enumerate(models.items()):
        result=compare(name,full,seed=9721+index,queries=args.queries)
        results.append(result)
        print(json.dumps({"fixture":name,"n":result.get("n"),
                          "ordinary_success":result.get("all_MILP_queries_met_requested_gap"),
                          "MILP_seconds":result.get("MILP_total_query_seconds"),
                          "compact_seconds":result.get("compact_total_query_seconds")}),flush=True)
    destination=HERE/args.output
    destination.write_text(json.dumps({"comparisons":results},indent=2)+"\n")


if __name__=="__main__":
    main()
