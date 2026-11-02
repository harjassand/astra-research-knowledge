# Exact thermal fibers and a sharp no-free-lunch test

Violation-energy convention H=Σ_j J_j(1-S_j)/2. Write B_j=βJ_j and q_j=e^(-B_j).

## Exact disjoint-fiber theorem

This is elementary exact parity summation, closely related to classical decoration transformations; no historical novelty is asserted. Its use here is as a stringent full-temperature certificate, not a new code theorem.

Assume a surjective endpoint chain projection P has each column either zero or a unit coordinate vector. Its nonzero columns partition the fine check coordinates into disjoint nonempty fibers F_a. Assume the full endpoint homotopy, so fine validity is precisely P s'∈S, with S the source allowed-syndrome space. No independence of the **physical allowed syndromes** is assumed.

Sum the unconstrained product weights over each fiber at parity s_a. The even/odd partition sums are

 Z_a(0/1)=(1/2)[∏_(j∈F_a)(1+q_j) ± ∏_(j∈F_a)(1-q_j)].

Therefore the marginal on old syndromes is **exactly**, on every allowed s∈S,

 Pr(s) ∝ 1_(s∈S) exp[-Σ_a B_eff,a s_a],

 tanh(B_eff,a/2)=∏_(j∈F_a)tanh(B_j/2),
 e^(-B_eff,a)=tanh[Σ_(j∈F_a)atanh(q_j)] ≤ Σ_(j∈F_a)q_j.

Zero columns contribute a syndrome-independent partition factor. Redundant source checks are retained through the indicator of S. All auxiliary excited states have been summed; no low-energy truncation or ground projector appears. At uniform B_new and fiber size ≤r, **B_new≥B_old+log r** suffices for B_eff,a≥B_old exactly. The equality choice is B_new=2atanh[(tanh(B_old/2))^(1/r)], asymptotic to B_old+log r at large B_old.

Both endpoint projections must satisfy this fiber property to get this conclusion in both Pauli sectors. A fiber property for only one CSS matrix does not certify a quantum thermal memory. More generally, any separately proved decoder theorem for the exact correlated parity marginal can replace the singleton-column condition, but such a theorem must retain its actual charge and entropy.

## Why generic cone equivalence does not imply the hypothesis

For a three-stratum cone reduction, P0=p0+p0δh0+p0δh0δh0. Internal fine checks in a qubit or opposite-color check cone can project to multiple old checks. Ground-space equivalence gives neither disjoint fibers nor independence of those contributions. Exact auxiliary summation then produces correlated parity noise and typically multispin effective terms. The general exact formula is in THERMAL_CONTRACTION_THEOREM.md.

### Algebraic counterexample

Take one source qubit and r identical X-check generators, r>d_f. Its allowed X syndrome space is {0,1^r}; the single Z error produces 1^r. Suppose a fine code of maximum qubit syndrome degree d_f had a chain-surjective error projection P1 and a singleton-column endpoint projection P_s. For every fine single-qubit error f, P_s D_f f is a valid source syndrome of weight at most d_f, hence must be zero. Thus d_source P1 vanishes on every fine basis vector. Surjectivity of P1 contradicts d_source≠0. The same conclusion holds if surjectivity is provided by a section I1 with P1I1=1.

This example deliberately retains redundant generator energies, as the thermal problem requires. It does not claim the sheaf code contains this exact redundancy block; it refutes a universal inference from code equivalence alone.

### Thermodynamic energy lower bound, independent of auxiliary entropy

For any such chain-surjective reduction (without a singleton-column assumption), some fine single-qubit fault f must map to the nonzero source error. Its fine syndrome τ=D_f f toggles at most d_f fine checks and toggles the coarse source sector. Translation s'→s'+τ bijects the two coarse fibers and changes the physical fine energy by at most d_f J_new (or the sum of the actual affected energies). Therefore

 Z_exc/Z_ground ≥ exp(-β d_f J_new).

The source Hamiltonian with r duplicate checks has Z_exc/Z_ground=exp(-β r J_old). Exact matching, or at least this degree of suppression, requires

 **J_new≥(r/d_f)J_old.**

No auxiliary-state count can evade the bound: the argument is a fiber-by-fiber bijection. Thus a universal logarithmic energy-overhead claim at bounded qubit degree is false absent a restriction on source generator redundancy/energy multiplicity or a different explicitly charged identification of sectors.

## Practical test for the explicit sheaf input

Build both finite endpoint maps in the declared physical bases. Record every column support. If columns are unit/zero, the theorem above gives the logarithmic cold cost. If not, retain their actual multisite patterns; do not replace them by independent singleton defects. The cone theorem itself supplies no certificate that the sheaf input passes this test, and its local incidence inventory has not been compiled here. A sparse-basis or specialized cone construction could still pass, but that is an additional task, not an earned fact.

## General necessary thermal resource inequality

The duplicate example is a special case of a useful implementation diagnostic. Let a fine error f produce τ=D_f f, and let u=P_s τ=d_source(P1f). Translation by τ bijects the fine fibers over s and s+u for every allowed source s. Put E_τ=Σ_(j∈supp τ)J'_j. Regardless of auxiliary dimension or number of excitations,

 exp(-βE_τ) ≤ Z_fiber(s+u)/Z_fiber(s) ≤ exp(βE_τ).

If the claimed coarse marginal is the actual source Gibbs law with energy E_source(s), it is necessary that

 |E_source(s+u)−E_source(s)|≤E_τ for every allowed s;
 in particular E_source(u)≤E_τ at s=0.

Thus every proposed source-error image of a native fine local fault imposes a quantitative energy lower bound. This can be checked **before** compiling or analyzing full cone gadgets. Minimizing the largest source syndrome energy over a bounded-local spanning error map is a meaningful next resource test; minimizing stabilizer support alone is not.

For merely protecting the source logical qubit under a different correlated thermal marginal, this exact-Gibbs necessity need not apply. Then the missing task is a direct decoder/contour theorem for that actual marginal, with its independent entropy and energy accounting. The two routes must not be conflated.
