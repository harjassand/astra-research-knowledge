# A logarithm-free global rate-saturation theorem

This is an independent strengthening found while auditing the actual survival
function in the two-sided Duhamel proof. It uses its integrated survival/Green
mean, rather than replacing that survival function by its pointwise Markov
envelope. It is internally proved below; historical priority is not assessed.

## 1. Elementary convolution lemma

Let X,Y be independent nonnegative random variables with finite means mu_X,
mu_Y and survival functions S_X,S_Y. For T>0,

    integral_0^T S_X(u) S_Y(T-u)du <= mu_X mu_Y/T.           (G1)

Proof. Tonelli identifies the integral with E ell_T(X,Y), where

    ell_T(a,b)=Leb{u in [0,T]: u<a and T-u<b}.

For every a,b>=0,

    T ell_T(a,b) <= ab.

If a,b<=T, the interval length is (a+b-T)_+; when it is positive, the
inequality is equivalent to (T-a)(T-b)>=0. If a>=T>=b the interval length is
b, and the inequality is Tb<=ab. The symmetric case is identical. If both
a,b>=T the length is T and T^2<=ab. Taking expectations proves (G1).

The constant one is optimal for general survival functions: X=Y=T
deterministically gives equality. No second moment is used. The same lemma
holds for any nonnegative nonincreasing functions with finite integrals by
their layer-cake representations.

## 2. Receiving it into the interchange sensitivity theorem

For an interchange edge e of rate w>0, let tau_w be the two-discrepancy meeting
time from that edge under the complete current graph. The independent Green
argument gives

    mu_w=E tau_w <= M/(2w),

where M is the number of transient unordered pairs in its reachable domain.
In particular c=binomial(n,2)/2=n(n-1)/4 is a uniform choice for M/2,
independent of all other rates. The finite-state derivative and group argument
already reconstructed in PROOF_RECONSTRUCTION.md gives

    ||d[delta_sigma P_w(T)]/dw||_TV
      <= integral_0^T S_w(u)S_w(T-u)du
      <= mu_w^2/T
      <= c^2/(T w^2).                                     (G2)

Integrate (G2) from a cap K>0 to any original rate W>=K:

    TV(P_W(T)(sigma,.),P_K(T)(sigma,.))
      <= c^2/T*(1/K-1/W)
      <= c^2/(T K).                                      (G3)

There is no assumption K>=2c/T and no logarithmic factor. The dimensionless
horizon-one statement uses r_e=T w_e and a cap on r_e. Sequentially cap all
changed edges, using the same uniform c:

    sup_sigma TV(original endpoint,capped endpoint)
      <= c^2 sum_(e changed) (1/K_e-1/r_e)
      <= c^2 sum_(e changed) 1/K_e.                       (G4)

For a common cap K this is at most m_changed c^2/K. The union bound and mean
estimate are uniform under previous caps. Zero-rate edges are not capped and
incur no term. Edgeless graphs and T=0 are trivial separately.

This is stronger than the supplied N727 O(c^2 log(K/c)/K) bound. The older
bound remains correct. Its logarithm is introduced when one integrates the
two pointwise Markov envelopes; (G1) retains the stronger mean information
that the actual survival function already has.

## 3. Consequence for the explicit polynomial sampler

Section 5 improves (G4) further, removing its changed-edge count. Using that
stronger result, at horizon one choose the integer

    K = ceil(4 c^2/epsilon),     0<epsilon<=1,

for n>=2,m>=1. The cap contribution is <=epsilon/4. With capped total attempt
rate Lambda<=mK, take

    D = ceil(max(1,4 Lambda^2/epsilon)).

At each of D steps choose an edge with probability r_e^K/D, or do nothing
with the remaining probability. The same Poisson/Bernoulli argument bounds
its capped endpoint error by Lambda^2/D<=epsilon/4. Exact integer-rational
categorical sampling from fair bits, with bounded rejection whose accumulated
fallback probability is <=epsilon/2, completes the epsilon sampler.

All rational numerators/denominators have polynomial bit lengths in the
supplied binary-rational input, n,m, and log(1/epsilon). The ideal expected
uniformization attempt count is O(m n^4/epsilon); the conservative D-step
construction uses O(m^2 n^8/epsilon^3) steps. These are proved operation bounds,
not measured practical runtimes or a comparison with the strongest incumbent.
Input acquisition, full-output O(n) cost and bit arithmetic remain charged.

## 4. Optional graph-specific Green certificate

For two finite rate arrays r,q, if the two meeting means from each changed edge
are finite, combine (G1) directly with the finite-difference Duhamel theorem:

    TV(P_r(T),P_q(T))
      <= (1/T) sum_e |r_e-q_e| mu_r,e mu_q,e.             (G5)

