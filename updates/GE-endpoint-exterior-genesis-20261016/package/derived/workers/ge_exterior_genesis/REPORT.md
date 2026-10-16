# Consequential exterior extension: a certified receiving and sampling operation

The strongest completed extension here is a **direct finite-bit receiver for the complete sorted endpoint of k identical walkers, conditional on no collision**, on weighted paths and cycles. It uses one-particle heat rows and fixed/free-endpoint Pfaffians of order at most 2k. It visits O(k log n) mass queries and never enumerates the binomial endpoint space or rejects a full trajectory until rare survival occurs.

A second operation applies to the **original interchange process on arbitrary graphs**: compute and certify the endpoint order parity of k selected labels, including branching graphs. This is a genuine nonlocal binary endpoint observable, but the underlying exterior/hook sector is classical. It does not give the full correlated labelled/color endpoint distribution.

The receiving composition is reviewable and implemented below. Historical novelty, external correctness, useful physical application and superiority over an equally informed classical heat/Pfaffian incumbent are **UNKNOWN**. The package is an extension of the supplied finite-bit workflow, not a claimed mathematical or technological breakthrough.

## Exact receiving contract

Input: supplied nonnegative state-independent symmetric rates on an ordered path or cycle, k distinct starting sites, a horizon, and one-particle row approximations with certified l1 errors epsilon_i. For the executed integer implementation the horizon is 1. Let

\[
 \delta=\sum_{i=1}^k\epsilon_i,\qquad
 s_0>0\text{ a certified survival lower bound},\qquad
 D=k\lceil\log_2 n\rceil.
\]

The receiving theorem proves:

- Whole living endpoint measure l1 error <= delta, even when approximate minors are signed.
- Whole one-bin endpoint-count coefficient vector l1 error <= delta.
- Direct conditional count sampling TV <= delta/s0 plus bounded-fair-bit rejection error.
- Direct conditional complete sorted-endpoint sampling TV <= `D(delta/s0+2^-A)` for A rejection attempts at each binary decision.

All mass queries must be exact marginals of the same approximate heat-row matrix. Each next endpoint is chosen by binary search, using prefix/suffix masses from a block Pfaffian. Clipping signed child masses is included in the proof; it is not an uncharged numerical repair.

Cycles require the ordinary one-particle kernel for odd k and the antiperiodic kernel for even k. The latter is enclosed through a positive 2n-cycle cover. The sorted endpoint on a cycle does not specify label rotation or winding. Nonnegative site potentials also give joint no-collision/no-death endpoints, or Laplace transforms of integrated total site exposure.

For the original symmetric interchange law on any graph, with ordinary heat K,

\[
 \mathbb E[s_X(\sigma_t)1_{\sigma_t(X)=Y}]=\det K_{X,Y}.
\]

The proof uses the exact rank-one swap identity `I-wedge^k(tau)=dGamma_k(I-tau)`. Summed minors are a Pfaffian, so a one-particle row error delta gives binary order-parity TV error <=delta/2. Two rate arrays r,q satisfy the observable-specific perturbation bound

\[
 \operatorname{TV}(\mathrm{parity}_r,\mathrm{parity}_q)
 \le\tfrac12\sum_{x\in X}\|K_r(x,:)-K_q(x,:)\|_1.
\]

On branching graphs these are signed order observables, not collision probabilities or unsigned bin-count probabilities.

## Executed finite-bit checks

`checks.py` uses only the Python standard library and the original local `sampler.py`. It imports no supplied executable and no acquired executable. Its independent rational uniformization comparison retains the entire Poisson-tail enclosure; floating decimals do not accept a check.

| Exact diagnostic | Passed instances |
|---|---:|
| All-k path/cycle generator identities, including site potentials | 68 |
| Positive antiperiodic-cover intertwiners | 15 |
| Rank-one interchange swap/exterior identities | 322 |
| Count Pfaffian versus explicit minor sums and recursive Pfaffians | 30 |
| Fixed-prefix block Pfaffians versus independent explicit minor sums | 1,149 |
| Bounded integer sampler selectors/fallbacks | 36 |
| Branching exchange loops with k-2 spectators | 5 |
| One-hole Hodge/signless exceptions on branching nonbipartite graphs | 6 |
| Whole conditional endpoint laws versus independent killed-generator enclosures | 4 |
| Exact signed-tree repair law, including negative leaf and bounded fallback | 2 |

