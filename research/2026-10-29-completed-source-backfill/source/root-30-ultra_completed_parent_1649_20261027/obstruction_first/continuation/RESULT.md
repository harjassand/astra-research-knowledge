# Compressed spin-two thermal inputs: warm operation acquired, cold seed missing

The continuation acquires certified partition/purity information for actual
128-,256- and512-site uniform spin-two rings from a three-vector compression
of the source's continuous history kernel. It includes an explicit bound on
every omitted spatial mode. **It does not prove the uniform spin-two gap or
acquire the required cold bootstrap pair.** No physical experiment, hardware
capability, exhaustive priority clearance or matched algorithmic speedup is
claimed.

The substantive operation is in CONSTRUCTION.md. Empty endpoint histories
turn the kernel's vacuum moments into thermal traces of open chains1–6.
Their exact all-state integer moments are acquired by CRT, with checked
no-overflow bounds and explicit Taylor tails. A rational three-vector trial
then gives a Rayleigh quotient and residual. Complete even moments count all
other modes before Temple's inequality is applied. This uses the actual
source kernel rather than assuming a fitted finite-rank model is correct.

The unprojected result includes log(Z256/5^256) widths below2.678e−11 at
beta1/8,5.197e−8 at1/4, and2.159e−4 at1/2. Parent independently replayed
those three inputs with stdlib Fraction exponential/Taylor bounds; that
receipt does not cover the subsequent A4 work. The source's established A4
rotation projection, with actually acquired P/C traces, extends the counted
mode through beta1.25 and fails at1.5. It proves

    1−S(256,3/4)<1.851e−24,
    1−S(256,1)<7.586e−13.

The first bound passed a separate Fraction replay in verify_continuation.py,
without mpmath or producer imports. Both replays consume exact CRT integers;
neither reruns every modular matrix multiplication on open chains4–6.

This now gives an actual warm restart for the source's all-temperature
identity: S256 at beta3/4 followed by seven doublings to beta96 requires
fourteen normalized thermal purities on rings256/512, plus final T512(96).
The fifteen cold/intermediate inputs remain unacquired. Their declared log
precision budget is explicit in data/thermal_purity_lift.json, including
the propagated initial error. The source criterion uses S(L,b) and **T(2L,b)**.
Earlier casual same-ring wording has been corrected; no seed claim relied on it.

The cold limitation is also constructive. A numerical producer supplies
dyadic Cholesky/inverse candidates, then exact rational products prove
H_open5>=−19.604. SU(2) completeness and Anderson averaging give H_n>=−4.901n.
Therefore TrK^4/||K||^4>=exp(.396beta)/625. The unprojected one-mode p4 count
cannot work after beta18.0073, even with an exact leading vector. The A4
version cannot work after24.2823; at beta64, a p4 trace-residual scheme needs
over13.54million captured invariant modes merely to reduce its residual mass
below one mode. This constrains that specific tail method, not arbitrary
MPO compression, higher moments, sector methods or the physical gap.

Supporting work in ORDER_AND_NORM.md preserves an exact reflection-positive
local gate, the actual CP dimension/readout cost, an NPT boundary for the
strong-noise/EB route, an acquired all-ring Strang relative-residual bound,
and a weaker norm-aware positive temperature lift. A400-site dimer control
executes that norm lift; a uniform-chain positive spike proves why HS error
alone can amplify enormously. None of those controls supplies the cold
uniform-chain MPO. The exact pair-gate rank25 budget is kept separate from
the quadratic rank9 gate and its Taylor error.

Strong ordinary comparators already include full-column validation,
symmetry-resolved counted spectra, sign-free QMC, all-Schatten controlled
thermal MPOs, Araki transfer algorithms, MED and direct local-purity
factorization. The last theorem is an interval result with beta-dependent
constants. Folding a ring into a dimension25 open ladder preserves its loop
but still needs endpoint control and paired-site marginal acquisition.
Source versions and exact scopes are in SOURCES.md. No advantage is inferred
from fixed local tensor storage, positivity or warm finite examples.

## Actual cost and replay

Recorded exact open-moment producer times were5.00s at degree24,46.53s at96
and175.69s at192, all single-threaded. The P/C four-site acquisition took
1.27s/1.39s. The accepted rational open5 proof took1.52s. The warm interval
consumer took under.3s; symbolic gate/orientation diagnostics took roughly
.5–1s. Failed producer invocations, rejected raw Cholesky candidates,
independent Fraction replay, source acquisition and proof work are additional
costs. No original source full verifier or cold MPO contraction was run.

The largest modular dense sector is1751x1751,24.5MB per int64 array; a few
such arrays coexist. Actual process peak RSS was not instrumented. The
earlier stage1 spectra/MPS work remains frozen and its costs are not erased
or treated as free. No formal proof-assistant or physical audit is claimed.

Run from this folder with PYTHONDONTWRITEBYTECODE=1 and BLAS/OMP threads1–2,
using the read-only solver_runtime/.venv/bin/python:

    python acquire_open_moments.py --degree 96
    python acquire_open_moments.py --degree 192
    python acquire_twisted4_moments.py
    python vacuum_krylov_transfer.py --degree 96
    python vacuum_krylov_transfer.py --degree 192 --sector-aware
    python verify_continuation.py
    python cold_moment_boundary.py
    python thermal_purity_lift.py

The other actually used supporting cores are local_gibbs_gate.py,
cp_generator_equivalence.py, relative_order_bridge.py,
norm_temperature_bridge.py and compile_seed_requirements.py. The final
scientific boundary is explicit: warm compressed inputs and a cold method
obstruction are achieved; the cold normalized-purity/MPO-tail interface and
uniform gap remain unachieved.
