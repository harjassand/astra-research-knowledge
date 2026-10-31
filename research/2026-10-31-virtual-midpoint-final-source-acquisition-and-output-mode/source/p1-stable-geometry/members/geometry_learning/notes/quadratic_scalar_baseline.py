"""Ordinary direct acquisition with a quadratic scalar leakage certificate.

Requires the physical controls to be self-adjoint contractions in the common
Hilbert geometry. Actual landmarks and their Gram floor are acquired. No
global rank, useful basis, or transition matrices are supplied. Source shots,
rejected stages, rational computations and finite caps are explicit.
"""
from __future__ import annotations

from fractions import Fraction as F
import argparse
import itertools
import json
from pathlib import Path
import sys
import time

import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import direct_baseline as direct
from spectral_baseline import (
    rational_matrix,transpose,multiply,subtract,sqrt_upper,
    spectral_norm_upper,certified_contraction,project_contraction,
)
cg=direct.cg


def identity(n):
    return [[F(int(i==j)) for j in range(n)] for i in range(n)]


def inverse_rational(a):
    n=len(a)
    aug=[list(row)+identity(n)[i] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if aug[i][j]),None)
        if pivot is None:
            raise RuntimeError("singular finite rational coordinate proposal")
        aug[j],aug[pivot]=aug[pivot],aug[j]
        d=aug[j][j]
        aug[j]=[v/d for v in aug[j]]
        for i in range(n):
            if i!=j and aug[i][j]:
                c=aug[i][j]
                aug[i]=[u-c*v for u,v in zip(aug[i],aug[j])]
    return [row[n:] for row in aug]


def float_matrix(a):
    return np.array([[float(v) for v in row] for row in a])


def checked_norm(a):
    return spectral_norm_upper(float_matrix(a),exact_matrix=a)


def submatrix(a,rows,columns):
    return [[a[i][j] for j in columns] for i in rows]


def symmetric(a):
    return [[(a[i][j]+a[j][i])/2 for j in range(len(a))] for i in range(len(a))]


def symmetric_contraction_proposal(exact):
    p=float_matrix(exact)
    values,vectors=np.linalg.eigh((p+p.T)/2)
    a=(vectors*np.clip(values,-1,1))@vectors.T
    a=(a+a.T)/2
    safe,cert=certified_contraction(a,1e-7)
    if not np.array_equal(safe,safe.T):
        raise RuntimeError("stored operation lost exact numerical symmetry")
    return safe,cert


