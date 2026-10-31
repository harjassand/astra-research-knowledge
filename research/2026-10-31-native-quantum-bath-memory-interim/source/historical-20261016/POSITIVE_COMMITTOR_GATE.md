# Positive committor route: native boundary-layer obstruction and a local coherent dressing

16 October 2026. Independent operator route for the completed pair generator. **Proof state:** Sections 1--4 are exact finite-volume algebra and geometry, subject to the generator and syndrome-diameter convention pinned in `../../lead/CONTRACTIVE_BOUNDARY_REDUCTION.md` and `../../../2026-10-16-quantum-stability-genesis/lead/PRINCIPAL_PAIR_THEOREM.md`. Section 5 gives a finite-volume semidefinite falsification certificate. The desired fixed-strength, uniform-in-`L` quantum boundary concentration and memory lifetime remain **OPEN**. Nothing here transfers to the original uncompleted pair generator.

## 1. The proposed operator target and its actual implication

Let `k_G` be the syndrome-factor generator of the killed CP compression in the lead reduction, `B=P_boundary` its diagonal boundary projector, and `rho_0=|0><0|` the code-syndrome input. The proposed certificate is a positive operator `F` on the **entire good syndrome Hilbert space** such that, for `gamma>0`, `epsilon>0`,

```
F >= B,
Tr(rho_0 F) <= a_L,
k_G^dagger F <= -gamma F + epsilon I.                 (C)
```

Because `k_G` is trace decreasing, `p(t)=Tr(exp(t k_G)rho_0)<=1`. Gronwall applied to `f(t)=Tr(F exp(t k_G)rho_0)` gives the exact implication

```
q_boundary(t) <= f(t)
  <= exp(-gamma t) a_L + (epsilon/gamma)(1-exp(-gamma t)).  (1)
```

Thus `a_L` and `epsilon/gamma` both need `poly(L) exp(-cL)`; `gamma` may be inverse polynomial. This is a **global operator inequality**, not a pointwise condition only along the code trajectory. A claimed certificate must include the syndrome off-diagonal blocks and the killed exits. The lead's later integrated variant, `k_G^dagger F <= -kappa B + kappa epsilon I` with `F>=0` and small code expectation, is weaker and does not require `F>=B`; Section 3 tests it separately.

## 2. Exact completed-channel action on syndrome coherences

For a pair label `alpha`, write `p_alpha(s)` for its two-check predicate in a syndrome sector. The completed proposal has Kraus operators `Q_alpha P_alpha` and `I-P_alpha`. On a syndrome dyad `|s><s'|`, it acts as follows (up to the syndrome-frame Pauli phase in the both-active case):

```
p(s)=p(s')=0:  |s><s'| is unchanged;
p(s)=p(s')=1:  both labels are face-flipped;
p(s) != p(s'):  the dyad is annihilated.             (2)
```

The code syndrome `0` is inactive for every pair. Every nonzero good syndrome has at least one active pair: lift each component to a contractible box, take a vertex minimizing the sum of its four coordinates, and use even syndrome degree to obtain two outgoing occupied edges. Consequently, for `s != 0` in the good domain, the **Schroedinger-picture** action is

```
k_0(|0><s|) = -kappa n_act(s)|0><s|,
n_act(s) >= 1,                                         (3)
```

where `k_0` is the completed pair generator without `H`; the same outgoing formula holds for the reverse dyad. This is **not** a Heisenberg eigenoperator statement. In fact `k_0^dagger(|0><s|)` can contain incoming dyads: for a pair `alpha` whose two checked bits are zero in `s`, the both-active predecessor dyad `|delta_alpha><s+delta_alpha|` can be face-flipped into `|0><s|`. Equation (3) therefore does not supply a local inverse for dressing `F`. It does **not** bound the entire off-diagonal sector: two nonzero syndromes can share active predicates and their dyads can be transported by correction jumps. An inverse of `k_0^dagger` on all syndrome coherences, with a volume-uniform weighted norm, has not been constructed.

## 3. Native strip obstruction to the *classical diagonal* committor

Choose one primal `Z`-face strip in the `1,2` plane,

```
S_m = product_(x=0,...,m-1) Z_((x,0,0,0);1,2),
s_m = syndrome(S_m).
```

