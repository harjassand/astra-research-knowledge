"""Direct ordinary successor-pool learner on the root's physical source.

The learner receives only a finite alphabet, a seed word, scalar Gram reports,
and the task horizon/accuracy. It discovers raw landmarks, a Euclidean factor,
and contraction matrices. Every fresh or unsuccessful stage is charged.
Finite caps produce an explicit failure, not a silently assumed oracle.

Run: python geometry_learning/notes/direct_baseline.py
"""
from __future__ import annotations

from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import compact_geometry as cg
from spectral_baseline import (
    certified_contraction, project_contraction, rational_matrix,
    sqrt_upper, spectral_norm_upper, transpose, multiply, subtract,
)


def positive_definite(a):
    """Exact rational unpivoted LDL' positivity test."""
    a = [list(row) for row in a]
    for j in range(len(a)):
        pivot = a[j][j]
        if pivot <= 0:
            return False
        for i in range(j+1, len(a)):
            for l in range(i, len(a)):
                value = a[l][i]-a[l][j]*a[i][j]/pivot
                a[l][i] = a[i][l] = value
    return True


def shifted(a, amount):
    b = [list(row) for row in a]
    for i in range(len(b)):
        b[i][i] -= amount
    return b


def physical_independence_certificate(gram, indices, eta):
    principal = [[gram[i][j] for j in indices] for i in indices]
    return positive_definite(shifted(principal, F.from_float(float(eta))))


def sqrt_lower(q, bits=80):
    result = sqrt_upper(q, bits)-F(1, 1 << bits)
    return max(F(0), result)


def certify_frame_floor(xw):
    """A measured floor for this computed frame, not a supplied condition."""
    xr = rational_matrix(xw)
    exact = multiply(xr, transpose(xr))
    proposal = float(np.linalg.eigvalsh(xw@xw.T)[0])
    if proposal <= 0:
        return None
    floor = F.from_float(proposal)*F(99,100)
    checks = 0
    while checks < 80:
        checks += 1
        if floor > 0 and positive_definite(shifted(exact, floor)):
            sigma = sqrt_lower(floor)
            if sigma <= 0:
                return None
            return sigma, {"squared_floor_exact": str(floor),
                           "squared_floor": float(floor),
                           "exact_ldl_attempts": checks}
        floor /= 2
    return None


def factor_pool(gram_exact, eta):
    proposal = np.array([[float(t) for t in row] for row in gram_exact])
    values, vectors = np.linalg.eigh(proposal)
    kept = values > 2*eta
    x = np.sqrt(values[kept])[:,None]*vectors[:,kept].T
    xr = rational_matrix(x)
    gram_factor = (multiply(transpose(xr),xr) if len(xr) else
                   [[F(0) for _ in gram_exact] for _ in gram_exact])
    residual_exact = subtract(gram_exact,gram_factor)
    residual_upper = spectral_norm_upper(proposal-x.T@x,
                                        exact_matrix=residual_exact)
    total = F.from_float(float(eta))+residual_upper
    alpha = sqrt_upper(total)
    # Prove that the numerical retained dimension is no larger than true rank.
    wr = rational_matrix(vectors[:,kept])
    congruence = multiply(multiply(transpose(wr),
                         shifted(gram_exact,F.from_float(float(eta)))),wr)
    rank_ok = positive_definite(congruence)
    return x, alpha, {
        "gram_factor_error_upper": float(residual_upper),
        "gram_factor_error_upper_exact": str(residual_upper),
        "true_gram_error_upper": float(total),
        "true_gram_error_upper_exact": str(total),
        "global_physical_factor_error_alpha": float(alpha),
        "alpha_exact_upper": str(alpha),
        "retained_rank_certified_no_larger_than_true_pool_rank": rank_ok,
        "factor_certificate": "exact-rational residual and checked SVD proposal",
    }


def certified_operator_residual(a,xw,target):
    exact = subtract(multiply(rational_matrix(a),rational_matrix(xw)),
                     rational_matrix(target))
    return spectral_norm_upper(a@xw-target, exact_matrix=exact)