def scalar_certificate(gram,landmarks,pool,eta,alphabet,horizon):
    """All physical-error enclosures below are exact rational inequalities."""
    lookup={w:i for i,w in enumerate(pool)}
    wi=[lookup[w] for w in landmarks]
    n=len(wi)
    g=submatrix(gram,wi,wi)
    if not direct.physical_independence_certificate(gram,wi,eta):
        return None,{"reason":"physical landmark independence not resolved"}
    # Dyadic upper Cholesky is a proposal; its inverse is exact rational.
    upper=np.linalg.cholesky(float_matrix(g)).T
    ur=rational_matrix(upper)
    r=inverse_rational(ur)
    rt=transpose(r)
    b0=multiply(multiply(rt,g),r)
    nu=checked_norm(subtract(b0,identity(n)))
    norm_r=checked_norm(r)
    z=F.from_float(float(eta))*norm_r**2
    t=nu+z
    normalization={"nu_upper":float(nu),"nu_upper_exact":str(nu),
                   "r_norm_upper":float(norm_r),"r_norm_upper_exact":str(norm_r),
                   "z_upper":float(z),"z_upper_exact":str(z),
                   "t_upper":float(t),"t_upper_exact":str(t),
                   "coordinate_inverse":"exact rational inverse of dyadic Cholesky proposal",
                   "physical_landmark_independence_certified":True}
    if t>F(1,2):
        return None,{"reason":"relative Gram uncertainty exceeds one half",
                     "normalization":normalization}
    inverse_b0=inverse_rational(b0)
    # R^{-1}e_seed is exactly the first column of the proposed upper factor.
    seed0=[[ur[i][0] for i in range(n)]]
    seed_proposal=project_contraction(float_matrix(seed0))
    safe_seed,seed_norm_certificate=certified_contraction(seed_proposal,1e-7)
    seed_error=checked_norm(subtract(rational_matrix(safe_seed),seed0))
    seed=safe_seed[0]
    matrices=[]
    operations=[]
    largest_e2=F(0)
    largest_operator_error=F(0)
    largest_bit_length=max((max(abs(v.numerator).bit_length(),v.denominator.bit_length())
                           for row in r for v in row),default=0)
    for a in range(alphabet):
        si=[lookup[w+(a,)] for w in landmarks]
        # True K is symmetric under the physical self-adjointness promise.
        khat=symmetric(submatrix(gram,wi,si))
        dhat=submatrix(gram,si,si)
        atilde=multiply(multiply(rt,khat),r)
        dtilde=multiply(multiply(rt,dhat),r)
        c=multiply(inverse_b0,atilde)
        rhat=subtract(dtilde,multiply(atilde,c))
        if rhat!=transpose(rhat):
            raise AssertionError("exact Schur expression must be symmetric")
        # Operator norm upper-bounds the largest eigenvalue; no sign guess.
        schur_upper=checked_norm(rhat)
        c_norm=checked_norm(c)
        e2=(schur_upper+z*(1+c_norm)**2)/(1-t)
        safe,norm_certificate=symmetric_contraction_proposal(atilde)
        d=checked_norm(subtract(rational_matrix(safe),atilde))
        operator_error=3*t+d
        largest_e2=max(largest_e2,e2)
        largest_operator_error=max(largest_operator_error,operator_error)
        largest_bit_length=max(largest_bit_length,
            max((max(abs(v.numerator).bit_length(),v.denominator.bit_length())
                 for matrix in (b0,atilde,dtilde,c,rhat)
                 for row in matrix for v in row),default=0))
        matrices.append(safe)
        operations.append({"operation":a,"squared_leakage_upper":float(e2),
            "squared_leakage_upper_exact":str(e2),
            "schur_matrix_norm_upper":float(schur_upper),
            "coefficient_operator_norm_upper":float(c_norm),
            "stored_to_empirical_operator_error_upper":float(d),
            "true_compressed_operator_error_upper":float(operator_error),
            "true_compressed_operator_error_upper_exact":str(operator_error),
            "contraction_certificate":norm_certificate,
            "stored_matrix_exactly_symmetric":True})
    leakage=F(horizon*(horizon-1),2)*largest_e2
    transition=horizon*largest_operator_error
    initial=2*(t+seed_error)
    numerical=direct.floating_evaluation_bound(n,horizon,F(1))
    bound=leakage+transition+initial+numerical
    cert={"normalization":normalization,"operators":operations,
          "squared_leakage_upper":float(largest_e2),
          "squared_leakage_upper_exact":str(largest_e2),
          "operator_error_upper":float(largest_operator_error),
          "seed_storage_error_upper":float(seed_error),
          "seed_norm_certificate":seed_norm_certificate,
          "error_terms":{"quadratic_leakage":float(leakage),
                         "estimated_operators":float(transition),
                         "initial_and_readout":float(initial),
                         "binary64_evaluation":float(numerical)},
          "complete_scalar_error_bound":float(bound),
          "complete_scalar_error_bound_exact":str(bound),
          "largest_selected_matrix_entry_bit_length":largest_bit_length,
          "final_error_bound_bit_length":max(abs(bound.numerator).bit_length(),bound.denominator.bit_length()),
          "rank_not_assumed":True}
    model={"matrices":matrices,"seed":seed,"certificate":cert,
           "bound":bound,"e2":largest_e2,"operator_error":largest_operator_error,
           "seed_error":t+seed_error,"dimension":n}
    return model,cert


