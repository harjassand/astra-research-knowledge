# Why the joint strength bound cannot be replaced by mean noise power
2026-10-30. Root boundary calculation, not a novelty claim. This is independent of whether the topology-free extension is accepted.

Consider a distance-growing code with a nontrivial logical Pauli L=product_(i in S)P_i. Let an initially classical shared bath bit be 1 with probability p_N and 0 otherwise. During a pulse of duration tau_N=pi/(2A_N), add

    H_noise=A_N |1><1|_B tensor sum_(i in S)P_i.

Each system term is onsite, although all share the bath bit. In the bath-1 branch, its noise-only unitary is L up to a phase. In the bath-0 branch it is identity.

Suppose the actual nominal finite-rate controller has total non-bath generator norm at most C N during this interval. Duhamel comparison bounds its change to the ideal pulse channel by O(N/A_N), including its finite apparatus and any reset records. After the pulse, turn this added noise off. An undetected logical Pauli on encoded DATA cannot be distinguished from a different legitimate logical input by the same preserving controller.

Take A_N=N^2 and p_N=eta^2/A_N^2. The expected squared coupling at EACH affected site is p_N A_N^2=eta^2, a fixed arbitrarily small number; its mean absolute coupling is even smaller. Nevertheless, the resulting encoded logical channel has an order-p_N logical-Pauli component, up to relative O(N/A_N) corrections. For a logical input orthogonal to its L transform, this gives polynomial rather than exponential logical error, of order eta^2 N^(-4).

The unconditioned comparison error is weighted by p_N: both branches have the same nominal evolution except for the rare pulse, so the pulse approximation costs O(p_N N/A_N), not O(N/A_N). Subsequent CPTP evolution cannot amplify that discrepancy. At fixed final storage time, the rare logical error remains incompatible with a uniform exp(-cN) guarantee based only on this mean-power condition.

This is an allowed counterexample to a MEAN-STRENGTH-only noise class, not to the bounded joint-norm theorem: the peak local interaction norm is A_N and violates its hypothesis. A common environment with rare simultaneous strong excursions is the critical issue. More physical unbounded-bath models require additional tail, dynamical or symmetry assumptions and an earned theorem; finite observed variance or a small reduced-state calibration score is not a substitute.
