# Paid packing for the exchanged three-site projection

This is an operational consequence of the three-site calculation supplied by the independent algebra constructor. Its projection and acquisition coefficients are inputs from that calculation, not outputs of the control searches here. The new deductions below concern physical packing, label statistics, and cost. This does not establish a new optimal memory exponent.

## Given instrument and recovery law

On each triple measure P versus I−P, retaining the complete selected quantum range, where

    P=I/4−(σ1·σ2+σ2·σ3)/6+σ1·σ3/12.

The ranges have dimensions 2 and 6. Put x=sin²θ. The supplied exact coefficients are

    b=x²(x⁴+30x³−60x²−12x+54)/18,
    h=(1−x)³(4x³+24x²+27x+9)/9,
    a_K=b(1−h^K)/(1−h).

Restoring the retained ranges and performing the reverse inverse-dummy sweep gives exact error 3(1−a_K)/4. Restoration can be done one packed group at a time. The weak-angle limit is a_infinity=.9: this projection has a Petz error floor .075 and an all-decoder lower floor (3/4)(1−sqrt(.9))≈.03849. It cannot supply arbitrary accuracy by increasing K alone.

## Input-independent labels and typical capacity

For each full block-label history h, the corresponding effect F_h on the bath is SU(2) invariant. Covariance makes C_N*(F_h) a scalar on the input qubit. Thus the probability of h is independent of every input, including its inaccessible-reference correlations. On tracial input the emitted bath is product tracial, so the labels are exactly iid with probabilities 1/4 (rank 2) and 3/4 (rank 6).

Let X_K count rank-2 outcomes. The actual retained branch space has

    D_K=2^(X_K)6^(K−X_K),
    log2 D_K=K log2 6−X_K log2 3.

Its mean logarithmic dimension is Kμ, where

    μ=1+(3/4)log2 3=2.1887218755... bits per triple,
    μ/3=.7295739585... qubits per incoming carrier.

Hoeffding gives

    Pr[log2 D_K>Kμ+(log2 3)sqrt{(K/2)ln(1/δ)}]≤δ.

A receiver may abort to a fixed output whenever its quantum capacity would overflow. Branch dimension grows monotonically, so prefix overflow is contained in the final tail event. Its input-independent probability makes the added half-diamond error at most δ. This converts average rank saving into a valid capacity bound; average entropy alone would not do that.

## Grouped coherent codec and processing bill

Packing the entire growing register after every triple would hide quadratic processing. Instead group L triples, with known classical radices r_i∈{2,6}, and store each group in ceil(log2 product_i r_i) qubits. Ceiling overhead is at most ceil(K/L). A packed-data capacity is therefore

    W=ceil{Kμ+(log2 3)sqrt[(K/2)ln(1/δ)]+ceil(K/L)},

plus O(L) quantum workspace and a possible final incomplete group.

An explicit coherent codec repeatedly maps valid basis states (a,b) to z=r a+b. It computes z in a separate accumulator and uncomputes a,b by reversible quotient/remainder arithmetic. Fixed-radix division by 2 or 6 needs only a constant-size remainder and a linear scan. With O(L) scratch space, the group needs O(L²) elementary arithmetic gates. The operation is an isometry on the actual branch space, preserving arbitrary superpositions and reference entanglement. Its inverse restores a group into the physical three-carrier ranges before reverse decoding.

There are K/L groups, so addressed packing and unpacking cost O(KL)=O(NL), plus O(N) projector and inverse-collision gates. For fixed L the addressed processing is linear, and the data-storage rate approaches μ/3 with O(1/L) ceiling overhead and the stated tail term. The live quantum memory also includes the current raw group, accumulators/scratch, the decoding dummy, and possibly a second O(L) group while packing the previous one.

This is not a free-routing claim. Loading chunks into a physical storage array, retrieving them, and delivering the output need an architecture and additional cost. Codec throughput must fit the arrival interval or its queue is added as quantum memory. Independent zero-state preparation, flag measurements/resets, classical labels, finite gate precision, and protection are paid as in the main continuation report. The grouping prevents the arithmetic itself from silently operating on the entire growing bath after every arrival.

## Attainable statement and limitation

For finite θ,K,L,δ, the grouped physical receiver and decoder achieve

    ε≤(3/4)[1−a_infinity+a_infinity h^K]+δ,
    a_infinity=b/(1−h),

using the packed capacity W and O(L) additional coherent workspace before routing/protection. Targets above the displayed projection floor are attained with a strict margin. This improves a storage coefficient; its weak-angle memory exponent is still quartic.

A larger-block family with vanishing loss/acquisition ratio and polynomial retained branch dimensions could potentially change that exponent. Neither the three-site calculation nor this codec proves such a family. No assumed Schur or Yangian compression is used here.
