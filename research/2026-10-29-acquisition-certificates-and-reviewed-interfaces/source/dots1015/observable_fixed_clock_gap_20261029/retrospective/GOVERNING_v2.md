# Model-free retrospective empirical-frame readiness diagnostic
2026-10-29. Additive author derivation, independent review pending. Does not modify fixed-comparator observable v1. This is a retrospective joint-event statement, NOT future prediction, policy regret or conditional accepted-error certification.

## 1. Retain the observable loss offset
Use every interface, neutral two-stage preflight filtration and finite-clock/gap bound from observable v1. No common hidden frame or small comparator-defect promise is imposed here.

For a real probe the native estimator is
 delta_hat(C)=3/4-(9/4)yz C_ab-(81/4)yzuv C_ab C_cd,
so it lies in[-87/4,93/4] for EVERY rotation. Write its nonconstant quaternion polynomial h_hat=sum_j beta_j phi_j(q), with g_hat=2beta and x=(phi+1)/2. The importance-weighted feedback identity is

 delta_tilde_it(C)=c_it+g_it dot x(C),
 c_it=I_probe*3/(4p)-(1/2)sum_j g_it,j.

It is unbiased for the actual current delta_it(C). On nonprobe rounds both c and g are0. The observed cumulative offset therefore needs only the existing feedback bank plus the shared probe count:

 Cobs_i=3 N_probe/(4p)-(1/2)sum_j G_iT,j.

The native estimator interval persists for every x in conv(K), by affine linearity. In particular a_it=grad Phi(G_(i,t-1)) lies in conv(K), since it is the mean of exact minimizing features. Thus c_it+g_it dot a_it has conditional range inside[-87/(4p),93/(4p)], including its nonprobe0 value. This uses the actual native estimator, not a generic loose35-coordinate bound.

## 2. Center one martingale before introducing any comparator
Let z_it=E[g_it|H], xbar_it=E[x_it|H]. Define

 Y_t=sum_i {delta_it(C_it)-[c_it+g_it dot a_it]
                         -z_it dot(xbar_it-a_it)}.

Current feedback/action independence makes its conditional mean0: the action-independent true offset cancels between the first and second expectations. Its conditional range has length at most m(2+45/p). No independence across edges is assumed. Conditional Hoeffding therefore gives, with probability>=1-delta_m,

 sum_t Y_t <= m(1+45/(2p))sqrt[2T ln(1/delta_m)].       (R1)

The observable-gap supermartingale of v1 independently gives sum_(t,i)E[e_it|H]<=U_e, with failure allowance delta_e. Its conservative rational substitute Ubar_e=2Eobs+2mB ell_e remains valid.

## 3. Pathwise minimization, safe retrospective candidates
The pathwise potential inequality gives

 sum_(t,i)g_it dot a_it
 <=sum_i [Phi(G_iT)-Phi(0)]+Vobs/(4R).

Concavity/mean-zero smoothing gives Phi(G)<=phi0(G)=min_(x in K)G dot x. This is a PATHWISE inequality at every final observed G. Consequently, for ANY rational candidate tuple qhat_i chosen AFTER seeing the complete actual record,

 Phi(G_iT)<=G_iT dot x(qhat_i).

No comparator was inserted into the martingale or selected after a uniform-concentration argument. The same probability event therefore works simultaneously for all such candidate choices. This does NOT compare the learner with the true counterfactual performance of a hindsight-selected controller.

Define the exactly computable retrospective score

 Lemp(qhat)=sum_i [Cobs_i+G_iT dot x(qhat_i)]
           =3m N_probe/(4p)+(1/2)sum_i G_iT dot phi(qhat_i).

Combine(R1), the pathwise inequality and the variable-gap bias argument to obtain, with probability>=1-delta_e-delta_m,

 Gactual:=sum_(t,i)delta_it(C_it) <= Lemp(qhat)+Hret,      (R2)

 Hret=mdR/4+Vobs/(4R)
      +720 sqrt[(mT/R)U_e+m²dT²/M]
      +m(1+45/(2p))sqrt[2T ln(1/delta_m)].

This is an observable upper bound on the actual selected losses, conditional only on the trusted/nonanticipating interface, not on an unknown common frame. The empirical score can be negative. On the simultaneous good event the whole RHS is necessarily nonnegative because Gactual>=0; an apparently impossible negative bound is a rare certificate-failure event, not proof of negative physical loss. Replacing the RHS by its maximum with0 is a safe looser numerical bound.

The retrospective candidate need not be a certified global empirical optimum. ANY candidate gives an upper bound on the pathwise minimum. A better candidate tightens the diagnostic; a lower bound alone cannot replace its score. It may be computed by one additional paid fixed-budget classical query at G_iT, or chosen from available candidates. No extra quantum source calls are needed. The retrospective tuple is not deployed into the already completed source history and need not be a prediction of future noise.

## 4. Model-free joint readiness consequence
Use the unchanged candidate-conditioned validation martingale from v1. Let Uret=max(0,Lemp+Hret) with conservative rational upper bounds. Compute

 a alpha_n Uret +sqrt[(T/2)ln(1/delta_v)] < b+1.          (CERT-R)

Let Cert-R also require verified code deployment and no non-source abort. Under the UNMODIFIED guarded protocol with J<=sT/2,

 Pr[reject AND Cert-R] <=delta_e+delta_m+delta_v+exp(-sT/8). (R3)

This now needs no exact-frame or approximate-symmetry promise. Arbitrary source noise can make Cert-R fail always; the theorem supplies no lower bound on Pr[Cert-R]. Consequently it is neither a universal positive-yield theorem nor Pr[reject|Cert-R] bounded by the displayed RHS. Publishing or postselecting the diagnostic as part of a new accepted quantum instrument needs separate interface/error analysis. Original model-free accepted soundness is not automatically a normalized conditional error claim on this diagnostic event.

## 5. Interpretation and obligations
This removes the hidden fixed-comparator defect from the RETROSPECTIVE diagnostic by preserving the observable estimator offset and using the pathwise empirical minimum before the martingale bound. It does not prove low empirical score on all sources, predictable future preservation, an advantage over equally informed adaptive conventional testing, or favorable finite constants. Fixed-clock implementation, gap certificates, control privacy, trusted buffers and actual quantum acquisition remain separate paid obligations.

The final empirical score is not the fidelity of any quantum code and may be conservative. Its validity comes from the shared feedback, online potential and actual-memory operational transfer. The diagnostic can be useful for auditing whether a particular run's recorded acquisition and solver work support a readiness claim at the stated joint-probability scope; it is not an ex ante guarantee that the run will be easy.
