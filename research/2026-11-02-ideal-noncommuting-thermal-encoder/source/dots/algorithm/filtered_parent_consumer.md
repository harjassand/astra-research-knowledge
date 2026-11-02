# Filtered-subspace parent: constructive consumer calculation

2026-11-01. Gap theorem is a separately reviewed input. This is the parent-construction/algorithm/logical-transport component. In computational/global norm bounds below, n denotes total accessible spin count N=n_memory+N_bath, not memory size alone.

## 1. Exact algebra

Let H=Href+V, with Href a bounded-degree commuting bounded-support stabilizer Hamiltonian plus a bounded-dimensional product-bath Hamiltonian. Fix a valid memory syndrome sigma and an explicit bath eigenbasis label b. Let Q_a be its signed-check violation projectors and onsite bath-complement projectors. They commute with Href and each other. Their common kernel P has the supplied logical dimension d_L (two for one logical qubit).

A(s)=exp(-sH/2), L_a(s)=A(s)Q_a A(s)^-1,
F(s)=sum_a L_a(s)†L_a(s), 0<=s<=beta.

F is positive and its kernel is EXACTLY A(s)ran(P): L_a psi=0 for all a iff A^-1 psi lies in every Q_a kernel. At V=0, L_a=Q_a and F=F0=sum_a Q_a; its nonzero spectrum is bounded below by1. This statement alone says nothing about the perturbed gap.

The logical kernel dimension remains exactly d_L for every finite n,s, even if a gap closes. There is no normalization/postselection in this algebra.

## 2. Commuting-reference imaginary-time expansion

For an operator O supported on a fixed set X, exp(tHref)O exp(-tHref) involves only Href terms touching X. Every other term commutes with O and with these reference terms and cancels from the conjugation. Hence it is supported on one bounded reference star of X, and its norm is at most exp(C|t|J|X|)||O||, with constants from local dimension, support size and degree.

Set U(s)=exp(sHref/2)exp(-sH/2). Then

U'=-(1/2)V_I(s)U, V_I(s)=exp(sHref/2)V exp(-sHref/2),
L_a=exp(-sHref/2)[U Q_a U^-1]exp(sHref/2).

Each V_I term has constant support on an enlarged bounded-degree interaction graph and strength at most v exp(C beta J), uniformly over0<=s<=beta. The conjugation U Q U^-1 has its time-ordered nested-commutator expansion. Only terms connected to Q survive.

An explicit majorant is obtained as follows. If the initial support has size r0 and each enlarged interaction adds at most r* sites, then summing the norms of choices at commutator step j contributes at most2v_I(r0+j r*). The time-ordered simplex contributes (beta/2)^k/k!. Therefore the total k-th-order absolute contribution is bounded by

C k^c (C beta v_I)^k.

The final Href conjugation multiplies the norm by at most exp(C beta J(r0+k r*)) and enlarges the support by only a fixed star. Consequently there are constants C,c,c0, independent of n,sigma,b, such that

sum_{order k} ||L_a,[k]|| <= C k^c q^k,
q=C beta v exp(C beta J),
|support(L_a,[k])| <= c0(k+1).

Choose v so that q times the desired support-weight factor is strictly below1. Re-rooting connected clusters bounds the sum incident on any site with the same geometric convergence (additional polynomial factors in k are harmless). Thus L_a-Q_a and F-F0 admit exponentially decaying connected-interaction decompositions with perturbation interaction norm O(q). Products in F are unions of two clusters sharing the same root a, hence still connected and of additive size. Constants and derivative bounds are uniform in sigma,b, because the signs/basis labels do not change projector norms or supports.

This is an interaction norm, NOT the extensive operator norm ||F-F0||=O(nq). It is the appropriate consumer input for a local gap-stability theorem, if the root's host-geometry and code-hypothesis audit actually supplies one.

## 3. Uniformity over syndrome sectors

For every valid sigma, a matched representative E_D(sigma) is a tensor product of physical Pauli operators. It conjugates the unsigned stabilizer parent to the signed parent. Its support can be extensive, but its conjugation does not enlarge any operator support or change its norm. Similarly the bath eigenbasis labels differ by onsite basis changes. Therefore a gap-stability theorem applicable to the unsigned code parent plus product ancillas, and uniform over arbitrary small local perturbations, transfers to every sampled signed parent with identical locality/norm constants. No separate gap proof for exponentially many syndromes is needed. This does not repair a missing hypothesis for the unsigned parent.

## 4. Polynomial classical representation: avoid ordered-history enumeration

