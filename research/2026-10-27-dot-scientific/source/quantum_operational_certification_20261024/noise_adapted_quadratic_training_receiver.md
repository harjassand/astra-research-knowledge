# Noise-adapted recovery with quadratic inverse-signal training

2026-10-27. New complete construction, pending independent receipt. It combines the noise-adapted Choi-discriminant guarantee with a population bound that does NOT assume that the target projector commutes with the individual program states.

## Theorem

For the fixed memoryless source E(rho)=pVrhoV*+qTr(rho)tau, p>=p0>0, define epsilon_ent=sqrt[5(p+3q)Delta] and assume epsilon_ent<=p/25. For any0<eps<=1, an explicit source-unknown instrument using ordinary discarded-label T/omega programs has complete UNHALVED diamond error at most

 eps p+50epsilon_ent                                  (1)

from(p/9 id,(1-p/9) erasure). All rejection and consumed training are charged. Its training count is at most

 131072 S^2/xi+2Lrm,                                  (2)

plus one data call, with

 xi=eps/2,
 L=max(1,ceil log_16[16/(p0 xi)]),
 eta=(xi/(100L))^2,
 M=2^m the least power of two with M>=768/p0,
 r=ceil log_2(1/eta),
 S=Lr pi(M-1)/2.

At fixed sufficiently small relative recovery error, the inverse-signal dependence is p0^-2 up to polylogarithms, while the sufficient entropy threshold is of order p^2. The exact-erasure adaptive-query lower bound applies to this constant-fraction-throughput task, so the inverse-signal exponent is worst-case optimal up to logarithmic factors. No optimal accuracy exponent, practical resource constant, unassisted capacity, or reusable decoder is claimed.

## 1. Received discriminant facts

Use H=4T-6omega=J-3omega. The received theorem in `source_unknown_chi_discriminant_noise_adapted_receiver.md`, including section6, gives its unique positive eigenprojector Pchi, eigenvalue lambda>=p/3, and a polar deficit e<=5epsilon_ent<=p/5. Put

 t=(2p/3-lambda)/p <=5e/(3p)<=1/3.

The IDEAL single Pchi Bell-contraction receiver has genuine-code complete error at most(5/2)pt<=25e/6 from the p/9 target after weighting by p. For a normalized reset datum the initial Pchi population r0 obeys

 q r0=(q/3)<chi|I3 tensor tau|chi> <=pt/2<=5e/6.       (3)

The actual sample programs have small weight on Pchi, even though they need NOT commute with it:

 Tr(Pchi omega)<=p/9+5e/6<=5p/18,
 Tr(Pchi T)=[lambda+6Tr(Pchi omega)]/4<=7p/12.

In particular both weights are at most p. Also [Pchi,H]=0. No Pchi or original-code projector is supplied as an available gate.

## 2. Actual repeated spectral classifier

Run L fresh nondestructive QPE classifiers for H, keeping the target after every result. The QPE phase, threshold, M and majority-r rule are exactly those in the discriminant theorem: exp[i pi(H+I)/2], threshold1/4+p0/24, accepted interval ending at3/4. Each ideal-evolution classifier has false-pass and false-fail probability at most eta.

Accept only if ALL L classifiers accept; otherwise erase. The receiver may stop on the first negative result, but the worst-case budget(2) pays every allocated program. Each controlled H-time t_a=(pi/2)2^a is simulated using

 N_(t_a)=ceil[65536 t_a S/xi]

rounds. A round consists of a controlled T partial-SWAP with angle4delta followed by a controlled omega partial-SWAP with angle-6delta, delta=t_a/N_(t_a). The distinct4,-6 simulation bound from the received theorem is256t_a^2/N_(t_a). Hence total simulation error<=xi/256, and for one classifier it is at mostxi/(256L). The sum of delta^2 over all signed rounds is at mostxi/65536; for one classifier it is at mostxi/(65536L). In particular |delta|<=1.

The accepted-only CP branch for ideal evolutions has target probability at least1-Leta and complementary probability at mosteta^L. The rank-one accepted-coherence estimate, followed by erased rejection, bounds its complete error from the exact Pchi instrument by

 2Leta+2eta^L+4eta^(L/2) <=4Leta+4sqrt(eta)<xi/2.

Adding the simulation error gives complete learned-filter error at mostxi. This generic bound will be applied only to the genuine data branch of weight p. A separate, stronger reset bound follows below.

## 3. Population estimate for a signed pair, without sector pinching

Here P denotes Pchi, sigma=T and rho=omega; w=max(Tr P sigma,Tr P rho)<=p. Let a=4delta,b=-6delta. The uncontrolled partial-SWAP adjoint is exactly

 C_(sigma,a)^*(X)=cos^2(a)X+sin^2(a)Tr(sigma X)I
                  -i cos(a)sin(a)[sigma,X].

For a controlled collision, the Heisenberg observable I_control tensor P has control-0 block P and control-1 block equal to this expression. Two signed collisions use the same control, so their population analysis reduces to C_(sigma,a)^* C_(rho,b)^*(P). This statement holds as an operator inequality and therefore allows arbitrary joint auxiliary/reference states.