def fit_operator_norm_contraction(xw,target,excess,max_steps,stop_at):
    """Direct subgradient method for ||A X_W-Y||op on ||A||op<=1."""
    k = xw.shape[0]
    lipschitz = float(np.linalg.norm(xw,2))
    prescribed = max(1,math.ceil(k*lipschitz*lipschitz/(excess*excess)))
    steps = min(prescribed,max_steps)
    rate = math.sqrt(k)/(lipschitz*math.sqrt(steps))
    a = np.zeros((k,k))
    best, best_loss = a.copy(), float("inf")
    iterations = 0
    for t in range(steps):
        residual = a@xw-target
        u,s,vt = np.linalg.svd(residual,full_matrices=False)
        loss = float(s[0])
        iterations = t+1
        if loss < best_loss:
            best, best_loss = a.copy(), loss
        if loss <= stop_at:
            break
        gradient = np.outer(u[:,0],xw@vt[0])
        a = project_contraction(a-rate*gradient)
    return best,{"iterations":iterations,"prescribed_iterations":prescribed,
                 "cap":max_steps,"best_float_residual":best_loss}


def fit_operations(x,word_to_index,landmarks,alphabet,alpha,sigma,horizon,epsilon):
    xw = x[:,[word_to_index[w] for w in landmarks]]
    s0 = sqrt_upper(sum((F.from_float(float(v))**2 for v in xw[:,0]),F(0)))
    # A measured tolerance. Its cost is included if the iterative fit is used.
    excess = max(1e-12,float(F.from_float(epsilon)*sigma/(16*horizon*(1+s0))))
    matrices,certificates = [],[]
    largest_r = F(0)
    for a in range(alphabet):
        target = x[:,[word_to_index[w+(a,)] for w in landmarks]]
        proposal = project_contraction(np.linalg.lstsq(xw.T,target.T,rcond=None)[0].T)
        safe,norm_certificate = certified_contraction(proposal,1e-7)
        residual = certified_operator_residual(safe,xw,target)
        fit_trace = {"least_squares_proposals":1,"projected_subgradient_iterations":0}
        target_residual = 2*alpha+F.from_float(excess)
        if residual > target_residual:
            proposal,trace = fit_operator_norm_contraction(
                xw,target,excess/2,200_000,float(target_residual)-excess/4)
            safe,norm_certificate = certified_contraction(proposal,1e-7)
            residual = certified_operator_residual(safe,xw,target)
            fit_trace["projected_subgradient_iterations"] = trace["iterations"]
            fit_trace["iterative_fit_trace"] = trace
        if residual > target_residual:
            raise RuntimeError("bounded contraction optimizer did not attain its certificate")
        matrices.append(safe)
        largest_r = max(largest_r,residual)
        certificates.append({"operation":a,"residual_operator_upper":float(residual),
                             "residual_operator_upper_exact":str(residual),
                             "norm_certificate":norm_certificate,"fit_trace":fit_trace})
    kappa = (2*alpha+largest_r)/sigma
    bound = alpha*(1+s0)+horizon*kappa*s0
    return matrices,certificates,kappa,bound,s0


def floating_evaluation_bound(k,h,s0):
    """Standard binary64 dot-product error allowance, with underflow reserve."""
    unit = F(1,1 << 53)
    gamma = k*unit/(1-k*unit)
    q = gamma*sqrt_upper(F(k))
    # Per-coordinate underflow allowance is conservatively k*2^-1074.
    underflow = sqrt_upper(F(k))*k*F(1,1 << 1074)
    growth = (1+q)**h
    state_error = s0*(growth-1)+h*underflow*growth
    state_norm = s0*growth+h*underflow*growth
    return s0*state_error+gamma*s0*state_norm+underflow


