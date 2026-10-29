# The one-simplex inverse form is not CQ conditional Umegaki order

30 October 2026. Completed analytic obstruction to the proposed representation, not a no-go for every CQ algorithm. The frozen23-file classical construction is unchanged. Eriksson's v3 support theorem does NOT assert the pairwise representation refuted here; no error in that theorem is claimed.

## 1. Precisely the candidate being refuted

For a CQ channel i->tau_i, Q_i>0 with sum Q_i=I and vectors u_i with sum u_i=0, define

    W_tau=sum_i tau_i tensor Q_i,
    Z_tau=sum_i tau_i tensor u_i,
    F_tau(Q,u)=Tr_out Z_tau^* W_tau^{-1} Z_tau.

Z maps the output Hilbert space into output tensor reference. The trace is essential; no implicit conjugation or replacement of Umegaki by an inverse metric is allowed. Common zero output support is compressed first. The active/vacuum construction supplies a lower witness family of this type. It does NOT supply an all-input upper representation when the tau_i fail to commute.

The candidate assertion would say J_K<=c J_L for all quantum references iff F_K<=c F_L for every such Q,u. Here J is EXACTLY the previous subtracted quantity D(output pair)-D(reference pair). We refute the assertion with reference dimension1, so it also fails for equal-reference comparison. We do not assume that equal-reference and conditional comparison coefficients coincide for general CQ outputs.

## 2. An exact all-level blindness of the inverse form

Let tau_i=|psi_i><psi_i|, where the normalized psi_i form a linearly independent basis of the output space. Put V=[psi_1,...,psi_n]. It is invertible, even when its columns are nonorthogonal. Then

    W_tau=(V tensor I) diag(Q_i) (V^* tensor I),
    Z_tau=(V tensor I) diag(u_i) V^*.

Consequently

    Z_tau^* W_tau^{-1} Z_tau
       = V diag(u_i^* Q_i^{-1} u_i) V^*,

and the trace equals sum_i u_i^* Q_i^{-1}u_i, since ||psi_i||=1. This is EXACTLY the form for the classical identity channel, at EVERY finite complex reference dimension and every admitted Q,u. Thus the candidate declares all invertible normalized pure preparations equivalent to a perfectly distinguishable classical experiment.

They are not Umegaki equivalent. For the SAME binary source throughout the subsequent comparison, take

    tau_0=|0><0|,       tau_1=|+><+|,
    |+>=(|0>+|1>)/sqrt(2).

The target is the classical identity experiment. At uniform scalar input base and tangent(1,-1), the input BKM metric is4. The output base has Bloch radius1/sqrt2 and its tangent is perpendicular to that Bloch direction; direct divided differences give output metric

    2 sqrt2 atanh(1/sqrt2) < 4.

Thus some faithful input pairs violate J_identity<=J_tau, while the proposed inverse inequality holds with equality1 at every free level. Section4 and certify_counterexample.py pay an explicit finite pair, rather than relying only on an infinitesimal argument.

This congruence blindness is the familiar RLD/reverse-estimation geometry, not a claim that RLD and Umegaki were previously believed interchangeable. Matsumoto's primary reverse-estimation papers and HRSF Section6.2 explicitly distinguish those geometries.

## 3. The failure persists strictly inside faithful prepared outputs

A natural continuation of the SAME0,+ pair removes a rank-boundary explanation. Let

    tau_0(r)=(I+r Z)/2,   tau_1(r)=(I+r X)/2,
    r=4/5,

so both output states have eigenvalues9/10,1/10. Let the target be the strictly positive binary classical channel

    K=[5/6  1/6],
      [1/6  5/6].

These are a depolarized continuation and a noisy identity continuation, not a stochastic search or a new data source. For binary input, Q_1=I-Q_0, so spectral calculus reduces the entire all-free-level inverse comparison to scalar t in[0,1]. Put z=2t-1 and Delta=tau_0-tau_1. The scalar reference form is

    g_tau(t)=Tr Delta[t tau_0+(1-t)tau_1]^{-1}Delta
            =4 r^2/[2-r^2-r^2 z^2]
            =4 a_eff^2/[1-a_eff^2 z^2],
    a_eff^2=r^2/(2-r^2)=8/17.

The target has signal a=2/3 and g_K(t)=4a^2/[1-a^2z^2]. Their ratio is

    (17/18) (1-(8/17)z^2)/(1-(4/9)z^2) <= 17/18,

with equality at t=1/2. Therefore the candidate all-level coefficient is EXACTLY17/18<1. Nevertheless the finite faithful pair below has D_K>D_tau. This is a strict-margin false admission even for full-rank rational prepared states. No numerical sampling of Q,u is used to establish that universal inverse inequality.

## 4. Finite native hypotheses and arithmetic

Use scalar classical input hypotheses p=(3/4,1/4) and q=(1/2,1/2); their reference is the same one-dimensional state, so the reference-relative-entropy subtraction is zero. All input hypotheses are faithful. The average output states for both pure and faithful-output cases are also full rank. The script evaluates their exact2-by2 relative-entropy formulas using rational intervals for square roots and logarithms; every logarithm is enclosed by a positive atanh series with an explicit geometric remainder, and every square root by rational bisection. Floating eigenvalues/logarithms are not proof premises.

The script checks the pure source's rational state identities, the faithful continuation's determinants and commutator, and the exact scalar-polynomial inequality proving its all-level17/18 coefficient. COUNTEREXAMPLE.json records finite divergence intervals, ratio intervals, margins and actual computation cost. The conclusion is only representation failure: no claim that all CQ synthesis is impossible, no reference-size/physical/preparation claim and no new generic RLD separation is made.

## 5. The surviving operation and the exact remaining gate

The true BKM form has BOTH left and right prepared-state multiplication. At reference blocks A_i>0 with M=sum A_i, a BKM parameter s gives Z=s L_M+(1-s)R_M on Hilbert-Schmidt reference space. Set

    Q_i^L=Z^{-1/2}s L_Ai Z^{-1/2},
    Q_i^R=Z^{-1/2}(1-s)R_Ai Z^{-1/2}.

Their combined sum is I, and the output denominator is

    W_tau=sum_i L_tau_i tensor Q_i^L + R_tau_i tensor Q_i^R.

For a_i=Z^{-1/2}H_i, v=sum a_i and u_i=a_i-(Q_i^L+Q_i^R)v, the exact gauge cancellation leaves

    <sum_i |tau_i> tensor u_i, W_tau^{-1}
       sum_i |tau_i> tensor u_i>,   sum u_i=0.

This formula was independently derived by this worker and root. Universal comparison over TWO unrestricted positive effect families is sufficient for conditional Umegaki order and has a definite free-pencil SDP. Necessity is NOT granted: actual left/right multiplication families have compatibility before the common congruence. Our next computation examines this upper operation on the SAME0,+ inverse experiment and confronts unambiguous discrimination as a strong ordinary upper. Equal-reference and conditional comparison must remain separate; the old classical equality of those coefficients cannot be imported here.
