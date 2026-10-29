"""New analytic reuse receiver, same accepted certificate and SAME old atoms.

No new source, optimizer, gradient fixture or flow run. Exact 35-coefficient
perturbation budgets for the already reconstructed Stokes/flow proof.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json
import time
import hashlib

HERE = Path(__file__).resolve().parent


def monomial(a,exponent):
    value = Q(1)
    for x,k in zip(a,exponent):
        value *= x**k
    return value


def main():
    start = time.perf_counter()
    consumed = json.loads((HERE/"EXACT_CONSUMER.json").read_text())
    nu = Q(consumed["actual_nu"])
    A = [Q(36),Q(0),Q(0),Q(35)]
    increments = [[Q(-264,28745),Q(-63481,114980),Q(5771,143725),Q(528,28745)],
                  [Q(0),Q(11,20),Q(-1,25),Q(0)],
                  [Q(12,5),Q(0),Q(0),Q(-24,5)]]
    weights = [Q(5749,11542),Q(1,2),Q(11,5771)]
    atoms = [[u+v for u,v in zip(A,x)] for x in increments]
    exponents = [e for e in product(range(5),repeat=4) if sum(e)==4]
    assert len(exponents)==35
    moments = [sum(w*monomial(B,e) for w,B in zip(weights,atoms))-monomial(A,e) for e in exponents]
    l1 = sum(abs(x) for x in moments)
    delta = Q(1,100000000)
    epsilon = 35*delta
    kappa = Q(1,400000)
    dissipation_margin = Q(1,12000)-24*(1+abs(nu))*(epsilon+kappa)
    nonpc_upper = Q(consumed["original_finite_nonpc_defect"])+delta*l1
    roc_half_hessian_margin = Q(7,35200)-6*epsilon
    positivity_margin = Q(1711,2800)-epsilon
    assert min(dissipation_margin,roc_half_hessian_margin,positivity_margin)>0 and nonpc_upper<0
    result = {"status":"PASS new full 35-coefficient analytic reuse receiver",
              "input_certificate_sha256":consumed["certificate_sha256"],
              "delta_each_ordinary_monomial_coefficient":str(delta),"coefficient_count":35,
              "coefficient_l1_budget":str(epsilon),"subtracted_norm_coefficient":str(kappa),
              "strict_compensated_dissipation_margin":str(dissipation_margin),
              "strong_quasiconvexity_constant":"1/1200000",
              "inherited_strict_ROC_half_hessian_margin":str(roc_half_hessian_margin),
              "pointwise_Frobenius_quartic_positivity_margin":str(positivity_margin),
              "same_atoms_monomials":[list(e) for e in exponents],
              "same_atoms_moment_differences":[str(x) for x in moments],
              "same_atoms_moment_l1":str(l1),"worst_perturbed_nonpc_defect_upper":str(nonpc_upper),
              "seconds":time.perf_counter()-start,
              "scope":"homogeneous real quartic coefficients in row-major A; no objectivity/isotropy constraint, new fixture, optimizer or world-priority inference"}
    (HERE/"ROBUSTNESS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ["same_atoms_monomials","same_atoms_moment_differences"]},indent=2))


if __name__ == "__main__":
    main()
