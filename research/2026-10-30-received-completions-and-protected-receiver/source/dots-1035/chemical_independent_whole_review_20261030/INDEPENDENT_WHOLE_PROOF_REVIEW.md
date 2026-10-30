# Independent whole-proof review: the explicit chemical Foster construction

Reviewed 2026-10-30 by `producer-workspace/review_chemical_global_foster`.

## Verdict

**PASS, for the one specified fixed-rate network.** The pinned construction proves nonexplosion, positive recurrence of every closed communicating class, and every stationary exponential moment of `A+C+B`. The two noncompact stopping targets are not assumed recurrent, and the controlled first residual is not confused with the unrestricted physical process. The resulting Lyapunov function is an earned, finite stopped-cost construction, not an assumed barrier.

This is a fresh whole-proof review. I read the governing proof and every load-bearing analytic dependency before consulting the earlier end-to-end child audit. I independently regenerated both finite-head certificates by a different exact combinatorial method. The receipt does **not** approve every theorem appearing in the dependency files, the new general summable-fiber lemma, general weakly reversible recurrence, efficiency, or novelty.

**Novelty is separately UNVERIFIED.** The checked primary theorems do not automatically settle this network; trace drift and stopped-cost Poisson propagation are established methodology. See `PRIMARY_PRIOR_SCOPE.md`, whose conclusions are not used to prove correctness here.

## 1. Exact object and evidence

Source bundle: `producer-workspace/chemical_joint_global_candidate_20261030`.
Its `SHA256SUMS.txt` has SHA-256
`14517cd21e1d2be24e9335cd166f5b0ec323ca5b684ef31a9a107eb765f8881e`.
All 24 listed entries verified. A copy is retained as `SOURCE_SHA256SUMS.txt`.
The governing proof has SHA-256
`45f4b3d405214147a608aad4ee6851faf375ba660f56f31584470d6ee307a6be`.

The dependency closure actually used is:

| File under `proofs/` | Used content |
|---|---|
| `FRACTIONAL_FACTORIAL_BULK.md` | finite killed-graph inequality and factorial bulk comparison |
| `PRIMAL_AND_EXACT_CORNER_TRANSFER.md` | its primal bulk paragraph only |
| `EXACT_LOW_PHASE_FORCING_CLOSURE.md` | exact low-B recursion, actual return feedback, endpoint margins |
| `INFINITE_PHASE_FIRST_EXIT_CONTRACTION.md` | controlled r trace, finite head, infinite tail |
| `ROBUST_PHASE_INFINITE_FIBER_LIFT.md` | elementary finite-policy common-resolvent argument only |
| `KILLED_SHELL_FAST_BOUNDARY_SCALE.md` | actual conservative-shell absorption estimate |
| `COMPLEMENTARY_ACTUAL_COMPOSITION_TRACE.md` | actual s trace, finite head, summable infinite tail |
| `JOINT_GLOBAL_FOSTER_CANDIDATE.md` | stopped values and global coupling |

No halo recurrence theorem, growing-shell Green comparison, source-completeness corollary, or general summable-fiber theorem is needed. References in unused paragraphs do not enlarge this approved closure.

The network has coordinates `(A,C,B)`, connector cycle
`0 -> A+B -> 3A+4B -> 0` with all constants 1, and the reversible chain
`3C+4B <-> A+2C+4B <-> 2A+C+4B <-> 3A+4B`, with increasing-A constants `(6,1,7)` and decreasing-A constants `(12,1,1)`. Its aggregate fast rates, after removing `(B)_4`, are

```
b_N(a)=6(C)_3+A(C)_2+7(A)_2 C,
d_N(a)=12A(C)_2+(A)_2 C+(A)_3.
```

There are six complexes, one linkage class, and rank three: `(1,0,1)`, `(2,0,3)`, `(1,-1,0)` are independent. Hence deficiency is two. At positive composition ratio `u=A/C`, the leading conservative drift is proportional to
`6-11u+6u^2-u^3=-(u-1)(u-2)(u-3)`; the two stable composition equilibria are separated by an unstable one. None of the proof assumes this chain mixes rapidly.

