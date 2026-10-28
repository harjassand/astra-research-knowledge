# Independent receiving: automatic row fast path, finite-M substitution

28 October 2026. **PASS for this scoped composition.**

Reviewed source: `AUTOMATIC_ROW_FAST_PATH_FINITE_M_SUBSTITUTION.md`, SHA-256 `c0846b68556ff828bac8221078ae129c411976f080389470fad5d587bc0ff599`. The source was not edited. This receipt is separate from both the already received local row learner and the new, UNREVIEWED complementary low-loss holdout construction. The latter is not a premise here.

## Accepted dependencies and review scope

I read the automatic local source and its independent audit/receipt, the required implementation-event clarification, the general finite-M wrapper and its root receipt, and the private-framed comparator source/receipt. All six governing version hashes stated in the substitution were verified, as were the ten bindings in the local learner's receipt. The general wrapper root receipt is at SHA `c082a5da23fb63e624cb1933d2f6db681f0f33fbad5e68724fde8139e7a75ad1`.

The new obligations are the local parameter substitution, shared-history power conversion, single whole-block implementation allocation, source-cap scaling and actual early-completion probability. This is not a re-proof or circuit execution of the received matrix acquisition, row estimator, generic fallback, compiler or collective-recovery comparator.

## 1. Correct local ideal-risk substitution

The local automatic learner's equation (3) is an IDEAL averaged Bell-risk bound

    E ell_h <= (1+gamma_local/2)ell_*+17epsilon_local/4096.

With `gamma_local=gamma/2` and `epsilon_local=epsilon/(4M)`, this is exactly

    E ell_h <= (1+gamma/4)ell_*+17epsilon/(16384M).

The substitution does not insert the local one-payload implementation error into this expression. That error is instead recompiled against the enlarged common horizon and paid once below. This distinction is essential and is made correctly.

## 2. Shared-history conversion, including endpoints

Write `a=1-ell_*` and `f_h=1-ell_h`. Every selected encoder/decoder is physically feasible in the comparator family even on a bad training history, so `0<=f_h<=a<=1`. For `f<=a`, the finite factorization gives

    a^M-f^M=(a-f) sum_(j=0)^(M-1) a^(M-1-j)f^j
            <=M a^(M-1)(a-f).

Also every term of `sum_(j=0)^(M-1) a^j` is at least `a^(M-1)`, giving

    M a^(M-1)(1-a)<=1-a^M.

For M=1 the exponent-zero factor is one, including a=0; for a=0 and M>1 both power-difference sides vanish. Thus the endpoint cases are legitimate without an unstated positive fidelity floor.

Apply these inequalities before averaging. The local bound implies

    a^M-E[f_h^M] <= (gamma/4)(1-a^M)+17epsilon/16384.

Therefore the ideal error is at most `(1+gamma/4)Delta_*M+17epsilon/8192`. The law is the correlated mixture with identity weight `E[f_h^M]`, not `(E f_h)^M`. The latter substitution could change the answer substantially and is not used.

The accepted comparator identifies `Delta_*M=2(1-a^M)` for predetermined encoder lists and permitted key-dependent collective recovery, with one physical source use per logical payload. This includes collective decoding but excludes new cross-use encoders, a changed communication rate, and public/exported records. No comparator enlargement occurs in the reviewed substitution.

## 3. One enlarged implementation ledger

The source prescribes one total unhalved complete-process discrepancy at most epsilon/2 over calibration plus all M payloads. The ideal error then increases by at most epsilon/2, and

    17/8192+1/2 < 1

leaves sufficient additive slack. The relative coefficient `1+gamma/4` is no larger than the claimed `1+gamma`. All M uses of the finite compiled decoder, frame gates, private keys, calibration measurements and source/reset controls must be included. The local one-payload allowance is not copied M times.

The known physical receiver basis and a retained classical finite circuit description justify repeated decoder uses with fresh local ancillas; no unknown quantum programme is copied. The reference ideal product law is conditional on the entire shared calibration history and stationary source reset. The actual finite experiment need not literally be a product or Pauli channel: the one complete-process comparison transfers the bound, including arbitrary entangled payload/reference inputs.

## 4. Source bill and actual fast-completion event

The product `gamma_local epsilon_local=gamma epsilon/(8M)` introduces the constant factor eight and the stated linear-M calibration scaling. The geometric row schedule and its ONE accepted quantum bank are run once, not once per payload. The generic maximum therefore remains `O_tilde(k^4 M/(gamma epsilon))+M`, and the favorable subclass bill is `O_tilde((d+dr)M/(kappa_* gamma epsilon))+M`.

The local resource-event clarification already requires a single predecision record-channel allowance epsilon_local/1024. Substitution gives `epsilon/(4096M)`, included inside the new total epsilon/2. The local actual failure bound `<epsilon_local/256` becomes `<epsilon/(1024M)`. A direct tighter estimate from the reviewed schedule is `<3epsilon/(4096M)`, so the displayed bound has slack.

The small predecision allowance protects the actual branch/resource event, not merely the final channel after its branch record is discarded. It is charged once over the entire adaptive predecision process, not separately at every stage, and is not added again to final error. Failed fast-path records remain covered by the predetermined generic maximum.

## Independent evidence and accepted conclusion

`automatic_row_finite_m_independent_checks.py/.json/.log` were newly authored for this review without importing or executing the author's finite-M check. They passed 28,224 exact Fraction power cases, 5,376 exact shared-history mixtures, and 63 exact substitution/budget cases, including endpoints and a guard against replacing `E[f^M]` by `(Ef)^M`. Six governing version hashes and ten local-receipt bindings were verified.

There were zero RNG draws, source calls or sampled trial outcomes. These are deterministic mathematical composition checks, not a quantum learner run, source experiment, production-size optimization, compiled-circuit run or hardware result.

**Received scope:** finite-M operational substitution of the already received automatic row learner, with the same physical known-basis/source/frame/comparator assumptions and the stated single implementation ledger. This adds no generic fast-acceptance theorem, no universal k-squared cap, no unknown-basis row acquisition, no posterior/public-record guarantee, and no practical-performance claim. No unresolved correction was required.