For `1 << m << L`, `s_m` is the single rectangular perimeter of an `m by 1` membrane. It has exactly one active outgoing pair, at its lower-left corner. The corresponding completed pair proposal removes the leftmost face, sending `s_m` to the syndrome of faces `x=1,...,m-1`, at rate `kappa`. Every other pair proposal is inactive. The single face correction never increases any coordinate extent of this strip. These statements follow directly by toggling the four face-boundary edges; they do not use a stochastic threshold theorem.

Use the inherited **ambient torus infinity-diameter** (also stated in the pinned earlier theorem). The occupied vertices of `s_m` span `m` in direction 1 and one in direction 2, so its diameter is exactly `m` for `1<m<L/4`. Set `m=ceil(L/32)-1`; then `s_m` is good and `s_(m+1)` is outside `G`. Take `L` sufficiently large that `m>=3`, and the bounded local Hamiltonian

```
H = h (Z_f_(m-1) + Z_f_m),                            (4)
```

where `f_j` is the face at `x=j`; `0<|h|<kappa/8` is fixed as `L` grows. Put `s_-=s_(m-1)` and `s_+=s_m`. The `f_(m-1)` term couples `s_-` to `s_+` with matrix element of magnitude `|h|`. The `f_m` term extends `s_+` to the bad strip `s_(m+1)`, so `s_+` lies in `B`. At `s_-`, the `f_(m-1)` action remains good, while the `f_m` action creates a separate one-face syndrome across a one-face gap; both components are good for large `L`. Hence `s_-` lies outside `B`. Neither strip has a pair-jump exit.

Consider the **classical pair-only** first-hit committor `c(s)` for reaching `B` before the code, with `c=1` on `B`. Starting from `s_-`, the only active correction repeatedly removes the leftmost face. No future pair-only state can enter `B`, so `c(s_-)=0`. Starting from `s_+`, `c(s_+)=1` by the boundary condition. Its sole correction leads to the shifted shorter strip, from which `B` is likewise inaccessible; therefore, with `Q_0` the diagonal classical pair generator,

```
(Q_0 c)(s_-)=0,       (Q_0 c)(s_+)=-kappa.           (5)
```

If one tries `F=diag(c)` in (C), the principal submatrix of
`M=k_G^dagger F+gamma F-epsilon I` on `s_-,s_+` is, after a harmless basis phase,

```
M|_{-,+} = [ -epsilon           i h ]
            [ -i h       -kappa+gamma-epsilon ].   (6)
```

For `M<=0`, its determinant must be nonnegative. Therefore

```
epsilon (kappa-gamma+epsilon) >= h^2.               (7)
```

For any `0<gamma<kappa` and fixed `h/kappa>0`, this forces a nonvanishing source `epsilon = Omega(h^2/kappa)`, incompatible with the required `poly(L) exp(-cL)`. This is a **rigorous no-go for lifting the classical pair-only committor as a diagonal observable**. It is not a no-go for a different diagonal function with a nonzero Hamiltonian precursor halo, nor for an off-diagonal `F`. The sharp classical zero at `s_-` is precisely what fails.

The lead's **integrated** operator certificate has an even sharper saturation test. Work in units `kappa=1`, set `x=h/kappa`, and consider the classical pair-only occupation potential of `B` on this strip. It has `f(s_-)=0`, `f(s_+)=1` and `Q_0 f(s_-)=0`, `Q_0 f(s_+)=-1`: from `s_+` the unique correction clock holds the process in `B` for mean unit time, then sends it to a strip from which `B` is unreachable. For `F=diag(f)`, the principal submatrix of `k_G^dagger F/kappa+B-epsilon I` is exactly

```
[ -epsilon     i x ]
[ -i x        -epsilon ].                              (9)
```

It is negative semidefinite only if `epsilon >= |h|/kappa`. Thus the **unmodified classical Poisson potential** cannot prove the integrated exponential certificate either. This is not an obstruction to the integrated criterion itself: a quantum candidate may put nonzero potential on `s_-`, overshoot above one at `s_+`, and add coherence. The same strip forces a nontrivial coherent precursor layer in any such construction.

