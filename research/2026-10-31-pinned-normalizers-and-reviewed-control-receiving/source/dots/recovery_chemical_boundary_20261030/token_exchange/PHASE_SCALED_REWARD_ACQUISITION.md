# Finite phase-scaled reward acquisition without a population-dependent inverse

30 October 2026. Local sufficient compiler rule building on REWARD_WEIGHTED_TOKEN_EXCHANGE.md; no whole-network extension.

Let Q0 be a fixed finite rational transient generator for token phases, including its own-restoration/terminal exits. Let s(y)>0 be a frozen configuration scale. Suppose the actual killed excursion generator is

    Q_y=s(y) Q0-diag(k(y)),   k>=0,

where k includes every ordinary-restoration exit and any additional terminal marks. Ordinary type-i per-particle restoring intensities obey 0<=h_i(p,y)<=hbar_i(p). Entrance intensities into each phase obey sum_{e:p_e=p} lambda_e(y)<=s(y) ell_p, with fixed ell>=0. All frozen-ordinary and actual-stopping conventions of the main note remain necessary.

Solve the constant rational system

    -Q0 t_i=hbar_i.

Transience implies t_i>=0. Put psi_i(p,y)=t_i(p)/s(y). Then pointwise

    -Q_y psi_i=hbar_i+diag(k)t_i/s >=h_i,
    sum_e lambda_e psi_i(p_e)<=ell dot t_i=:b_i.

Hence every summed exchange out of ordinary type i has full trace intensity <=b_i y_i. No small-return probability, bounded entry rate, or population-dependent matrix inversion is needed. The diagonal killing term is useful, not a perturbation to be assumed small. Rational acquisition consists of a finite graph reachability check for Q0, exact linear solves, and raw rate factorization/inequality certificates for s, ell, hbar. Factoring a common scale is sufficient, not necessary.

Illustrative exact algebra (abstract phase kernel, not a new reaction-network claim):

    Q0 = [[-3, 2], [1, -4]],  hbar=(1,2),  ell=(2,1).
    t=(4/5,7/10),  b=23/10.

Thus for every s>0 and every nonnegative diagonal killing vector, entrance rates bounded by (2s,s) give total ordinary-i exchange rate <=(23/10)y_i. If an ordinary restoring intensity grows as s instead of remaining <=hbar, this rule does not apply. The failed time-only example in the main note is precisely of that type.

This is ordinary killed-chain reward/resolvent algebra, used as a constructive certificate rather than a novelty claim. Before global use the actual physical model still has to supply the required trace-clock scaling, retain non-restoration terminal outputs, and satisfy all other graded signed-cycle interfaces. In particular the rule does not make a hidden nonneutral face transfer harmless unless its actual ordinary-label changes fit the single-exchange representation.
