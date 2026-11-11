CRITICAL WEAK PACKETS, ACTUAL DECAY AND THE JOINT-MEMORY BOUNDARY
ROOT mathematical derivation, 11 November 2026

1. What changes, and what is inherited

The accepted finite-packet heat note10810/2184b383 already proves an actual
unforced coupled filter in the regime amplitude q^2, carrier Q=q^4, time
mu^{-1}q^{-7}. Its constant-H propagator, finite-tree frequency accounting and
two-norm rough-error estimate are inherited once, not new results here.

Here use amplitude Q sigma, with sigma small compared with mu but chosen
independently of Q. The natural high-frequency decay time can then retain a
quadratic slow velocity of order sigma^2. A critical Fourier estimate, instead
of a short-time amplitude estimate, controls the entire decay window uniformly
in its length. The result below does NOT implement packet preparation, an
unknown-velocity-preserving register restore or the entire response compiler.

2. Exact non-autonomous coupled propagator and a critical norm

On the unit three-torus write B=H+b with mean-zero u,b and use the actual
unforced coupled MHD equations. Unknown measurable nu,rho lie in[mu,1]. At each
nonzero Fourier frequency k, with lambda_k=2pi|k|, the linearized constant-H
matrix is
  -lambda_k^2 diag(nu I,rho I)+i(2pi H.k) offdiag(I,I).
The second term is skew-Hermitian, even when the two diffusivities differ or
vary in time. Thus the six-vector propagator satisfies
  ||S_k(t,s)||<=exp[-mu lambda_k^2(t-s)].                  (1)
No coefficient history or propagator is evaluated by an emitted programme.

For a pair V=(v,c), put
  ||V||X^r=sum_(k!=0) lambda_k^r (|vhat(k)|^2+|chat(k)|^2)^(1/2),
  ||V||E_T=sup_(0<=t<=T)||V(t)||X^(-1)
           +mu int_0^T ||V(t)||X^1 dt.
Fourier Cauchy--Schwarz gives
  ||V||X^0^2<=||V||X^(-1)||V||X^1,
  ||V||L2_t X^0<=mu^(-1/2)||V||E_T.                    (2)
All remaining MHD terms are quadratic divergences. The Leray multiplier has
norm at most one. For their bilinear Duhamel operator B(V,W), (1) and time
integration at each mode give
  ||B(V,W)||E_T<=C int_0^T ||V||X^0||W||X^0 dt
                <=C mu^(-1)||V||E_T||W||E_T.            (3)
C is a fixed computable constant including both equations and polarizations.
This uses the output derivative once, then its critical inverse weight; the
time-integrated X^1 bound uses int exp(-mu lambda^2 t)dt. There is no assumption
that the time-dependent coupled matrices commute.

3. An actual smooth-background plus weak-packet solution

Let Z0 be an unknown smooth mean-zero reference pair with supplied Fourier
envelopes P0>=||Z0||X^0, P1>=||Z0||X^1 and fixed Sobolev bounds P_s. Let p0 be
a prescribed finite mean-zero packet pair with ||p0||X^(-1)<=sigma. Put
  L(t)=S(t,0)Z0,  V=L+w.
The actual perturbation equation is
  w=S p0+B(L,L)+B(L,w)+B(w,L)+B(w,w).
The first forcing term has E_T norm at most C P0^2 T. The two cross terms have
operator norm at most C P0 sqrt(T/mu), by (2). Therefore for a fixed sufficiently
small computable c, the conditions
  0<sigma<=c mu,
  P0^2 T<=c sigma,
  P1 T<=1
give a contraction with ||w||E_T<=C sigma. Equivalently one may use explicit
safe rational caps with 1+P0,1+P1 in their denominators. In particular,
  int_0^T ||grad(u,b)||infinity dt
      <=P1 T+C sigma/mu<=C.                            (4)
The reference is a solution of the ACTUAL unforced coupled equations, not an
averaged induction equation or an assigned horizontal velocity. Smooth initial
data and the tame Sobolev energy inequality yield, for each fixed s>=4,
  sup_(t<=T)||(u,b)(t)||H^s<=C_s(P_s+||p0||H^s).         (5)
