# Complete nonlocal transport action from event memory

30 October 2026. Root receiving construction. The key new dependency is the
actual weighted-current correction in
`record_geometry/INVERSE_ACTIVITY_AND_WEIGHTED_CORRECTOR.md`. The independent
reference action, its path topology, energy identification and smoothing methods
remain the established machinery preserved in continuation7. This file supplies
the previously missing corrected spatial-tilt receiver and its action argument.

## 1. Actual operation and theorem

On an even N-site exclusion ring write delta_i=eta_i-eta_(i+1), a_i=delta_i^2,
A=sum a_i, c=s/2, and p(eta)=(-1)^(sum_i i eta_i). There is one shared bit u.
Every native active exchange flips u atomically, at physical rate

    r_i=c(1+alpha u delta_i),  0<=alpha<1.                  (1)

An actual external clock flips u without moving eta, at physical rate gamma_N.
Equivalently use sigma=u p(eta): native exchanges leave sigma fixed and the
clock flips it. The warranted regime is

    N gamma_N -> infinity,   gamma_N/N -> 0.               (2)

A fixed positive physical clock is included. Zero clock and alpha=1 are not
included in this action theorem. They retain their separate exact current
results, not the uniformly elliptic receiver used here.

Observe the persistent specimen for physical time N^2 T, T fixed. Let
pi_t^N=N^-1 sum eta_i(N^2t)delta_(i/N), and
W_t^N=N^-2 sum J_i(N^2t)delta_(i/N), using actual signed native currents.
The actual initial occupancy is any deterministic sequence associated with
the flat profile m in (0,1); the initial bit may be fixed and recorded.
The full future native-and-clock conditional law must remain (1)--(2).
Uniformity across families of initial sequences requires a common association
modulus. Random initial profiles carry their own initial large-deviation cost.

In the same D([0,T],H^-3 x H^-3) path space as the accepted reference theorem,
with continuous limiting support, the speed-N density/current action is

    I_alpha(rho,j)=(1/(2s)) int_0^T {
       int [j+c rho_x]^2/chi(rho) dx
       +[alpha^2/(1-alpha^2)] (int j dx)^2 / C_rho }dt,
    chi(rho)=rho(1-rho), C_rho=int chi(rho) dx,              (3)
    rho_t+j_x=0, rho(0)=m, W_t=int_0^t j_v dv.

The primary definition is the variational one below. The quotient has its
usual lower-semicontinuous convention at zero denominator. A finite-action
path has C_rho>0 at almost every time by interior mass and spatial energy.
The new term is nonlocal in space. At alpha=0 this is the reference action.

## 2. Covariance form and the actual-current correction

For smooth H set A_H=sum H_i a_i, S_H=sum H_i delta_i, F_H=A_H/A. On an active
native edge define d_i(H)=H_i delta_i-alpha u F_H. The base compensated sum

    K_H=sum_native d_i(H)-int c S_H dv                     (4)

is a martingale. Its exact cross-bracket rate with K_E is

    sum_i r_i d_i(H)d_i(E)
      =c[A_HE-alpha^2 A_H A_E/A]
        +c alpha u[S_HE-F_E S_H-F_H S_E].                 (5)

For smooth fields every S term is O(1). The weighted-corrector dependency proves,
uniformly on each fixed macroscopic horizon and at speed-N superexponential
accuracy,

    N^-2 J_H(N^2t) = N^-2 K_H(N^2t)
                         +c int_0^t S_H(eta_(N^2v))dv+o(1). (6)

It proves (6) both in the actual law and after any bounded predictable weak
native tilt |q_i|<=K/N. This is essential: the original current, not a substitute
mathematical observable, enters (3). The proof pays for low activity with an
inverse-activity energy/compactness estimate, rather than a typical-state bound.

The limiting quadratic form is

    M_rho(H,E)=s[ int chi(rho) H E
           -alpha^2 (int chi(rho)H)(int chi(rho)E)/C_rho ]. (7)

At C_rho=0 define it as zero. Positivity and coercivity follow from weighted
Cauchy--Schwarz:

    s(1-alpha^2)int chi H^2 <= M_rho(H,H) <= s int chi H^2. (8)

## 3. Comparison tilt and a rigorous nonlinear receiver

