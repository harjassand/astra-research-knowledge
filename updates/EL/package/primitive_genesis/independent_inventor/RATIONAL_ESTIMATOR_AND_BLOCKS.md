# Exact rational evaluator and an honest within-grade extension

Internal proof, 2026-10-12. Historical novelty UNKNOWN. This supplements `PROOF_AND_GATES.md` and uses its notation.

## A. Removing transcendental output from the estimator

Assume all generator coefficients, terminal values, and row-sampling probabilities are rational, with exact rational local access. Fix an integer k>=max(1,A), set rho=k/(k+1), and sample N with

    Pr(N=n)=(1-rho)rho^n, n=0,1,... .

The sampler uses repeated exact Bernoulli(rho) coins. Follow N symbolic successor steps exactly as in the original proof. Return

    Y = W_N t_{I_N} / [(1-rho)rho^N],

or zero if the path terminates first. Every output is rational. With |t|<=T and |W_n|<=A^n/n!,

    E Y = sum_n (K^n t)_i,
    |Y| <= (k+1) T exp(A/rho) <= (k+1) T exp(A+1),
    E Y^2 <= (k+1) T^2 sum_n (A^2/rho)^n/(n!)^2
           <= (k+1) T^2 exp(2A/sqrt(rho))
           <= (k+1) T^2 exp(2A+1),
    E[N+1]=k+1.

The penultimate inequality uses sum_n z^{2n}/(n!)^2 <= exp(2z). The last uses sqrt(1+1/k)<=1+1/(2k) and A<=k. No exponential needs to be evaluated by the implementation; it appears only in the analysis.

Exact rational probability sampling can use uniform random bits to sample an integer in the denominator range, rejecting the top incomplete interval. For an explicitly represented B-bit denominator the expected number of rejection attempts is less than two. The complexity of obtaining that denominator from a row's coefficients is part of row acquisition.

If the bit size and cost of a row at depth n are polynomial in n and the input bit size, then the accumulated rational product has polynomial bit size in n and the input. Geometric N has all moments finite, bounded polynomially in k for any fixed moment. Standard exact arithmetic therefore gives finite expected bit work, polynomial in the declared row parameters and k. A claim of this type is not valid if the row representation itself grows exponentially with depth; that remains a separate gate.

This closes the finite-bit exact-unbiasedness issue for rational data and rational-valued terminal functions. General real-valued functions still require exact-real output or controlled approximation.

## B. Within-grade motion without supplying a block inverse

Suppose the local identity is

    L phi_i = -d_i phi_i + sum_j C_ij phi_j
              + sum_j B_ij phi_j + c_i,

where C stays in the same grade and B strictly raises grade. Signs are permitted. Put

    kappa_i=d_i-sum_j |C_ij|.

Require, at grade g,

    kappa_i >= gamma(g+1)>0,
    sum_j |B_ij| <= A gamma,
    d_i/kappa_min(g) <= V,
    |c_i|/kappa_i <= U.

The bound V must hold over every row reachable within the grade. This is a real microscopic-work assumption, not a hidden block solve.

To apply (D-C)^{-1} to a terminal vector f, perform the following killed signed walk inside the grade. At state i, move to j with probability |C_ij|/d_i, multiplying a sign by sign(C_ij). Kill with probability kappa_i/d_i. At the killing state J return sign*f_J/kappa_J.

The expected output is exactly

    sum_{n>=0} (D^{-1}C)^n D^{-1} f = (D-C)^{-1}f.

Indeed each path ending at J has probability equal to its absolute C/d product times kappa_J/d_J; multiplying by f_J/kappa_J restores precisely the corresponding inverse coefficient. The output is bounded by ||f||_infinity/kappa_min(g). At each microscopic step killing occurs with probability at least 1/V, so the expected number of row visits is at most V. Thus the inverse is acquired by a killed local walk, with a declared cost bound; it is not supplied.

To produce one effective higher-grade transition, first run the within-grade killed walk. At J sample K with probability |B_JK|/sum_l |B_Jl| and multiply the macro weight by

    sign(within-grade path) sign(B_JK) sum_l |B_Jl|/kappa_J.

Its absolute magnitude is at most A/(g+1), so successive macro transitions have the same factorial envelope as in the original theorem. The terminal macro step uses phi_J(x)/kappa_J for a Poisson value or c_J/kappa_J for a stationary mean. The geometric evaluator in part A now has at most V(k+1) expected microscopic row visits. Terminal outputs are bounded by 1/gamma and U respectively before macro weighting.

This extension permits arbitrarily complex within-grade topology and feedback if diagonal damping dominates its **absolute** coefficients. It does not permit cancellation between positive and negative coefficients to be silently charged as free. If d_i-sum |C_ij| approaches zero, V or the output bound diverges. This is precisely where a difficult block inverse can reappear.

## C. Why a finite closure alone does not remove the obstruction

For the active-copy/slow-hidden-spin example,

    Lx=-x+z,       Lz=-epsilon z,

the two-dimensional observable closure is already known exactly. Its inverse still has norm of order 1/epsilon. Calling this a small block does not make the inverse independent of the slow rate. The extension above rejects it through kappa_min=epsilon.
