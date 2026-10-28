"""Exact rational consumer for the general force/commit contracts.

Not an apparatus simulation or acquired material qualification. No fitting,
random starts, external solver, force measurements or physical actions.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import hashlib
import json
import time
import sympy as sp

HERE = Path(__file__).resolve().parent


def qr(x):
    x = Q(x)
    return {"exact": f"{x.numerator}/{x.denominator}", "display": float(x)}


def compile_contract(g, b, fmin, fmax, joint):
    assert 0 <= b < g <= fmax and fmin <= 0
    legal = 2*g if joint else g
    illegal = fmax+b if joint else b
    assert legal > illegal
    gap = legal-illegal
    center, scale = (legal+illegal)/2, gap/3
    lo, hi = ((2 if joint else 1)*fmin-center)/scale, ((2 if joint else 1)*fmax-center)/scale
    X = 1
    while X**3-X < max(abs(lo), abs(hi)):
        X += 1
    assert (legal-center)/scale == Q(3, 2)
    assert (illegal-center)/scale == -Q(3, 2)
    assert center/scale >= Q(3, 2)
    assert Q(4, 27) < Q(4, 25)  # critical cubic height <2/5
    checks = []
    if joint:
        for a, btype in product(["G", "B", "absent"], repeat=2):
            if a == btype == "G":
                checks.append({"inputs": [a, btype], "legal_lower": qr(legal), "drive_lower": qr(Q(3, 2))})
            else:
                maxforce = sum({"G": fmax, "B": b, "absent": Q(0)}[v] for v in (a, btype))
                drive = (maxforce-center)/scale
                assert drive <= -Q(3, 2)
                checks.append({"inputs": [a, btype], "illegal_upper": qr(maxforce), "drive_upper_at_commit": qr(drive)})
    return {"kind": "joint_commit" if joint else "independent_recognizer",
            "input": {k: qr(v) for k, v in dict(g=g,b=b,fmin=fmin,fmax=fmax).items()},
            "gap": qr(gap), "center": qr(center), "E_over_F0_ell": qr(scale),
            "spring_beta": qr(center/scale), "drive_range": [qr(lo), qr(hi)],
            "invariant_X": X, "dimensionless_latency_upper": qr(Q(10*(X+1),11)),
            "two_input_cases": checks,
            "status": "CONDITIONAL_FORCE_AND_KINEMATIC_CONTRACT_ONLY"}


def linear_comparator(g,b,fmax):
    L,I=2*g,fmax+b
    G=L-I
    assert G>0
    preload=I+G/3
    kscaled=G/3
    assert L-preload-kscaled == G/3
    assert I-preload == -G/3
    # Both worst-case scalar equilibrium distances give a log(2) passage.
    assert (L-preload)/kscaled==2
    assert (I-preload)/kscaled==-1
    F0,ell=Q(4,25),Q(1,200000)  # illustrative .16N,5um, NOT apparatus spec
    P,k=preload*F0,kscaled*F0/ell
    return {"gap":qr(G),"preload_over_F0":qr(preload),"k_ell_over_F0":qr(kscaled),
      "precompression_over_stroke":qr(preload/kscaled),
      "preloaded_energy_over_F0_ell":qr(preload*preload/(2*kscaled)),
      "stroke_energy_over_F0_ell":qr(I+G/2),
      "worst_write_and_reset_time":"(zeta/k)*log(2)",
      "nominal_dimensional_control_only":{"F0_N":qr(F0),"stroke_m":qr(ell),
        "preload_N":qr(P),"stiffness_N_per_m":qr(k),"precompression_m":qr(P/k),
        "preloaded_J":qr(P*P/(2*k)),"stroke_energy_J":qr((I+G/2)*F0*ell)},
      "status":"ORDINARY_OPERATION_REPRODUCES_GATE_WITH_SIMPLER_SPRING"}


def main():
    start = time.perf_counter()
    # Symbolic Maxwell derivative; attractive normal force is dE/dh.
    r,h,C,m = sp.symbols("r h C m", positive=True)
    energy = C*m*m*(r*r-2*h*h)/(r*r+h*h)**sp.Rational(5,2)
    force = 3*C*m*m*h*(2*h*h-3*r*r)/(r*r+h*h)**sp.Rational(7,2)
    assert sp.simplify(sp.diff(energy,h)-force) == 0
    v=sp.symbols("v", nonnegative=True)
    relative=(1-sp.Rational(3,2)*v)/(1+v)**sp.Rational(7,2)
    assert sp.simplify(sp.diff(relative,v)-(-5+sp.Rational(15,4)*v)/(1+v)**sp.Rational(9,2)) == 0
    assert Q(53,48)<Q(10,9)

    # Illustrative source-surrogate compilation, NOT calibration of these bands.
    rep=Q(9,100)
    offset,slope=(1-rep)/2,(1+rep)/2
    bad_surrogate=offset+slope*Q(9,25)
    assert bad_surrogate == Q(407,625)
    assert 1+3*offset == Q(473,200)>2
    g,b,fmin,fmax=Q(19,20),bad_surrogate+Q(1,20),-Q(7,50),Q(21,20)
    soft=compile_contract(g,b,fmin,fmax,False)
    soft_joint=compile_contract(g,b,fmin,fmax,True)
    linear=linear_comparator(g,b,fmax)

    # Hard-dipole, all-pair, pose and FULL-STROKE force transfer.
    rho,a,eta,s=Q(9,25),Q(1,20),Q(1,10),Q(1,100)
    etamax=(1+s)*eta
    fringe=Q(40,3)*etamax**5/(1-a*etamax)**5
    error=5*a*a+fringe
    gh=(1-error)/(1+s)**4
    bh=(rho+error)/(1-s)**4
    fm=(1+fringe)/(1-s)**4
    hard=compile_contract(gh,bh,-fm,fm,True)
    hard_linear=linear_comparator(gh,bh,fm)

    # Inertial upcrossing despite currently illegal force.
    xl,xu=Q(99,100),Q(101,100)
    acceleration=lambda x:-Q(3,2)+x-x**3
    assert 1-3*xl*xl<0
    assert -2<acceleration(xu)<acceleration(xl)<0
    tm=Q(1,50)
    inertial_lower=xl+tm-tm*tm
    assert inertial_lower>1 and 1-2*tm>0

    # All-rational finite-history counter, no numerical ODE used as proof.
    period=Q(1,100000)
    primitive=Q(9,8)*period
    assert 2+primitive<Q(201,100)
    assert 3*(2+primitive)**2-1<12
    average_drift_floor=Q(3,4)-Q(2,5)
    assert (Q(11,10)+1)/average_drift_floor == 6
    final_lower=Q(11,10)-12*primitive*(3**6-1)
    assert final_lower>1
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (HERE/"source_cache").iterdir() if p.is_file()}
    result={"status":"PASS_MODEL_SIDE_COMPILER_AND_HISTORY_OBSTRUCTION",
            "global_theorem_not_finite_test":"PROOF.md Sections 2,3,6,8",
            "soft_force_surrogate":{"offset":qr(offset),"slope":qr(slope),"wrong_upper":qr(bad_surrogate),
              "one_match_three_zero_correlation":qr(1+3*offset),"two_matches":qr(2),
              "independent_recognizer":soft,"joint_commit":soft_joint,"ordinary_linear":linear,
              "nominal_per_face_error_limit_strict":qr((1-bad_surrogate)/4)},
            "hard_dipole":{"rho":qr(rho),"pixel_motion_over_gap":qr(a),"gap_over_pitch":qr(eta),
              "fractional_half_stroke":qr(s),"fringe_force_error":qr(fringe),"total_force_error":qr(error),
              "joint_commit":hard,"ordinary_linear":hard_linear,
              "quartic_stroke_constraint":"ell <= s*h0/X","linear_stroke_constraint":"ell <= 2*s*h0"},
            "unowned_two_bit_counter":{"period":qr(period),"time":6,"both_state_lower":qr(final_lower),
              "never_two_good_inputs":True,"proof":"one-sided Lipschitz, rational exp(6)<729"},
            "finite_inertia_obstruction":{"initial_position":qr(xl),"initial_velocity":1,
              "illegal_drive":qr(-Q(3,2)),"test_time":qr(tm),"position_lower_unless_crossed":qr(inertial_lower)},
            "source_hashes":source_hashes,"physical_shots":0,"external_actions":0,
            "precision":"Fraction exact; Sympy symbolic derivatives; floats display only",
            "wall_seconds":time.perf_counter()-start}
    (HERE/"FORCE_COMMIT_RECEIPT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"soft_joint_gap":soft_joint["gap"],
      "hard_joint_gap":hard["gap"],"counter_lower":qr(final_lower),"wall_seconds":result["wall_seconds"]},indent=2))


if __name__=="__main__":
    main()