For fixed smooth deterministic E(t,x), change the native comparison rates to

    r_i^E=r_i exp[d_i(E)/N],                              (9)

leaving the clock unchanged. This is a likelihood construction, not an asserted
physical force port. Since |d_i(E)|<=(1+alpha)||E||, its likelihood has second
moment exp(O(N)); all superexponential replacements transfer by Cauchy--Schwarz.

Under (9), the base-compensated K_H has additional physical drift

    sum_i r_i(exp[d_i(E)/N]-1)d_i(H)
       =N^-1 sum_i r_i d_i(H)d_i(E)+O_(E,H)(N^-1).         (10)

The compensated martingale divided by N^2 has macroscopic bracket O(1/N).
Use (5), occupation replacement and (6). Every subsequential limit satisfies

    j=-c rho_x+s chi(rho)[E-alpha^2 q_E(rho)],
    q_E(rho)=(int chi(rho)E)/C_rho,                       (11)
    rho_t=c rho_xx-s partial_x{chi(rho)[E-alpha^2 q_E(rho)]}.

Where C_rho=0 set q_E=0; always |q_E|<=||E||. There is no unjustified division
by a rare small activity in this step. For positive measures a, the function
(int H da)(int E da)/(int da), set to zero at zero mass, is continuous and
globally Lipschitz in the three moments on their natural cone
|int H da|<=||H||int da, |int E da|<=||E||int da. Consequently the existing
occupation replacements apply to the ratios in (5), first at a fixed spatial
mollification scale and then as that scale tends to zero.

Density exponential tightness and spatial L2 energy come from the reversible
forward/backward and exchange-form estimates in the dependency; likelihood
transfer retains them under (9). Continuity identifies density limits from the
actual current (6). Thus (11) is an energy-class weak equation, not a formal
closure on its mean.

To prove uniqueness, first obtain strict interior bounds for every weak
solution starting at m. Write q_E(rho)(t) as a bounded measurable scalar.
The flux chi(rho)(E-alpha^2 q_E) is Lipschitz in rho. Truncation comparison with
spatially constant subsolutions, justified by the energy class, gives

    rho(t,x)>=m exp[-s||partial_x E||_infinity t],
    1-rho(t,x)>=(1-m)exp[-s||partial_x E||_infinity t].    (12)

Indeed the constant subsolution has derivative -s||E_x||rho, which is at most
-s chi(rho)E_x, and the shared scalar q_E has no spatial derivative. The same
argument applies to holes. Put delta_T=min(m,1-m)exp[-s||E_x||T]. Then
C_rho>=delta_T(1-delta_T)>0. On this range q_E is Lipschitz in rho in L1,
with constant at most 2||E||/[delta_T(1-delta_T)].

For two solutions, multiply the difference equation by the density difference.
The diffusion term is -c||partial_x difference||_2^2; the flux difference is
bounded in L2 by a fixed multiple of ||difference||_2. Young's inequality and
Gronwall give uniqueness. Existence follows from the just-identified compact
limits (or a uniformly parabolic approximation). Hence the comparison process
converges to the unique solution (11). This proves the required tilted LLN for
every fixed smooth E and the actual associated deterministic initial sequence.

## 4. Likelihood, upper bound and action identification

The exact likelihood is

    log Z_E=N^-1 K_E
       -int sum_i r_i[exp(d_i(E)/N)-1-d_i(E)/N]dv.         (13)

The cubic Taylor remainder is O(1) on physical N^2 T and therefore negligible
after division by N. Equations (5)--(7) and (6) identify its limiting functional

    L_E(rho,j)=int_0^T {int E[j+c rho_x]dx
                                      -(1/2)M_rho(E,E)}dt. (14)

For time-dependent fields, int E j is interpreted as integration by parts
against W, exactly as in the reference path theorem. The action is
I_alpha=sup_(smooth E) L_E, with continuity and initial association enforced.
For the upper bound use finite spatial mollification in the mobility functional,
then occupation replacement, before removing mollification. Ratios in (7) are
continuous at zero activity as above. Compact covers and mean-one likelihoods
give the local upper bounds.

