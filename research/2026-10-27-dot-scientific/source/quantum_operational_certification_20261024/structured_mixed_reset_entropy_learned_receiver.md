# Unknown-isometry logical-isotropic mixed-reset receiver

2026-10-27. Frozen candidate for independent receiving. Unhalved diamond norm throughout. This theorem is restricted to the source family below; it is not an entropy theorem for arbitrary mixed-success/reset channels.

## 1. Source, target, and result

Let

 E(rho)=V[p rho tensor sigma+q Tr(rho) I3/3 tensor tau]V*, q=1-p,

where V is an unknown isometry from C3 tensor F into B, sigma,tau are arbitrary flag density matrices (not necessarily commuting), rank(sigma)<=r is supplied, and p>=p0>0. The source is memoryless. Ordinary labelled training produces fresh mixed T=(J+3omega)/4 and omega=I_A/3 tensor E(I3/3). Each costs one channel call. Known A-only Weyls produce T_j. No purification, inverse oracle, hidden factorization, or eigenbasis access is assumed.

For 0<nu<=1 there is a consumed-program receiver with complete accepted-qutrit/erasure error

 ||R E-[p id+q erase]||diamond <= 2 sqrt(5 Delta)+0.495 nu p.       (1)

In particular Delta<=nu^2 p^2/80 suffices for error<nu p. The explicit training count below is O(r^2/(p0^2 nu^3) polylog(r/(p0 nu))), independent of the ambient output dimension. Gate/memory cost is not dimension independent. The original noisy datum is an additional call.

The entropy input is the received `physical_flat_mixed_reset_helstrom_capability.md`: for K=p sigma-q tau, M=1_(0,infinity)(K), the Bayes error

 e=p Tr[(I-M)sigma]+q Tr[M tau]=(1-||K||1)/2 <=sqrt(5 Delta).

This statement is invariant under the unknown isometry. No entropy-to-code-overlap inference is used.

## 2. Actual source discriminant and nine-band ideal map

Use H_j=J_j-5omega=4T_j-8omega=p J_s,j-D, where J_s,j is the normalized success Choi state and, in hidden coordinates,

 D=I9 tensor (5p sigma+4q tau)/9.

In Bell sector j, H_j=4K/9; in each other Bell sector H_j=-(5p sigma+4q tau)/9. Outside the isometry image it is zero. Thus positive bands are the nine mutually orthogonal Phi_j tensor M. Their corrected Bell contractions perform exactly the flag effect M followed by the inverse logical channel; summing labels removes the Bell factor 1/9. The reset accepted map is q Tr(M tau) times logical replacement I3/3. This holds even when sigma,tau do not commute with M, since the flag is discarded.

Useful bounds are

 TrD=4+p, ||D||<=5/9, T_j<=D, omega<=D/4,
 Tr(H_j)_+<=p, rank(H_j)_+<=r, Tr(H_j)_-<=5,
 H_j^2<=8D, ||H_j||<=1,
 D=(H_j)_-+p J_s,j-(H_j)_+ <=(H_j)_-+p J_s,j.       (2)

The positive-rank bound follows because p sigma-q tau has no positive direction on ker(sigma). The square bound follows (A-B)^2<=2A^2+2B^2, p J_s,j<= (9/5)D, and the displayed operator bounds.

## 3. Soft reference, not discarded success mass

Set kappa*=nu p0/(16r). Classify H_j above threshold 2 kappa*/9. Eigenvalues kappa of K with kappa>=kappa* are reliably accepted; kappa<=0 are reliably rejected. The intermediate positive modes may carry LARGE sigma mass and are NOT discarded by a small-mass argument.

Define an analytical soft reference classifier eigenwise: on reliable positive modes replace the ideal finite-QPE classifier isometry by exact accept; on every nonpositive H mode replace it by exact nondestructive reject; on 0<kappa<kappa* retain the actual exact-evolution QPE compute/classify/copy/uncompute isometry. This defines a valid isometry with flag Kraus operators functions of H. The replacement differs in complete instrument norm by at most4 sqrt(eta), uniformly, when reliable-mode misclassification is <=eta. Transition modes are unchanged.

Repeat each binary classifier L times, require all accepts, and otherwise retain the data for the next Bell label. All nine soft reference classifiers use the same scalar rule. Wrong Bell sectors are exactly nondestructively rejected. Consequently the full corrected accepted map is

 p Tr[F(K)sigma] id +q Tr[F(K)tau] R0,

