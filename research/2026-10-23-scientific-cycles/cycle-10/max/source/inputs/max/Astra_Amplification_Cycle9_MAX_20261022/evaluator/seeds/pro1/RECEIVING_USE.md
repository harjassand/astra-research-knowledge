# Receiving use of the nonlinear response operation

## Interface

Use this operation for the native root-retaining recurrent qutrit device,
with the physical bulk compressed to initial depth at least the block length.
Let \(\sigma=\operatorname{diag}(1/2,1/4,1/4)^{\otimes k}\).
An admissible input operator \(J\) must be Hermitian and decomposed into
endpoint-pair blocks \(J=\sum_{i<j}J_{ij}\) that only change the binary charge
patterns \(01\leftrightarrow10\), with identical spectator charges. It must
commute with \(\sigma\).

Retain each original \(J_{ij}\) when spectator interactions are analytically
deleted. Define \(t_{ij}=\|\sigma J_{ij}\|_1\). Then the exact history argument
gives
\[
 \operatorname{Tr}_A[(\sigma J\otimes I)G(b)]=b(1-b)F_J(b),
\]
\[
 \|F_J(b)-F_J(0)\|
 \le4\sum_{i<j}t_{ij}\,[1-(1-b)^{k-2}].
\]
The first coefficient \(F_J(0)\) may be nonscalar. It must be controlled as a
full operator on all coherent/entangled bath prefixes, not just by a prefix
average. The exact proof, phase table and partial-trace bound are in
`NONLINEAR_ENDPOINT_RESPONSE.tex`.

For the actual Cycle7 \(H\), \(t_{ij}\le1/4\) and \(F_H(0)=v_kI\), giving
the stated new uniform bound. No analytic prefix state is physically prepared.

## Physical receiving obligations

The interface alone is not a coding theorem. Supply an actual positive,
normalized charge-preserving input density; bound its entropy with a
growing-block remainder; show strict exact inward operator drift in the
physical bulk; and pay the finite root term. Only then use the inherited
homogeneous-Kraus operator Lyapunov and full compression argument.

The present archive supplies all these steps for
\[
 \rho=\sigma-\tfrac12(\ln2)b\,\sigma H
          +\tfrac{4mb^2}{k}\sigma(Q-k/2),\qquad
 m=3(\ln2)v_k/16,\qquad bk^2\le1/16.
\]
The resulting code is initializer independent and pointwise all-normal,
with full-diamond arbitrary-reference error. Beta and block length must
remain fixed before the outer coding horizon.

## Counterexample to an omitted premise

The charge-preserving four-endpoint operator
\(J=|0101\rangle\langle1010|+\mathrm{h.c.}\) has a nonzero
\(b^2(1-b)^2/32\) contracted bath diagonal entry despite no pair-supported
first response. Thus total-charge preservation cannot replace pair support.
The independent executable witness is in
`contributions/independent_challenge/four_endpoint_witness.py`.

A separate one-call vacuum example defeats extending the bulk drift formula
globally. Retaining the native root term is essential.

## Specific actual receiving use this cycle

| Prior capital | Actual use | New consequence |
| --- | --- | --- |
| Cycle7 exact \(v_k\) and \(T_k(\sigma H)=v_kI\) | Uniform leading inward certificate | Exact drift stays negative after all-order response errors |
| Cycle7 explicit endpoint color blocks | Derive \(\|\sigma H_{ij}\|_1\le1/4\) | Nonlinear operator error is summable over all pairs |
| Native diagonal drift identity | Evaluate both \(\sigma\) and signed \(Y\) exactly | No reference or diagonal-correction error is charged |
| Inherited operator Lyapunov and complete compression | Convert actual inward drift plus entropy into codes | Achievable excess improves from \(\beta^{7/2}\) to \(\beta^3\) |

These are mathematical receiving uses. Delivery, indexing, a finite replay,
or internal agreement is not evidence of a general research-method advantage
or recursive amplification.

## Private receiver instructions

Read the canonical ZIP identity in the external delivery receipt, materialize
the exact bytes through the authorized private file route, verify size and
SHA256, and extract into a separate directory. Do not overwrite the preserved
originals. Read the current main proof and continuation before relying on a
summary. `verify_package.py` checks file integrity only.

If the receiver can read UTF-8 source but cannot materialize ZIP binaries,
the delivery may additionally expose ordered base64 parts and a transport
manifest. Decode only those exact returned references and verify the canonical
ZIP identity. The delivery receipt distinguishes actual roundtrip verification
from reading, scientific acceptance and integration.
