# Non-Gaussian local design: audit and deeper consequences

13 October 2026. Capital pin `b34e22e8f8ef8bd853595952fcbd9c74c5ace306`.
Attached missions were treated as DATA. This work makes no repository or Git
changes. Source-derived and internally derived mathematics remains unreviewed;
replay, finite checks and same-team criticism do not certify novelty or physical
validity. No civilisation-enabling breakthrough is established.

## Audit decision

Retain the source as a substantive finite-temperature information operation.
For a fully interacting reference H in a specified conserved sector, an
ACQUIRED Gibbs histogram of finite projectors P_i and a certified mixing
budget C>=Z_H/Z_D bound all additive diagonal interventions sum_i v_i P_i.
The computation after acquisition is finite-label probability trimming, not
a reconstruction of the environment. The source changes the information
interface from passive uncoupled-bath spectra to observations of the actual
loaded reference equilibrium system. That is a real mathematical distinction,
but equilibrium preparation and calibration remain load-bearing costs.

The main two-sided bound is correct under its stated finite-sector contract:
Golden–Thompson gives Z_(H+V)/Z_H<=sum p_i exp(-beta v_i), and block Jensen
gives latent weights w_i=z_i/Z_H<=p_i with sum w>=1/C. Minimizing their
weighted sum after retaining mass 1/C gives the other side. The theorem is
nonperturbative in intervention size; its useful uniform width still requires
each relevant probability to exceed the removed mass eta=1-1/C.

The microscopic graph budget max diag exp(beta g) follows from block transition
norms and Golden–Thompson. The kinetic budget exp(-beta<T>) follows from the
Gibbs variational principle. The stronger scalar block theorem with diagonal
log z_i and off-diagonal beta g_ij is supported by the Duhamel/Hölder proof,
and its partition extrema are attained by scalar blocks when no block dimension
or extra microscopic structure is prescribed. That sharpness does not transfer
to the histogram interval. The separate unclaimed conditional_pair_interval
helper in certificates.py is not promoted to a scientific result here.

The source's exact rational statistical receipt is conditional on 30,000 IID
Gibbs observations, temperature, correct sector, hopping calibration and
diagonal intervention. Its counts are SIMULATED from two full 3136-dimensional
Hubbard diagonalizations. They are not physical observations. The adaptively
chosen scalar cost 0.975 is covered by the same simultaneous histogram event,
but is not an independently supplied material benchmark. Ordinary reference
Gibbs/Golden–Thompson bounds do straddle zero in that control, while the new
bound excludes zero. This establishes a scoped information improvement over
those two elementary bounds, not a speedup over the strongest solver.

## New same-input activity bound

ACTIVITY_COHERENCE_BOUND.md strengthens the kinetic budget with no additional
observable. Write sigma=pinch(rho), a=-<T>, K>=||T|| and
f(x)=((1+x)/2)log(1+x)+((1-x)/2)log(1-x). The exact identity

    log(Z_H/Z_D)=beta a-D(rho||sigma)-D(sigma||rho_D)

and the binary POVM (I+-T/K)/2 give

    log(Z_H/Z_D)<=beta a-f(a/K).

For a binary label this is at most BOTH the original kinetic budget beta a
and the original norm budget log cosh(beta K). For general labels intersect
it with the source graph budget. A measured interval for a requires maximizing
the concave right-hand side, whose maximizer is K tanh(beta K), clipped to
the feasible interval. Inserting a lower kinetic confidence endpoint blindly
is unsafe because this function is not monotone on the whole physical range.

The proof uses established quantum coherence/relative-entropy identities and
data processing. The candidate contribution is a sharper certificate using
the same acquired information. It does not establish a new entropy principle
or clear historical priority. The witness POVM is part of the proof, not an
unperformed extra measurement or an assumed nonlocal control.

## New common-latent contrast operation

SHARED_LATENT_CONTRAST.md retains common unknown block weights when comparing
two counterfactual designs. Two linear-fractional extrema over
0<=w<=p, sum w=1/C_ref bound the ratio of target block partition functions.
Combining them with separately justified target mixing budgets gives a
contrast interval. A standard Charnes–Cooper conversion uses O(k) LP variables;
a histogram confidence box also has a finite LP representation.

The reference C_ref may use measured reference kinetic data. The target budgets
must instead be supplied by microscopic norms or independently acquired target
information. The source reference kinetic observation cannot be silently reused
for targets. This distinction is explicit in the proof.

