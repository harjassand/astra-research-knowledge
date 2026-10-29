# Native excursion acquisition, and the information it cannot supply cheaply

29 October 2026, Brisbane. Complement to the root's predictive-information construction. Reversible potential theory, milestoning and forest formulas are conventional ingredients. The contribution here is the native second-moment acquisition identity, its confidence/cost obligations, and a precise lower model for the information discarded by a first-moment boundary record.

## 1. Source and physical access

Q is a finite irreducible reversible CTMC generator, π its stationary probability, and L=diag(π)(−Q). B is a known observable port set and I its complement. The source evolves natively between observations. The experiment can prepare a specified port and observe port identities, interior/port membership and elapsed time nonintrusively. These are supplied access/source warranties; samples do not establish them.

A trial from port i waits for the first actual state-changing jump, with holding time X_i and rate λ_i=−Q_ii. If that jump reaches B, set σ_i=0. Otherwise continue without restarting until the first return to B. Record endpoint J_i and interior duration σ_i. Returning to the same port is permitted. Full trial time is X_i+σ_i. Define P_ij=Pr_i(J_i=j), d_i=E X_i=1/λ_i, and ρ_i=π_iλ_i. Reversibility gives ρ_iP_ij=ρ_jP_ji. The endpoint chain is irreducible, with stationary vector s=ρ/Z, Z=Σ_Bρ_i. This acquisition does not need an interior equilibrium sampler.

## 2. The decisive second-moment identity

The root's Schur quantities are

    S=L_BB−L_BI L_II^−1 L_IB,
    b=π_B−L_BI L_II^−1 π_I,
    c=π_I^T L_II^−1 π_I.

For I empty hidden terms vanish. Otherwise let h=L_II^−1π_I be the mean time to B from I. The second hitting-time moment is g=2L_II^−1diag(π_I)h. The departure law gives

    ρ_i Eσ_i=−(L_BI h)_i,
    ρ_i Eσ_i²=−(L_BI g)_i.

Using L_II1_I=−L_IB1_B and symmetry,

    Σ_iρ_iEσ_i²
      =−1_B^T L_BI [2L_II^−1diag(π_I)h]
      =2π_I^Th=2c.

Thus endpoint, duration and squared-duration observations acquire

    S_ij=−ρ_iP_ij (i≠j),
    b_i=π_i+ρ_iEσ_i,
    c=(1/2)Σ_iρ_iEσ_i².                         (1)

S has zero row sums: define its diagonal from the off-diagonal conductances. An independently noisy diagonal can lose Laplacian structure. The second moment in (1) is of the interior duration after departure. Using total holding-plus-excursion time would require subtracting its holding and cross terms.

Dividing everything by Z produces a scale-free record:

    w_i=s_i d_i,
    Sbar=diag(s)(I−P),
    bbar_i=s_i(d_i+Eσ_i),
    cbar=(1/2)Σ_i s_iEσ_i²,
    W=Σ_i bbar_i=1/Z.                            (2)

The equality for W follows from Σ_i b_i=1. For nonempty A⊆B, R=B\A, root's block-elimination identity becomes

    T_A=[cbar+bbar_R^T(Sbar_R)^−1bbar_R]/D_A,
    D_A=Σ_{i∈R}w_i+Σ_{i∈B}s_iEσ_i.              (3)

This is the mean from true equilibrium conditioned outside A. For R empty the quadratic term is zero. Physical preparation of that initial ensemble remains distinct from predicting its mathematical mean. This finite record does not certify arbitrary starting laws, killing inside I, or complete first-passage distributions.

## 3. Finite confidence and complete time cost

Run n_i fresh independent port-i trials. Pay every full departure wait X_i. Cap the interior evolution at H_i and record min(σ_i,H_i), its square, and endpoint-by-H indicators. A still-interior trial is censored, not a completed return, and is charged through H_i.

If the source class supplies Pr_i(σ_i>t)≤C_i exp(−κ_i t), then missing probability, first and second moments are at most

    e_i=C_i exp(−κ_i H_i),
    u_i=e_i/κ_i,
    v_i=2e_i(H_i/κ_i+1/κ_i²).                    (4)

These follow by tail integration. With ℓ>0, Hoeffding statistical radii are sqrt(ℓ/(2n_i)), H_i sqrt(ℓ/(2n_i)), and H_i² sqrt(ℓ/(2n_i)), respectively. Add (4) to their upper endpoints. Simultaneous union bounds yield one event reusable for all later queries. If a pilot chooses H_i, use a fresh main batch. The source tail warranty must apply to the chosen horizon.

Square-duration Hoeffding can be costly. Ordinary Bernstein can instead use Eσ_i⁴≤24C_i/κ_i⁴ and Eσ_i²≤2C_i/κ_i² for variance bounds. It retains a bounded-variable linear term and the tail allowance. Samples do not supply C_i, κ_i, or timing precision. Measurement error must be added separately; the square error grows with H_i.

Departure holds have an exponential family supplied by the CTMC contract. For 0<a≤1,

    Pr(|mean(X_i)/d_i−1|≥a)≤2exp(−n_i a²/4).

