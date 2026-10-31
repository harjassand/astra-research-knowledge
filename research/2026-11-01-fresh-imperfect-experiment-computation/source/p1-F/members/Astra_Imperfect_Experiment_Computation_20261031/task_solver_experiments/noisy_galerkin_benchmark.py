"""Reproducible noisy Galerkin cache experiment.

Run from this directory or any cwd:
  OPENBLAS_NUM_THREADS=1 python noisy_galerkin_benchmark.py

The solver receives only an action callback, alpha, mu, and requested epsilon.
True matrices are confined to source and verification/workload construction.
Noise is deterministic and correlated: action(v,tol)=Bv+tol Fv, ||F||=1.
The precision proxy sum(tol^-2) is recorded, not interpreted as a physical cost.
"""
from dataclasses import dataclass
from pathlib import Path
import copy
import json
import time
import numpy as np
from scipy.linalg import eigh, solve


EPS = np.finfo(float).eps


def spectral(a):
    return float(np.linalg.norm(a, 2)) if a.size else 0.0


def next_power_two(value):
    return 1 << (int(value) - 1).bit_length()


def project_out(u, vector):
    result = vector.copy()
    if u.shape[1]:
        result -= u @ (u.T @ result)
        result -= u @ (u.T @ result)
    return result


def near_zero_threshold(n, vector_norm):
    # A finite-precision decision only. It is not evidence of exact dependence.
    return 16 * EPS * n * max(vector_norm, np.finfo(float).tiny)


class Source:
    def __init__(self, bmat, noise_matrix):
        self.__bmat = bmat.copy()
        self.__noise = noise_matrix.copy()
        self.n = bmat.shape[0]
        self.calls = 0
        self.precision_cost = 0.0
        self.output_scalars = 0
        self.tolerances = []

    def action(self, vector, tol):
        assert tol > 0
        self.calls += 1
        self.precision_cost += tol ** -2
        self.output_scalars += self.n
        self.tolerances.append(float(tol))
        return self.__bmat @ vector + tol * (self.__noise @ vector)

    def counts(self):
        return self.calls, self.precision_cost, self.output_scalars


class Audit:
    """Checker-only information; no returned value influences the learner."""
    def __init__(self, bmat, alpha):
        self.bmat = bmat
        self.amat = bmat + alpha * np.eye(bmat.shape[0])
        self.max_error_matrix_ratio = 0.0
        self.max_orthogonality_defect = 0.0
        self.min_h_eigenvalue = float("inf")
        self.checked_trials = 0
        self.true_inverse = np.linalg.inv(self.amat)

    def trial(self, v, y, sigma, h):
        ratio = spectral(y - self.bmat @ v) / sigma
        orth = spectral(v.T @ v - np.eye(v.shape[1]))
        minimum = float(eigh(h, eigvals_only=True)[0])
        self.max_error_matrix_ratio = max(self.max_error_matrix_ratio, ratio)
        self.max_orthogonality_defect = max(self.max_orthogonality_defect, orth)
        self.min_h_eigenvalue = min(self.min_h_eigenvalue, minimum)
        self.checked_trials += 1
        assert ratio <= 1 + 2e-8, (ratio, sigma, v.shape)
        assert orth < 1e-10, orth

    def solution(self, rhs, x, epsilon):
        truth = self.true_inverse @ rhs
        relative_error = float(np.linalg.norm(x-truth) / np.linalg.norm(truth))
        true_residual = float(np.linalg.norm(rhs-self.amat @ x))
        assert relative_error <= epsilon + 2e-9, (relative_error, epsilon)
        return relative_error, true_residual


