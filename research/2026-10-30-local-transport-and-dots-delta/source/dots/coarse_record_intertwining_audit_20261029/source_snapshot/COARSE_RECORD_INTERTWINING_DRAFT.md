# Coarse-record intertwining and local approximate axes
2026-10-29. New author lemma; not independently received. No Fopt-competitive approximate decoder yet.

Work first with the IDEAL controlled-Hamiltonian implementation of the finite coarse-record circuit. Program collision and known-control errors are separately paid in full-instrument diamond distance as in the received finite acquisition construction. Let the Hermitian response operators Delta_a have norm<=1 and set B_ab={Delta_a,Delta_b}/2. Suppose max_(a,b,c)||[B_ab,Delta_c]||op<=kappa. Then ||B_ab||<=1 and ||[B_ab,B_cd]||<=2kappa by expanding the two products in B_cd. No centrality or joint eigenbasis is assumed.

## 1. Coherent record instruments intertwine approximately
Let V_j be the complete Stinespring isometry of the jth coarse measurement, including uncomputed workspace and all copied record/dephasing registers. Let T_j be a public upper bound on the TOTAL absolute controlled-B_j evolution time in the compute and uncompute circuits. All other gates act on clean registers and commute with any target-only X. The Duhamel bound
 ||[exp(i t B_j),X]|| <= |t| ||[B_j,X]||
and circuit telescoping imply
 ||V_j X-(X tensor I)V_j|| <= T_j ||[B_j,X]||.
Copying/dephasing a clean record adds no term. The same statement holds for Hermitian X or arbitrary X; here only Hermitian targets are needed. For sequential V=V_q ... V_1,
 ||V Delta_a-(Delta_a tensor I)V|| <= kappa sum_j T_j,
 ||V B_ab-(B_ab tensor I)V|| <= 2kappa sum_j T_j.
Ancilla identities are suppressed below. This is stronger than nonselective disturbance: it controls the full record isometry, and does not assume later measurements see an unchanged target.

## 2. The actual copied number localizes each Gram entry
For one finite coarse measurement of B_j, let g_j be the real center of the copied bin, choosing representatives in [-3,3]. On every eigenvalue b in[-1,1], if the coherent median estimate is within g_guard<=w/2 of b, the copied center obeys |g_j-b|<=w. Otherwise |g_j-b|<=4. If the QPE tail probability is at mostbeta, then
 ||V_j B_j-g_j V_j|| <= zeta0:=w+4sqrt(beta).
This follows by squaring on each eigenvector and averaging the orthogonal record components; it does not discard low-probability records or normalize a selected outcome. The following uncompute acts only on workspace and target, commuting with B_j, and cannot change the recorded-label probabilities.

In a sequential instrument, compare B_j through the preceding stages. Since g_j is a retained classical register, later stages commute with g_j. Thus
 ||V B_j-g_j V|| <= zeta0+2kappa sum_(ell<j) T_ell.
Combining this with the full intertwining bound gives OUTPUT-side localization
 ||(B_j-g_j)V|| <= zeta:=zeta0+4kappa T_total.
This covers all six Gram entries and is valid even though their measurements do not commute.

## 3. Record-dependent linear combinations
Let v and u be orthonormal real coefficient vectors computed from the classical records; their entries commute with every target operator. Put D(v)=sum v_a Delta_a and g(v,u)=sum v_a u_b g_ab, with symmetric stored g_ab. Since sum_a|v_a|<=sqrt3,
 ||(D(v)^2-g(v,v))V||<=3zeta,
 ||({D(v),D(u)}/2-g(v,u))V||<=3zeta.
If the numerical recorded matrix is shifted or rounded by operator normeta, add eta to the right-hand scalar discrepancy. On a branch with positive recorded eigenvalues g1^2,g2^2>=h^2, choose its orthonormal eigenvectors and define A=D(v)/g1, B=D(u)/g2. Let W be V restricted by the corresponding record projector (a subisometry, no conditioning division). Then
 ||(A^2-I)W||, ||(B^2-I)W|| <= delta:=(3zeta+eta)/h^2,
 ||{A,B}W|| <= 2delta.
Globally on these record branches ||A||,||B||<=sqrt3/h. These are local algebra relations on W, not global Pauli identities and not a claim that the record describes a pre-existing source mode.

## 4. Reflection replacement and the propagated-support issue
Define R=sign(A), S=sign(B), assigning+1 at zero. Spectral calculus gives for every vector
 ||(R-A)psi||<=||(A^2-I)psi||,
and similarly for S,B. Hence both replacements on W cost at mostdelta, with no global spectral gap.

To control products one MUST also control a replacement on B W, not silently assume B preserves the record image. Since
 ||[A^2,B]|| <= (3sqrt3 kappa)/h^3
(by expanding D(v)^2 as a coefficient combination of B_ab and commuting with D(u)), one obtains
 ||(R-A)B W|| <= ||(A^2-I)B W||
 <= (sqrt3/h)delta+3sqrt3 kappa/h^3=:delta_cross.
The symmetric bound holds for (S-B)A W. Thus
 ||{R,S}W|| <= 4delta+2delta_cross.
Indeed compare RS W to AB W and SR W to BA W, spending delta+delta_cross each, then use the 2delta anticommutator bound. R,S are EXACT Hermitian unitaries even outside W. This supplies valid two-observable extraction inputs without a free global Clifford rounding.

## 5. Unresolved objective bridge
A standard two-observable extraction isometry is valid for any R,S, so the preceding relations are potentially enough to approximate a local qubit extraction. They do not yet prove additive optimality against Fopt(N), especially on approximate opposite-chirality components and when the third response is not a true central-fiber Pauli direction. An upper certificate or a weighted approximate representation argument is still needed. No nearby exact channel, block projector, named source mode, or source inverse has been constructed.