The upper exponent uses a−log(1+a)≥a²/4; the lower uses −a−log(1−a)≥a²/2. Thus d_i lies in [mean(X_i)/(1+a),mean(X_i)/(1−a)]. Exact gamma intervals are stronger conventional alternatives. These complete waits cost n_i d_i in expectation, not under a hard elapsed-time deadline. Capped holds require their own censoring likelihood.

Expected native evolution time is Σ_i n_i[d_i+E min(σ_i,H_i)], plus pilot time. At most Σ_i n_i specified port preparations are used by this fresh-reset protocol. Membership monitoring, endpoint discrimination, timestamp precision, preparation/control latency, and storage are separate costs. Reusing a known terminal port may save preparations, but count it from actual endpoints. There is no physical execution claim here.

## 4. Propagating statistical information soundly

An empirical row-stochastic P_hat need not be reversible. If it has the true off-diagonal support and all positive entries are within factor Kp of P, then its stationary vector s_hat satisfies componentwise factor Ks=Kp^{2(|B|−1)} relative to s. The positive Markov-tree numerator has |B|−1 factors, and normalization adds at most the same logarithmic error. This safe bound is not the sharpest entrywise perturbation result.

Symmetrize proposed conductances as

    chat_ij=(s_hat_iP_hat_ij+s_hat_jP_hat_ji)/2.

Each lies within Ks Kp of the true s_iP_ij. Their graph Laplacian therefore approximates Sbar in quadratic-form order. This does not falsely treat the empirical P as reversible.

More generally obtain nonnegative boxes for w,bbar,cbar and every undirected conductance. Lower/upper edge Laplacians Slo,Sup obey Slo≼Sbar≼Sup. Compute Dlo,Dup from the nonnegative expression (3), avoiding cancellation of independent W and target-mass intervals. Then

    Tlo=[clo+blo_R^T(Sup_R)^−1blo_R]/Dup,
    Tup=[cup+bup_R^T(Slo_R)^−1bup_R]/Dlo.         (5)

Inverse Loewner order controls S. Inverses of grounded connected graph Laplacians are entrywise nonnegative, so their quadratic forms are coordinatewise increasing on nonnegative vectors; this controls b boxes. If Slo_R is singular or Dlo=0, this consumer releases no finite upper certificate. That failure concerns the acquired information/certificate, not necessarily the true lifetime.

If d,Eσ,Eσ² have factors Kd,K1,K2, a simpler sufficient factor is

    Kb=Ks max(Kd,K1), KD=Kb,
    Kc=Ks K2, KE=Ks Kp,
    Ktask=KD max(Kc,KE Kb²).

Then T_hat/T∈[Ktask^−1,Ktask]. Handle exact zero hidden contributions with additive boxes, not an unjustified relative estimate. Learning every positive endpoint probability relatively costs order 1/p_min trials per row by elementary multinomial/Chernoff methods. A count of |B|² coefficients is not that information cost. Unknown support cannot be certified as zero from no observed events. Spectral sparsification may ignore redundant small edges, but learning a valid importance distribution from an unknown source is an additional obligation.

## 5. Exact missing-information model and native-time lower bound

Take states 0,1,h with uniform π and rates q01=q10=1, q0h=qh0=ε, 0<ε≤1/8. For B={0,1}, I={h},

    S=(1/3)[[1,−1],[−1,1]], b=(2/3,1/3),
    π_B=(1/3,1/3), c=1/(3ε).

All of S,b,π_B are independent of ε, but for A={1},

    E_{π(.|A^c)}τ_A=2+1/(2ε).                   (6)

The mean from boundary 0 is exactly 2 for every ε. Equilibrium-conditioned starting mass includes residual trap residence. Raw endpoint P and departure clocks do vary with ε: only the compressed S,b record is identical.

At port 0, λ0=1+ε, hidden entry has probability ε/(1+ε), and conditional hidden time is Exp(ε). Hence ρ0Eσ0=1/3 while (ρ0/2)Eσ0²=1/(3ε). Rare entry and long residence cancel in the first moment but not the second.

Compare Q_ε and Q_{2ε}. Even an algorithm observing the full state path and resetting to any of the three states adaptively satisfies

    KL(P_ε || P_{2ε})
      ≤ ε(1−log2) E_ε[total native time].         (7)

Only 0↔h rates differ. Their instantaneous path relative entropy is ε log(1/2)−ε+2ε=ε(1−log2) at 0 or h, and zero at 1. Source-independent resets add no conditional information. Standard stopped likelihood integration gives (7) whenever expected native time is finite.

Errors at most 1/3 for both hypotheses require KL≥2/9 by Pinsker, hence

    E_ε[native time]≥2/[9ε(1−log2)].             (8)

The means in (6) for ε and 2ε differ by at least factor 5/3 when ε≤1/16; both sources are in the stated class. A procedure returning an interval with factor strictly below 5/3 and coverage at least 2/3 under each source distinguishes the pair and inherits (8). This is a coverage-and-release obligation: a procedure allowed to abstain always has no such cost lower bound. This is a specified-interface information lower bound, not a limit with supplied ε or a new legal operation. It shows why no finite record alone supplies a uniform upper bound on the missing excursion moment over an unrestricted finite-state class.

