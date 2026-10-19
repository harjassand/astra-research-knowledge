> Public selected edition of the 19 October audit. Original review SHA-256: `0c9c6162849916455303bf4f95c21dc34dbaba16d807091b402ad3e19d937376`. Original scientific inputs are retained unchanged. Navigation and historical-receipt pointers are adapted to the selected public subset; mathematical statements, caveats and attribution are retained. Past private-audit statements describe that audit, before approved publication. Current reproduction and retained-file hashes are in the release README and FILES.json.

# Independent audit of the explicit finite-ramp certificate

**Conclusion: bounded mathematical support; no blocking error found in the stated five-piece, two-duration construction.** The certificate's exact rational estimates were reproduced independently with Python standard-library `Fraction` arithmetic. The analytic step needed to turn those estimates into actual positive waveform existence also has a valid derivation, given below. This is an audit of the specified mathematical model, not physical validation, novelty clearance, or a practical identification result.

The conclusion covers labels `(1,3,8,10)`, orders `(1,4,2,3)` and `(2,3,1,4)`, eta=`2^-128`, and the two positive durations `d=5 log 2` and `2d`. It does not independently audit the arbitrary-finite-menu theorem or the smooth endpoint-matching corollary.

## Source pinning and independence

The private frozen source root was `sources/ultra` below this verification root. Inspected files and SHA-256:

| File | SHA-256 |
|---|---|
| `workers/kinetic_frontier/exact_collision_certificate.py` | `e6f6dc44f92ca6c949df839bc8d578653365933322487e9a49f9a20869f44dda` |
| `workers/kinetic_realization/fixed_hazard_jacobian.py` | `45a7f7085f7ea7b69f8de9440f34866d1627ac01946b5f34128480b680328fdf` |
| `workers/kinetic_frontier/THEOREM.md` | `a3383e0215400ed6e8a3082e2d3ab8941d9bb2cc96ce5bc0d75d56be2788b5b2` |

The source modules and theorem were read before execution. Required proof obligations were recorded in `obligations_before_checks.md` before numeric checks. No retained JSON output or prior audit was used as input. A broad source-search command accidentally exposed two claim paragraphs from the worker's `REPORT.md` while locating `THEOREM.md`; this limits source-blindness and is recorded rather than concealed. No other reviewers' work was read.

`independent_certificate_check.py` imports neither inspected module. In particular, its Jacobian is not copied from the helper or obtained by executing that helper. Only after the independent reconstruction succeeded were the two inspected Python files copied into this review's disposable tree and replayed. The original source hashes remained unchanged. All writes are beneath this review directory; no repository/public files were edited.

## Independent endpoint differential and exact bounds

Let `h=D log 2`, `D in {1,2}`, and let `P_i` be the physical spectral projectors of `Q(a)` computed by

    P_i = product_(j!=i) (Q(a)+a_j I)/(a_j-a_i).

The one-interval flow is `E=sum_i 2^(-D a_i) P_i`. For a stage derivative generator `B`, write the off-diagonal spectral part of the interval Frechet derivative as

    L = sum_(i!=j) P_i B P_j (2^(-D a_j)-2^(-D a_i))/(a_i-a_j).

The omitted diagonal spectral term is `h sum_i 2^(-D a_i) P_i B P_i`. It contributes the same matrix at every interval position and cancels exactly in a compensated control. Thus the physical compensated derivative for a variation in interval `ell` and its negative in interval 4 is

    E^(4-ell) L E^ell - L E^4,      ell=0,...,3.

This reconstruction includes every spectral projector pair and then reads the physical strict-lower entries. It avoids the source's eigenbasis lower-entry formula, so it independently tests its sign, chronological order, interval compensation, coordinate choice, and conditioning. Both resulting 12x12 matrices have exact nonzero determinant, and their exact inverses multiply to the identity on both sides. Their entries, inverses, determinants, and infinity norms match the source replay exactly.

| Ordered baseline | `||J(0)^-1||inf` | Determinant, approximately |
|---|---:|---:|
| `(1,10,3,8)` | `3.3969655974943666e25` | `-3.999177127557257e-100` |
| `(3,8,1,10)` | `2.4923317159897347e28` | `-4.937255713033651e-102` |

