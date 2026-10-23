# Targeted primary comparison and a transferable normal-state obstruction

**Contributor:** `/root/quantum_walk_comparison`  
**Checkpoint:** Pro 1 Cycle 3, 22 October 2026  
**Status:** Source-grounded comparison plus independently written operator lemmas. No assertion that the present coherent input is stable or unstable follows from the literature alone.

## 1. Actual owner source and scope

Read the current `work/cycle2/CONTINUATION.md` and the coherent drift/product-stationarity portions of `SUPPLEMENTARY_RESULTS.tex`. The fixed setting is the actual two-seed binary Fock bath, including the root exchange, with `beta=1/512`, `alpha=sqrt(1-beta^2)`, `q=1/2-3 beta^2/32`, `g=beta/8`, and actual initial state `tau_pi`. The task was a bounded comparison with quantum birth-and-death mechanisms, not another audit of the capacity floor.

## 2. Closest primary sources and exact non-transfer

### Bücher, *Invariant states of quantum birth and death chains* (2014)

Original source: <https://arxiv.org/pdf/1408.6162>. The full original PDF was available. Relevant locations are Proposition 6 (printed page 5), Theorem 7 (pages 5–7), and Proposition 9 (pages 10–12). Proposition 6 uses an operator Foster–Lyapunov inequality and compact spectral sublevels. Theorem 7 gives scalar nearest-neighbour existence and nonexistence criteria. Proposition 9 constructs coherence-corrected number observables and controls their bounded truncations, avoiding an assumption of finite number expectation for a hypothetical invariant state. This last proof mechanism transfers abstractly as Lemma A below; its scalar recurrence coefficients do not transfer automatically to the tree.

Retrieval references: `turn92view0`, `turn94view0`, `turn94view1`, `turn94view2`, `turn95view0`, `turn95view1`, `turn95view2`. In particular, `turn95view2` shows the bounded-truncation contradiction. These are subagent refs: the root should open the primary URL itself before citing it in final chat.

### Bücher, Gärtner, Kümmerer, Reußwig, Schwieger and Sissouno, *Ergodic Properties of Quantum Birth and Death Chains* (2013)

Original source: <https://arxiv.org/pdf/1306.3776>. The original PDF was available. Proposition 5.1 classifies pure invariant normal states for their homogeneous one-shift model. Theorem 5.5 gives an exact invariant-state classification for its baby-maser specialization, including coherent incoming two-level states. Thus coherence-sensitive invariant-state questions and exact homogeneous examples are established literature. The channel acts on `B(ell2(N0))` and has a two-level incoming system. Its classification cannot be applied to the present qutrit/tree channel by identifying total up and down probabilities.

Retrieval references: `turn92view1`, `turn93view1`, `turn93view2`, `turn94view3`. The exact model definition and diagonal-algebra discussion are around `turn94view4`; the root should open the original URL before final citation.

### Hypothesis map

| Structure | Scalar birth-and-death papers | Present operation |
|---|---|---|
| Bath | One copy of `ell2(N0)` | `C^2_seed tensor F(C^2)` |
| Routing | One unilateral shift | Two isometries with orthogonal ranges |
| Depth multiplicity | One per level | `2^(ell+1)` per level |
| Incoming port | Two levels | Three levels; both child colors have positive weight |
| Boundary | One vacuum boundary coefficient | A coherent exchange of two vacua |
| Coherent depth law | Requires full operator equations | `f(L)` is not an invariant algebra when `g != 0` |
| Compact finite cutoffs | Finite scalar intervals | Finite vertex-coordinate projections; still finite rank |

The last row permits abstract compactness and operator-Lyapunov arguments to transfer after their inequalities are proved on the actual Fock space. The other rows prevent importing the scalar classification. Enumerating tree vertices by integers does not repair the mismatch: branching edges cannot all become nearest-neighbour edges in one scalar enumeration. Restricting to the all-color-1 ray also does not repair it, because the positive color-2 input population moves mass outside that ray.

## 3. Lemma A: a bounded-truncation test excludes normal invariant states

This is a reusable abstract version of the final contradiction mechanism, with an independent proof. It requires no finite moment of an unbounded observable.

Let `T:B(H)->B(H)` be normal and unital completely positive on a separable Hilbert space. Let `P_m` be increasing finite-rank projections with `P_m -> I` strongly. Suppose there are bounded selfadjoint observables `A_m`, a constant `c>0`, and selfadjoint errors `Z_m` such that

```text
T(A_m)-A_m = c P_m + Z_m,
P_m Z_m P_m = 0,
sup_m ||Z_m|| <= C < infinity.
```