def acquire_direct(source,alphabet,horizon,epsilon,*,delta=0.01,initial_eta=0.01,
                   maximum_stages=24,maximum_landmarks=12,
                   maximum_preparations=100_000_000_000_000_000):
    """Acquisition uses no truth_gram, latent state, useful basis, or true rank."""
    started = time.perf_counter()
    landmarks = [()]
    eta = initial_eta
    history = []
    initial_preparations = source.ledger()["stationary_preparations"]
    for stage in range(1,maximum_stages+1):
        pool = list(landmarks)
        for w in landmarks:
            for a in range(alphabet):
                candidate = w+(a,)
                if candidate not in pool:
                    pool.append(candidate)
        lookup = {w:i for i,w in enumerate(pool)}
        before = source.ledger()
        d_stage = F(str(delta))/(stage*(stage+1))
        trace = {"stage":stage,"landmarks":[list(w) for w in landmarks],
                 "pool_words":[list(w) for w in pool],"eta":eta,"delta":float(d_stage),
                 "delta_exact":str(d_stage)}
        try:
            planned_per_pair,statistical_eta,_ = cg.gram_shot_schedule(
                len(pool),eta,d_stage)
            planned_preparations = planned_per_pair*len(pool)*(len(pool)+1)//2
            trace["planned_stage_preparations"] = planned_preparations
            used_preparations = before["stationary_preparations"]-initial_preparations
            if used_preparations+planned_preparations > maximum_preparations:
                raise RuntimeError("declared physical preparation budget would be exceeded")
            gram,sampling = cg.acquire_geometry(source,pool,eta,d_stage)
            trace["sampling"] = sampling
            trace["physical_bill"] = cg.subtract_ledger(source.ledger(),before)
            x,alpha,geometry = factor_pool(gram,eta)
            trace["geometry"] = geometry
            k = x.shape[0]
            trace["retained_dimension"] = k
            wi = [lookup[w] for w in landmarks]
            if not physical_independence_certificate(gram,wi,eta):
                trace["outcome"] = "refine_unresolved_existing_landmark_independence"
                history.append(trace)
                eta /= 4
                continue
            if k == 0 or not geometry["retained_rank_certified_no_larger_than_true_pool_rank"]:
                trace["outcome"] = "refine_unresolved_numerical_factor_rank"
                history.append(trace)
                eta /= 4
                continue
            xw = x[:,wi]
            if k > len(landmarks):
                coordinates = np.linalg.lstsq(xw,x,rcond=None)[0]
                residuals = np.linalg.norm(x-xw@coordinates,axis=0)
                candidates = sorted((j for j,w in enumerate(pool) if w not in landmarks),
                                    key=lambda j:(-float(residuals[j]),j))
                accepted = None
                tested = []
                for j in candidates:
                    independent = physical_independence_certificate(gram,wi+[j],eta)
                    tested.append({"word":list(pool[j]),"coordinate_residual_proposal":float(residuals[j]),
                                   "physical_independence_certified":independent})
                    if independent:
                        accepted = pool[j]
                        break
                trace["successor_tests"] = tested
                if accepted is not None:
                    if len(landmarks) >= maximum_landmarks:
                        raise RuntimeError("declared landmark cap exhausted")
                    trace["outcome"] = "add_certified_independent_actual_successor"
                    trace["added_word"] = list(accepted)
                    landmarks.append(accepted)
                    history.append(trace)
                    continue
                trace["outcome"] = "refine_unconfirmed_successor"
                history.append(trace)
                eta /= 4
                continue
            frame = certify_frame_floor(xw)
            if frame is None:
                trace["outcome"] = "refine_unresolved_frame_floor"
                history.append(trace)
                eta /= 4
                continue
            sigma,frame_certificate = frame
            trace["frame_certificate"] = frame_certificate | {"sigma_lower":float(sigma)}
            matrices,fits,kappa,bound,s0 = fit_operations(
                x,lookup,landmarks,alphabet,alpha,sigma,horizon,epsilon)
            roundoff = floating_evaluation_bound(k,horizon,s0)
            complete_bound = bound+roundoff
            trace |= {"operator_fits":fits,"normalized_operation_error_upper":float(kappa),
                      "normalized_operation_error_upper_exact":str(kappa),
                      "seed_coordinate_norm_upper":float(s0),
                      "exact_stored_model_error_bound":float(bound),
                      "binary64_evaluation_error_bound":float(roundoff),
                      "complete_task_error_bound":float(complete_bound)}
            if complete_bound <= F.from_float(float(epsilon)):
                trace["outcome"] = "accepted"
                history.append(trace)
                model = {"x":x,"matrices":matrices,"pool":pool,"landmarks":landmarks,
                         "alpha":alpha,"kappa":kappa,"s0":s0,
                         "task_error_bound":complete_bound,"horizon":horizon,
                         "epsilon":epsilon,"history":history,"status":"success"}
                model["acquisition_cpu_seconds"] = time.perf_counter()-started
                return model
            trace["outcome"] = "refine_task_error_certificate"
            history.append(trace)
            eta /= 4
        except (ValueError,RuntimeError,OverflowError,np.linalg.LinAlgError,FloatingPointError) as error:
            trace["outcome"] = "unsuccessful_bounded_attempt"
            trace["failure_reason"] = str(error)
            trace["physical_bill"] = cg.subtract_ledger(source.ledger(),before)
            history.append(trace)
            return {"status":"failure","reason":str(error),"history":history,
                    "landmarks":landmarks,"acquisition_cpu_seconds":time.perf_counter()-started}
    return {"status":"failure","reason":"declared acquisition-stage cap exhausted",
            "history":history,"landmarks":landmarks,
            "acquisition_cpu_seconds":time.perf_counter()-started}


