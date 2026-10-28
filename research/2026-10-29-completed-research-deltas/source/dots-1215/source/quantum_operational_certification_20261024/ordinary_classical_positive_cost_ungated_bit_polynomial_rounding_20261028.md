# Bit-polynomial positive-cost rounding on a binary decoder cube

28 October 2026. Separate author construction, with an independent analytic check by the original gated-lemma reviewer before this manuscript was frozen. A bound receipt is still required. This strengthens the received gated lemma without editing it. It is a classical optimization subroutine on a PRODUCT binary action set, not a full-CPTP decoder rounding theorem or a new physical acquisition rate.

## 1. Input and output contract

Let the known rational data be

    A >= 0, N(z)=(1,z)^T A(1,z)=||a_0+sum_i a_i z_i||^2,
    u(z)=m+sum_i w_i z_i, m>0, w_i>=0, z in {0,1}^n.

The Gram vectors are used only in the proof; their computation is unnecessary. Supply a rational a>=max(1,||A||op), a rational feasible basic moment matrix

    M>=0, M_00=1, M_0i=M_ii=p_i in [0,1],
    d=m+sum_i w_i p_i, S=Tr(A M), F=S/d,

and 0<beta<1. The decoder action is returned as an EXACT binary vector. For F>=1, there is a capped randomized algorithm, polynomial in n, the rational input bit length, and log(1/beta), returning

    N(z)/u(z) >= F/[8192 max(1,L)]                         (1)

except with probability beta, where L is the number of retained nonempty dyadic groups defined below. In particular L=O(log(2+an/m)). For F<1, returning zero incurs less than an additive-one relaxation loss. This is a bit-polynomial rather than merely numerical-magnitude-polynomial trial guarantee.

Optimizing the basic moment relaxation is optional. Its standard Charnes-Cooper SDP and a finite strict-feasibility witness are given in the received predecessor. The theorem here rounds ANY supplied feasible rational M, so an approximate optimization tolerance can be debited separately rather than assumed away.

## 2. Tail reduction, inherited with explicit constants

Let R_0=A_00/m and delta=min(1/2,m/(64an)). Discard indices with p_i<delta and group the remaining indices by p_i in (p_I/2,p_I], p_I a distinct dyadic power in (0,1]. These groups are determined by rational bit positions; no scan through a numerically long interval is used. Write S_I=Tr(A_II M_I) and S_keep for the retained principal block contribution.

PSD Cauchy and Tr(A_tail M_tail)<=a sum_tail p_i<=m/64 imply

    S <= 2 A_00 + 4 S_keep + m/16.                        (2)

Thus, if F>=1 and R_0<F/4,

    S_keep >= F d/16,   S_keep <= L sum_I S_I.             (3)

If L=0, (2) contradicts R_0<F/4, so the baseline handles that case. A preliminary baseline test can therefore return zero whenever R_0>=F/4.

## 3. Optimize an UNGATED correlation round within each group

For every retained group I with Tr A_II>0, solve the ordinary correlation SDP

    T_I = max { Tr(A_II Y): Y>=0, diag Y=1 }.              (4)

Its identity point is strictly feasible in its affine hull, T_I>=Tr A_II, and its feasible set is bounded. Obtain a rational feasible Y_I with certified value t_I=Tr(A_II Y_I)>=T_I/2. For example, an additive objective debit Tr A_II/4, including inward feasibility rounding, gives this guarantee with slack. The required tolerance has polynomial bit length, including when Tr A_II is small. Zero-trace PSD blocks vanish and are skipped.

The matrix M_I/p_I+diag(1-p_i/p_I) is feasible for (4). Therefore

    p_I t_I >= S_I/2.                                    (5)

Let c_I=m+(1/2)sum_(i in I) w_i. Distinct dyadic scales satisfy sum_I p_I<=2, while p_I/2<=p_i. Consequently

    sum_I p_I c_I <= 2m+sum_keep w_i p_i <= 2d.

Choose a group maximizing the known rational ratio t_I/c_I. Equations (3)-(5) give

    t_I/c_I >= (sum_J p_J t_J)/(sum_J p_J c_J)
              >= S_keep/(4Ld) >= F/(64L).                (6)

This is the essential cost calculation. It is legitimate to remove the rare Bernoulli gate because the group is selected by its OPTIMIZED homogeneous quadratic value divided by its actual ungated expected cost. Merely dropping the gate in the predecessor's selected group would not prove (6).

## 4. Feasible Gaussian signs and a dimension-only success probability

For the chosen group draw g~N(0,Y_I), put s_i=sign(g_i), and set z_i=(1+s_i)/2 on I and zero elsewhere. Every outcome is binary. Gaussian symmetry gives E u(z)=c_I. The exact arcsine identity and its positive Schur-power series give

    E ss^T=(2/pi)arcsin(Y_I)>=(2/pi)Y_I,
    E ||sum_(i in I) a_i z_i||^2 >= t_I/(2pi).            (7)