Four constant-rate finite-bit inputs were run with `N=2^35`, `Q=2^86`. Every endpoint-count coefficient enclosure was independently checked against a rational killed-generator uniformization enclosure.

| Input | Cover size | Certified survival lower bound | Conditional count TV bound, before fair-bit fallback | Complete sorted endpoint TV bound, including fallback |
|---|---:|---:|---:|---:|
| Six-path, k=3, nonnegative site killing | 6 | >0.1015669858 | <2.751e-8 | <2.497e-7 |
| Five-cycle, k=2, antiperiodic | 10 | >0.4198142736 | <2.496e-9 | <1.638e-8 |
| Six-cycle, k=3, periodic | 6 | >0.1236461404 | <1.272e-8 | <1.165e-7 |
| Six-cycle, k=4, antiperiodic | 12 | >0.0067625260 | <3.099e-7 | <3.722e-6 |

These printed decimals are outward conservative summaries. Exact integer numerators, common denominators, error bounds, input rates, potentials and source hashes are in `checks_receipt.json`.

The four-particle six-cycle receiver was executed for 100 sorted-endpoint samples. All outputs had four distinct ordered sites. The run receipt retains observed decision/query maxima, exact software-random-bit consumption, fallbacks and setup/sample process times; these vary on replay. These observations are diagnostics; the probability theorem assumes independent fair bits. The static heat setup used 60,480 products of at-most-86-bit integer matrix entries, and the declared decision bound is D=12. Small-run process timings are not inference time, scientific performance evidence or an incumbent comparison.

For a branching four-star with rates `(0,1)=1,(0,2)=2,(0,3)=3`, selected labels initially at `(0,1)`, the signed bin-count coefficients for bin `{2,3}` include a value near **-0.2109544551**. This is an explicit diagnostic against a positive collision interpretation. The odd final order probability is about 0.5632483052. Changing the last rate from 3 to 4 gives a certified **binary parity TV bound below 0.011047321** from one-particle rows. A separately constructed exact-rational 24-permutation-state enclosure gives parity TV below 0.004424372. This is a concrete original-generator observable perturbation operation; it is not a bound on its full permutation endpoint law.

## Costs and receiving precision

Let c=n for paths/odd cycles and c=2n for even cycles. With integer rates/potentials and `Lambda=max C_ii`, the exact integer heat receiver proves

\[
 \epsilon=2\Lambda^2/2^m+c2^m/2^p.
\]

For target delta<=eta, choose `2^m>=max(Lambda,4k Lambda^2/eta)` and `2^p>=2kc2^m/eta`. Thus m,p charge rate bit size and log(1/eta). For conditional full endpoint target alpha, take eta proportional to alpha*s0/D and separately budget the fair-bit fallback. There is no hidden iteration proportional to the huge numeric rate or 1/s0; there is also no input-uniform certified s0.

Let A_bit(b) charge b-bit multiplication, exact integer division and linear arithmetic; O(b^2) is a sufficient conservative bound. Using dense schoolbook matrix products, reusable heat powers cost `O(c^3 m A_bit(p))` bit work and `O(c^2 m p)` stored bits. A unit-time-only square, as implemented here, uses only `O(c^2 p)` heat storage. After receiving k rows, suffix skew blocks cost `O(nk^2 A_bit(p))` work and `O(nk^2 p)` bits. Each mass query costs `O(k^3 A_bit(O(kp)))`; a full sorted-endpoint sample uses O(k log n) queries and O(A D k p) worst-case fair bits. Scalar survival is one Pfaffian. A complete one-bin count polynomial uses O(k^3) degree-k polynomial operations, conservatively `O(k^5 A_bit(O(kp)))` bit work with the implemented naive polynomial arithmetic. Exact divisions are charged separately from multiplication, rather than assumed free or automatically as fast as Python multiplication.

