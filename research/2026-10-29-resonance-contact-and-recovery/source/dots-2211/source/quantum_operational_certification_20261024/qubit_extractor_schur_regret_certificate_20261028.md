# A stationary-residual Schur certificate for native qubit-recovery regret

28 October 2026. New candidate; separate internal review required. This bounds the actual full-CPTP recovery oracle gap of a fixed physical extractor. It does not require a positive operator-block model or that the fixed extractor is exactly optimal.

## 1. Same full physical recovery SDP

Use C_j=N(sigma_j/2), H=sum_j sigma_j^T tensor C_j, a physical Pauli triple B_j, K_B=2P_B and unscaled objective J_C(B)=sum_j Tr(C_j B_j) from qubit_extractor_oracle_normal_cone_20261028.md. The actual entanglement fidelity is (1+J_C)/4, output dimension d=2g.

Set

 Y_sym=(1/2)sum_j(C_j B_j+B_j C_j),
 Q_sym=I_2 tensor Y_sym-H,
 Z=(I-P_B)Q_sym P_B,
 W=(I-P_B)Q_sym(I-P_B).

All these matrices are known from actual channel contrasts and a specified candidate; no microscopic environment is needed.

## 2. Exact zero kernel block, despite nonzero stationarity residual

Let S=sum_j[C_j,B_j], so S is anti-Hermitian. The Bell transpose identity gives

 Q_sym P_B=-(1/2)(I_2 tensor S)P_B.

Furthermore P_B(I_2 tensor S)P_B=0. In B's logical/gauge frame, compression onto P_B is the partial logical trace of S times the Bell projection; each partial trace Tr_L[C_j,sigma_j tensor I] vanishes by cyclicity in that logical factor. Hence, IDENTICALLY for every Hermitian contrast tuple,

 P_B Q_sym P_B=0,
 Q_sym = [[0,Z^dagger],[Z,W]] in P_B direct-sum P_B-perp.     (1)

This is stronger than an approximately small observed top-left block: exact physical B and exact Hermitian arithmetic enforce it. A generic floating candidate that only approximately satisfies the Pauli algebra cannot use (1) without a separate physical rounding/error treatment.

## 3. Dual repair and actual oracle regret

Suppose W>=kappa(I-P_B), kappa>0, and z>=||Z||op. Define

 lambda_star=(sqrt(kappa^2+4z^2)-kappa)/2,
 lambda_star<=z^2/kappa.

The Schur complement proves Q_sym+lambda_star I>=0: its lower block is >=(kappa+lambda_star)I and z^2=lambda_star(kappa+lambda_star). Thus Y_sym+lambda_star I_d is a valid dual witness. Since Tr Y_sym=J_C(B), weak duality gives

 0<=F_e,opt(N)-F_e(D_B N)
    <=min(1,d lambda_star/4)
    <=min(1,d z^2/(4kappa)).                                (2)

An outward rational lambda>=lambda_star can be used, or the simpler rational quadratic bound. The certificate depends on a squared stationarity residual and a verified transverse gap, not on the norm of an entire contrast-model residual. At z=0 it reduces to the exact full normal cone, including the earlier negative-contraction and gauge-only-contrast examples. A zero/negative transverse lower bound does not license division; return UNKNOWN or use a different valid dual witness.

This is an a posteriori native oracle-gap certificate, not a generator-distance or global-locality certificate. A candidate can be nearly oracle-optimal even when the oracle fidelity itself is poor. No future noise stability, complete-memory process comparison, capacity or hardware threshold follows merely from (2).

## 4. A finite ordinary holdout with actual simultaneous confidence

Here is a conservative complete statistical interface, not a claim that an existing small pilot meets it. Freeze an exact physical B using training data INDEPENDENT of a new stationary, independently restarted holdout. Fix all allocations before observing holdout outcomes. Let d=2^m for the measured output envelope.

For every input j=X,Y,Z and every NONIDENTITY m-qubit Pauli P_l, use n independent calls. On each choose an independent uniform sign s, prepare (I+s sigma_j)/2, measure P_l by actual product-Pauli readout and retain x=s times the product outcome. It lies in[-1,1] and has mean Tr(P_l C_j). Identity coefficients are exactly zero because N is TP. Each C_j is reconstructed as

 Chat_j=(1/d)sum_l chat_jl P_l.

There are M=3(d^2-1) coefficient experiments and exactly M n source calls. Hoeffding and a simultaneous union bound give, with probability>=1-beta,

 |chat_jl-c_jl|<=eta=sqrt(2 log(2M/beta)/n),
 ||Chat_j-C_j||op<=||Chat_j-C_j||F<=sqrt(d) eta=:a.          (3)

No conditional-success/postselection inference is used. Measurements include all failed outcomes. Preparation/readout imperfections, finite random bits and source/record discrepancies require their own paid allowance. This statement assumes one fixed channel across holdout settings; it cannot be silently applied to history-dependent conditional means that differ between allocated experiments.

Construct Qhat_sym, Zhat and What from the ACTUAL holdout Chat and fixed B. Exact Hermitian/Pauli relations preserve its zero top-left block. From(3),

 ||Qhat_sym-Qsym||op<=6a,
 ||Z||op<=||Zhat||op+6a,
 W>=(kappahat-6a)(I-P_B),                                  (4)

where kappahat is any certified lower bound on What restricted to P_B-perp. Numerical norm/gap residuals must be included in the outward bounds, not ignored. If kappahat>6a, set kappa_cert=kappahat-6a and z_cert=certified_upper(||Zhat||)+6a and evaluate(2). Otherwise the certificate abstains. The confidence level is beta for this frozen candidate/declared holdout; adaptive reuse of data requires a separately justified simultaneous design or fresh holdout, not a post-hoc nominal interval.

One may also use sharper valid concentration or direct estimates of the needed blocks, but those would be separate acquisition proofs. The elementary full-Pauli interface here is enough to make the claimed certificate executable at finite, potentially expensive cost.

## 5. What the formal horizon actually costs

If the fixed candidate is exactly oracle-optimal with true transverse gap kappa0, then Z=0. The simultaneous event gives ||Zhat||<=6a and kappahat>=kappa0-6a when the exact empirical gap is computed (or with its paid arithmetic slack). If a<=kappa0/24, the conservative certified denominator is >=kappa0/2 and z_cert<=12a. Equation(2) is then <=72d a^2/kappa0, that is

 regret_certificate <=144 d^2 log(2M/beta)/(kappa0 n).       (5)

This is a sufficient-horizon calculation, not knowledge of kappa0 available for free. The observed guard uses(4). With n calls PER Pauli coefficient, total source calls are M n, so this elementary certificate has substantial dimension cost. It does not turn the earlier floating small-sample pilot into a statistically certified advantage. Finite budgets may yield only UNKNOWN, even when the nominal model candidate is good.

## 6. Prior science and exact scope

Recovery optimization by SDP and constructing dual feasible points to certify near-optimality are established techniques. Fletcher, Shor and Win, “Structured Near-Optimal Channel-Adapted Quantum Error Correction,” arXiv:0708.3658v2, SectionV (especially Eqs28–29 and the dual-repair discussion), explicitly develops this approach: https://arxiv.org/html/0708.3658 . The present source specializes a block Schur repair to the exact Bell-times-gauge kernel and supplies the stated ordinary-holdout uncertainty accounting. No historical novelty is claimed.

The same equally informed conventional method can use this witness. The possible benefit is a tighter, targeted certificate for a physically specified extractor when a full model-fit residual was unnecessarily large. Acquisition, model stability and actual controls remain obligations. Numerical fixtures and proof checks below do not replace those interfaces.