More generally, for any diagonal `F=diag(f)` and any two good syndromes connected by a Hamiltonian matrix element `H_(s,t)`, the `2 by 2` principal-minor condition is

```
|H_(s,t)|^2 |f(t)-f(s)|^2 <= d_s d_t,
d_u = epsilon - gamma f(u) - (Q_0 f)(u) >= 0.       (8)
```

Thus every sharp classical boundary layer must be replaced by enough diagonal drift slack and/or coherent off-diagonal dressing. A classical Doob transform based on `c` does not erase `i[H,c]`; `c` is not a positive eigenoperator of the quantum adjoint. A genuine quantum Doob transform would require a new full-rank positive eigenoperator of the **coherent** killed generator, together with usable locality and condition-number bounds.

## 4. Coherent dressing is possible in an exact native one-face block

The obstruction in Section 3 must not be overread. Fix one face `f` and set `H=h Z_f`, with no other Hamiltonian terms. The subspace `code plus Z_f code` is invariant under this Hamiltonian and every completed pair proposal. The one-face syndrome activates exactly the pair based at `f`'s lower-left vertex; its proposal sends `Z_f code` to `code`. All other proposals act as identity there, including the opposite CSS sector. In the syndrome basis `|0>,|1>=Z_f|0>`, the exact restriction is

```
ell(rho) = -i h [X,rho]
  + kappa (J_1 rho J_1^dagger + J_0 rho J_0^dagger - rho),
J_1=|0><1|, J_0=|0><0|.                          (10)
```

The logical factor is the identity. Notice that a completed proposal damps `|0><1|` at rate `kappa`, not `kappa/2` as a single amplitude-damping jump would.

The exact stationary excited population of (10) is `p_1=2h^2/(kappa^2+4h^2)`. Any certificate `F>=B_1`, `ell^dagger F<=-gamma F+epsilon I` must therefore obey `epsilon>=gamma p_1`, by taking its expectation in the stationary state. At `gamma` proportional to `kappa`, the quadratic `h^2/kappa` source is necessary in this local block.

Put `x=h/kappa`, `|x|<=1/8`, `a=8x^2`, `d=2`, `b=4h(2-a)/(3kappa)`, and

```
F_1 = [ a     i b ]
      [ -i b   2  ].                                  (11)
```

Then `F_1>=|1><1|`: the difference has diagonal `(a,1)` and determinant `a-b^2 >= (8/9)x^2`. Direct substitution into the exact dual of (9) gives, with `gamma=kappa/4` and `epsilon=8h^2/kappa`,

```
ell^dagger(F_1)+gamma F_1-epsilon I
  = diag( -(2+8a)h^2/(3kappa),
          -3kappa/2-2h b ) <= 0.                     (12)
```

The initial expectation is `a=8(h/kappa)^2`. This is a **constructive two-dimensional matrix-cone step**: the off-diagonal entry cancels the commutator, the `F_1>=B_1` overshoot to `2` preserves positivity, and the source has the physically necessary order `h^2/kappa`. It is only a local calibration block. Its target `B_1=|1><1|` is a one-face defect, **not** the macroscopic `P_boundary`; the invariant block never reaches the macroscopic boundary. Extending (11) through interacting, overlapping syndromes and obtaining an exponential code expectation is the unresolved problem.

For the lead's integrated format, divide (12) by `kappa` and use `F_1>=B_1`: `F_int=4F_1` satisfies `(ell^dagger/kappa)F_int <= -B_1+32(h/kappa)^2 I` and `<0|F_int|0>=32(h/kappa)^2`. The quadratic source improves on the linear floor for the undressed classical occupation potential in (9), while remaining a one-face statement only.

## 5. Exact finite-volume SDP obstruction test

For fixed `L,H,gamma,epsilon,a_L`, (C) is a semidefinite feasibility problem. A rigorous *infeasibility witness* is any positive `X,Y` and `z>=0` obeying

```
X = (k_G+gamma Id)(Y) + z rho_0 >= 0,
Tr(B X) > epsilon Tr(Y) + z a_L.                  (13)
```

