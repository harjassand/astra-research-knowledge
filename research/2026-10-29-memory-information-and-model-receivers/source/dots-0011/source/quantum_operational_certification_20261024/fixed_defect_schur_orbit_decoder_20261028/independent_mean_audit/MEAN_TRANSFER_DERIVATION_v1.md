# Independent derivation: rectangular weighted moments and redundant labels

28 October 2026. Reviewer working derivation for the new orbit-frame bridge. This is not yet a receipt for the author's pending full construction. Representation access and gate normalization require their separate review.

## Rectangular orthogonal frame

Let F_a:C^d->C^e, a=1,...,N, satisfy Tr(F_a†F_b)=d delta_ab and sum_a F_a F_a†=(Nd/e)I_e. The latter follows from irreducible output symmetry and trace for the proposed full selected error space. An efficient code isometry C:C^K->C^d is drawn as U C_0. Let W_C=[F_1 C ... F_N C], G_C=W_C†W_C, R=T tensor I_K/K, T>=0 fixed independently of U, and t=Tr T. Require d>1 and 1<=K<=d; K=1 has no quantum payload, and d=1 can be handled trivially without dividing by d²−1.

For Haar U, P=C C† has second moment

    E(P tensor P)=a I+b Swap,
    a=K(dK−1)/[d(d²−1)],
    b=K(d−K)/[d(d²−1)].

The coefficients follow from total trace K² and swap trace K. Therefore E Tr(P X P Y)=a Tr(XY)+b Tr(X)Tr(Y). Applied to each error-index matrix entry,

    E Tr_logical(G_C)/K = I_N,
    E Tr_logical(G_C²)/K
      = [(dK−1)Nd/e+d(d−K)]/(d²−1) I_N.

Here sum_b Tr(F_a†F_b F_b†F_c)=(Nd²/e)delta_ac and sum_b Tr(F_a†F_b)Tr(F_b†F_c)=d²delta_ac. Consequently

    E Tr[R(G_C−I)²] = beta t,
    beta=(dK−1)(Nd/e−1)/(d²−1),
    E Tr(R G_C)=t.

The square-input/output formula is the e=d specialization, not the general formula. No commutation of T with G is required. Source weight independent of the random code is required.

## Redundant Parseval labels

Suppose the efficiently accessible redundant frame is A=F V†, where V:C^N->C^M is an isometry, V†V=I_N. Put P=VV† and J=V tensor I_K. Then W_A=W_F J† and G_A=J G_F J†. Embed the actual error weight as T_A=V T V†, so R_A=J R_F J†, Tr T_A=t and R_A is supported on P tensor I.

It follows exactly that

    Tr[R_A(G_A−I_MK)²]=Tr[R_F(G_F−I_NK)²].

The zero eigenvalues on the redundant-label complement do not contribute because the source weight has zero support there. Replacing T_A by arbitrary/uniform coefficients would not be the same physical source and would generally create an artificial null-mode defect. The decoder must similarly use the isometric singular-vector lift: any odd soft singular-value filter vanishes at zero, so its success map is J times the orthogonal-frame success map. Tracing the error register removes V and yields the same logical channel. No eigenvalue inversion on the null space is needed.

## Subnormalized source branches

A selected good Schur branch need not be TP for each code. Let chi purify R, ||chi||²=t, and actual source vector W chi have squared norm p_C=Tr(RG). The decoder's success overlap with chi is z. The unnormalized Bell success mass is at least |z|²/t for t>0. Hence its Bell ERROR MASS is bounded by

    p_C−Bell_mass <= p_C−|z|²/t <= p_C+t−2 Re z.

This is exactly the same soft-filter penalty Tr[R(I+G−2sqrt(G)f(sqrt(G)/alpha))]. The t=0 case is zero. Thus the good-branch error bound extends without pretending each branch is trace preserving or dividing its error by a random branch probability. A total protocol still needs the actual bad-source mass and source block-decomposition contract.

## Explicit approximate-design budget

Let the implemented U distribution have two-copy twirling channel within unhalved diamond distance delta of Haar. This also bounds its one-copy twirl by delta, by adjoining maximally mixed input and tracing the second copy.

The linear moment obeys |E_D Tr(RG)−t|<=d delta t. Indeed Q_T=sum_ac T_ca F_a†F_c is positive with trace dt, and E(P) differs in trace norm by at most K delta.

For the quadratic moment, write T as a positive combination of unit vectors z. F_z=sum_a z_a F_a has Hilbert-Schmidt squared norm d and hence operator norm at most sqrt(d). The two-copy test operator is a sum over b of (F_z†F_b tensor F_b†F_z)Swap, whose norm is at most N d². Since the normalized input to the twirl is (P_0/K) tensor (P_0/K), the unnormalized P tensor P difference has trace norm at most K² delta. Therefore

    |E_D Tr[R(G−I)²]−beta t| <= (K N d²+2d)delta t,
    E_D Tr(RG) <= (1+d delta)t.

This is conservative but explicit. Combining the received nonnegative soft filter with weighted Cauchy–Schwarz gives

    E_D Bell_error_mass
      <= [(20/9)(beta+(K N d²+2d)delta)
          +2 epsilon sqrt(1+d delta)] t.

The redundant-label transformation preserves this bound exactly; N is the true error-space dimension, not the redundant label count M. An exponentially small delta in log-d is not automatically an exponential gate cost, but polynomiality requires an actual design/encoder-access algorithm with cost polynomial in log(d) and log(1/delta). If only inverse-delta access is available, the claim fails. The metric must be the stated twirling diamond metric or converted with explicit dimension factors.

Finite complete-circuit implementation error must be added separately. Bounding each implemented unitary gate in operator norm and telescoping across the actual gate list supplies a complete Stinespring error budget. A small projected-block matrix error alone is not automatically the same gate-level guarantee.