The exponent is bounded through (4), rather than by a power of the packet's
large amplitude. If Z0=0, the construction is global in time and the caps
involving P0,P1 are unnecessary. Constant H is included exactly and does not
enter the smallness condition on sigma.

4. Arbitrary-mode errors and admitted disturbances

Against the smooth actual reference, coupled L2 relative energy gives
  sup ||actual-reference||2<=C(e0+eta T),                (6)
for incoming joint L2 error e0 and mean-zero L-infinity-time/L2 disturbances
eta. It applies to energy-admissible weak realizations. The coefficient is
bounded by (4), not by exp(C Q sigma/mu).

For an incoming H1 error e1, differentiate the joint difference energy. The
highest coupled terms cancel; first reference derivatives multiply the H1
energy, while second reference derivatives multiply the ALREADY controlled
L2 error. With D2=sup||D^2 reference||infinity, one gets
  E1'+c mu||error||H2^2
   <=C G(t)E1+C D2 sqrt(E0 E1)+C mu^(-3)E1^3+C eta^2/mu,
where E0,E1 are squared error norms and int G<=C by (4). Young's inequality
with time scale T gives a constant exponential and hence
  sup||error||H1
   <=C[e1+T D2(e0+eta T)+eta sqrt(T/mu)]                 (7)
inside an explicitly polynomial small ball, for example after making the
right-hand bracket's fourth power times T mu^{-3} sufficiently small.
For packet frequencies <=JQ, (5) at fixed s=5 bounds D2 by
  C(P5+sigma(JQ)^6).
Thus all tolerances in (7) have polynomial reciprocal bounds in the stated
envelopes, mu^{-1}, J,Q,T,T^{-1} and accuracy. Large second derivatives are a
polynomial source term through E0, not a new exponential. Strong perturbative
continuation and same-data weak--strong uniqueness supply the all-weak
endpoint interpretation where H1 service composition is needed.

These are full-space perturbation bounds. They do not restrict a disturbance
to the packet frequency geometry.

5. Actual spectral clearing for pure finite packets

Now take Z0=0, u(0)=0 and
  b(0)=Q sigma sum_j (b_j exp(2pi i k_j.x)+conjugate),
  Q<=|k_j|<=JQ, k_j.b_j=0, sum_j|b_j|<=c0,
where a fixed rational c0 makes ||p0||X^(-1)<=sigma. The coefficient functions
b_j may be unknown register values; only their bounds enter the proof. This
is a PREPARED-state theorem, not a magnetic actuator or preparation algorithm.

The convergent homogeneous Picard series has n-leaf critical norm bounded by
  C sigma theta^(n-1),  theta=C sigma/mu<=1/4,
after choosing the universal smallness constant accordingly. Its n-leaf
frequencies are bounded by nJQ, so conversion from X^(-1) to X^1 costs at most
C(nJQ)^2. The entire tail after degree L therefore satisfies
  ||tail_(n>L)(T)||H1
      <=C(JQ)^2(L+1)^2 sigma theta^L.                   (8)
No tree enumeration is needed for this geometric majorant.

For an output |k|>=Q/2 in a tree with n leaves, every time slice has at most n
active edge frequencies whose vector sum is the output. Cauchy--Schwarz gives
sum_active |k_edge|^2>=Q^2/(4n). Factoring half of the parabolic decay and using
the other half for (3) bounds its additional decay by
  exp[-c mu Q^2 T/n].
Consequently the COMPLETE actual high output obeys
  ||P_(|k|>=Q/2)V(T)||H1
   <=C(JQ)^2 sigma [sum_(n=1)^L n^2 theta^(n-1)
                      exp(-c mu Q^2 T/n)
                    +(L+1)^2 theta^L].                (9)
This pays modes created during the interval, not only surviving initial heat.
Choosing L by an explicit logarithmic majorant and then a rational T of order
L log(poly(JQ,sigma,zeta^{-1}))/(mu Q^2) makes (9)<=zeta. Logarithms can be
majorized using integer bit lengths. All choices are finite and have fixed
polynomial bounds; L is a proof/computation of a geometric bound, not a demand
to enumerate exponentially many tree coefficients or solve a PDE.