def predict(model,word):
    y = model["x"][:,0].copy()
    for a in word:
        y = model["matrices"][a]@y
    return float(model["x"][:,0]@y)


def acquire_exhaustive_table(source,alphabet,horizon,epsilon,delta=0.01,
                             maximum_words=20_000):
    """Ordinary finite-horizon competitor; not executed in the saved runs.

    This stores exact rational empirical means for every declared word. It
    often dominates acquisition cost at small horizons, at the price of
    exponentially many stored predictions. All reports use the same source.
    """
    jobs = sum(alphabet**h for h in range(horizon+1))
    if jobs > maximum_words:
        raise ValueError("declared exhaustive-table word cap would be exceeded")
    eps = epsilon if isinstance(epsilon,F) else F(str(epsilon))
    dr = delta if isinstance(delta,F) else F(str(delta))
    statistical_eps = eps-F(1,1 << 52)
    if statistical_eps <= 0:
        raise ValueError("source coin precision cannot meet table accuracy")
    n = cg.ceil_fraction(2*cg.log_upper_integer(2*jobs/dr)/(statistical_eps**2))
    table = {}
    for length in range(horizon+1):
        for word in itertools.product(range(alphabet),repeat=length):
            source.sample_mean((),word,n)
            table[word] = source._last_exact_mean
    return {"predictions_exact":table,"reports_per_word":n,
            "horizon":horizon,"epsilon":eps,"delta":dr,
            "physical_bill":source.ledger()}