Indeed, pair `F>=B` with `X`, pair `epsilon I-(k_G^dagger+gamma Id)F>=0` with `Y`, pair `a_L-Tr(rho_0F)>=0` with `z`, and add: the `F` terms cancel while (13) makes the nonnegative sum negative. This is a one-way certificate without any strong-duality assumption.

A transparent special choice is `Y=integral_0^T exp(gamma t) exp(t k_G)rho_0 dt`, `z=1`, giving `X=exp(gamma T)exp(T k_G)rho_0`. It recovers the necessary weighted occupation inequality

```
exp(gamma T) q_boundary(T)
 <= a_L + epsilon integral_0^T exp(gamma t) p(t) dt.  (14)
```

More adversarially, if a normalized positive quasi-stationary state obeys `k_G Y=-delta Y` with `delta<gamma`, then `z=0`, `X=(gamma-delta)Y` proves that any certificate needs

```
epsilon >= (gamma-delta) Tr(BY).                  (15)
```

The known winding dark strips lie **outside** `G`, so they do not instantiate (15). No good-domain quasi-stationary witness with polynomial boundary mass and sub-polynomial decay was found. Equation (13) is a concrete falsification gate for finite reductions or candidate tensor-network ansatzes; it is not an asymptotic theorem.

## 6. What is still needed, resources, and closest prior art

The next viable candidate is an `H`-dependent positive matrix-cone observable that puts a graded halo around `B`: diagonal mass of order `(h/kappa)^{2j}` at `j` coherent face steps from the boundary, off-diagonal terms of order `(h/kappa)^{2j+1}`, and enough overshoot on each inner boundary for `F>=B`. The local block and (8) specify the first grade exactly. A proof must control all overlapping face paths, pair-conditioned transport of two-syndrome coherences, CSS cross terms, killing, and the exponentially many strip/cluster shapes **uniformly in volume**. The classical service-ticket envelope is history dependent and does not directly give an instantaneous operator drift. A global-norm inverse or `exp(theta * syndrome-edge-count)` pays `O(L^4 h)` creation and has no uniform negative edge-count drift because pair corrections may preserve edge count. No global `F` is constructed here.

This route needs no added data-noise floor or matched dissipative bath, and changes no physical generator. It is an analytic certificate over a syndrome Hilbert space of exponential dimension, not an efficient decoder or implementable measurement. The one-face dressing uses only `h/kappa` and one completed pair clock; the hypothetical global certificate would have to account for `12L^4` physical proposal streams, arbitrary bounded local Hamiltonian terms, the exact `G` projector, and both CSS sectors. The resulting memory claim would remain ideal 4D, with inherited preparation/readout and physical-resource gaps.

Closest primary predecessors, checked 16 October 2026:

- [Becker--Datta--Salzmann, *Quantum Zeno Effect in Open Quantum Systems*, arXiv:2010.04121](https://arxiv.org/abs/2010.04121) treats projected open-system semigroups and their Zeno dynamics. The lead's CP compression is standard in this sense; the new unmet issue is its macroscopic boundary occupation under fixed local coherent drift.
- [Anderson--Dodin--Fay--Limmer, *Coherent control from quantum committment probabilities*, arXiv:2403.19533](https://arxiv.org/abs/2403.19533) defines a quantum committor for master equations with absorbing boundaries and studies coherence-sensitive reaction outcomes. The operator-committor concept is therefore prior art; it supplies no Toom-tail theorem for this model.
- [Carollo--Garrahan--Lesanovsky--Pérez-Espigares, *Making rare events typical in Markovian open quantum systems*, arXiv:1711.10951v2](https://arxiv.org/abs/1711.10951) is a primary quantum-Doob predecessor. Its rare-trajectory transformation does not provide a local positive eigenoperator or the boundary estimate for the present killed generator.
- [Han--Zhao--Xu--Wang--Liu, *Coherent error threshold for quantum LDPC codes*, arXiv:2609.20537v1](https://arxiv.org/abs/2609.20537) proves a constant-depth coherent channel threshold using cluster resummation. That result is an incumbent for static coherent recovery, not a continuous autonomous Lindbladian estimate.
- The current lead compression and the pinned pair theorem are local source artifacts, not externally reviewed proof of the new uniform claim. The exact strip and local matrix derivations above are candidate internal results needing independent mathematical review.