Exponential tightness of total circulation follows from its exact corrected
martingale (bounded jumps, bracket<=cN per physical time) and the clock remainder
cost O(gamma_N/N) in divided log moments. Density tightness was already proved.
Exact one-dimensional conservation gives ||W_t^N||_TV<=|sum_iJ_i/N^2|+1, and
smooth current tests use (6) and bounded-jump martingale moduli. These are the
same explicit topology/compact-containment steps as continuation7, now with the
proved current correction. They give the full closed-set upper bound.

By (8) the variational energy is equivalent to the reference weighted L2
energy. Weighted Riesz representation identifies a=j+c rho_x, and inversion of
(7) gives

    E=(a/(s chi))+[alpha^2/(1-alpha^2)](int a)/(s C_rho).   (15)

Substitution yields (3), since int rho_x=0. The reference energy identification
therefore applies with equivalent norms, not with an unproved new finite-state
model. In particular I_0<=I_alpha<=I_0/(1-alpha^2), and the same finite-energy
path class and compact sublevel sets are retained.

Lower semicontinuity can also be checked directly rather than inferred from
the norm comparison alone. For each fixed E and each time,

    M_rho(E,E)/s=inf_b int chi(rho)[E^2-2 alpha b E+b^2].

The bracket is (E-alpha b)^2+(1-alpha^2)b^2>=0. Each expression before the
infimum is concave and weakly upper semicontinuous in rho; so is the infimum.
The integrated form follows by approximation of the minimizing bounded scalar
b(t) by simple or smooth time functions. Thus (14) is lower semicontinuous in
the weak density/current topology on bounded-density paths. Its supremum is
lower semicontinuous, and sublevels contained in the reference compact
sublevels are closed. This supplies the asserted goodness.

## 5. Matching lower bound and complete approximation

For a smooth path with rho bounded strictly between zero and one, continuous
current j, continuity equation and initial rho=m, define E by (15). It is smooth
after the usual path approximation and has a finite sup norm on the fixed
horizon. Equation (11) has this desired path as its unique solution. Under the
comparison law the path is typical; (13)--(14) converge to I_alpha. Restricting
the inverse likelihood to a typical neighborhood supplies its lower exponent.

Every finite-action path has a cost-preserving smooth approximation. First mix
it with the flat zero-current path to stay away from 0 and 1. The first term
in (3) is convex because chi is concave and a^2/chi is convex in (rho,a). The
second term is also convex: its numerator is the square of a linear functional
of j and its denominator C_rho is concave in rho. Next convolve in space. The
first cost decreases by Jensen; int j is unchanged and C_rho increases by
concavity of chi, so the second cost also decreases. Finally extend the path
as (m,0) before time zero and convolve using a smooth past-only temporal kernel
supported in [epsilon,2epsilon]. Continuity, initial m and a flat interval near
zero are preserved; convexity again does not increase the cost. Lower
semicontinuity and convergence give equality of limiting costs. No future-end
extension with uncontrolled cost is inserted.

The smooth lower bounds consequently give the lower bound for every open set.
Together with the preceding upper and tightness steps this proves the stated
good path LDP, conditional on the explicit corrected-current and occupation
lemmas whose proofs and exact versions are retained in this round and round7.

## 6. Consequence and earned limits

The zero-cost path satisfies the ordinary heat equation with current -c rho_x.
The same uniform canonical equilibrium law is preserved by the microscopic
operation, while the complete nonlinear history cost is changed by the second
term of (3). A fixed alpha tunes the penalty of spatially integrated transport.
At flat density its circulation contraction is
q^2/[2s chi(m)(1-alpha^2)T], agreeing with the earlier scalar result; the new
spatial receiver no longer needs its canonical-only lower-bound argument.

This action is not an unchanged full density-path law: minimizing it over
currents consistent with a nonuniform density history can change that history's
cost. The harmonic paired-current comparator separately preserves an entire
density law and has a different supplied interaction. At equilibrium the
linearized density fluctuations do not see the constant-current subtraction;
a full fluctuation theorem requires its own proof and is not inferred solely
by differentiating this LDP.

The result is population mathematics, not finite-data acquisition, an apparatus
or a demonstrated speedup. Exact rates, atomic event/bit updates, the common
clock, initial law and retained-record interface are actual premises. Generic
MFT, corrected currents, internal-state and paired-current mechanisms have
primary predecessors. Historical novelty and practical superiority are not
established by closing this receiving theorem.
