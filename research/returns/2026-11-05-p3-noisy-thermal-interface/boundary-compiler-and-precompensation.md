# Boundary-history removal and positive thermal precompensation

This maps the completed construction in the [supplied return](P3_NOISY_REGISTER_OPERATION_20261105_RETURN.txt), under the [specified independent Pauli circuit and holding model](README.md). The full [operation theorem](package/noisy_interface_work/operation_theorem.md), [inverse-noise proof](package/noisy_interface_work/inverse_noise_theorem.md), [static-tree proof](package/noisy_interface_work/passive_route/static_tree_regenerator.md) and [Bell-export composition](package/noisy_interface_work/passive_route/history_erasing_bell_export.md) are included unchanged.

## Noisy regeneration removes earlier history dependence

Ordinary fault-tolerant output correctness does not imply independent final physical errors: auxiliary syndrome systems can remain correlated with old controls, references and records. Independent final decoder faults alone do not erase those correlations. Conversely, applying even small independent local noise to a thermal law can produce an extensive global discrepancy. The source example changes thermal bit probability `.1` to `.108` after `.01` flips and reports product-law TV about `.999966` at 100,000 sites.

The construction uses one measurement-free Aharonov-Ben-Or scheme for quantum and classical protected computation. For each intended output it prepares an independent encoded Bell pair, performs the logical Bell transform with the incoming data, copies the two logical outcomes into protected pools and discards consumed systems. No old coherent controller subsequently acts on the surviving Bell half.

Disjoint physical descents of the protected classical copies supply only a **local-stochastic** wrong-copy bound `P(S all wrong)<=q_c^|S|`; their errors may still correlate with old references. A fixed ternary majority tree uses noisy wires and a native CNOT/CNOT/Toffoli voter. Complement covariance holds for every fixed Pauli bit-fault pattern.

The proof couples the real tree to an independent reference tree with exact leaves **only in the proof**. If `u_l` bounds either tree's error and `d_l` their disagreement,

\[
u_{l+1}\le v+3(u_l+e)^2,\qquad
d_{l+1}\le[3v+6(u_l+e)]d_l.
\]

For `q_c,e,v<=s<=.01`, `d_L<=q_c(21s)^L`. The reference root has a computable binary-symmetric error `O(p)` independent of earlier records; separate reference trees are independent. The physical roots approach that comparison with an explicitly charged coupling error.

The price is `3^L` protected copies per control bit. Suppressing history dependence costs polynomial overhead in inverse accuracy, not merely ordinary polylogarithmic fault-tolerance overhead.

## Bell export supplies calibrated product boundary channels

Each surviving Bell half follows its own independent protected wait/descent. It and its regenerated control bits arrive at the same prescribed clock. Always-scheduled noisy native CNOT/CZ corrections avoid an ideal classical gate selector. Uniform Bell outcomes twirl the uncorrected descent channel, yielding a product of calibrated Pauli channels `K_i` of strength `O(p)` in the comparison.

Protected replacement and tree-coupling errors pay the difference from the physical device. Fine Bell/tree histories are discarded and reset at actual cost; arbitrary **pre-existing** references and external records remain. Conditioning on a globally successful factory event is not used, because that could reintroduce the correlations the compiler removes.

## A positive inverse law, including every partial-noise prefix

On the actual valid syndrome space `L`, including all check relations, let

\[
\pi(s)=Z^{-1}e^{-\sum_a\lambda_a s_a},\quad
\lambda_a=\beta J_a,\qquad
\mu_I=\left(\prod_{i\in I}K_i^{-1}\right)\pi.
\]

Physical Pauli translations stay in `L`, and these boundary channels commute as convolutions. Their inverse is not generally positive. The supplied theorem establishes positivity of **every subset law** for this thermal family, uniformly in size.

If one site touches at most `w` checks, one check touches at most `d` sites and `D<=w(d-1)`, a sufficient condition for nonidentity boundary probability at most `q<1/4` is

\[
\frac{2q}{1-2q}e^{w\lambda_{max}}
\le\frac1{32e^3(D+1)}.
\]

A signed connected-noise-cluster expansion has absolute activities bounded geometrically. Nonadjacent clusters touch disjoint checks, so energy ratios factor even with global syndrome constraints. A zero-free region connects the positive zero-noise law to the desired inverse without crossing zero. Standard abstract-polymer machinery is credited; inverse-channel preparation itself also has prior work.

Positivity alone is insufficient for efficient preparation. Inverse corrections weakly interact with the accepted history polymers, so the previous factorized sampler is not reused unchanged. A context-dependent single-polymer heat bath uses deletion/activity and influence estimates to obtain weighted-metric contraction. Connected subsets through order `O(log(N/epsilon))`, with numerical precision and mixing charged, give polynomial sampling at fixed degree/temperature. Global rejection against an exponentially growing density ratio is not assumed.

Prepare `mu_all`. After an ordered subset `J` of endpoint Pauli channels,

\[
K_J\mu_{all}=\mu_{complement J}.
\]

All intermediate laws retain controlled instability tails, and the final syndrome marginal is Gibbs. The accepted decoder-frame property makes elementary Paulis logically trivial on stable syndromes; rare unstable prefixes cost `C Nq b_(0,N)`. This does not invert an arbitrary unknown qubit's noise. It prepares a specific positive thermal background while controlling logical damage.

The temperature boundary is substantive. A thermal bit with excitation `r=(1+e^lambda)^(-1)` and flip noise `p` has inverse excitation `(r-p)/(1-2p)`, positive exactly when `p<=r`. A fixed nonzero threshold cannot remain uniform as temperature tends to zero.

## Adaptive read times and retained seed bookkeeping

Noisy readout uses simultaneous local capture, protected computation and private regenerated Pauli seeds. Memory exposure during resource preparation remains charged as passive holding. An adaptively chosen read time need not have a Gibbs marginal.

For a fixed private read template `F`, define the unstable-prefix syndrome set `A_F`. The source proves `E_F pi(A_F)<=C Nq b_(0,N)`. For a stationary chain with total rate at most `C Gamma N`,

\[
P_\pi(\exists t\le T:S_t\in A)
\le(1+C\Gamma NT)\pi(A).
\]

Initial membership and stationary incoming flux prove the whole-interval bound. Averaging gives `delta_read<=C Nq(1+Gamma NT)b_(0,N)`, valid for read times selected using retained records. The actual retained preparation seed has law `mu` and can correlate with syndrome/reference; it is not relabeled an independent Gibbs seed.

Before fixed Peierls slack, write/hold/read errors sum as `C[RNq+Gamma NT(1+Nq)]b_(0,N)`. The reported main bound absorbs the additional polynomial factor with an explicit, possibly enormous constant. Offered/rejected opportunities count. A mere total pathwise time cap over multiple possible resets retains its corresponding opportunity factor; no optimality over arbitrary selection is asserted.