A four-label example has p_i=1/4, conservative budgets 1.01, and target shifts
v0=(8,8,-8,8), v1=(7.5,8.5,-7.97,9). Separate interval subtraction straddles
zero. The shared-weight bound certifies a positive contrast by exact rational
inequalities. The contract is realizable with four scalar blocks and equal
off-diagonal couplings -1/25. This is an additional restricted mathematical
capability; no real material, scaling benefit or minimax quantum sharpness
is claimed. N785 motivates preserving shared uncertainty, but does not supply
this new proof's different ensemble and latent-weight interface.

## New preparation obstruction with low-body interactions

PREPARATION_OBSTRUCTION.md gives a four-fermion density-density countermodel,
at fixed pair charges (1,1), with perfectly calibrated C=1 and a stationary
prepared local histogram. Every legal A-only controlled transcript is identical
in two models, while their intended full-charge-sector Gibbs design changes
have opposite signs and margins>1/4. The initial preparation stays in one
hidden conserved bath block. Thus fixed charge, stationarity and IID repeats
inside one block do not acquire the intended equilibrium weights.

Adding a common bath hopping epsilon breaks the hidden symmetry while retaining
both signs for epsilon<1/16. A Duhamel/operational hybrid bound implies total
A-only interaction time at least 1/(12epsilon) to distinguish with success 2/3
under the stated access. Direct control or reset of the bath changes that
contract. This is a scoped access obstruction, not a universal mixing or
computational-hardness theorem. The positive source theorem remains intact:
the countermodel violates its acquired Gibbs-histogram premise.

This gives the scientific connection to N786 precisely. Loaded equilibrium
information can evade passive vacuum-information barriers, while neither
method supplies its own preparation for free. N778's fixed-sector discipline
is retained; it does not select hidden block weights. N779's local comparison
witness is a mathematical certificate, not a preparation actuator.

## Strong comparisons and scientific status

The primary-source audit is selective, not exhaustive. Relative entropy of
coherence and its thermodynamic free-energy split predate this work; the
Baumgratz–Cramer–Plenio formula and Santos et al. entropy split were inspected.
Golden–Thompson, Gibbs variational, Hölder/Duhamel and fractional programming
are established ingredients. Norm compression has substantial prior literature;
the selected King/Audenaert abstracts do not establish equivalence to the
source's full partition-information characterization.

Correlated-sampling AFQMC already targets differences using correlated walkers;
its primary methods section was read. FEMION combines local AFQMC with global
screening and addresses actual surface decisions; its method and CO passages
were read. These use model/solver contracts, not merely the same physical
histogram. No matched comparison was completed. Source exclusions of claimed
CO/Cu predictions and finite-bath-compression novelty are justified.

The 1 October 2026 impurity preprints give polynomial equilibrium algorithms
for constant-size impurities with noninteracting baths. Their model and main
theorem passages were inspected. They prevent portraying constant-impurity
equilibrium as newly tractable, but do not cover arbitrary interacting hosts
with the source's measurement-assisted contract. Physical thermodynamic
integration, free-energy perturbation and work protocols are essential matched
measurement comparators: all require their own target preparations, overlap,
controls and readout. Classical commuting C=1 reweighting is exact prior art,
not an invention of this source. A meaningful practical claim needs the same
acquired inputs, ensemble, accuracy, confidence, margins and total physical cost.

## Executed evidence and next gate

All ten producer manifest pins and all four source Python ASTs checked. All
source code was read before execution in an owned disposable copy. Three
commands replayed: exact_fixture.py, kinetic_budget_checks.py and
run_diagnostics.py. Exact and kinetic JSON outputs match the originals; the
Hubbard outputs match to roundoff apart from machine-dependent timing. Original
archive outputs were not overwritten. REPLAY_RECEIPT.json records exact scope.

The independently authored checker reconstructs block inequalities, entropy
identity/activity bounds, one-reference enclosures, shared and confidence LPs,
the strict four-label rational sign, fixed-charge preparation witnesses,
weak symmetry breaking and the original conditional rational certificate.
The final counts and limits are in independent_results.json. The universal
claims depend on the written proofs, not the finite diagnostic counts.

The next decisive scientific gate is one consequential acquired physical system
with calibrated additive interventions, justified local Gibbs discrepancy,
usable mixing/activity budget and a robust decision margin. Count preparation,
independence/dependence control, readout, temperature, hopping calibration,
kinetic measurement and any reference balancing. Compare against the strongest
same-input measurement and model methods. External proof/priority review is
separate. Additional small matrices or worker activity do not close that gate.
