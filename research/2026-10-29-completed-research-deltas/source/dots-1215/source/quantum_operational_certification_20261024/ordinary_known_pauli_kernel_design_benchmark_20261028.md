# Known Pauli-kernel dictionary: a constructive rank-squared benchmark

28 October 2026. A scoped ordinary adaptive theorem and an explicit information invariant. The known flag/Pauli basis is a supplied or already PAID receiver asset; its discovery is not proved. This note does not replace the generic unknown-direction target or the received generic k^6 polynomial-processing baseline.

## 1. Physical class and exact full-CPTP comparator

There are G known orthogonal qubit output blocks. In their known logical Pauli frames,

    E_x(rho)=direct_sum_g sum_(a=I,X,Y,Z) p_ga(x) sigma_a rho sigma_a*,
    p_ga(x)=x^T A_ga x>=0,   sum_ga A_ga=I_4.             (1)

This is a fixed CPTP source: measure the control POVM {A_ga}, apply the indicated Pauli to the logical qubit, and emit flag g. The source inputs remain ordinary real-quaternion controls and ordinary logical probes. More generally the proof needs the same known Pauli form with positive quadratic probabilities. Zero probabilities and changing encoded Choi rank are allowed.

Put w_g=sum_a p_ga. The ACTUAL ordinary loss density, prepared with six states and a receiver-local anti-state, is diagonal in the known flag/Bell projectors P_ga, with

    lambda_ga(x)=Tr[P_ga T_x]=(w_g-p_ga)/3.               (2)

A single ordinary T_x copy followed by this known Bell/flag measurement gives a Bernoulli observation of any selected lambda. No Choi input was sent through the source.

Pauli twirling each actual flag block proves the unrestricted full-CPTP optimum

    ell_opt(x)=sum_g(w_g-max_a p_ga)=3 sum_g min_a lambda_ga. (3)

A decoder that applies the selected Pauli correction on each flag attains it. Its Choi transpose is2 sum_g P_g,a_g. Thus the relevant kernel dictionary has4G=2k KNOWN orthogonal directions, where k=2G. There is no exponentially enumerated decoder menu and no restriction of the comparator beyond the stated physical source class.

## 2. Paid global acquisition and relative risk

Freeze this dictionary and the retained frame before acquisition. Use a known finite encoder net X containing the ten quadratic anchors; write M=|X|. For each of the4G kernel directions independently run the received10-feature nonnegative adaptive design, with stage endpoint

    t=gamma epsilon/(168G),   0<gamma,epsilon<=1,

and confidence failure beta/(4G). Its raw linear predictions satisfy simultaneously, with probability at least1-beta,

    |lambdahat_ga(x)-lambda_ga(x)|
        <=sqrt(t lambda_ga(x))+t                         (4)

for all x in X. The constants in the received bound are smaller than those in(4). Each pilot call measures an actual known kernel probability; discarded outcomes and all repetitions count.

For any flag correction policy a=(a_1,...,a_G), put ell_a=3 sum_g lambda_g,a_g and ellhat_a=3 sum_g lambdahat_g,a_g. Cauchy--Schwarz gives

    |ellhat_a-ell_a|<=sqrt(3Gt ell_a)+3Gt.                (5)

Select the minimum of3 sum_g min_a lambdahat_ga(x) over X. For each x the corrections are obtained separately by four comparisons per flag. Empirical optimality and Young's inequality with coefficient gamma/8 imply

    ell_selected <=(1+gamma/2)min_(x in X)ell_opt(x)
                      +21Gt/gamma
                   <=(1+gamma/2)min_X ell_opt+epsilon/8. (6)

At a true globally optimal encoder, a fixed optimal flag correction has a bounded nonnegative quadratic risk and that encoder is its minimum eigenvector. A chord net with h^2<=epsilon/32 therefore adds at most epsilon/32 to the comparator. Good-event loss is consequently at most(1+gamma/2)ell_star+epsilon/4. Taking beta<=epsilon/16 and a separate whole-process/deployment loss debit at most epsilon/4 proves

    E ell_selected <=(1+gamma)ell_star+epsilon.           (7)

The received scalar cap, conservatively including finite design slack, gives with J=ceil(log_2(1/t))

    N <=4G [J+(40960/t)log(16GMJ/beta)]
      =O_tilde(G^2/(gamma epsilon)).                    (8)

All four-real encoder-grid points are classical candidates, not a physical scan. Source acquisition, known Bell measurements, flag-conditioned decoder synthesis, fixed-horizon common-frame use and finite controls remain paid. Runtime is polynomial in G,1/(gamma epsilon), the known-grid size and the declared precision. No positive spectral floor, contrast parameter or zero-optimum premise is used.

## 3. What the log-det potential genuinely certifies

For each fixed P_ga, the action features are ten known quadratic monomials. At a confidence stage the scalar learner builds

    V_ga=sum_x pi_x a_2(x)a_2(x)^T/u_ga(x),

where u is a positive acquired upper envelope. The determinant increase for a leverage-violating point is the received finite G-optimal update; it bounds classical design iterations and supplies the variance control for actual queried data. One may retain the block-diagonal information matrix direct_sum_(ga) V_ga. This is a known design covariance, NOT a Loewner lower bound on any source state or a learned source component.

The O(k) number of directions here is valid because the physical Pauli structure supplies exactly4G orthogonal task kernels. It is not deduced from Hilbert-space leverage after arbitrary new decoder directions arrive. The rare Bell-kernel pair is included in this class: a useful kernel probability is genuinely observed, rather than inferred from independent row-cone radii.

## 4. A valid generic control-matrix invariant, and its missing count

For a fixed known receiver vector v, q_v(x)=v*T_xv=x^T B_v x is a nonnegative quadratic. A paid global scalar fit can be converted into a real4-by4 matrix confidence cut. To make the word GLOBAL precise, choose a classical chord net of radius h<=t/1000 containing the ten anchors. On the event(4), raw anchor values have magnitude at most3, so the reconstructed Bhat has diagonal magnitude at most3, off-diagonal magnitude at most6 and operator norm at most22. True0<=B_v<=I. Net extension therefore gives

    |x^T(Bhat-B_v)x|<=sqrt(t x^T B_v x)+2t

on the whole sphere. Young's inequality implies, for0<kappa<1,

    (1-kappa)B_v-c_kappa t I <= Bhat
       <=(1+kappa)B_v+c_kappa t I,
    c_kappa=2+1/(4kappa).                               (9)

Because B_v(H) is linear in the feasible PSD source lift H, these are literal LMI confidence cuts containing the truth. They do NOT acquire H, select its invisible completion, or make returned row components monotone PSD lower bounds. For an orthonormal output basis, sum_v B_v=I_4, a genuine normalization identity.

What is missing generically is a valid rule charging newly selected decoder kernels to O(k) such directions at the desired precisions. Output-space covariance alone cannot certify this: after basis projectors are learned, that covariance is full rank, but two states with identical basis populations can still disagree on a superposition kernel. A valid unrestricted projector-information covariance naturally lives in Hermitian OPERATOR space of dimension k^2. Turning its count into O(k), or replacing scalar cuts by a sufficiently informative matrix-valued batch, needs a task-specific theorem. Ordinary entropy mass gains and independently learned row cones do not supply that theorem.

## Scope

This is an equally informed active conventional learner. Its improvement over a generic exponential decoder menu comes from the supplied finite orthogonal Pauli task dictionary, not from a claimed quantum advantage. The generic unknown-algebra/source frontier remains open; the received generic k^6 polynomial-processing baseline remains a separate result. The companion finite checks are mathematical diagnostics, not execution of the conservative full pilot or hardware.