No spectral lower bound on Y_I is needed. The arcsine/PSD-Grothendieck ingredient is established; it is reproduced here to identify the exact guarantee being used.

If R_0>=t_I/(64c_I), return the baseline. Otherwise A_00<t_I/64. The pointwise offset inequality

    N(z)+A_00 >= (1/2)||sum_(i in I)a_i z_i||^2

and pi<4 yield E N(z)>=3t_I/64. Put r=t_I/(128c_I). Then

    E[N(z)-r u(z)] >= 5t_I/128.                          (8)

Also T_I>=Tr A_II and t_I>=T_I/2 give the POINTWISE bound

    ||sum_(i in I)a_i z_i||^2 <= n Tr A_II <= 2n t_I,
    N(z) <= 2A_00+4n t_I <= (4n+1/32)t_I.                (9)

On the event N(z)<=r u(z), the margin in (8) is nonpositive. Its positive part is bounded by (9), regardless of how large a particular cost is. Hence

    Pr[N(z)>r u(z)] >= (5/128)/(4n+1/32) >= 1/(128n).     (10)

This is the improvement over rare gating: the success probability does not contain m, min p_i, ||A||, or any reciprocal numerical range. With total-variation sampling error at most 1/(256n), it remains at least 1/(256n). At most

    ceil(256n log(1/beta))                               (11)

independent finite-precision attempts suffice. Evaluate every realized rational ratio exactly, include the baseline, and return the largest. The baseline case gives at least F/(4096L); otherwise (6) and r give (1). Failed histories still return an exactly feasible action with its actually computed cost.

## 5. Finite sampling and bit complexity

A singular feasible correlation matrix presents no hidden eigenvalue-floor assumption. Approximate its positive square root in Frobenius norm by a rational factor, couple the resulting Gaussian vector to the exact one, and use the variance-one marginal anti-concentration bound. Concretely, if the factor error is at most eta, then E||g-g_tilde||_2^2<=eta^2. For any threshold h>0,

    Pr[any sign differs] <= Pr[||g-g_tilde||_2>h]
                          +sum_i Pr[|g_i|<=h]
                        <= eta^2/h^2 + n sqrt(2/pi) h.

Choose h and eta inverse-polynomial in n to make this at most 1/(512n). Bounded rational approximations to independent standard Gaussian coordinates can be coupled similarly: truncate at a radius polynomial in log(n), discretize to inverse-polynomial mesh, and sample cell probabilities to an inverse-polynomial aggregate variation tolerance. Every coordinate of the transformed approximation is a finite rational number; signs and the returned policy are exact. Allocate the other 1/(512n) to this finite Gaussian approximation. Equivalently one may use a certified finite Gaussian sampler with that joint coupling bound. The sample space and bit precision are polynomial-size descriptions, not a claim that a continuous random variable is physically exact.

The two SDPs used here are ordinary bounded rational SDPs with explicit relative-interior points, and all requested accuracies are specified by rational numbers of polynomial bit length. Standard certified polynomial-time SDP optimization followed by inward mixing/rounding supplies the stated feasible values; diagonal-one equalities are kept exact. This note supplies the mathematical oracle contract and finite precision ledger, not an executable SDP solver. The diagnostics do not constitute a production optimization or random-bit compiler.

The number of groups is at most n and also at most 1+ceil(log_2(1/delta)). Thus even exponentially large/small rational coefficient magnitudes cost only their bit lengths in grouping, SDP precision, and Gaussian sampling. The returned ratio is compared exactly, so very small absolute objectives do not create a hidden statistical test. No source calls or unknown-state operations occur in this subroutine.

## 6. Boundary and comparison

The separately saved parallel-gate companion gives a basic-moment-SDP integrality gap Omega(log coefficient range). Its geometric example therefore also limits removal of the logarithmic relaxation factor here. That gap violates valid RLT pairwise inequalities and does not apply to stronger relaxations; it is not an optimization-hardness or physical-source lower bound.

Full CPTP Choi coordinates do not form a product cube. Grouping and independently setting them to signs generally violates positivity or the input partial trace. The received dual representation u(C)=m+Tr(WD), W>=0, does not supply such a product parametrization. No generic source-rate improvement follows from this note alone. The equally informed conventional learner can use the identical classical algorithm. The received generic k^6/(gamma epsilon) polynomial construction is unchanged.

Governing local sources: `ordinary_classical_positive_cost_gated_rounding_20261028.md` (d30bebfe86d4abc4154482d9b3a435de247c09e9dbc2ecf164dcabafbfa99e01), its independent receipt, and `ordinary_classical_positive_cost_gated_rounding_log_improvement_20261028.md` (00d5eec77b9660ebf91e8ab21554c5014ddc22c5f5e5de293829c19aac07869c). This manuscript makes no historical-priority claim.