On a fixed low band |k|<=F, the tail after the QUADRATIC term instead costs
only
  C(1+F)^2 sigma theta^2=O((1+F)^2 sigma^3/mu^2).        (10)
This follows directly from the critical norm and geometric tail, with no Q^2
conversion. Its leading quadratic velocity is the low-frequency Duhamel
Lorentz term of the exact coupled linear packet.

For H=0, its coefficient at a nonzero slow m is exactly
  i(2pi) Q^2 sigma^2 P_m sum_(k_j+k_l=m)
   [(b_j.m)b_l] int_0^T
     exp[-(2pi)^2 |m|^2 int_s^T nu]
     exp[-(2pi)^2(|k_j|^2+|k_l|^2) int_0^s rho] ds,       (11)
with ordered real-conjugate terms. For |H|<=M, use the exact coupled propagator
in that expression. Its difference from pure magnetic heat on high packets is
bounded by a polynomial multiple of M/(mu Q), through Duhamel of the
skew-Hermitian coupling. Low-output Alfven/heat changes are controlled by
MFT+F^2 T. No coefficient value or time integral in (11) is evaluated by the
programme. Unknown resistivity normalization is still a physical readout issue;
the earlier internal two-frequency signal is not silently a measurement.

The leading slow signal is order sigma^2, independent of increasing Q, whereas
the old amplitude-q^2 packet filter's slow velocity vanished like q^{-4}.
Many weak writes are therefore a plausible different cost allocation. Bounds
(8)--(11) do NOT by themselves prove their physical concatenation or a complete
unknown-even-velocity writer.

6. The exact remaining joint-memory and composition gaps

Equation (9) is proved for the pure-packet reference, not for an arbitrary
unknown smooth velocity already carrying an answer. Section3 gives existence
and stability WITH such a smooth background, but does not give its complete
low/high output separation or a uniform near-addition endpoint theorem. That
separation, packet preparation/routing and unknown normalization must still be
paid if this route is used. The pure-packet bounds do not erase a general
joint-memory gap by declaration.

Moreover, even a constant incoming-error factor multiplied once per weak cell
would become exponential in a variable number of cells. To obtain a variable-
degree compiler one needs actual absolute local near-assignment bounds on the
uniform logical register ball, a valid finite-rank/rebasing argument or another
global error estimate. Historical errors cannot be dropped at a proof-only
projection. The stable eleven-register Horner algebra does not itself provide
that physical operation. No variable-degree compiler follows from this note.

7. Governing sources and boundaries

ROOT refreshed Lei--Lin1203.2699v3 Theorem1.1 and proof(2.5)--(2.7) at
https://arxiv.org/pdf/1203.2699v3 . It is a whole-space, constant-viscosity,
small-X^(-1) Navier--Stokes theorem. The torus pair norms, non-autonomous
constant-H contraction, smooth-background decomposition and particular packet
output bounds above are derived here; they are not imported as an existing
unknown-history MHD theorem.

ROOT also read NEW DISTINCT Gerard-Varet's original go_roberts.pdf equations
(1.1)--(1.5), Theorems1.4--1.5 at
https://dgerardv.github.io/files/go_roberts.pdf . It fixes Re=Rm=1 and a specified
epsilon^{-1}U(epsilon^{-4}t,epsilon^{-2}x) velocity reference, with smooth
whole-space perturbations and profile/time-dependent constants. It proves
fixed-time stability and generic logarithmic-time dynamo instability at that
scope. It supplies neither twelve-actuator realization, arbitrary coefficient
histories, general rough disturbances nor universal polynomial resource
constants. No broader instability or compiler obstruction is inferred.

Both exact source accesses succeeded after completed local hold checks. No
alternate/version recovery or unavailable proof import occurred. No energy
trajectory was numerically simulated or packet filter experimentally run here;
the results are the displayed mathematical construction and bounds.
