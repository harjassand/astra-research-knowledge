# Finite moment deflation cannot make the raw hard-sphere correction subcritical

29 October2026. A second, stronger test of the proposed near-equilibrium
operation. This is not merely another selected negative kernel entry. It
rules out ALL fixed finite-dimensional moment control spaces in the stated
one-velocity absolute-kernel receiver, and gives the sharp asymptotic factor2.
Historical priority is UNKNOWN. Other norms/references, correlated states and
whole-semigroup operations are not excluded.

## 1. Candidate operation and equally informed control

Write a perturbation as g=M u and use the actual linearized hard-sphere
operator from POSITIVE_RESIDUAL_BARRIER.md. In relative variables,

    du(v)/dt=int u(w) A_v(dw)-nu(v)u(v),
    A_v(dw)=M(w)[4 exp(|v_perp|^2/2)/|v-w|-|v-w|]dw.

If known moments imply int F_j(w)u(w)M(w)dw=0, subtracting any P_v in their
span F leaves this generator unchanged. This is a serious ordinary control
variate, stronger than ignoring the exact conservation constraints. Collision
invariants1,w1,w2,w3,|w|^2 have exactly zero moments for an invariant-matched
perturbation at all times. Additional fixed moments may be granted for the
negative result; they are not silently acquired in a positive algorithm.

A natural bounded signed query would sample the controlled absolute kernel
and let nu kill the lineage. It needs an absolute gain rate below nu, or
another separately paid stabilization. Can finite moment deflation do that?

## 2. Sharp theorem

Let F be ANY fixed finite-dimensional subspace of L1(M dw) containing constants.
Coefficients may depend arbitrarily on v. Define

    J_F(v)=inf_(P in F) int |dA_v/dw-P(w)M(w)|dw /nu(v).

Then, along every direction as |v| tends to infinity,

    lim J_F(v)=2.                                      (D)

In particular no such F supplies a uniform substochastic/subcritical bound
J_F(v)<=1, let alone1-eta. The theorem includes ALL finite polynomial moment
deflations, not only mass, momentum and energy. It is not a lower bound on
the complexity of every exact hard-sphere sampler.

## 3. Native gain mass escapes; the loss stays tight

Decompose A_v=G_v-H_v into positive measures,

    G_v(dw)=4 M(w)exp(|v_perp|^2/2)/|v-w| dw,
    H_v(dw)=|v-w| M(w)dw.

Maxwellian stationarity LM=0, with the exact kernel convention, gives

    G_v(R3)=2nu(v), H_v(R3)=nu(v).

This is also the usual separate gain/loss balance, not an assumption about
the unknown perturbation. Let m1=int |w|M(w)dw. Triangle inequality gives

    ||v|-nu(v)|<=m1, hence nu(v)/|v|->1.

For every fixed radius R and |v|>R, |v_perp|=|w_perp|<=R on its ball, so

    G_v(B_R)<=4 exp(R^2/2)/(|v|-R),
    G_v(B_R)/nu(v)->0.                                 (6)

Thus G_v/nu has mass2 escaping every fixed compact velocity region.
Conversely H_v/nu is a tight probability family; in fact it converges in
total variation to M dw, since

    int ||v-w|/nu(v)-1| M(w)dw <=2m1/nu(v)->0.          (7)

The gain/loss signed kernel is asymptotically split between escaping mass2
and a tight negative mass1. This is native large-velocity hard-sphere geometry.

## 4. Every bounded set of finite moment controls is uniformly tight

Choose any minimizing/near-minimizing P_v. Taking P=0 gives cost<=3nu.
Thus it is enough to consider controls with cost<=3nu+o(nu), for which

    int |P_v|M /nu <=6+o(1).

The unit ball of a finite-dimensional subspace F of L1(M) is compact. Hence
its normalized controls are uniformly tight: for each eta>0 one can choose
R so that int_(|w|>R)|P_v|M/nu<eta for all such controls. Explicitly choose
a basis of F; finite-dimensional norm equivalence bounds coefficients by
their L1 norm, and the finitely many basis tails all tend to zero.
No well-conditioned or cheaply acquired basis is granted; this negative
statement permits any fixed F, including badly conditioned ones.

Outside this R, triangle inequality and (6)--(7) give

    int |dA_v/dw-P_v M|/nu
      >=G_v(B_R^c)/nu-H_v(B_R^c)/nu-int_(B_R^c)|P_v|M/nu
      >=2-2eta-o(1).

Take first |v| to infinity, then eta to zero. This proves liminf J_F>=2.

## 5. Matching upper bound

Since constants belong to F, choose P_v=-nu(v). Then

    A_v-P_v M dw=G_v+[nu(v)-|v-w|]M(w)dw,
    int |dA_v/dw-P_v M| <=2nu(v)+2m1.

The last inequality follows from (7). Thus limsup J_F<=2, proving (D).

## 6. Scientific consequence and exact boundary

The most direct conservation-aware repair of the signed correction therefore
fails: even granting any fixed finite set of moment controls, the raw
relative-Maxwellian absolute gain is asymptotically TWICE its loss/killing
rate. This cannot supply the earlier Maxwell sampler's norm-one mark or a
uniformly subcritical one-velocity correction tree. Adding more fixed moments
does not change the asymptotic obstruction.

This does NOT refute time-block spectral cancellation; an adapted weighted
norm/reference; growing velocity-dependent control families; positive
multi-particle couplings; or an operation estimating the integrated semigroup
without sampling this absolute instantaneous kernel. Such alternatives need
their own actual sampler/cost bridge. Neither a spectral gap nor signed
LVDSMC output supplies that bridge automatically. The faster-time exact
normalized hard-sphere target remains NOT_ACQUIRED in this branch.