## 2. Bulk and the physical low-B function

### 2.1 The small-exponent killed-graph step is valid

For a finite killed generator and `0<alpha<=1/2`, each positive edge term
`z_i^(1-alpha) z_j^alpha-z_i` is at most `2alpha/e`. If nonnegative total energy existed along `alpha_n -> 0`, compactness gives a limiting nonempty positive support. Killing forces every killed vertex out of that support. A path to killing then has an edge from a positive limiting coordinate to a zero limiting coordinate. Its negative contribution divided by `alpha_n` diverges, since

```
(1-exp(-alpha_n L_n))/alpha_n -> infinity,  L_n -> infinity.
```

All positive contributions divided by `alpha_n` remain bounded. This contradiction proves the stated small-alpha interval. Applying it to the finitely many proper complex subsets gives strict, uniform negativity of the full mixed-power energy near the simplex boundary.

The forward factorial ratio has the same mixed-power leading term as the adjoint ratio, with relative error `O(1/min x_i)`. Weighted Young bounds the total error by `C sum_y (x)_y / min x_i`. For this specific network, bulk escape is particularly direct: the zero-complex monomial equals 1, while `sum_y (x)_y -> infinity` along any unbounded sequence with all coordinates above a fixed `K>=3`. Thus its normalized zero-complex coordinate tends to zero. There is no dependence on a sequence of different stoichiometric-class exceptional radii. Fix one sufficiently small rational `alpha<1/2`; this gives

```
L V0 <= -c V0 sum_y (x)_y,     V0=(A! C! B!)^alpha,
```

in the high-coordinate bulk outside one finite set.

### 2.2 Low-B recursion and return feedback are actual, not reflected

For `B<4` only immigration and activation are enabled. They increase B, so first arrival at `B>=4` takes at most four jumps; C is unchanged, A increases by at most eight, and each mean holding time is at most one. The displayed recursion is precisely first-jump conditioning with running cost V0 and terminal data V0. It gives

```
F>=V0,  LF=-V0 at B<4,
F/V0 <= C(1+N)^(8alpha),  N=A+C,
```

after harmless enlargement of constants. In particular the negative low-B margin is at least an inverse-polynomial multiple of F.

Descending substitution gives the stated `f_b` asymptotics. For clearing from B=4, the actual landing value is `F(A-3,C,0)`; its ratio to the source is `1+O(A^-delta)`, where `delta=min(1-alpha,3alpha)>0`. At B=5,6,7 the ratio is `O(A^-alpha)`, and at B>=8 the base factorial function applies at both ends. Hence positive clearing feedback is bounded by
`C (B)_4 [1+A^(3-delta)] F`.

Near A/N=0, fast forward conversion has negative contribution of order `N^3(B)_4 F`; the reverse positive terms are smaller by positive powers of A/C. The symmetric estimate holds near C/N=0. Exact endpoints A=0 or C=0 are included by their enabled one-way channels. Immigration and activation are bounded by `C(B)_4[1+A^(1+2alpha)]F`. Both residual powers are strictly below three. Thus F has the asserted uniform negative margins in both composition endpoint sectors, at every B>=4, for large N.

When B>=`max(8,K_bulk)` and A,C>=K_bulk, F and V0 agree at every reaction target, so the bulk generator inequality transfers exactly. There is no selector commutator.

## 3. Independent exact head certification

The supplied Schur scripts were read, run, and their output matched the supplied JSON byte for byte. Their elimination is mathematically legitimate: off-diagonal Schur rates add positively; self-return paths are discarded; reconstructing the outgoing denominator avoids diagonal-subtraction cancellation. A rate-one source probe produces the desired exit probabilities after transient elimination.

I additionally wrote `recheck_tree_degrees.py`, which does **not** use that elimination. It generates all enabled transitions directly from the actual reaction complexes, appends rate-one returns from the three absorbing labels to each queried start, and applies the positive Markov-chain tree formula. The degree of a tree sum is its maximum integer tree weight. Exact Chu-Liu/Edmonds cycle contraction computes these maxima. The tree implementation was also compared with exhaustive enumeration on 1,000 seeded small graphs and matched every result.

