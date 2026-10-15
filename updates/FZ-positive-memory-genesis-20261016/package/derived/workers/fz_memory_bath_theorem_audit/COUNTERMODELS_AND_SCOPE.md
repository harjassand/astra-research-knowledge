# Omitted-assumption countermodels and material scope corrections

16 October 2026. These examples delimit the theorem; none is a counterexample
to its stated finite-bath, universal-schedule, fixed-decoder hypotheses.

## 1. A data-controlled clock includes a quantum instrument

Take one unencoded logical qubit and generate a classical clock label
`h=0,1` by measuring it in the Z basis. Suppose both subsequent scheduled
circuits are identity and one calls both schedules good. The resulting
channel is nevertheless

    Gamma(rho) = |0><0| rho |0><0| + |1><1| rho |1><1|.

For `rho=|+><+|`, the output is `I/2`, and
`||Gamma(rho)-rho||_1=1`. A claimed `p_bad=0` would falsely predict zero.
The missing operation is the clock-generating measurement. Its true branches
are trace-decreasing maps `rho -> P_h rho P_h`; their probabilities depend
on the input. After normalization they are not linear channels on all inputs.
Thus one cannot regard them as an externally sampled mixture of conditional
CPTP identity circuits.

A bath can implement the same failure by copying logical Z information into
a clock register and subsequently reading it. Including the generating
interaction in the charged support circuit restores the correct accounting;
declaring only the later identity actions to be faults does not.

State independence of a schedule marginal must not be confused with its
independence from the joint initial state or from bath records. Nor does this
countermodel prove that every bath-controlled schedule fails: bath-only
operations preserve the reduced logical state on average. It proves that the
fresh exogenous schedule decomposition and its probability proof cannot be
discarded in general.

## 2. Outcome conditioning can steer the logical marginal

Let `rho_LB=|Phi+><Phi+|`. Apply a bath-only projective measurement with Kraus
operators `I_L tensor |0><0|` and `I_L tensor |1><1|`. The complete operation
is exactly of the good-schedule form `Id_L tensor Lambda_B`.

Outcome zero occurs with probability `1/2` and produces normalized state
`|00><00|`. Its logical marginal is `|0><0|`, whereas the original logical
marginal was `I/2`. Outcome one behaves analogously. Their average preserves
the logical marginal exactly.

Therefore the good-schedule factorization does not imply preservation after
postselecting each individual quantum outcome. On joint input `L B`, a leaf
Kraus operator `I_L tensor B_alpha` need not define a TP map. The candidate's
proof correctly uses completeness only after summing all such records.

## 3. Pointwise failure events are not one universal event

Let a schedule label `h` be uniform on `{0,...,N-1}` and let admissible error
labels be `e` in the same set. Define an abstract failure predicate by
`Bad(h,e) iff h=e`.

For each fixed `e`, its failure probability is `1/N`. But for every schedule
there exists a failing error, and a schedule-aware choice `e(h)=h` fails with
probability one. The set `h` on which **all** choices are good is empty.

This finite probability countermodel is not offered as a physical code. It
isolates the forbidden quantifier interchange:

    for every e, P_h[Good(h,e)] >= 1-epsilon

does not imply

    P_h[for every e, Good(h,e)] >= 1-epsilon.

The receiving enlarged-envelope certificate is stated in the latter form.
It does not need a union over exponentially many Pauli histories.

## 4. Individual inverses do not correct a coherent span

On an unencoded logical qubit, `I` is inverted by `I` and `Z` is inverted by
`Z`. Those error-dependent inverses cannot be replaced by one decoder that
corrects both. The cross-error matrix is `I^dagger Z=Z`, which is not scalar
identity. The equally weighted I/Z mixture dephases `|+>`.

Likewise, a coherent-span proof for a multi-qubit fault patch must expand in
the **full** Pauli basis of the patch. For a two-qubit patch, `Z tensor Z` is
orthogonal in Hilbert-Schmidt inner product to identity and every weight-one
Pauli. An arbitrary patch Kraus operator therefore cannot be expanded using
only independent single-qubit fault alternatives. A correctable-error set
must include every Pauli product supported on the declared patch.

