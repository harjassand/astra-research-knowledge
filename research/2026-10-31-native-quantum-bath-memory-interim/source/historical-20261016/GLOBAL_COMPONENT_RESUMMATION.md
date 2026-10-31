# Global coherent resummation: exact component criterion and the missing spacetime shield

16 October 2026, Australia/Brisbane. Independent targeted follow-up. **Status:** the abstract signed-union theorem, joint local-predicate lemma, relative small-component cancellation, no-information obstruction, and occupation dual below are proved under their stated hypotheses. A uniform floor-free theorem for the completed autonomous sweep is **not** proved. The signed route still needs a bounded joint isolated-component map for dynamic Toom/envelope contours; the separate CP-compression route needs an exponentially small positive boundary-occupation certificate. Do not infer that the prior connected-run countermodel rules out either eroder-specific interface; it lacks the sweep's scalar-good cancellation.

## Pinned model and the new algebraic simplification

Take the completed proposal corrector `G_0=kappa sum_v(C_v-Id)` from `ultra/research/2026-10-16-adversarial-quantum-memory/lead/REGULARIZED_ROBUST_MEMORY.md`, remove its depolarizing floor, and add a fixed-range Hamiltonian `H=sum_i h_i` with bounded local strength. Work at finite torus side `L`, finite `T`, and condition on a correction proposal schedule. Classify whole local commutator insertions `E_i=-i[h_i,.]` by the common Pauli-support envelope, before expanding their left/right Pauli branches.

For every insertion pattern whose envelope stays below the pinned macroscopic threshold, the decoded superoperator is scalar `alpha Id_logical` by the inherited Kraus-span/homology argument. Every pattern with at least one intact `E_i` is also trace annihilating, even after the trace-preserving correction channels and final recovery. Hence `alpha=0`. The no-insertion path is exactly `Id_logical` on code inputs. Therefore the exact finite-time logical channel satisfies

```
Lambda_(L,T) = Id_logical + B_(L,T),
||B_(L,T)||_diamond <= 2,                                 (1)
```

where `B` is the signed sum of all escaping insertion patterns, averaged over correction schedules. This sharpens the earlier `||Lambda-Id||<=2||B||` reduction but does not give the exponential `L` estimate.

## 1. A global signed-union theorem that works for arbitrarily long time

Fix any finite, absolutely summable path expansion `Lambda=sum_p F_p` in a Banach space of superoperators. Suppose a deterministic rule attaches to each path a finite set `C(p)` of **distinct maximal large components** drawn from a finite universe `K`. Components simultaneously present are declared compatible. Set

```
B = sum_(p: C(p) nonempty) F_p,
W_J = sum_(p: J subset C(p)) F_p
```

for each nonempty compatible collection `J`. These are signed maps, not probabilities. Assume a positive activity `w(K)` for each possible component satisfies the *joint-component estimate*

```
||W_J||_diamond <= product_(K in J) w(K)                 (JC)
```

for every nonempty compatible `J`. Put `Xi=sum_(K in K) w(K)`.

**Proposition (exact Möbius resummation).** Under (JC),

```
||B||_diamond <= exp(Xi)-1.                               (2)
```

If additionally `Lambda=Id+B` is CPTP, then for **all** `Xi>=0`,

```
||Lambda-Id||_diamond <= min(2,2 Xi).                    (3)
```

**Proof.** For each path with `n=|C(p)|>=1`, the identity `sum_(j=1)^n (-1)^(j+1) binom(n,j)=1` gives the exact finite Möbius expansion

```
B = sum_(compatible J nonempty) (-1)^(|J|+1) W_J.
```

Take norms only **after** each `W_J` has resummed all unconstrained exterior insertions. By (JC), the norm is at most `sum_(J nonempty) product_(K in J)w(K) <= product_K(1+w(K))-1 <= exp(Xi)-1`. CPTP gives `||Lambda-Id||<=2`; for `0<=Xi<=1`, `exp(Xi)-1<2Xi`, and for `Xi>=1`, `2<=2Xi`. QED.