def run_case(name,mixing,horizon=8,epsilon=0.5,seed=20261102):
    source = cg.StationaryEndpointSource(mixing,seed)
    model = acquire_direct(source,3,horizon,epsilon)
    acquired = source.ledger()
    report = {"case":name,"status":model["status"],
              "source":"same common-stationary four-state endpoint-product source as root",
              "source_control_mixing_for_audit_only":mixing,
              "learner_access":"actual words and scalar Gram reports only",
              "task_horizon":horizon,"task_epsilon":epsilon,
              "joint_failure_probability_at_most":0.01,
              "complete_physical_bill":acquired,
              "acquisition_stage_cap":24,"landmark_cap":12,
              "physical_preparation_cap":100_000_000_000_000_000,
              "history":model["history"],
              "acquisition_cpu_seconds":model["acquisition_cpu_seconds"],
              "physically_executed":False,
              "simulation_method":"same exact physical moments and aggregate binomial law; coin-rounding bias reserved",
              "comparison_scope":"direct ordinary retained spectral/contraction learner; no teacher model supplied"}
    if model["status"] != "success":
        report["failure_reason"] = model["reason"]
        return report,{"case":name,"status":"failure","scalar_batch_ledger":source._raw_batches}
    # Truth is accessed only after acquisition ends, for explicitly marked audit.
    programs=0
    max_task=max_all=0.0
    for word in cg.candidate_words(3,horizon,seed+1):
        true = source.truth_gram((),word)
        error = abs(predict(model,word)-true)
        h = len(word)
        bound = model["alpha"]*(1+model["s0"])+h*model["kappa"]*model["s0"]
        bound += floating_evaluation_bound(model["x"].shape[0],h,model["s0"])
        if error > float(bound)+1e-12:
            raise AssertionError("audit violated acquired direct certificate")
        max_all=max(max_all,error)
        if h <= horizon:
            max_task=max(max_task,error)
        programs += 1
    assert source.ledger() == acquired
    last = model["history"][-1]
    vertices = np.column_stack([source._feature(w) for w in model["landmarks"]])
    report |= {"landmark_count":len(model["landmarks"]),
               "landmarks":[list(w) for w in model["landmarks"]],
               "final_pool_count":len(model["pool"]),
               "learned_euclidean_dimension":model["x"].shape[0],
               "true_landmark_rank_audit_only":int(np.linalg.matrix_rank(vertices)),
               "all_word_error_certificate_at_task_horizon":float(model["task_error_bound"]),
               "attained_frame_sigma_lower":last["frame_certificate"]["sigma_lower"],
               "attained_global_coupling_alpha":float(model["alpha"]),
               "attained_normalized_operation_error":float(model["kappa"]),
               "acquisition_stages":len(model["history"]),
               "unsuccessful_task_certificate_stages":sum(t["outcome"]=="refine_task_error_certificate" for t in model["history"]),
               "heldout_words":programs,"later_source_calls":0,
               "maximum_error_over_declared_task_audit":max_task,
               "maximum_error_over_all_checked_lengths_audit":max_all}
    saved = {"case":name,"status":"success","pool":[list(w) for w in model["pool"]],
             "landmarks":[list(w) for w in model["landmarks"]],
             "x":model["x"].tolist(),"matrices":[a.tolist() for a in model["matrices"]],
             "scalar_batch_ledger":source._raw_batches}
    return report,saved


def run():
    reports,models=[],[]
    for name,mixing in [("mixed_controls",0.4),("weak_reachable_directions",1e-8)]:
        report,model=run_case(name,mixing)
        reports.append(report)
        models.append(model)
    # Comparison consumes the teacher report only after direct acquisition.
    teacher_path = HERE.parent/"compact_geometry_results.json"
    if teacher_path.exists():
        teacher={r["case"]:r for r in json.loads(teacher_path.read_text())}
        for r in reports:
            old=teacher.get(r["case"])
            if old and r["status"]=="success":
                r["teacher_route_comparison"]={
                    "teacher_atoms":old["old_atoms"],
                    "teacher_euclidean_dimension":old["learned_euclidean_dimension"],
                    "teacher_task_certificate":old["all_word_error_certificate_at_task_horizon"],
                    "teacher_physical_bill":old["complete_physical_bill"],
                    "preparation_ratio_teacher_over_direct":old["complete_physical_bill"]["stationary_preparations"]/r["complete_physical_bill"]["stationary_preparations"],
                    "control_ratio_teacher_over_direct":old["complete_physical_bill"]["primitive_controls"]/max(1,r["complete_physical_bill"]["primitive_controls"])}
    (HERE/"direct_baseline_results.json").write_text(json.dumps(reports,indent=2)+"\n")
    (HERE/"direct_baseline_models.json").write_text(json.dumps(models,indent=2)+"\n")
    keys=["case","status","landmark_count","learned_euclidean_dimension",
          "all_word_error_certificate_at_task_horizon","complete_physical_bill",
          "acquisition_stages","maximum_error_over_declared_task_audit",
          "teacher_route_comparison"]
    print(json.dumps([{key:r[key] for key in keys if key in r} for r in reports],indent=2))


if __name__=="__main__":
    run()
