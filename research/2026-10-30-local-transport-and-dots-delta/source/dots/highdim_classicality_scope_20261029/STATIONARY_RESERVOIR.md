# A faithful actual prior does not remove the high-dimensional reservoir obstruction

2026-10-29. Analytic variant/diagnosis of retained N61/N552/N553, not a counterexample to the small-Holevo-loss question N371. Independent receiving review not yet requested. No novelty or efficient-acquisition claim.

## What is already known, and the additional boundary
The retained copy reservoir already disproves every dimension-independent residual-to-EB modulus, even for one common finite prior. Its actual Holevo loss diverges. Therefore the accepted qubit residual theorem cannot be generalized by removing its input-dimension restriction.

The additional construction below makes the **actual ensemble mean faithful and exactly stationary**, and can make the broadcaster marginal primitive. The entire obstruction still resides in finite-lived quantum transients. Thus faithfulness, actual stationarity, primitivity, and a finite entanglement-breaking power do not individually produce a dimension-free residual modulus. Entropy loss remains large; the special entropy-production requirement is not replaced by any of those hypotheses.

## 1. The stationary reset construction
Fix L>=2, d>=2, k_j=2^j, j=0,...,L-1, m=2^(L-1), H_j=Sym^(k_j)(C^d), D_j=dim H_j, and H=direct_sum_j H_j. Choose a probability law r_j on the levels, with r_(L-1)>0. Write

`a_j=sum_(k=j)^(L-1) r_k`, `Z=sum_j a_j=sum_j(j+1)r_j`, `p_j=a_j/Z`.

Let tau_j=I_(H_j)/D_j and tau=direct_sum_j r_j tau_j. Define a two-output channel B as follows: measure the sector; at j>=1 split its symmetric tensor into equal halves and put both halves into level j-1; at j=0 discard the input and prepare tau tensor tau. The splitting isometries and full-domain CP/TP argument are exactly the retained construction. The reset term is an ordinary replacement channel. Both marginals equal Phi.

For a pure qudit psi, set

`rho_psi=direct_sum_j p_j (|psi><psi|)^tensor k_j`.

Use a common finite positive projective moment design of order at least m+1, so all moments and estimation inequalities below are exact. Its actual mean is

`sigma=direct_sum_j p_j tau_j`.

This sigma is faithful because every a_j>0. The uniform symmetric-state partial trace identity gives Phi(tau_(j+1))=tau_j for j<L-1, and the scalar balance law

`p_j=p_(j+1)+p_0 r_j` (set p_L=0)

therefore proves **Phi(sigma)=sigma** exactly.

The family disturbance is also exact:

`Phi(rho_psi)-rho_psi = direct_sum_j p_0 r_j (tau_j-psi^tensor k_j)`,

so

`T(Phi(rho_psi),rho_psi)=p_0 sum_j r_j(1-1/D_j) <=1/Z`.

The state-estimation proof in N61 applies with weights p_j and gives, for EVERY EB E,

`average_x T(E rho_x,rho_x) >=1-sum_j p_j(k_j+1)/(k_j+d)
 >=1-(m+1)/(m+d)`.

This lower bound uses the same finite design prior for every E; no minimax interchange is involved.

### Uniform stationary ladder
For r concentrated at the top, Z=L and p_j=1/L. Then

`b_displayed=(1-1/D_top)/L`, `e_average >=1-(m+1)/(m+d)`.

Taking d=Lm makes b->0 and e->1. The actual mean remains faithful and stationary at every finite L.

### Primitive version
Take, for example, r_j=(1-epsilon)1_(j=L-1)+epsilon/L for fixed 0<epsilon<1. Then every r_j>0, Z=(1-epsilon)L+epsilon(L+1)/2, hence b=O(1/L) and the same e->1 conclusion holds.

This Phi is primitive. Every initial sector reaches a bottom-reset event within L applications. After the first reset its marginal is tau, which is faithful; every later image of a faithful state is faithful, since its positive bottom-sector trace supplies a positive multiple of tau. Thus Phi^L maps every nonzero positive operator to a positive definite operator. This is an explicit finite-time positivity-improving property, not an inference from sample spectra.

## 2. All ensemble letters can also be faithful
For 0<eta<1, define rho_psi^eta=(1-eta)rho_psi+eta sigma. They are faithful, have the same actual mean sigma, and

`T(Phi rho_psi^eta,rho_psi^eta)=(1-eta) b_displayed`.

By trace contraction and triangle inequality, every common EB map still has average error at least

`1-(m+1)/(m+d)-2eta`.