Thus if a *genuine* autonomous component construction gave

```
Xi_(L,T) <= C L^4 (1+kappa*T) exp(-cL),                (4)
```

then (1)--(3) would deliver the target lifetime for every `T>=0`, without assuming `Xi<1` globally. The same conclusion follows from the Han--Zhao--Xu--Wang--Liu component interpolation with a backward Grönwall estimate: if `M(t)=sup_W ||T_W(t)||` and `M(t)<=1+Xi int_t^1 M(s) ds`, then `M(t)<=exp(Xi(1-t))` and the error is at most `exp(Xi)-1`. This extends their small-`Xi` algebra to the storage-time regime; it is **not** a proof of (JC) for the sweep.

The distinction from the inventor's marked-guard estimate is exact. That estimate controls specified separated **bad sinks**; (JC) controls the signed sum in which specified **maximal contours occur as components**, including the absence of joining defects on each contour's boundary and unrestricted errors elsewhere. One cannot replace these component conditions by sink conditions using probability monotonicity. The prior connected-run counterexample shows this abstract shortcut can fail; its role stops there.

### A sufficient local-predicate lemma for the missing joint estimate

There is a useful analytic reduction stronger than simply postulating (JC). Fix compatible components `K_1,...,K_m`. Suppose the assertion that `K_j` occurs is **exactly** a Boolean predicate `f_j(S_j,omega_j)` of a finite set `R_j` of local Hamiltonian term-time blocks and local clock primitives `omega_j`; require the `R_j` to be pairwise disjoint and the clock primitive sets to be independent. No disjointness of the physical Hilbert-space supports is needed. Let `a_(j,U)` be the Boolean Moebius coefficient of `f_j` on `U subset R_j`, and let every block have integrated generator norm at most `eta`. Define

```
g_j(omega_j) = sum_(U subset R_j) |a_(j,U)(omega_j)| eta^|U|,
w(K_j) = E_(omega_j) g_j(omega_j).
```

**Lemma (joint local predicates).** Under these hypotheses, the complete path sum for the simultaneous occurrence of all `K_j`, with every Hamiltonian term outside `union_j R_j` and all correction operations unrestricted, obeys

```
||W_{K_1,...,K_m}||_diamond <= product_(j=1)^m w(K_j).      (LP)
```

**Proof.** At fixed clocks, Moebius inversion of `product_j f_j` on the disjoint Cartesian block sets has coefficient `product_j a_(j,U_j)` for the marked block collection `union_j U_j`. The continuous-time marked-Duhamel bound is `eta^(sum_j |U_j|)` for that collection, regardless of how the unrestricted physical dynamics couples these block supports. Summing absolute coefficients factorizes into `product_j g_j(omega_j)`. Average over clocks; independence of the disjoint primitive sets factorizes the scalar majorant. QED.

If `f_j(S_j,omega_j)=0` below `s_j(omega_j)` occupied blocks, the inventor's local Moebius estimate gives `g_j<=G(|R_j|,s_j,eta)`. Thus *once* a maximal component has a bounded local Boolean predicate, its signed analytic joint estimate is already available, even with time-ordered quantum operations outside. The missing operation is proving this predicate locality for the sweep: maximality and exclusion of connecting descendants may inspect faults far outside `R_j` or earlier in time. A no-hit collar is one way to make the predicate local, but the lemma shows that physical tensor factorization across the collar is more than the norm estimate itself needs. This narrows the open interface without proving its geometry.

## 2. What the closest coherent LDPC predecessor actually supplies

