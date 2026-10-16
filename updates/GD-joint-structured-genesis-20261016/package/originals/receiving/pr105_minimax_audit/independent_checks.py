#!/usr/bin/env python3
"""Bounded original checks for PR105. No acquired repository code is imported or run."""
from pathlib import Path
import hashlib
import itertools
import json
import math
import sys
import numpy as np
import scipy
from scipy.linalg import expm
import sympy as sp

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(1052688)

def q_bound(actions):
    return 1.0 - math.prod(math.cos(min(float(a), math.pi / 2)) ** 2 for a in actions)

def unitary(h):
    w, v = np.linalg.eigh(h)
    return (v * np.exp(-1j * w)) @ v.conj().T

def pinch(x, b):
    y = x.copy()
    y[:b, b:] = 0
    y[b:, :b] = 0
    return y

def endpoint_effect(gaps, b):
    effect = np.diag([0.] * b + [1.] * b).astype(complex)
    for k in reversed(range(len(gaps))):
        effect = gaps[k].conj().T @ effect @ gaps[k]
        if k:
            effect = pinch(effect, b)
    return effect[:b, :b]

def exact_sink():
    # Three exact rotations, on an eight-dimensional joint memory/bath space.
    cs = [(sp.Rational(4, 5), sp.Rational(3, 5)),
          (sp.Rational(12, 13), sp.Rational(5, 13)),
          (sp.Rational(15, 17), sp.Rational(8, 17))]
    m, b = len(cs), len(cs) + 1
    def u(k, sign):
        c, s = cs[k - 1]
        mat = sp.eye(2 * b)
        for x, y in [(0, b + k), (k, b)]:
            mat[x, x] = mat[y, y] = c
            mat[x, y] = mat[y, x] = -sp.I * sign * s
        return mat
    rho = sp.zeros(2*b)
    rho[0, 0] = 1
    for k in range(1, m + 1):
        mat = u(k, 1)
        rho = mat * rho * mat.conjugate().T
        if k < m:
            for i in range(b):
                for j in range(b, 2*b):
                    rho[i, j] = rho[j, i] = 0
    expected = 1 - sp.prod(c*c for c, _ in cs)
    actual = sum(rho[k, k] for k in range(b, 2*b))
    assert actual == expected
    e0 = sp.eye(2*b)[:, 0]
    walsh_values = []
    for bits in itertools.product([0, 1], repeat=m-1):
        outputs = []
        for f in [0, 1]:
            state = e0
            parity = f
            for k in range(1, m+1):
                if k > 1:
                    parity ^= bits[k-2]
                state = u(k, (-1)**parity) * state
            outputs.append(state)
        odd = (outputs[0] - outputs[1]) / 2
        even = (outputs[0] + outputs[1]) / 2
        weight = (odd.conjugate().T * odd)[0]
        assert weight == expected
        assert all(odd[i] == 0 for i in range(b))
        assert all(even[i] == 0 for i in range(b, 2*b))
        walsh_values.append(str(weight))
    return {"bath_dimension":b, "action_sines":[str(s) for _,s in cs],
            "exact_final_flip":str(actual), "exact_prediction":str(expected),
            "all_four_toggle_paths_odd_walsh":walsh_values,
            "float_probability":float(actual)}