The mathematical endpoint space has `binomial(n,k)` states, but that number appears only in separate small diagnostics, never in the receiver's algorithm. A full multivariate endpoint probability table would still have an exponential output cost. This receiver outputs one k-site sample, a binary parity sample, or a short count distribution.

## Prior and importance judgment

Karlin–McGregor directly supplies the k-particle path determinant. De Bruijn and minor summation supply the Pfaffian. Stembridge's Theorems 3.1 and 3.2 directly anticipate free and fixed/free terminal masses. Fulmek and the circle literature anticipate the parity twist. Alon–Kozma's Appendix A explicitly places interchange exterior powers in the classical hook representation sector and credits Bacher. See `PRIOR.md` for primary links and exact prior boundaries.

Therefore the **strongest equally informed incumbent** is the same classical heat/exterior/Pfaffian construction with equally accurate one-particle enclosures, conventional Doob conditioning/sequential mass sampling, and relevant Pfaffian-ensemble samplers (including the directly inspected Edelman–Jeong–Schaub May 2026 preprint). It can implement the same operations at the same asymptotic cost. No distinct information source or physical intervention was invented. The consequential local extension is an exact receiving/sampling interface: whole-vector error k epsilon, consistent signed prefix masses, a direct rare-conditioned sampler, and a narrowly quantified original-interchange parity perturbation certificate. This is useful mathematical/computational capital if the requested output really is one of these observables. It does not defeat its classical structural incumbent or establish a new important scientific capability by itself.

## Unresolved obligations

1. Independent theorem and implementation review, especially the coherent signed-prefix tree error and all bit-growth claims.
2. Historical priority of the exact finite-bit receiving composition and comparison with established Pfaffian-ensemble samplers.
3. A supplied scientific workload with a valuable collision/conditional-position/parity observable and a matched validated-heat incumbent comparison, including setup amortization and output costs.
4. A stronger all-color/full-permutation perturbation result would require new mathematics beyond this exterior sector; the supplied pair Duhamel certificate cannot be upgraded by substituting k survival.
5. General branching collision compression, cycle label/winding outputs, particle-dependent walkers and configuration-dependent physical rates remain outside the proved receiving contract.
6. Removing the tree-depth loss using a polynomial-cost positivity-preserving approximate endpoint measure remains open here.

No installs, outreach, third-party executable runs, git mutations, W mutations, originals mutations or subagents were used. Model token usage and pure inference time are **UNKNOWN**.

The assignment named W pin `adb0a306e9bfdc33b9fbd105efb58baed0cc021e`. A final read-only HEAD query reported `72ca5ee1b0e903df86353bfca896c88ff4cd9092`; these are recorded separately. No scientific content from W entered the derivations, so that observed checkout change does not silently change a proof premise. The actual mathematical source data are the three hashed R/originals reports in `checks_receipt.json`.

## Artifacts and replay

- `PROOF.md`: complete derivations and exact quantifiers.
- `PRIOR.md`: primary-literature confrontation; third-party full texts excluded.
- `FAILED_CONSTRUCTIONS.md`: rejected transfers and exact obstruction boundaries.
- `checks.py`: exact generators, polynomial/blocked Pfaffians, uniformization diagnostics and receipt builder.
- `sampler.py`: bounded integer count selector and full sorted-endpoint binary receiver.
- `receive.py`: full-endpoint replay on a certified finite input.
- `checks_receipt.json`, `full_endpoint_receiver_receipt.json`: exact numerical certificates and process observations.
- `MANIFEST.json`: exact authored/output file hashes and supplied-versus-observed source pins; an integrity receipt, not theorem validation.

From this worker directory, replay with the existing Python installation:

```
python3 checks.py
python3 receive.py --case 3 --samples 100
python3 sampler.py --case 3 --samples 10
```

The certificate rationals and exact checks are deterministic. Sample endpoints, consumed software-random-bit counts and elapsed process times vary on replay. Receipt hashes bind the three actually read original reports; no source bytes were copied into authored publication prose beyond mathematical definitions and short attributed discussion.
