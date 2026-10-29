# Bounded uniformity challenge: literature verdict and one concrete transfer

2026-10-29. Read alongside `producer-workspace/END_TO_END_THEOREM_CANDIDATE.md` and `audit/relative_interface_20261029/POLYNOMIAL_BIT_VERDICT.md`. This is a focused source check and new derivation, not an exhaustive novelty search or a replacement review of that theorem.

## Verdict

**The inspected primary sources do not explicitly imply the precise claimed theorem**: deterministic full-state positive periodic Toda prediction from arbitrary exact rational data in polynomial(N,input bits,time bits,output bits), including closed gaps and without conditioning promises. Calling that entire statement “already known because the mechanism is classical” would overstate the evidence. Conversely, a bounded unsuccessful search is not proof of historical novelty.

The defensible distinction is **a potentially meaningful uniform physical-output complexity transfer of a classical computational mechanism**. The transfer is the quantified, everywhere-physical inverse Abel collar and physical decoder, with data-derived bit bounds and exact degeneration handling. Neither raw-coordinate recognition nor rounded-kernel arithmetic nor repeated doubling should be presented as a new mechanism.

## Strongest sources, actual contracts

1. **Henrici–Kappeler, Global Birkhoff coordinates (2008), Theorem 1.1 and §7.** This constructs a global real-analytic canonical diffeomorphism of positive periodic Toda phase space and makes the Hamiltonian action dependent. It is not an algorithmic bit bound for forward/inverse coordinates or time evaluation. Existence and regularity alone do not bound growing-N conditioning by exp(poly(input size)). [Primary text](https://arxiv.org/pdf/0802.4252).

2. **Bambusi–Maspero (2016), introduction and main result.** Explicitly says the preceding construction is not uniform in chain size. Establishes uniform analytic control on shrinking neighborhoods of equilibrium with radius R/N^alpha, alpha≥2; this is valuable quantitative prior art, but not arbitrary rational positive phase-space data or a global bit-complexity theorem. [Primary text](https://arxiv.org/pdf/1407.4315).

3. **Couveignes (2006), §§3.1–3.3, especially Theorem 2.** This is very close algorithmically: round the evaluation matrix to Q(i), obtain an exact integer kernel vector, normalize by its largest coefficient, and locate section zeros. Fast exponentiation gives polynomial dependence on target logarithmic magnitude. The explicit theorem is for modular curves X0(p), with accuracy measured in Abel coordinates. Thus the rounded-kernel/doubling design is prior art, but this theorem cannot simply be invoked for arbitrary Toda hyperelliptic curves or physical outputs. [Primary text](https://arxiv.org/pdf/math/0606210).

4. **Couveignes–Edixhoven (2012), §§2.2, 3.2–3.3.** Explains the same method and cites book Theorems 12.9.1/12.10.5. Explicitly distinguishes direct accuracy on the Jacobian from closeness of divisor points: special divisors can move without any Abel error. The polynomial theorem again concerns modular curves; controlled local nonspeciality at a selected initial divisor is enough for their direct-accuracy inverse problem. It does not give uniform inverse conditioning at every physical Toda output. [Authors’ primary exposition](https://arxiv.org/pdf/1205.5896). The cited 2011 book chapter was not independently retrieved here; no unseen theorem is being attributed to it.

5. **Bilman–Trogdon (2017), introduction, Eq. (2).** Their no-time-stepping numerical inverse scattering treats a doubly infinite lattice with decaying perturbations of a constant background. Its O(1)-in-(n,t) operation claim is not the finite periodic, growing-genus, rational-bit/output-precision contract. It decisively prevents presenting long-time evaluation without stepping as new in itself. [Primary text](https://arxiv.org/pdf/1508.01788).

6. **Bilman–Nabelek–Trogdon (2023), §§1.2, 2.2, Eq. (53).** Computes genuinely large-genus finite-gap KdV solutions. The authors explicitly state that rigorous error bounds and full numerical analysis are absent. Their gap divisor and trace reconstruction formulas identify a concrete transfer target below. This does not certify arbitrary PDE input spectral acquisition or an infinite-genus truncation error. [Primary text](https://arxiv.org/pdf/2205.00153).

The exact-query searches “Toda bit complexity” and “Toda polynomial time precision” returned no matching explicit theorem (mostly unrelated Toda complexity-class results). This weak negative evidence does not exclude an obscure result, a different terminology, or a direct consequence of literature not inspected.

## Concrete transfer: uniformly conditioned physical reconstruction for finite-gap KdV

**New derivation in this note, not attributed as a new historical result.** Unlike a formal renaming of Toda, the output here is the value of a continuous-space PDE potential; a simple trace decoder replaces Toda's finite-Jacobi weight/Gram reconstruction. We prove one load-bearing step, not an end-to-end KdV fast-forwarding theorem.

Use distinct real branch points E0<...<E_(2g), |E_k|≤M with M≥1 and mutual separation ≥delta, 0<delta≤1. Let

    R(lambda)=product_(k=0)^(2g)(lambda−E_k).

A real nonsingular finite-gap Schrödinger potential has its signed divisor point P_j over the gap [E_(2j−1),E_(2j)], j=1,...,g. This standard spectral representation and the trace formula are the imported facts (source 6, §2.2). Put

    c_j=(E_(2j−1)+E_(2j))/2,
    r_j=(E_(2j)−E_(2j−1))/2,
    mu_j=c_j+r_j cos(theta_j),
    H_j(mu)=product_(k not in {2j−1,2j}) |mu−E_k|.

Use signed sheet coordinate w_j=r_j sin(theta_j) sqrt(H_j(mu_j)), with w²=−R. Multiplying the standard holomorphic forms by a fixed phase gives omega_k=lambda^(k−1) dlambda/w, 1≤k≤g. Cancellation of sin(theta_j), with continuation at endpoints, gives the local Abel differential

    J_(k,j)=−mu_j^(k−1)/sqrt(H_j(mu_j)).

The endpoint limits are nonzero columns: there is no inverse-square-root endpoint singularity in signed-angle coordinates. The Vandermonde identity gives

    |det J| = product_(i<j)|mu_j−mu_i| / product_j sqrt(H_j(mu_j))
            ≥ D := delta^(g(g−1)/2) / (2M)^(g(2g−1)/2) > 0.

Indeed distinct gaps are separated by ≥delta; every remaining branch factor lies between delta and 2M. This proves nonspeciality at **every physical divisor**, not just a selected initial point. Moreover with

    W = M^(g−1) delta^(−(2g−1)/2),
    S = (gW)^(g−1)/D,

we have ||J||_2≤gW and ||J^−1||_2≤S by the product of singular values. All logarithms of these bounds are polynomial in g, log M, log(1/delta).

For an explicit inverse collar, differentiation of each column yields the conservative real derivative bound

    L = g W M ((g−1)+(2g−1)/(2delta)).

This follows from |mu'_j|≤M and |H'_j/H_j|≤(2g−1)/delta. Hence ||J(theta+h)−J(theta)||_2≤L||h||_2 on real angle lifts. Choose

    r=min(1,1/(4SL)),   eta=r/(2S).

The quantitative inverse theorem (or contraction with fixed J(theta)^−1) gives a unique local inverse for every direct Abel displacement of Euclidean norm ≤eta, with angle error ≤2S times direct error. The same r,eta work for every physical theta. No claim is made that arbitrary complex approximate divisors automatically lie on this physical branch: arithmetic must select/project the physical representative and stay inside this collar, exactly the substantive interface issue in the Toda proof.

In the conventional operator L=−d²/dx²+u convention, the trace formula is

    u(x,t)=sum_(k=0)^(2g) E_k − 2 sum_(j=1)^g mu_j(x,t).

(The q used in source 6 has the opposite sign.) Therefore |du/dtheta|_2≤2M sqrt(g). Within the collar, a direct Abel error bounded by epsilon_A in max norm yields

    |u_approx−u| ≤ 4 M g S epsilon_A.

Thus requesting p+ceil(log2(4MgS)) direct bits suffices for p physical-output bits, subject to the collar budget. For rational spectral endpoints of bit size B, both log M and log(1/delta) are polynomial in B. Algebraic endpoints specified by polynomial degree/height also admit standard separation bounds. This is a genuine polynomial-log physical-output bridge on the entire real finite-gap torus, including moving Dirichlet points at gap edges.

**Executed evidence:** `audit/kdv_physical_transfer_check.py` verifies the squared determinant identity and lower bound exactly in 24 rational cases, genera 1–8, including all endpoint configurations used by the fixtures, midpoint divisors, and compressed spectral scales. JSON records each rational determinant and bound. These checks support the formula; the preceding argument proves it. They are not KdV evolution tests.

**What this does not yet buy:** no full KdV theorem is asserted. One must still supply the odd-degree/one-infinity relative-section arithmetic and its norm/root multiplicity bookkeeping; compatible KdV x/t velocities and initialization; exact closed-gap input conventions; and, for a PDE initial-value claim, a polynomial-bit spectral acquisition/truncation theorem. The proved bridge changes the direct-versus-physical-output obstacle in a concrete PDE family, but does not solve those remaining obligations by analogy.

## Disposition

Keep the Toda statement as a candidate uniform-complexity contribution whose precise antecedent was **not found**, not as either a priority-certified discovery or an already-published theorem. Attribute the computational mechanism to classical Jacobian arithmetic, especially Couveignes. The demonstrated transfer is the explicit finite-gap KdV physical inverse/decoder bound above; expanding it to a theorem should proceed only if those additional interfaces are worth proving, not merely to multiply examples.
