# Label-observed acquisition of collective quantum-flag recovery

28 October2026. New scoped composition and executable simulation; independent review pending. This extends the collective Pauli oracle bridge to genuinely noncommuting quantum side information and removes a tree promise under an explicit error-label observation interface. It is not a new state-discrimination or Pauli-learning algorithm, and does not solve arbitrary unknown noise.

## 1. Complete physical source, feature promise and resources

For n logical/data qubits let d=2^n and let P_x be the n-qubit Pauli strings, or the bit-flip subgroup X^x. The fixed stationary source is

    N(rho)=sum_x p_x P_x rho P_x tensor tau_(f(x)).

Here f is a known feature taking K values, tau_a are unknown density matrices on an accessible gauge/flag register G, and p is ANY distribution, including arbitrary spatial correlations and zero probabilities. The flag states need not commute and may have rank one. The error mixture is classical in x; arbitrary coherent superpositions of error labels and arbitrary input-dependent flag states are not covered. Fresh calls and future service use the same source, with initial payload/reference independent of acquisition/environment memory. The microscopic environment is not reconstructed.

The training interface reveals x on a sacrificed probe without destroying the flag before its chosen measurement. There are two explicit, different realizations:

1. BIT-FLIP-ONLY source: prepare ordinary |0>^n and measure Z on each data output. The observed bit string is x. No stored entangled reference is used. This interface does NOT reveal phase errors for a general Pauli source.
2. GENERAL PAULI source: prepare n local Bell pairs, send one half of each, retain the other halves, and perform n Bell readouts on the returned/reference pairs. This reveals the full Pauli x and leaves the emitted flag available. It costs n entangled pairs, n retained reference qubits with their storage/noise, and n two-qubit Bell readouts per call. This is not an ordinary unentangled preparation interface.

Deployment does not measure the unknown payload as a probe. It measures only G with a learned K-outcome POVM and applies a known product-Pauli correction to the returned data. Trusted implementation of that small POVM and the Pauli corrections is an explicit control resource. The proof is not a hardware implementation/noisy-control guarantee. f must be efficiently evaluable and each nonempty fiber must have an efficiently specified fallback word; the root-bit feature in the pilot has this property.

## 2. Exact reduction of the FULL collective CPTP oracle

Every CPTP decoder R:L tensor G -> L, including arbitrary internal ancillas, has Kraus maps

    K_b=sum_x P_x tensor <v_(b,x)|.

Pauli orthogonality and the output partial trace of sum_b K_b^dagger K_b=I_L tensor I_G give

    M_x=sum_b |v_(b,x)><v_(b,x)| >=0,  sum_x M_x=I_G.

The entanglement-fidelity Kraus formula, evaluated on the maximally entangled d-dimensional logical/reference input, then gives exactly

    F_e(R N)=sum_x p_x Tr(M_x tau_(f(x))).

Conversely every such POVM is physically realized by measuring G and applying correction P_x. Thus this is the FULL-CPTP global oracle, not a local marginal or unitary-decoder restriction.

For each feature a, choose x*_a maximizing p_x in its fiber and put m_a=p_(x*_a). Since all flag states in a fiber are identical, grouping its POVM effects and assigning that grouped effect to x*_a cannot decrease the objective. Consequently

    V*=max_{M_a>=0, sum_a M_a=I_G} sum_a Tr(M_a m_a tau_a).

The collective optimization has reduced from an exponential error alphabet to K-state quantum discrimination. Computing the fiber modes remains a real acquisition/computation obligation, not a supplied oracle. The next section acquires them directly under the label-observation interface. No tree is needed there.

## 3. Finite ordinary flag data and a global regret theorem

Specialize G to a qubit. After observing x on each training call, choose j uniformly from X,Y,Z and measure the flag Pauli j, obtaining b. For every possible word x define the actual sample estimates

    phat_x=(1/N) sum_t 1[x_t=x],
    rhat_(x,j)=(3/N) sum_t 1[x_t=x] 1[j_t=j] b_t,
    Shat_x=[phat_x I+sum_j rhat_(x,j) sigma_j]/2.

These estimate p_x and S_x=p_x tau_(f(x)). Shat_x need not be positive; it is a known Hermitian objective coefficient, not an implemented state or channel. Only observed words need storage; unobserved estimates are exactly zero. A hash map requires at most N keys of length O(n), not an exponentially sized alphabet table. The pilot uses a256-entry array for convenience.

Suppose one simultaneous event gives |phat_x-p_x|<=delta_p and |rhat_(x,j)-r_(x,j)|<=delta_r for all words and axes. The exact trace norm of a qubit Hermitian matrix(a I+v.sigma)/2 is max(|a|,|v|). Thus

    ||Shat_x-S_x||_1 <= e=max(delta_p,sqrt(3) delta_r).

Choose xhat_a as the highest empirical word count within each feature (use a fixed fallback if unseen). Then p_(xhat_a)>=m_a-2delta_p. Solve the KNOWN K-outcome POVM optimization with coefficients Shat_(xhat_a) to certified additive empirical slack eta_alg, and implement that POVM. For each candidate POVM, objective perturbation is at most K e because each effect has operator norm at most1. Therefore the actual recovered channel obeys

    V* - F_e(Rhat N) <= 2K delta_p + 2K e + eta_alg.

Proof: replacing each true fiber mode by xhat_a loses at most2delta_p per feature. Optimizing the noisy coefficients and returning to the true coefficients loses at most2e per feature. No rare-event probability is divided by, no state rank floor is supplied, and no global distribution reconstruction is needed. This is ordinary finite hypothesis selection plus small quantum state discrimination; no novel learning-method superiority is claimed.