class Cache:
    def __init__(self, action, n, alpha, mu, epsilon, audit=None):
        self.action = action
        self.n, self.alpha, self.mu = n, alpha, mu
        self.u = np.empty((n, 0))
        self.yu = np.empty((n, 0))
        self.cap = 1
        self.audit = audit
        self.append_diagonals = []
        self.refresh_events = []
        self.omitted_transient_norms = []
        self.set_accuracy(epsilon, refresh=False)

    @property
    def rank(self):
        return self.u.shape[1]

    def set_accuracy(self, epsilon, refresh=True):
        self.epsilon = epsilon
        self.tau = self.mu * epsilon / (1 + epsilon)
        self.sigma = self.tau / 16
        if refresh and self.rank:
            self.refresh("accuracy_change")

    def refresh(self, reason):
        tol = self.sigma / np.sqrt(self.cap)
        self.yu = np.column_stack([self.action(self.u[:, j], tol)
                                   for j in range(self.rank)]) if self.rank else np.empty((self.n,0))
        self.refresh_events.append({"rank": self.rank, "cap": self.cap,
                                    "reason": reason, "tol": float(tol)})

    def append(self, direction, proof_diagonal=None):
        q = project_out(self.u, direction)
        size = np.linalg.norm(q)
        if size <= near_zero_threshold(self.n, np.linalg.norm(direction)):
            return False
        q /= size
        self.u = np.column_stack([self.u, q])
        newcap = next_power_two(self.rank + 1)
        if newcap != self.cap:
            self.cap = newcap
            self.refresh("capacity_increase")
        else:
            y = self.action(q, self.sigma / np.sqrt(self.cap))
            self.yu = np.column_stack([self.yu, y])
        if proof_diagonal is not None:
            self.append_diagonals.append(float(proof_diagonal))
        return True

    def initialize_range(self, q):
        self.u = q.copy()
        self.cap = next_power_two(self.rank + 1)
        self.refresh("randomized_range_initialization")

    def clone(self):
        c = Cache(self.action, self.n, self.alpha, self.mu, self.epsilon, self.audit)
        c.u, c.yu, c.cap = self.u.copy(), self.yu.copy(), self.cap
        return c

    def solve(self, rhs, max_steps=None):
        if max_steps is None:
            max_steps = self.n + 2
        rank_before = self.rank
        max_residual_ratio = 0.0
        for iteration in range(max_steps):
            q = project_out(self.u, rhs)
            qnorm = np.linalg.norm(q)
            if qnorm > near_zero_threshold(self.n, np.linalg.norm(rhs)):
                q /= qnorm
                v = np.column_stack([self.u, q])
                yq = self.action(q, self.sigma / np.sqrt(self.cap))
                y = np.column_stack([self.yu, yq])
            else:
                self.omitted_transient_norms.append(float(qnorm))
                v, y = self.u, self.yu
            if not v.shape[1]:
                raise RuntimeError("Nonzero task lost all vectors through floating-point cutoff")
            g = v.T @ y
            h = self.alpha*np.eye(v.shape[1]) + (g+g.T)/2
            if self.audit is not None:
                self.audit.trial(v, y, self.sigma, h)
            z = solve(h, v.T @ rhs, assume_a="sym")
            x = v @ z
            xnorm = np.linalg.norm(x)
            residual = np.linalg.norm(rhs - self.alpha*x-y@z)
            certificate = residual+self.sigma*xnorm
            ratio = float(certificate/(self.tau*xnorm))
            max_residual_ratio = max(max_residual_ratio, ratio)
            if certificate <= self.tau*xnorm:
                return x, {"rank_before": rank_before, "rank_after": self.rank,
                           "enrichments": self.rank-rank_before,
                           "trials": iteration+1, "certificate_ratio": ratio,
                           "certificate_absolute": float(certificate),
                           "max_trial_certificate_ratio": max_residual_ratio}
            w = project_out(self.u, y@z)/xnorm
            diag = float(np.linalg.norm(w))
            assert diag + 2e-10 >= self.tau-2*self.sigma, (diag,self.tau,self.sigma)
            if not self.append(w, proof_diagonal=diag):
                raise RuntimeError("Failed certificate with no numerically resolvable enrichment")
        raise RuntimeError("Task did not reach residual certificate")


