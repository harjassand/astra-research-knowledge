# Closing local fast D=0 feedback with preserved polynomial path capital
Status: personal local synthesis, unreviewed. This is about one conserved fast/clearing fiber, NOT full connector-cycle recurrence.

The earlier reviewed complex-path lemma already supplies a crude polynomial clearing mean on ANY active homogeneous finite-graph fiber containing the kill complex: choose an enabled source, follow a graph path of fixed length to the kill complex, then kill. Desired rates have a fixed positive lower bound, total rates are O(N^v), and activity is invariant. Fixed-length jump blocks therefore have absorption probability >=cN^-M and bounded mean duration. In the degree2 dormant test this gives a bound C N^M uniformly over every active state, including large D. This is preserved capital from ACTIVE_CREDIT_GENERAL_ORDER_EXTENSION.md and its audit, not a new claim or a mixing premise.

Apply it at the exponentially rare d>=J exit of SEEDED_D_EXIT_KERNEL_CANDIDATE.md. Its forcing contribution is at most C N^M exp(-cN^(1/8)), negligible compared with any inverse power. Thus the opposite-face FULL-CHAIN return problem remains open, but the local fast/clearing remaining mean at that exit does NOT have to be assumed.

At d=0, active states have a>=2. The first fast/clearing event has mean <=C/a^2<=C. It is clearing with a fixed positive probability, otherwise creates d=1 and decreases a by1. Let M_0 be the supremum full operational clearing mean over active d=0 states, and M_1 over d=1 states, at fixed N. The regional seeded kernel gives

    M_1<=C N^-1/2+C N^-1/8 M_0
                   +C N^M exp(-cN^(1/8)),
    M_0<=C+(1-p)M_1.

These inequalities are justified first for finite stopped horizons; the crude polynomial path bound already guarantees finiteness, so the suprema are legitimate. They yield

    M_0<=C,    M_1<=C N^-1/8.

This closes the local non-small dormant/seeded fast feedback without claiming a uniform small mean over all initial large-D compositions. Incoming profile and physical connector interfaces remain separate obligations.

A useful distinction: the polynomial path bound suffices here because its coefficient is exponentially small. It would NOT suffice at the d=0 return, whose probability is only an inverse power; that block needed its own actual first-event equation. This is the precise small-gain logic intended for more general boundary operators.
