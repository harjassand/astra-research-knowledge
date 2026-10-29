# A strict one-use budget is not an unchanged budget for correlated releases

30 October 2026, Brisbane. Standard repetition counterargument, written here
to qualify the operational use of the new channel-design theorem. This is
not a new information-theory result or a correction to that one-use theorem.

Take binary L with crossover1/4 and K=(1/2)L+(1/2)U, where U releases an
independent fair bit. Thus K has crossover3/8. For EVERY admitted cq pair,
joint convexity of relative entropy gives

    D(K rho||K sigma)<= (1/2)D(L rho||L sigma)
                         +(1/2)D(rho_R||sigma_R).

Subtracting the reference divergence proves J_K<=(1/2)J_L. This is exactly
the universal one-use information budget, including quantum references.

Now let R be one fair classical bit and set all N=129 raw input symbols
equal to R. Apply K independently to each symbol. A majority decoder makes
an error only if at least N/2 crossover bits occur. For independent
Bernoulli(3/8) errors, the elementary exponential Markov inequality, with
exponential parameter log(5/3), gives

    p_error <= (sqrt(15)/4)^N,
    p_error^2 <= (15/16)^129 < 1/1024.

The last inequality was checked using exact Fraction/integer arithmetic;
its left side is approximately0.00024226721985020735. No random samples,
channel simulations or enumeration of2^129 output strings were used.
Hence p_error<1/32. The binary decoding entropy bound yields

    I(R:K^N(X^N)) >= ln(2)-h(p_error)
                 > ln(2)-(5ln(2)+1)/32
                 > (3/4)ln(2).

The final strict inequality uses ln(2)>1/2.
For the SAME source, I(R:L^N(X^N))<=ln(2). Consequently the product-channel
inequality with factor1/2 fails. These mutual informations are instances
of J obtained by comparing the correlated input state with its input/reference
product. Classical reference information already suffices for the failure.

Conclusion: do not turn the single-use design certificate into an unchanged
strict information budget for an arbitrarily long correlated release,
persistent privacy or cryptographic security. A different multi-use budget,
source restriction or composition theorem would be a new input/result.
All competitors receive the same restriction. The exact one-use synthesis
and its separate bounded-calibration extension remain valid at their scopes.
