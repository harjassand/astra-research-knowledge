# Weighted two-axis optimality without a central third response
2026-10-29. New author lemma, independent receiving pending. This is an analytic decoder comparison, not an acquisition theorem.

Consider qubit-input CPTP N whose three response operators, in an unknown output decomposition C2 tensor H_junk, are
 Delta_x = X tensor a W,
 Delta_y = Y tensor b W,
 Delta_z = Z tensor J,
where a>=b>=0, W>=0, J=J*, and J>=-bW. The output background N(I/2) is arbitrary subject to N being CPTP. The junk matrices J and W NEED NOT COMMUTE. Direct sums of such blocks are also allowed, with independent parameters and a common chosen logical frame on each block.

Then extraction of the displayed qubit, discarding junk, is an exactly optimal maximally mixed entanglement-fidelity decoder. Its fidelity is
 Fopt(N)=1/4+1/4[(a+b)Tr W+Tr J].
For direct sums, sum the bracketed contributions and retain ONE global1/4 baseline. No claim that this decomposition/extraction is known or physically supplied is made.

## Elementary positive-semidefinite upper certificate
Let L=sum_(c=x,y,z) sigma_c^T tensor Delta_c on a clean test qubit, the displayed output qubit and junk. Set
 Y0=I_output_qubit tensor [(a+b)W+J].
Then I_test tensor Y0-L>=0. To verify, diagonalize only the two known qubits in the Bell basis. The four junk-valued blocks are
 0,
 2(aW+J),
 2(bW+J),
 2(a+b)W.
They are positive by J>=-bW and a>=b. This proof nowhere diagonalizes W and J simultaneously. For any CPTP recovery, its Choi operator is positive with the appropriate output partial trace identity; pairing with the displayed slack gives an upper bound on its response objective. Equivalently, expand a Stinespring Kraus representation and sum the nonnegative Bell-block quadratic forms. The extracting decoder attains equality because its Choi support selects the zero slack block. The factor1/8 in the Pauli response formula yields the stated1/4 times the weighted traces.

This is the precise opposite-chirality boundary: negative J is allowed down to -bW; one does not need to identify its eigenvectors or interpret it as a classical sign register. The bound is objective-specific, not a channel capacity or entanglement-breaking classification.

## Relevance to approximate-central acquisition
After analytically rounding two nearly Pauli axes, one may try to replace the positive record weight by its Pauli twirl, yielding I2 tensor W. The third response need only be approximated by Z tensor J satisfying the LOWER order bound above; it need not commute with W. A possible analysis-only repair is J=W^(1/2) max(Z0,-bI) W^(1/2). This expression remains meaningful for singular W and supplies the order bound without assuming a minimum eigenvalue. However a bound on how much this repair changes the actual response is still required. The lemma does not supply that bound or an executable unknown matrix square root.