def make_problem(n=160, tasks=80, seed=6731, epsilon=0.02):
    rng = np.random.default_rng(seed)
    q, _ = np.linalg.qr(rng.normal(size=(n,n)))
    alpha = mu = 0.2
    tau = mu*epsilon/(1+epsilon)
    rank = 4
    tail = tau/8
    eigenvalues = np.r_[4.0, 2.0, 1.0, 0.5,
                       tail * rng.uniform(0.15, 1.0, n-rank)]
    eigenvalues[-1] = tail
    bmat = (q*eigenvalues)@q.T
    noise = rng.normal(size=(n,n))
    noise /= spectral(noise)
    rhses = []
    late_index = 55
    for t in range(tasks):
        coefficients = rng.normal(size=n)
        if t < late_index:
            coefficients[3] = 0.0
        if t == late_index:
            coefficients[:] = 0.0
            coefficients[3] = 1.0
            coefficients[4:] = 0.03*rng.normal(size=n-rank)
        rhs = q@coefficients
        rhs /= np.linalg.norm(rhs)
        rhses.append(rhs)
    return {"bmat":bmat, "q":q, "noise":noise, "rhses":rhses,
            "alpha":alpha,"mu":mu,"epsilon":epsilon,"tau":tau,"tail":tail,
            "rank":rank,"n":n,"late_index":late_index,
            "eigenvalues":eigenvalues,"seed":seed}


def summarize(method, source, cache, rows, audit, elapsed, setup_calls=0):
    return {
        "method":method, "source_calls":source.calls,
        "source_output_scalars":source.output_scalars,
        "sum_inverse_tolerance_squared":source.precision_cost,
        "minimum_action_tolerance":min(source.tolerances) if source.tolerances else None,
        "maximum_action_tolerance":max(source.tolerances) if source.tolerances else None,
        "retained_rank":cache.rank if cache else 0,
        "max_rank_during_tasks":max(row["rank_after"] for row in rows),
        "retained_basis_scalars":2*cache.n*cache.rank if cache else 0,
        "total_task_trials":sum(row["trials"] for row in rows),
        "maximum_true_relative_error":max(row["true_relative_error"] for row in rows),
        "maximum_error_matrix_to_sigma_ratio":audit.max_error_matrix_ratio,
        "maximum_basis_orthogonality_defect":audit.max_orthogonality_defect,
        "minimum_reduced_matrix_eigenvalue":audit.min_h_eigenvalue,
        "minimum_enrichment_diagonal":min(cache.append_diagonals) if cache and cache.append_diagonals else None,
        "required_diagonal_floor":cache.tau-2*cache.sigma if cache else None,
        "randomized_setup_calls":setup_calls,
        "wall_seconds_including_checker":elapsed,
        "task_rows":rows,
        "refresh_events":copy.deepcopy(cache.refresh_events) if cache else [],
        "status":"PASS",
    }


def run_method(problem, method):
    p=problem
    source=Source(p["bmat"],p["noise"])
    audit=Audit(p["bmat"],p["alpha"])
    cache=Cache(source.action,p["n"],p["alpha"],p["mu"],p["epsilon"],audit)
    rows=[]
    start=time.perf_counter()
    setup_calls=0
    if method in ("gaussian_range_8_plus_certified_enrichment",
                  "gaussian_svd_8_plus_certified_enrichment"):
        rng=np.random.default_rng(991)
        omega=rng.normal(size=(p["n"],8))
        omega/=np.linalg.norm(omega,axis=0)
        tol=cache.sigma/np.sqrt(16)
        y=np.column_stack([source.action(omega[:,j],tol) for j in range(8)])
        if method=="gaussian_svd_8_plus_certified_enrichment":
            # This is merely a basis proposal, not a claim that a tiny singular
            # value proves a component absent. Every task still receives the
            # full residual certificate and enriches on failure.
            vectors,singular,_=np.linalg.svd(y,full_matrices=False)
            proposed=vectors[:,singular>cache.tau/4]
            cache.initialize_range(proposed)
        else:
            qr=[]
            for j in range(y.shape[1]):
                basis=np.column_stack(qr) if qr else np.empty((p["n"],0))
                v=project_out(basis,y[:,j])
                if np.linalg.norm(v)>near_zero_threshold(p["n"],np.linalg.norm(y[:,j])):
                    qr.append(v/np.linalg.norm(v))
            cache.initialize_range(np.column_stack(qr))
        setup_calls=source.calls
    for index,rhs in enumerate(p["rhses"]):
        counts_before=source.counts()
        if method == "reset_per_task":
            worker=Cache(source.action,p["n"],p["alpha"],p["mu"],p["epsilon"],audit)
            x,info=worker.solve(rhs)
        elif method in ("retained_solution_snapshots","retained_correction_snapshots"):
            worker=cache.clone()
            x,info=worker.solve(rhs)
            if info["enrichments"]:
                snapshot=x if method=="retained_solution_snapshots" else x-rhs/p["alpha"]
                cache.append(snapshot)
            info["global_retained_rank"]=cache.rank
        else:
            x,info=cache.solve(rhs)
        err,true_residual=audit.solution(rhs,x,p["epsilon"])
        calls,precision,scalars=source.counts()
        info.update({"task_index":index,"source_calls":calls-counts_before[0],
                     "precision_cost":precision-counts_before[1],
                     "true_relative_error":err,"true_residual":true_residual,
                     "source_calls_cumulative":calls,"global_retained_rank":cache.rank})
        rows.append(info)
    elapsed=time.perf_counter()-start
    result=summarize(method,source,cache,rows,audit,elapsed,setup_calls)
    return result,cache,source,audit


