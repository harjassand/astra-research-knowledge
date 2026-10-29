# Fault-free adaptive gadget equals the full syndrome-reset channel

28 October 2026. Algebraic supplement to `flagged_five_qubit_storage_round_20261028.md`. New load-bearing claim for repeated-cycle analysis; independent review pending.

Let commuting independent stabilizer generators be g_0,...,g_3 and define their joint projectors

    Π_s = product_(j=0)^3 [I + (−1)^(s_j) g_j]/2,   s ∈ {0,1}^4.

For the perfect five-qubit code, choose the unique weight≤1 Pauli E_s with syndrome s. Then E_s Π_s E_s=Π_0 and define

    P(X) = sum_s E_s Π_s X Π_s E_s.

This is CPTP on the full five-qubit operator space: Kraus operators K_s=E_s Π_s satisfy sum_s K_s†K_s=I. Its range is supported on Π_0, and it acts identically on every operator supported on Π_0. Hence **P²=P** as a full superoperator, not just on code states or Pauli-conjugated code states. The statement remains true after tensoring with an arbitrary reference identity channel.

## Equality to the actual fault-free adaptive circuit

A data-P parity coupling is a data-controlled syndrome flip in the P eigenbasis. All such couplings commute with CX(flag,syndrome), since they act via commuting X powers on the same syndrome target and have disjoint controls. Therefore the two flag-to-syndrome CX gates commute together and cancel in a fault-free check. The prepared flag |+> remains |+>, unentangled with arbitrary data. Its X outcome is deterministically trivial. The syndrome ancilla's measurement implements the projector (I±g_j)/2. This derivation also covers the explicitly compiled H-CX-H data-X coupling.

There are two types of noiseless adaptive branch:

- All four measured syndromes are trivial. The total data Kraus operator is Π_0; no correction is applied.
- The first nontrivial syndrome is at index k. The preliminary checks multiply the input by J_k=[product_(j<k)(I+g_j)/2](I−g_k)/2. The fresh complete unflagged pass then projects onto Π_s. Because all these projectors commute, Π_s J_k equals Π_s if s has first nonzero bit k and zero otherwise. The applied physical Pauli is E_s.

Every nonzero syndrome s occurs on exactly one such first-hit branch. Repeated syndrome projections do not create another map or disturb within-sector coherences. Discarding/resetting the classical records and ancillas therefore gives exactly

    X ↦ Π_0 X Π_0 + sum_(s≠0) E_s Π_s X Π_s E_s = P(X).

Off-diagonal operators between distinct syndrome sectors are removed by this instrument; coherences inside each sector are preserved up to E_s. This proves the equality on **all physical operators**, including arbitrary logical/syndrome entanglement and an external reference.

The reset assertion concerns the **fault-free** physical gadget only. A faulty gadget can retain a correctable syndrome residual; the repeated-round analysis must retain that residual, rather than replace every actual cycle by P. Any ideal receiver preceding this gadget must be incorporated into the ideal complete-round map: it is not enough that it acts identically on clean code states if it changes arbitrary syndrome sectors. For an identity ideal receiver, the ideal full round is exactly P.

## Reproducible matrix fixture

`flagged_all_operator_reset_check_20261028.py` constructs all 16 rank-two syndrome projectors and the actual first-hit branch Kraus operators as 32×32 dyadic matrices. It checks exact equality (not a numerical tolerance) of the 15 nonzero first-hit branches with E_s Π_s, trace preservation, code-space range, and all 256 composition-Kraus identities K_s K_t=0 for s≠0 and K_0 K_t=K_t. Thus P²=P is checked as a full operator map rather than only on sampled states. Its JSON records PASS. The flag cancellation is the explicit Clifford commutation proof above, not a separately claimed numerical seven-qubit simulation.

## Useful block estimate for a closed CPTP actual round

For a proposed closed physical round E with epsilon=||E−P||_diamond, write Q=I−P and define S_t=P E^t P, G_t=Q E^t P. Then ||S_t||_diamond=1, QG_t=G_t, and

    G_t = Q(E−P) S_(t−1) + Q(E−P) G_(t−1),

so ||G_t||≤2 epsilon/(1−2 epsilon) for epsilon<1/2 (using ||Q||≤2). If 2b=||P E P−P||_diamond, then

    S_t−S_(t−1) = (P E P−P) S_(t−1) + P(E−P)G_(t−1),

and therefore

    (1/2)||P E^T P−P||_diamond
       ≤ T [ b + epsilon²/(1−2 epsilon) ].

Here the retained G_t is the actual syndrome leakage; no ideal intermediate decoder is inserted. The final P is the declared ideal analysis decoder/re-encoder interface, not a supplied hardware operation. The bound requires the closed, same-round CPTP model (or a separately specified uniformly bounded time-varying extension), not marginal channels with hidden persistent bath coupling. It is an algebraic candidate for independent review, with initial/final real interface errors separate.
