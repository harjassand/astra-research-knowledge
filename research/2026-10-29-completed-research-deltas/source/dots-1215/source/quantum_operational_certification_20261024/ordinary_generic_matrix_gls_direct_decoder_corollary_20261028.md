# Direct-decoder decision refinement of the matrix GLS acquisition

28 October 2026. Separate author corollary; independent receiving pending. The governing matrix-design source stays IMMUTABLE at SHA `a331566da59a07b7d9b679e4516368866fd38df20e44cff4f87f8496332d52ea`; its fixed-cap companion stays at `23a7d41b408007eb11c5616129cb2bc5253ba3bd44e92538659d2382cda3072c`. Root has independently received those sources. This note improves only the final decision use of their simultaneous coefficient event. It uses no stronger tomography or tail theorem.

## 1. Retain the matrix statistical event, not just its projector consequence

Use all source, reset, fixed-four-real-coordinate encoder, full-CPTP comparator, paid common frame and ordinary loss-state assumptions of the governing construction. Let d=2k, D=10d^2, L=8D. Its stage sample choice n=ceil(2^24 DL/eta) and coordinate-median event imply, BEFORE final coefficient rounding,

    ||theta_med-theta||_V<=64 sqrt(D/n),
    F_x^T V^(-1) F_x<=L K(U_x),
    U_x<=3T_x+32eta I.                                   (1)

The operator inequality in (1) holds on the ENTIRE real Hermitian Hilbert space, not just rank-one tests. Therefore, for every actual full CPTP decoder C,

    |Tr[C(T_med,x-T_x)]|
       <=(sqrt(eta)/64) sqrt(Tr(U_x C^2)).                (2)

Using C>=0, C<=2I and Tr C=k,

    Tr(U_x C^2)<=3Tr(T_x C^2)+32eta Tr(C^2)
                  <=6q(x,C)+64k eta.                    (3)

This is the important difference from the older final step, which first summed rank-one root bounds and unnecessarily multiplied the leading statistical term by sqrt(k).

Round all coefficient matrices at every stage on a mesh at most eta/(2^12 d k), instead of the allowed larger mesh eta/(2^12 d). This still satisfies every earlier Loewner induction and finite-range proof, costs only additional arithmetic bits, and makes the final risk rounding debit at most eta/64 for every C. Thus the actually rounded affine predictor obeys, simultaneously over X and all full CPTP decoders,

    |qhat-q| <= sqrt(6eta q+64k eta^2)/64 +eta/64.         (4)

No decoder net, favorable chosen-decoder event, or trace-normalization change is used.

## 2. A direct relative decision inequality

Put K=ceil(sqrt(k)), an integer computable by exact integer square root and comparison. Since sqrt6<3 and K>=1, (4) gives

    |qhat-q| <=(3/64)sqrt(eta q)+(9K/64)eta.

For 0<gamma<=1, Young's inequality with delta=gamma/16 yields

    |qhat-q| <=delta q+A,
    A=(eta/4)(gamma^(-1)+K).                             (5)

Indeed the square-root term costs at most delta q+9eta/(1024gamma), which is below the displayed A after adding9K eta/64.

Keep the same finite encoder grid, decoder interior body K_s, comparator mixing s in [epsilon/512,epsilon/256], and h^2<=epsilon/256. Minimize the rounded final qhat with a feasible decoder-SDP objective gap at most eta (rather than the looser k eta). Then

    (1-delta)q_selected <=(1+delta)min_(X,K_s)q+2A+eta.

Since gamma<=1 and gamma^(-1)+K>=2,

    q_selected <=(1+gamma/4)min_(X,K_s)q
                    +2eta(gamma^(-1)+K).                (6)

These constants have slack: (1+delta)/(1-delta)<=1+2gamma/15, and the additive coefficient is at most16/15 times eta(gamma^(-1)+K). Do NOT convert (4) first to a uniform root-distance bound; that would discard the improvement.

Choose the final dyadic scale within a factor two below the rational target

    eta_target=gamma epsilon/[2^10(1+gamma K)].           (7)

The usual stationary fixed-decoder quadratic comparator gives min_(X,K_s)q<=(2/3)ell_star+s+h^2. Multiplying (6) by3/2 and using (7) gives on the good ideal-frame event

    ell_selected <=(1+gamma/4)ell_star+epsilon/32.          (8)

The mixture/grid debit is at most15epsilon/1024 and the final statistical debit at most3epsilon/1024, so (8) is conservative. The unchanged beta<=epsilon/32 bad-history budget and epsilon/4 whole-process implementation debit imply

    E ell_selected <=(1+gamma)ell_star+epsilon            (9)

for ONE subsequent payload, against the same original unrestricted full-CPTP encoder/recovery optimum.

## 3. Actual source, query-count and control consequence

Run exactly the received block-design/GLS schedule down to (7), with the finer coefficient mesh and stricter final SDP gap above. In the governing fixed-cap formulas replace only the predetermined final J by the least integer satisfying eta_J<=eta_target. The per-stage n, support bound, bias target min{eta/(10^6Dn),m_bar^(-2)}, paid local m/l/coarse banks and deterministic H=N_bar+1 remain identical. Every failed history, support ceiling and local purification is still paid.

Since the dominant cap is O_tilde(D^2/eta_final), this variant has

    N=O_tilde[ k^4/(gamma epsilon)+k^(9/2)/epsilon ].       (10)

This is sometimes conveniently written O_tilde(k^4(1/gamma+sqrt(k))/epsilon). It is not uniformly k^(9/2)/(gamma epsilon); keeping the two terms exhibits the better small-gamma behavior. The number of actual chosen-x homogeneous matrix-query invocations remains O_tilde(k^2), counting repeated banks separately. The finite grid is scanned classically, not paid as a source menu.

Processing is polynomial in the same charged parameters; a factor k finer numerical mesh and eta rather than k eta SDP tolerance add logarithmic precision only. The retained causal compiler, all collective receiver memory, random-purification centers and gates, frame horizon and log ambient output dimension remain explicit costs. Different local purification gauges are reduced to the same output matrix coordinates; no alignment or unknown source inverse is assumed.

The received scalar-bit k^6 route remains a valid weaker-receiver alternative. The independently received k^5 matrix construction remains valid and unchanged. This corollary still does not attain the generic k^2 fast-rate target, assert a practical hardware advantage, or separate quantum from an equally informed conventional learner. It is a deterministic decision refinement of the SAME received second-moment confidence event, pending its own receiving check.