The exact rational values are in `independent_checks.json`, together with the full Jacobians and inverses. Consequently

    alpha = 2.4923317159897347115968928009784643e28 approximately,
    r = 1/(4 alpha * 9216)
      = 1.0884079329038574624641172593816753e-33 approximately.

For each source target I independently computed the raw physical discrepancy, multiplied by the independently obtained inverse, and took its exact infinity norm. Decimal values below display exact rational comparisons; no floating-point inversion or optimizer was used.

| Order index | Direction | `beta/r` | Contraction upper bound `q` |
|---|---|---:|---:|
| 0 | outward | `0.0000445589573039518929` | `0.000340741721467179478` |
| 0 | return | `0.0000294605282475723422` | `0.000340741721467179478` |
| 1 | outward | `0.000354291577735642403` | `1/4` exactly |
| 1 | return | `0.000222166761258321713` | `1/4` exactly |

The displayed theorem bound `beta <= 0.00035429158 r` is a valid upper bound, including its last displayed decimal. The largest `beta/r+q` is below `0.250354292`, far below 1. The inverse norms are very large, but they are charged explicitly through the small radius; they are not hidden by normalized/spectral output coordinates.

## Analytic step: positivity, Hessian bound, and Banach

The following argument is essential. Executing the source script alone does not prove it or sample it over the parameter box.

For each of stages 1 through 3, the first four intervals use rates `a_i+v_i,ell`, while the last interval uses `a_i-sum_ell v_i,ell`. Stage 4 remains fixed. On `||v||inf<=r`, rate deviations are at most `r` in the first four intervals and `4r` in the last. Since the exact rational `r<1/16`, every rate is strictly above `1-4r>3/4` and below `10+4r<11`. This holds throughout the closed convex box, so all completed five-state generators are Markov generators there and their propagators have induced column 1-norm 1.

For any one parameter, the completed generator derivative is `+B_i` on one interval and `-B_i` on the last, with zero elsewhere. `||B_i||1=2`, so its integrated norm is

    M = 2*(2 D log 2) = 4 D log 2 < 8.

Duhamel differentiation expresses the first derivative as a single insertion between stochastic propagators. The mixed second derivative is the sum of the two chronological insertion orders. Bounding the propagators by 1 and combining the two triangles of the time square gives

    ||partial_a partial_b U||1
      <= (integral ||B_a(t)||1 dt)(integral ||B_b(t)||1 dt)
      = (4 D log 2)^2 < 64.

The formula also covers identical parameters; its factor of 2 fills the two half-squares and creates no additional factor. Piecewise-constant coefficients are analytic functions of the finite parameters, so the differentiations and mean-value argument are legitimate. Each raw transient entry is bounded by this full-matrix norm. Hence each scalar Hessian entry is below 64 uniformly on the entire box. This proves, rather than samples, the needed estimate. Exposition clarification: a bound on the first derivative alone would not imply the Hessian bound; the source's brief “therefore” needs precisely this second-order insertion argument.

There are 12 output rows and 12 parameters. Each Jacobian entry changes by at most `12*64*r`; summing a row gives

    ||J(v)-J(0)||inf <= 12^2*64*r = 9216*r.

For `A=J(0)^-1`, the identity `A J(0)=I` yields

    ||I-A J(v)||inf <= ||A||inf*9216*r = q <=1/4.

The exact residual estimates give `||N(0)||inf=beta` for `N(v)=v-A(F(v)-target)`. Therefore `||N(v)||inf <= beta+q*r<r`, and `N` is a contraction of the closed radius-r box into itself. Banach gives one exact parameter vector in this box for each direction and each order. Invertibility of `A` makes its fixed-point equation precisely the desired endpoint equation. There is no remaining unproved numerical inequality in this scoped argument; the script itself still relies on the analytic Duhamel/stochastic-contraction reasoning supplied here.

## Fixed hazards, rational branch, residues and all words

Every control integrates to zero: the same physical interval length `D log 2` multiplies `+v` and `-v`. The integrated hazard is exactly `5D log 2*a_i` for each physical stage. Thus the physical diagonal is exactly `2^(-5D a_i)` for every point in the box; at the two durations `R_2,ii=(R_1,ii)^2`. This is an exact affine tie in log-diagonal coordinates, not an approximate Jacobian statement. Both outward and return targets satisfy it. The hazard is fixed to the ordered A labels even for a return waveform; the piecewise construction does not impose the pure B endpoint rates on that waveform.

