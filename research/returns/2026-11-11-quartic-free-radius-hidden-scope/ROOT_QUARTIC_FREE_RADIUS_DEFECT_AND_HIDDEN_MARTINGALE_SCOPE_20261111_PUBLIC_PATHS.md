Free-radius affine defect and the scope of the hidden-martingale identity
11 November 2026 Brisbane / 10 November UTC

QUESTION AND PREMISES

For k>1/3, ell=3k-1,n=k+1, u=|F_1|^2,v=|F_2|^2,j=det F,
 J_k(F)=ell(ku-v+2j)^2/(8n)+ell uv/4+j^2.
The unrestricted original periodic quasiconvexity question is still open.
This note composes the available compatible four-mean estimate with its
scalar defect, and separately supplies sufficient hypotheses for the
displayed integrated fourth-moment identity. Neither operation proves the
original inequality or supplies an admissible negative.

The starting premises are the displayed constructions in the complete
7A567B final, .astra-dispatch/sources/Focused_allocation_20261103/
P1_PRO_7A567B_QUARTIC_RETURN_20261111.md, and the accepted periodic
Burkholder quasiconvexity theorem in Agazzi et al.,2609.28311v2,
https://arxiv.org/html/2609.28311v2, Theorem1/Corollary2. The latter
passages were refreshed directly: the torus has area one, the affine mean
is arbitrary, and the potential is a smooth real vector potential.
Fourth-order growth and strong W1,4 approximation extend the p=4 use.
No linked packet, component proof, code, audit or coefficient table is
imported. These are direct ROOT derivations from the stated premises,
not a new execution of producer calculations or an independent audit.

1. RETAIN THE FREE AFFINE RADIUS

Use complex columns G_1=p+h,G_2=i(p-h) for G=Dphi on the original torus.
Then p=B h, integral p=integral h=0, integral|p|^2=integral|h|^2.
Put R=[[0,-1],[1,0]], W(F)=F_1+RF_2, W(A)=2q,
 D=integral|q+h|^4-|q|^4,
 P=integral|p|^4, C=integral|h|^4,
 S=integral|h|^2, Q=|q|^4, a=|q|^2 S,
 b=integral[Re(conj(q)h)]^2, so a>=b>=0.

Let U(p,q)=27(3|q|-|p|)(|p|+|q|)^3/16. The accepted scalar majorant is
 81|q|^4-|p|^4-U(p,q)
 =(|p|-3|q|)^2(11|p|^2+66|p||q|+135|q|^2)/16.
For ANY r>=0 apply quasiconvexity to the SAME periodic potential at four
affine means (p0,q), p0=r omega q, omega in {1,i,-1,-i}. The four-point
average of the p part is P+4r^2 a+r^4 Q. Consequently
 P+4r^2 a <=81D+E(r)Q,                              (1)
 E(r)=(r-3)^2(11r^2+66r+135)/16.
The original four-mean result is exactly r=3. Formula(1) retains a whole
scalar envelope; no new field or moment oracle is supplied.

For t=r-3>=0, E(3+t)=27t^2+33t^3/4+11t^4/16, hence
 81D-P-36a >=24at+4at^2-Q(27t^2+33t^3/4+11t^4/16).
When Q+a>0 choose t=a/[4(Q+a)] in [0,1/4]. Since
 27+33/16+11/256=7451/256<30,
the right side is at least
 6a^2/(Q+a)-(15/8)Q a^2/(Q+a)^2
 >=(33/8)a^2/(Q+a)>=4a^2/(Q+a).
The zero case is defined continuously. We have therefore proved
 P+36a+4a^2/(Q+a)<=81D.                             (2)
The extra term can also be written 4|q|^2 S^2/(|q|^2+S), with value zero
at q=0. It retains a nonlinear interaction of affine mean and fluctuation
scale, rather than introducing another independent reserve.

2. A CORRESPONDING RETAINED COERCIVE BOUND

The exact fourth-power expansion and Cauchy--Schwarz give
 D>=y^2+2a, y=sqrt(C)-2sqrt(b).
Adding nine copies to (2) and using a>=b yields
 P+9y^2+54b+4a^2/(Q+a)<=90D.
Weighted Cauchy--Schwarz with weights(1,9,54) gives
 (sqrt(P)+sqrt(C))^2
 <=(32/27)[P+9y^2+54b].
This does not assume y>=0. Since
 integral|G|^4=4 integral(|p|^2+|h|^2)^2
 <=4(sqrt(P)+sqrt(C))^2,
we obtain
 Delta|W|^4=16D
 >=(3/80)integral|G|^4+(32/45)a^2/(Q+a).            (3)
The numerical3/80 term is the producer's bound; only the simultaneous
retained nonlinear defect is added here by varying the affine radius.

For k>1 and d=det A>=0 the producer's exact SAME-companion allocation is
 Delta J_k+sigma Vj
 =kappa Delta|W|^4+gamma_A S1
  +kappa(k^2-1)integral(du+2dj/(k-1))^2,
where sigma=n/[2(k-1)], kappa=ell/(8n),
 gamma_A=ell[(k-1)u0+2d]/4>=0,
 S1=integral|G_1|^2, du=|A_1+G_1|^2-|A_1|^2,
 dj=det(A+G)-d, Vj=integral dj^2.