[Han, Zhao, Xu, Wang and Liu, *Coherent error threshold for quantum LDPC codes*, arXiv:2609.20537v1](https://arxiv.org/html/2609.20537) studies a **constant-depth** local error circuit followed by perfect syndrome measurement and recovery. Appendix B.5 defines `T_W(t)=sum_B t^{number of large components} F_B`. Their equation (78) factors the derivative around a connected large component because disjoint error-location components in that identity-baseline circuit have no intervening ideal dynamics and their error maps commute. Appendix B.6 then bounds the resummed complement. Appendix C.3--C.5 treats a fixed minimum-weight decoder: for a specified set of large syndrome-support components, errors outside a component and its check-graph collar are summed in the original circuit order **without requiring commutation**; the syndrome subset map is CP and trace nonincreasing, and a fixed-depth bound controls the number of gate locations touching the component. This is the closest explicit precedent for (JC), not a theorem for continuous autonomous repair.

The fixed-depth collar is the precise transfer obstruction. In the sweep, correction proposals are always present. A Hamiltonian insertion outside a spatial collar may be carried toward the proposed component by a long chain of ideal correction operations, even if no Hamiltonian term acts in that collar. A collar whose width is guaranteed by ordinary worst-case circuit light cones grows with `T`, destroying the required `O(|K|)` local count. The pinned eroder forcing gives a possible *random-schedule shield* against such chains, but no exact component factorization or componentwise CP instrument follows from its support envelope alone.

**Two-qubit check against a fixed interaction graph.** Put a SWAP channel between a weak `X` rotation on qubit 1 and a weak `Z` rotation on qubit 2. The perturbation supports are disjoint as physical gate supports. In the toggling frame, however, SWAP carries the first `X_1` rotation to `X_2`, where it interacts with the later `Z_2` rotation. The mixed fault term is exactly `Delta_2 o Ad(SWAP) o Delta_1`; it does not factor as a product of independent components indexed by the two raw perturbation supports. A graph that includes all intervening ideal gates restores causal edges but, over arbitrary `T`, joins much of spacetime before any rare fault occurs. The sweep needs a finer *activated* influence graph or a certified spacetime shield.

## 3. Relative cancellation of a small isolated component

The following algebra shows why a shield, if constructed, is useful even when another component is already macroscopic.

**Lemma (relative Pauli cancellation).** Let `E_A` be an arbitrary Pauli error chain and `E_B` a Pauli error chain whose entire spacetime evolution, including correction writes, lies in a contractible region `V` of diameter below the decoder's local-fill threshold. Assume `E_A`'s syndrome and physical operations are separated from `V` by more than the local correction/check range throughout `B`'s lifetime. Extend the fixed final decoder by first filling each small syndrome component locally, then applying a deterministic fallback to the residual large syndrome. Suppose the syndrome of `E_B` is a component disjoint from that of `E_A`. Then

```
[E_A+E_B+D(boundary(E_A+E_B))]
    = [E_A+D(boundary(E_A))]                         (5)
```

in logical homology, even if `E_A` is macroscopic. The assertion holds in each CSS sector and hence for joint Pauli labels.

**Proof.** Componentwise filling gives `D(boundary(E_A+E_B))=D(boundary(E_A))+D_B(boundary(E_B))`, with the fallback acting only on the residual syndrome of `A`. The difference of the two sides of (5) is `E_B+D_B(boundary(E_B))`, a closed chain supported in the contractible local region `V` together with its local fill. Such a chain is a stabilizer boundary. QED.

**Corollary (vacuum-bubble cancellation, conditional on circuit separation).** Suppose, in addition, that all complete Hamiltonian commutators and correction proposals inside the isolated tube `V` can be commuted/surgically separated from exterior operations until `V` clears, and that the local tube output has zero syndrome and stabilizer residual for every Pauli branch, **without selecting Kraus outcomes**. Sum all Kraus records of the local correction proposals and keep every Hamiltonian commutator intact. A Dyson term containing at least one insertion in `V`, with arbitrary fixed exterior operations, vanishes after final decoding and summation over the local tube records.

**Proof.** Separation permits the local tube superoperator to be evaluated on a code input before the exterior operations that can overlap its qubits later. Its Pauli branches act as scalar identity on logical states by (5) and the cleared syndrome. The summed local tube superoperator is trace annihilating because it contains an intact commutator and all its other channels are trace preserving. Its scalar must therefore be zero. Operations entirely exterior to the tube may be placed before or after this zero factor by the separation hypothesis. QED.

This is stronger than merely saying a small component is correctable when it is the **only** component. It would remove disconnected small components from a linked expansion even next to an arbitrary bad component. The hypothesis that allows circuit separation is not a free consequence of geometric disjointness at one time; the SWAP example shows why.

## 4. Native correction records cannot be a full-syndrome history

The completed proposal at vertex `v` is `C_v(rho)=sum_O Q_O Pi_O rho Pi_O Q_O^dagger + Pi_0 rho Pi_0`, with `Pi_0=Pi_inactive`. On the inactive subspace `K=ran(Pi_0)`, this channel is exactly the identity. This has a stronger consequence than the absence of a convenient Kraus labeling.

**No-information lemma.** Let `{I_a}` be any CP, trace-nonincreasing instrument whose sum is exactly `C_v`. For any density operator `rho` supported on `K`, there are fixed numbers `p_a>=0`, `sum_a p_a=1`, such that `I_a(rho)=p_a rho`. Thus its outcome law is independent of the state within `K`. In particular, no exact instrument refinement of the pinned `C_v` can report which of two inactive local syndrome patterns occurred.

**Proof.** Restrict the instrument to inputs on `K`. The sum is the identity channel `Id_K` as a map into the full physical output space. Its Choi operator is rank one, namely the projector onto the vectorized inclusion of `K`. Every CP Choi operator `J(I_a|_K)` is positive and their sum is this rank-one operator, so each must be a nonnegative scalar multiple `p_a J(Id_K)`. Choi inversion yields the claim. QED.

There are distinct inactive patterns: the code has no syndrome, while a single-face Pauli error produces a boundary whose vertices with incoming incident syndrome edges are inactive for the sweep rule. More strongly, the two winding syndrome loops in `workers/quantum_zeno/DARK_STRIP_OBSTRUCTION.md` are inactive at **every** pair-rule vertex. The code--dark-strip operator algebra is fixed by all completed proposals. At `H=0`, therefore, even the entire native proposal clock and outcome record over arbitrary `T` cannot distinguish a code state from a dark-strip state. This is an exact obstruction to treating a positive *full syndrome history* as an unraveling of the existing generator. Splitting `Pi_0` into individual inactive-pattern projectors or adding stabilizer monitors supplies new information but changes the channel on cross-syndrome coherences; any memory theorem for that architecture needs its own transfer proof. This observation does not rule out a different eroder-specific signed resummation for the pinned channel.

The impossibility applies even to a hypothetical instrument for the **whole** ideal semigroup, rather than just the displayed proposal Kraus operators: restricted to the global code-plus-dark-strip subspace, that semigroup is the identity for every `T`, and the same rank-one Choi argument makes every outcome state-independent there. A full-syndrome monitor that separates the two sectors is therefore an additional physical operation, not a hidden record of the pinned dynamics.

The information loss is not confined to macroscopic dark sectors. In one coordinate plane, let `E_1` be one Z face and `E_2` the two adjacent Z faces of a `2 by 1` rectangle, with the same lower-left vertex `v`. Their distinct contractible X-edge syndromes have the same **sole** active sweep pattern: the two outgoing edges at `v`. Along the rest of either rectangular loop, every occupied vertex has an incoming edge and is inactive. For a sufficiently large torus both component diameters are below the safe threshold, yet the first completed proposal at any `u` has the same active/inactive outcome on `E_1 C` and `E_2 C`; at `v` it applies the same Pauli correction to each. Later records can distinguish the resulting syndromes, so this example establishes only the absence of an instantaneous full-syndrome readout in the safe sector, not permanent indistinguishability. The dark-strip pair establishes the latter at `H=0`.

A direct `F_2` boundary check at `L=16` gave the sole active record `((0,0,0,0),(0,1))` for each rectangle. This finite check illustrates the elementary boundary argument; the latter proves the statement for every sufficiently large `L` without relying on the check.

## 5. Exact interface still needed for the 4D sweep

A viable next construction is a **certified spacetime hull** for each maximal zero/envelope component. Its boundary would contain a thick layer of target/slab sites that are healthy throughout the slab and have *good primitive guards*: the local clock certificate succeeds, no fast dependency chain occurs, and no Hamiltonian insertion hits the enlarged guard. On a fixed such hull, no-hit Hamiltonian constraints simply remove selected local terms, leaving the unrestricted exterior evolution CPTP. The pinned good-flag forcing is uniform over exterior histories, so it is a plausible ingredient for a shield. A componentwise decoder as in Section 3 would make a small isolated hull algebraically removable.

Three exact statements remain unproved and must not be silently replaced by classical probability estimates:

1. **Coverage with bounded complexity.** Every escaping common-envelope history must admit a deterministic family of maximal certified hulls. Their possible rooted shapes must be countable with exponential cost in a number of disjoint marked primitive regions proportional to their diameter. A maximal zero component need not already have an all-good boundary: a boundary cell can be healthy despite a bad clock flag or a cancelling Hamiltonian insertion. Enlarging the hull until its boundary is certified might produce a much larger, branching object; the existing Toom contour theorem controls zero-component diameter, not this new hull's joint marked complexity.
2. **Exact surgical identity.** For a specified compatible collection of hulls, partition all Dyson paths exactly into inner marked terms, a no-hit/good-clock collar, and an unrestricted exterior, while preserving the original correction order and the fixed decoder. The no-hit collar must shield quantum interference as well as classical syndrome support. This is the autonomous replacement for Appendix C.4's fixed-depth buffer identity, not established by the current forcing lemma.
3. **Joint bound.** Prove (JC) for those specified maximal hulls with activities summing as in (4). The inventor's separated-sink bound is a candidate estimate *inside* this proof, but it does not handle maximality, overlapping collars, or unrestricted exterior histories by itself.

The independent transfer-adversary construction in `workers/transfer_adversary/GOOD_DOMAIN_AND_COLLAR_AUDIT.md` makes item 1 sharper: for the native coarse eroder recurrence, a singleton zero component at late time can be joined by an earlier zero cube inserted arbitrarily far back while all primitive flags in any fixed collar of that singleton stay unchanged. Thus maximal zero-component membership is not a fixed-collar Boolean predicate of the recurrence alone. That freely assigned flag history does not prove a no-go for an eroder-specific certified hull using the actual physical flag process; it shows the hull must include ancestry or an additional shield certificate.

If these steps succeed, Proposition 1 provides the global signed union for all `L,T` and the exact cancellation (1) turns it into the logical diamond bound. If any step fails, retain the failed hull or surgery example; it identifies whether the obstacle is geometric coverage, quantum factorization, or contour counting. No floor-free threshold, physical implementation, or historical novelty is asserted here.

## 6. Alternative positive boundary-occupation certificate for the compressed route

The root campaign is also testing a safe-syndrome compression. The following finite-dimensional criterion makes its remaining concentration step precise without asking for a pointwise-in-time bound. Let `Psi_t=exp(t A)` be a CP trace-nonincreasing semigroup on the safe subspace `P`, with `tau_t=Psi_t(tau_0)` and `tr(tau_0)=1`. For a positive boundary cost `Q`, suppose there is an operator `F>=0` and `epsilon>=0` such that

```
A^*(F) <= -Q + epsilon P,
tr(F tau_0) <= epsilon.                              (OC)
```

**Lemma (occupation dual).** Then, uniformly for every `T>=0`,

```
integral_0^T tr(Q tau_t) dt <= epsilon(1+T).       (6)
```

**Proof.** Differentiate `tr(F tau_t)`, apply (OC), and use `tr(tau_t)<=1`. Integrating gives `int tr(Q tau_t) <= tr(F tau_0)-tr(F tau_T)+epsilon int tr(tau_t) <=epsilon(1+T)`. QED.

If the proposed compressed-channel comparison has instantaneous integrand `2 sqrt(chi_t)+2 sqrt(R lambda_t)+2 lambda_t`, where `chi_t=tr(Q_H tau_t)`, `lambda_t=tr(Q_J tau_t)`, and `R=O(kappa L^4)`, two certificates (OC) with errors `epsilon_H,epsilon_J` give, by Cauchy--Schwarz and `sqrt(T(1+T))<=1+T`, the conditional all-time estimate

```
error(T) <= (1+T)[2 sqrt(epsilon_H)
                     + 2 sqrt(R epsilon_J) + 2 epsilon_J]. (7)
```

Exponential `epsilon_H,epsilon_J` with polynomial prefactors would suffice, even though no uniform bound on `tr(Q tau_t)` was proved. The assertion that such `F` exist for the sweep is wholly open. An exact construction would be a **positive quantum contour committor**, or a supersolution of the adjoint compressed generator, with exponentially small expectation on code inputs.

**One positive pivotal projector suffices.** The independent transfer-adversary note `workers/transfer_adversary/GOOD_DOMAIN_AND_COLLAR_AUDIT.md` already identified this boundary projector and the corresponding norm reduction; it is restated here to connect (OC) to the additional geometric lemma below. Let `Q_out=I-P` and let `P_piv` be the sum of safe syndrome sectors from which at least one local Hamiltonian term or ideal correction Kraus operator has nonzero amplitude to `Q_out`. Then `Q_out H P=Q_out H P_piv` and `Q_out J_a P=Q_out J_a P_piv` for every local jump. Consequently

```
P H Q_out H P <= ||H||^2 P_piv,
sum_a P J_a^dagger Q_out J_a P <= R P_piv,
R := sum_a ||J_a||^2 = O(kappa L^4).                 (8)
```

The first inequality is the positive operator bound on `(Q_out H P_piv)^dagger(Q_out H P_piv)`; the second follows termwise. Thus (OC) for `Q=P_piv` implies (OC) for both boundary costs with polynomial factors, and a single positive occupation estimate is the real target. `P_piv` must include local merges of multiple safe syndrome components.

**Geometric pivotal lemma.** Suppose one local Pauli error or correction changes syndrome only in a spatial patch `U` of diameter at most `D`, and the component adjacency range is one. If a configuration with every component diameter `<r` becomes one with a component diameter `>=r`, then before that event it had a component of diameter at least `(r-D-2)/2`. Indeed the new large component intersects `U`. Every point in it is either in `U` or in an old component touching the one-neighborhood of `U`. For two extremal points in old components `C_i,C_j`, choose their nearest points to `U`; the distance between extremes is at most `diam(C_i)+D+2+diam(C_j)`. The same bound covers points inside `U`. Hence `r<=2 max_i diam(C_i)+D+2`. This proof allows any bounded number of components to merge. It yields the operator inclusion `P_piv <= P_{diam>=(r-D-2)/2}` (with integer rounding). For fixed-range terms and `r=Theta(L)`, pivotal occupation is bounded by occupation of a macroscopic but still safe component. The existing classical Toom tail establishes that estimate for a positive classical fault process; its quantum compressed analogue remains open.

The classical diagonal committor cannot simply be imported as an operator inequality. On two safe syndrome sectors `|s>,|t>` with `F=diag(f_s,f_t)` and Hamiltonian matrix element `h=<s|H|t>`, the off-diagonal block of `i[H,F]` has magnitude `|h(f_s-f_t)|`. Even if the classical correction drift has diagonal entries `0,-a` with `a>0`, the matrix `[[0,c],[conj(c),-a]]` has positive eigenvalue `(sqrt(a^2+4|c|^2)-a)/2>0` whenever `c!=0`. Thus a diagonal classical superharmonic function with zero source at the code sector does not satisfy the quantum operator order condition. A coherent off-diagonal dressing, an explicit positive source term, or a different occupation certificate is required. This 2-by-2 calculation is an obstruction to the *naive committor transfer*, not to (OC) or to the compressed route itself.
