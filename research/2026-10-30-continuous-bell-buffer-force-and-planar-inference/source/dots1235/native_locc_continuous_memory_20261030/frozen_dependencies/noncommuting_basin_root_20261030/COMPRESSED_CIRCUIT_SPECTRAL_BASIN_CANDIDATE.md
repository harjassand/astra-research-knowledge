# A compressed proof circuit and an inner spectral basin
2026-10-30. Root construction and proof outline. Independent review and actual-interface verification pending. This is intended to repair a real gap, not retroactively certify the earlier noncommuting drift.

## The actual obstruction
The accepted older global-memory proof used a witness commuting with its raw syndrome/history basin projector. New debt witnesses need not commute raw energy. Therefore neither a basin-supported state after a noncommuting congruence, nor the adjoint killed-generator inequality, is automatic. A full-space low-witness spectral subspace also fails: remote low-syndrome sectors can lie outside the Tanner radius. The construction below keeps an OUTER canonical basin and uses a different INNER spectral cutoff.

## 1. Precise structural premises
Let E be a sum of bounded commuting local terms, 0<=E<=e_max N, V=exp(sE). Let P0 be the projector onto canonical error radius below r0 N, with r0 strictly below the radius where Tanner confinement and canonical logical-edge identities hold. It commutes E and the credited raw potential

 A=V product_i D_i,    exp(-c_t tN)V<=A<=V,

where the positive commuting discounts D_i are local and uniformly bounded away from zero. Local physical and proof operators have fixed system support and energy bandwidth bounded independently of N.

The outer-boundary premise is: whenever a bounded-support operator connects P0 to its complement, its source and target lie in a boundary strip R0 with

 R0<=1_(E>=bN-O(1)),                                  (1)

for a fixed b>0. This follows from actual canonical-radius confinement only when the boundary strip on BOTH sides is still within the admitted radius. It is not inferred from small syndrome globally.

The uncompressed local proof circuit Y=product exp(epsilon_i Xi/2) has fixed color depth, Xi>=0 bounded and local, max epsilon_i=delta, and O(N) gates. Its actual relative drift has been earned in the unconditional coverage observable D:

 L^*(W)<=S†[-kappa D+rho N I]S,
 W=S†S, S=Y A^(1/2),                                 (2)

with D>=c E on P0 (not globally). The constant c can be absorbed into kappa. Any already-proved uniform Taylor/noise errors are included in rho. All actual system-leg generator norms sum to O(N); bath-only dynamics commutes system observables. Existing joint-CPTP regularity is retained.

Finally, compression of each bounded-support operator to P0 acts as logical identity tensor an auxiliary operator in the canonical frame. This is the same distance/representative edge property used for the raw killed process, and must apply to proof Xi as well as physical generator legs. It is NOT an assumption of global logical identity before compression.

## 2. Compress the proof gates, not just the final witness
On the Hilbert space P0 H set

 Xi,0=P0 Xi P0,
 Y0=product exp(epsilon_i Xi,0/2),
 S0=Y0 A0^(1/2),  W0=S0†S0,
 A0=P0 A P0, V0=P0 V P0.

All inverses below are on P0 H. Positivity and uniform spectral bounds give W0>0 there. Define the inner spectral projector

 P1=1_(W0<=exp(aN))  within P0 H,                     (3)

where a>0 will be chosen small. Extend the witness to the full space by F=W0+Q0, Q0=I-P0. Then [F,P1]=0 exactly. P1 is NOT asserted geometrically local.

The compressed gates lose geometric locality, so the finite-depth Taylor lemma must NOT be applied to them as if they were local. Instead compare them with the already-analyzed uncompressed circuit on P1-supported inputs, using the boundary estimates below.

## 3. Higher moments from weighted conjugation: exact algebra
Since [P0,E]=[P0,A]=0, compressing Xi does not enlarge its norm after energy conjugation:

 ||exp(theta E) Xi,0 exp(-theta E)||
   <=||exp(theta E) Xi exp(-theta E)||<=C_theta.

The same fixed-theta bound holds for A^theta Xi,0 A^-theta: the raw energy factor has bounded local bandwidth, and only a bounded number of local discounts fail to commute the original Xi. Consequently for every FIXED theta,

 ||A0^theta Y0^(+/-1) A0^-theta||
 +||A0^theta (Y0†)^(+/-1) A0^-theta||
   <=2 exp(C_theta delta N).                         (4)

No geometric cancellation of compressed gates is needed in (4); simply multiply their O(N) bounded exponential norms.

Write G0=Y0†Y0, W0=A0^(1/2)G0 A0^(1/2). For any fixed positive integer k,

 A0^k W0^-k
   = product_(j=k down to1)
       [A0^(j-1/2) G0^-1 A0^(-j+1/2)].              (5)

Equation(4) bounds the norm in (5) by exp(C_k delta N). Taking the adjoint square and conjugating by W0^k yields

 A0^(2k)<=exp(C_k delta N) W0^(2k).

Because A0 commutes V0 and A0>=exp(-c_t tN)V0,

 V0^(2k)<=exp([2k c_t t+C_k delta]N) W0^(2k).         (6)

This is a derived higher-power comparison, not the invalid inference that arbitrary operator inequalities can be raised to powers.