Thus (3) pays the joint bound
 Delta J_k+sigma Vj
 >=3ell integral|G|^4/(640n)+4ell a^2/[45n(Q+a)]
   +gamma_A S1
   +kappa(k^2-1)integral(du+2dj/(k-1))^2.           (4)
One must NOT add (4) to another copy of the same W/companion reserve.
The complementary negative-determinant allocation can use the same
free-radius argument after the producer's paid anisotropic finite-torus
covering and target reflection; that transfer does not improve its k^-2
factor by assertion. No new torus-changing ansatz is required here.

These inequalities still do not pay sigma Vj for arbitrary actual
compatible fields. They do not extend that completion through k=1 or
settle 1/3<k<1. A useful comparison or concentration decomposition must
still involve the ACTUAL joint compatible moment cone.

For finite Fourier or piecewise-rational compatible input the extra
choice t uses a fixed number of rational moment operations, or explicit
error bounds for the supplied representation. An actual real W1,4 field
is handled mathematically by approximation, not a unit-cost moment
oracle. This note runs no optimization, field search, clipping, PDE
solver, stochastic simulation or external proof verification.

3. WHY THE INTEGRATED MARTINGALE FOURTH-MOMENT IDENTITY CAN HOLD

The displayed Wick-type identity in the return is NOT true for an
arbitrary continuous martingale with a random bracket. Here is a
sufficient spatial condition satisfied by the displayed smooth rotated
heat-gradient operation.

Let X_t=X_0+sqrt(2)B_t on the unit torus, with X_0 uniform and independent
of Brownian increments. Let V_0=0 in R^m and
 dV_i=g_i(t,X_t) dot dB_t,
where each smooth deterministic periodic row g_i(t,.) is divergence
free. Set a_ij=g_i dot g_j and Acal_ij(t)=integral_0^t a_ij(s,X_s)ds.
All finite-time coefficients are bounded; the following moment-density
computations therefore follow from Ito's formula and integration by
parts. Spatial integration in the producer's formula corresponds to
this uniform X_0. No conditional Gaussian assertion is needed.

Write m_i(t,x)=E[V_i(t)|X_t=x], with the uniform spatial density one.
It satisfies
 partial_t m_i=Delta m_i-sqrt(2)div g_i=Delta m_i,
and m_i(0)=0, hence m_i=0. The second moment density satisfies
 partial_t m_ij=Delta m_ij
  -sqrt(2)div(g_i m_j+g_j m_i)+a_ij=Delta m_ij+a_ij.
The bracket density z_ij=E[Acal_ij(t)|X_t=x] solves the same equation
and the same zero initial condition. Thus
 E[V V^T-Acal | X_t]=0.                            (5)

For fixed symmetric m by m matrices C,D, Ito's formula gives
 d/dt E[(V^T C V)(V^T D V)]
 =E[tr(CVV^T)tr(Da)+tr(DVV^T)tr(Ca)
     +4tr(CaD VV^T)].
Since a is a deterministic function of(t,X_t), (5) replaces VV^T here
by Acal. The resulting expression is the derivative of
 E[tr(CAcal)tr(DAcal)+2tr(CAcal D Acal)].
Indeed the two differentiated mixed trace terms agree by transposition
and cyclicity of trace, as C,D,a,Acal are symmetric. Both sides start
at zero. We have proved the integrated identity
 E[(V_T^T C V_T)(V_T^T D V_T)]
 =E[tr(CAcal_T)tr(DAcal_T)]
   +2E tr(CAcal_T D Acal_T).                       (6)

For the displayed hidden integral, each row is a scalar multiple of
 (partial_2 P_t G_i,-partial_1 P_t G_i), hence divergence free. This
checks the required spatial property for finite Fourier data on a
finite time interval. An infinite-time/rough-data passage additionally
needs the actual fourth-moment convergence and uniform integrability;
it is not a theorem about unrelated stochastic integrals. The return's
paid L4 construction is the available candidate for that passage.
Fixed initial x is not the uniform spatial average, and a general
adapted integrand does not have (5).

As a concrete scope check, let V_t=B_(t wedge tau) in one dimension,
tau the first exit time from(-1,1) starting at0. At infinity V^4=1,
whereas E tau^2=5/3. The exit equations are
 u''=-2,u(+-1)=0, u=1-x^2,
 v''=-4u,v(+-1)=0, v(0)=5/3.
Thus E V_infinity^4=1 is not 3E[V]_infinity^2=5. This also precludes
a universal finite-time identity, by stopping/time limits with finite
exit-time moments. It is not a counterexample to (6) under its stated
spatial hypotheses.

4. NO EXTRA SHARP-NORM RESERVE IS CREATED

The producer's common-affine-mean identity remains
 inf_A E Delta J_k(A,G_theta)
 =cos(theta)^2[c_G-b_G^T H_G^dagger b_G/2]
   +sin(theta)^2 E integral J_k(V_infinity).
It does not imply nonnegativity of the first parenthesis. Nor can the
infimum over one common A be interchanged with an expectation of
sample-dependent minima. Adding a conditionally null hidden variable
changes total and conditional covariance by compensating terms; it
does not improve their difference. The new scope derivation (5)--(6)
supplies a legitimate identity, not a new independent18c reserve.

The original all-k/all-mean/all-compatible-gradient question, an actual
negative realization, arbitrary total-Jacobian variance control, and
the sharp joint endpoint/area operation remain unresolved here.
