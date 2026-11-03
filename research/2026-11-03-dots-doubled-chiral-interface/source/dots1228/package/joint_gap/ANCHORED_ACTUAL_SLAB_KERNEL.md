# Explicit local, vector-covariant charged kernels on the actual slab

2026-11-03. This is a new microscopic operation after the conjugate-fiber comparator, not a transfer of that comparator's gap. The operator is defined on the actual free-slab fermions and actual decorated-rotor Majoranas. No inverse decoration, global ground projector, gapped interpolation, or physical reference ancilla is supplied.

## 1. Local relational anchor removes the vector-covariance failure

Consider a rotor update at vertex v, leaving an adjacent anchor a!=v unchanged. Enlarge a bounded patch R to contain both endpoint changed Majorana pairs and their partners, all affected scalar axial-density cells, and the chosen free-slab orbitals. Let Q_V,R be the actual onsite free-slab vector charge in R, with integer spectrum. Decoration Majoranas have zero vector charge. Work in turns phi in R/Z and set

 theta_i=phi_i-phi_a mod1, theta'_i=phi'_i-phi_a mod1.

Given ANY bounded patch coefficient operator T0(theta',theta), define

 T(phi',phi)=R_R(phi_a) T0(theta',theta) R_R(phi_a)^dagger,
 R_R(beta)=exp(2pi i beta Q_V,R).

The seed T0 is a *specified finite-patch computation*, not a pointwise globally optimized map. Its support and coefficient dependence are restricted to the fixed patch.

This formula has four exact properties:
- It is individually periodic in every rotor, since R_R(1)=1.
- Under a common rotor shift alpha, T(phi'+alpha,phi+alpha)=R_R(alpha)T(phi',phi)R_R(alpha)^dagger.
- It depends on no exterior rotor: the unchanged anchor is a local physical rotor already present, not a global reference or extra quantum clock.
- It preserves every seed norm and the corresponding matrix element in the canonically rotated slice. There is no group averaging of complex amplitudes, hence no cancellation penalty from covariance completion itself.

Thus the coherent kernel |phi'><phi| tensor T(phi',phi), plus its Hermitian conjugate, is exactly U(1)V invariant. This is a local chart for the *move kernel*, not a global gauge-fixed wavefunction section; arbitrary loops of moves can still have nontrivial physical holonomy. The construction does not assert flatness or a collective gap.

## 2. A fully specified seed: bounded spectral-polynomial slab mode

The audited barycentric spinor gives U(phi+alpha)=diag(exp(2pi i alpha),exp(-2pi i alpha)) U(phi). The actual four-flavor Wilson slab in the charge-conjugated convention therefore obeys

 h(phi+alpha)=r(alpha) h(phi) r(alpha)^dagger,
 q_V=diag(1,-1,0,0), q_A=1.

Dirichlet restriction to a bounded patch preserves this covariance; it need not preserve the global spectral gap or topology. Let W be a uniform norm bound from onsite/hopping/mass term norms. Define

 p_0(h)=(1-h/W)/2,
 p_{k+1}=3p_k²-2p_k³.

For every Hermitian h with ||h||<=W, 0<=p_k<=1, with no spectral-gap assumption. Its degree is 3^k. Fix a physical orbital e_j in the patch and define

 f_j(phi)=r(phi_a) p_k(h_R(phi-phi_a)) e_j.

Then ||f_j||<=1 and f_j(phi+alpha)=r(alpha) f_j(phi). The slab annihilator c(f_j) has exact axial charge -1. It is a bounded, explicitly computable local operator with the required vector covariance. The opposite axial transfer uses its adjoint. No normalizing by a possibly tiny norm is hidden.

**Stronger exact locality:** If R contains the degree-d hopping neighborhood of seed j, then for any degree-d polynomial p,

 p(h_R)e_j=p(h_full)e_j

on the whole lattice after zero extension. This is the finite-path expansion of h^k: a path of k<=d steps starting at j cannot leave that neighborhood. Thus finite-degree filtering can avoid artificial patch-boundary effects entirely. Rotor dependence is within the corresponding mass-template neighborhoods. The numerical diagnostic below uses a small Dirichlet patch to check exact covariance and exterior independence; it does not claim that this particular patch has the buffer needed for a degree-9 global-filter identity.

