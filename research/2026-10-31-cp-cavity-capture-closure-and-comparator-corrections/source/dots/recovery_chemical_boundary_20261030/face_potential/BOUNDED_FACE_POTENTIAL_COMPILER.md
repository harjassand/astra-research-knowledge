# From one-hold tracing to an acquired face potential

30 October 2026. New theoretical construction, not independently reviewed. This preserves the accepted carried-launch bundle. It proposes a certificate-level replacement of its one-hold face restriction, not a general recurrence theorem.

## 1. Raw structural changes and unchanged restrictions

Keep the acquired connector, conservative binary residual architecture, positive seeds producing D, a+D->2a, baseline pooled forcing, direct true-F ingress guards, and full weak reversibility. At D=0 allow additional nonseed residual moves with a-count zero on BOTH ends, including moves that remain at D=0. Every such internal move and every restoring move must be pooled-neutral. Their rates may depend on the actual hidden counts. Let F be the D=0 states with no enabled hidden nonseed move, and B the remaining D=0 states. Require every internal D=0 hidden move from B to stay in B; thus only a positive-D exit or a seed/clearing can end a B excursion. This is an explicit finite source/output enablement check, not an assumed communicating property.

The carried launch row remains all D=0 at connector starts. A positive-D traced row includes entire B excursions internally. The ACTUAL hidden state evolves during a launch; it is not frozen or resampled. Internal moves preserve A,N,B, so every required reward is constant along them.

## 2. The new certificate

Fix residual a as a parameter during a B excursion. Define Q_B(a) to be the hidden-chain subgenerator, killed at:

* restoring exits to D>0;
* seed exits, with total operational rate k_seed(a)_2;
* ordinary clearing, with rate k0(a)_2.

The last two are genuine stopping events for the relevant face episode. No connector is included; adding connector stopping can only shorten the episode.

Seek a nonnegative function psi(a,h) on B and finite constants Psi,C such that

    0 <= psi <= Psi,                    -Q_B(a) psi >= 1,       (P)
    sum_{positive-D ingress r into B} q_r(x) psi(x+nu_r) <= C. (I)

The sum in (I) is over actual enabled ingresses and uses actual outputs. It is not a maximum over reaction types. Extend psi by zero outside B. These are generator/entrance inequalities, not a guessed stationary distribution.

For the accepted one-hold module, psi=1/[h_restore+(k_seed+k0)(a)_2] satisfies (P) exactly; (I) is its existing trace-cost comparison. Including seed/clear killing in psi is ESSENTIAL: psi=1/h_restore alone need not pay an a-proportional ingress when hidden restoring counts are small. Thus the proposed replacement contains the old certificate rather than inadvertently excluding its a-born channel.

## 3. Exact trace-cost theorem

For any stopped full episode, localized to finite state/time boxes, Dynkin's formula for the zero extension gives

    E integral 1_B dt_op
       <= psi(initial) 1_{initial in B}
          + E integral_{D>0} sum_r q_r(X_t)psi(X_t+nu_r) dt_op
       <= Psi 1_{initial in B} + C E integral_{D>0}dt_op.       (T)

On B the generator is at most -1; outside B the only positive generator contribution comes from actual ingress. Terminal seeds/clearing/connector jumps set the stopped potential to zero. Nonnegative terminal potential can be discarded. Localization and Fatou give the minimal-process inequality without a prior recurrence assumption. This prices every repeated internal B excursion, regardless of its jump count or return probability.

During a B excursion A is constant until its terminal event. Multiplying by any fixed A-profile or restored physical-factor reward therefore gives the same theorem; bounded A shifts at ingress change constants only. The initial term is deliberately bounded rather than n-small. It belongs to the carried launch row.

From (P), E tau_B<=Psi uniformly. Strong Markov and Markov's inequality at 2Psi give P(tau_B>2jPsi)<=2^-j, hence all fixed time moments uniformly. This does not assume independent blocks. Extra connector killing only improves these bounds.

## 4. Pooled forcing and positive-D reset survive

Delete whole B excursions from the D-clock. Internal face moves and restoring moves are pooled-neutral; therefore they do not alter any abstract pooled label. Seeds still remove at most two original-a labels and have a geometric count before clearing. The positive-D baseline and adapted extra-to-a construction are unchanged.

