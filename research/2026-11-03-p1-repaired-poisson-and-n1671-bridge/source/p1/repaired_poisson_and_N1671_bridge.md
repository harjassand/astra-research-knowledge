# Corrected frozen-slice transport and a common low-corner/high/service receiver

**Scope.** Raw six-species ten-rate generator, arbitrary fixed strictly positive rates. The original Sol high-region construction is used only at its stated scope (fixed commit `487bfb76526a4218c71990cd32dda8e0a52478c7`). The service inequality and one-sided transport of `W` are taken from Sol N1671 (commit `23d0ada35f0340d1460403d23503620e3686c2d0`); the new consequences below are derived from those inequalities. No complete recurrence or global nonexplosion theorem is claimed. All source shifts below are actual raw reaction shifts.

## 1. Frozen A background and correct common Poisson law

Fix A=a>=0 and regard the four A-block reactions as kill/transfer channels. The frozen-A background G_a contains all four D-block reactions and both core reactions, with their raw rates. Put

    d*=beta0 beta3 / beta2^2
    e*=beta2^2 / (beta1 beta3)
    f*=beta1 beta2 / (beta0 beta3).

Choose b*,c*>0 with **b*c*=sqrt(kb/kf) e*f***. Then beta0=beta1 d*e*=beta2 d*^2 e*f*=beta3 d*^3 e*^2 f*^2 and kf a d* (b*c*)^2=kb a d* (e*f*)^2. The product law pi=Pois(b*) x Pois(c*) x Pois(d*) x Pois(e*) x Pois(f*) is invariant for every G_a. Complex-balanced nonexplosion applies to each frozen background. For a=0 this invariant law need not be the stationary law in an individual communicating class: B,C are frozen by G_0; invariance and Lp contraction still hold.

## 2. Exact Lp -> Lq source-weighted operator

Let z=(B,C,D,E,F), let s_r be the five-coordinate reactant complex of A-source r, let nu_r be its five-coordinate net shift, and let kappa_{a,r} be its anchor-dependent rate factor (alpha0,alpha1*a,alpha2*(a)_2,alpha3*(a)_3). Denote the actual source hazard by lambda_r(z)=kappa_{a,r}(z)_{s_r}. For the output density relative to pi,

    T_{a,r}u(z+nu_r)=kappa_{a,r}(z)_{s_r} pi(z)/pi(z+nu_r) u(z).

Unavailable transitions have value zero. For q>=1 set

    M_{a,r,q}(z)=kappa_{a,r}^q (z)_{s_r}^q [pi(z)/pi(z+nu_r)]^(q-1)

on the enabled set, zero elsewhere. Change variables from the endpoint to its actual predecessor to obtain the exact identity

    ||T_{a,r}u||_q^q=E_pi[|u|^q M_{a,r,q}].

For 1<=q<p<infinity, Holder yields

    ||T_{a,r}u||_q <= [E_pi M_{a,r,q}^{p/(p-q)}]^{(p-q)/(pq)} ||u||_p.

For q=p/2 (p>=2), the constant is [E_pi M_{a,r,p/2}^2]^(1/p).

The four weights, with muB=b*, muC=c*, are

    r0: alpha0^q ((B+1)/muB)^(q-1)
    r1: (alpha1*a)^q B^q ((C+1)/muC)^(q-1)
    r2: (alpha2*(a)_2)^q (B*C)^q (((B+1)*(C+1))/(muB*muC))^(q-1)
    r3: (alpha3*(a)_3)^q (muB*muC)^(2*(q-1)) (B)_2 (C)_2.

All weights have all finite positive pi moments. In particular, source 3's factorial hazard cancels the entire denominator caused by its backward shift. **There is no Lp->same-Lp claim.** A positive-coordinate shift alone need not be bounded on a fixed Poisson Lp space.

Let Q_a(t) be the Feynman--Kac semigroup of G_a killed at total A-source hazard lambda_A>=alpha0. Its pi-adjoint obeys ||Q_a(t)^*u||_p<=exp(-alpha0 t)||u||_p and its occupation resolvent obeys ||int_0^infty Q_a(t)^*u dt||_p<=alpha0^-1||u||_p. Compose with T_{a,r}. For K actual A-source events, initial p=2^(K+1) gives successive densities in L^(2^K),...,L^2; every fixed input has all polynomial and linear-exponential moment costs up to those K events. There is no uniform-in-K or polynomial-in-initial-population estimate: for point input z0, ||delta_z0/pi||_p = pi(z0)^(-(1-1/p)), factorially large as z0 diverges. Actual moments may be smaller; the present proof does not establish a polynomial bound.

## 3. A new polynomial receiver on the entire simultaneous-low corner

