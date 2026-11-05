# Local perfect sampling yields a thermodynamic AKLT pair correlation

## Precise statement

Fix distinct lattice sites i,j and an increasing sequence of open rectangular regions R_n exhausting Z² and containing i,j eventually. In each region take the spin-2 AKLT virtual-identity boundary mixture

    sigma_R = V_R I_boundary V_R† / Tr(V_R I_boundary V_R†).

Assume the independently established marked-loop ancestor construction has an almost surely finite complete ancestor clan for each finite vertex query, and that its finite-box and infinite-lattice versions realize the same canonical loss-network process under restriction of one underlying marked Poisson field.

Then the specified pair correlations have a limit

    lim_n Tr(sigma_Rn S_i·S_j)
      = 9 (-1)^parity(i,j) E[C_ij delta(P,Gamma_infinity)],

where a null path contributes zero, P is drawn from the rational all-length source-path proposal, and only the exact stationary loops touching P are needed. The output has deterministic range width 9C_ij and therefore the same finite-sample Hoeffding guarantee as the finite-box estimator. No finite-box extrapolation is used in the infinite-lattice implementation.

This theorem identifies this pair-correlation limit for the specified boundary mixtures. It does not establish uniqueness of the full infinite-volume quantum state, boundary-condition independence, a quantum gap, or a dynamical/Kubo response.

## Proof by an explicit coupling

Draw the infinite-lattice path proposal first. Its non-null output is one finite physical path P almost surely. The finite-box proposal can be coupled by returning that same path when it is contained in R, and null otherwise. Early rejection in the finite implementation has exactly this law; unused random bits may simply be assigned on a larger probability space.

Independently construct the stationary marked loop cylinder field on Z². To determine the accepted time-zero loops touching P, explore their complete backward ancestor clan. Almost-sure finiteness gives finitely many cylinders, each with a finite loop route. Hence there is an almost surely finite random radius containing P and the full spatial union of this clan.

Every sufficiently large R_n contains that union. Under the same underlying cylinder field and pair marks, restricting to loops wholly contained in R_n cannot remove any relevant ancestor. No additional finite-box ancestor appears because every finite-box cylinder is already a cylinder of the unrestricted field. Therefore the accepted loops touching P, and thus the entire physical readout, agree exactly for every sufficiently large n.

Let X_n and X_infinity be the coupled finite-box and infinite-lattice readouts. We have X_n→X_infinity almost surely, with |X_n|≤9C_ij uniformly. Dominated convergence gives convergence of their expectations. The finite-box coherent-state/source-edge identity identifies E[X_n] with Tr(sigma_Rn S_i·S_j), proving the formula.

The proof uses the fixed finite source-path normalizer. It does not require an estimate of the rate of convergence, a physical-box cutoff, or a statement about arbitrary observables.

## Exact confidence arithmetic

`exact_confidence.py` combines the proved rational log enclosure from `exact_lazy_time.py` with integer square-root rounding. For a fixed sample count M and rational failure probability alpha, let l_upper≥log(2/alpha) be an exact rational upper bound. Set

    q = (9C)^2 l_upper / (2M).

The displayed radius is an outward rational square-root bound r with r²≥q. Both sample mean and interval endpoints are exact Fractions. Consequently the reported closed interval has mathematical coverage at least 1-alpha under the independent ideal-fair-bit specification. There is no floating-point ordering or inward confidence rounding.

For nearest neighbors, C=301805115576299/500964985405440. The exact outward radius for 10,000 attempts and alpha=1/20 is

    73636640719 / 1000000000000 = 0.073636640719.

For requested radius1/100, exact rational upper-bound arithmetic gives M=542236 attempts. This is a fixed budget chosen in advance, not a data-dependent stopping rule.

## Implementation

`estimate_local_spin.py --infinite` uses the infinite-lattice path proposal and local perfect loop sampler, reusing prevalidated proposal tables between queries. `--size N` instead computes the corresponding specified finite open-box mixture. All path generation, rejected local proposals, exact time comparisons, ancestor cleaning and output processing are included in elapsed time. Mathematical confidence assumes independent fair bits; Python PRNG benchmarks are reproducible numerical diagnostics.