for one common effect 0<=F<=M, F=1 on kappa>=kappa*, F=0 on kappa<=0. Ancilla garbage and the flag are discarded. This also proves logical coherence with an arbitrary external reference: within each Bell sector the circuit acts only on the flag, and the usual corrected Bell contraction is identity on the logical input. Earlier labels act identically on all other Bell sectors. Acceptance at an intermediate mode is not required to be projective.

Let alpha_F=p Tr[(I-F)sigma], beta_F=q Tr[F tau]. Then

 alpha_F+beta_F=e+Tr[(M-F)K]<=e+r kappa*.

The complete ideal error is at most2(alpha_F+beta_F)<=2e+2r kappa*. The rejected quantum register is ultimately replaced by one erasure flag.

## 4. Fresh-program weighted branch lemma for coefficients 4,-8

This section gives the constants needed to reuse the proof, not just its conclusion, of `noise_adapted_weighted_classifier_branch_lemma.md`. Put sigma0=T_j,rho0=omega. A controlled pair uses angles a=4delta,b=-8delta, |delta|<=1/10. The exact controlled collision has principal Kraus I+(cos a-1)C-i sin(a) C sigma0 and positive residual sin^2(a) C[replacement_sigma0-sigma0(.)sigma0]C. The bracket is CP; the same holds for rho0.

Let c=cos a cos b, L0=(cos b I-i sin b rho0)(cos a I-i sin a sigma0), E0=L0-c exp(-i delta H_j). Four-square expansion gives

 E0 E0*<=8192 delta^4 D.                              (3)

Explicit budgets inside the four-square bound are: cubic sine/cosine coefficient squares at most [(64/3)^2+(512/3)^2]delta^6 D; product term at most1024 delta^4 D; exponential remainder at most2 delta^4 D. With delta^2<=.01, four times their sum is below8192 delta^4 D. These use sigma0,rho0<=D, sigma0^2<=D, rho0^2<=D and rho0 sigma0^2 rho0<=D, plus (2).

For a positive CQ input R=sum_i R_i tensor|i><i| in an H_j eigenbasis, its ideal attenuated principal output R0 remains CQ. The cross-term square inequality with epsilon=delta^2 and (3) bounds both signs of principal-minus-R0 by

 delta^2 R0+16384 delta^2 (C Ranc C) tensor D.

The first residual, propagated through the second collision, and the second residual have total auxiliary trace at most144 TrR times delta^2 (budgets80+64). Thus the auxiliary trace constant is16528. Attenuation versus exact ideal evolution costs the absolute CQ majorant with each eigenspace trace at most80 delta^2 TrR_i, since 2(1-c)<=80delta^2. No selected-branch claim A R_i A*<=R_i is made.

Define CQ cap k by TrR_i<=k(-lambda_i)_+. Since TrH_-<=5, all local positive propagation and signed actual-minus-ideal errors fit cap100000 delta^2 k and arbitrary positive remainder pR with TrR<=100000 delta^2 k. The separate remainder is propagated by actual CPTP maps, not presumed to contract. Positive cap-plus-remainder grows at most exp(200000 sum delta^2). Ideal-prefix/actual-suffix Duhamel telescoping with common positive majorants therefore gives, for every selected whole-circuit branch,

 +/- (Psi_actual-Psi_ideal)(H_-) <= e_H H_-+p R,
 TrR<=e_H,  e_H=400000 H exp(200000H), H=sum delta^2.    (4)

Ancillary selection cannot increase CQ cap. This includes fresh-program reverse-time uncomputation and arbitrary controls. It does not apply a false transported-projector uniform population inequality.

For one classifier squared-time h, negative acceptance<=eta. Write beta=eta+e_h. Repeating L all-pass tests yields accepted H_- trace <=5 beta^L+p e_h/(1-beta). Generic signed-pair simulation error <=512delta^2 gives complete actual-versus-soft-reference instrument error

 u=L(4sqrt(eta)+512h).

Let A,B be its retained-data accepted/rejected maps, A0,B0 the soft reference. Decomposing D=H_-+pJ_s-H_+ and using TrH_+<=p gives

 ||A(D)-A0(D)||1 <=5beta^L+p e_h/(1-beta)+2pu,           (5)
 +/-[B(D)-B0(D)]<=k D+pR,
 k=e_(Lh)+eta^L, TrR<=k+e_(Lh)+2u.                     (6)