For each start, if `tau_label` denotes its augmented stationary-tree numerator, then
`P(label)=tau_label/(tau_up+tau_down+tau_tail)`; the absorbing states have equal unit residence times. This remains valid when one label is unreachable, in which case its tree sum is zero. The resulting degrees matched **every entry**, including absent exits:

| Head | States | Maximum up degree | Maximum neutral-tail degree |
|---|---:|---:|---:|
| r fixed, B<=12 | 13 | -1 | -2 |
| s fixed, N<=8 | 45 | -1 | -3 |

The independent full output is `INDEPENDENT_TREE_DEGREES.json`. This is a finite exact certificate, not a numerical slope fit or an extrapolation in head width.

For the r head, all positive compact coefficient choices have the same degrees. To cover adapted controls, use `v_pi=(-Q_pi)^-1 b_pi` for each endpoint row policy and maximize the sum of its components. If a replacement row had `Q'v+b'>0` there, then
`v'-v=(-Q')^-1(Q'v+b')>=0`, with at least one strict component, contradicting maximality. This proves a common supersolution for all rows, including their convex combinations; the exit-intensity reward must change with its row. Stopped Dynkin then bounds all adapted policies. Every head is transient because immigration gives a uniformly available escape path.

The governing proof's common time exponent **12** is justified explicitly as follows. In the r head, at most four consecutive immigrations cause a killed exit; total rate is at most `Cr^3` and immigration rate is bounded below. Thus a block of at most four jumps succeeds with probability at least `c r^-12`. Its mean duration is uniformly bounded because total rate is bounded below. Hence mean head stopping time is `O(r^12)`. In the s head, at most three immigrations cause an exit; total rate is `O(s^4)` and immigration rate is one, giving `O(s^12)`. This completes the r dependency's less explicit notation `r^D` without changing any source file or theorem.

## 4. Infinite tails and stopping targets

### 4.1 Controlled r tail

The given h satisfies `2B/3<=h_B<=2B/3+1`. For `r=N-h_B`, activation is neutral, immigration has increment zero or one, and clearing zero or minus one. Beyond B=12 and before immigration, at most three clearings give a down exit or head entry: activation preserves B modulo three and clearing cycles it. Clearing intensity is at least `c r^3(B)_4`, so time to the stopped event has mean `O(r^-3)`. Bounded immigration intensity makes its interruption probability `O(r^-3)`.

This does not conceal explosion. At fixed r, n is determined by B; for the neutral killed process the drift of `1+B` is upper bounded: activation grows as `O((r+B)B)`, while clearing provides a negative term of order `(r+B)^3(B)_4`. A killing clearing only strengthens that estimate. Finite-set localization gives nonexplosion before the stop. Neutral immigration restarts have probability `O(r^-3)`, so their count is geometrically bounded.

With head/tail worst up probabilities H,T,

```
H <= C/r + (C/r^2) T,     T <= C/r^3 + H.
```

For times, the same renewal decomposition has finite head cost `Cr^12`, finite tail cost `Cr^-3`, and a head-to-tail coefficient `Cr^-2<1`. These prove a uniform `C/r` up bound and `Cr^12` mean residual-exit time over all B and controls. They do not assert that the threshold set is compact.

### 4.2 Actual s tail

Let `g_N=4 floor(N/3)+(N mod 3)` and `s=B-g_N`. Fast reactions and clearing are exactly neutral; immigration has increment zero or minus one, activation zero or one. Every enabling condition in the finite certificate matches the actual network.

The killed shell bound can be verified directly from the aggregate rates above. For sufficiently small fixed epsilon,
`b+d<=CN^3` everywhere and `b-d>=cN^3` at `a<=epsilon N`. Put `u=N^(3/4)` and `w(a)=(a+u)^-3`. Taylor's formula gives