def acquire(source,alphabet,horizon,epsilon,delta=F(1,100),initial_eta=0.01,
            maximum_stages=24,maximum_landmarks=12,
            maximum_preparations=100_000_000_000_000_000,resume=None):
    started=time.perf_counter()
    eps=epsilon if isinstance(epsilon,F) else F(str(epsilon))
    dr=delta if isinstance(delta,F) else F(str(delta))
    warm_check=None
    if resume is None:
        landmarks=[()]
        eta=initial_eta
        history=[]
        first_preps=source.ledger()["stationary_preparations"]
        first_stage=1
    else:
        if dr!=resume["delta_budget"] or alphabet!=resume["alphabet"]:
            raise ValueError("warm continuation must keep the same confidence budget and alphabet")
        landmarks=list(resume["landmarks"])
        history=list(resume["history"])
        first_preps=resume["initial_source_preparations"]
        first_stage=len(history)+1
        # Actually reuse the retained exact Gram means before buying precision.
        retained,retained_cert=scalar_certificate(resume["last_gram_exact"],
            landmarks,resume["pool"],resume["eta"],alphabet,horizon)
        warm_check={"retained_data_certificate":retained_cert,
                    "additional_source_calls":0,
                    "accepted_without_new_samples":retained is not None and retained["bound"]<=eps}
        if retained is not None and retained["bound"]<=eps:
            retained|={"status":"success","history":history,"landmarks":landmarks,
                "pool":list(resume["pool"]),"horizon":horizon,"epsilon":eps,
                "eta":resume["eta"],"last_gram_exact":resume["last_gram_exact"],
                "delta_budget":dr,"alphabet":alphabet,
                "initial_source_preparations":first_preps,"warm_retained_check":warm_check,
                "acquisition_cpu_seconds":time.perf_counter()-started}
            return retained
        eta=resume["eta"]/4
    for stage in range(first_stage,maximum_stages+1):
        pool=list(landmarks)
        for w in landmarks:
            for a in range(alphabet):
                if w+(a,) not in pool:
                    pool.append(w+(a,))
        lookup={w:i for i,w in enumerate(pool)}
        before=source.ledger()
        ds=dr/(stage*(stage+1))
        trace={"stage":stage,"landmarks":[list(w) for w in landmarks],
               "pool_words":[list(w) for w in pool],"eta":eta,"delta_exact":str(ds)}
        try:
            shots,_,_=cg.gram_shot_schedule(len(pool),eta,ds)
            planned=shots*len(pool)*(len(pool)+1)//2
            trace["planned_preparations"]=planned
            if before["stationary_preparations"]-first_preps+planned>maximum_preparations:
                raise RuntimeError("declared preparation cap would be exceeded")
            gram,sampling=cg.acquire_geometry(source,pool,eta,ds)
            trace["sampling"]=sampling
            trace["physical_bill"]=cg.subtract_ledger(source.ledger(),before)
            model,certificate=scalar_certificate(gram,landmarks,pool,eta,alphabet,horizon)
            trace["scalar_certificate"]=certificate
            if model is not None and model["bound"]<=eps:
                trace["outcome"]="accepted_quadratic_scalar_certificate"
                history.append(trace)
                model|={"status":"success","history":history,"landmarks":landmarks,
                        "pool":pool,"horizon":horizon,"epsilon":eps,
                        "eta":eta,"last_gram_exact":gram,"delta_budget":dr,
                        "alphabet":alphabet,"initial_source_preparations":first_preps,
                        "warm_retained_check":warm_check,
                        "acquisition_cpu_seconds":time.perf_counter()-started}
                return model
            # Rank and probes are discovered from this same paid pool.
            x,alpha,geometry=direct.factor_pool(gram,eta)
            trace["discovery_geometry"]=geometry
            wi=[lookup[w] for w in landmarks]
            if x.shape[0]>len(landmarks):
                xw=x[:,wi]
                coeff=np.linalg.lstsq(xw,x,rcond=None)[0]
                residuals=np.linalg.norm(x-xw@coeff,axis=0)
                candidates=sorted((j for j,w in enumerate(pool) if w not in landmarks),
                                  key=lambda j:(-float(residuals[j]),j))
                tests=[]
                chosen=None
                for j in candidates:
                    ok=direct.physical_independence_certificate(gram,wi+[j],eta)
                    tests.append({"word":list(pool[j]),"physically_independent_certified":ok})
                    if ok:
                        chosen=pool[j]
                        break
                trace["successor_tests"]=tests
                if chosen is not None:
                    if len(landmarks)>=maximum_landmarks:
                        raise RuntimeError("declared landmark cap exhausted")
                    landmarks.append(chosen)
                    trace["outcome"]="add_certified_independent_actual_successor"
                    trace["added_word"]=list(chosen)
                    history.append(trace)
                    continue
            trace["outcome"]="refine_unattained_scalar_certificate"
            history.append(trace)
            eta/=4
        except (ValueError,RuntimeError,OverflowError,np.linalg.LinAlgError,FloatingPointError) as error:
            trace|={"outcome":"unsuccessful_bounded_attempt","reason":str(error),
                    "physical_bill":cg.subtract_ledger(source.ledger(),before)}
            history.append(trace)
            return {"status":"failure","reason":str(error),"history":history,
                    "landmarks":landmarks,"acquisition_cpu_seconds":time.perf_counter()-started}
    return {"status":"failure","reason":"declared stage cap exhausted", "history":history,
            "landmarks":landmarks,"acquisition_cpu_seconds":time.perf_counter()-started}


def predict(model,word):
    y=model["seed"].copy()
    for a in word:
        y=model["matrices"][a]@y
    return float(model["seed"]@y)