For the soft reference, accepted effect is F(H) supported on H>0. Its rejection fixes H_- and maps H_+ to H_+(I-F). Hence

 B0(D)-D=p[B0(J_s)-J_s]+H_+F,
 ||B0(D)-D||1<=3p, Tr A0(D)<=p.                       (7)

These formulas hold for nonprojective soft rejection, not only projectors.

## 5. Explicit phase estimation and resource budgets

Set xi=nu/100,
 L=ceil log_16[1000/(p0 xi)], eta=(xi/(100L))^2,
 M=2^m>=1152/kappa*, R=ceil log_2(1/eta).

Use QPE for U_j=exp[i pi(H_j+I)/2], with phase acceptance interval [1/4+kappa*/18,3/4]. The physical spectrum lies within [-5/9,4/9], so no wrap/upper-edge issue occurs. Reliable modes are at least kappa*/18 from the lower boundary; M times that margin is >=64. The usual finite-QPE tail and R independent coherent repetitions with reversible majority give error <=eta. Compute, copy the majority bit, and uncompute all phase registers, retaining their residual garbage until traced. This preserves within-band coherence up to4sqrt(eta), not merely membership probability.

Each forward controlled time is t_a=(pi/2)2^a; all reverse steps use fresh samples. Across nine labels, L classifiers and R repetitions, let

 S=9LR pi(M-1).

Implement each signed segment t with N_t=ceil[10^10 |t| S/xi] pairs. Then total squared time Htot<=xi/10^10 and each classifier h<=xi/(9*10^10 L). All steps have |delta|<=.1. The train-call count is

 ntrain<=2*10^10 S^2/xi+36LRm.                         (8)

Each pair consumes two ordinary T/omega programs. The extra term counts rounding, forward and reverse segments.

The numerical implications, with considerable slack, are

 u<=xi/20, e_(Lh)<=xi/20000, e_h<=xi/(20000L),
 beta<=1/16, beta^L<=p0 xi/1000,
 ||A(D)-A0(D)||1<=p xi/9,
 k<=xi/4000, TrR in (6)<=xi/9.                         (9)

## 6. Full instrument and reset telescope

For any actual suffix of k<=9 labels, its total acceptance effect F_suffix obeys Tr(F_suffix D)<=7kp. To see this, (7),(9) imply A(D) trace<=10p/9 and B(D)<=(1+k)D+pS with TrS<=5; the recursion 10p/9+(1+k)7(k_labels-1)p+5p is below7k_labels p. Here the coefficient k in (6) is <=xi/4000. This coarse bound is used only on small signed errors, never as the ideal reset baseline.

The reset input marginal including source weight is

 S0=q I9/9 tensor tau=D/4-(5p/4)Omega_s,
 Omega_s=I9/9 tensor sigma, TrOmega_s=1.

After j ideal soft rejected labels, S_j=D/4+p Z_j with Hermitian ||Z_j||1<=5/4+3j/4<=10 for j<=8, by (7) and trace-norm contraction. This remains true for noncommuting flag states.

Telescope actual-minus-soft circuits with ideal prefixes and actual suffixes. For the D/4 component, (9) and the suffix bound charge at most pxi/36+(1/4)[7k_labels pxi/4000+pxi/9]. The pZ_j component costs at most2pu||Z_j||1<=p xi. Thus each label costs less than2p xi in reset acceptance; nine labels cost at most18p xi. Common positive order majorants in (6) justify both signs through actual CP suffixes.

The ideal reset accepted mass is beta_F. Actual reset acceptance is at most beta_F+18p xi; relative to erasure, complete reset error is exactly twice this mass, regardless of the accepted reset state. On the genuine branch, the ideal logical loss is at most2alpha_F and the learned complete error is at most9pu<=.45p xi, uniformly with external reference. Therefore

 complete error <=2(alpha_F+beta_F)+36.45p xi
                <=2e+2r kappa*+37p xi
                <=2sqrt(5Delta)+.495nu p,

proving (1). All rejected paths are finally erased; accepted labels receive the known Weyl/transpose correction and are discarded.

## Scope

The logical-isotropic reset and hidden tensor isometry promises are essential. This is not a theorem for general overlapping mixed reset, not an entropy-to-overlap bound, and not a classification of all zero-deficit channels. It consumes fresh programs per data register and makes no batching, reusable-decoder, unassisted-capacity, or finite-block coding claim. The exact-erasure flat-flag subclass has the received Omega(r^2/p^2) Choi-program lower bound; fresh known classically adaptive probe reductions preserve the exponent with their explicit logarithmic overhead. Genuine coherent adaptive channel-query optimality remains separate.