For a positive state rho supported in P1,

 Tr(V0^(2k) rho)
 <=exp([2ka+2k c_t t+C_k delta]N) Tr rho.             (7)

## 4. Weighted boundary suppression can beat coarse exponential norms
For any fixed p<2k, (1),(7) imply

 Tr(V0^p R0 rho)
 <=exp([2ka+2k c_t t+C_k delta-(2k-p)sb]N+O(1)).      (8)

The analogous Hilbert-Schmidt bound after any partial compressed or uncompressed proof circuit follows by inserting V^k and V^-k; each partial circuit has energy-weighted norm exp(C_k delta N). A fixed number of local insertions adds only a constant factor. Powers of A^(1/2), or coarse global observable norms, add a fixed exponential exp(CN), independent of k.

Choose a<sb. First choose a FIXED k large enough that 2k(sb-a) beats all such fixed exponential costs by a desired margin; then choose t and delta small enough that 2k c_t t+C_k delta retains that margin. Constants C_k can grow rapidly with k; no uniform k limit is claimed. All choices remain fixed independently of N.

Thus polynomially many boundary terms are exponentially small, even if one uses conservative exp(CN) operator bounds on their other factors.

## 5. The comparison still requiring a full written term-by-term check
For a single local Xi, the difference between exp(epsilon P0 Xi P0)P0 and P0 exp(epsilon Xi)P0 has a Duhamel expansion containing a P0 Xi Q0 or Q0 Xi P0 crossing. That crossing is supported in R0. The same holds for the difference before the final P0 compression. Telescoping O(N) gates and differentiating the actual O(N)-term generator introduces only polynomially many such terms. Bounds(7)-(8), including partial-circuit versions, should therefore give, uniformly on positive P1-supported rho,

 |Tr[(L^*F-L^*W)rho]|<=exp(-cN),
 ||S rho S†-S0 rho S0†||_1<=exp(-cN),                (9)

after absorbing the fixed extensive norm costs as in section4. The arbitrary extension Q0 in F adds only actual P0-boundary transitions and is covered by the same estimate.

Equation(9) is the principal comparison obligation. It must be proved with exact operator orders, complete actual losses, and a joint-reference uniform bound. It is NOT certified merely by the outline above. In particular, never treat a nonlocal compressed gate as an ordinary local gate.

If(9) is earned, S0 rho S0† is EXACTLY P0-supported, so(2) and actual basin coverage give

 Tr(L^*F rho)
 <=-kappa Tr(S0† E S0 rho)+rho_coeff N Tr(F rho)
       +exp(-cN).                                  (10)

The symbol rho_coeff denotes the scalar noise/remainder coefficient, not the state rho.

## 6. Entropy and killed moment on the INNER basin
The weighted-conjugation bounds also give

 S0 S0†=Y0 A0 Y0†<=exp(gN)V0,       g=O(delta).

Operator log monotonicity and polar functional calculus on P0 H imply

 S0† E S0 >= [W0 log W0-gN W0]/s.                   (11)

Now kill the ACTUAL generator at P1. Since[F,P1]=0, killed adjoint drift differs from compressed full drift by subtracting positive outgoing jump gains; no noncommuting raw-P0 shortcut is used. Equations(10)-(11) yield a scalar inequality

 x'<=-(kappa/s)x log x+(rho_coeff+kappa g/s)N x
         +exp(-cN),                                (12)

for x=Tr(F rho_killed). A fixed coefficient nu>g+s rho_coeff/kappa gives the invariant bound x<=exp(nu N), provided initialization is below it and N is large. Choose nu<a. The small additive error is absorbed at this barrier; no division by a potentially tiny killed trace is needed.

## 7. Exit and logical comparison obligations
A local system leg J obeys ||S J S^-1||<=C for the original uncompressed finite-depth circuit. Boundary comparison should transfer, on P1-supported states,

 Tr(F J rho J†)<=C Tr(F rho)+exp(-cN).                (13)

Inside P0, its P1-complement is bounded by exp(-aN)W0. Escape to Q0 is separately exponentially suppressed by(7)-(8). Thus actual off-P1 Hamiltonian/jump/system-leg effects are controlled by exp[-(a-nu)N/2], times polynomial norms, and the usual full-versus-killed Duhamel estimate applies. For joint HP noise one must use finite system-leg expansion and the actual joint cb norm, not assume a selected physical unraveling or finite bath dimension.

Each P0 Xi P0 and P0 local physical leg P0 is logical identity by the structural canonical-edge premise. Hence Y0,W0 and its spectral P1 are also logical identity on the canonical code factor. The inner spectral kill does not secretly perform a logical gate. The final output can be transferred to the ordinary common correctable span using P1<=P0 and the actual fixed recovery radius.

## Scope
This construction may repair BOTH failed compression transfers: the state after congruence is kept in P0, while actual killing uses P1 commuting with the constructed witness. The higher-moment algebra is exact under its stated weighted-locality premises. The boundary comparison(9), local-leg transfer(13), and actual native canonical-edge checks remain to be completed and independently reviewed. No new physical measurement, reset, global control or environment reconstruction is introduced; all compressed circuits and spectral filters are analysis objects.