def run_case(horizon,epsilon=F(1,2),seed=20261104):
    source=cg.StationaryEndpointSource(0.4,seed)
    model=acquire(source,3,horizon,epsilon)
    bill=source.ledger()
    report={"case":f"mixed_controls_quadratic_H{horizon}","status":model["status"],
            "task_horizon":horizon,"task_epsilon":float(epsilon),
            "joint_failure_probability_at_most":0.01,"complete_physical_bill":bill,
            "source":"same common-stationary self-adjoint four-state controls",
            "learner_access":"actual-word scalar Gram reports only",
            "supplied_structure":"finite alphabet, norm-bounded seed, self-adjoint contractions in one common geometry",
            "no_supplied_rank_basis_or_gram_floor":True,
            "physically_executed":False,"simulation_method":"root exact-moment aggregate binomial law with coin-bias reserve",
            "resource_caps":{"acquisition_stages":24,"landmarks":12,"preparations":10**17},
            "history":model["history"],"acquisition_cpu_seconds":model["acquisition_cpu_seconds"]}
    if model["status"]!="success":
        report["failure_reason"]=model["reason"]
        return report,{"case":report["case"],"status":"failure","raw_batches":source._raw_batches}
    # Audits are after the entire acquiring routine has stopped.
    largest=0.0
    programs=0
    task_max=0.0
    for word in cg.candidate_words(3,horizon,seed+1):
        truth=source.truth_gram((),word)
        error=abs(predict(model,word)-truth)
        h=len(word)
        bound=F(h*(h-1),2)*model["e2"]+h*model["operator_error"]+2*model["seed_error"]
        bound+=direct.floating_evaluation_bound(model["dimension"],h,F(1))
        if error>float(bound)+1e-12:
            raise AssertionError("post-acquisition audit violated scalar certificate")
        largest=max(largest,error)
        if h<=horizon:
            task_max=max(task_max,error)
        programs+=1
    assert source.ledger()==bill
    report|={"learned_dimension":model["dimension"],"landmarks":[list(w) for w in model["landmarks"]],
             "acquisition_stages":len(model["history"]),"final_pool_size":len(model["pool"]),
             "all_word_error_certificate":float(model["bound"]),"certificate":model["certificate"],
             "heldout_words":programs,"maximum_task_error_audit":task_max,
             "maximum_checked_error_audit":largest,"later_source_calls":0,
             "literal_task_word_count":sum(3**h for h in range(horizon+1))}
    saved={"case":report["case"],"seed":model["seed"].tolist(),
           "matrices":[a.tolist() for a in model["matrices"]],
           "landmarks":[list(w) for w in model["landmarks"]],
           "raw_batches":source._raw_batches}
    return report,saved


def run():
    reports,models=[],[]
    for h in (8,64):
        r,m=run_case(h)
        reports.append(r);models.append(m)
    (HERE/"quadratic_scalar_baseline_results.json").write_text(json.dumps(reports,indent=2)+"\n")
    (HERE/"quadratic_scalar_baseline_models.json").write_text(json.dumps(models,indent=2)+"\n")
    keys=["case","status","learned_dimension","acquisition_stages","all_word_error_certificate",
          "complete_physical_bill","maximum_task_error_audit","literal_task_word_count"]
    print(json.dumps([{key:r[key] for key in keys if key in r} for r in reports],indent=2))


