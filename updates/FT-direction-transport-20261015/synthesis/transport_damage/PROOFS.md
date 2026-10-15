# Committed output before failure under accessible stiffness

15 October 2026. Independent extension of the supplied transport checkpoint. These are conditional mathematical results, not material measurements. External correctness, historical originality and physical capability remain UNKNOWN. The row-time-change mechanism is standard Markov-chain machinery; no priority claim is made.

## 1. Exact domain and accounting boundary

Let I be a finite set of operational states. A transition event t from i either reaches another operational state j or an absorbing failure label D_alpha. Multiple events can connect the same ordered state pair; keep their labels when their reservoir, damage mechanism, reward or stiffness response differs. Every operational state is transient: absorption occurs almost surely. Rates are finite and positive on the fixed retained event set. Fix an initial distribution rho, independent of the control, and a fixed per-event reward g_it. Failure events may carry fixed terminal/inventory settlement rewards; otherwise their reward is zero. There is no separate continuously accrued reward and no finite laboratory-time cutoff in the first theorem.

For the row-generator convention, Q_ij=sum_t:i->j k_it for i != j and Q_ii=-sum_all outgoing t k_it. Absorbing-state values are zero. Put r_i=sum_t k_it g_it. Then

    v=(-Q)^(-1) r,      Y=rho^T v,
    nu^T=rho^T(-Q)^(-1),      tau=rho^T(-Q)^(-1) 1.

Here v_i is expected cumulative reward starting in i, nu_i is expected time spent in i before failure, and tau is mean lifetime. Finite transient state space with finite rates and almost-sure absorption makes the relevant fundamental matrix finite. Alternatively the formulas apply whenever its inverse and reward expectations exist. Signed rewards are allowed; a positive technological endpoint still needs an explicit accepted-output definition.

Net right-port counting, with right entry -1 and right exit +1, is different from gross exits. A finite-life pore may retain or lose its last ion. Terminal inventory and its free energy must be accounted for before interpreting particle count as useful transport or work. In particular, zero stationary equilibrium current does not imply that every failure-stopped signed count is zero.

## 2. Common-host rate factorization

Write chi=kappa*c/(1+kappa*c) for the source's rank-one clamp. In its common-host, fixed-prefactor transition-state reduction,

    k_it(chi)=k_it(0) exp[-beta chi (R_t^dagger-R_i)].

R_i is the well's accessible relaxation response and R_t^dagger the corresponding transition ensemble's response. Every damage event must obey the same stated law for the theorem to apply to that event. Introduce

    D_ii(chi)=exp(beta chi R_i),
    bar_k_it(chi)=k_it(0) exp(-beta chi R_t^dagger).

Then Q=D bar_Q and r=D bar_r. This factorization includes the entire negative diagonal, including killing. It follows exactly that

    v=(-bar_Q)^(-1) bar_r.

**Theorem: at fixed saddle responses, topology, baseline rates, initial state/distribution and event rewards, every expected cumulative jump reward before absorption is independent of every well response R_i.** All success/failure committors are likewise independent. The embedded transition probabilities

    P_it=k_it/sum_u k_iu=bar_k_it/sum_u bar_k_iu

make the reason transparent: R_i rescales the entire clock at i and cannot change the next event. The full distribution of any path-count functional is unchanged, not only its mean. This extends immediately to waiting-time changes in a semi-Markov description whenever the conditional next-event/history law is unchanged and the path functional is integrable. It does not justify a Markov approximation to an unacquired correlated material.