## 6. Strong conventional comparator: large means can be easy

Let Q,Q_hat be any finite generators with the same off-diagonal support and K-relative positive rates. For any target A put n=|A^c|. Positive directed-forest formulas give

    K^{−(2n−1)}(−Q_Ac)^−1_ij
       ≤(−Qhat_Ac)^−1_ij
       ≤K^{2n−1}(−Q_Ac)^−1_ij.                  (9)

The Green denominator is a positive homogeneous polynomial of degree n in rates; its numerator has degree n−1. Uniformization transfers the discrete-time forest identity to rates. Summing against fixed nonnegative initial/reward vectors preserves (9). Therefore all target-set means have a simultaneous relative certificate with no gap or rarity factor. Use a conventional killed solve for computation; enumerating forests is only a proof device.

A biased nearest-neighbour chain can have an exponentially large end-to-end mean while every local transition probability is moderate. With reset access to each known state, ordinary local estimation and this comparator are polynomial in the state count and requested accuracy. Conversely a single small unknown local rate may force inverse-rate observation time as (8) shows. A boundary representation must reduce actually acquired state/information complexity while preserving the task; a large printed time alone establishes no advantage.

### Executed local-rate comparator

`acquire_local_chain_comparator.py` generated and streamed 138,412,032 elementary binary outcomes, 2^22 at each of 33 individually accessible states on a reflected nearest-neighbour path. These are actual software Bernoulli outcomes, not aggregate Binomial draws. The source has a supplied marked unit-attempt clock, known state graph, exact port/state resets, and unknown right probabilities lying in [1/4,3/4]. Its dyadic private parameters enter only generation and checks after the acquired counts and consumer are frozen.

Exact radius 1/800 and an elementary rational lower bound on exp(13) establish a common failure probability below 1/4096. The record supports (9) for every target set, every outside initial state and each fixed nonnegative reward, with interval factor 1.8733885518342708 (display). For the selected crossing 0→32, the stronger equally informed positive birth-death recurrence gives factor 1.4429579304955222 (display). The exact rational endpoints and factors are stored, so these decimals are not the authoritative bounds.

The private true selected mean is approximately 624,141,593,816,165.9 unit-clock time units. The task is nevertheless handled by ordinary local acquisition and an O(N) positive recurrence on the same record. The protocol charges all 138,412,032 fresh state preparations and the same number of expected native unit-clock waits. Actual software acquisition took about 0.4931 seconds; this is not a physical-time claim. No hardware operation or equilibrium preparation occurred. This is a counterexample to inferring difficulty from mean magnitude, not a new superior rare-event method or a demonstration that a compact accessible macrostate graph exists for a general many-body source.

The first post-acquisition diagnostic attempted to reconstruct Fraction values from two string arguments and raised TypeError. The consumer parse was corrected to convert those arguments to integers; the already frozen count record was replayed without any redraw. No mathematical assertion failed and the observation bill is not doubled by that replay.

`check_excursion_information.py` separately verifies the three-state identities at six rational epsilon values through 2^-64, including both scale-free and unscaled records, and checks every killed-inverse entry for all 14 nontrivial target subsets in four exact four-state fixtures: 256 entry checks. These are supplied-source rational controls with zero observations, distinct from the acquired 33-state experiment.

## Sources and scope

Primary antecedents inspected:

- Aristoff, Bello-Rivas, Elber, *A Mathematical Framework for Exact Milestoning* (2016), https://pmc.ncbi.nlm.nih.gov/articles/PMC4879838/ . Sections 2–5 retain the point on a milestone, its semi-Markov kernel and correct stationary flux. Endpoint/time reconstruction alone is established.
- Lin, Lu, Vanden-Eijnden, *A Mathematical Theory of Optimal Milestoning* (2016/2017), https://arxiv.org/abs/1609.02511 . Optimal milestones give exact means; their construction and starting laws have costs.
- Pitman and Tang, *Tree formulas, mean first passage times and Kemeny's constant of a Markov chain*, Theorem 1.2, equations (1.5)–(1.8), https://www.columbia.edu/~wt2319/Tree.pdf . Precise positive-forest premise for (9).
- Thiede, Van Koten, Weare, *Sharp Entrywise Perturbation Bounds for Markov Chains* (2015), https://doi.org/10.1137/140987900 . Stronger stationary perturbation comparators than generic gap bounds.

Astra search found RENEWAL_ACQUISITION.md and RENEWAL_SCHUR_FORM_REVIEW.md at input version 9301bf5171d4110151e38e5ddebeb1212f593a1c14f7751e019e9a8264a3b8ef, revision d6672151ce8e86d4af3e74b3b880abcdc82ae304. Their full local originals were read. Their source SHA256 values are 2cf593d72850e97abcd6e5cd36e3a1342679e646153596d81f786ac3153f8bfd and b70c109e972d9bc74fb7856d051b783c9701e1607ac313844989ff80383110e8. They already separate native return acquisition, censoring, actual resets, physical time and precision. This work builds on those accepted scopes rather than routinely re-auditing them.