## 5. A memory-only depolarizing floor is not a joint-bath CP interior

Let `A,B` both be qubits and define `D_A(X)=Tr(X) I_A/2`. Suppose one attempts
to absorb an arbitrary small joint Hamiltonian into the floor by declaring

    N = D_A tensor Id_B + epsilon[-i Z_A Z_B, .]

to be CPTP. Use normalized Choi matrices, and write
`u=|Omega_A> tensor |Omega_B>` and
`v=(Z_A,out tensor Z_B,out)u`. These are orthonormal. The floor has Choi matrix
`I_AA/4 tensor |Omega_B><Omega_B|`. Its compression to `span{u,v}` is
`diag(1/4,0)`. The commutator contributes the off-diagonal block, giving

    J(N)|span{u,v} = [ 1/4       i epsilon ]
                      [ -i epsilon    0   ].

Its determinant is `-epsilon^2`, so it has a negative eigenvalue for every
nonzero real `epsilon`, however small. This proves that memory-only
depolarization has no full joint A-B Choi interior in these directions.

It does not prove failure of the underlying memory or illegitimacy of the
Hamiltonian-plus-depolarization generator, which is itself a valid Lindblad
generator. It disproves this particular extension of the finite-rate CPTP
uniformization argument. The receiving Choi-ball theorem applies to maps on
the memory patch alone; the persistent-bath theorem applies to explicitly
scheduled CPTP A-B interactions. Combining their names does not prove open
norm-ball tolerance of arbitrary continuous A-B coupling.

## 6. Exact bounded example and script scope

The independent script uses the code stabilized by `XXXX, ZZZZ` with codewords
`(|b>+|b xor 1111>)/sqrt(2)` for `b=0000,0011,0101,0110`. It corrects any Pauli
at a known single physical location. A full correction at the first location
separates two faults; the final fixed decoder corrects the second location.
Thus every pair of local Paulis on this particular schedule is correctable.

The first joint unitary is

    U1 = [(5I+12i Z_1 X_B)/13] [(3I+4i X_1 Z_B)/5].

After a complete ideal syndrome correction, apply bath-only amplitude damping
with `K0=diag(1,3/5)` and `K1=(4/5)|0><1|`, then

    U2 = [(8I+15i X_2 Y_B)/17] [(7I+24i Z_2 X_B)/25].

Both factors are unitary by direct squaring of their Pauli involutions. The
same bath qubit participates in both interactions, and its Pauli coefficients
do not commute. Exact recovered Kraus identities and completeness are saved
in `EXACT_CHECKS.json`; no floating-point fidelity criterion is used.

## 7. Scope wording to preserve on integration

The justified positive wording is: "An exact operator extension to arbitrary
finite persistent baths at fresh state-independent scheduled local fault
proposals, conditional on one universal location-only Pauli-history certificate
and its receiving tail theorem."

The following stronger descriptions have not been supplied:

* an unrestricted non-Markovian memory theorem for continuous bath coupling;
* arbitrary bath-controlled proposal intensities from an average-rate bound;
* a state-independent logical channel from an arbitrary correlated bath
  assignment to logical inputs;
* a postselected-outcome identity channel;
* arbitrary noisy initialization, imperfect ideal correctors, readout, leakage,
  or actions on the reference outside the explicit charged fault model;
* an infinite-bath result obtained merely by quoting finite-dimensional
  dimension independence;
* a new general QEC principle, externally validated 4D lifetime, practical
  threshold, engineered reservoir, or acquired memory technology.

Completed correction channels must be named as actual model modifications.
The full pattern completion and the lumped-inactive completion are both
admissible for the Pauli-orbit proof, but they are different quantum channels
on inactive syndrome coherences. The actual construction must specify which
one it implements. The depolarizing floor is a physical-model resource, not
a free analysis step. Arbitrary finite bath dimension is not a bound on bath
engineering, storage, preparation, reset or energy costs.
