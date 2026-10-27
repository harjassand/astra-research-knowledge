# Quadratic mixed-flag rank lower bound for full-Choi programs

2026-10-27. New proof candidate, independent receipt requested. This strengthens the received collision theorem ONLY in full normalized Choi-copy access. No quadratic lower bound for arbitrary adaptive physical channel calls is inferred.

## Statement

For the reversible p=1, Delta=0 family

 E_U(rho)=U(rho tensor I_r/r)U*, U Haar on dimension d=3r,

suppose a fixed processor using n IID normalized Choi programs J_U and one independent noisy datum achieves complete unhalved diamond inverse error at most0<zeta<1 uniformly in U. Then

 n >= (r²/144)[log3-h(zeta/2)-(zeta/2)log2],          (1)

where h is binary entropy with NATURAL logarithms. In particular constant inverse accuracy requires Omega(r²) mixed Choi programs. The bracket is positive for0<zeta<1; at zeta<=1/4 it is at least the value at1/4.

The processor may perform arbitrary collective quantum processing of its programs and datum, with arbitrary ancillas. Programs are mixed copies, not purified preparation or inverse oracles. The earlier Omega(r) latent-collision bound remains the separately received result for general bounded adaptive physical queries.

## 1. Entropy deficits of averaged program states

Let

 R_m=E_U[J_U^tensor m], R_0=1,
 F_m=m log(9r)-S(R_m).

The one-copy Haar mean is R_1=I/(9r). The states R_m are consistent and permutation symmetric. Define a_m=F_m-F_(m-1). Then

 a_(m+1)=I(X_(m+1):X_1...X_m)_(R_(m+1)),

where each X_i is a complete qutrit-reference/physical-output Choi register. Data processing plus permutation symmetry makes a_m nondecreasing; equivalently this is strong subadditivity. Therefore, for n>=1,

 a_(n+1)<= [F_(2n)-F_n]/n <=F_(2n)/n.               (2)

The final inequality uses F_n>=0. This entropy increment removes correlations already present among the n programs; it is not their full relative entropy to a flat baseline.

## 2. Pair purity reduces F_m to a Haar moment

Write J_U=P_U/r, where

 P_U=(I_A tensor U)(Phi_3 tensor I_r)(I_A tensor U*).

Thus P_U is a rank-r projector and Tr_A P_U=I_d/3. Define

 g(U)=9r Tr(J_I J_U)=(9/r)Tr(P_I P_U).

It is nonnegative, bounded by9, and E g=1. Haar invariance gives

 (9r)^m Tr(R_m²)=E[g(U)^m].

Since von Neumann entropy is at least order-two Renyi entropy,

 F_m<=log E[g^m]<=log E exp[m(g-1)].                 (3)

The last inequality uses log g<=g-1, with g=0 treated directly. No support-invertibility assumption or Schur-diagram truncation is involved.

## 3. Dimension-scaled Haar concentration

The only external concentration input is the SU(d) logarithmic Sobolev inequality with Hilbert-Schmidt Riemannian metric:

 Ent(f²)<=(4/d) E||grad f||².

This normalization is explicitly stated as constant2/d under Ent(f²)<=2C E||grad f||² in the Appendix/proof of Theorem15 of [Meckes and Meckes, Spectral measures of powers of random matrices](https://arxiv.org/html/1210.2681). We use SU(d), not an unjustified Ricci bound on U(d). All projectors and g are invariant under global phase, so their Haar averages on SU(d) and U(d) coincide.

For a tangent Hermitian generator K of Hilbert-Schmidt norm1,

 |d/dt Tr[P_I P_(exp(itK)U)] at t=0|
 <=2||P_I||_2 ||(I_A tensor K)P_U||_2
 =2sqrt(r)*sqrt(Tr[K² Tr_A P_U])
 =2sqrt(r/3).

Consequently g has gradient norm at most L=6sqrt3/sqrt(r). The standard Herbst calculation is included to fix constants: with M(t)=E exp(tg) and psi=log M, apply the log-Sobolev inequality to exp(tg/2) to obtain

 t psi'(t)-psi(t)<=t²L²/d.

Integrating the derivative of psi(t)/t from0 yields

 log E exp[t(g-Eg)]<=L²t²/d=36t²/r².                 (4)

All functions are bounded on the compact group, so the differentiation/integration is legitimate. Combining(3)-(4),

 F_m<=36m²/r², for EVERY integer m>=1.              (5)

This bound can be loose for large m, but remains valid; it does not continue a finite-dimensional Haar inverse-Gram formula past a support change.

## 4. The entropy increment bounds the actual logical-label information

Consider R_(n+1), and call the final qutrit reference A and its physical output B. Because Tr_A J_U=I_d/d for every U,

 Tr_A R_(n+1)=R_n tensor I_d/d.

Also A is maximally mixed. It follows EXACTLY that

 I(A:programs,B)=log3+S(R_n)+log d-S(R_(n+1))
               =F_(n+1)-F_n=a_(n+1).

Measure A in the logical basis. Its outcome a is uniform on three values, and the conditional remaining state is precisely

 Omega_a=E_U[J_U^tensor n tensor E_U(|a><a|)].

Measurement data processing therefore bounds the Holevo information of this actual program/data ensemble by a_(n+1). Equations(2) and(5) give

 I(a:programs,B)<=144n/r².                           (6)

This is the needed label-specific cancellation. It does not assert the stronger conjectured conditional chi-square formula6n/(9r²-1).

## 5. Uniform complete inversion forces a constant amount of label information

Feed one of the three logical basis states uniformly into E_U and apply the learned inverse. Complete unhalved diamond error zeta implies that measuring the logical output in that basis has error probability at most zeta/2, for each U and hence after Haar averaging. The factor1/2 uses the trace-zero difference of two normalized output states.

Fano's inequality and classical/quantum data processing imply

 I(a:programs,B)>=log3-h(zeta/2)-(zeta/2)log2.

Together with(6), this proves(1). No zero-program strategy can meet zeta<1, since its averaged data state is independent of the label; thus the n>=1 step in(2) loses no case.

## Scope and implications

The bound is quadratic in mixed-flag rank even at exact reversibility and zero WH3 deficit. It matches the r² exponent suggested by the positive spectral gap2/(3r) in the available sample-filter construction, but does not by itself prove a complete inverse upper bound for arbitrary mixed success.

This proof uses the exchangeable family of IID Choi programs in an essential way. It DOES NOT upgrade the separately received adaptive physical-query Omega(r) collision lower bound to Omega(r²). A suitable reduction/comb argument would be needed for such a stronger access claim.

Nor is(1) an optimal accuracy-dependence statement: its Fano bracket saturates as zeta decreases. The collision lower bound retains the separate r log(1/zeta) term. Both necessary conditions can be imposed together in the Choi-program model.