```
Q_N w <= -3(b-d)/(a+u)^4 + CN^3/(a+u)^5 - (a)_3/(a+u)^3.
```

At a<=u, the first negative term is bounded away from zero and absorbs its remainder. At u<a<=epsilon N the killing term is bounded away from zero, while the motion-plus-remainder remains negative. At a>=epsilon N the motion is `O(1/N)` and the killing term tends uniformly to one. Thus `Q_N w<=-c`, and finite-chain Dynkin gives `E tau_clear<=C N^-9/4`. All shells N>=3 are connected to a positive killing state, so finitely many small shells can be included by increasing C.

The factor `(B)_4` multiplies both fast motion and clearing. Competing births have intensity at most `1+NB`. A coupling with the pure killed shell therefore gives

```
P(birth before clearing) <= C B^-3 N^-5/4,
E(time until birth or clearing) <= C B^-4 N^-9/4.
```

With no birth, clearings reduce N by three and preserve s, so B>=s. The sums of `n^-5/4` and `n^-9/4` over the descent are finite uniformly in its starting N. Hence a tail attempt is interrupted by a birth with probability `O(s^-3)` and has mean duration `O(s^-4)`. Each birth-free descent has only finitely many finite-shell stages. Neutral-birth restarts are geometrically bounded, excluding hidden infinite activity.

Combining this actual tail with the independently checked head gives

```
H <= C/s + (C/s^3)T,     T <= C/s^3+H,
sup P(up)<=C/s,          sup E tau<=Cs^12.
```

No recurrent distribution, frozen composition, or fast equilibration is used.

## 5. Stopped-cost construction, overshoots, and control

For either residual z, take `phi(z)=exp(kz)(z!)^alpha` above a sufficiently large integer threshold z0 and `Psi(z)=(1+z)^12 phi(z)`. Unit overshoots and the exact factorial ratios imply

```
E[Psi(z_next)]/Psi(z)
 <= C exp(k) z^(alpha-1)(1+O(1/z))
    + exp(-k) z^-alpha(1+O(1/z)) -> 0.
```

Use a factor 1/2 above z0. Iteration for the process killed upon z<=z0 bounds the expected sum of pre-threshold Psi by `2Psi(z_start)`. Its strictly positive minimum above z0 also bounds the expected number of residual excursions. Each excursion was independently proved nonexplosive and of finite mean. Thus finitely many excursions reach the target almost surely, without any compactness or recurrence assumption on that target.

Because phi is constant during a neutral excursion, its conditional mean cost is at most `C Psi(z)`. Therefore the total stopped cost is finite and at most `C Psi(z)`, uniformly over hidden coordinates and controls. This uses an expectation bound on holding time, not an invalid pathwise substitution.

For the actual s process, ordinary first-jump conditioning gives `L W_s=-phi_s`. For controlled r, hold any admissible row until its first jump, then concatenate epsilon-optimal continuation policies at its finitely many targets. Since W_r is the supremum, multiplication of the resulting inequality by the finite total rate and passage epsilon->0 give `L_row W_r<=-phi_r` for **every** admissible row. No optimizer or measurable selector over an uncountable state space is required.

W_r depends only on `(N,B)`. At `A>=epsilon1 N`, the actual activation and clearing coefficients lie in fixed positive intervals for large N; therefore the physical generator inequality holds at that state. Every fast reaction contributes exactly zero, even if its destination leaves the cone. No trajectory-level cone invariance is asserted.

Outside this cone, discard negative connector terms and use target residual at most r+1. When r>r0, `B<=3N/2`, so the actual rates and all factorial shift factors are polynomially bounded in N:
`(L W_r)^+<=C N^D phi_r(r)`. On r<=r0 only immigration from r=r0 can enter the positive domain, so its defect is uniformly bounded.

For W_s, the generator equation is actual at every composition. On s<=s0, only activation from s=s0 can enter the positive domain, giving `(L W_s)^+<=C AB<=CNB`; below that slice the generator is zero. All Gamma expressions are used only above positive thresholds. Values at and below threshold are defined as zero, not by an invalid factorial at a negative argument.

