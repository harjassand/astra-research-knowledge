# Higher-dimensional boundary: zero record leakage does not force unitary recovery

28 October2026. Author exact counterexample using the standard Werner–Holevo channel. Independent review pending. This is a scope boundary for the new qubit theorem, not a new Werner–Holevo construction or a claimed quantum-storage capability.

For odd dimension d>=3 define the CPTP unital channel

    N(rho) = [Tr(rho) I − rho^T]/(d−1).

A Kraus representation is K_ij=(|i><j|−|j><i|)/sqrt(d−1), one for each i<j. Their adjoint products sum to I. Treat N as an instrument with ONE classical outcome. Its record is exactly constant, so its record-channel distance to constants is zero.

Nevertheless a nonunitary recovery can outperform every unitary recovery. Choose recovery D=N. Direct composition gives

    N²(rho) = [(d−2)Tr(rho) I + rho]/(d−1)²,
    F_e(N²) = 2/[d(d−1)].

For a unitary recovery U, the Kraus trace formula gives

    F_e(U composed with N)
      = [d − Tr(U conjugate(U))]/[d²(d−1)].

The trace is real. The unitary W=U conjugate(U) has conjugate-paired spectrum because conjugate(W)=U† W U, and det(W)=1. For odd d, its unpaired real eigenvalues include at least one +1: the number of −1 eigenvalues is even by the determinant, while the total number of real eigenvalues is odd. Thus Tr(W)>=2−d. Equality is attained by real orthogonal U having one1×1 block +1 and(d−1)/2 blocks [[0,1],[−1,0]]. Consequently

    max_unitary U F_e(U composed with N) = 2/d².

At d=3, the actual CPTP candidate D=N achieves1/3 while all unitary receivers achieve at most2/9. Hence no universal higher-dimensional version of the qubit zero-leakage receiver conclusion is possible. We do NOT need or assert that D=N is the full-CPTP optimizer. The lower bound from this explicit candidate already gives a strict separation.

Crucially D=N is UNITAL. The failure is that unital channels in dimension3 and above need not be mixtures of unitaries, unlike qubits. Therefore the relevant higher-dimensional comparison is **nonunitary versus unitary** recovery, not necessarily nonunital versus unitary. The qubit theorem remains a statement in which any premium requires a nonunital receiver because every unital qubit receiver is mixed-unitary.

This example does not establish useful coherent storage: in dimension3 the corrected depolarizing channel N² is at the entanglement-breaking boundary. It is used solely to show which structural step fails beyond qubits.

Primary channel source: R. F. Werner and A. S. Holevo, *Counterexample to an additivity conjecture for output purity of quantum channels*, arXiv:quant-ph/0203003 (2002), https://arxiv.org/abs/quant-ph/0203003 . The channel definition and the counterexample calculations above are explicit; no external claim of novelty or optimality is borrowed from the source.

The dimension3 entanglement-breaking statement can be checked without an external classification theorem: N²(rho)=(rho+Tr(rho)I)/4 equals the Haar measure-and-prepare channel3 integral <psi|rho|psi>|psi><psi| dpsi, by the second-moment identity. Its normalized Choi has Bell overlap1/3, the maximum possible for a separable qutrit-pair state. Increasing the isotropic identity coefficient would exceed that separable overlap, explaining the boundary terminology.
