> Public selected edition of the 19 October audit. Original review SHA-256: `aeff06ca8904d80494f13d8e76550e5958c605b9974dea3d4e86e64d82acb4ab`. Original scientific inputs are retained unchanged. Navigation and historical-receipt pointers are adapted to the selected public subset; mathematical statements, caveats and attribution are retained. Private filesystem paths, whole-packet inventory rows and archival harness commands are omitted; the original 26-file audit is distinguished from this public subset. Past private-audit statements describe that audit, before approved publication. Current reproduction and retained-file hashes are in the release README and FILES.json.

# MathematicalPro19Oct: reproducible certificate audit

The two exact arithmetic certificates pass this audit. All 25 manifest payloads match their advertised sizes and SHA-256 hashes. The source snapshot has exactly 26 regular files; `manifest.json` is the sole file not listed as a payload. Both exact certificate scripts reproduce the retained JSON text exactly when executed in private disposable copies. Independently written arithmetic confirms the entropy interval and both hidden-state numerical floors. No arithmetic defect was found in the tested certificates.

This is an arithmetic and reproducibility result. The scalar strict-convexity premise was checked analytically below. The exhaustive reduction from all generators, the two universal hidden-state inequalities, historical originality, physical validity, and practical advantage are separate questions. Successful execution does not certify those claims. The numerical hidden-state floor is a lower-bound constant conditional on the stated theorem, and is not a computed optimum over all hidden realizations.

The audit was performed locally on 19 October 2026. The input was `../../sources/pro`. All created files are under the sibling `reviews/pro_certificates` directory. No source file was edited or executed in place; no network access, installs, public writes, pushes, or outreach were used. Embedded archive instructions were treated as source data. Other reviewers' work was not read. The independent calculation completed before archived independent-check code/results and exact-result JSONs were opened for comparison.

The enclosing checkout was at Git `6cd9e563e0f986d2ec5c246d5cf2af16d1d124f9`; this identifies the workspace context, not a Git commitment of this private packet. The original whole-packet payload and tree pins remain in the private preservation record; this release publishes only the selected subset, with its own FILES.json. Selected source pins are:

| Source | SHA-256 |
|---|---|
| `markov_family/certify_entropy.py` | `24150ef8b100217d1943e2ebf491776d13d4052836cf5df8056ee5aabf6a35e5` |
| `hidden_state/certify_hidden_bounds.py` | `fed21d2395e3c872235b47b08b30ef1bd42e4b6ea63f8ce9d4d3a0a3f0c319d2` |
| `markov_family/independent_check.py` | `bb0c8e6bdc0304b82fe104d32dd68bbf4f1e3d5992b957afb59271019a2f10ac` |
| `hidden_state/proof.tex` | `b30f74046317dabb24f0b0022cff7e336dd6218c267a45456d2dfad450f96dd0` |

**Execution and dependencies.** Both exact scripts were inspected before execution: they import only standard-library rational/integer arithmetic and JSON, have bounded loops for these inputs, print JSON, and contain no subprocess or network operations. The copied scripts ran with `/opt/homebrew/opt/python@3.14/bin/python3.14 -I -B`, with assertions enabled, a 120-second wall timeout, a 90-second CPU limit, an 8 MiB regular-file limit, and 64 open descriptors. No hard memory bound was imposed or claimed. The actual platform was macOS 26.4, arm64, Python 3.14.3. The scripts completed in under one second each with zero stderr.

NumPy and mpmath were discoverable in the selected interpreter; SciPy was not. The source's 80-digit Decimal check was run without `--matrix`. Every scalar field matches the archived `independent_check_results.json`. The optional source SciPy branch was not run and no package was installed. A separate standard-library Decimal matrix diagnostic was written and run instead; its evidence remains numerical and uncertified. The exact and independent arithmetic require no NumPy, SciPy, or mpmath.

**Reproduction of this public subset.** Run the release's `verify.py --replay exact` and optional `--replay all` commands from its README. They copy the selected files to a temporary directory before executing them. The original inventory/harness scripts and complete private execution paths are not published. The retained source programs, independent implementations and new release replay receipt cover the selected mathematical values.

**Source arithmetic review.** In `certify_entropy.py`, lines 22–91, `lower_grid` uses integer floor division and `upper_grid=-lower_grid(-x)`, so signs and negative endpoints round in the required directions. Addition, negation, multiplication via all four endpoint products, and reciprocal division on an interval excluding zero are valid interval operations. The reciprocal endpoint order also works for a strictly negative denominator interval. Square roots use integer square roots of the grid-scaled endpoints; taking the integer square root after a floor gives the correct lower integer. The extra unit in the upper endpoint is safe, including at exact squares. It is slightly loose, not a defect.

For a reduced rational input `1 <= r < 2`, `z=(r-1)/(r+1)` lies in `[0,1/3)`. The logarithm identity and tail used in lines 101–134 are