The means are obtained from killed Green solves on reachable pair domains.
Unlike time quadrature this bound uses only mean meeting times. It may be much
looser than the survival-profile certificate, and is uninformative when a
required meeting mean is infinite. A rate may be zero at the starting edge yet
the mean can still be finite through alternate paths. Added/deleted edges
therefore are not categorically excluded; finiteness is the actual condition.

The direct infinite-boost formula also has a mean-only corollary. When the
relevant original and coarse meeting means are finite,

    TV(original,exact averaged endpoint)
      <= (1/T) sum_e a_e mu_r,e
           [h_e+sum_D beta_e(C,D) mu_coarse,{C,D}].       (G6)

This follows either by taking the limit in (G5), or from (G1) and the same
pointwise interval argument including the zero-time atom. It can be computed
with Green solves alone. Its validity does not establish that it certifies a
useful partition; that requires an actual exact receipt.

## 5. Exact normalization removes the edge count globally

There is a stronger consequence than the sum in (G4). Suppose r,q have the
same positive physical edge support. Delete its isolated vertices for the
following normalization if desired, and decompose it into connected physical
components V_j. On the pairs within component V_j, H_r is positive definite.
Let mu_r=H_r^{-1}1. The row sum of H_r at pair {x,y} is 2r_xy. By symmetry,

    sum_(e in V_j) r_e mu_r,e = binomial(|V_j|,2)/2 = c_j. (N1)

The identical normalization holds for q, regardless of its rate values.
Apply (G5) within each independent physical component and put
x_e=r_e mu_r,e, y_e=q_e mu_q,e. Then

    sum_e |r_e-q_e| mu_r,e mu_q,e
      = sum_e |1/r_e-1/q_e| x_e y_e
      <= max_e |1/r_e-1/q_e| (sum_e x_e)(sum_e y_e)
      = c_j^2 max_e |1/r_e-1/q_e|.

Consequently the full joint endpoint obeys the reciprocal-rate infinity norm
modulus

    TV(P_r(T),P_q(T))
      <= (1/T) sum_j c_j^2 max_(e in V_j)|1/r_e-1/q_e|.   (N2)

Empty component maxima are zero. Tensor coupling/TV subadditivity combines
the physical components. A looser single global constant is
c=sum_j c_j<=n(n-1)/4, giving c^2/T times the maximum reciprocal change.

For common capping q_e=min(r_e,K), positive support is preserved and every
reciprocal change is at most 1/K. Hence

    TV(original endpoint,capped endpoint)
      <= (sum_j c_j^2)/(T K)
      <= [n(n-1)/4]^2/(T K).                            (N3)

This is valid for every K>0 and has neither a logarithm nor an edge-count
factor. At dimensionless horizon one it gives the cap used in Section 3.

An alternative proof differentiates the simultaneous threshold path
r_e(u)=min(r_e,u). Its active edges all have current rate u; (N1) implies
sum_active mu_e<=c/u and therefore sum_active mu_e^2<=c^2/u^2. Integrating its
two-sided derivative bound gives (N3). The direct proof from (G5) avoids even
the piecewise differentiability bookkeeping.

This infinity-norm modulus requires common positive support. It does not
assign a finite reciprocal value to an added/deleted zero-rate edge. The
original survival-profile theorem continues to handle those changes.

## 6. Root's stopped-local extension, independently checked

After receiving (G1), the root investigator supplied the following local
extension; its algebra and assumptions were checked here independently.
For a set C containing a changed edge, let S_C,r and S_C,q be the internal
stopped meeting survivals, with means mu_C,r and mu_C,q. Let b_r,b_q bound the
total external hazard while the discrepancies remain inside C. The full
survivals obey

    S_r(t)<=S_C,r(t)+p_r,    p_r<=b_r mu_C,r,
    S_q(t)<=S_C,q(t)+p_q,    p_q<=b_q mu_C,q.

Expanding the convolution and applying (G1) to the internal survivals gives

    integral_0^T S_r(u)S_q(T-u)du
      <= mu_C,r mu_C,q/T + p_r mu_C,q+p_q mu_C,r+T p_r p_q
      <= mu_C,r mu_C,q/T (1+b_r T)(1+b_q T).            (L1)

For positive changed edge rates r_e,q_e, the local Green means are at most
c_C/r_e and c_C/q_e, c_C=|C|(|C|-1)/4. Thus arbitrary simultaneous positive
rate changes obey

    TV(P_r(T),P_q(T))
      <= sum_(e changed) c_Ce^2/T * |1/r_e-1/q_e|
             (1+b_r,e T)(1+b_q,e T).                  (L2)

The sets C_e may differ. For capping, both boundary hazards can be bounded by
their original values. No logarithm or cap-size threshold is needed. A zero
changed rate is excluded from this reciprocal form; the unspecialized (L1)
can still be useful if an alternate internal path gives a finite meeting
mean. This is a root/worker composition, not independently discovered twice
and not externally validated.
