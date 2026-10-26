## ASTRA — Whole-run quantum-private control

The strongest new direction is to certify an entire sequence of private quantum-control keys at once, rather than paying a separate secrecy penalty for every gate.

The previous harmonic-key construction gives exact positive fault branches when the frame keys are independent of the interacting bath. But even a small correlation with the bath can invalidate that exact decomposition.

A different construction handles imperfect privacy: prepare a complete classical key tape, use quantum-secure privacy amplification to make it approximately uniform against the entire apparatus, and execute the gate sequence using that tape.

If the complete tape has trace distance at most \\(\varepsilon\\) from an independent uniform tape, then the resulting entire adaptive quantum process is within \\(\varepsilon\\) of the ideal framed process:

\\[ \boxed{ D(\rho\_{\mathrm{actual\ run}},   \rho\_{\mathrm{ideal\ framed\ run}}) \leq\varepsilon. } \\]

Crucially, this is one error allowance for the whole run, not one allowance per gate.

The theorem permits an arbitrarily large noncommuting quantum bath and adaptive feedback. It requires a correctly implemented frame-controlled operation, an initially protected key tape, and secrecy against all quantum systems that could be correlated with the raw randomness. The ideal positive-fault theorem applies to the comparison process; approximate privacy does not create exact fault labels in the real process.

### Independent computational verification

I implemented two coherent quantum calls sharing the same bath, with a public Toeplitz-hash seed and quantum side information about the raw random string. All 2,048 possible public seeds were enumerated.

| Verified quantity                           | Result                   |
| ------------------------------------------- | ------------------------ |
| Actual joint key–bath distance from uniform | 0.03018                  |
| Complete two-gate process distance          | 0.00964                  |
| Quantum leftover-hash theoretical ceiling   | 0.16332                  |
| Exact ideal positive fault-path residual    | \\(2.03\times10^{-16}\\) |

The full process includes an input entangled with an untouched reference and a noncommuting, never-reset bath. The numbers are exact finite-model calculations within numerical precision, not laboratory measurements.

One finding is especially relevant: a particular public hash seed can perform very poorly, even when the jointly seed-aware protocol has a valid security guarantee. One must keep the public seed inside the security analysis rather than select a convenient successful seed afterward.

## Stronger consequence: reducing the randomness-certification cost

The whole-run construction has a substantial resource advantage when private randomness must be extracted from a source with quantum side information.

For 1,024 quantum operations, each requiring two private control bits, with a total secrecy allowance of \\(10^{-3}\\):

Separate extraction per operation

# 40,890 bits

Sufficient raw conditional min-entropy budget

One extraction for the full run

# 2,066 bits

Sufficient raw conditional min-entropy budget

This is a 19.79-fold reduction in the sufficient raw entropy budget relative to the specified separate-extraction approach, not a reduction in the 2,048 actual frame bits required.

The public extractor seed also has a cost: a straightforward Toeplitz implementation would require 4,113 independent public-seed bits for this example. A controller already equipped with trustworthy private random bits may therefore be simpler than either extractor.

The underlying quantum-proof extraction theorem is established work.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://arxiv.org\&sz=32)

arxiv.org

+1



### Three decisive failures

The continuation also produced independently executable counterexamples.

- Arbitrarily small quantum key leakage: even when the key marginal is exactly uniform, a key–bath correlation of trace distance 0.000375 can eliminate every exact independent-key substate. An approximate security bound cannot be treated as an exact positive fault probability.
- Key reuse: two individually uniform but identical frame bits produce an operational trace-distance discrepancy of 0.25 in an explicit coherent two-call example.
- Public seed disclosed too early: a raw source that adapts to the hash seed can retain at least four bits of conditional entropy while producing an entirely predictable two-bit extracted key.

These failures identify exactly which privacy and causal-independence assumptions must be physically established.

## Preserved research

All four executable studies passed the final consolidated rerun. The archive contains the full mathematical proof, four Python programs, actual results, counterexamples, validation log and verified checksums.

Complete scientific derivation

Whole-run theorem, complete-memory proof, entropy budgets, mathematical limitations and physical requirements

Reproducible research archive

Four executable Python studies, JSON outputs and validation records

Scientific conclusion: Astra can now connect its exact quantum-memory fault accounting to imperfect, quantum-private randomness without charging the secrecy approximation separately at every gate. This strengthens the conditional architecture, but is an application of established privacy-amplification and composability principles rather than a demonstrated foundational discovery.

The next high-leverage physical problem is still the causal endpoint interface: certifying that the real randomizing gates do not expose their keys to the interacting apparatus and that their complete quantum instruments match the stated control model. The new construction reduces the randomness-certification overhead; it does not remove that physical requirement.