Let C0={A<=2,D<=2}, let b0=alpha0+beta0, and let tau_C be the first time either anchor reaches 3. On C0 both terminal channels vanish; every genuine noncore reaction is a growth reaction and increments exactly one anchor by 1. Core reactions fix both anchors and conserve total population M=A+B+C+D+E+F. Thus, from initial (a,d), tau_C occurs by the (5-a-d)th noncore reaction (<=5), with no terminal before exit. Each growth increases M by at most 3. Therefore on every path up to exit

    J_nc(tau_C)<=5,   M<=M_t<=M+15,
    E tau_C <=5/b0.

The stopped state space for each finite input is finite (all counts nonnegative and M_t<=M+15), so this is a genuine nonexplosive physical episode, including arbitrarily fast competing core motion. Its expected core count is finite and bounded, for example,

    E J_core(tau_C) <= [20(kf+kb)/b0]*(M+15)^4,

because lambda_core<=4(kf+kb)(M+15)^4 before exit.

Let W be N1671's globally proper quadratic service receiver, with c(1+M)^2<=c0+W<=C(1+M)^2. Define

    F_C(x)=E_x[tau_C+J_nc(tau_C)+W(X_tau_C)],  x in C0.

Then 0<=F_C(x)<=5/b0+5+C(1+M+15)^2, and F_C(x)>=c M^2. Every actual exit lands in {A=3,D<=2} union {D=3,A<=2}. First-step conditioning gives

    L F_C(x)=-1-q_nc(x) for ALL x in C0,

where L uses the full eight block hazards and two core hazards. This is polynomially controlled in the **initial** population, unlike the one-sided Poisson Lp bound.

The same 'monotone activation box' works for any finite number m of low-anchor ports whose terminal reactions are disabled at anchor <=2 and whose growth changes one anchor by +1, with a core that fixes anchors and total mass. First exit from the box uses at most 2m+1 noncore growth events, so any polynomial receiving terminal value has a uniform polynomial input bound.

## 4. A single actual high+corner receiver sharing N1671 boundary values

Take Sol's N large enough, N>=6, and let B={A<N or D<N}. Let V be Sol's high-region quadratic dominating potential and q_nc the actual total noncore hazard. N1671's W is globally proper, nonnegative, and quadratically upper bounded, so W<=K V for some fixed K on B. Sol's proven high-region stopping law gives E_x[tau_B+J_nc(tau_B)+V(X_tau_B)]<=V(x).

Define

    H_W(x)=W(x), x in B,
    H_W(x)=E_x[tau_B+J_nc(tau_B)+W(X_tau_B)], x outside B.

