# Couple collective transport while leaving two density histories free

30 October 2026. Root construction. The physical task is more selective than
blocking all transport or obtaining some useful relaxation: link two net
currents, retain a common channel for load transfer, and retain each system's
independent nonflat heat density history. The actual realization uses a local
signed ladder of reciprocal wave ports. Conventional tight coupling and passive
networks are direct predecessors; priority for this composition is unresolved.

## 1. Native ports and the controller we build

There are two colocated periodic native rings with N sites. Their native
carrier channels remain separate. Visible x_1,x_2 are signed harmonic densities
with zero sum, not exclusion occupations. Put `(B_N j)_i=j_(i-1)-j_i` and

    B=diag(B_N,B_N), R=diag(r_1 I_N,r_2 I_N),
    0<r_-<=r_1,r_2<=r_+.

The native resistances may be unknown frozen values. Actual current response,
load and temperature-one noise are

    dx=Bv dt,
    tau dv=-(B^*x+g_N q)dt-Rv dt+f_N(t)dt+sqrt(2R)dW.       (1)

Here tau>0 is fixed. The reciprocal local tap into q and its reaction -g_N q
are supplied matched ports. They do not follow from equilibrium weights.
W has independent components in the two native systems.

Build the local 3N-by-2N matrix

    A = [[ B_N,     0 ],
         [   0,  -B_N ],
         [ I_N,   I_N ]].                                 (2)

The first two row blocks connect neighbors along each memory ring; the last
connects colocated cells across rings. Thus range and degree are bounded.
This is a ladder incidence after reversing the second ring's memory polarity:

    ker A=span{h_N}, h_N=(1_N,-1_N)/sqrt(2N), B h_N=0.       (3)

Run the actual controller

    dq=(g_N v-a A^*p)dt,
    dp=(a A q-gamma A A^*p)dt+sqrt(2gamma)A dV,              (4)

with fixed a>0, gamma>=0 and independent same-temperature local bath V.
Relative-momentum damping is structural. Grounded loss is a different port.
The actual native current is `J_a,tot=sum_i int v_(a,i)dt`, counting all
reaction motion. Apparatus transport is a separate declared channel.

Write kappa_N=g_N^2 and assume

    kappa_N ->0,       N^2 kappa_N ->infinity.               (5)

Every local native/wave coefficient is bounded; the tap becomes weak and pays
accuracy/compliance and range. Gaussian coordinates are not a hard-capacity
apparatus. Native current has finite response tau/r_a, while the mathematical
voltage baths use white noise. The separate finite-duration rotation program
supplies a different isolated bath interface; it is not composed through an
unknown resistor by inference.

## 2. Invariance, preparation, and the selected counter

For E=(||x||^2+||q||^2+||p||^2+tau||v||^2)/2 all conservative transfers cancel.
The dissipations v^*Rv and gamma||A^*p||^2 have their matched noises. At f=0 the
exact invariant law is independent unit Gaussians for x on the two fixed-mass
spaces, q,p, and covariance tau^(-1)I for v. Conserved p directions in ker A^*
decouple and may be fixed. Time reversal flips p,v; identity reversal is not
a self-adjoint symmetry.

For the nonflat theorem prepare deterministic x_N^0 sampling two smooth
zero-mean profiles rho_(a,0), total energy at most CN, and independent thermal
q,p,v. This is an actual conditional preparation, not postselection on a fully
retained thermal realization. A thermal visible initializer has its own static
large-deviation cost. Any retained old record must warrant the same conditional
preparation and future bath law.

On every actual trajectory,

    J_1,tot(t)-J_2,tot(t)
      =sqrt(2N)/g_N [h_N^*q(t)-h_N^*q(0)].                 (6)

The common current is not a counter endpoint and may grow indefinitely.
The difference of local density profiles is not conserved: the wave term
transports the counter memory. No microscopic copying is proposed.

## 3. Both nonflat density histories remain ordinary and independent

