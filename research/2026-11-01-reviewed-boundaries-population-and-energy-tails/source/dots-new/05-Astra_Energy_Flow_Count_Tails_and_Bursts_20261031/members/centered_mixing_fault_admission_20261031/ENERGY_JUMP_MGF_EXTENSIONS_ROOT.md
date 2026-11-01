# Time-local and joint energy-count certificates

Status: new root extensions, independent review pending. The basic generator,
actual-count, bounded-energy and history-uniform control premises remain those
of ENERGY_JUMP_MGF_ROOT_CANDIDATE.md, including its explicit counted-intervention
and local detector-mark accounting. No hardware or priority claim.

## 1. A better constant tilt using an optimized Young split

For q>=0 with g=kappa-2h q>0, choose theta=g/(2kappa),
a=4q/g, W=I+aH and r=8q C^2/g^2. The Young bound is

  i sqrt(lambda) a[V,H]<=lambda a theta kappa H
                          +a C^2/(theta kappa) I.

The remaining H coefficient is -a[kappa(1-theta)-2h q]+2q=0.
Thus the same MGF conclusion holds with these constants. The allowed tilt is
q<kappa/(2h); the earlier half-split threshold was sufficient, not intrinsic.
At q=0 take a=r=0 by continuity. Zero-tilt expected-count constants are unchanged.

## 2. Backward time-local counting windows

Let q(t)>=0 be a bounded deterministic piecewise-continuous counting weight on
[0,T]. Define a(T)=0 by

  a'=lambda[(kappa/2-2h q(t))a-2q(t)],
  a(t)=2lambda int_t^T q(u)
        exp{-lambda int_t^u[kappa/2-2h q(v)]dv}du >=0.

With W_t=I+a(t)H and r(t)=2a(t)C(t)^2/kappa, the coefficient of H in
partial_t W_t+L_q(t)*W_t vanishes after the same half-Young split. Therefore

  E product_{jump times t_j}(1+q(t_j))
      <=Tr(W_0 rho0) exp(int_0^T r(t)dt).

For actual exp(s(t)) counting weights take q(t)=exp(s(t))-1. Before a counted
window, a(t) decays backward at the source relaxation rate when q=0, so preceding
energy injection is charged without treating unrelated future time as counted.
The formula works for any bounded finite-horizon q. If q exceeds the stationary
threshold, however, a and the bound can grow exponentially in lambda; this is
NOT the earlier lambda-uniform resource advantage. Instruments must contract
the current W_t in aggregate for every prior record when uncounted; counted
interventions need the corresponding tilted bound or separate count accounting.
Initial warm energy and
all admitted interaction exposure remain charged by the displayed quantities.

## 3. Several local sources, without independent data

Assume the FULL generator decomposes as the sum of admitted source generators
lambda_i G_i and interactions sqrt(lambda_i)V_i, plus Hamiltonians commuting
with all H_i. Source spaces are disjoint, H_i act only on source i, and V_i may
act on shared data but commutes with all H_j for j!=i. Each G_i acts only on its
source. Any other term needs a separately proved product-observable bound.

Choose individual backward weights a_i and W_i=I+a_iH_i, with their own q_i,
kappa_i,h_i,C_i,lambda_i. For W=product_i W_i, the factors commute and
the local generator contributions satisfy

  (partial_t+L_q*)W <=sum_i r_i product_{j!=i}W_j
                      <=(sum_i r_i)W.

Thus the joint generating functional is at most

  Tr[(product_i W_i(0))rho0] exp(int sum_i r_i(t)dt).

The initial expectation CANNOT be replaced by a product of initial mean
energies for correlated sources. Joint dark initialization makes it1. A general
safe but possibly expensive substitute is product_i(1+a_i(0)h_i).
Shared data, even entangled, need not factor. Adaptive instruments must contract
the WHOLE product observable conditionally on every prior record; separate
single-factor contraction alone is not the required premise.

This is joint count control, not automatically a local-stochastic logical-fault
theorem. Reused source memory, clustered emissions, coherent no-jump logical
action, actual observation/control failures and the consumer's event definition
must still be handled. Independent thinning uses q_i=eta_i(exp(s_i)-1) only when
the actual instrument supplies that classical thinning.

## 4. The dark-source scope is forced by the premises

For any stationary source state sigma, 0=Tr(sigma G*H)<=-kappa Tr(sigma H)
and H>=0 imply support(sigma) subset ker H. Since sum L_j*L_j=2H, each counted
L_j annihilates that support. A faithful stationary sigma would force H=0 and
all counted L_j=0. Thus nontrivial examples are externally driven dark/draining
sources, not generic thermal sources emitting forever at stationarity. A thermal
variant with G*H<=-kappa H+bI would need a separate, explicitly charged theorem.
