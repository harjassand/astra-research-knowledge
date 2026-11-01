# Independent receipt: killed CP subchannel transfer

2026-11-01. This audits the root's proposed killed-subchannel lemma supplied in the task message. **Mathematical PASS under the explicit finite-bandwidth and protected-factor hypotheses below.** It is an analysis construction, not a physical absorbing reservoir or a microscopic implementation theorem.

## 1. Exact generator and CP property

Let P be a projector, R=I-P, and [P,F]=0 for a positive observable F (in the intended application F=exp(aQ)). Define on P-supported trace-class operators

    L_kill(rho)=-i[PHP,rho]
      +sum_j P J_j P rho P J_j† P
      -(1/2)sum_j {P J_j†J_j P,rho}.

Write L_j=PJ_jP and

    K=sum_j P J_j†R J_j P >=0.

Then L_kill is the ordinary Lindblad generator with H_P and jumps L_j, minus {K,rho}/2. It generates a completely positive trace-NONINCREASING propagator. One proof embeds an auxiliary absorbing copy with jump sqrt(K) into that copy and restricts the resulting CPTP evolution to P. This auxiliary copy is solely a proof device. For time-dependent generators use the same bounded/measurable well-posedness conditions as in the parent channel comparison.

The trace derivative is -tr(K rho)<=0. The killed state is never renormalized in this argument.

## 2. Adjoint compression and Foster inheritance

Put F_P=PFP. Direct expansion, using only [P,F]=0, gives exactly

    L_kill*(F_P)=P L*(F)P
      -sum_j P J_j† R F R J_j P.

The last term is positive semidefinite because F>0. Thus L_kill*(F_P)<=P L*(F)P. This works for GENERAL jumps: no conditional-Pauli form, injectivity, downhill direction, or positivity of an outgoing energy increment is required.

For example, if the actual full generator has the restricted Foster bound

    P L*(F)P <=-k n F_P+D n exp(a theta n)P,

then for tau_t=K_(t,0)(rho_0), rho_0 supported in P,

    d tr(F_P tau_t)/dt
      <=-k n tr(F_P tau_t)+D n exp(a theta n)tr(tau_t)
      <=-k n tr(F_P tau_t)+D n exp(a theta n).

Therefore the same Gronwall moment bound holds. The shell probability used below is the UNNORMALIZED p_j(t)=tr(S_j tau_t), not a conditional probability given survival. Treating it as a normalized state would be an error.

The lemma transfers an ALREADY PROVED actual-generator Foster inequality. It does not create that inequality for a new sensor/progress apparatus, nor establish [P,F]=0 for a proposed dressed projector.

## 3. Precise finite-bandwidth hypotheses

Let S1,S2<=P be one- and two-step boundary projectors. For each Hamiltonian summand H_i and jump J_j it suffices to establish

    R H_i P(P-S1)=0,
    R J_j P(P-S1)=0,
    R J_j†J_j P(P-S2)=0.

The usual label-component construction with Q cutoff B and actual move increments <=b gives S_r=P 1_{Q>=B-rb}: every one/two-step path from a deeper interior point remains in the admitted component. This requires the ACTUAL transition/component structure. Ordinary spatial locality alone does not imply these annihilation identities, particularly after non-Clifford/progress dressing.

The two-step condition remains necessary for general jumps because of J†J. The earlier X1+X2 counterexample to a one-step anticommutator bound remains applicable here.

## 4. Actual-minus-killed bound

Let tau=P tau P>=0 with tr(tau)<=1. For any X=XS_r,

    ||X tau||_1 <=||X|| sqrt(tr(S_r tau)tr(tau))
                 <=||X|| sqrt(p_r).

For one jump set L=PJP, E=RJP and Z=R J†J P. The jump-output difference is

    J tau J†-L tau L†=E tau J†+L tau E†,

whose trace norm is <=2||J||^2 sqrt(p1). The anticommutator difference between actual and killed generators is exactly

    -(Z tau+tau Z†)/2,

with ||Z||<=||J||^2, so its norm is <=||J||^2 sqrt(p2). Thus

    ||(D_actual[J]-D_kill[J])(tau)||_1
      <=3||J||^2 sqrt(p2).

For a Hamiltonian summand the difference is the off-block commutator, bounded by 2||H_i||sqrt(p1)<=2||H_i||sqrt(p2). Hence, if sums of the relevant local norms obey

    sum_i ||H_i||<=h_all n,
    sum_j ||J_j||^2<=Gamma_all n,

variation of constants with the actual CPTP propagator yields

    delta(T):=||rho_actual(T)-tau_T||_1
      <=n(2h_all+3Gamma_all) integral_0^T sqrt(p2(t))dt.

