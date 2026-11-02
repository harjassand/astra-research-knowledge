# Independent trial: source-certified dynamic passive port compression

**Origin**: Independent research role, 2026-11-02. Base repository revision **5489b118101275c81500d823361592c670ec77bb**, before other trial-role proposals. **Not** a laboratory device, independent mathematical review, historical novelty claim, or civilization-scale achieved capability.

## Consequential question and result

Can real scalar pulse/step experiments on an unknown fixed dissipative physical network support *new controls and price objectives* without reconstructing its internal degrees of freedom? For a grounded linear RC multiport `C xdot=-Gx+Bu, y=B^T x`, with source reset and calibrated scalar collocated report `q_v(t)=v^T y_v(t)/t` accurate within `eta`, we construct a sound experimental certificate with no input pole count or rate bound.

Acquire measured `R0=S(t0)/t0` diagonal and `r` selected actual columns by single and pair-port scalar commands. Form a port reconstruction `L=E_J Z`, measured source norm upper `M0`, and sound residual trace upper `D` from entrywise noise caps. Then **for every time** `t` in a specified horizon:

`||S(t)-L^T S(t)L||op <= max(t,t0) [2 sqrt(M0 D)+D]`.

Analytic interpolation of `S(t)/t` in `log t` on selected ports (piecewise Chebyshev, no acquired eigenrates) yields a dimension-free (in hidden nodes) number of scalar experimental settings:

`m+r(m-1)+(r(r+1)/2)(n+1)ceil(log(T/t0))`.

It produces a correct bound on outputs under every later bounded-variation current history. A sharper *task-dependent* bound certifies specific terminal actions without incurring the loose global operator radius.

For fixed known rectangular waveform, linearity plus vertex-interval separation certifies the **unique optimum over the entire nonnegative port allocation simplex**, not just a discrete menu. For one pulse with continuously variable onset, the passive fact `0<=K(t)<=R(t0)` for `t>=t0` and a finite time mesh give a **continuous allocation-and-timing global regret bound** (complete derivation in THEOREM_AND_PROOF.md).

## Actual executed numerical tests

- Hidden synthetic grounded RC states: **180**; controllable port channels: **24**; acquired adaptive ports: **4**; logarithmic time panels: **8**; Chebyshev degree: **22**.
- Native scalar experiment count: **1,956**. Assumed calibrated normalized scalar error <= **1e-7**. Earliest raw output accuracy requires **4e-10 benchmark units**. Total experimental step-duration **1310.6 simulation time units**, excluding instrument resets, calibration, settling and trial repetition.
- Withheld max full step-operator error on 221 times: **1.6205e-5**. The best tested **ordinary cubic spline on the same data** instead achieves **1.5180e-5**, slightly better.
- **Failure retained**: universal all-waveform operator-error certificate **2.5442**, far too loose for useful controller decisions.
- New fixed pulse [3.5,4.5], terminal T=5, target port7 with new port7 cost 0.1: the acquired intervals certify **port4 as unique optimal for every fractional 24-port allocation**. Chosen lower **0.114915335698**, strongest other upper **0.106645569401**, strict source-class margin **0.008269766298**.
- Broader **continuously timed one-unit pulse**: every fractional port allocation and onset in [0,3.996]; a 4,001-timepoint offline grid plus source-derived Lipschitz bound certifies **global regret <=0.009630017986**, selects port7, onset3.996, using **zero new source experiments**. Certified chosen lower **0.370736031853**, global upper **0.380366049839**.
- Exact-real theorem is source-conditional. Benchmark floating execution is **not** an interval-verified implementation or real-source experiment.

## Fair existing solutions and hardest debts

The physical spectral representation is old: Zemanian, *Relaxive Hilbert Ports* (1974; DOI 10.1137/0312010). Adaptive PSD-column recovery is strongly developed: Chen–Epperly–Tropp–Webber, *Randomly Pivoted Cholesky* (2025; DOI 10.1002/cpa.22234). Loewner, AAA, rational fitting and smooth splines compete on the same acquired data (Aumann–Gosea, DOI 10.1002/acs.3691). The strongest not-yet-implemented comparator is **adaptive Nyström acquisition + certified matrix-valued positive spectral moment optimization (passive Loewner/moment SDP)** on identical scalar reports, including a rigorous finite-spectral-grid error. It may match or improve our certificate. Do not claim exclusive algorithmic or practical advantage.

Astra N1571 at the fixed revision is a **static resistor shunt/dose-response** result, not the acquired dynamic current/terminal interface here. No interface is borrowed for free.

Principal unpaid obligations: physical source qualification and real sensor/actuator calibration; short-time measurement precision and resetting cost; physically realistic instantiation; feedback/multipulse/unknown-input controller rather than a single open-loop pulse; a full same-data certified passive SDP comparator; independent proof and numerical interval review.

## Files and replay

- [THEOREM_AND_PROOF.md](THEOREM_AND_PROOF.md) — complete definitions, proof, exact source contract, temporal and task control certificates, comparisons, and frozen original source Git SHA/readbacks.
- [prototype.py](prototype.py) — reproducible synthetic 180-state scalar-only acquisition pilot, withheld diagnostics and matched spline/AAA checks. Run `OPENBLAS_NUM_THREADS=1 python prototype.py` with Python, NumPy, SciPy.
- Additional reproduction scripts, saved numerical data and SHA256 manifest are distributed in the current ChatGPT conversation artifact `astra_independent_temporal_port_compression.zip`. The GitHub branch intentionally stays separate from main and peers' independent outputs.

**Status**: a meaningful, physically conditional acquisition-to-continuous-intervention certificate with an executable positive example and a known failure of the all-purpose bound; not the full civilization-scale capability.