Let A be the known error-alphabet size, A=2^n or4^n. For fixed N, Hoeffding yields probability failure at most2A exp(-2N delta_p^2) for counts. The moment variable3*1[x_t=x]*1[j_t=j]*b_t has second moment<=3 and centered magnitude<=4. Scalar Bernstein therefore bounds all moment failures by

    6A exp[-N delta_r^2/(6+(8/3)delta_r)].

For completeness this Bernstein bound follows by expanding the centered mgf: |Y|<=4 and E Y^2<=3 imply E exp(theta Y)<=exp[3theta^2/(2(1-4theta/3))], using k!>=2*3^(k-2). Chernoff optimization gives the displayed exponent. Independence is across complete fixed-source calls; no independence between word estimates is required. Consequently N=O((K^2/epsilon^2)(n+log(1/beta))) suffices for fixed K and qubit flag, plus implementation slack. This is a statistical/computational statement at the stated label interface, not a uniform efficient decoder for all unknown quantum channels.

## 4. Actual noncommuting-flag pilot

The fixed8-qubit source used here generates an arbitrary-correlation test family: a fair binary root error, then a spatial chain copying its predecessor with probability999/1000. The LEARNER is not given or required to use this chain structure. The known feature is its first error bit. The two unknown emitted flags are

    tau_0=[[1,0],[0,0]],  tau_1=[[1/10,3/10],[3/10,9/10]].

They are pure and noncommuting. Rational source/measurement probabilities are sampled through uniform integer draws, not floating CDFs. The fixed plan uses2^22 training calls, then a fresh65536-call validation, distinct seeds, and target F_e>=19/20 at significance1/1000. Source parameters are used only by the generator and posthoc diagnostic, not by the count selector or measured flag optimizer.

The learner selects words00000000 and11111111. With K=2, delta_p=1/500 and delta_r=1/200, its simultaneous training failure bound is below4.106e-5. The theorem certifies full-CPTP oracle regret at most .042641200001, including the exact measured optimizer slack. The constant can be loose; it is not substituted for actual performance.

The learned binary measurement is the positive eigenspace of the difference of two acquired2×2 matrices, then rounded to a rational stereographic projector. Saved rational parameters tx,ty define exactly

    Pi_0=[[1,tx-i ty],[tx+i ty,tx^2+ty^2]]/(1+tx^2+ty^2),
    Pi_1=I-Pi_0.

This is exactly a physical rank-one projective POVM. It is implemented by a known single-qubit unitary followed by Z measurement; its entries are algebraic functions of the saved rationals. The empirical coefficient difference is(t I+h.sigma)/(2N), with integer t,h. The saved exact condition t^2<|h|^2 gives one positive and one negative eigenvalue. An integer-square-root enclosure of |h| at120 bits bounds its empirical optimization slack by3.7e-14. No unverified floating eigenvalue is the certificate. Gate-synthesis precision and physical control noise must be charged in any hardware implementation.

On deployment, outcome0 returns the data unchanged; outcome1 applies X to all8 data qubits. Under the promised bit-flip extension, the ordinary |0>^8/Z test succeeds exactly when the actual error word equals the chosen correction. Its success probability is the GLOBAL entanglement fidelity for this operation. This equivalence would fail for unmodeled phase/coherent errors.

Fresh validation observed2201 failures in65536 trials and passed the exact one-sided binomial test at the preset .95 fidelity target. The combined training/validation error allowance is at most .00104106. This is a simulated implemented-record-law certificate conditional on the stated trusted source/control interface, not a laboratory measurement.

Posthoc exact-source diagnostics give actual F_e=.9675410648, full-CPTP oracle .9675416846, and no-flag full-CPTP oracle .4965104825. Those values do not enter the learner or confidence decision. The first two agree closely because the learned measurement approximates the binary Helstrom measurement. A conventional equally informed method can use this identical strategy. The no-flag comparison removes an actual quantum resource; it is not an equal-resource algorithm comparison. Further, a different encoder could exploit the strongly correlated noise to protect a smaller payload; this work preserves the specified full8-qubit payload and does not optimize coding rate.

## 5. Actual cost and corrections

Training plus fresh validation generated4,259,840 complete source calls,34,078,720 data-qubit exposures, and4,259,840 emitted flag qubits. Each training call uses8 ordinary data preparations/readouts and one random flag-Pauli measurement. No entangled reference halves are used in this bit-flip-only pilot. Deployment uses one physical flag measurement and at most8 X gates. Classical word counting and the binary2×2 optimization are explicit. Waiting times, energy, hardware SPAM, synthesis drift and arbitrary persistent environment memory are not modeled or claimed.

`learn_and_recover_v1.py` completed all planned sampling but failed while serializing the large exact-binomial integer for its digest. The count files remained intact. `reanalyse_v2.py` performs ZERO new draws, reuses those records, permits large-integer serialization and applies the same exact-tail recurrence. No target, policy, sample size or seed changed. The original failure and correction are preserved.

## 6. Scope boundary and prior mechanisms

This construction removes the tree and marginal-floor requirements because the measurement interface reveals complete classical error labels; it does not acquire that interface from arbitrary noise. Pure phase errors are invisible to the ordinary all-zero bit-flip probe. The general-Pauli Bell-probe extension pays a different entangled-memory/readout resource. Feature-conditioned flag equality is also a source promise, not inferred from finitely many rare words.

The full-CPTP Pauli/gauge reduction, mode selection, Bernstein concentration and binary Helstrom measurement are standard mechanisms or direct consequences, not priority claims. The useful new local bridge is the complete finite data path from observed error words and noncommuting emitted flags to an implemented joint recovery at the actual scope. Parent Astra's learned-frame acquisition could potentially supply an approximate frame before this consumer, but no such transfer is asserted here without its complete instrument and feature-error bounds.
