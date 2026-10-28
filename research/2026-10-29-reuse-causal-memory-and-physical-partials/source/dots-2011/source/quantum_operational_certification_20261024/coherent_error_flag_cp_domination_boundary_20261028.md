# Reduced Pauli noise does not establish the complete-memory Pauli premise

28 October 2026. Root boundary construction; independent receiving pending. This does not invalidate the received complete-Pauli-instrument theorems. It shows why system-only Pauli calibration cannot certify their joint-memory premise, even when every single-call reduced channel is exactly Pauli.

Take the native isometry

    A|psi>=sqrt(1-p)|psi>|0>_M+sqrt(p)Z|psi>|1>_M,
    0<p<1.

The error flag is retained COHERENTLY in memory, not dephased into an actual complete CP mixture. Tracing M gives the exact Pauli channel (1-p)id+p Ad_Z. The unknown coherent mixer can be identity in this example. Let the nominal learned inverse have a small coherent error W=cI−isZ, c²+s²=1. Its virtual entanglement infidelity is b=s².

Apply a fresh uniformly random input Pauli Q and output inverse Qdagger, after W, then retire Q. Pauli averaging of the COMPLETE isometry produces two logical Pauli branches with memory vectors

    l_0=c sqrt(1-p)|0>−i s sqrt(p)|1>,
    l_Z=−i s sqrt(1-p)|0>+c sqrt(p)|1>.

The exact-inverse, equally framed reference instead has memory vectors sqrt(1-p)|0> and sqrt(p)|1>. In the logical-identity Choi block, subtracting (1-b)=c² times the exact reference gives

    |l_0><l_0|−c²(1-p)|0><0|,
    determinant=−c²s²p(1-p)<0.

The complete CP domination asserted for a genuinely Pauli-diagonal native instrument therefore FAILS in this different source class. In fact no positive multiple of the exact reference branch is dominated when the two rank-one memory vectors are noncollinear. A vector orthogonal to l_0 witnesses the negative quadratic form directly.

For a normalized Bell input, the complete learned-minus-reference output is block diagonal on the two orthogonal logical Bell states, with memory blocks D and −D, where

    D=[[-b(1-p), i c s sqrt(p(1-p))],
       [−i c s sqrt(p(1-p)), b p]].

Its half trace distance is exactly

    ||D||_1=sqrt(b)*sqrt[b(1-2p)²+4p(1-p)].

For fixed0<p<1 this has order sqrt(b), not order b. After tracing memory, the reduced system-channel half-diamond difference is only |1-2p|b. At p=1/2 the reduced channels are IDENTICAL while the complete Bell/memory outputs differ by sqrt(b). Future interactions capable of exposing these correlations can distinguish them; if the actual port never accesses them, that is a separate operational-quotient condition, not a full-memory norm statement.

The two source forms must not be conflated:

1. Complete CP Pauli instrument sum_f Ad_Pf tensor F_f: permits arbitrary coherent updates WITHIN each branch and dephased which-error records; the received learned-inverse CP domination applies with its other hypotheses.
2. Coherent superposition of different error labels retained in memory: system-only reduction may still be Pauli, but cross-error coherences can interfere with receiver error before the private average. The same CP domination does not follow.

The complete-input/output process-learning route can address such distinctions under its actual IC port/rank/stationarity promises. A generic operator-norm inverse approximation also supplies a complete norm debit, but this example forbids replacing that debit by the small Bell loss without a further mechanism. No generic impossibility of learning coherent noise, historical novelty, source acquisition or hardware result is claimed.
