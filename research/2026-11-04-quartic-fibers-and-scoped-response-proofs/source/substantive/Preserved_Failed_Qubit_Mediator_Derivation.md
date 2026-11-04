# A two-body qubit mediator: exact single-check calibration fails to compose

Working internal calculation, 2026-11-04. No scalable-memory, novelty, thermal
phase, native-bath, or practical-advantage claim. This is not a replacement for
the existing stronger native qudit-clock constructions.

## Target and primitive

For three commuting Pauli factors P1,P2,P3 on distinct data qubits, add one
ancilla a and use Delta=1, lambda=r, mu=-r:

    h = B + (1 + mu P3) n_a + lambda (P1+P2) X_a,
    n_a = (I-Z_a)/2.

Every term is one- or two-body on qubits. Put

    F(c) = [(1+mu c)-sqrt((1+mu c)^2+16 lambda^2)]/2,
    f0 = [F(+1)+F(-1)]/2, f3 = [F(+1)-F(-1)]/2,
    B = -f0 (I+P1P2)/2 - f3 P3/2.

In a joint data eigenstate with a=s1*s2 and c=s3, the ancilla's lower eigenvalue
before B is zero when a=-1 and F(c) when a=+1. Hence the full lower eigenvalue
is exactly (f3/2)*a*c. This proves an exact single-check ground-band spectrum,
with target coefficient J=f3/2. It does not prove a tensor product encoding
compatible with overlapping noncommuting physical factors.

## Decisive adverse example

Choose the commuting target checks

    S1=X1 X2 X3, S2=Z1 Z2 X4.

They overlap on two qubits. Use two copies of the gadget, with ancillas a,b.
The target -|J|(S1+S2) has a four-dimensional degenerate ground space.
The calibrated six-qubit Hamiltonian does not: its lowest four levels split.

The comparison includes the third-order truncation of the same construction,
with B0=2 lambda^2 (I+P1P2), B3=-2 lambda^2 mu P3. Its lambda is reduced to
sqrt(|J_exact|/(2|mu|)) so that both constructions have the same intended J
and satisfy the same lambda upper bound, Delta, |mu| and qubit count.
This is a matched comparison within the mediator family, not a proof that it
is the strongest possible two-body architecture.

At r=.1, exact single-check calibration gives a lowest-four splitting of
0.451829919788815 times |J|. The matched third-order truncation gives
1.47359089132349 times |J|. The single-check gain does not supply a protected
logical manifold.

Independent reconstruction in four 16-dimensional sectors, using the conserved
data X3 and X4 eigenvalues, confirms the full 64-dimensional spectrum at 70
decimal digits for r=.02,.1,.2. COMPOSITION_70_DIGIT_CERTIFICATES.json retains
the values, independently of the floating dense construction.

## Sustained construction: cancel the fourth-order overlap term

The split has a simple leading obstruction, which can be canceled without
adding a three-body term. For a finite family of these gadgets, write
A_g=P_g1+P_g2 and C_g=P_g3. The expansion of the exact single-check counterterm
is

    B_g = r^2 A_g^2 + 2 r^3 C_g - 3 r^4 A_g^2 + O(r^5).

Let P project onto all ancillas zero. A Feshbach expansion about
H0=sum_g n_g yields a zero second-order term, the desired
-2 r^3 sum_g P_g1 P_g2 P_g3, and the fourth-order residual

    R4 = -(1/2) sum_(g<h) [A_g,A_h]^2.

For completeness, the self contribution is
-3 A_g^2 - A_g^2 + A_g^4=0, since A_g^4=4 A_g^2. For each distinct pair,
the counterterm insertion contributes A_g A_h^2 A_g+A_h A_g^2 A_h.
The double-excited ancilla has energy 2, so the four hopping paths subtract
half this sum and half (A_g A_h A_g A_h+A_h A_g A_h A_g). The difference is
exactly minus half the squared commutator. Terms involving the unknown
eigenvalue in the resolvent start at order r^5 because the second-order
effective Hamiltonian has been canceled.

Here every A is a sum of single-qubit Paulis. Its commutator with another A
is a sum of single-qubit Paulis on their shared sites; its square therefore
contains only constants and two-body terms. Thus adding

    H_shield = +(r^4/2) sum_(g<h) [A_g,A_h]^2

cancels the complete fourth-order coefficient in the finite-system expansion.
Bounded incidence bounds the number of such terms per data qubit. This is a
scoped perturbative cancellation, not an all-orders or thermodynamic theorem.
Perturbative gadgets and shielding are established ideas; no priority claim
is made for this specialization.

In the example A=X1+X2, B=Z1+Z2, the residual is
4 r^4(I+Y1Y2), since [A,B]=-2i(Y1+Y2). In the target ground sector it gives a
leading split 8 r^4, consistent with the exact spectra. The added shielding
term is -4 r^4(I+Y1Y2). At r=.1 it reduces the split to
0.128250970013218 times |J|, but does not restore exact degeneracy.
At r=.02 the unshielded and shielded ratios are .0830501215648851 and
.00635364127960058 respectively. The higher-order remainder is real.

## The central unclosed physical step

An isolated low-ancilla-band expansion is insufficient at nonzero temperature
and increasing volume. There is a finite density of excited mediators at every
fixed finite temperature. Excitation-preserving resonances and mediator motion
must be included, together with the actual local bath and all clock levels.
No uniform thermal Peierls bound, logical operator algebra for this all-qubit
model, preparation mechanism, or physical lifetime follows from canceling R4.

Taking Delta to grow with the total system size, taking r to zero with size,
or silently discarding all excited mediators would change the resource
contract. No such step is used as a successful construction here. Existing
fixed-dimensional qudit clocks already offer a stronger internally reviewed
all-spectrum reference. Restricting to qubits does not by itself earn a greater
consequence or a better operating point.

## Numerical correction and retained scope

The first baseline comparison held lambda fixed in both models, which gave
different intended target J. It was replaced by the matched-J comparison
described above. Only the corrected JSON and 70-digit reconstruction support
the numbers reported here. Single-check exact spectra were checked across
nine r values; that finite check is distinct from the algebraic proof.

The fourth-order identity is a finite-system formal expansion with an explicit
derivation. No size-uniform remainder or complete finite-temperature memory
proof is asserted. The mission remains NOT ACHIEVED.

## Primary comparisons

* Kempe--Kitaev--Regev, The Complexity of the Local Hamiltonian Problem,
  https://arxiv.org/abs/quant-ph/0406180: perturbative locality reduction is
  established, not an invention of this study.
* Jordan--Farhi, Perturbative Gadgets at Arbitrary Orders,
  https://arxiv.org/html/0802.1874v4: higher-order perturbative simulation is
  established and does not automatically provide the needed thermal theorem.
* Ocko--Yoshida, Non-perturbative gadget for topological quantum codes,
  https://arxiv.org/html/1107.2697v3: exact two-body qudit gadgets and shielding
  are strong prior work, with their stated model scope.

No external publication or messages occurred; source code remains private.