Write c_a=cos a,s_a=sin a and likewise for b. Direct expansion gives

 c_a^2 c_b^2 P +(c_b^2 s_a^2 w_sigma+s_b^2 w_rho)I
 -i c_b^2 c_a s_a[sigma,P]-i c_b s_b c_a^2[rho,P]
 -i c_b s_b s_a^2 Tr(sigma[rho,P])I
 -c_b s_b c_a s_a[sigma,[rho,P]].                      (4)

The first-order commutators cancel because a[sigma,P]+b[rho,P]=delta[H,P]=0. Positivity of the program states gives the operator estimates

 +/- i[sigma,P] <=P+wI,
 +/- i[rho,P] <=P+wI,
 +/- [sigma,[rho,P]] <=P+3wI,
 |Tr(sigma[rho,P])|<=2w.                              (5)

For example sigma P sigma<=Tr(Psigma)sigma<=wI. The terms sigma rho P+P rho sigma are bounded above and below by P+wI using the square of P minus/plus sigma rho P; the remaining cross terms are bounded by sigma P sigma+rho P rho<=2wI. The scalar trace bound follows from Hilbert-Schmidt Cauchy-Schwarz on P sigma and P rho.

The coefficient remainders satisfy

 |c_b^2 c_a s_a-a|+|c_b s_b c_a^2-b|
 <=(1280/3)|delta|^3.

This follows from |sin u cos u-u|<=(2/3)|u|^3 and sin^2 u<=u^2. The remaining identity coefficient is at most52w delta^2, the double commutator coefficient at most24delta^2, and the scalar trace term at most192w|delta|^3. Dropping the negative change in c_a^2 c_b^2 P and using |delta|<=1 yields the conservative received inequality

 K^*(I_control tensor P)
 <=(1+800delta^2)(I_control tensor P)+800delta^2 p I.   (6)

No actual or virtual measurement of P is inserted. In particular, (6) remains valid when the data has coherent off-diagonal P/complement blocks.

## 4. A two-variable accepted-mass recurrence

Known control/phase gates preserve I_control tensor P. Compose(6) throughout one complete classifier, and set

 v=800 sum_rounds_in_classifier delta^2 <=xi/(80L),
 a0=exp(v), b0=p(exp(v)-1)<=p xi/(40L).

For an arbitrary positive, possibly subnormalized input with total mass m and P-population r, the total output P-population is at mosta0 r+b0 m. Selecting the accepted outcome can only decrease that population.

The ideal classifier's acceptance effect is at mostP+eta I. Its actual simulation error therefore gives accepted mass at most r+beta0 m, where

 beta0=eta+xi/(256L)<xi/(200L)<=1/16.

Consequently the positive accepted-state sequence satisfies, WITHOUT any block-diagonality assumption,

 r_(k+1)<=a0 r_k+b0 m_k,
 m_(k+1)<=r_k+beta0 m_k.                              (7)

Take m0=1 and arbitrary r0. Let Rmax=max_(0<=k<=L)r_k. Iterating gives

 Rmax<=a0^L[r0+b0 sum_(j=0)^(L-1)m_j],
 sum_(j=0)^(L-1)m_j<=[1+L Rmax]/(1-beta0).

Since a0^L<=exp(1/80)<=80/79 and b0L<=1/40, the coefficient of Rmax on the right is less than1/16. It follows, conservatively, that

 Rmax<=2r0+4b0,
 m_L<=3r0+5b0+beta0^L.                               (8)

For the second inequality one can retain the slightly sharper intermediate bound Rmax<=2r0+3b0, obtained from1/(1-beta0)<=16/15, and then use m_L<=Rmax/(1-beta0)+beta0^L. All bounds are uniform over the coherences and retained auxiliaries of the accepted state.

The chosen L ensures beta0^L<=p0 xi/16<=p xi/16. Thus a reset datum's final accepted mass, after its original source weight q is included, obeys by(3) and(8)

 q m_L<= (5/2)e +3p xi/16.                           (9)

The term proportional to p comes from the actual small Pchi weights of the training programs, not an assumed projection onto an unknown code sector.

## 5. Complete original-source receiving

On genuine encoded data, the ideal noise-adapted filter contributes at most25e/6 complete error by the received positive-resolvent argument. Its learned implementation adds at mostp xi. On reset data, the final classical accepted/erased output differs from erasure by exactly twice the accepted mass(9). Therefore

 total error <=25e/6+p xi+5e+3p xi/8
             =55e/6+11p xi/8
             <=50epsilon_ent+eps p.

This proves(1). For any desired relative error0<nu<=1, choose eps=nu/2 and require epsilon_ent<=nu p/100. Then total error<=nu p, with sufficient entropy condition

 Delta<=nu^2 p^2/[50000(p+3q)].

The target identity contribution remains p/9. To claim a useful nonzero fraction of that throughput, nu must be correspondingly small; the always-erasing strategy has error2p/9. For fixed nu below the complete-recovery lower-bound threshold, the worst-case p^-2 lower bound and this upper bound have the same signal exponent, up to logarithmic factors.

All training samples are ordinary mixed programs and are consumed. Data is independent of training conditional on one fixed stationary memoryless source. The statement neither verifies this promise nor guarantees performance for hidden-memory channels, every public training transcript, or unspecified conditional postselection.
