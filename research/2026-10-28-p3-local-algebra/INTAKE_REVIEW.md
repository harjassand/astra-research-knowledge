# Completed internal review of the acquired local-algebra archive

Decision: **accepted, internally verified**, at the exact versions bound in
`knowledge/reviews/A1122-local-algebra-*.json`. This is a completed intake-owner
proof/interface review recognizing the acquired substantive independent audits.
It does not promote every statement in the 251-member archive. No scientific
archive program was executed by this intake.

## Acquisition and quotient fitting

Read the computational statement and algebra acquisition in
`proofs/Astra_P3_Acquired_Local_Algebra_Counters.tex`, the quotient-fitting and
weighted descent in `proofs/Local_Algebra_Stationary_Proof.tex`, and the completed
`GENERAL_MODULE_QUOTIENT_AUDIT.md` and `WEIGHTED_QUOTIENT_AUDIT.md`.
The input is the original cubic Boolean ANF, not an oracle supplying a useful
ring, basis, center or phase. Radical freeness, the full chain centroid and a
free module are acquisition gates. Fitting is an ordinary coefficient identity
modulo the justified quotient. The center is acquired modulo `J^(e-h)`; a
full-ring solve can reject an otherwise valid quotient fit. Rank-three fitting
requires `d>=3`; the counting theorem separately requires `3h<=e+1`.

The weighted origin branch is `(e,h)->(e-3,max(h-1,0))`. Omitting the quotient
weight is a real error: the archived audit retains an `e=3,h=2` counterexample
outside the legal height range. Accepted units expose the actual height and
costs, rather than extending coefficient-fitting completeness to counting at
every height. The rank-three fixed-variable point-count closure is mathematical;
its general engine has not been shipped.

## Pair acquisition, Gaussian states and eight moments

Read `proofs/Local_Algebra_Finite_Moments_Proof.tex` and the completed
`EIGHT_MOMENT_TERMINAL_AUDIT.md`, then inspect the actual callback in
`work_chain_root/acquired_pair_counter.py` and the production alias at the end of
`work_stationary_prior_agent/acquired_pair_terminal.py`.
For `3` not dividing `d`, descent uses `K=S^d`, `D=K^(d^-1 mod 3)` and
`F=D^-1 S`. The common phase coefficient after descent is
`gamma=theta gamma0 t^3`; the radial coefficient remains separate. Full ordinary
coefficient equality, not sampled equality of polynomial functions, certifies
the pair template. The binary quadratic pair types must remain binary.

The order-three symmetry fixes the minus Gaussian's sign. Its polar radical
has dimension `0,2,4`, giving at most eight joint Gaussian states. This
field-level identity works at every field degree; the acquisition and deep
lifting theorem still has its separate `d>=3, 3 not dividing d` promise.
The eight displayed moment indices determine signed state masses with
determinant magnitude `2^15*3^7*q^14`. The radial phase and `0^0=1` survive
reconstruction. Seven nontrivial moments are ordinary cubic Artin--Schreier
point counts in at most eight field variables; the zeroth is binary Gaussian.

The callback returns an actual cardinality `N_AS`. The moment is
`N_AS-q^(variables-1)`, not `2*N_AS-q^(variables-1)`. Ordinary field powers must
not be reduced with Boolean idempotence. Source inspection confirms that the
production callback uses the eight-moment alias; the enumerating reference
also retains the older correct 49-moment cross-check. A callback integer/range
check cannot establish that its answer is the cardinality.

The primary Lauder--Wan theorem, [Theorem 1 and its quantitative bounds](https://arxiv.org/pdf/math/0612147),
allows singular affine hypersurfaces and, at fixed characteristic, degree and
variable count `v`, gives field-degree exponents `3v+7` and `2v+4` for time and
space. Thus `v<=8` gives `d^31/d^20`; `v<=4` gives `d^19/d^12` for the separate
rank-three branch. This dependency establishes the stated theoretical bounds.
The archive supplies no general executed Lauder--Wan engine. The default
reference explicitly scans one field coordinate, with a 24-bit degree budget.
No practical speed, scaling experiment, priority or acquired device is inferred.

## Contact counting and its real geometric gate

Read `proofs/Local_Algebra_Contact_Proof.tex` and the completed
`CONTACT_COUNTER_AUDIT.md`. The homogeneous semilinear kernel's binary-independent
vectors are also field-independent when its coefficient matrix is invertible;
the minimal-dependence/Frobenius argument gives `kappa<=b-1`. This bounds a
parameter, not the cost of enumerating its `2^kappa` combinations by a constant.
The contact algorithm acquires its covector, requires both nonsingularity gates,
keeps the weighted radial phase and recurses only at the origin. Its displayed
`(2^kappa+1_(e=1 mod 3)2^d)poly(n+L)` cost remains explicit.

The general-module audit gives a complete obstruction proof for
`H=X1(X2X3+X4X5)`: radical-free third form and full scalar centroid coexist with
a positive-dimensional projective singular quadric and an isolated vertex.
There are `(q+1)^2+1` points, hence 82 over F8, of which 81 have degenerate
transverse Hessian. The contact counter correctly rejects the singular matrix
gate. This witness refutes a proposed implication from acquired centroid to
tractable critical geometry; it is not itself a claimed hardness reduction.

## Fixed-residue hardness and non-transfer to a field decoder

Read the entire `J_RESIDUE_HARDNESS_AUDIT.md` and the corresponding section of
the finite-moment proof. The reduction fixes `F8[t]/t^2`, uses `N>=2` even,
`r=N+1`, `b=2N+3`, `n=12N+18` and no extra binary quadratic. An unused source
input handles odd parity with its known multiplicity. The critical-coordinate
extractor is an explicit ordinary field-linear form. The exceptional zero
fiber contributes `s0=(-1)^p(0)`; it cannot be discarded. With
`Ncrit=2^(N-1)(2^N+1)`, the complete signed ring count is

`ZA=8^(2N+3) [1+3Ncrit+4*2^(N-1)(Zp+s0)]`.

The affine recovery is exact. Independent finite controls check nonzero signed
source counts at `N=2,4`; they do not replay raw 42/66-bit acquisition or exhaust
the full ring input space. The source's circuit-to-cubic hardness proof charges
its extra wire/multiplier summations and normalization. That reduction is
separate from a compiler frontend retaining its original independent inputs.
The fixed `d=3` family lies outside the strong all-depth theorem. We do not
extend the unchanged F8 formula to every degree divisible by three.

An algebra with nonzero nilradical is not the field required by the existing
Frobenius-band decoder. Projecting to the residue discards exactly the higher
nilpotent coefficients that can encode this hardness instance. Conversely,
`e=1` alone does not establish the other decoder's cubic and defect promises.
The new incompatible interface records this obstruction. It makes no claim
that all specially factored field subfamilies lack compatible adapters.

## Acceptance and remaining work

The current N1122 card and the nine named units are accepted at their exact
contracts, recognizing the completed archived audits and this source-exposed
review. Original proofs, failed mechanisms, outputs and audits retain their
bytes. The former summary-only card/status are preserved; the dated semantic
notice resolves only the old source-availability gap, including references to
it in earlier P3 reviews. Other theorem conditions and ETH imports are unchanged.

Remaining: implement and validate the generic point-count engine if an executed
polynomial terminal is wanted; independently benchmark against equally informed
comparators before claiming practical advantage; reconcile other unextracted
archive mechanisms separately. Formal certification and historical priority
are not established. These gaps do not undo the accepted conditional mathematics.