## 6. Global matching covers every cylinder

Choose endpoint width epsilon0, a narrower epsilon1, and
`alpha H(epsilon1)<d1<alpha H(epsilon0)`. Put
`phi_r=exp(-d1r)(r!)^alpha`, and choose any fixed d2>0 for
`phi_s=exp(d2s)(s!)^alpha`.

For large N, the only possibly positive-F region is the balanced cone with `4<=B<B0`, for one fixed B0. There `r=N-O(1)` and, uniformly in composition,

```
log(phi_r/F)=N[alpha H(A/N)-d1]+O(log N).
```

This is uniformly positive linear in N. W_r has negative drift there and dominates every polynomial-F positive contribution.

On the C-dominant side `A<epsilon1 N`, F is negative. To bound the unwanted r-value uniformly in B, split at a small fixed eta N. If B<=eta N, the elementary bounds `r!<=N!`, `binomial(N,A)<=exp(NH(A/N))`, and `r>=N-2eta N/3-1` give

```
phi_r/F <= C exp{N[alpha H(epsilon1)-d1(1-2eta/3)]}.
```

Choose eta so its exponent is negative. If B>=eta N while r>r0, `N-r>=2eta N/3`. The product N!/r! contains a positive linear number of factors comparable with N, so its logarithm is at least `c_eta N log N`. This dominates the at-most-linear binomial entropy. B! only helps. Since B<=3N/2, all rate and value prefactors remain polynomial. Thus the positive r contribution is negligible against the inverse-polynomial-F margin at B<4 and the stronger endpoint margin at B>=4.

Where A>=epsilon1 N and r>r0, the r generator is already nonpositive. Where r<=r0 and N is large, B is proportional to N and bulk/endpoint negativity absorbs its bounded threshold defect. These cases prove negativity of `U=F+W_r` for every sufficiently large N, uniformly in B, with either an inverse-polynomial-F margin or, on the bounded-B bad cone, a fixed fraction of phi_r.

Adding W_s can hurt this large-N inequality only at s=s0. There `B=g_N+s0~4N/3`; bulk or endpoint negativity has a factorial margin and absorbs CNB. This covers all unbounded-N states.

For the remaining bounded-N cylinder and B sufficiently large, r and every successor r lie below r0, so W_r contributes zero. F agrees with V0 at source and targets, with `(LF)^+<=poly(B) F`, uniformly over the finitely many compositions. But

```
phi_s(B-g_N)/F >= c exp(d2 B) B^-D.
```

Thus W_s dominates. The only uncovered set is finite. There is no omitted A-small, C-small, B-small, simultaneous-large, or bounded-N/large-B cylinder, and no closed truncation is substituted for any of them.

## 7. Nonexplosion, recurrence, and moments without integrability circularity

The constructed `V=F+W_r+W_s` is finite at each state, normlike because V>=F, and has finitely many finite-rate outgoing terms. The preceding estimates imply `LV<=-1` off a finite set and hence `LV<=b` globally.

Stop on finite V-sublevel sets. Dynkin yields
`E V(X_{t wedge tau_m})<=V(x)+bt`, so the probability of leaving that sublevel before fixed t tends to zero as its level grows. An explosive path must leave every finite set, since rates are bounded on each finite set. Thus the minimal chain is nonexplosive. Stopping additionally at the finite negative-drift target gives finite expected entrance time and the usual classwise positive recurrence criterion.

For each fixed theta>0, the same V satisfies
`LV<=-exp(theta(N+B))` outside a possibly larger finite set. Indeed a factorial of at least one of A,C,B dominates every exponential of their sum, even after division by a polynomial; the other margins have bounded B or bounded N and factorial residual growth. Absorptions above can be made with a fixed fractional reserve.

