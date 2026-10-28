# Excitation discovery: finite guarantees, a noise obstruction, and tolerance

28 October 2026. Companion to shifted_theorem.md. The positive-reference
genericity proof in N1082 was read directly: it proves almost-sure nonzero
coupling under a continuous reference distribution, and explicitly does not
promise finite-grid conditioning. The following distinctions preserve that
scope.

## 1. No uniform identification of every relevant control at fixed error

Even with one scalar state and one actuator, set Q0=1, e=1 and v=a. Then

    R_a(u)=r0+1+u*a^2,    0<=u<=Delta.

The source a=0 has an irrelevant actuator; every a>0 has a relevant actuator.
Both belong to the class z0<=1, v^T Q0^-1 v<=1 when 0<=a<=1. If
Delta*a^2<=2*eta, their raw responses are everywhere within 2*eta. An
adversarial sensor bounded by eta can return their pointwise midpoint under
either source, for every adaptive query and every repetition. This is an
all-domain indistinguishability example, not merely a missed finite seed.

Consequently upper source-class bounds alone cannot guarantee resolution of
every relevant coupling. A method must retain unresolved controls, impose a
quantitative relevance margin, or certify an approximation tolerance. No
number of repeated readings defeats the stipulated correlated error.

## 2. A dark chain and what it does NOT prove

Take Q0=I in dimension L+1, e=e0, edge actuators

    v_j=e_j+e_(j+1), j=0,...,L-1,

and terminal actuator v_L=e_L. The squared actuator norms are at most two,
independently of L. The terminal actuator is exactly dark at the origin.
For a positive reference w, tridiagonal cofactor expansion gives

    h_L(w)=e0^T Q(w)^-1 e_L
          =(-1)^L * product_(j=0,...,L-1) w_j / det Q(w).

This nonzero coupling begins at order L in the illuminating edge doses.
At a small shared reference, its squared singleton strength can be far below
the raw error floor even while the mathematical genericity condition holds.

The same source structure also bounds the terminal control's full-domain
importance. Because det Q(u)>=1 and sum u<=Delta,

    |h_L(u)| <= (Delta/L)^L,
    0<=Z(u with u_L=0)-Z(u)<=Delta*(Delta/L)^(2L).    (1)

The second inequality integrates the exact derivative h_L^2. Moreover
Q(u)<=(1+2*Delta)I, so Z(u)>=1/(1+2*Delta) and

    |R(u with u_L=0)-R(u)|
       <=(1+2*Delta)^2*Delta*(Delta/L)^(2L).          (2)

Thus long high-order dark paths obstruct exact all-control identification,
but do not by themselves obstruct a fixed-tolerance global response/control
capability. Their global influence also shrinks under the same total-dose
and norm bounds. It would be wrong to turn this example into an impossibility
theorem for tolerance-based approximation. Conversely, simply deleting the
terminal actuator without such a bound remains wrong.

## 3. An explicit finite discovery / tolerant-omission procedure

Suppose independent source specifications warrant

    z0<=zeta,   alpha_i(0)=v_i^TQ0^-1v_i<=tau_i.

Whiten by Q0 and write a_i=Q0^-1/2 v_i, b=Q0^-1/2 e. Define

    D(u)=det(I+sum_i u_i a_i a_i^T),
    p_i(u)=D(u)*b^T(I+sum_j u_j a_j a_j^T)^-1 a_i.

The determinant is used only in the proof; it is not supplied to the learner.
The rank-one determinant and adjugate identities show:

* D(u)>=1 on the nonnegative domain.
* D(u)<=product_i(1+u_i*tau_i), by the determinant lemma and Hadamard.
* Each p_i is multiaffine, independent of u_i, and has total degree <=n-1.

The last statement follows by varying one rank-one update: det(Q+taa^T)
times its inverse is affine in t. For i's own update, Sherman-Morrison
shows numerator independence exactly.

Reserve a reference budget dref<Delta, let a=dref/n, and acquire at every
vertex w in {0,a}^n. A baseline and one positive increment t<=Delta-dref
per control cost at most (n+1)*2^n raw source reactions, before calibration,
setting, reset and any reuse. No matrix entries are provided for free.

At w, the true singleton loss is

    L_i(t;w)=t*h_i(w)^2/(1+t*alpha_i(w)),
    0<=alpha_i(w)<=tau_i.

From the calibrated Z intervals acquire the upper loss L_i^+(t;w). Even
when no positive lower loss is resolved, the sound bound

    h_i(w)^2 <= (1+t*tau_i)*max(0,L_i^+(t;w))/t      (3)

requires no division by a weak coupling. Keep the raw record and report
inconsistent bounds if the premise-compatible interval is empty.

Let H_i^2 be the maximum acquired upper bound (3) over vertices, and set

    Dref=product_j(1+a*tau_j),
    C=1 if n=1, else (1+2*Delta/(a*(n-1)))^(n-1).

Multiaffine interpolation of p_i on the other n-1 coordinates gives

    |p_i(u)| <= max_vertex |p_i(w)| *
                product_(j!=i)(|1-u_j/a|+u_j/a)
              <=Dref*H_i*C.