Then `T` has no invariant normal state.

**Proof.** Assume an invariant normal state `omega` exists, and put `Q_m=I-P_m` and `epsilon_m=omega(Q_m)`. Normality implies `epsilon_m -> 0`. Since `P_m Z_m P_m=0`,

```text
Z_m = Q_m Z_m + P_m Z_m Q_m.
```

Cauchy–Schwarz for the positive functional `omega` gives

```text
|omega(Q_m Z_m)| <= C sqrt(epsilon_m),
|omega(P_m Z_m Q_m)| <= C sqrt(epsilon_m).
```

Every `A_m` is bounded, so invariance can legitimately be applied to it, regardless of the growth of `||A_m||`. Hence

```text
0 = c omega(P_m)+omega(Z_m),
c(1-epsilon_m) <= 2 C sqrt(epsilon_m).
```

Taking `m -> infinity` gives the contradiction `c<=0`. This proves the lemma.

The same argument tolerates an additional bounded remainder whose norm tends to zero, or a lower operator inequality with the same off-cutoff error structure. None of these versions permits an unbounded tail error with no independent control.

### Load-bearing counterexample: remove uniform error control and the conclusion fails

Consider the reflected classical nearest-neighbour chain on `N0` with up probability `p`, down probability `q=1-p`, and `0<p<q`; a proposed down step at zero stays at zero. It has the normal invariant law

```text
pi_n = (1-r) r^n,   r=p/q<1.
```

Define increments and a growing potential by

```text
d_n = ((q/p)^n-1)/(q-p),   n>=1,
A(0)=0,  A(n)=sum_(j=1)^n d_j.
```

Then `p d_1=1` and `p d_(n+1)-q d_n=1`. Consequently the formal unbounded drift is `P A-A=1` at every state. This does not contradict positive recurrence because the invariant expectation of `A` is infinite.

Use genuinely bounded truncations `A_m(n)=A(min(n,m))`, and let `P_m` be multiplication by `1_{n<m}`. Direct calculation gives

```text
P A_m-A_m = P_m - q d_m |m><m|.
```

Thus the error is supported outside `P_m`, exactly as in Lemma A, but its norm grows exponentially. In fact,

```text
pi(P_m)=1-r^m,
q d_m pi_m=1-r^m.
```

The outside error cancels the positive drift exactly in the invariant state. This shows why a formal unbounded drift, finite-support identities without tail control, or merely vanishing invariant tail probability cannot replace the uniform error hypothesis. The example can be regarded either as a classical channel or as a normal completely positive quantum channel that measures the position and applies this transition.

## 4. What nonexistence of an invariant normal state would and would not imply

Let `Phi=T_*` be the trace-preserving predual. If one normal orbit `{Phi^n(tau)}` is uniformly tight in finite-rank projections, then `Phi` has a normal invariant state.

**Proof.** Uniform tightness is inherited by the Cesaro averages

```text
sigma_N = (1/N) sum_(n=0)^(N-1) Phi^n(tau).
```

Finite-rank compression and the gentle-projection estimate make this family totally bounded in trace norm; its trace-norm closure consists of positive trace-one trace-class operators. Extract a trace-norm convergent subsequence with limit `sigma`. Trace-norm contractivity and

```text
||Phi(sigma_N)-sigma_N||_1
  = ||Phi^N(tau)-tau||_1/N <= 2/N
```

give `Phi(sigma)=sigma`. No physical initializer is changed in this compactness proof.

Therefore a valid application of Lemma A excludes uniform normal tightness from `tau_pi`, indeed from every normal initializer. It does **not** by itself prove ballistic escape, positive entropy-production rate, failure of sublinear-depth compression, or a capacity converse. The reflected critical symmetric walk already separates these notions: no invariant probability exists, while its finite-horizon depth remains diffusive and sublinear-depth compression can work. The owner's existing exact critical-depth result supplies that comparison without a new audit.

Conversely, an abstract Foster–Lyapunov proof that some invariant normal state exists need not prove convergence of the actual orbit from `tau_pi`, much less justify physically preparing that state without charged operations. A coding consequence needs the owner's additional whole-block, arbitrary-reference estimates.

## 5. Local algebra observation, already reconciled with the owner

During the comparison I independently obtained the exact first-coherence identity, with `S=S1`, `h=alpha beta g`, and `a=(1-q)/2`:

```text
T(S) = (beta^2+alpha^2 a) S
       + alpha^2 q sum_b S_b S S_b*
       + i alpha^2 g R - i alpha beta q S R
       - h(I-SS*).
```

