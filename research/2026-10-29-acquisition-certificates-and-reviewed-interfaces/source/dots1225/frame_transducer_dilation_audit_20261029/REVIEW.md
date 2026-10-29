# Independent receiving review: known-control implementation of the frame transducer

2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`. **Accept the exact dilation and conservative finite arbitrary-single-qubit/CNOT compilation bound.** This establishes a finite known-control construction, not an efficient, fault-tolerant, native or experimentally calibrated implementation. No optimization of constants was attempted.

## Encoding and dilation

Two nine-dimensional input programs occupy two four-qubit blocks with encoded indices16a+b,0<=a,b<=8. These81 indices are distinct in the256-dimensional eight-qubit space. The four four-dimensional outputs occupy all256 basis entries in the ordered tensor convention. Padding K with zero columns on the other175 input indices is therefore the correct physical embedding; it is not padding the81-vector contiguously while claiming a two-block encoding.

The accepted T certificate has TᵀT spectrum {0(46),1/16(25),1/8(1),3/16(9)}. Scaling K=4T/sqrt3 and padding gives A=K†K spectrum {0(221),1/3(25),2/3(1),1(9)}. The Lagrange polynomials therefore give exact mutually orthogonal projectors P_lambda, including all invalid input states in P0. The independent exact check reestablishes the reduced annihilating polynomial, all four projector identities and multiplicities before applying the coordinate embedding.

For lambda>0 set Q_lambda=K P_lambda K†/lambda. Using P_lambda A=lambda P_lambda shows that these are mutually orthogonal output projectors. Q0=I-sum_{lambda>0}Q_lambda completes the output resolution. Then

D=sum_lambda sqrt(1-lambda)P_lambda,
E=sum_lambda sqrt(1-lambda)Q_lambda

are self-adjoint and satisfy D²=I-K†K and E²=I-KK†. The author's displayed E formula is exactly this expression after substituting Q0. Also Q_lambda K=K P_lambda for positive lambda, while Q0 K=K P0=0. Hence EK=KD, including the unit-singular-value sector where the defect coefficient vanishes.

Consequently U=[[K,E],[D,-K†]] is unitary: the two diagonal blocks of U†U are K†K+D²=I and E²+KK†=I, and the cross block K†E-DK† is zero. For input |flag0> tensor |psi>, the output is |flag0>K|psi>+|flag1>D|psi>. Thus measuring flag0 realizes precisely the accepted successful K, with valid failure branch D on flag1, even on data entangled with references. An invalid input basis column has zero success and unit-norm failure; it is not silently accepted. All operators are fixed known real algebraic matrices, unrelated to any unknown-source inverse.

## Exact finite compilation bound

For a512-dimensional unitary, elimination of each strictly lower-triangular entry needs at most one two-level unitary, totalling512*511/2=130816. A triangular unitary is diagonal, leaving at most512 basis phases. Degenerate zero pivots can use identity or a known swap; no numerical nonzero threshold is needed in the exact argument. Since the matrix entries are algebraic, exact arithmetic and positive algebraic square roots specify such elimination coefficients. The executed floating QR is only a diagnostic.

For two distinct9-bit strings at Hamming distance h<=9, choose a no-repeat Gray path of h edges. The first h-1 adjacent basis transpositions move one endpoint next to the other without moving the latter. Apply the desired two-level gate on this adjacent pair and undo those h-1 swaps. This gives2h-1<=17 eight-controlled one-qubit operations. Each adjacent basis transposition is one controlled-X with the other eight bits fixed. A basis phase is likewise one eight-controlled diagonal one-qubit operation. Exhaustive reviewer checks covered all130816 pairs and attained maximum17.

Thus G=17*130816+512=2224384 eight-controlled operations is valid. Seven clean work bits compute the AND of eight positive controls via seven Toffolis, one ordinary controlled-U acts on the data target, and seven reverse Toffolis clean the work. At most16 X gates convert open controls and restore them. Exhaustive256-input truth-table checks verify the AND value and cleanup; linearity extends this reversible computation coherently.

For U=e^{i alpha}Rz(beta)Ry(gamma)Rz(delta), choose A=Rz(beta)Ry(gamma/2), B=Ry(-gamma/2)Rz(-(beta+delta)/2), C=Rz((delta-beta)/2). Then ABC=I and AXBXC=e^{-i alpha}U. The phase on the control completes an exact controlled-U using two CNOTs and four arbitrary single-qubit gates. Each A,B,C counts as an ARBITRARY single-qubit gate, not a native restricted-axis gate.

Choose V with V²=X. The proposed controlled-V/CNOT sequence has target exponent b-(a xor b)+a=2ab, proving the Toffoli action without an unwanted relative phase. Its three controlled-V variants plus two direct CNOTs cost at most8 CNOTs and12 arbitrary singles. Therefore fourteen Toffolis plus controlled-U and open-control flips cost114 CNOTs and188 singles per eight-controlled operation. Overall:

- CNOTs:253579776;
- arbitrary one-qubit gates:418184192;
- combined elementary count:671763968;
- qubits:8 data+1 herald flag+7 clean AND work=16.

These are loose upper bounds, not the78822-rotation floating diagnostic count, not nearest-neighbor routing counts, and not gates synthesized to a discrete universal set. Reset, readout, physical isolation, routing, storage lifetime, precision synthesis and fault-tolerance costs remain additional.

## Error convention

For an L-gate circuit with individually unitary approximations and operator-norm errors at most zeta/L, telescoping gives total operator-norm error at most zeta. Unitary-channel half-diamond distance is at most that operator norm, and initializing work, measuring the flag and discarding subsystems cannot increase it. Thus the unconditioned flagged instrument error is bounded by zeta. Normalizing a rare accepted branch can amplify error and is not covered by that unconditioned bound. The number of ideal arbitrary gates is precision independent; their native synthesis cost and required accuracy are not.

## Executed evidence and provenance

Original source manifest verified. Replayed copied dilation/QR code: orthogonality residual1.8156e-15, off-diagonal QR residual1.5576e-15,78822 floating nontrivial rotations. These values are consistent diagnostics, not exact unitary or finite-precision hardware certificates. Independent exact input-projector checks, encoding validation, exhaustive Gray paths, AND cleanup and integer resource counts are in `check_exact_compiler.py/json`. Original sources were not altered.

Primary decomposition context checked2026-10-29: Barenco et al., *Elementary gates for quantum computation*, https://arxiv.org/abs/quant-ph/9503016. The explicit decomposition/count derivations above govern this receipt; generic gate universality is established prior work. No practical advantage, new universal compiler or hardware execution is claimed.