Let F=B A^dagger, with the Moore--Penrose inverse used only in the proof.
Since ker A is contained in ker B, F A=B. At Fourier eigenvalue ell of B_N^*B_N,
A^*A has eigenvalues ell+2 on the common-ring combination and ell on the
difference combination. Consequently

    ||F||<=1,       F A A^* F^*=BB^*.                      (7)

No nonlocal F sensor is used by the apparatus. Combining actual equations gives

    R_x dx=-BB^*x dt-tau d(Bv)-(g_N/a)F dp
            -(g_N gamma/a)F AA^*p dt
            +sqrt(2R_x)B dW+(g_N/a)sqrt(2gamma)B dV,        (8)

where R_x has the same two constant blocks as R. Couple reference densities to
the same mathematical W and initial x_N^0:

    dy_a=-(1/r_a)B_N B_N^*y_a dt+sqrt(2/r_a)B_N dW_a.       (9)

These reference laws are independent. This proof coupling does not physically
branch one specimen. For a unit Fourier vector f in one density ring, put
w=F^*f. Then ||w||<=1 and w^*(gamma AA^*)w=gamma ell. The actual stationary
forward/backward martingale identity gives

    E |int_0^t <gamma AA^*w,p_s>ds|^2<=2t gamma ell.        (10)

Indeed, for h=<w,p> its symmetric generator is Sh=-<gamma AA^*w,p>.
The forward and adjoint backward martingales sum to twice the displayed
integral, and each has expected square 2t gamma ell. Cauchy--Schwarz proves
(10), without mixing. Conditioning deterministic initial x reduces the centered
covariance of this linear path functional.

The Fourier difference from (9) obeys a scalar Volterra equation with decay
ell/r_a. The source in (8) consists of two endpoint momenta, (10), and the
controller martingale. Uniformly for physical t<=N^2T its centered second moment
is bounded by

    C_T[ell+kappa_N(1+N^2 ell)].                            (11)

The Volterra resolvent has L1 norm at most one. Thus (11), up to factor four,
bounds the difference at each time and vanishes for every fixed macroscopic
Fourier index. For the deterministic mean, energy contraction tested by
f/sqrt(N) bounds the native endpoint by O(sqrt(ell)), the auxiliary endpoint by
O(g_N), and the loss integral by C_T g_N N sqrt(ell). They vanish too.

The native matrix impedance has real part at least r_-I, giving the thermal
spectrum S_v=2 Re Y <=(2/r_-)I and the increment bound

    E |<f,x_t-x_s>|^2 <=(2 ell/r_-)|t-s|.                  (12)

Gaussian moments, Sobolev summation, and compact embedding give joint path
tightness on the macroscopic clock in C([0,T],H^(-s)), s>3/2. Conditioning only
reduces covariance. Energy/Fourier tails treat smooth nonflat means. Together
with (11), the coupled centered difference converges to zero in this path space.
For a tight Gaussian sequence converging to zero, a common Fernique bound
makes its expected norm and weak variance tend to zero. Borell's inequality
therefore makes the macroscopic difference (divided by sqrt(N)) superexponentially
small at speed N. This step is specific to the exact Gaussian path laws.

Thus the two complete density histories are exponentially equivalent to
independent native heat histories, with respective deterministic receivers

    partial_t rho_a=(1/r_a)partial_x^2 rho_a.               (13)

Their two limiting centered fluctuation fields are independent conservative OU
fields, started at zero for the specified deterministic visible initializer.

## 4. The common current remains a stochastic transport channel

Translation invariance makes the harmonic mode independent of every density
mode in this Gaussian model. In the normalized common/difference basis
s=(1,1)/sqrt(2), h=(1,-1)/sqrt(2), put

    rbar=(r_1+r_2)/2,       rdiff=(r_1-r_2)/2.

The exact harmonic native impedance is

    Z_0(omega)=[[rbar+i tau omega+c_2(omega), rdiff],
                [rdiff, rbar+i tau omega+kappa/(i omega)]],
    c_2(omega)=kappa(i omega+2gamma)
                      /(2a^2-omega^2+2i gamma omega).      (14)

