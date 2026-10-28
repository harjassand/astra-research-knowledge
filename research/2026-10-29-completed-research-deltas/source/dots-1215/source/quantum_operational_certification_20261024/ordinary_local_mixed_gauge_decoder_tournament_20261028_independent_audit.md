# Independent audit: local mixed-quantum-gauge acquisition

28 October 2026. Auditor: `producer-workspace/audit_algebra_extraction`.

**Status: mathematical construction received under the explicit structural, reset-source, and paid-control contracts.** Received source SHA-256: `b1102426bfb3af58483e0d84fedde59e9317a6c0bfaac0a9e59a761f4976a9be`. The companion JSON binds this audit and the deterministic checks. This is not a source-count experiment, a hardware result, a membership certificate, or a separation from an equally informed conventional learner. No source sampler was executed during this review; existing pilot files were not changed.

## 1. Scope and received dependencies

The reviewed source is `ordinary_local_mixed_gauge_decoder_tournament_20261028.md`, Sections 1–10. Its source is a fixed memoryless physical family with an exact common logical Pauli algebra supported on one unknown width-at-most-w interval, positive operator-valued quadratic Pauli contrasts, and aggregate relative visibility `Hbar_X,Hbar_Z >= kappa Gbar`. Physical output coordinates and geometry are known. The gauge can be noncommuting, correlated across patches, rank deficient, and arbitrarily ill-conditioned. The exact locality and family promises are not inferred from data.

The already received main hidden-algebra proof supplies the raw-sign perturbation bound, physical extraction isometry, unrestricted-CPTP comparator, and quadratic domination `G(x)<=4Gbar`. The received Bures primitive supplies actual collective estimators at the stated copy cap. The received nonnegative-design proof supplies the ten-feature Bernoulli encoder stage. The 14 bound hashes in the main-theorem receipt and the 17 bound hashes in the active-design receipt were independently reverified unchanged during this review. This audit does not replace their physical contracts by sample oracles.

## 2. Reduction to a true local interval

Write `R_j=U(I/2 tensor Hbar_j)U†`, `rho=U(I/2 tensor Gbar)U†`, and `X_j=B_j R_j`. Then `R_j>=kappa rho`, `R_j<=rho`, and `R_j` commutes with the exact logical reflection `B_j`, even though `Hbar_j` need not commute with `Gbar`. Thus `|X_j|=R_j`.

If `B_j` is supported on `I_*`, partial trace gives `X_j^I=B_j^I Tr_notI R_j`. The positive factor still commutes with `B_j^I`; hence its value is exactly `|X_j^I|`, and the same relative margin survives. The reduced `rho_I` commutes with both exact anticommuting reflections. Their finite-dimensional representation is a qubit tensor a residual factor; `rho_I` is maximally mixed only on this logical qubit, NOT on its arbitrary residual gauge. This proves that the received local sign/extraction lemma applies without a physical-output eigenvalue floor.

For a learned pair of reflections `X',Z'`, let `P=(I+Z')/2`, `Q=I-P`, and `V=[P;X'Q]`. Directly, `V†V=P+Q=I`. Its actual pullbacks are

- `A_Z=Z'`;
- `A_X=P X'Q+Q X'P=(X'-Z'X'Z')/2`;
- `A_Y=i(Q X'P-P X'Q)`.

They are contractions because they are images under a unital completely positive adjoint. No empirical anticommutation is needed or assumed. The imported constants give `delta_j<=56m/kappa²` and `ell0<=154m/kappa²` on the true patch.

## 3. Correlated parallel acquisition is an actual marginal experiment

Intervals whose starts have a common residue modulo w are disjoint. An entire bank consists of independent physical source outputs, not independent patches within one output. On the `N`-copy joint bank, every particular patch has marginal `(r^I)^{tensor N}`. Trace-preserving local instruments on the other disjoint patches leave that marginal experiment unchanged, including when the bank is entangled across patches. Each estimator may adapt to its own records; cross-patch conditioning and conditioning on per-copy anchor labels are excluded. Union bounding its individual marginal guarantees needs no patch independence.

Consequently four fine banks cost `4qN_B`, not `4MN_B`, while invoking `4M` estimators and paying their actual memory and gates. The fine logarithm `log(48*4^w*M/beta_A)` is exactly the received primitive with failure `beta_A/(4M)`. The two coarse banks analogously use `log(24*4^w*M/beta_0)`. Collective across-copy storage and routing are not made free by the one-dimensional source geometry.

