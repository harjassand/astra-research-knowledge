# Independent review: directed mean-record realizability and state cost

29 October 2026. Ordinary proofs and exact controls for the root's oriented sufficient mean record. No statistical experiment or raw-data re-audit is performed. Here a positive CTMC means nonnegative transition rates and positive stationary weights; absent edges may have zero rate. Clocks are free design variables. An oriented record is not claimed minimal for scalar mean observations: time reversal can leave those observations unchanged.

## 1. Characterization

Let S be an irreducible m-port directed Laplacian with zero row and column sums, and F_ij=−S_ij>=0 for i≠j. Let w_B>0, v_R=b_R−w_B>=0, v_L=b_L−w_B>=0, with common total V>0. Let c>0. Let T be the transportation set of M>=0 with row sums v_R and column sums v_L, allowing every diagonal and only off-diagonals where F_ij>0. Define

    J*=min_{M in T} sum_{i!=j} M_ij²/F_ij.        (1)

The root's claim is sound: a finite irreducible CTMC realizes exactly (S,b_R,b_L,c,w_B) if and only if T is nonempty and 2c>J*. The strict inequality matters. Equality is a zero-variance limit, not a positive-duration finite CTMC realization.

## 2. Necessity and orientation

For an actual source, use positive invariant weights w and L=−diag(w)Q. Put C=L_II for hidden interior I and ρ_i=w_iλ_i. A trial departs port i and evolves natively to the next port J. Let σ be interior time after departure, zero for a direct port jump. Define

    Fall_ij=ρ_i Pr_i(J=j),
    M_ij=ρ_i E_i[σ 1_{J=j}].

The full flow Fall is balanced; its off-diagonals are F. Its diagonal return flows are not determined by S. The first excursion-moment matrix satisfies

    M=L_BI C^−1 diag(w_I) C^−1 L_IB.

It is entrywise nonnegative. Using C1=−L_IB1 and 1^TC=−1^TL_BI gives row(M)=v_R and column(M)=v_L. The second excursion moment gives

    sum_ij Fall_ij E_i[σ²|J=j]=2w_I^TC^−1w_I=2c. (2)

This identifies an acquisition distinction: in a nonreversible source, marginal duration means acquire v_R, whereas v_L generally requires duration jointly resolved by endpoint.

Every positive-M channel has a positive-duration component. A finite CTMC interior hold has nonzero conditional duration variance, even after conditioning on the terminal port; direct jumps only add a zero atom. Since V>0, conditional Jensen is strict for at least one channel. Therefore

    2c > sum_{ij:Fall_ij>0} M_ij²/Fall_ij
       >= sum_{i!=j} M_ij²/F_ij >= J*.

Zero flow implies zero M and contributes no undefined term. Thus the transport support and strict scalar conditions are necessary.

## 3. Sufficiency and exact second-moment calibration

T is compact and the objective is continuous, so a minimizer exists. Its off-diagonal entries are unique by strict convexity; diagonal entries then follow from the row sums. Set Vdiag=sum_i M_ii.

If Vdiag>0, choose 0<delta<2c−J*, set mu_diag=delta/Vdiag, and choose Fall_ii=M_ii/mu_diag for every positive diagonal entry. If Vdiag=0 set delta=0 and add no self channels. Keep all off-diagonal Fall=F. The full flow remains balanced. Then

    D=sum_{ij:M_ij>0}M_ij²/Fall_ij=J*+delta,
    0<D<2c.

Choose k=ceil[D/(2c−D)]>=1. Replace each positive-M channel by k serial exponential stages with total mean mu_ij=M_ij/Fall_ij. A channel with zero M remains a direct edge. Each hidden stage has invariant weight equal to its through-flow times its mean holding time. Thus the channel's total hidden weight is M_ij, and the record's S,w_B,v_R,v_L are exact. Its initial residence scalar is

    c0=(1/2)(1+1/k)D<=c.                        (3)

If needed, raise the second moment of one positive-M channel without changing its mean or flow. For channel mean mu and desired second moment q>=(1+1/k)mu²:

- If k>1 and q<=2mu², mix an Erlang-k and an exponential, both of mean mu. The exponential branch probability is [q−(1+1/k)mu²]/[(1−1/k)mu²].
- If q>=2mu², mix exponentials of means a=mu/2 and d=q/mu−mu, with probability p=(d−mu)/(d−a) on the first. At equality p=0 and the unused branch is omitted. Direct substitution gives mean mu and second moment q.

Use q equal to the channel's original second moment plus 2(c−c0)/Fall_ij. This raises the total scalar to exactly c. At most one extra phase beyond the k-per-channel allocation is needed. All used rates and state weights are finite and positive. Irreducibility of S makes the full channel graph irreducible. Rational data with a rational optimizer give rational calibration; no square roots are needed. The channel construction has a separate companion review; this note checks its feasibility and variance calibration.

## 4. Record-level lower bound on hidden state count

If ANY finite realization uses k hidden states, then

    2c >= (1+1/k)J*,
    k >= J*/(2c−J*) when J*>0.                  (4)

Here is a self-contained proof of the phase-type variance ingredient. Consider any proper transient CTMC with at most k states and hitting time τ of its absorbing state. Let h_i=E_iτ and h_abs=0. The stopped Dynkin martingale t+h(X_t) gives

    Var_i(τ)=E_i sum_{jumps before absorption}(Δh)².