\[
\log r=2\sum_{n=0}^{N-1}\frac{z^{2n+1}}{2n+1}+R_N,
\qquad 0\le R_N\le\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.
\]

The bound follows by replacing every omitted denominator by `2N+1` and summing the geometric progression. The binary range-reduction correction `k log 2` remains valid for negative `k`, since interval multiplication handles its sign. The exact remainder does not need to use the rounded recurrence's `z`: that recurrence already encloses the exact finite partial sum. The separate exact positive tail encloses the omitted true series. The arctangent terms alternate and decrease at `1/5` and `1/239`; the next-term enclosure in lines 137–143 is valid, and Machin's identity gives pi. Exact tail fractions and the resulting source constant intervals are retained in `source_arithmetic_checks.json`.

The additional finite API audit performed 2,032 enclosure checks: 200 rational interval cases including sign changes, reciprocals with either sign, square roots, 107 positive log inputs spanning binary scales and very small/large rationals, formatting, and independent containment checks for pi and log 2. These finite checks supplement the preceding analytic reasoning; they do not prove a general interval library correct. During harness development, an overly strong nesting test for the exact identity `log(1)=0` and an absolute-grid representation of a tiny input were corrected. Neither changed the target calculations or indicated a source error; the final harness records these corrections.

**Independent entropy calculation.** `independent_arithmetic.py` does not import source code. Its rigorous portion uses integer dyadic endpoints with grid `2^-256`, a separate implementation of interval operations, a different pi identity

\[
\pi=4\left(\arctan\frac12+\arctan\frac13\right),
\]

and positive logarithm-series tails. Its log objective is written as differences of logarithms, rather than the source's logarithm of a quotient; its derivative differentiates these split logs directly. It also independently checks the exact rational matrix's stochasticity, positivity, symmetry, and four displayed spectral pairs. Its own arithmetic fixtures make 1,561 exact checks. These are exact integer/rational certificates with elementary analytic series premises, not a proof-assistant verification.

The independent derivative bounds at `A=2.29` and `A=2.30` have signs negative and positive, respectively (approximately `-0.0413833` and `0.695244`). Bisection using rigorously decided derivative signs gives

\[
2.2905478380320088794502388023657123516287
\le A_*\le
2.2905478380320088794502388023657123525918.
\]

The final endpoint derivative intervals are strictly negative and positive, of order `-3.39888e-35` and `3.86418e-35`. The root exceeds the constraint `b-2a` by more than `0.9042534769121182606`. The unconstrained feasible open interval endpoints are approximately `2.0815892093756173965` and `2.7672583136094908117`.

The independent entropy enclosure is

\[
26.1789116783463539085579023985380632587789
\le F_b(A_*)\le
26.1789116783463539085579023985380632908159.
\]

It proves the advertised strict bounds `26.178911678346 < F_b(A_*) < 26.178911678347`. Applying the independent derivative calculation to the source's exact rational root endpoints confirms their signs too. The source's internal entropy interval is contained in

\[
[26.1789116783463444529202003078363338999293,
 26.1789116783463633641956044892589309683621],
\]

strictly inside its printed 12-place endpoints. Therefore outward display rounding does not turn a weak enclosure into an unsupported strict inequality here.

All positive-generator margins are comfortably separated from zero. For `t=2pi/sqrt(7)`, the certified numerators `b-5t`, `2a-b+t`, `b+3t`, and `b+11t` are approximately `0.6025451328417560817`, `0.9885264623275612787`, `19.6011117204213712622`, and `38.5996783080009864428`; dividing the smallest by four gives a lower bound above `0.1506362832104390204` for the witness's smallest off-diagonal entry. At the optimizer, `b-A-s > 0.7282975440583556517` and `b+3A-2s > 0.4326850281977401311`, so logarithms and denominators stay in their proper domains. The principal-log entry is strictly negative, approximately `-0.3465735902799726547`. All detailed conservative endpoints appear in `independent_arithmetic.json`.

**Scalar global-convexity premise.** This was checked analytically instead of inferred from a grid or optimizer. Let

\[
f(z)=z\log\frac{1+z}{1-z},\quad 0<z<1,
\qquad h(c,j)=c f(j/c).
\]

Then `f'(z)=log((1+z)/(1-z))+2z/(1-z^2)>0` and `f''(z)=4/(1-z^2)^2>0`. With `c1=b-A`, `c2=b+3A`, `j1=s(A)`, `j2=2s(A)` and `s(A)=sqrt(2)*sqrt(A^2+omega^2)`, the source objective is exactly

\[
F_b(A)=\tfrac12h(c_1,j_1)+\tfrac18h(c_2,j_2).
\]

For a linear positive `c(A)` and `j(A)>0`, direct differentiation gives

\[
\frac{d^2}{dA^2}h(c,j)
=\frac{f''(j/c)}{c}\left(j'-\frac jc c'\right)^2
  +f'(j/c)j''.
\]