## 4. Excess calibration risk: no commuting-gauge shortcut

For a physical decoder let `A_j=D†sigma_j` and `K_j=I-{B_j,A_j}/2`. Since `A_j` is a Hermitian contraction and `B_j` a reflection, `K_j>=0`. Also `Tr rho K_j=1-t_jj`. The actual random-sign binary calibration errors obey

`r(D)=g(D)-g_*=(1/4)sum_{j=X,Z} Tr R_j K_j`.

Pairing the positive `K_j` with `kappa rho<=R_j<=rho` gives the two bounds in (8); no product of two unordered positive operators is declared positive. For the qubit channel `D E0`, Bell/Pauli-twirl positivity gives `1+t_YY-t_XX-t_ZZ>=0`, and `t_YY<=1`. Therefore

`2 ell0 <= (1-t_XX)+(1-t_ZZ) <= 4 ell0`,

and hence `kappa ell0/2 <= r <= ell0`. This holds for every CPTP candidate, including candidates acquired on bad estimation histories. The unknown common calibration floor cancels in differences; it is not supplied or estimated.

## 5. The actual comparison law and its finite implementation

On one fresh ordinary source output choose axis and sign uniformly and measure the real spectrum of `H_(j,s)=s(A_j^b-A_j^a)/2`. Direct averaging over the two actual input states gives

`E Z=r_a-r_b`,

`E Z²=(1/8)sum_j Tr rho(A_j^a-A_j^b)²`.

The contraction inequality `(A-B)²<=2I-{A,B}` and the operator square inequality give

`E Z²<=2(ell0_a+ell0_b)<=4(r_a+r_b)/kappa`.

The outcome distribution matters: replacing this spectrum-valued measurement by a binary `+/-1` POVM with the same mean invalidates the second moment and the fast comparison rate. The source explicitly excludes that replacement.

For overlap, the two patches have one contiguous union of width at most `2w-1`. For disjoint patches their known contractions commute, so two local spectrum measurements on the SAME output and the value `s(b-a)/2` realize the requisite first and second moments. Their actual correlations must be retained; independent outputs or independently resampled marginals do not implement this experiment.

A certified finite observable `C=V diag(c_l)V†`, with rational clipped labels and a known exactly unitary reference circuit, is sufficient. If `||C-H||<=xi` and both are contractions, the bias is at most `xi` and `||C²-H²||<=2xi`. Gate approximation is then charged separately to the entire operational process.

The stated Jacobi construction needs no eigenvalue gap. Let `S=sum_{p!=q}|a_pq|²`. A maximum-pivot exact plane rotation removes `2|a_pq|²>=2S/[d_c(d_c-1)]`; initially `S<=d_c`. Thus `O(d_c² log(d_c/xi))` rotations reduce the Frobenius residual to the target. A finite implementation can stop at the residual threshold. While above threshold, a near-maximum pivot has magnitude at least a constant times `xi/d_c`; computing that two-dimensional rotation requires no division by a vanishing eigenvalue gap. Certified near-maximum pivots, rational-unitary Givens approximations, and smaller accumulated matrix/rounding budgets give the same polynomial precision guarantee. A direct Frobenius upper bound certifies the final operator residual. The task is approximate diagonalization, not stable recovery of individual eigenvectors. This receives a finite known-matrix construction, not free access to an arbitrary exact eigenbasis or exact universal-gate realization of arbitrary angles.

## 6. Finite concentration and tournament constants

Put `R=r_a+r_b`. With `N>=512 L/(kappa t)`, `xi<=kappa t/4096`, the ordinary bounded-variable Bernstein threshold is at most

`(1/8)sqrt(tR) + t/sqrt(524288) + t/384 + t/4096`.

The last three terms are less than `t/96`: even replacing `1/sqrt(524288)` by the larger rational `1/512` preserves the strict inequality. Thus (15), with leading coefficient `1/4`, is conservative. Every batch is fresh, so conditional concentration applies to the adaptive pair identity; union bounding `M-1` comparisons with `L=log(2(M-1)/beta_Q)` is valid.

If the larger risk `m+d` wins, (15) implies

`d <= (1/2)sqrt(2tm)+t/12 <= eta*m+t/(4eta)` for `0<eta<=1`.