def run_warm():
    """One source, one confidence budget, retained H8 state continued to H64."""
    wall_started=time.perf_counter()
    source=cg.StationaryEndpointSource(0.4,20261104)
    first=acquire(source,3,8,F(1,2))
    if first["status"]!="success":
        raise RuntimeError("initial H8 acquisition failed")
    bill_first=source.ledger()
    first_batches=[dict(row) for row in source._raw_batches]
    first_stage_count=len(first["history"])
    final=acquire(source,3,64,F(1,2),resume=first)
    if final["status"]!="success":
        raise RuntimeError("warm H64 acquisition failed")
    bill_final=source.ledger()
    new_batches=source._raw_batches[len(first_batches):]
    old_words={tuple(w) for row in first_batches for w in (row["u"],row["v"])}
    new_words={tuple(w) for row in new_batches for w in (row["u"],row["v"])}
    old_pairs={(tuple(row["u"]),tuple(row["v"])) for row in first_batches}
    new_pairs={(tuple(row["u"]),tuple(row["v"])) for row in new_batches}
    old_unordered={tuple(sorted(pair)) for pair in old_pairs}
    new_unordered={tuple(sorted(pair)) for pair in new_pairs}
    independent_models=json.loads((HERE/"quadratic_scalar_baseline_models.json").read_text())
    independent_reports=json.loads((HERE/"quadratic_scalar_baseline_results.json").read_text())
    same_first=first_batches==independent_models[0]["raw_batches"]
    same_final=source._raw_batches==independent_models[1]["raw_batches"]
    same_model=(final["seed"].tolist()==independent_models[1]["seed"] and
                [a.tolist() for a in final["matrices"]]==independent_models[1]["matrices"])
    if not (same_first and same_final and same_model):
        raise AssertionError("warm execution did not reproduce the retained-prefix experiment")
    report={
        "status":"success","operation":"continue retained H8 knowledge to H64 on the same source",
        "initial_horizon":8,"later_horizon":64,"epsilon":0.5,
        "shared_joint_soundness_failure_budget":0.01,
        "confidence_statement":"probability any returned certificate is false is at most delta; no conditional-on-acceptance claim",
        "initial_error_certificate":float(first["bound"]),
        "retained_H8_certificate_evaluated_at_H64":final["warm_retained_check"],
        "final_error_certificate":float(final["bound"]),
        "initial_physical_bill":bill_first,"marginal_physical_bill":cg.subtract_ledger(bill_final,bill_first),
        "total_physical_bill":bill_final,
        "initial_acquisition_cpu_seconds":first["acquisition_cpu_seconds"],
        "marginal_acquisition_cpu_seconds":final["acquisition_cpu_seconds"],
        "initial_stage_indices":[s["stage"] for s in first["history"]],
        "new_stage_indices":[s["stage"] for s in final["history"][first_stage_count:]],
        "new_stage_delta_exact":[s["delta_exact"] for s in final["history"][first_stage_count:]],
        "initial_gram_tolerance":first["eta"],"final_gram_tolerance":final["eta"],
        "initial_selected_matrix_entry_max_bits":first["certificate"]["largest_selected_matrix_entry_bit_length"],
        "final_selected_matrix_entry_max_bits":final["certificate"]["largest_selected_matrix_entry_bit_length"],
        "initial_exact_mean_max_denominator_bits":max(v.denominator.bit_length() for row in first["last_gram_exact"] for v in row),
        "final_exact_mean_max_denominator_bits":max(v.denominator.bit_length() for row in final["last_gram_exact"] for v in row),
        "stored_operator_rounding_budget":1e-7,
        "old_word_types":len(old_words),"new_word_types":len(new_words-old_words),
        "old_ordered_return_pair_types":len(old_pairs),
        "new_ordered_return_pair_types":len(new_pairs-old_pairs),
        "old_unordered_gram_pair_types":len(old_unordered),
        "new_unordered_gram_pair_types":len(new_unordered-old_unordered),
        "return_depth_before":bill_first["maximum_return_depth"],
        "return_depth_after":bill_final["maximum_return_depth"],
        "same_retained_raw_prefix_as_independent_H8":same_first,
        "same_final_raw_batches_as_independent_H64":same_final,
        "same_final_stored_model_as_independent_H64":same_model,
        "total_bill_matches_independent_H64":bill_final==independent_reports[1]["complete_physical_bill"],
        "retention_policy":"raw means, all old stages, landmarks, geometry and model retained; existing exact Gram is recertified first; finer stages use fresh fully charged cohorts",
        "generic_precision_scope":"fixed binary64 proposals and 1e-7 stored rounding suffice here; smaller tasks require refined arithmetic or yield explicit failure",
    }
    report["end_to_end_cpu_seconds_before_serialization"]=time.perf_counter()-wall_started
    saved={"landmarks":[list(w) for w in final["landmarks"]],
        "initial_seed":first["seed"].tolist(),"initial_matrices":[a.tolist() for a in first["matrices"]],
        "final_seed":final["seed"].tolist(),"final_matrices":[a.tolist() for a in final["matrices"]],
        "initial_exact_gram":[[str(v) for v in row] for row in first["last_gram_exact"]],
        "final_exact_gram":[[str(v) for v in row] for row in final["last_gram_exact"]],
        "raw_batches":source._raw_batches,"full_stage_history":final["history"]}
    (HERE/"quadratic_scalar_warm_results.json").write_text(json.dumps(report,indent=2)+"\n")
    (HERE/"quadratic_scalar_warm_model.json").write_text(json.dumps(saved,indent=2)+"\n")
    keys=["status","initial_error_certificate","final_error_certificate","marginal_physical_bill",
          "total_physical_bill","marginal_acquisition_cpu_seconds","new_stage_indices",
          "initial_gram_tolerance","final_gram_tolerance","new_word_types","new_ordered_return_pair_types",
          "new_unordered_gram_pair_types",
          "return_depth_before","return_depth_after","same_final_stored_model_as_independent_H64"]
    print(json.dumps({key:report[key] for key in keys},indent=2))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--warm",action="store_true")
    if parser.parse_args().warm:
        run_warm()
    else:
        run()