Replacing 3 by 4 is a valid conservative convention. ALL ideal and noisy terms must be included unless their off-block contribution is separately proved zero. A bath-only Hamiltonian commuting with P contributes zero and need not be charged by an infinite/global bath norm. The comparison is unchanged by arbitrary untouched reference factors.

For F=exp(aQ), a moment bound <=C exp(a theta n), cutoff B=beta n and the verified two-step shell imply

    delta(T)<=n(2h_all+3Gamma_all)T sqrt(C)
              exp(ab)exp[-a(beta-theta)n/2].

This comparison involves subnormalized killed states throughout. It does not assume their trace remains near one; proximity to one follows from the same comparison when its bound is small.

## 5. Protected factorization must include J†J

Assume a fixed decoding identifies P H with H_L tensor H_G, with arbitrary external reference R untouched. Sufficient conditions are

    PHP=I_L tensor H_G,
    P J_j P=I_L tensor L_j,G,
    P J_j†J_j P=I_L tensor A_j,G

for every actual term, with the usual sum/time qualifications. Then the killed propagator factors as id_L tensor K_G, where K_G is CP and trace-nonincreasing. The positive killing operator is itself gauge-only.

Internal PJP flatness ALONE is insufficient: escaping amplitudes can reveal protected information through PJ†JP. For a Pauli-based proof, include every needed local component of J†J as well as J and H in the protected-flatness argument. Products may enlarge support/bandwidth constants; no theorem follows merely by calling them local. Direct factorization is an equally valid alternative.

### Necessary-hypothesis counterexample

Take P spanning logical |0>,|1>, an outside state |e>, H=0, and J=|e><1|. Then PJP=0 is trivially logical-flat, but PJ†JP=|1><1| is not. Start at |+>. At t=2 log 2 the killed logical matrix is

    tau_L=[[1/2,1/4],[1/4,1/8]].

The initial-minus-killed matrix has determinant -1/16, hence is NOT positive. Lost trace is 3/8. The actual state is embedded tau plus (3/8)|e><e|, so actual-minus-killed trace norm is 3/8. If the outside state decodes to |0>, decoded logical error is sqrt(13)/4>3/4=2 delta. Thus the proposed logical conclusion genuinely fails if J†J flatness is omitted. `killed_flatness_counterexample.py` checks these exact rational quantities. This is not a counterexample to the fully stated lemma, which explicitly requires that missing hypothesis.

## 6. Correlated gauge states: the exact positive-deficit statement

Under full factorization, let E=K_G†(I_G), so 0<=E<=I_G. For ANY initial logical/reference/gauge state rho_LRG, including arbitrary correlations, the decoded killed output is tau_LR. Its deficit is

    rho_LR-tau_LR
      =Tr_G[(I_LR tensor sqrt(I_G-E)) rho_LRG
                              (I_LR tensor sqrt(I_G-E))] >=0.

Its trace is p_loss=1-tr(tau_T). Therefore its trace norm is exactly p_loss. It is generally NOT a scalar multiple of rho_LR, and normalizing the surviving state need not preserve logical information when gauge is correlated.

Equivalently the gauge-only CP map X -> tr[(I-E)X] sigma_G, for any fixed gauge state sigma_G, completes K_G to a trace-preserving map. Tensoring this complement with identity on logical/reference systems preserves the original protected marginal. This is a time-T analysis completion, not a claim that the actual escaping dynamics implements a logical recovery.

Let D be any CPTP terminal decoder agreeing with protected-subsystem decoding on P. Then

    ||D(rho_actual(T))-rho_LR||_1
      <=||rho_actual(T)-tau_T||_1+p_loss
      <=2 delta(T),

because tr(rho_actual-tau_T)=p_loss and trace norm dominates absolute trace. Thus the root's factor-two output bound is valid even with logical-gauge correlations, precisely in this unnormalized positive-deficit sense.

For a fixed independent bath input this can be stated as a restricted-code channel/diamond bound. For correlated initial baths retain the pointwise joint/output formulation and do not infer a system-only channel without an initialization map.

## Scope and closure

The killed-channel generalization correctly removes the need for reflected CPTP drift transfer or individually uphill-censorable jump structure. It therefore applies to more general microscopic sensor/progress/reset jumps ONCE their full Foster inequality, [P,F]=0, finite-bandwidth identities, complete protected factorization, physical costs and initialization are earned.

It does not by itself synthesize those jumps, establish their protected flatness, or supply a physical CP complement. No hardware practicality or novelty is certified. The standalone lemma and its necessary qualification are now independently received; no algebraic blocker remains under those hypotheses.