The unknown native mismatch is retained. For fixed nonzero Omega and
omega=Omega/N^2, conditions (5) give

    Z_0(omega)^(-1) -> diag(1/rbar,0).                     (15)

The passive bound S_v<=2/r_- is uniform at all frequencies. In the spectral
covariance formula for integrated current, the scaled integration kernels
are products of (exp(i Omega t)-1)/Omega. Their product is integrable.
Dominated convergence and (15) therefore give

    (J_1,tot(N^2t),J_2,tot(N^2t))/N^(3/2) => (Z_t,Z_t),
    Z_t=sqrt[2/(r_1+r_2)] W_t.                            (16)

The integrated-current variance bound is linear in macroscopic elapsed time;
Gaussian fourth moments give tightness in continuous-path topology. The
limiting Brownian motion is independent of both density fields.

The counter supplies a stronger selected-current tail. Its variance is at most
8N/kappa_N. The passive increment bound and Gaussian entropy integral give

    E sup_(t<=N^2T)|J_1,tot(t)-J_2,tot(t)|
       <=C_T sqrt[(N/kappa_N)log(2+N^2 kappa_N)].            (17)

The unforced harmonic mean is zero even for the nonflat visible preparation.
Borell's inequality and (5) make the probability of a difference exceeding
epsilon N^2 anywhere on the horizon superexponentially small at speed N.
The common current in (16) retains its ordinary unbounded Brownian scale.

## 5. Full joint action and the independent-density consequence

Define empirical density and integrated-current fields

    rho_(a,N)=N^(-1)sum_i x_(a,i)(N^2t)delta_(i/N),
    W_(a,N)=N^(-2)sum_i J_(a,i)(N^2t)delta_(i/N).

Exact continuity reconstructs each nonconstant current mode from the density
change by a discrete inverse gradient. The inverse multipliers converge in
the weak Sobolev path topology. Sections 3-4 give the joint Gaussian fluctuation
limit and exponential tightness. The Gaussian LDP (or quadratic finite-projection
moment-generating functions plus exponential tightness) supplies the speed-N
good rate

    I(rho_1,rho_2,j_1,j_2)
       =sum_(a=1,2)(r_a/4) int_0^T int_0^1
                       [j_a+(1/r_a)partial_x rho_a]^2 dxdt, (18)

on

    partial_t rho_a+partial_x j_a=0,
    rho_a(0)=rho_(a,0),
    integral j_1(t,x)dx=integral j_2(t,x)dx  a.e. t,        (19)

and infinity otherwise. W_a(t)=int_0^t j_a(s)ds is the measured current path.
Finite action is the weak controlled-PDE/Cameron--Martin image of an L2
control, rather than a formula defined only on smooth paths.

Indeed, write j_a=j_a^perp+I(t), with zero-mean j_a^perp. The independent density
costs are the two ordinary native ones. The common Brownian mode contributes
((r_1+r_2)/4)int I^2dt by (16), exactly giving (18). Contracting over current
sets I=0 and leaves the sum of the independent heat density actions. The local
operation thus changes joint transport without locking spatial density profiles,
including their rare histories at this Gaussian precision objective.

## 6. Actual load response, work, and the forced action

Supply spatially uniform physical forces f_(a,i)(s)=F_a(s/N^2)/N, with F_a in
L2([0,T]), extended by zero to the past. These are actual native force ports
in (1), with work sum_i f_i v_i ds. A likelihood tilt is not an actuator.
The forces act only on the harmonic block, so density laws are unchanged
exactly. The scaled transfer functions (14)-(15) converge to

    I_0(t)=[F_1(t)+F_2(t)]/(r_1+r_2).                      (20)

They are uniformly bounded by passivity. Plancherel and dominated convergence
give L2 convergence of the macroscopic mean currents, hence uniform convergence
of their integrals on finite horizons. This accounts for the actual initial
charging transient: all auxiliary means start at zero. A compactly supported
force is not called strictly band limited.