Naively enumerating all ordered commutator histories costs k! and would be an unnecessary quasipolynomial overhead at k~log n. Instead group by ROOT-CONNECTED sets C of distinct perturbation terms: C union {Q_a} must be connected in the enlarged interaction graph. C alone may have several branches meeting Q_a. For such a set C, define its linked coefficient by inclusion-exclusion over T subset C of the exact local conjugation with perturbations in T. Use the commuting-reference star of C together with the root Q_a; it contains O(|C|) physical spins. Coefficients vanish when C union {Q_a} is disconnected. The linked coefficient sums all repetitions/orderings automatically.

The local matrix exponentials and the 2^|C| inclusion-exclusion sum cost exp(O(|C|)) at fixed dimension. Their condition/absolute-precision costs are also exp(O(beta|C|)), hence polynomial when |C|=O(log(n/eta)). The connected-set count on a bounded-degree graph is n exp(O(|C|)). The above absolutely convergent expansion bounds the omitted sets by n poly(K) q^K. Choose K=C log(n/eta).

This produces an explicit polynomial-size list of O(log(n/eta))-spin operators approximating every L_a and hence F in global norm eta. Expand products termwise: never construct one dense matrix on the whole log-radius collar (which might contain log^3 n spins). Each pairwise union still has O(K) spins, and the number of pairs remains polynomial. This is a concrete charged representation rather than an arbitrary collar-channel oracle. The exact linked-cluster implementation should be audited for its chosen graph/star conventions, but the ordering-factorial obstacle is avoided explicitly.

## 5. Algorithm conditional on the separate uniform gap result

If the exact path F(s) has gap g>=1/poly(n) above its d_L-dimensional zero band, with polynomial derivative bounds, ordinary degenerate adiabatic evolution prepares parallel transport of the supplied signed-syndrome encoded state in polynomial time. The connected interaction bounds give global first/second derivatives O(n) times fixed physical constants. Standard Hamiltonian simulation of the explicit polynomial list has polynomial cost. Choose the parent truncation/synthesis accuracy eta small enough that eta times the adiabatic runtime is below the output-error budget; this also controls any spurious dynamical splitting of the logical band introduced by truncation.

At the start, sample sigma,b by the separately earned target-weight sampler, apply the matched Pauli representative to the supplied encoded input, and prepare the accessible bath basis state b. All randomness, bath accessibility, pure ancillas, control precision and Hamiltonian-engineering/simulation resources must be supplied and charged. The procedure has no global success event and no exponentially small normalization probability. If the bath is inaccessible, the joint-state version cannot be implemented.

## 6. Logical holonomy calculation

Write A_P(s)=exp(-sH/2)P, G(s)=A_P†A_P=P exp(-sH)P on the input logical space, and W(s)=A_P(s)G(s)^-1/2. W is the canonical filter isometry. Crucially H is FIXED while s varies, so

A_P† A_P'=G'/2

is Hermitian. Therefore

W†W'= (1/2)G^-1/2 G' G^-1/2 + G^1/2 (G^-1/2)'.

If G(s)=g(s)I, this vanishes exactly: the canonical isometry is already parallel transport. There is no unknown logical Berry rotation. This is special to the scalar inverse-temperature path; a generic changing-Hamiltonian filter path need not share it.

If G=g(I+E) with ||E||<=delta<1/2 uniformly, the Frechet derivative of inverse square root gives ||W†W'||<=C delta ||H||. One way to see the scale is to subtract the scalar-G expression in the displayed formula; scalar derivatives cancel, and ||G'||/g<=||H||(1+delta). Consequently the adiabatic parallel-transport unitary differs from W by at most C beta delta||H||. Since ||H||=O(n), an exponentially small uniform relative Gram error remains exponentially small after this polynomial loss. The same operator bound gives reference-safe error for arbitrary logical entanglement. Uniform near-scalarity must actually be proved; diagonal thermal weight estimates alone do not imply it.

## 7. Relation to established methods and exact remaining gates

The weighted ensemble of normalized imaginary-time filtered basis states is the METTS idea (White, arXiv:0902.4475; Stoudenmire–White, arXiv:1002.1305). That representation does not guarantee efficient imaginary-time preparation or Markov-chain mixing. Rapid adiabatic parent-state preparation is established machinery, especially for commuting Gibbs/PEPS settings (Ge–Molnár–Cirac, arXiv:1508.00570). The potentially substantive join here is the weak-noncommuting, signed-code filtered parent with protected logical transport, not invention of these general methods.

The essential unclosed gates are exactly: (i) the actual code/host gap-stability hypothesis for F0 and the derived interaction norm; (ii) sampling the correct noncommuting diagonal ensemble weights; (iii) the uniform relative logical Gram estimate. No dressed-sampler gap or target conditional-marginal oracle is used by this alternative. Physical final noise and inaccessible-bath constraints remain separate.