For eta_L=L^-3, the same maximal separation survives. Thus neither singular letters nor a singular mean drives this variant.

## 3. Exact entanglement-breaking index and the transient mechanism
For either reset law, Phi^L is EB: in every word in the sector-transition expansion there has been at least one bottom reset, which is EB, and arbitrary CP pre/postcomposition preserves EB. The entire sum is CPTP. This is a finite positive channel expansion, not the invalid state-dependent left-resolvent normalization.

No smaller positive power is EB. For j<L, restrict Phi^j to the top sector. It maps each pure tensor psi^tensor m to the distinct pure tensor psi^tensor(m/2^j), in the corresponding lower sector. An EB map cannot send two nonorthogonal pure inputs to two distinct pure outputs: every preparation state with nonzero probability must equal the corresponding pure output, so the outcome supports would be disjoint, implying perfect discrimination of nonorthogonal inputs. Choose two distinct nonorthogonal psi. Therefore the entanglement-breaking index of Phi is exactly L.

The elementary implication for any channel with Phi^L EB is

`T(rho,Phi^L rho) <= L T(rho,Phi rho)`.

The reservoir shows the L dependence cannot be removed uniformly: along d=Lm, the best possible common EB error is nearly one while its original residual is about 1/L. This diagnoses a physical supply of long-lived noncommuting transient information, not merely a count of eigenvalues close to one.

## 4. The even sharper zero-spectrum diagnostic in the original reset model
In the retained N61 channel, reset the bottom to a fixed state omega in the bottom level. Then Phi^L=replace_omega. On the real space of Hermitian traceless operators, Phi is nilpotent with index exactly L. All its eigenvalues there are zero, yet

`||(I-Phi)^-1||_(1->1, Hermitian traceless)=L`.

The upper bound is the finite Neumann sum sum_(j=0)^(L-1) Phi^j, with each channel trace-contracting on Hermitian operators. For the lower bound, take orthogonal qudits psi,phi and X=rho_psi-rho_phi with uniform level weights. Then ||X||_1=2, while (I-Phi)X is the top-sector difference divided by L and has trace norm 2/L. Thus the inverse norm is at least L. This is an exact nonnormal-transient obstruction to using eigenvalue gaps alone in a high-dimensional generalization of the qubit proof.

This original zero-spectrum model does not have the faithful stationary actual mean of Section1; those are distinct variants, not one set of simultaneously claimed properties.

## 5. Why this still does not answer N371
For the uniform stationary ladder, outputs preserve every lower pure block and replace only the top block by tau_top. Since sigma is stationary, the exact actual-prior Holevo loss is

`delta=log D_top/L`.

With faithful letters, replace the numerator by

`log D_top-S((1-eta)P+eta I/D_top)`

for any rank-one top-sector P. It still diverges when d=Lm and eta=L^-3.

For the primitive reset version, write alpha_j=r_j/a_j. Its block outputs are `(1-alpha_j)P+alpha_j I/D_j`; entropy concavity gives

`delta >= p_0 sum_j r_j log D_j >=p_0(1-epsilon)log D_top`.

This also diverges for d=Lm. (For faithful letters use the same concavity comparison against their block entropy.) Thus the construction expressly fails the small-Holevo-loss premise. It blocks a proposed *residual* extension even under strong regularity, while leaving the actual entropy-loss question intact.

## 6. Resource and acquisition contract
Each input already contains a random, genuinely supplied number of copies of an unknown qudit. The splitting does not synthesize copies from one unknown qudit. For the primitive/uniform reset version, a high-dimensional maximally mixed reset supply is additionally specified, independent of psi. Finite design existence does not supply an efficient physical preparation or short classical description. The lower bound is information-theoretic against every EB comparator, not computational hardness or lack of comparator acquisition.

The useful next question is therefore not another dimension-free residual conjecture, already refuted, but whether actual small entropy production forbids these long quantum transients, or whether a genuinely different classical-label/data-hiding mechanism can retain nonclassical information while spending vanishing Holevo loss. None is established here.

## Provenance
Governing retained sources were read at Git revision d5366275f4886a027526b70997e75db2c19e4efa in harjassand/astra-research-knowledge: N61 proof web/pages/d-b7d3e0402d7b0078.html; N553 RESEARCH_PROOF.md; N371 entropy-tree and power-exponent sources. Exact retrieved copies and source hashes are retained in sources/ and SOURCE_SHA256SUMS.txt. The stationary/primitive reset modification and exact nilpotent inverse calculation are the additions in this note, not a reassertion that the original reservoir newly resolves any gate.