def hidden_tail_challenge(problem,cache,source,audit):
    p=problem
    rng=np.random.default_rng(4101)
    old_rank=cache.rank
    old_epsilon=cache.epsilon
    new_epsilon=0.00025
    before=source.counts()
    cache.set_accuracy(new_epsilon,refresh=True)
    rows=[]
    for index in range(12):
        c=np.zeros(p["n"])
        if index==0:
            tail_values=p["eigenvalues"][4:]
            c[4+int(np.argmin(tail_values))]=1/np.sqrt(2)
            c[4+int(np.argmax(tail_values))]=1/np.sqrt(2)
        else:
            c[4:]=rng.normal(size=p["n"]-4)
            c/=np.linalg.norm(c)
        rhs=p["q"]@c
        count0=source.counts()
        x,info=cache.solve(rhs)
        err,residual=audit.solution(rhs,x,new_epsilon)
        info.update({"task_index":index,"true_relative_error":err,"true_residual":residual,
                     "source_calls":source.calls-count0[0],"precision_cost":source.precision_cost-count0[1]})
        rows.append(info)
    return {"old_epsilon":old_epsilon,"new_epsilon":new_epsilon,
            "old_retained_rank":old_rank,"new_retained_rank":cache.rank,
            "new_tau":cache.tau,"source_tail_norm":p["tail"],
            "new_source_calls_including_precision_refresh":source.calls-before[0],
            "new_precision_cost_including_refresh":source.precision_cost-before[1],
            "max_true_relative_error":max(r["true_relative_error"] for r in rows),
            "task_rows":rows,"status":"PASS"}


def main():
    problem=make_problem()
    methods=["adaptive_image_cache","reset_per_task","retained_solution_snapshots",
             "retained_correction_snapshots","gaussian_range_8_plus_certified_enrichment",
             "gaussian_svd_8_plus_certified_enrichment"]
    results=[]
    main_cache=main_source=main_audit=None
    for method in methods:
        result,cache,source,audit=run_method(problem,method)
        results.append(result)
        if method=="adaptive_image_cache":
            main_cache,main_source,main_audit=cache,source,audit
        print(json.dumps({k:v for k,v in result.items() if k not in ("task_rows","refresh_events")}),flush=True)
    challenge=hidden_tail_challenge(problem,main_cache,main_source,main_audit)
    meta={k:problem[k] for k in ("alpha","mu","epsilon","tau","tail","rank","n","late_index","seed")}
    meta.update({"tasks":len(problem["rhses"]),"source_noise":"fixed correlated Fv; ||F||=1; multiplied by requested tolerance",
                 "tail_structure":"generic dense positive full-rank tail on dominant-subspace complement",
                 "comparison_scope":"Synthetic action/precision cost comparison; no wall-time or physical advantage claim",
                 "floating_point_scope":"Proof assumes exact arithmetic; code uses two-pass orthogonalization and explicit machine-scale cutoff",
                 "precision_cost_scope":"sum tol^-2 is an explicit proxy, not an inferred physical law",
                 "global_randomized_scope":"Range-basis baseline with per-task checks; not a globally certified zero-query Nystrom compiler"})
    output={"metadata":meta,"methods":results,"tightened_accuracy_hidden_tail_challenge":challenge,"status":"PASS"}
    path=Path(__file__).with_name("benchmark_results.json")
    path.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({"hidden_tail_challenge":{k:v for k,v in challenge.items() if k!="task_rows"}},indent=2))


if __name__=="__main__":
    main()