The entrance theorem (T), rather than a one-hold denominator, restores all deleted operational occupation. Low-A D-clock arrival, cohort concentration, clearing hazard, and direct true-F ingress bounds therefore have the same proofs. There is no new B-to-F return by the explicit structural check. The positive-D-start population reset and graded interfaces follow with changed constants, not with a reset on initial B.

The independent polynomial-moment proof also survives: each prescribed pooled path uses finitely many positive-D transfers. A B interruption exits within 2Psi with probability at least1/2; its restoring output is pooled-neutral, a seed is accounted for by the existing seed restart, and clearing ends the episode. Thus the former finite time-block argument replaces a single prescribed restoring jump by a uniformly controlled face excursion. No physical-species independence is introduced.

If the protected pool were empty on a B state, pooled neutrality would prohibit any restoring exit. At a=0 or1 the seed/clear kill is absent, contradicting (P). Hence a certificate automatically rules out a supposedly active empty-protected-pool face; the actual terminal guard still handles positive-D jumps into F.

## 5. Launch Green and complementary clock

The A,B connector and seed rates are independent of the current hidden state. Couple their reference path while running the hidden internal face chain at its actual rates. Until a restoring exit, its extra hidden jumps preserve A,N,B and all phase/counter flags. The accepted jump/excessive envelope therefore pays an arbitrary adapted restoring exit exactly as before. Hidden metadata need not remain frozen: only the reward and the reference A,B rates must remain unaffected. The reference path is nonexplosive independently, and on each fixed total-count interval the hidden chain is finite.

For an active mixed launch at fixed A>=a0,b>=q, the physical expected time to a restoring/seed/clear mark is at most

    Psi / [(A)_a0 (b)_q].

Consequently activation before that mark has probability at most

    tAb Psi / [(A)_a0(b)_q] <= C b^{1-q},

and immigration costs O(b^-q). This replaces the previous h_min one-hold race by a bounded FACE MEAN. Activation is still treated as an actual Z-up event, not an inactive neutral move. The seed/restoring share of the first terminal fast mark is bounded below by k_seed/(k_seed+k0): conditional on a seed-or-clear kill, its seed mark has this fixed probability, and a restoring exit only adds successful launch mass. Thus the accepted complementary trial continuation remains available. Initial A<a0 uses the original inactive approach.

## 6. A finite sufficient finder for (P),(I)

This is a concrete certificate search design, not yet implemented. Supply a finite degree budget and a finite denominator dictionary constructed from raw face hazards. For each enable-signature cell choose a fixed denominator D_sigma(a,h)>0 and a polynomial numerator N_sigma with unknown rational coefficients. Set psi=N_sigma/D_sigma. Candidate denominators may include the total enabled hidden jump hazard plus (k_seed+k0)(a)_2, or fixed bounded products/powers of such hazards. Their positivity on each cell must itself be certified.

As in the reviewed raw finder, partition counts into 0,1,2,3,4+z. Binary shifts fix every source and output enable-signature. Substitute actual rates and output shifts into (P),(I). Multiply by the product of the positive denominators at the finitely many actual neighboring states. Require every coefficient of each resulting polynomial to be nonnegative. Impose also N_sigma>=0 and Psi D_sigma-N_sigma>=0 coefficientwise. Denominators are FIXED before solving, so these are finite linear rational inequalities in numerator coefficients, Psi and C. A rational feasible solution is a directly checkable all-population certificate; infeasibility means only that this finite ansatz failed.

Enumerating a finite denominator/degree dictionary is terminating. An unbounded sequence of growing budgets would only be a semidecision procedure and is not called a complete algorithm. Size grows exponentially with species/cell count and rapidly with denominator products. No efficient or universal synthesis claim is made.

## 7. Proposed consequence and remaining verification

Subject to checking the finite-face certificate and the inherited phase foundations, (P),(I) supply exactly the trace, launch, moment and complementary-clock inputs of the accepted carried construction. They would replace the one-hold restriction by a bounded rational face-potential condition. This is an actual generator proof plus a finite certificate format, not an inference that all hidden face dynamics are stable.

Still required before claiming an implemented extension: code the rational inequality finder/checker; test actual multi-step raw inputs and adversarial failures; independently review the mode/pool/terminal conditions and full transfer. Unbounded face potentials, transitions from active B into dead F, A-changing internal face dynamics, adverse pooled moves and failure of the ingress inequality remain outside this result. Ordinary trace/Dynkin and stopped-time/Foster machinery are the mathematical comparators; no historical novelty is claimed.
