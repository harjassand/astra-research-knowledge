# Noncommuting energy/congruence entropy bridge
2026-10-30. Root derivation, awaiting independent check. Intended use: the new weighted native-LOCC debt observable need NOT commute with raw syndrome energy. This lemma does not supply missing useful DATA service.

## 1. Exact general lemma
Let E>=0 act on the finite physical system, V=exp(sE), s>0, and Y be an invertible system operator. Define

  S=Y V^(1/2),       W=S†S=V^(1/2)Y†YV^(1/2).

Suppose the actual comparison

  Y V Y† <= exp(gN) V                                      (1)

has been earned. No commutation of Y or W with E is assumed. Operator monotonicity of log gives

  log(SS†) <= sE+gN I.

Congruence by S, together with the polar-decomposition identity

  S† log(SS†) S = W logW,

yields the OPERATOR inequality

  S† E S >= [W logW-gN W]/s.                              (2)

The identity follows by S=U W^(1/2), so SS†=U W U†. This is not an assertion that exp is operator monotone, nor an illicit replacement logW=sE+log(Y†Y).

## 2. Local proof gates earn the comparison
Suppose E is a sum of commuting bounded local terms with bounded incidence. Every bounded-support gate X_j touches a local energy part E_j whose spectral width is <=K, uniformly in N. Assume ||X_j||<=C_X and Y is an ordered product of m<=c_g N gates exp(δX_j), with X_j Hermitian (positivity is useful below but not needed for (1)).

Unaffected energy factors commute with X_j. The conjugated generator X'_j=V^(-1/2)X_j V^(1/2) has norm at most exp(sK/2) C_X. Hence

  ||V^(-1/2) exp(δX_j) V^(1/2)|| <= exp(|δ| exp(sK/2) C_X).

It follows that

  exp(δX_j) V exp(δX_j) <= exp(C_loc |δ|) V.

Iterating this order inequality by positive congruence through the ordered product gives (1) with g<=c_g C_loc|δ|. This step does not require the gates to commute. Fixed circuit depth is still needed for the SEPARATE local-noise/similarity locality arguments; the global comparison alone only uses O(N) such gates.

If every X_j>=0 and δ>=0, minimum singular values multiply, so Y†Y>=I. Upper singular values give Y†Y<=exp(C'δN)I. Consequently

  V<=W<=exp(C'δN)V.                                       (3)

These raw barrier/initial-moment comparisons coexist with the noncommuting weighted drift (2).

## 3. Scalar entropy law from a real weighted energy drift
If the actual adjoint generator has already been proved to satisfy

  L*W <= -λ S† E S + ρN W,

then (2) gives

  L*W <= -(λ/s) WlogW + (ρ+λg/s)N W.

For any positive subnormalized state with mass<=1, x=Tr(Wρ_state), scalar spectral Jensen gives Tr(WlogW ρ_state)>=xlogx. Therefore

  (logx)' <= -(λ/s)logx + (ρ+λg/s)N,

with limiting coefficient g+sρ/λ. No global mixing of the logical state or operator Jensen inequality is assumed.

If an OUTER unital CP proof map T is used, retain the actual proved form

  L*F <= T[-λ S† E S+ρN W],   F=T(W).

Apply (2) before T and use the positive subnormalized σ=T_*(ρ_state). Then x=Tr(Wσ) and the SAME scalar Jensen argument applies to T(WlogW), not to FlogF. An arbitrary inverse linear map is never used for an order comparison.

## 4. Concrete receiving obligation
The new native-LOCC weighted-debt construction already has W=V^(1/2)Y†YV^(1/2) and negative terms of the form S† Q_i S. Raw E consists of U plus finite-weight mechanical/false-token debt. If actual useful-service work eventually earns

  L*W <= -S†[λ_U U+λ_D Σ_iQ_i]S + ρN W,

and the actual defect energy is bounded by C_D ΣQ_i, then λ=min(λ_U,λ_D/C_D) supplies the hypothesis above. The entropy and raw-energy boundary proof would then work WITHOUT forcing DATA-dependent weighted debt witnesses to commute with U.

This removes a specific representational obstacle exposed by the real malformed-terminal counterexample. It does not grant λ_U>0, acquire a useful correction, or complete continuous LOCC logical lifetime. Those are still the hard actual service obligations.