For the diagonal initializer `tau_pi`, its real expectation starts negative. This was sent to the root and agrees with the independently assigned moment and stability calculations. It is only an initial-time sign, not a proof of the long-time sign.

An initially tempting inference was that the bulk coefficients on the right sum to approximately `3/4`, suggesting a uniform coherence gap. The owner correctly rejected iterating that one-observable norm bound: the insertion observables `F_k=sum_(|w|=k) S_w S1 S_w*` generate a hierarchy, and for `k>=1` their diagonal-input evolution has coefficients `q` and `1-q`, not a uniformly killed `3/4` recurrence. This invalidated shortcut is preserved explicitly. The moment helper owns the full hierarchy; this note does not duplicate that construction.

## 6. Focused comparison for the owner's corrected-depth and exponential-tilt route

The owner subsequently reported a provisional bounded coherence correction to depth and is proving an exponential escape bound. This note does not certify that reported calculation from its summary. The following additional primary comparisons were checked specifically for the tilt step.

### Cedzich, Joye, A. H. Werner and R. F. Werner, *Exponential Tail Estimates for Quantum Lattice Dynamics*

Original PDF: <https://arxiv.org/pdf/2408.02108>, dated 4 August 2024. Lemmas 3.1–3.2 and the proof of Theorem 2.1 rigorously conjugate dynamics with exponential position weights, establish a bounded analytic deformation, control exponential moments, and derive spectral-event bounds. Their setting is translation-invariant unitary dynamics on `ell2(Z^d) tensor C^k` with fixed finite site multiplicity. The resulting theorem does not supply the strict outward drift for our rooted Fock CP channel. It is a close primary precedent for exponential conjugation and tail estimation; those generic ideas should not be claimed as new. Retrieval: `turn99view0`, especially `turn100view1` (original proof, pages 6–8).

### Carbone and Pautrat, *Homogeneous Open Quantum Random Walks on a Lattice*

Original PDF: <https://arxiv.org/pdf/1408.1113>. Their lattice OQRWs admit deformed completely positive maps used for position large deviations. The exact channel definition, Eq. (2.1), removes position off-diagonals after one step, as explicitly shown in Eq. (2.4). That is an essential mismatch with the present bath: it retains and generates spatial coherences. The fixed finite-dimensional internal channel and lattice homogeneity are also absent here. Its large-deviation theorem cannot be applied by treating final-bath coherent histories as classical transition probabilities. Retrieval: `turn99view1`, `turn100view0`.

### Novelty boundary and a necessary proof distinction

The credible specific contribution, if the owner's remaining uniform estimate closes, is the explicit bounded correction on the full branching Fock algebra, the treatment of the vacuum-exchange defect, and the resulting seed-specific escape theorem. A new general theory of quantum Lyapunov functions, coherent birth-and-death processes, or exponential tilting is not supported by this search.

Even an established operator drift inequality `T(H)-H >= nu I` must not simply be exponentiated: scalar exponential monotonicity does not give the required noncommutative operator inequality. The additional finite-propagation/finite-band structure must yield a positive tilted weight and an actual uniform second-order remainder estimate. The root is retaining that obligation. This is precisely the extra step that can strengthen mere growth of a mean into a bound on low-depth probability.

The comparison is bounded, mechanism-focused research. It does not establish exhaustive historical priority. An additional repository copy of a quantum Lyapunov paper returned HTTP 403; no theorem from that inaccessible copy was used.

## 7. Outcome and observed costs

The targeted literature changes the appropriate proof standard: normal invariant-state assertions should be established by an actual operator compactness/Lyapunov argument, and nonexistence can be certified with controlled bounded truncations. It does not settle the current tree channel by a ready-made scalar theorem.

Work performed: source reading, two search systems, direct reads of four relevant original arXiv PDFs, exact hypothesis comparison, an independent general bounded-truncation proof, a positive-recurrent counterexample, and the tight-orbit compactness implication. No finite reflecting-bath simulation, hardware-credit job, purchase, outreach, publication, or separate scientific programme was started. No runtime-intensive experiment was required. Tool/model/search wall time, token cost, energy and total discovery cost were not independently metered; no such totals are claimed.

**Receiving use:** if the owner's exact moment or tilted-depth construction produces observables of the form in Lemma A, the normal-state contradiction is available without a finite-depth-moment assumption. Verify the uniform tail-error bound on the entire two-seed Fock bath. For any coding conclusion, separately establish the required finite-horizon information or overflow estimate; nonexistence alone is insufficient.
