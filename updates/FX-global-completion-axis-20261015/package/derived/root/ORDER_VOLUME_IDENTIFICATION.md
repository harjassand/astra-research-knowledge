# Chemical-order intensity does not identify volume-weighted axis writing

15 October 2026. Root derivation; internal mathematical result under an explicit measurement model. Historical originality and physical acquisition are UNKNOWN.

Let a domain have unit chemical axis n, nonnegative ordered volume dV, and order magnitude S. Define unnormalized tensors

    M = integral n n^T dV,       f = trace M,
    W = integral S^2 n n^T dV.

The requested volume-weighted tensor is Q=M/f when f>0. A normalized superlattice pole tensor is W/trace W only when its corrected/integrated intensity actually obeys this additive model. These are different targets. Coherent antiphase interference, incomplete angular/satellite integration, unknown structure factors, absorption, phase contamination and instrument normalization can invalidate the W acquisition interface. A theoretical tensor is not an acquired observable.

## Exact counterexample to the proposed simple contrast

Keep two fixed domain populations, each of volume 1/2, with axes x and y. In the first loading condition set Sx=4/5,Sy=2/5; in the second swap these magnitudes. Then

    M1=M2=diag(1/2,1/2,0),
    W1=diag(8/25,2/25,0), W2=diag(2/25,8/25,0).

Both total ordered volumes and total superlattice weights are unchanged. The normalized intensity contrast D_int=(Wxx-Wyy)/traceW changes from 3/5 to -3/5, a difference 6/5, with no axis reorientation at all. Persistence, repeatability and constant total intensity do not resolve this counterexample. An independently tracked degree of order for each orientation population would be additional information.

## Sharp identified set with an acquired order floor

Assume independently calibrated 0<s<1 and s<=S<=1 for every included domain, plus acquired total f. For a supplied W, the exact set of possible M over unrestricted unit-axis support is

    s^2 M <= W <= M,     trace M=f,       (Loewner order).

Necessity follows by integrating the positive rank-one matrices (S^2-s^2)nn^T and (1-S^2)nn^T. For sufficiency let

    P=(W-s^2 M)/(1-s^2),    R=(M-W)/(1-s^2).

Then P,R are PSD, M=P+R and W=P+s^2 R. Spectral decompositions of P and R realize the pair by finitely many domains at order magnitudes 1 and s, respectively. They need not commute. This establishes exact attainability, not only an outer bound. Feasibility requires traceW<=f<=traceW/s^2 and W PSD; those conditions also suffice by taking M proportional to W (zero case treated separately).

For known restricted axis support {n_i}, the exact finite-mixture model must instead retain M=sum m_i n_i n_i^T and W=sum w_i n_i n_i^T, with s^2 m_i<=w_i<=m_i, m_i>=0 and sum m_i=f. This is a linear program for supplied directions, coefficients and total volume. The unrestricted spectral construction may use forbidden directions, so its matrix sandwich is only an outer bound under physical support restrictions. Known per-parent weights, indivisible variants or same-domain coupling require their own additional constraints; arbitrary continuous-mixture LP weights must not be substituted for an indivisible-grain promise.

For any requested linear orientation contrast tr(T M)/f, minimization and maximization over these three-by-three LMIs give sharp bounds in this idealized model. A calibrated convex uncertainty set for W can be included as an additional variable; its acquisition and coverage must be charged separately. The small SDP is post-supplied-information computation, not a newly demonstrated instrument or improved experimental efficiency.

When W and T are diagonal in the same basis, pinching M in that basis preserves both LMIs and the target. The exact problem reduces to

    wi<=mi<=wi/s^2, sum mi=f.

A rational water-filling linear program gives the exact endpoints. For the counterexample above, s=2/5 and f=1 yield volume-axis D1 in[0,21/25] and D2 in[-21/25,0]. Thus the true contrast difference can lie anywhere in[0,42/25], including zero, despite the observed normalized difference6/5.

At s=1, M=W. If the only premise is S>0 with no acquired uniform floor, the exact set has W<=M and kerW=kerM; dropping support equality gives the closure of the JOINT feasible set when W may vary. For a fixed singular W and fixed f, the exact identified fiber is already closed: M>=W implies rangeW is contained in rangeM, and equal support adds the linear constraint rangeM subset rangeW. Thus dropping support equality is not a fixed-fiber closure operation. To prove sufficiency on equal finite-dimensional support, choose an existential positive generalized eigenvalue floor and apply the preceding construction. For example W=diag(1,0,0), f=2 has the single exact positive-order M=diag(2,0,0). M=diag(1,1,0) is a joint limit through W_epsilon=W+epsilon(M-W), not a limit at fixed W. A joint closure-boundary M with an extra direction absent from W would require zero order in that direction; it cannot be labelled an included ordered domain with S>0. If f=0, Q is undefined rather than a manufactured zero texture.

## What this changes and what it does not establish

The operation is a sharp conditional information bound and a decisive falsifier of a proposed single-tensor assay. It changes which data would support a volume-axis decision. Even an identified M change does not alone establish rotation of the same chemical axes: orientation-selective phase formation/destruction can change M. Same-domain tracking, immobilization, load transfer, chemical reset and retention remain independent physical requirements.

The most valuable next measurement acquires orientation-resolved volume and order, or a validated order floor plus absolute integrated tensor and phase fraction. The same specimen must separately distinguish reorientation from selective ordering, grain motion, phase conversion and antiphase interference. No such response has been acquired in this round. General moment-cone/semidefinite methods and spectral decomposition are classical; no historical novelty for those tools is asserted.
