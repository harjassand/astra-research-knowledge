# Known-matrix recovery synthesis without a spectral-gap promise
2026-10-29. Additive finite-control clarification; original governing file preserved. The square-root/isometry idea was suggested by receiving reviewer sharpen; the public arithmetic bounds below are supplied by the author for checking.

Let h=kd and let J' be the exact rational PSD/TP recovery Choi. Fix0<e<=1/4, eventually e<=gamma_rec/8. Let B=sqrt(J'). Its h columns reshape into Kraus operators L_i:k×d; stacking those Kraus operators gives a Stinespring matrix V:k*h by d with V†V=I_d. Reshaping is a Frobenius isometry.

## Explicit bounded square-root algorithm
Set tau=e²/(4h), M=(d+1)² and A=(J'+tau I)/M. Since ||J'||op<=TrJ'=d, the spectrum of A lies in[mu,1], where mu=tau/M. Regularization changes the square root in Frobenius norm by at most sqrt(h*tau)=e/2.

For exact arithmetic define T0=I and T_(j+1)=(3T_j-T_j A T_j²)/2. These exact matrices commute with A. For each eigenvalue a of A, y_j=a t_j² lies in(0,1], and1-y_(j+1)=(1-y_j)²(3+(1-y_j))/4<=(1-y_j)². Thus1-y_j<=exp(-mu*2^j), and the Frobenius error of (d+1) A T_j as an approximation of sqrt(J'+tau I) is at most sqrt(h)*(d+1)*exp(-mu*2^j).

Choose m as the least integer with2^-m<=e/[4h(d+1)], then choose j with2^j>=m/mu. Both choices use rational integer comparisons; j=O(log(hd/e)). The exact iteration error is at most e/4.

To prevent exact rational denominator growth, round/symmetrize every T update to a public dyadic grid with Frobenius rounding error at most
 eta=e/[8h(d+1)*j*L^j], where L=12/mu².
On the operator-norm ball ||T||<=2/sqrt(mu), the update is Lipschitz with constant at mostL. The accumulated operator error is at most j L^j eta=e/[8h(d+1)]<1. This bound in turn keeps every rounded iterate in that ball, since exact ||T_j||<=1/sqrt(mu). Symmetrization does not enlarge the error relative to the Hermitian exact iterate. The resulting square-root output error adds at most e/8 in Frobenius norm. Thus the final rational Bhat satisfies ||Bhat-B||F<e. All dyadic bit lengths are polynomial in log(1/e), log h and log d: log(1/eta)=O(j log(1/mu)+log(jhd/e)). Matrix multiplication and rounding therefore have a public polynomial bit-operation budget, not an unbounded iterative stopping test.

## Well-conditioned physical isometry
Reshape Bhat into Vhat. Then ||Vhat-V||op<=||Vhat-V||F<e, so all singular values of Vhat lie in[1-e,1+e]. The known polar correction
 Q=Vhat(Vhat†Vhat)^(-1/2)
is an exact isometry. Its inverse square root is well-conditioned (e<=1/4), independently of the spectrum of J' or the unknown source. Also ||Q-Vhat||op<=e and ||Q-V||op<=2e. Hence the induced recovery channels differ in full diamond norm by at most4e. Compute/compile the known Q to a further declared error using bounded inverse-square-root arithmetic and standard known-isometry Givens completion; this is a small classical matrix problem with total Stinespring dimension k²d. Taking e<=gamma_rec/8 leaves at least half of a full-diamond budget gamma_rec for that final synthesis.

No inverse or purification of the unknown source appears. This is a theoretical finite synthesis algorithm; the packet's executable tests verify algebra/fixtures, not a compiled arbitrary recovery circuit.