For completeness, stationary exponential integrability need not assume `pi(V)<infinity`. Stopped Dynkin bounds the expected integrated exponential cost until entrance into a finite set by V(x). From that finite set, there are only finitely many one-jump destinations, all with finite V, and its own holding costs are finite. Successive finite-set entrance states form a finite irreducible trace chain within any closed class. The expected number of such excursions before returning to a chosen trace state is finite. Thus the full regenerative cycle has finite exponential reward and finite positive mean duration; its stationary occupation formula gives the desired moment. Repeat for every theta using the same V.

Finally, the physical reaction graph is weakly reversible. A realized step `z+y -> z+y'` has an enabled return path `z+y_i` along a complex return path, with the same nonnegative z throughout. Thus physical communicating classes really are closed. This conclusion is not borrowed from a projected graph.

## 8. Failures that remain failures

1. **Unrestricted physical r contraction is false.** At `(A,C,B)=(0,N,3)`, only immigration is enabled. It gives the first residual up exit with probability one. The positive coefficient lower premise cannot be deleted.
2. **F alone is not a global Lyapunov function.** At B=4 and A/C->5/2, exact clearing return cancels its leading sink. With `b=209/4`, `d=415/8`, its leading fast coefficient is
   `(u^alpha-1)[b-d/u^alpha]>0`, since b-d=3/8. This holds for every alpha>0.
3. **Uniform endpoint Green-entry transport is false.** For the unit-rate conservative Ehrenfest A/C chain killed at rate one,
   `G_N(N,0)=2^(-N-1) Beta(1/2,N+1)`, while physical fixed-C insertion gives
   `G_(N+1)(N+1,1)/G_N(N,0)=(N+1)(N+2)/(2N+3)~N/2`.
   Direct binomial transition probabilities and the substitution u=exp(-2t) prove both identities. A fixed spectral gap does not repair this pointwise kernel failure. The new Foster construction does not use that invalid extension.
4. Historical actual-adjoint numerical failures are not reclassified as passes. `ACTUAL_JOINT_CHECKS.json` records 23 positive tests out of 28,476, including the listed endpoint near `(1,79,4)`. Those exploratory results are retained as historical evidence, not rerun or used as this proof's certification.

The additional failure records read from the live continuation tree have hashes:

```
22a4631c9b05511f8af39e24ea5a4c864f6744ab3d3a663490e6c7ebfb372e71  FORCING_VERSUS_KERNEL_ENDPOINT_OBSTRUCTION.md
50c461a0215f44568639ae0ed246b4e8f6ccc892fdce2fe743ad27466cac79c0  NUMERICAL_SCOPE.md
c2d655dcad27fa593f60880c955d65528803e4425075a17eb3568d90868799be  ACTUAL_JOINT_CHECKS.json
```

Their directory is `producer-workspace/chemical_joint_shell_20261030`.

## 9. Separate primary-scope conclusion

The independently sourced comparison in `PRIMARY_PRIOR_SCOPE.md` checks actual hypotheses, including non-binary theorems rather than just binary summaries. In brief:

- [ACKN, arXiv:1808.05328v2](https://arxiv.org/html/1808.05328v2): the ASE bounds couple volume to concentration; recurrence Theorem 7.2 adds pure-species degradation families absent here. Strong endotacticity alone is expressly insufficient.
- [ADE, arXiv:1710.07240v2](https://arxiv.org/pdf/1710.07240v2): Theorem 4.11 is a large-volume estimate on bounded concentration regions, not a fixed-volume global Foster inequality.
- [ACK, arXiv:1904.08967v2](https://arxiv.org/html/1904.08967v2): even its general Theorem 6.1 fails the relevant top-tier inclusion along the reachable sequence `(n,0,0)`, whose only active source is 0 but whose top D-complex is `3A+4B`.
- [Laurence–Robert](https://arxiv.org/html/2310.01949v3) and [Athreya–Kolba–Mattingly](https://arxiv.org/html/1111.1755v2) establish pertinent stopping-time and Poisson-propagation methodology; they do not directly verify this generator.

The exact-result novelty question remains open after this bounded comparison. Correctness and novelty are not conflated. No external publication or experimental chemistry/biology was performed.