Here both `j1''=s''` and `j2''=2s''` are strictly positive because `omega>0`. Thus each displayed second derivative is strictly positive on the finite-entropy domain `c1>j1>0`, `c2>j2>0`, proving `F_b''>0` there. This validates the scalar unique-minimum premise and the use of signed root isolation. Identifying that scalar minimum with the minimum over every real generator still uses the separate exhaustive-logarithm, feasibility, balancing, and winding reduction arguments. Those are not certified by the execution or treated as an independently completed theorem review here.

**Independent hidden-state constants.** A second exact Fraction calculation, separate from the dyadic engine, isolates the unique positive root `y^64=1/2` on a decimal grid of width `10^-90` using integer polynomial comparisons. It proves `yl^64 < 1/2 < yh^64`. For `alpha=1/64`, `a0=2^-18`, `c=a0/2=2^-19`, the spectral formula gives

\[
m=\frac{2y^8-1-y^{18}}4,
\qquad
C_\alpha=\frac{y^{19}}{c^2}\{\alpha c+4(1-\alpha)\}
=2^{38}y^{19}\left(\frac{2^{-19}}{64}+\frac{63}{16}\right).
\]

The factor `1/4` in the entropy floor is exactly the observed stationary minimum. The code's factorization of `C_alpha` matches the theorem. Also `a0^(2-alpha)=2^-36/y^18`, so the equilibrium-defect formula is correct. All signs and endpoints are propagated monotonically using exact Fractions. The resulting intervals include:

| Quantity | Certified enclosure, shortened outwards |
|---|---|
| `m` | `[0.002782586833090010306926206806344408310912912477002449693270, 0.002782586833090010306926206806344408310912912477002449693271]` |
| `C_alpha` | `[881032897935.831853652574628047170851806951737229514226995836479566433917, 881032897935.831853652574628047170851806951737229514226995836479566433918]` |
| `m/C_alpha` | `[0.000000000000003158323417444820620295732351761117455155963743, 0.000000000000003158323417444820620295732351761117455155963744]` |
| Defect floor | `[0.000000000000049988832366564808166163302737774822539840017857, 0.000000000000049988832366564808166163302737774822539840017858]` |
| Hidden entropy floor, `tau=1` | `[0.000000000000000789580854361205155073933087940279363788990935, 0.000000000000000789580854361205155073933087940279363788990936]` |

In particular, `m/C_alpha < c=1/524288` is rigorously decided, so the active minimum branch is `m/C_alpha`, not `a0/2`. The defect floor is strictly greater than `4.99e-14`; the entropy floor is strictly greater than `7.89e-16` nats per observation interval. These numerical substitutions assume the hidden theorems' stationary homogeneous finite CTMC, deterministic partition, all-even time reversal, and specified exact one-/two-lag data. The compatibility and entropy inequalities themselves were not proved by this numerical audit.

**Numerical diagnostics and comparison.** A separate 120-digit Decimal check computes pi by Gauss–Legendre iteration, optimizes independently, builds the balanced generator in the original basis, evaluates entropy by summing all state pairs, and computes its matrix exponential by Taylor series at `Q/64` followed by six squarings. The scalar/pairwise entropy difference is `1.7e-117`; `max|exp(Q)-P|` is `1.4e-119`, row- and column-sum residuals are `1e-119`, and the minimum optimizer off-diagonal rate is about `0.108171257049435033`. These are uncertified diagnostics: no rounding or truncation proof was attached to that Decimal matrix exponential.

The two exact source JSON outputs are identical to their archived text and have no numerical differences. The archived 80-digit Decimal scalar fields reproduce exactly. The archived optional double-precision matrix fields were not rerun; their reported errors and rate agree at the expected numerical scale with the separate diagnostic. The distinct archived `independent_decimal_check.json` describes a 70-digit computation; its root differs from our 120-digit diagnostic by about `1.30e-57`, well inside the certified root bracket. Its displayed trailing digits are not a certificate. A standalone recipe for regenerating that separate 70-digit record is not identified in the README; the provided current independent-check script uses 80 digits. This is a minor provenance/reproducibility omission, not a contradiction of the exact numerical claims.

The source certificate output does not include its exact rational root endpoints, `m/C_alpha` branch margin, all internal positivity margins, or exact internal entropy interval. They can be recomputed from the source; this audit records the relevant values. The source relies on Python `assert`, so reproductions must keep assertions enabled (as this audit did). The arithmetic proves tested constants and scalar-root statements; it neither machine-checks general convexity nor constructs a formal proof of the universal theorems. The manifest is an internal integrity manifest, not an independent authenticity attestation of the packet's origin.

The original private preservation receipt confirmed identical paths, bytes, hashes, modification times, and file modes for all 26 source files before and after that audit; this release is an explicitly selected subset of it. No source symlinks were present. Access times are not included in that receipt. The final structured outcome, complete source pins, result paths, differences, and dependency limitations are in the original private structured receipt (not part of this selected public subset).
