# Scale-invariant parameters and finite-error receiving plan

31 October 2026. UNREVIEWED companion to the two-sector excursion and finite-matrix arithmetic candidates. No whole theorem is asserted before the joint review. The exact source/activity candidate is a premise, not retrospectively accepted by this note.

## 1. Physical invariance and input costs

Define

    mu=lambda*c*T, B=b^2*T/c, R=tr(C0)/c,
    D=||D0||/c, Pi=1/pi_min, H=alpha0*T.

Replacing base Q by Q/c, lambda by lambda*c and centered K by K/sqrt(c) leaves the physical process unchanged. Thus c is not a gratuitous absolute unit. Explicit Q dimension d, stationary preparation, certified gap acquisition, input bits and actual controlled coupling encodings remain paid. A nonzero stationary mean belongs to H0 and its charged H; no centering step hides a sqrt(lambda) deterministic action.

The desired conditional complexity is polynomial in

    d, 1+H+B+p, R, D, Pi, input lengths,
    log(2+mu), log(1/epsilon),

plus supplied operator-encoding and consumer-instrument costs. It is for an explicit finite source, not a succinct exponentially large state space or an unknown chain.

## 2. Two branches

For mu<=64B, the free reservoir Hamiltonian action is at most mu*D<=64BD. Jump normalization action is at most mu*R<=64BR. Centered coherent action is sqrt(mu*B)<=8B. Ordinary high-precision Lindblad simulation can therefore serve as a source-conditioned low-rate branch without a hidden unbounded microscopic action. Its access-model theorem and costs still must be received explicitly.

For mu>=64B, let x=t/T. The two-sector parameters satisfy

    gT=sqrt(mu B), kappa T=mu/2-sqrt(mu B), sT<=8B/3.

Use windows tau/T<=1/(16B), with W<=ceil(16B)+p+1. The first-event enclosing power-of-two normalization can be chosen

    64sqrt(1+R)<=A<128sqrt(1+R).

The exact source activity tail, conservatively replacing B0 by b, gives

    M=ceil(12B Pi^2+4Pi log(100/epsilon))+1,
    S=M+W+2.

This is an actual-jump cap. Virtual bridge/self-insertion caps are different and are derived from the conditional exponential bound in the excursion note.

## 3. Correct event endpoint semantics

In the four-sector-pair event LCU, the final sector label is the virtual PRE-JUMP sector. It must be fast. Apply the actual contraction L_e^0/ell_e after that fast-ending word. Its physical output is |y> and can have both ground and fast components. Never project its output back to fast, never replace it by the ground state, and never interpret the pre-jump label as a physical output label. The private endpoint and inner source labels are unprepared after averaging, while the actual reservoir survives the first-event instrument.

This is essential because a general Markov edge jump is not the amplitude-damping reset of an independent qubit. The first-event completeness identity holds for arbitrary retained reservoir inputs only with the actual jump operator.

## 4. Finite error parameters, with all new error mechanisms exposed

Use the reviewed exact attenuated amplification with degree d_A=2A+1. For e_step=epsilon/(100S), a deliberately conservative choice is

    beta=(e_step/(10^6 d_A^2))^4,
    sigma=(beta/[100 A(E+1)])^4,

where E is the number of nonzero directed edges, E<=d(d-1). Constant factors for the new source operations must be fixed in the final joint proof; the powers here have ample room but do not excuse omitting a term.

A dimensionless physical generator bound is

    L=1+2H+2mu D+2sqrt(mu B)+2mu R.

The count-augmented exact process frozen after M jumps has the same bound up to a fixed universal factor, independent of the count-space dimension. Choose x_min<=e_step/(100L). Compare private representative event times against this exact capped future, not against a claim that continuous and rounded public timestamps are close in TV.

For the event envelope, after canceling ell_e analytically, the derivative of the normalized event amplitude with respect to physical t is at most

    sqrt(lambda)*c*h_eff/(32b)+kappa,
    h_eff=||H0||+lambda||H_env^0||+sqrt(lambda)b+lambda||C0||/2.

Multiplication by T expresses this as a polynomial in mu,B,D,R,H and inverse sqrt(B), with encoded parameter lengths paid. In the high-rate branch b>0; absent edges are omitted. Any tiny b enters precision through its input logarithm, not an uncontrolled rejection count.

The outer density is a truncated-exponential/uniform mixture. Excluding uniform tails and threshold strips of width sigma gives an L2 error proportional to the square root of their total measure. On retained coordinates the quantile and endpoint-floor estimates from the fixed-mode proof apply with exponential rate2kappa. In normalized time a valid local floor is proportional to

    sigma*min(x_min,1/(1+2kappa*T)).

Choose the outer time approximation so both the normalized-amplitude perturbation and L times its error are below their per-call budgets.

For the inner source, its total unconditioned event intensity is bounded by max(s,d_down)+g. Apply a single global near-endpoint/near-tie cut before endpoint conditioning. Divide bad-event probabilities only by the original endpoint probability. This retains common lower bounds for every recursive bridge denominator; the uniform precision involves their logarithmic inverses.

Changing a fast-interval duration by delta ell changes Poisson(g*ell) by TV at most g|delta ell|. This follows by adding an independent Poisson increment to the longer interval. Conditional on equal counts, couple the uniform insertion positions by the same unit uniforms. Numerical bridge kernels, Poisson-count samplers and uniform insertion positions therefore have additive capped-path error bounds. No inverse-CDF sensitivity product over all steps is needed.

The actual contraction word now has two duration-sensitive factors:

    exp(-iH0*t),  exp[lambda(D_Q+cI/2)t].

Both have norm at most1. Its telescoping timing bound uses

    ||H0||+lambda||D_Q+cI/2||,

times the total interval-time discrepancy (conservatively O(K^2 h) for K events rounded to h). Omitting the second term would be incorrect. The finite-matrix lemma supplies each contraction block to error beta/poly(K), with all dense reservoir arithmetic and unitary synthesis charged. Each source word uses fresh contraction success ancillas, retained coherently until the complete-isometry amplification.

The exact first-event identity, not small jump activity alone, makes amplification legitimate. After amplification measure or retain only the private outer event record for internal iteration; keep the reservoir state. A backward hybrid through at most S calls sums local isometry errors and the capped-future duration errors. The exact source MGF prices the actual count cap. No assumption about the approximate algorithm's jump tail is needed.

## 5. Remaining joint-review boundary

The local excursion law, scalar count/envelope inequalities, explicit finite reservoir arithmetic and scale-invariant receiving plan now form a concrete candidate route. A complete joint receipt must still check their numerical source constants, coherent arithmetic/synthesis integration, ordinary low-rate receiving theorem and error budget simultaneously. Until then the accepted theorem remains the independent-telegraph result. No practical crossover or novelty is inferred.
