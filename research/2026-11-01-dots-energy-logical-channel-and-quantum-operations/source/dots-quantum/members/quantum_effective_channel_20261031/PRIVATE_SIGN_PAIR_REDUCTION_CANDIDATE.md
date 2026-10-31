# One private interaction-sign bit: complete finite-rate cancellation candidate

Status: root derivation, unreviewed. This is not a novelty claim. It is a proposed cheap physical alternative to projecting every source jump into dark/excited output sectors. Strong existing symmetrization, randomized compiling, antithetic simulation and adiabatic-elimination methods must be compared.

## Physical operation, not algebraic extrapolation

Assume the same acquired native pure-dark source and exactly centered K as DARK_SOURCE_LOGICAL_REDUCTION_CANDIDATE.md. The device must actually implement BOTH lambda G-i[H0+sqrt(lambda)K,.] and lambda G-i[H0-sqrt(lambda)K,.], with the SAME G and H0 and with sign-setting cost and errors charged. Reversing H0 as well does not meet this interface. A norm certificate, a symbolic minus sign, or a block encoding does not by itself supply physical sign control.

Choose one fair private bit independently of the initial source/system/reference state. Use its sign for the ENTIRE prescribed-time system-control protocol; use exactly the same control policy in both branches, retaining user control records but not the sign. Then discard the private bit. This implements the CPTP average of the two complete physical channels, not a negative-weight extrapolation or postselection. Source output is still discarded. The sign cannot be exposed for sign-dependent user feedback. A bit already correlated with the initial bath is not a fresh independent choice.

The second-order effective GKSL generator is unchanged because it is quadratic in K. In the generic two-corrector notation, epsilon=lambda^(-1/2),

    T_+=P+epsilon F1+epsilon^2 F2,
    T_-=P-epsilon F1+epsilon^2 F2.

The residuals are +/-epsilon A1+epsilon^2 A2, with ||A1||cb<=C1 and ||A2||cb<=C2. At control j the corresponding defects are +/-epsilon J1_j+epsilon^2 J2_j. Let f1,f2 bound the correctors and J1=sum||J1_j||, J2=sum||J2_j||. These are already constructed analysis bounds, not implemented source inverses.

## Fast-centered pair lemma

Write Pi for source stationary averaging/embedding and Q_sup=I-Pi for centered OBSERVABLES (not the source projector Q). Let q(t)=||exp(tG^dagger)-Pi||cb, whose integral is <=ell. Base propagation with K=0 has only lambda G, system H0 and the SAME system-only instruments. All its system operations commute with source G and Pi, so its terminal-centered norm is at most q(lambda t), where t is total intervening physical time. This remains valid when the records change algebra dimension and the system policy is controlled by earlier records.

Duhamel comparing the plus and minus evolutions with this same base gives, for every protocol prefix or suffix of duration t,

    ||(E_+(t)-E_-(t)) Q_sup||cb
       <=4b sqrt(lambda) integral_0^t q(lambda u)du
       <=4b ell epsilon.

No additional per-control mixing penalty is inserted: base source time accumulates through system-only instruments, and actual propagation on the other side of each insertion is contractive. This statement is about all centered observables, not only the stationary initial state.

On embedded system observables, the existing generic theorem bounds each sign by

    delta <= min(2, epsilon B1+epsilon^2 B2),
    B1=2f1+T_total C1+J1,
    B2=2f2+T_total C2+J2.

Consequently the full pair difference is at most 2delta+4b ell epsilon, by splitting an arbitrary observable into Pi and Q_sup parts. The factor for Q_sup is already in the centered-pair lemma and is not charged again.

## Averaged complete logical-channel bound

Average the two exact intertwiner Duhamel identities. The odd endpoint F1 and odd control defects J1_j are centered: Pi F1=Pi J1_j=0. Their signed averages therefore gain the extra epsilon from the centered-pair lemma. The even endpoint/control terms cost epsilon^2 directly. The odd residual A1 need not be centered, so use the full pair bound. All effective backward propagators remain CPTP/unital and contractive.

This gives

    error_pair <= min(2,
      epsilon^2 [2b ell(f1+J1)+B2]
       +epsilon T_total C1 [delta+2b ell epsilon]).

In particular, substituting the uncapped generic bound,

    error_pair <= min(2,
      epsilon^2 {2b ell(f1+J1)+B2+T_total C1(B1+2b ell)}
       +epsilon^3 T_total C1 B2).

For fixed task length and control budget this is O(1/lambda), uniformly over arbitrary initial QUANTUM source/system/reference correlations. It has a real T_total^2 contribution, consistent with mixing two opposite residual coherent drifts; it is not an automatically linear-time bound. No cold source or P/Q-homogeneous jump assumption was used. Lambda>0; at zero rate use the trivial bound2.

One may use the already earned bounds

    f1=2b ell, f2=4b^2 ell^2,
    C1=2d ell+16b^3 ell^2,
    C2=8bd ell^2+16b^4 ell^3,
    J1=ell sum gamma_j, J2=4b ell^2 sum gamma_j,

where gamma_j bounds the control commutator with V=i[K,.]. These can be conservative. The theorem does not assume that calculating a tight norm or accessing K/b is free.

## Evidence, costs and boundaries

check_sign_symmetrization.py records a small mixed-output recycling qutrit source with QQ coupling, where the cold-input and all-quantum-input Choi differences numerically change from lambda^(-1/2) to lambda^(-1) under the physical positive mixture. It is only a floating diagnostic and does not establish the theorem or novelty.

The extra abstract operation is one independent bit and one sign setting per whole protocol, provided the native device truly offers that setting. Both branches run for the full physical duration. If only simulation encodings are available, signed Hamiltonian simulation is often ordinary, but its actual cost remains; that does not earn analog control of equipment. This construction does not reproduce bath outputs or an exposed private sign record, and it does not remove coefficient acquisition or the effective-channel implementation. Sign-setting bias, distinct source dynamics between settings, switching transients and control inaccuracies require additional charged error bounds.

The possible consequence to test is whether a genuinely available sign switch reduces the finite dissipation rate/coupling cost needed for a useful logical operation. A direct fresh-ancilla implementation of the same effective channel may still win. The original expensive full-source simulator is not the comparator to beat by itself.