This is finite, globally proper, at most quadratically growing, and obeys L H_W=-1-q_nc outside B. (Properness follows by Sol's event-count/total-mass dichotomy, not an unjustified lower quadratic equivalence.)

Now set

    Hhat(x)=F_C(x), x in C0;
    Hhat(x)=H_W(x), x outside B;
    Hhat(x)=W(x), elsewhere.

This is ONE globally defined nonnegative proper receiver, at most quadratic in M. Every jump from the simultaneous-high region into B lands with A,D>=N-3>=3 and therefore cannot land in C0. Every jump from C0 lands with at least one anchor <=3 and cannot enter the high region. Thus the two exact stopped generator identities survive this gluing without a source correction:

    L Hhat=-1-q_nc on {A>=N,D>=N} and on {A<=2,D<=2}.

This does **not** imply the same inequality throughout B. It does give a bona fide common receiving function for the high region and full low-low overlap, with actual output values and rewards.

## 5. Additional N1671 consequence: full-generator service-dominant region at intermediate anchors

Use N1671's global receiver W=eta1*A^2+eta2*D^2-J1*v1-J2*v2+R*S^2 with J1=floor(min(B,C)/2), J2=floor(min(E,F)/2), S=B+C+E+F. Its proved one-sided transport estimates have raw constant C: positive own-profile increment <=C, negative own-profile decrement <=C(1+a_i), off-diagonal absolute increment <=C. Suppose R>=3*C/8+1 plus its properness choice. Put K0=4R-3C/4>0.

N1671's terminal/core identity, keeping the true terminal landing, yields

    L_service W <=-K0 S (lambda_T1+lambda_T2).

Indeed each terminal changes S by -4, and on its enabled state S>=4, so Delta(R*S^2)=R*(-8S+16)<=-4R*S; the exact packet-routing cancellation leaves at most (3C/4)S times the terminal hazard.

A growth on port i has hidden increment 1,1,2 and eta_i anchor-square increment eta_i(2a_i+1). N1671's one-sided profile estimates and nonnegative new-packet value imply

    Delta W <= eta_i(2a_i+1)+5R*S+C*(1+a_i)*J_i+C*J_j       (S>=4).

Suppose BOTH ports are ready: a_i>=3 and hidden pair counts B_i,C_i>=2. Let G_i be that port's sum of its source0,1,2 rates, T_i^rate its source3 terminal rate, and P_i=(a_i-2)(B_i-1)(C_i-1). Define the raw constants

    g_i=(rate_i0/24+rate_i1/4+rate_i2)/rate_i3,
    t_i=(rate_i0/6 +rate_i1 +4rate_i2)/rate_i3.

Direct falling-factorial division gives, on ALL ready states,

    G_i <= (g_i/P_i)*T_i^rate,
    (1+a_i)*J_i*G_i <= t_i*T_i^rate,
    (1+a_i)*G_i <= t_i*T_i^rate.

The lower-degree terms in the first bound use (a_i-1)>=2, B_i>=2, C_i>=2. Summing over every growth reaction and retaining all terminal/core contributions gives the **full raw generator bound**

    L W <= SUM_i T_i^rate [-K0*S+(2eta_i+C)*t_i+(5R+C/4)*S*g_i/P_i].

Let g=max(g_i), t=max_i((2eta_i+C)*t_i). Set

    P_star=2*(5R+C/4)*g/K0,
    eps=g/P_star=K0/(2*(5R+C/4)),
    S_star=max(8,4*t/K0,4*(1+eps+1/(24*(alpha3+beta3)))/K0).

Whenever both ports are ready, P_1,P_2>=P_star and S>=S_star,

    L W <= -(K0/4)*S*(lambda_T1+lambda_T2) <= -1-q_nc.

This includes arbitrarily large hidden inventories even for BOTH anchors fixed at 3, and states with an intermediate bounded anchor and an unbounded other anchor. It is a substantive full-generator region outside the simultaneous-high theorem. It is not a global solution: unready activation and source-heavy regions remain.

**Exact attachment to Hhat.** At a ready-service state in B with min(A,D)<=N-2, all one-reaction destinations remain in B (growth raises one anchor by at most 1), and no terminal can send both anchors to <=2 in one jump because the other anchor stays >=3. Hhat equals W at this state and EVERY one-step destination. Hence L Hhat=L W<=-1 there. Define the noncompact union

    Omega = {A>=N,D>=N}
            union {A<=2,D<=2}
            union {A,D>=3, min(A,D)<=N-2, both ready, P1,P2>=P_star, S>=S_star}.

The new globally proper Hhat obeys L Hhat<=-1-q_nc on **every** state in Omega. Its complement is inside B outside the low-low corner, so Hhat equals W at *every* actual exit point from Omega. Localizing Hhat at finite population and time, and using the compensated genuine noncore count, gives the actual stopped operation

    E_x[tau_Omega+J_nc(tau_Omega)+W(X_tau_Omega)]<=Hhat(x), x in Omega.

Properness and the negative physical-time drift rule out explosion before tau_Omega and prove that this stop is finite almost surely, including every intervening core jump. This is a single genuine composable source-count/physical-time receiver on a noncompact union, not a global recurrence theorem. No unknown receiving profile is hidden at any of these endpoints.

Unit rates on both blocks, kf=2,kb=1, eta1=eta2=1, C=R=100: K0=325, g=31/24, t=(102)*(31/6), P_star=217/52 (~4.173), S_star=8. Thus A=D=3, B=C=E=F=4 satisfies the bounds and exact generator evaluation gives L W=-17,964,449. This and other exact-rational checks are in service_dominance_exact_check.py; the proof is algebraic, not computational.

## 6. Exact remaining incompatibilities

1. **One-sided strip vs polynomial corner.** The A<=2 stopped value with boundary W at A=3 and the D<=2 stopped value with boundary W at D=3 are individually finite, but inserting both into one function changes each other's first-step outputs. At A=2,D<=2, any A-growth jump into A=3 acquires an extra raw term lambda_r(x)[F_D(x+nu_r)-W(x+nu_r)]; its sign is not earned. The symmetric seam has the analogous term. The polynomial corner F_C removes this conflict *inside* A,D<=2 but does not solve infinite alternation outside that corner.
2. **Service/high seam.** If min(A,D)=N-1 and the other anchor>=N, a growth event can enter the eliminated high region where H_W replaces W. A full-generator service inequality for W does not automatically pay lambda_r[H_W(y)-W(y)]. The positive part of this source-indexed receiving error remains to be controlled.
3. **Intermediate unready strips.** States with 3<=A<N (or symmetric D), one or both unready ports, and arbitrary other inventories are not covered in general by the demonstrated regions. N1671 explicitly leaves activation source switches unpaid.
4. **No globally common Poisson measure.** The frozen-A backgrounds have a common pi across a, and frozen-D backgrounds have their analogous reference, but these two reference families cannot in general be made the same full product-Poisson law. Such equality would impose the full complex-balance flux condition kf*(b_A*c_A)^2=kb*(e_D*f_D)^2, which is not true for arbitrary rates.

**Conclusion:** the repaired Lp theorem, a new polynomially uniform full overlap receiver, exact high/corner composition with N1671, and a new ready intermediate-anchor drift region are established. The seam and activation drift needed for unrestricted recurrence and nonexplosion are not established. The common Omega-stop is a positive global-coordinate interface only on the stated noncompact union; its complement is still unbounded. Do not infer a full-network theorem from the fact that separate killed resolvents exist.