The rational branch identity `12(9+w)^2-5(5+u*w)^2=847`, both pair-sum equalities, both scaled-product equalities, positivity/distinctness of mu, `t!=1`, and all six pairwise response-ratio inequalities were checked with exact fractions. Direct closed-product residue formulas, independent of the eigenvector routine, agree by label in both directions. In particular,

    t-1 = 8.1318325995859986623427575534670552e-40 approximately,
    min_(i!=j)|mu_i/lambda_i-mu_j/lambda_j|
        = 3.9755626042420437904786814705838937e-40 approximately.

The ratios are exactly distinct, but their separation is extremely small. Those inequalities do not imply a useful experimental margin.

I separately constructed the controllability gauges `T_A,T_B` and obtained exact zero for all ten preparation, readout, generator, and ramp-intertwining residuals. They establish

    T_m e=e,   c T_m=c,   Q_m^(1) T_m=T_m Q_m^(0),
    F_D^(1) T_A=T_B F_D^(0),
    G_D^(1) T_B=T_A G_D^(0),    D=1,2.

The generator identities imply `exp(t Q_m^(1))T_m=T_m exp(t Q_m^(0))` for every `t>=0`. Multiplying the appropriate identities along any finite legal word telescopes the intermediate gauges. Preparation/readout identities then give equal terminal noncompletion probabilities, hence equal completed/incomplete endpoint laws. This is an all-word algebraic proof; it does not infer universality from a finite test grid.

The source's 64 replay samples use rational exponentially distributed holds `z(zI-Q)^-1`, with `z` drawn from `{1,2,3,5}`, and words up to 16 operations. They are not 64 deterministic-time exponential-flow replays. This is a scope clarification rather than a defect in the theorem: the exact generator intertwinings independently cover arbitrary deterministic hold durations. Nothing here establishes the distribution of completion times or intermediate readouts inside a ramp.

## What is and is not explicit

The source computes rational targets, Jacobians, inverses, a parameter box, preconditioned residuals, and endpoint gauges. It does not evaluate the fixed-point iteration or output fitted waveform coefficients. Its phrase “actual positive shared waveform exists” depends on the analytic step above.

The waveform is specified exactly by `v^(0)=0`, `v^(n+1)=N(v^(n))`, `v*=lim_n v^(n)`, followed by the five-interval rate formulas. This is a convergently defined implicit witness and an actual bounded positive waveform in the mathematical model. It is not a finite table of exact/numeric waveform coefficients. Each of the four root vectors supplies one shared waveform stretched to both durations; no independent-per-duration waveform has been introduced. The construction permits jumps at interval boundaries and at the pure-mode interfaces. Smooth endpoint matching, monotonicity, envelope constraints, time reversal, and a calibrated rate-control interface are not established by this explicit box.

## Commands and actual execution evidence

Working directory for all audit executions: this review directory. The source files were executed only under `disposable/`.

1. `python3 -I -B independent_certificate_check.py` — exit 0, CPU budget 180 seconds, observed elapsed calculation time about 0.058 seconds. Actual stdout is in `independent_stdout.txt`; exact results and full matrices are in `independent_checks.json`.
2. First `python3 -I -B replay_disposable.py` — exit 1 because its initial child `-I` option hid the already installed user-site SymPy. The actual `ModuleNotFoundError` and diagnosis are recorded in `initial_replay_failure.json`. No dependency was installed.
3. The same runner after changing only copied-source child flags to `-E -B` — exit 0. It used existing local SymPy, a 60-second wall and CPU limit for each source subprocess, and no network operation. Both source scripts exited 0. The helper printed its rank12 message; the collision script printed its scoped `PASS_EXACT_RATIONAL_POSITIVE_SHARED_WAVEFORM_COUNTEREXAMPLE` receipt and 64 replay count. These source status strings are implementation receipts, not the audit conclusion. Full commands, stdout, stderr, elapsed times, and 12 exact source-versus-independent comparisons are preserved in `replay_results.json`.

No optimizer, optimizer restart, network lookup, installation, publication, author contact, or research redirection was used. No claim of historical priority, physical capability, practical advantage, or mission achievement follows from these checks.