The Arrhenius branching-fraction cancellation itself is explicit in Rahav, Horowitz and Jarzynski, PRL 101, 140602 (2008), Eq.3. The result here applies that established machinery to all killing events and accepted lifetime rewards; it is not a new stochastic primitive. [Primary author PDF](https://sites.lsa.umich.edu/horowitz-lab-new/wp-content/uploads/sites/1181/2018/06/pump.pdf).

The mean lifetime is instead

    tau=rho^T(-bar_Q)^(-1) D^(-1) 1,

and generally changes. Thus a de-trapping-induced speedup can change throughput per second without changing accepted output per failed specimen. With replacement/reset duration t_reset, the renewal throughput is Y/(tau+t_reset), where the full reset boundary and retained endpoint must be specified. Equal Y does not imply equal service rate, energy cost, or practical value.

**Precise exclusions.** An independently fixed laboratory-time corrosion hazard is not multiplied by D and can break invariance. So can control-dependent prefactors/recrossing, topology, preparation distribution, event rewards or failure definitions. A hard horizon, a deadline, or an occupation-time/holding cost depends on waiting times. If rho=rho(chi), add the preparation contribution rho'^T v. A clamp may change microscopic geometry/chemistry and invalidate the assumed rate family. These are acquisition gates, not negligible corrections.

## 3. Full target sensitivity: saddle contrasts weighted by continuation value

Define the event advantage

    A_it=g_it+v_destination(t)-v_i,

with v_Dalpha=0. Differentiating -Qv=r gives

    Y'=rho'^T v + nu^T(r'+Q'v)
       =rho'^T v + sum_i,t nu_i k_it A_it (d log k_it/d chi).

For fixed rho and the common-host law, d log k_it/d chi=-beta(R_t^dagger-R_i). The Bellman identity at each i is

    sum_t k_it A_it=0.

Consequently all well terms cancel:

    boxed: dY/dchi = -beta sum_i,t nu_i k_it A_it R_t^dagger.

Group events sharing saddle t into w_t=sum_origins nu_i k_it A_it. Then dY/dchi=-beta sum_t w_t R_t^dagger. A nominally forward hop can have negative A_it because it leads toward a damaging trap or increases return probability. An absorbing event with zero reward has A_iD=-v_i, which is negative when v_i>0; raising its saddle helps. Several damaging channels must all appear with their own visits, rates and response. Local ordering R_U<R_A<R_H does not determine this global signed sum.

For arbitrary acquired rate slopes s_it=d log k_it/dchi, the first sensitivity formula remains exact. It therefore supports an experimental rate-level test without an oracle for transition-state barriers. It cannot, from rates alone, identify whether a slope arose from a barrier, prefactor, recrossing, solvation or contact change. If k_it=p_it exp[-beta(B_it)], add sum nu_i k_it A_it d log p_it/dchi to the barrier contribution.

For an actual added energy kappa*q^2/2 and fixed dividing ensembles, a transition-state model gives d log k_it/dkappa=-(beta/2)(<q^2>_t^dagger-<q^2>_i)+d log p_it/dkappa. The same Bellman cancellation removes the well expectation from lifetime jump yield. The target contrast is the weighted transition-ensemble response plus the acquired dynamical correction, not a well phonon spectrum alone. Moving dividing surfaces, unresolved memory and path changes require a more complete rate/path model.

## 4. Legal accessible support design is a target objective, not a local barrier list

For rank one, R_t^dagger=(b^T K^(-1) f_t)^2/(2 b^T K^(-1)b). Define M=-sum_t w_t f_t f_t^T at the current operating point. Then

    dY/dchi=(beta/2) [b^T K^(-1) M K^(-1)b]/[b^T K^(-1)b].

If legal support coordinates restrict b=Bz, optimizing this **first-order**, fixed-normalized-clamp response is a generalized Rayleigh problem with numerator B^T K^(-1) M K^(-1)B and metric B^T K^(-1)B. Use an independent support basis, or quotient out its zero-coordinate kernel, so the metric is positive definite. It is not permission to choose arbitrary atomic coordinates or to compare controls of unequal fabrication/stiffness cost. The weights require the actual network and accepted-output boundary.

For the separate accessible_clamps worker's multiport parametrization, use Delta F_s=tr(Qc C_s)+common_term, with C_s=.5 a_s a_s^T and legal 0<=Qc<I subject to physical fixture constraints. The exact directional derivative is

    boxed: dY=-beta tr[dQc sum_t w_t C_t^dagger].

This supplies a signed global saddle objective for legal PSD direction selection. The finite-change map Y(Qc) is generally nonlinear and need not be concave. A linear PSD optimization is a local direction proposal; recompute the complete changed network before asserting a finite improvement. Neither computation acquires f_t, C_t, a legal fixture, or a physical response.

## 5. Many-state passivity and affinities

For each reversible pair with a shared saddle response and fixed reciprocal prefactors,

    log[k_ij(chi)/k_ji(chi)]
      =log[k_ij(0)/k_ji(0)]+beta chi(R_i-R_j).

The added term telescopes around every closed cycle. Static stiffness therefore changes no imposed cycle affinity. If all affinities vanish, detailed balance persists, and stationary antisymmetric currents remain zero. At nonzero reservoir affinity, existing paid chemical/electrical work can be dissipated differently. Irreversible damage represents an open thermodynamic boundary; making it absorbing does not remove its chemical work from the physical ledger. No equilibrium pump or free energy source is inferred.

Time-dependent stiffness is a different driven protocol. Static cycle-affinity invariance does not prove a generic no-pumping result for it. Known stochastic no-pumping theorems have additional restrictions, and modulation of both wells and barriers can pump at a paid control cost. We do not optimize such an apparatus here.

## 6. Exact two-state damage-channel stress test

Retain source entry A=a_L+a_R, exit B=b_L+b_R and N=a_L b_R-a_R b_L. Add a second absorbing damage rate d from the empty state, alongside occupied damage h. Starting empty,

    D=A h+d(B+h),
    E[T]=(A+B+h)/D,
    E[N_right]=(N-a_R h)/D.

These follow by solving the 2x2 transient generator with rows [-(A+d), A] and [B, -(B+h)] and reward vector [-a_R,b_R]. They reduce to the source's expressions at d=0.

Under the same source clamp, a'=alpha a, b'=q b, h'=r h. If the empty-state route has no clamp response, d'=d, then

    Y' = alpha(q N-a_R r h) /
         [alpha A r h+d(q B+r h)].

At d=0, Y'=q N/(A r h)-a_R/A; its large gain depends on q/r=exp[beta chi(R_H-R_U)], not R_A. If a positive finite crossover exists, Y'>Y exactly when

    d < alpha A h N(q-r) /
        [(N-a_R h)(q B+r h)-alpha(q N-a_R r h)(B+h)].

This inequality assumes the denominator and baseline positive useful yield are positive; other signs must be handled directly, not by dividing blindly. For the source's partly blocked synthetic example, the independent checker records the crossover and both outcomes. The new damage pathway need not accelerate: an unaffected competitor is enough to defeat an advertised local protective response. No corrosion rate is assigned to hBN, LLTO, a support, or a real specimen.

## 7. Dynamical and resource qualification

A migration free-energy shift alone does not acquire committed transport. In a parabolic-barrier generalized-Langevin approximation, a reactive growth rate lambda_b solves lambda_b^2+lambda_b gamma_tilde(lambda_b)-omega_b^2=0; the Grote-Hynes transmission factor is lambda_b/omega_b. A support changes the friction/memory spectrum as well as static free energy. The complete rate and branching slope must include this correction or be measured directly. This established theory is not a prediction for a named membrane here.

For a regenerative device, compare expected accepted output Y, lifetime tau, reset/replacement duration, fabrication yield, active area, support installation, electrode/reservoir work, heating/cooling, holding, maintenance, conditioning and disposal under one task boundary. Eventwise resource costs use the same fundamental-matrix reward calculation; clock-based utilities use occupation times. The source's fixed-current ohmic saving is only the available benefit under its illustrative geometry, not a total-system cost result.

If a homogeneous damage channel with unknown constant hazard h has zero events in a predeclared independently sampled at-risk exposure E, its one-sided zero-count Poisson bound is h_U=-log(delta)/E at confidence 1-delta. Exposure means time in that channel's actual precursor state, not total wall-clock duration. Multiple-channel qualification needs declared simultaneous coverage, censoring and hazard assumptions. Rate-level identification can therefore have a destructive lifetime/exposure cost; a local optical signal does not make it free.

The checker compares the exact reward, row-time-change, sensitivity and damage formulas against independent linear solves and finite differences. Those checks establish their numerical scope only.