def random_joint_effects():
    cases = []
    for c in range(144):
        b = 1 + c % 5
        m = 1 + (c // 5) % 6
        actions = RNG.uniform(0.005, 0.8 if c < 120 else 2.2, m)
        gaps = []
        max_one_gap_excess = -1.0
        for a in actions:
            # Three independent noncommuting pieces per gap, all with exact odd norm a/3.
            gap = np.eye(2*b, dtype=complex)
            for _ in range(3):
                d = RNG.normal(size=(b,b)) + 1j*RNG.normal(size=(b,b))
                d *= (a/3) / np.linalg.norm(d, 2)
                h = np.zeros((2*b,2*b), dtype=complex)
                h[:b,b:] = d
                h[b:,:b] = d.conj().T
                for ix in [slice(0,b),slice(b,2*b)]:
                    raw = RNG.normal(size=(b,b)) + 1j*RNG.normal(size=(b,b))
                    block = (raw+raw.conj().T)/2
                    h[ix,ix] = 1.7 * block
                gap = unitary(h) @ gap
            gaps.append(gap)
            cross = gap[b:,:b]
            err = np.linalg.norm(cross, 2)**2 - math.sin(min(a,math.pi/2))**2
            max_one_gap_excess=max(max_one_gap_excess, float(err))
        effect = endpoint_effect(gaps,b)
        largest = float(np.linalg.eigvalsh((effect+effect.conj().T)/2)[-1])
        upper = q_bound(actions)
        good = np.eye(b,dtype=complex)
        for gap in gaps:
            good = gap[:b,:b] @ good
        survival_min=float(np.linalg.eigvalsh(good.conj().T @ good)[0])
        assert largest <= upper + 2e-12
        assert survival_min >= 1-upper-2e-12
        assert max_one_gap_excess <= 2e-12
        cases.append({"bath_dimension":b,"gaps":m,"actions":actions.tolist(),
                      "endpoint_effect_norm":largest,"upper":upper,
                      "ratio":largest/upper,"good_history_min_eigenvalue":survival_min,
                      "one_gap_max_excess":max_one_gap_excess})
    return {"count":len(cases),"maximum_ratio":max(x["ratio"] for x in cases),
            "minimum_margin":min(x["upper"]-x["endpoint_effect_norm"] for x in cases),"cases":cases}

def sink_numeric():
    cases=[]
    for actions in [[0.],[.1,.2,.7],[.3,0.,.4,1.0],[2.,.3],[.4,1.7,.2],
                    [.1,.2,.3,.4,.5,.6]]:
        m,b=len(actions),len(actions)+1
        gaps=[]
        for k,a in enumerate(actions,1):
            h=np.zeros((2*b,2*b),dtype=complex)
            for x,y in [(0,b+k),(k,b)]:
                h[x,y]=h[y,x]=min(a,math.pi/2)
            gaps.append(unitary(h))
        actual=float(endpoint_effect(gaps,b)[0,0].real)
        target=q_bound(actions)
        assert abs(actual-target)<2e-14
        cases.append({"actions":actions,"actual":actual,"target":target})
    return cases

def optimize_slot_partitions():
    worst=0.0
    count=0
    for m in range(2,8):
        for a in [0.,.1,.8,2.,4.,10.,20.]:
            optimal=q_bound([a/m]*m)
            for _ in range(40):
                partition=a*RNG.dirichlet(np.ones(m))
                excess=optimal-q_bound(partition)
                assert excess<=2e-14
                worst=max(worst,float(excess))
                count+=1
    return {"count":count,"max_violation":worst}

def walsh_virtual_channel():
    cases=[]
    for case in range(24):
        d=1+case%4
        m=2+(case//4)%4
        actions=RNG.uniform(.03,.6,m)
        physical_gaps=[]
        virtual_gaps=[]
        for action in actions:
            raw=RNG.normal(size=(d,d))+1j*RNG.normal(size=(d,d))
            h0=(raw+raw.conj().T)/2
            raw=RNG.normal(size=(d,d))+1j*RNG.normal(size=(d,d))
            a=(raw+raw.conj().T)/2
            a*=action/np.linalg.norm(a,2)
            physical_gaps.append([unitary(h0+a),unitary(h0-a)])
            hv=np.block([[h0,a],[a,h0]])
            virtual_gaps.append(unitary(hv))
        classical=np.zeros((d,d),dtype=complex)
        for bits in itertools.product([0,1],repeat=m-1):
            us=[]
            for f in [0,1]:
                u=np.eye(d,dtype=complex)
                sign=f
                for k in range(m):
                    if k: sign^=bits[k-1]
                    u=physical_gaps[k][sign]@u
                us.append(u)
            odd=(us[0]-us[1])/2
            classical+=odd.conj().T@odd/(2**(m-1))
        virtual=endpoint_effect(virtual_gaps,d)
        distance=float(np.linalg.norm(classical-virtual,2))
        largest=float(np.linalg.eigvalsh(classical)[-1])
        assert distance<3e-14
        assert largest<=q_bound(actions)+3e-14
        cases.append({"physical_dimension":d,"gaps":m,"operator_distance":distance,
                      "walsh_effect_norm":largest,"minimax_upper":q_bound(actions)})
    a=.6
    forbidden=math.sin(a)**2
    allowed=q_bound([a/4]*4)
    assert forbidden>allowed
    return {"cases":cases,"maximum_operator_distance":max(x["operator_distance"] for x in cases),
            "privacy_assumption_falsifier":{"total_action":a,"slots":3,
              "forbidden_private_path_following_error":forbidden,"allowed_independent_adversary_bound":allowed,
              "explanation":"If the coefficient reads the private sign and cancels it, the drive stays coherent. This deliberately violates independence and does not refute the theorem."}}

def poisson(j_segments, rate_segments, durations):
    # Bloch evolution is independent of the covariance-moment ODE used for C.
    yz=np.array([0.,1.])
    moment=0.0
    certificate=0.0
    for j,rate,h in zip(j_segments,rate_segments,durations):
        yz=expm(np.array([[-rate,-2*j],[2*j,0.]])*h)@yz
        if rate == 0:
            integral=moment*h+j*h*h/2
            moment+=j*h
        else:
            decay=math.exp(-rate*h)
            integral=moment*(-math.expm1(-rate*h))/rate+j*(h/rate+math.expm1(-rate*h)/rate**2)
            moment=moment*decay+j*(-math.expm1(-rate*h))/rate
        certificate+=2*j*integral
    a=sum(j*h for j,h in zip(j_segments,durations))
    p=float((1-yz[1])/2)
    kappa=(math.sin(a)/a)**2 if a else 1.
    assert kappa*certificate <= p+2e-13
    assert p <= certificate+2e-13
    return {"a":a,"physical_error":p,"certificate":certificate,"lower":kappa*certificate}

def poisson_checks():
    cases=[]
    for _ in range(120):
        durations=RNG.dirichlet(np.ones(5))
        js=RNG.uniform(.01,2,5)
        a=RNG.uniform(.01,3.0)
        js*=a/sum(js*durations)
        rates=RNG.uniform(0,12,5)
        rates[RNG.integers(0,5)]=0
        cases.append(poisson(js,rates,durations))
    examples=[]
    for n in [1,2,3,8,32]:
        for a in [.001,.2,math.pi/4]:
            h=1/(n+2)
            result=poisson([a]*3,[0,n+2,0],[h,n/(n+2),h])
            cstar=2*a*a/(n+2)
            assert abs(result["certificate"]-cstar)<2e-14
            grid=q_bound([a/(n+1)]*(n+1))
            assert grid < result["lower"]
            examples.append({"N":n,"a":a,"fixed_grid_exact":grid,"poisson_certificate_star":cstar,**result})
    counterexample={"certificate_optimal_schedule":poisson([3.1]*3,[0,4,0],[.25,.5,.25]),
                    "known_h_competitor":poisson([3.1]*3,[0,100,0],[.49,.02,.49])}
    assert counterexample["certificate_optimal_schedule"]["physical_error"]>.1814
    assert counterexample["known_h_competitor"]["physical_error"]<.0275
    assert sp.Rational(8,1)/(sp.Rational(22,7)**2)>sp.Rational(3,4)
    return {"random_schedule_count":len(cases),"cases":cases,"equal_resource_examples":examples,
            "finite_action_known_h_counterexample":counterexample,
            "rigorous_strict_constant_check":"pi < 22/7 implies 8/pi^2 > 98/121 > 3/4",
            "a_zero_strict_comparison":{"grid":0,"intermediate":0,"poisson":0,"strict":False}}

def replay_accounting_static():
    # This is an independent truth table, not import/exec of acquired Python.
    accepted={"PASS","ENVIRONMENT_BLOCKED","INPUT_EXCLUDED","INSPECTED_NOT_RUN"}
    cases=[]
    for available in [False,True]:
        row="NOT_RUN" if available else "ENVIRONMENT_BLOCKED"
        statuses=["PASS",row,"INPUT_EXCLUDED","INSPECTED_NOT_RUN"]
        overall="PASS" if all(s in accepted for s in statuses) else "FAIL"
        cases.append({"launcher_openpyxl_available":available,"unrun_producer_row":row,"aggregate":overall})
    assert cases[0]["aggregate"]=="PASS" and cases[1]["aggregate"]=="FAIL"
    return {"status_policy_truth_table":cases,"all_dependency_blocked_rows_are_accepted":True,
            "method":"Read-only source inspection plus independent truth table. Acquired wrapper never executed."}

def main():
    result={"scope":"Own exact algebra and bounded numerics; no acquired repository code executed.",
            "pin":"2688d7a383502df4fc1e64001d04bb76e6ec05e5",
            "runtime":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,"sympy":sp.__version__},
            "exact_sink":exact_sink(),"random_joint_effects":random_joint_effects(),
            "numeric_sink":sink_numeric(),"slot_optimization":optimize_slot_partitions(),
            "walsh_virtual_channel":walsh_virtual_channel(),
            "poisson":poisson_checks(),"replay_static":replay_accounting_static()}
    result["check_script_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/"independent_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"exact_sink":result["exact_sink"],
                      "random_joint_effect_count":result["random_joint_effects"]["count"],
                      "random_joint_effect_max_ratio":result["random_joint_effects"]["maximum_ratio"],
                      "slot_optimization":result["slot_optimization"],
                      "walsh_virtual_channel_max_distance":result["walsh_virtual_channel"]["maximum_operator_distance"],
                      "poisson_schedule_count":result["poisson"]["random_schedule_count"],
                      "finite_action_known_h_counterexample":result["poisson"]["finite_action_known_h_counterexample"],
                      "replay_static":result["replay_static"]},indent=2))

if __name__ == "__main__":
    main()
