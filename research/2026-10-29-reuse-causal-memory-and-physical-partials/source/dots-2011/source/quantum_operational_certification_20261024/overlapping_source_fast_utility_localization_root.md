# Fast utility learning with overlapping reset: split the physical source, not the noise eigenbasis

2026-10-27. Root construction submitted for independent receiving. Separate extension of the received exact-source fast theorem; its original text is unchanged.

Let E(rho)=p V(rho tensor sigma)V*+q Tr(rho)tau, rank sigma<=r, arbitrary tau (no rank/orthogonality restriction). Write S for the genuine normalized-convention Bell Choi block, trace p; Pi is its support projector, rank<=r. Let O be the sum of the other eight known Weyl-orbit success Bell blocks, each trace p and mutually orthogonal. Let N=I_A tensor q tau. Then
 H=J-3omega=(2/3)S-(1/3)O-(2/3)N,
 A=J+3omega=A_c+A_n,
 A_c=(4/3)S+(1/3)O, A_n=(4/3)N.
Only A_c commutes with Pi. There is no claim that the full A commutes with Pi or is bounded by2|H|.

All feasible decoder SDP effects satisfy0<=F<=I and TrF<=r. Define L(F)=2p/3-TrHF. Direct expansion gives
 L(F)=(2/3)TrS(I-F)+(1/3)TrOF+(2/3)TrNF>=0.     (1)

## Two-decoder square-root localization
For the code part, use the four-block proof of low_trace_decoder_square_root_noise_localization_child.md relative to Pi. Its weighted misses now are
 l1=(4/3)TrS(I-F), l2=(1/3)TrOF,
 and l1+l2<=2L(F) by(1). Thus
 ||(F-Pi)sqrt(A_c)||_1<=4sqrt(rL(F)).
For any second feasible F_* with loss L_*, triangle/Cauchy gives
 ||(F-F_*)sqrt(A_c)||_1<=4sqrt(2r(L+L_*)).

For noise use F=F^(1/2)F^(1/2), Schatten Cauchy and TrF<=r:
 ||F sqrt(A_n)||_1<=sqrt[r TrA_n F]<=sqrt(2rL).
The same holds for F_*. Hence
 ||(F-F_*)sqrt(A_n)||_1<=2sqrt(r(L+L_*)).

Put D=F-F_*. The concatenated matrix [D sqrt(A_c),D sqrt(A_n)] has Gram matrix D A D*, the same as D sqrt(A). Its trace norm is therefore ||D sqrt(A)||_1. Applying the triangle inequality to its two padded blocks proves
 ||D sqrt(A)||_1 <=(4sqrt(2)+2)sqrt(r(L+L_*))
                  <8sqrt(r(L+L_*)).                 (2)
No full-source block diagonality, commutation, least eigenvalue, or rank(F) restriction is used.

## Transfer of acquired square-root noise
Suppose Hhat-H=sqrt(A)Z+Z*sqrt(A)+R, ||Z||<=z, ||R||<=b. For a feasible learned SDP solution within additive objective tolerance kappa, variational comparison with F_* gives
 L-L_* <=16z sqrt(r(L+L_*))+2rb+kappa.
Put U=L+L_*. Young's inequality yields
 U<=2L_*+U/2+128rz²+2rb+kappa,
 so
 L<=3L_*+256rz²+4rb+2kappa.                         (3)

The ACTUAL acquired pilot/filter routine from acquired_sylvester_filtered_fast_utility_child_theorem.md remains valid for arbitrary T,omega in this source model: T=A/4 and omega<=A, and none of its covariance, pilot, recentering or clipping steps used reset orthogonality. Only its old final deterministic localization used full-source commutation. Replace that step by(3).

On the same successful acquisition event, G<=(9/8)(A+tI), filtered error norm<=sqrt(t). Douglas factorization gives z²<=(9/8)t and b<=2sqrt(9/8)t. Consequently
 Lhat <3L_*+300rt+2kappa.                            (4)

The same deterministic ordinary-labelled copy cap and physical/computational resource limitations apply. In particular the general-n collective Keyl measurement is not known to have an efficient circuit; this remains a query theorem, not a cheap hardware implementation. No physical J copies are introduced.

## Concrete operational comparator and interpretation
The independently received recovery_utility_discrimination_equivalence_root.md supplies a feasible comparator with L_*<=2e(A_phys,Y), where A_phys=p V(I3/3 tensor sigma)V* and Y=q tau/3, for ANY reset rank. Therefore
 Lhat<=6e(A_phys,Y)+300rt+2kappa.
Combined with the received complete error bound6sqrt(3pLhat/2)+9Lhat, this gives fast reusable recovery whenever the actual discrimination error is small enough. The unknown Helstrom test is only an existence proof; the learned optimizer uses Hhat and the known trace constraints.

At t=nu²p0/(10^7r) and kappa<=rt, the acquired term is <=0.0000302nu²p. Thus the source-query accuracy rate is nu^-2 up to logarithms even with overlapping reset; approximation error from intrinsic source ambiguity is charged separately. Entropy sufficient conditions require the independently proved entropy-to-discrimination input, not an assumption about a whitened replacement source. Fixed-accuracy all-p lower comparisons do not establish a sharp accuracy lower against coherent adaptive queries.