Deterministic forcing leaves covariance unchanged. The forced rate is the
same two density costs plus

    ((r_1+r_2)/4) int_0^T [I(t)-I_0(t)]^2dt.               (21)

Merely restricting the original forced native action to equal currents would
add the spurious constant F_1^2/(4r_1)+F_2^2/(4r_2)
-(F_1+F_2)^2/[4(r_1+r_2)] at each time. The actual rate has minimum zero at
(20). This distinguishes a physical constraint law from an unnormalized
restriction of a path weight.

For constant F_1>0>F_2 with F_1+F_2>0, the first force drives common transport
against the second. On horizon N^2T, the mean input/output work per N tends to

    W_in/N=T F_1 I_0,       W_out/N=-T F_2 I_0,
    (W_in-W_out)/N=T(r_1+r_2)I_0^2.                        (22)

The ratio -F_2/F_1 is ordinary tight-coupling efficiency at this declared
isothermal native work interface. It is not a new thermodynamic relation,
apparatus-inclusive efficiency, or a power guarantee for unbounded friction.
At finite-size unscaled DC and gamma=0, each current per bond is exactly
(f_1+f_2)/(r_1+r_2). With conservative gamma the denominator becomes
r_1+r_2+2kappa gamma/a^2. The protected difference is blocked at DC while the
common channel remains conducting.

The limiting low-frequency common-current spectrum per averaged ring is
2/[N(r_1+r_2)], with the same positive cross-spectrum. Response and noise
change together; the difference channel's DC susceptibility is removed.
There is no passive precision gain at unchanged response.

## 7. Same-task alternatives and boundaries

- A direct pointwise gear v_(1,i)=v_(2,i) locks x_1-x_2 at every site. It
  supplies common transport but fails independent nonflat density histories.
- A constraint at one cut or a series connection can couple boundary fluxes,
  but changes the native periodic density boundary problem. It is a valid
  alternative at a different supplied state/transport interface.
- An instantaneous global projector onto the allowed harmonic-current
  subspace supplies the desired Gaussian law directly. This is the ideal
  constrained Langevin/Onsager comparison, with an actual nonlocal port.
- Conventional reciprocal wave hardware supplies (1)-(4). The addition here
  is its selective whole-history receiver, independent-density property,
  hidden-rate scope, and matched response/noise accounting. An ordinary
  designer supplied with these same ports can implement it; no advantage over
  that equally informed consumer is asserted.

Topology selects what is coupled. Native kinetics still determine conductivity
and power. Arbitrary spatially varying native resistance is outside unchanged
density scope; it has the metric receiver in `LOCAL_PASSIVE_LAW_REALIZATION.md`.
A mixture over hidden r values is not itself Gaussian. Apply this result
conditionally on each warranted frozen value and actual old record; do not
inherit a fixed-r large-deviation rate by averaging.

Spatially nonuniform tap errors or leakage of q into an uncontrolled reservoir
alter the counter. Their actual event/flow residual must be counted. A bounded
coefficient, a finite response, and a hard bandwidth or amplitude cap are
different specifications. No apparatus, finite-data confidence event, nonlinear
exclusion action, or practical speedup is proved here.

## 8. Close primary machinery

The proof uses established Gaussian and passive-network machinery. Paolo Baldi,
*Tightness and exponential tightness of Gaussian probabilities*, ESAIM:PS24
(2020),113-126, https://doi.org/10.1051/ps/2020003, is a direct primary theorem
for the Gaussian step. Freitas--Delvenne--Esposito, PRX10,031005(2020),
https://arxiv.org/abs/1906.11233, gives the close stochastic RLC framework.
Lelievre--Rousset--Stoltz, https://arxiv.org/abs/1006.4914, treats matched
metric-constrained Langevin dynamics. Ordinary tight coupling and its force
balance were already credited and preserved in continuation8, including
Lipowsky--Liepelt and the Utsumi one-bit comparison. None of that credit is
withdrawn by changing the architecture. The new particle-field attack has its
own close Maggs--Levrel predecessor and is not completed by this Gaussian law.
