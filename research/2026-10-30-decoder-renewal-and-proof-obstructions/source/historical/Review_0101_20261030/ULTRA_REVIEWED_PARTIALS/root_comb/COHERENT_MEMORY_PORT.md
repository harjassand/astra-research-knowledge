# A fixed known memory port for the growing feedback controller

30 October2026. Root algebraic construction. This is a literal circuit
interface, not a proved high-fidelity recurrence. It changes no frozen C map.

## 1. Factor the known four-label environment once

The existing conditional Pauli isometry, with real J=-iY, is

    V(a,b)|m> = b sum_(P=I,X,Z) P|m>_A |P>_E
                        + a J|m>_A |J>_E,
    a^2+3b^2=1.

Use the same FIXED known real orthogonal change of basis on E for every a,b:

    (|I>+|Z>)/sqrt2 -> |M=0,R=0>,
    (|X>+|J>)/sqrt2 -> |M=0,R=1>,
    (|X>-|J>)/sqrt2 -> |M=1,R=0>,
    (|I>-|Z>)/sqrt2 -> |M=1,R=1>.                         (C1)

Then the entire isometry becomes exactly

    V_can(a,b)
      =[(a+b)I_MR+(b-a)SWAP_MR]
                           (id_M tensor |Phi_2>_AR)
      =[2b P_+^(MR)+2a P_-^(MR)]
                           (id_M tensor |Phi_2>_AR).     (C2)

One can check(C2) directly on the two input basis states. In order(M,A,R),

    |0> -> sqrt2 b |000>
             +(a+b)/sqrt2 |011>+(b-a)/sqrt2 |110>,
    |1> -> sqrt2 b |111>
             +(a+b)/sqrt2 |100>+(b-a)/sqrt2 |001>.

Their supports are disjoint and each squared norm is a^2+3b^2=1.
Equivalently <Phi_AR|SWAP_MR|Phi_AR>=I_M/2, so the operator in(C2)
is an isometry on the displayed Bell-appended INPUT SUBSPACE.

It is NOT a unitary filter on arbitrary existing M,R data, and it does not
grant postselection or amplify arbitrary states for free. Its physical
implementation is the already explicit Pauli Stinespring isometry followed
by(C1), with its known finite-dimensional unitary completion.

At a=b=1/2 it is exactly id_M tensor |Phi>_AR. Thus an old logical memory
port and a fresh Bell query pair are exposed in a fixed, parameter-independent
basis. Away from that point the old information is distributed across M,R,A;
the named M output is a KNOWN port, not an assertion that the old input is
restored on that port.

## 2. Compose the actual physical feedback coherently

Let P_s^(B0,Bprev) be the known whole-physical-register SWAP sectors. The
existing C feedback has the canonical form

    sum_(s=+,-) P_s^(B0,Bprev) tensor
               [2b_s P_+^(MR)+2a_s P_-^(MR)]
                              (id_M tensor |Phi>_AR).    (C3)

Send the A output through the next ordinary source call and retain M,R and
its new physical output. Nothing is conditioned on an unknown microscopic
junk label; both SWAPs are known operations on named laboratory registers.
The source itself is not controlled, conjugated or inverted.

This supplies an explicit uniform family of UNClOSED controllers. Query1 is
the initial Bell source query, leaving its known reference as M and its
physical output B1. For t=2,...,Q apply(C3) using B0,B_(t-1), the current M
port and a fresh Bell pair, then query the new A. Retain B0,...,Bt, all newly
created R's and the new M port until final extraction. A later controller
can use this named port without first interpreting an opaque four-label E.
It may also act coherently on the retained history. Parameters are known
numbers and a_s^2+3b_s^2=1 for each sector at every step.

The preprocessing portion uses Q native calls, one of which may be offline,
O(Q log D+Q) protected qubits and O(Q log D) known-control gates for fixed
precision per cell, plus allocated synthesis error. All subsequent calls
are online in this schedule. The final known decoder's circuit size and its
precision must still be supplied. An arbitrary final CPTP map on an
exponentially large history has NOT been credited as a polynomial circuit.
At Q=2, the original finite group kernel and rational24->2 decoder provide
that final map explicitly. No such high-accuracy all-Q extraction is proved.

## 3. The exact scientific gate is still present

The identity(C2) solves a representation/interface issue: the known logical
memory can be named at every step in a fixed basis. It does not close its
state evolution on M alone. Newly created R's, physical carriers and their
correlations are real quantum history. Erasing them to assume a fresh
independent programme at every step produces a different process.

To establish a scalable operation one must now derive the whole retained-
history channel or a justified sufficient state, supply a known final
extraction circuit, and prove a full error bound at its original source bill.
For a weak deformation a=1/2+eta, b=1/2-eta/3+O(eta^2),

    2b P_+ +2a P_- =I+(2eta/3)I-(4eta/3)SWAP+O(eta^2).

This is a real isometric-dilation deformation, not an assumed Hamiltonian
step. A useful logical signal and its second-order dissipation must be
computed in the actual history state. The old independent-Choi HME route
already has signal1/r and constant one-collision variance, giving a quadratic
rank bill; renaming that collision as feedback is not an improvement.
An O(1/r) noise suppression, a different coherent recurrence, or a robust
obstruction would materially decide the new route. None is asserted here.

The accepted exact-heralding Schur theorem excludes exact renewal as a
subquadratic-r substitute. Approximate coherent history remains open.
No source, quantum circuit, parameter scan, optimizer or physical experiment
was executed to obtain this algebraic port.