If a uniform ACTUAL endpoint gap is later earned, standard polynomial approximation can turn this local filter into an approximate occupied-mode filter. The present operator definition does not assume that gap, and the filter alone is not a complete ground-state transport.

## 3. Actual decoration partial map and exact axial neutrality

Let P_phi and P_phi' be products of the actual local pairing projectors (1+i gamma gamma')/2, in a patch closed under both endpoint pairings. Outside the patch the pairings agree. Define

 D(phi',phi)=P_phi' Gamma P_phi,

where Gamma is a specified local Majorana monomial. It is noninvertible, bounded by one, and annihilates undesired endpoint local excitations. Choose Gamma parity congruent to delta s, the local total change of integer self-linking charge. Since both endpoint pairing-number operators vanish on the projectors,

 Q_dec(phi') D-D Q_dec(phi)=delta s D.

For delta s=+1, take T=D c(f_j); for delta s=-1, use D c(f_j)^dagger. Each total operator is fermion-even and exactly axial-neutral. General finite delta s can use correspondingly charged monomials if sufficient physical modes exist; no uniform rank/amplitude is inferred from that formal option. The stencil for delta s includes every changed cup-product density term, so its value is the actual global change, not an arbitrary fractional cell charge.

These expressions use the actual Kasteleyn-decorated model, not an inverse copy. A bounded integral update over the replacement angle phi'_v with normalized Haar measure has bounded operator norm by the Schur test, since every fiber kernel is bounded by one. The discontinuities at rounding walls are measurable and cause no unbounded rotor-derivative-domain issue.

## 4. Executed actual-model check

`anchored_kernel.py` builds a 2x2x2 local restriction with two slab layers, the actual Wilson gamma/hopping terms, four flavors, and the explicit barycentric SU(2) mass evaluated at refined interior points. There are 256 one-body modes. It uses k=2, hence a degree-9 contractive filter, W=13 (onsite 3, at most eight unit-norm incident hopping terms, boundary mass1.2). It checks both saved self-linking-changing rotor endpoints under several global rotations, wrapping each angle modulo one, and changes all exterior rotors outside the local coarse stencil.

Results:
- h covariance residual <=5.47e-15;
- anchored-mode covariance residual <=2.62e-16;
- changing every exterior rotor changes the mode by exactly 0;
- saved actual eight-Majorana decoration partial map norm .3535533906;
- its charge-plus-one and odd-parity algebra residuals are exactly zero in the finite matrix check.

Files: `anchored_kernel.py`, `anchored_kernel_results.json`. The decoration patch and the cubic free patch are separate retained examples; the script checks their respective operator contracts and does not misidentify them as one geometrically matched interface instance.

## 5. The consequential remaining test

What is now acquired is a microscopic family of bounded-range, exterior-independent, vector-covariant and axial-neutral coherent reconnection terms. The earlier pointwise-optimal patch map had no such coefficient rule; global phase averaging could destroy its amplitude. This compiler avoids those defects.

What is NOT acquired is a lower bound on these terms' matrix elements between the actual free-slab ground sectors, common coherent motion around all rotor loops, or a many-body gap. In the retained full-slab finite rows, the tested scalar self-linking change -1 still has zero free occupied-charge difference. In those regimes any correctly charged operator has exactly zero ground-to-ground amplitude, by charge selection. Changing the local filter or taking a more powerful seed cannot repair a wrong endpoint index. A small finite patch's charge count must not replace that full-slab diagnostic.

The next stronger noninvertible seed, when the actual endpoint index is correct, is a principal-angle Gaussian partial map. If P_a,P_b have occupied ranks differing by one, D=P_a(1-P_b)P_a has an eigenvalue-one crossing subspace. Annihilate the corresponding occupied mode, then rotate the remaining occupied subspace toward P_b. This avoids the determinant suppression of a single guessed annihilator. However, computing a uniform fixed-patch version requires endpoint locality bounds and control of the principal-angle/polar operation; this has not yet been established for the barycentric slab family. The anchored compiler applies to such a seed once acquired, without an additional V-symmetry cost.

No interface gap or improvement over ordinary mirror SMG is claimed. Standard charged rotor dressing, finite spectral polynomials, and Gaussian partial maps are credited as established ingredients; the useful advance here is an explicit compatible local kernel for this microscopic family and an exact account of what it does and does not establish.