The last inequality uses |1-t|+t<=1+2t for t>=0 and AM-GM with the total
dose bound. Since D(u)>=1,

    sup_original_domain h_i(u)^2 <= (C*Dref)^2*H_i^2. (4)

This is an acquired, full-domain upper relevance bound. Deleting a set J
only as an approximation, by setting their doses to zero, changes Z by at
most

    sum_(i in J) u_i*(C*Dref)^2*H_i^2
      <=Delta*max_(i in J) [(C*Dref)^2*H_i^2].      (5)

The removal path stays in the original nonnegative simplex. Equation (5)
is a tolerant omission certificate, never a claim of exact irrelevance.
If the amplified sensor floor makes it too large, the outcome is unresolved.

Conversely, if sup_domain |h_i|>=sigma, some vertex has
|h_i(w)|>=sigma/(C*Dref). Its true singleton loss is at least

    t*sigma^2 / [(1+t*tau_i)*(C*Dref)^2].            (6)

If this exceeds the sum of the two observed Z-interval diameters, the lower
loss endpoint is positive at that vertex. This is a finite quantitative
discovery statement with explicit exponential cost and conditioning. It
does not guarantee a COMMON well-conditioned reference for all controls.

## 4. Finite common-reference existence with a quantitative promise

A deliberately expensive construction fills that logical gap. It is not the
recommended practical route. Suppose every desired control satisfies
sup_original |h_i|>=sigma>0, and choose a>0 with n*a<=dref. Use the positive
rational moment curve

    w_j(t)=a*t^(2^j),    1/2<=t<=1,   j=0,...,n-1.

Distinct multiaffine monomials map to distinct powers. Therefore
q_i(t)=p_i(w(t)) is a nonzero univariate polynomial of degree at most
D=2^n-1. Let

    Acoef=(8D)^D/D!,
    C0=Acoef*(1+Delta/(n*a))^n.

Lagrange interpolation at D+1 equally spaced points of [1/2,1] bounds every
coefficient of q_i by Acoef*sup|q_i|. Indeed each Lagrange numerator has
coefficient absolute sum at most 2^D, its denominator magnitude is at least
(1/(2D))^D*j!*(D-j)!, and summing over j gives Acoef. Since coefficients
of q_i are exactly a^|S| times multiaffine coefficients of p_i,

    sup_original |p_i| <= C0*sup_[1/2,1]|q_i|.

Thus sup|q_i|>=sigma/C0. Now sample M=n*D+1 equally spaced points on
[1/2,1], with spacing h=1/(2nD), and put

    Cgrid=(2nD)^D/D!.

Any D+1 selected grid points have a Lagrange interpolation constant at most
Cgrid on [1/2,1]: numerator factors are at most 1/2, while denominator
factors are at least h times their index distances. If q_i were at most
sigma/(2*C0*Cgrid) at D+1 sampled points, its supremum would be at most
sigma/(2*C0), a contradiction. Hence each control has at most D bad grid
points. With M=nD+1, at least one sampled point is good for every control.

Since D(w)<=Dref, that common positive reference obeys

    min_i |h_i(w)| >= sigma/(2*C0*Cgrid*Dref).        (7)

Actual acquisition can test every seed using its bounded-error singleton
intervals. Equation (7) guarantees a resolved positive loss only if the
sensor/actuation allowance is sufficiently below its explicit loss scale.
Successful two-dose normalization additionally requires its acquired inverse
scale interval to have positive lower endpoint; that gate is never bypassed.

For completeness a sufficient bound for that second gate is explicit. If
P>=pmin, alpha<=tau and the singleton loss interval endpoints are each
within Omega of truth, let lk=tk*pmin/(1+tk*tau). When Omega<min(l1,l2),
the inverse-scale interval's deviation from 1/P is at most

    [Omega/(l1*(l1-Omega))+Omega/(l2*(l2-Omega))]
       /(1/t1-1/t2).

If this is smaller than 1/(zeta*tau), the inverse scale has positive lower
endpoint, since P<=zeta*tau. All constants and stringent noise requirements
are visible; genericity supplies none of them for free.

This common-reference construction costs up to M*(1+2n) raw reactions
before pair/landmark acquisition, and polynomial evaluation/reference
precision grows exponentially with n. Tiny coordinates on the moment curve
can be destroyed by a fixed DAC. Its preparation allowance must therefore
be included, or sufficiently many finite bits actually supplied and charged.
This is a finite conditional existence bound, not a scalable apparatus or a
uniform promise at fixed precision. The main continuation's dark-tolerant
whole-domain representation may be much more useful precisely because it
need not normalize every actuator separately.

## 5. Comparator and conclusion of this branch

Ordinary shifted Woodbury and interval reduced models can use the same
reference, acquired trace margin, signed resolvent bound and interval
discovery tests. Certified reduced-basis methods likewise explicitly pay
for coercivity/stability estimation when their error bounds require it.
No advantage over that equally informed route is claimed.

The shifted theorem removes a real full-domain obstruction once excitation
is acquired. The excitation branch shows why it is not a universal dark-safe
compiler at a fixed noise/actuation budget. Tolerant full-domain approximation
remains possible; this branch's finite global bounds are expensive, and they
justify comparing against representations that avoid individual excitation.
