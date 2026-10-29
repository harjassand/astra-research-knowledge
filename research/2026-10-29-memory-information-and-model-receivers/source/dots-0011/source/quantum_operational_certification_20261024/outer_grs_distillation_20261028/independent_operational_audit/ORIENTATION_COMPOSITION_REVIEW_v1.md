# Independent operational review: orientation, total decoding and composition

28 October 2026. Reviewer: bridge_operational_memory_recovery, independent of outer-code author. Scope is algebraic circuit/decoder interface and composition, not an independent replay of finite-field implementation.

## Bilateral orientation

For row basis labels and Lin(T)|x>=|xT>, direct application to a basis state gives

    Lin(T)† X(e) Lin(T)=X(eT^−1),
    Lin(T)† Z(f) Lin(T)=Z(fT^T).

Decoding applies Lin(T)† before the first-s trace Fourier gates. Fourier swaps X and Z, up to irrelevant Pauli phase, on those registers. Thus their measured computational differences are f'_first=Hf. The last-s differences are e'_last. Since e=e'T and the first B−s rows of T lie in C=ker H, He=HR^T e'_last. Invertibility of HR^T follows because the R rows complement ker H. Hence the protocol extracts both actual classical syndromes, not an unrelated pair of check values.

Every gate here has a real matrix. For real orthogonal U, (U tensor U)|Phi>=|Phi>; more generally the second side must use the conjugate. Clifford conjugation maps a Pauli label to a Pauli label, so the decoded Bell state factors across all B registers. Measuring/discarding endpoint factors cannot induce an extra logical byproduct beyond the transformed middle Pauli. The forward syndrome differences and exact recovered errors determine precisely that middle Pauli. This verifies the claimed one-way operation at the Bell-label level, including every endpoint outcome, rather than merely a code-existence assertion.

## Syndrome-only BW decoding

The deterministic representative y obeying Hy=sigma differs from the true error by a codeword. With w<=t errors, multiplying the true error locator to monic degree t supplies a solution to the BW equations. Any solution has Q−Ef of degree<B−t and at least B−w>=B−t roots, hence vanishes identically. Polynomial division and distance checks therefore return the correct codeword; uniqueness follows from classical distance2t+1. The actual error vector is y−c. No nearest-codeword oracle is assumed. A fixed flag/fallback beyond the correctable event leaves a total quantum output and needs no reverse communication.

## Independence and stripes

The input contract requires a tensor product across whole inner blocks after averaging fresh independent local randomness. Marginal Bell fidelity alone would not suffice. After bilateral twirling, a whole block has a classical Pauli label, possibly with arbitrary within-block correlations among stripes. The event that at most t whole-block labels are nonidentity implies at most t errors in every stripe simultaneously. Therefore the full output Bell-error probability is at most the single whole-block tail; multiplying by the number of stripes would be an unnecessary weakening.

The small field q=2^ceil(log2B) satisfies B<=q. For payload m growing faster than log B, loss from discarding the incomplete final stripe is less than log2(2B)/m and tends to zero. With t=floor(gamma B), gamma>epsilon0, the threshold (t+1)/B in the binomial upper tail eventually remains separated from epsilon0. The exponent is linear in B. Local circuit deviations must be separately summed or fault-tolerantly controlled; the algebra supplies no noisy-hardware threshold.

## Verdict and limitation

These operational parts of GOVERNING_WRAPPER_v1.md are mathematically consistent. Its equation U_enc=Lin(T)(F^tensor s tensor I) fixes the time order; a nearby prose phrase is awkward, but the subsequent decoding and code use the correct order. Final byte-bound acceptance can be issued once the author freezes its source/clarification. Field programs, exact arithmetic replay, historical priority and practical performance are outside this review. Conventional reblocking prevents treating this composition alone as a new dilute-source capability.
