# Bulk-free finite sparse-entrance current certificate

Combine THERMAL_CORE_CAPACITY_LOWER.md with SPARSE_ENTRANCE_CURRENT_CERTIFICATE.md and the governing acquired basin comparison Z_M5/Z_A≤1/(1−u_r).

Assume θ≥4,1≤r,r+2≤R/3,r<L/4,u_r<1,κ>0. Let n=L²,K=floor5R²,M<K+1, and F_M be the genuine nonwinding M5 entrance states whose unique violating augmented-plus component contains at mostM plus spins. With a=49999/50000 and Γeff=8θR/a+8θ,

    j(F_M)/Cκ ≤ min{1,
      [n M²64^(M−1)/(1−u_r)]
      [κ^(-1)+2n exp(Γeff)]
      exp[−8θ(√(K+1)+√(K+1−M))+2φM]
    }.

Every factor is finite and explicitly payable. The thermal normalizer Z_A CANCELS. No extensive contour-pressure factor, bare allminus normalization, hidden conditional entrance law, or unknown asymptotic threshold remains. This is more than a technical capacity lower bound: it is an actual source-current coverage certificate for a defined family of pathological entrances.

For M=cR, its principal exponential rate, when κ^(-1) and n are polynomial in R, is

    −[16sqrt(5)θ−8θ/a−c log64]R.

For θ4,c10 the bracket is approximately69.52>0. Thus the former extensive-bulk loss no longer destroys this certificate as the polynomial torus volume increases. This does NOT prove that the complement grows rapidly.

## Executed analytic evaluations

`sparse_current_thermal_normalization.py` chooses r to make the source error bound≤.01 using the conservative rationalq5≤59/500, then checks every explicit size condition. With θ4,L8R,κ1,M10R:

    R20, r4: log bound ≈−1178.24
    R80, r5: log bound ≈−5341.93
    R1000, r6: log bound ≈−69284.40
    R10000, r7: log bound ≈−694940.52

R4 andR8 are explicitly REJECTED because the required r violates r+2≤R/3. No silent extension of the thermal-flow theorem is made. Decimal values are floating evaluations; the displayed symbolic formula supports interval evaluation. κ1 is illustrative, not a replacement for the research program's chosenκ.

## Prior-art and source check

Freshly fetched current GitHub N1722 card: modified2026-11-04, still states full polynomial mean prediction unfinished and retains the acquired core and exact source convention used here. Authorized completed source `P2_DIRECT_CURRENT_COMPLETE_RETURN.txt` states that exceptional current is bounded by raw boundary flux divided by a constructed C_flow; it explicitly says a suitable normalized capacity lower bound remains an obligation for the cited pruning. The checked current return does not contain this nested-square thermal spin-flip flow or its explicit constant bound. This is not proof of global novelty or of absence in held/unacquired material.

The strongest directly checked primary comparator is Gaudillière–Milanesi–Vares, arXiv1809.07044v2, Lemma4.5, which already proves a NORMALIZED soft-capacity lower bound with the sharp thermal barrier, asymptotically as h→0, on its finite Wulff box and tailored metastable/stable sectors. Its construction uses conditioned random block flows and standard Thomson machinery. Therefore normalized capacity control is NOT a new scientific concept, and our coarse8θ/a exponent is not an improvement on that asymptotic exponent.

The narrower reusable result here is a finite explicit bound for the actual torus/core/majority-target source, an edge-queryable thermal-carrying flow, and its bulk-free sparse-current corollary. No full residence correction, dense-entry growth theorem, sharp capacity estimator, or civilization-level breakthrough has been established.
