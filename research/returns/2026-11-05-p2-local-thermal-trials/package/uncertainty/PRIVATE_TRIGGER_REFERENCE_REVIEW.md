# Independent reference, conditioning and reuse check

This checks the selected thermal-intervention quantifiers; the main package
constructs its clock and sensor. Total variation is half L1. References here
are classical. Classical conditional Gaussian log-Sobolev inequalities do not
automatically establish an arbitrary quantum-reference statement.

## Private time is part of the reference

Assume the local thermostat has variance sigma^2 and friction gamma, invariant
law pi=Gamma_p x pi_rest, fresh Brownian noise independent of the initial
system and retained reference R, and actual initial budget

    D0=D(rho_SR||pi x rho_R)<infinity.

Entropy dissipation and conditional Gaussian LSI give

    -D'(t)>=gamma sigma^2 I_p(t),
    D(rho_SR(t)||Gamma_p x rho_rest,R(t))<=sigma^2 I_p(t)/2.

For an independent trigger with density w(t)<=C this implies

    D(law(tau,S_tau,R)||Gamma_p x law(tau,rest_tau,R))
       <=C D0/(2 gamma),
    TV<=sqrt[C D0/(4 gamma)].

Thus Z=(tau,rest_tau,R) includes the actual time. D0 includes I(S:R). A source
marginal entropy bound alone cannot prove arbitrary-reference decoupling. An
exact continuous-coordinate copy can have infinite D0; a reference possessing
future thermal noise is inconsistent with the fresh-noise premise.

Integrated dissipation does not itself certify a finite point-grid trigger.
Bounded timing error can round a continuous draw into atoms. A physically
supplied bounded-density trigger or a separate discrete/window theorem is
necessary. Taking Z at the actual launch avoids comparing two hidden states
at slightly shifted times.

## Joint arms and conditional arms

Let P on (p,Z) satisfy TV(P,Gamma_p x P_Z)<=delta. Mark p with

    a_b(p)=[1+b sin(p/sigma)]/2, b in {-1,+1}.

Under the product comparison law this gives exactly

    Q(dp,dz,b)=(1/2) q_b(dp) P_Z(dz),
    q_b(dp)=Gamma_p(dp)[1+b sin(p/sigma)].

Data processing bounds the actual marked joint law within delta of Q. Q is
the valid Markov operation: retain Z, discard p, draw a fair arm, draw p~q_b.
Both arms are used, so no rejection normalization appears. With a noninvasive
marker the actual unconditioned Z marginal is exactly unchanged; approximate
arm independence is the preparation consequence. Any common subsequent
arm-dependent physical evolution or outcome channel contracts this TV error.

Individual-arm statements do require conditioning. The sharp classical bound

    TV(P(.|A),Q(.|A))<=TV(P,Q)/max(P(A),Q(A))

follows by taking the common part mu of P,Q: mu(A)>=max(P(A),Q(A))-TV(P,Q),
and the conditional common mass is at least mu(A)/max(P(A),Q(A)). Ideal arm
probability 1/2 therefore gives conditional error at most 2 delta, provided
the actual arm has positive mass. The joint delta bound must not be reused
unchanged as a conditional-arm certificate.

## Finite metrology and backaction

Since |a_b'|<=1/(2 sigma), using p_hat rather than actual launch p changes the
joint marking law by at most E|p_hat-p_launch|/(2 sigma). Include integration,
clock error and processing latency in this estimate. Error/source independence
is not needed. A good-event error r with failure probability eta instead gives
r/(2 sigma)+eta. Finite Bernoulli evaluation/random-bit error adds directly.

A small displacement or momentum perturbation alone does not bound arbitrary
hidden/reference TV. For a predictable force d_t in the same thermostatted
momentum equation, the pathwise action bound integral d_t^2 dt<=J gives by
Girsanov and Pinsker

    D(P_backaction_paths||P_nominal_paths)<=J/(4 gamma sigma^2),
    TV(P_backaction_paths,P_nominal_paths)<=sqrt[J/(8 gamma sigma^2)].

The deterministic action bound supplies Novikov integrability. Initial
reference and identical independent extra randomness can be included. This
controls hidden/reference path disturbance without hidden-density regularity.
It does not cover arbitrary errors outside the declared noisy coordinate.

Girsanov TV alone is not a restart entropy ledger. Entropy balance with force d
and Young's inequality separately give

    D'<=-(gamma sigma^2/2)I_p+E[d_t^2]/(2 gamma sigma^2).

Thus ignoring remaining dissipation costs at most J/(2 gamma sigma^2) in a
restart budget, under the declared Fokker-Planck regularity. Relative entropy
has no triangle inequality that could replace this argument.

## Actual history and adaptive reuse

Appending a report Y increases the relevant entropy by exactly

    D(rho_SRY||pi x rho_RY)-D(rho_SR||pi x rho_R)=I(S:Y|R).

A b-bit report costs at most b log(2). Count all retained/accessible reports,
not only the final arm. If the arm is computed from retained Y and fresh
randomness, do not double-count it. A discarded record cannot be treated as
absent from a reference that still has access to it. Physical reset/erasure
costs are additional.

Fresh randomness is independent when drawn. A private clock later correlates
with the state through the selected evolution time, but conditioning on the
clock gives an average of contractive fixed-time relative entropies. Its
continuous Shannon entropy is not inserted as a spurious infinite charge.

At round j with actual retained history h, let D_h be the incoming conditional
entropy and C_h the new conditional trigger density cap. Then

    delta_j<=sqrt[E_h(C_h D_h)/(4 gamma)].

A uniform C_j gives sqrt[C_j E_h D_h/(4 gamma)]. Replacing E(C_h D_h) by
E(C_h)E(D_h) needs an independence argument. Work, backaction and records must
first be included in the actual incoming budget.

Let A_j be the actual history-adaptive kernel and I_j the same waiting policy
followed by the exact fair-arm momentum reset. Each process uses its own
history through the same specified policy. If on actual input P_{j-1},

    TV(A_j P_{j-1},I_j P_{j-1})<=delta_j,

then for ideal input Q_{j-1}, contraction gives

    TV(A_j P_{j-1},I_j Q_{j-1})
       <=delta_j+TV(P_{j-1},Q_{j-1}).

Induction yields full-campaign error <=sum_j delta_j. This uses preparation
bounds only along actual histories; it never transfers an actual-history
entropy budget to an unobserved ideal-history distribution. Adaptive clocks
need not make the histories identical. The ideal retained source can still
produce dependent outcomes: iid specimens or iid error bars do not follow.

## Physical comparator

If independent momentum replacement while retaining all other coordinates
is already supplied, direct reset followed by q_b sampling is a stronger
ordinary baseline that can avoid this waiting. A thermal full momentum swap
or controllable thermostat gain can also change the cost. The selection
operation must be assessed at its actual observation/trigger interface.
Factory hidden-loading access is separate; it cannot remain covertly
available only to the claimed protocol.
