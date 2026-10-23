#!/usr/bin/env python3
"""Principal finite checks of the new anchor inequality (stdlib, no sampling)."""
from decimal import Decimal as D, localcontext
import hashlib
import json
from pathlib import Path
import resource
from time import perf_counter, process_time
from experiments import (ONE, ZERO, identity, convex_mix, mh_kernel, path_proposal,
                         law_after, family, tv, kl, fmt)

root = Path(__file__).resolve().parent
started, cpu_started = perf_counter(), process_time()
rows = []
with localcontext() as ctx:
    ctx.prec = 360
    alpha = D(".5")
    # Fixed before evaluation: prior four-state input and the already-fixed funnel.
    pi4 = list(map(D, (".01", ".10", ".29", ".60")))
    q4 = list(map(D, (".0001", ".20", ".30", ".4999")))
    pi3, q3, _, _ = family(D(".05"))
    for label, pi, q in (("shared_four_state", pi4, q4), ("previous_funnel_p_0.05", pi3, q3)):
        G = mh_kernel(pi, [list(q) for _ in pi])
        L = mh_kernel(pi, path_proposal(len(pi)))
        C = convex_mix(identity(len(pi)), convex_mix(G, L, alpha), ONE/2)
        K, J = kl(pi, q), kl(q, pi)
        W = [x/y for x, y in zip(pi, q)]
        M = (2*K+ONE).exp()
        s0 = sum((p for p, w in zip(pi, W) if w <= M), ZERO)
        assert s0 >= ONE/2
        for B, R in ((D(3), D(3)), (D(10), D(101)), (D(100000), D(200))):
            core = [ONE/B <= w <= R for w in W]
            qout = sum((p for p, inside in zip(q, core) if not inside), ZERO)
            piout = sum((p for p, inside in zip(pi, core) if not inside), ZERO)
            I = sum((p*max(w, M)*(ONE/w-ONE)**2 for p, w, inside in zip(pi, W, core) if inside), ZERO)
            U = M*(B+ONE)+R
            assert I <= U
            for t in (1, 10, 100, 1000, 1000000):
                # Check every event of each finite state space, not just TV.
                max_anchor_ratio = ZERO
                for mask in range(1 << len(pi)):
                    indicator = [D(bool(mask & (1 << i))) for i in range(len(pi))]
                    # Evolved observable uses column action; transpose via explicit sums.
                    transition_columns = [[C[i][j] for i in range(len(pi))] for j in range(len(pi))]
                    g = law_after(indicator, transition_columns, t)
                    m = sum((p*x for p, w, x in zip(pi, W, g) if w <= M), ZERO)/s0
                    energy = sum((pi[i]*C[i][j]*(g[i]-g[j])**2
                                  for i in range(len(pi)) for j in range(len(pi))), ZERO)/2
                    spectral_ceiling = ONE/(4*(2*t+1))
                    assert energy <= spectral_ceiling+D("1e-280")
                    energy_g = sum((pi[i]*G[i][j]*(g[i]-g[j])**2
                                    for i in range(len(pi)) for j in range(len(pi))), ZERO)/2
                    anchor_integral = sum((p*(x-m)**2/max(w, M) for p, w, x in zip(pi, W, g)), ZERO)
                    assert s0*anchor_integral/2 <= energy_g+D("1e-280")
                    outside = sum(((qi-pi_i)*(gi-m) for qi, pi_i, gi, inside in zip(q, pi, g, core) if not inside), ZERO)
                    assert abs(outside) <= max(qout, piout)+D("1e-280")
                actual = tv(law_after(q, C, t), pi)
                exact_core_bound = max(qout, piout)+(I/(alpha*s0*(2*t+1))).sqrt()
                stated_bound = max(qout, piout)+(U/(alpha*s0*(2*t+1))).sqrt()
                assert actual <= exact_core_bound+D("1e-280")
                rows.append({"case": label, "B": str(B), "R": str(R), "t": t,
                             "K_actual": fmt(K), "J_actual": fmt(J), "M": fmt(M), "s0": fmt(s0),
                             "actual_outside_max": fmt(max(qout, piout)), "I_actual": fmt(I),
                             "TV": fmt(actual), "bound_with_actual_core_integral": fmt(exact_core_bound),
                             "stated_bound": fmt(stated_bound)})
result = {"all_checks_passed": True, "precision_decimal_digits": 360,
          "not_a_universal_or_interval_proof": True,
          "inputs_selected_before_this_evaluation": True,
          "event_checks": "Every subset of each fixed finite state space, at every recorded B,R,t",
          "rows": rows,
          "resources": {"wall_seconds": perf_counter()-started,
                        "process_cpu_seconds": process_time()-cpu_started,
                        "peak_process_RSS_KiB_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
(root/"results/joint_kl_checks.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"all_checks_passed": True, "finite_comparisons": len(rows),
                  "resources": result["resources"], "example": rows[9]}, indent=2))