Order the distinct positive h levels, with 0 first. Every realized path from h_i to 0 must cross each intervening level gap at least once. A jump crossing several gaps has squared increment at least the sum of the squared gaps it crosses. Consequently the pathwise sum of squared increments is at least the sum of squared gaps below h_i. There are at most k such gaps, so Cauchy–Schwarz gives at least h_i²/k. Thus Var_iτ>=h_i²/k. Mixing initial states preserves Varτ>=(Eτ)²/k by the variance decomposition. Finite proper chains have finite second moments, which justify the stopped martingale identity.

Condition an excursion on a given exit port. Its positive-duration component is a Doob-transformed absorption time on at most the original k hidden states: restrict to states having positive probability of that exit and transform by that exit harmonic function. A direct port jump supplies an optional atom at zero. If p is the positive-duration probability and its conditional mean is mu, then

    Eσ² >= p(1+1/k)mu²
          >= (1+1/k)(Eσ)².

Multiply by Fall_ij, sum channels, and minimize their off-diagonal transport cost to obtain (4). This uses no reversibility. The bound is sharp: one directed excursion channel may be Erlang-k, its reverse trace flow direct, and there may be no diagonal time mass. Then 2c=(1+1/k)J* exactly.

## 5. Approximation with state count independent of exact slack

Assume the strict criterion and fix 0<eta<=1. If Vdiag>0 choose delta=eta*c/2; otherwise use zero. Set k=ceil(4/eta), form c0 from (3), and raise it to c'=max(c,c0) if needed. Although D may now exceed 2c,

    D<=J*+eta*c/2<2c(1+eta/4),
    c0<c(1+eta/4)^2<=(1+eta)c.

Hence c<=c'<=(1+eta)c with all other record entries exact. At most m² channels have positive M, giving at most m+k*m²+1 states. This is a state-count bound, not a bound on rates, bit lengths or acquisition cost. Tiny positive M_ij can still require large rates kF_ij/M_ij. Original holding rates and complete survival laws are not preserved.

For each allowed mean context whose module contribution has form (c+B)/D0 with B>=0 and unchanged D0>0, the new mean is between the original and (1+eta) times the original. Grounded M-matrix inverses make the other bilinear contributions nonnegative in the stated passive population/mean contexts. No claim is made for signed rewards, hidden interventions, arbitrary initial laws or full time-dependent responses.

## 6. Balanced hidden load does not require a reversible core

If v_R=v_L, take M diagonal and J*=0. Attach one leaf of invariant weight v_i to each positive-v_i port, with balanced flow gamma*v_i where gamma=V/c. The leaf exit rate is gamma, its residence contribution is v_i/gamma, and their sum is c. The directed Eulerian core S remains unchanged. This needs at most 2m states even when S is nonreciprocal. Balanced hidden load is therefore sufficient; requiring the whole source to be reversible would be stronger.

## 7. Exact controls and scope

The adjacent checker verifies rational KKT certificates, a transport-support obstruction, exact slack and approximate-size calibrations, and a full nine-state directed realization:

- Two ports: F01=F10=1, v_R=(2,1), v_L=(1,2), M=[[1,1],[0,1]], J*=1. For c=1, delta=1/4 and k=2 give c0=15/16. A rational phase mixture raises c to one.
- Split three-port optimum: symmetric F01=F12=1,F02=1/10; v_R=(2,1,1), v_L=(1,1,2). The optimizer has M01=M12=5/6,M02=1/6 and diagonal (1,1/6,1). J*=5/3. Row potentials (10/3,5/3,0) with opposite column potentials certify global optimality.
- Impossible support: directed cycle 0→1→2→0 with v_R=(1,0,0),v_L=(0,0,1). Row 0 can reach only columns 0,1, whose required total is zero. Strong connectivity of S alone does not ensure transport feasibility.
- Balanced loads yield a zero-cost diagonal certificate. Approximation arithmetic is checked at rational eta values and exact slacks down to 2^-64. Erlang channels attain the state lower bound in the unbalanced two-port family.

For each KKT certificate, the allowed-position gradient is 2M_ij/F_ij off diagonal and zero on diagonal. Subtract row and column potentials; the remaining values are nonnegative and vanish on positive M entries. Equal marginal constraints cancel the potentials in the objective difference, leaving a sum of nonnegative squares and nonnegative slacks. Thus no floating optimizer status is used as a premise.

The phase-type variance inequality is classical: David Aldous and Larry Shepp, *The least variable phase type distribution is Erlang*, Stochastic Models 3(3), 467–473 (1987), DOI 10.1080/15326348708807067. Primary author-institution copy: https://escholarship.org/content/qt7w51x4rb/qt7w51x4rb.pdf ; metadata/abstract: https://escholarship.org/uc/item/7w51x4rb . The ordinary martingale argument above supplies the exact ingredient used here; the new record-level use is the coupling to J* and the directed transport constraints. The scan's text extraction exposed only its cover, so it is not counted as a line-by-line review of the original proof.

Transportation programming, phase-type moment matching and Markov comparison arguments are known ingredients. No historical-priority or external-acceptance claim is established here. The review establishes the stated oriented-record characterization and resource bounds at their actual scope.