On a balanced bracket with height `h`, use `eta=1/(2h)`. The accumulated factor is below 2, and the additive term is at most `t h²`. Hence `r_selected<=2r_min+t h²`. The displayed choices satisfy

`r_min<=154*kappa*epsilon/2^17 < kappa*epsilon/640`,

`r_selected < kappa*epsilon/160`,

`sup_x[ell(D E_x)-ell_star(x)]<=8r_selected/kappa<epsilon/20`.

The single-candidate case correctly omits all `log(M-1)` and zero-height formulas. The encoder stage with `epsilon_q=epsilon/6` yields (22), since its additive Bell loss is `epsilon/4` and `(1+gamma)epsilon/20<=epsilon/10`. Failure and whole-process implementation budgets are charged without postselection.

## 7. Stronger coarse localization and both resulting algorithms

The central cancellation is exact:

`B_Z X_X B_Z=-X_X`.

For any interval `J` disjoint from a true padded interval `I_*`, the conjugating `B_Z` acts only on traced-out qubits. Partial-trace invariance therefore forces `X_X^J=0`, even for correlated or noncommuting gauges. On the true interval, `||X_X^I_*||_1=Tr Hbar_X>=kappa`.

Two coarse Bures estimates per interval at `m0=kappa²/512` give half-difference trace error at most `2sqrt(2m0)=kappa/8`. A trace-norm score certified within `kappa/16` is at least `13kappa/16` on the true interval and at most `3kappa/16` on every disjoint interval. The first score exceeding `kappa/2` must overlap `I_*`. Trace norm is itself approximable without a gap, for example by known-matrix diagonalization with sufficiently small Frobenius residual and rounded absolute diagonal labels. A deterministic fallback on failure preserves physicality and caps.

All width-w intervals overlapping the selected interval form a contiguous list with size at most `R_max=min(M,2w-1)` and contain a true interval on the coarse good event. Fresh fine banks and comparisons justify conditioning on the whole coarse record. Using `R_max` in the cap and confidence parameters handles every realized list. Their entire geometric hull has width at most `3w-2`, even on failure histories, so fine-stage routing does not require an n-distance hidden alignment.

The coarse/fine/tournament route therefore has the source costs (26)–(30), with logarithmic n dependence only in coarse confidence and polynomial-n receiver work explicitly retained. Its fine scaling is `w*4^w/(kappa³ epsilon)` plus `w/(kappa² epsilon)` selection and the encoder stage.

Alternatively expand the certified-overlap interval by `w-1` sites on both sides. The resulting patch contains a true interval and has width at most `W_max=min(n,3w-2)`. One received four-bank learner at `m_exp=kappa² epsilon/32768` gives uniform regret `616m_exp/kappa²<epsilon/20`, with no tournament. The predeclared cap uses the maximum possible width while the deployed decoder can use its smaller realized width. This genuinely competing conventional option trades a larger exponential-in-w patch for the smaller inverse-kappa power and simpler measurements.

## 8. Independent deterministic evidence and limits

`ordinary_local_mixed_gauge_decoder_tournament_20261028_deterministic_check.py` uses only exact prescribed SymPy rational matrices. It has no RNG or source sampler and charges zero source calls. Its four-qubit example has noncommuting, correlated, rank-deficient gauge matrices and a width-two hidden logical algebra. Three explicitly constructed decoders include the ideal one, a deliberately non-anticommuting learned raw pair, and a disjoint gauge decoder. Checks include:

- exact source unitarity, positive-margin triangle certificates, and noncommutation;
- literal extraction isometry and actual X/Z pullbacks;
- normalized-Choi Bell losses computed independently of the diagonal-t formula;
- excess-risk sandwich and all three exact comparison means/second moments;
- exact disjoint-marginal contrast cancellation and true-patch trace norm;
- rational Bernstein, tournament, and coarse-score constants.

All checks passed. They illustrate and guard the algebra but do not replace the general proofs above. There was no sampling, no experiment on the new family, and no claim that small static examples validate arbitrary source behavior.

The received result remains conditional on exact local common algebra, positive contrasts, aggregate visibility, independent source resets, known output coordinates, and a fully budgeted finite receiver. Collective memory and its interconnect can be large. Final decoder synthesis is local to its learned patch; the tournament may require larger union measurements. Neither unrestricted noisy controls, arbitrary approximate locality, automatic visibility for varying gauges, generic unflagged discovery, multiple logical qubits, nor superiority over the equally informed conventional constructions is received.
