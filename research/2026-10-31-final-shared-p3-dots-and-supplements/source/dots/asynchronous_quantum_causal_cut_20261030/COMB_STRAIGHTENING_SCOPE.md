# From a bounded quantum boundary to a circuit-order norm estimate

2026-10-30. Algebraic lemma and precise norm gap. This is not an accepted threshold theorem.

## 1. The danger to avoid

A false DONE may cause an output to be consumed before the legitimate input arrives. A later replay may receive that input and communicate it through a shared bath to another damaged module. The aggregate process is physically causal, but need not be an ordinary noisy gate at the intended circuit time. Port count alone cannot establish ordinary circuit fault locality.

## 2. Exact Bell-link identity

For a d-dimensional input A and channel M:A->B, let

    Phi_AA' = |Phi_d><Phi_d|,
    Omega_M = (M tensor id_A')(Phi_AA'),
    |Phi_d> = d^(-1/2) sum_i |i i>.

With a retained reference, contraction of the actual input with A' by the Bell effect gives

    <Phi_d|_(A_in,A') [rho_(A_in,R) tensor Omega_M] |Phi_d>
       = d^(-2) (M tensor id_R)(rho).

The identity holds linearly for non-CP maps too. It is just the matrix-unit expansion; no physical postselection is asserted in the proposed computer.

A finite quantum comb has the analogous normalized process Choi operator: feed halves of independent Bell pairs into every input port, retain the other halves, and retain each emitted output. For a genuine CP/TNI comb, this is positive and has trace at most one (include terminal timeout branches if needed). Reconnecting an input port of dimension d_j uses its Bell effect and a factor d_j^2. Reconnection order can be rearranged algebraically because the contractions act on separate tensor factors.

## 3. Conditional straightening lemma

Assume a damaged subsystem has been cut from the physical execution as a finite comb B with named input/output ports. Its boundary includes ALL quantum and relevant classical information exchanged with the undamaged computation. Each boundary wire is used once; repeated internal bank accesses are internal to B. The unmarked computation is ideal CPTP on its named quantum ports and identity on B's retained external environment. A cut process with variable event order must first be represented with its complete classical control record or a valid finite process-matrix interface; that representation is not supplied merely by a terminal channel norm.

Let Omega_B be its normalized process Choi operator, or the corresponding operator-valued map if the initial bath is retained. If the cut-process norm obeys

    ||Omega_B|| <= epsilon_F,

then reconnecting m input ports with dimensions at most d has norm at most

    d^(2m) epsilon_F.

Here the norm is trace norm for an already-fixed initial bath, or the completely bounded/diamond norm of the retained-bath map. Bell effects, state preparations, relabellings, and tracing auxiliary factors are CP/TNI contractions. The only norm amplification is the displayed Bell-link normalization. The statement extends by linearity to signed coefficient maps, provided the same cut-process norm is available.

For the static destructive-transfer fabric, the boundary-port lemma gives m <= c k |F| for a fixed geometric incidence constant c. Thus straightening costs only

    (d^(2 c k))^|F|.

The reconnected expression can be regarded as a circuit-order tensor expansion or as local CP/TNI Bell-interface insertions using a correlated retained auxiliary state. It is NOT a claim that the original bad process was a single CPTP gate. If a conventional threshold receiver is to be invoked, its fault-path expansion must allow these correlated insertions and this norm factor, or an explicit expansion into the receiver's local linear-map basis must be made.

## 4. What is established by the destructive reset

For a bank produced by an undamaged gate, every earlier operation on that bank is overwritten at production. For a bank consumed by an undamaged gate, every later operation on it acts on a freshly reset disposable register. Therefore the only unknown quantum information exchanged with B occurs at its boundary's production/consumption cuts. This justifies the finite quantum-port count even for arbitrary replay times.

It does NOT automatically bound classical timing/control information crossing the same boundary, guarantee all ports occur within a finite horizon, or construct the cut process from a repaired Gács history. Those require the physical adapter proof.

## 5. The actual remaining norm question

A small norm of the CLOSED endpoint error map does not imply a small norm of its OPEN process Choi map: opening ports changes the tester, and can remove cancellations or expose hidden conditional dependence. Therefore the existing inclusive cavity estimate cannot be reused by writing epsilon_F=q^|F| without a new check.

A sufficient receiving statement would be: the inclusive marked-box bound holds uniformly after replacing any of these finitely many boundary exchanges by CP input preparations/output captures, with the same all-state service witnesses and a bounded incidence enlargement. Then Bell feeding is such a replacement, and the displayed norm estimate follows. The actual native witness is reference-stable and all-state, which is encouraging, but the preservation of its service and forest hypotheses under these cut-port interventions still needs proof.

No stronger conclusion is claimed here. This is a concrete route for closing the retained-comb objection, not an assumption that it has already closed.
