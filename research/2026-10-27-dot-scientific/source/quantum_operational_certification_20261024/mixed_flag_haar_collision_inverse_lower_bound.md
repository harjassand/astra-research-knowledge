# Mixed-success flag rank forces dimension-dependent inverse learning

2026-10-27. New exact proof, independent audit requested. Main theorem is stated for full normalized Choi programs. A separate direct adaptive-query extension is proposed below and must be received on its own merits; no teleportation simulation is assumed.

## Family and task

Fix integer r>=2 and let B=C^3 tensor C^r, of dimension3r. Let U be an unknown Haar unitary on B and define the reversible channel

 E_U(rho)=U(rho tensor I_r/r)U*.

If U were known, applying U* and discarding the flag recovers rho exactly. This is a genuinely MIXED success flag, not a pure isometric embedding. For the present normalized WH3 deficit, this family has EXACT Delta=0. Before receiver conjugation its Choi state is Phi_3 tensor I_r/r; the input has r nonzero eigenvalues1/r, its receiver marginal has3r eigenvalues1/(3r), and its WH3 output has3r nonzero eigenvalues1/(3r). Thus f(J)+f(Tr_A J)-2f((W3 tensor id)J)-log3 equals -log r-log(3r)+2log(3r)-log3=0. Receiver conjugation by U preserves all these spectra. The inverse-learning argument itself uses only the displayed channel family.

Its normalized Choi program and fixed logical data states are

 J_U=(1/r)sum_(k=1)^r |Phi_(U,k)><Phi_(U,k)|,
 |Phi_(U,k)>=(1/sqrt3)sum_(a=0)^2 |a>_A U|a,k>,
 sigma_(U,a)=(1/r)sum_k |u_(a,k)><u_(a,k)|,
 |u_(a,k)>=U|a,k>.

The learner receives n independent mixed J_U copies and one independently generated datum sigma_(U,a), all sharing one fixed U. It may perform any joint CPTP processing and may know r and the family. It does not receive purified program preparations or classical U.

Let Omega_a be the Haar average of J_U^tensor n tensor sigma_(U,a). For any two distinct logical basis values a,b,

 (1/2)||Omega_a-Omega_b||1
 <=1-(1-1/r)^n<=n/r.                                (1)

## 1. Exact unseen-flag symmetry

Expand each mixed program using an IID latent flag k_i uniform on{1,...,r}; the independent datum has latent flag k. This is an exact convex decomposition, not an accessible flag oracle.

Condition on any fixed flag tuple(k_1,...,k_n,k) in which k is absent from{k_1,...,k_n}. Let R_k be the known-in-the-proof unitary on the ORIGINAL logical/flag domain that swaps |a,k> with |b,k> and is identity on every other flag sector. Right multiplication U->U R_k preserves Haar measure.

For every program flag k_i, all three vectors U|c,k_i> remain unchanged, so the entire entangled program vector Phi_(U,k_i) is unchanged. Meanwhile U R_k|b,k>=U|a,k>. Hence the conditional Haar-averaged joint program/data state for logical a is IDENTICAL to that for logical b.

The probability of this noncollision event is(1-1/r)^n. Therefore the two experiments share a common positive component of that weight. On its complement the half trace distance is at most1. This proves(1).

No pairwise-information or asymptotic approximation is used. Program copies and data are IID only conditionally on one fixed U; the Haar prior is a proof device for a worst-case guarantee.

## 2. Complete inverse and heralded-recovery lower bounds

Suppose a fixed processor, averaged over its program randomness, satisfies for EVERY U

 ||R_(J_U^n) composed E_U-id_3||_diamond<=zeta,

with unhalved diamond norm and0<zeta<1. Its averaged outputs for logical a and b are within trace norm zeta of the two orthogonal pure states. Their half distance is therefore at least1-zeta. Data processing and(1) imply

 (1-1/r)^n<=zeta,
 n>=log(zeta)/log(1-1/r).                            (2)

For example zeta<=1/4 requires n>=(r-1)log4. More generally n=Omega(r log(1/zeta)) for r>=2. No finite n can give exact uniform inversion at zeta=0 by this bound.

For a complete accepted-plus-erased target alpha id+(1-alpha)erasure with unhalved error delta<alpha, the two target outputs have half distance alpha. The same argument gives

 n>=log(1-alpha+delta)/log(1-1/r).                    (3)

Thus any fixed nonzero throughput fraction with sufficiently smaller constant complete error requires Omega(r) programs. The statement is not restricted to deterministic inversion.

## 3. Exact first-moment corroboration

For n=1 let d=3r and F swap the two physical B registers. Two-copy Haar twirling gives

 Omega_a=[(I_A/3)-P_a/(3rd)] tensor I/(d²-1)
        +[P_a/(3r)-(I_A/3)/d] tensor F/(d²-1).

Hence

 Omega_a-Omega_b=(P_a-P_b) tensor(F-I/d)/[3r(d²-1)].

Since ||P_a-P_b||1=2 and ||F-I/d||1=d²-1,

 (1/2)||Omega_a-Omega_b||1=1/(3r).

The collision estimate1/r is deliberately loose at one program but has the needed rank scaling.

## 4. Consequence for the pure-versus-mixed operational boundary

The positive discriminant for this family is unitarily equivalent to

 [(Phi_3-I_9/3) tensor I_r]/r.

Its positive eigenvalue is2/(3r), with multiplicity r; its negative eigenvalue is-1/(3r), with multiplicity8r. Thus the supplied-gap cost in the mixed-success positive-band filter extension cannot be replaced here by a dimension-independent gap inferred from p=1 or reversibility alone.

This lower bound shows that the pure-success operational theorem cannot extend to arbitrary mixed-success rank with the SAME dimension-independent constant-accuracy training budget. It does not prove an optimal r exponent for the available filters, and it does not negate known-source reversibility. The current filter's r² gap cost and this Omega(r) lower bound leave a rank-scaling gap.

## 5. Proposed direct adaptive physical-query extension — separate audit gate

There is a direct symmetry route that does not require a common teleportation correction. Each physical E_U call is exactly the uniform mixture of isometries

 E_(U,k_i)(rho)=U(rho tensor|k_i><k_i|)U*.

For an arbitrary fixed definite-causal-order adaptive strategy using at most n training/decoder calls, expand all calls with independent latent flags k_i. Conditional on a fixed flag sequence and a datum flag k not among them, the same U->U R_k transformation leaves EVERY queried isometry E_(U,k_i) identical as a channel, including on entangled inputs. It changes the logical-b datum into the logical-a datum. By induction through the adaptive circuit, the entire conditional output experiment is identical. Internal measurements/choices can be deferred or included in the comb.

If this conditional-comb argument is received, equations(1)-(3) extend to arbitrary bounded adaptive physical calls of this family, even if calls occur after receiving the datum. Strategies stopping early may be padded with unused calls to a fixed cap n. The independent noisy datum preparation is one extra physical use when included in total accounting.

This extension is NOT being inferred merely from Choi-copy access. It relies on the special direct-sum IID-flag realization and right-Haar symmetry. It does not claim indefinite causal order, purified/coherently indexed flag access, or a general reduction from arbitrary channels to Choi programs. Until independently checked, the primary received target of this note is the Choi-program theorem above.
