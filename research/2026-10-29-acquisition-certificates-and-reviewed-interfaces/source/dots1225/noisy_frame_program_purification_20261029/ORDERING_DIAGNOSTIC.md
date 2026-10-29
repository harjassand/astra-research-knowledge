# Purify rotation programs or quaternion programs first?
2026-10-29. Additive author diagnostic; not covered by the v1 freeze.

For dimension d and isotropic error e, the same symmetric-SWAP derivation gives
 D_d(e)=2-2e+d e^2/(d-1), p=D_d/2,
 e'=e(1+e/(d-1))/D_d, C'=4C/D_d.
This permits dimension-nine purification before the transducer, dimension-four purification after it, or a mixture. It does not require learning the unknown pure-state direction.

Root's separate exact transducer calculation gives p(v)=(405v^2-720v+512)/864 and w(v)=3v(62-9v)/(405v^2-720v+512), with a conditional isotropic quaternion marginal. The latter requires the separately supplied equivariance proof, not just evaluation at the identity quaternion. Each retained output is obtained from its own independent pair of R-program batches; three other outputs are discarded to guarantee product copies for subsequent purification.

`compare_orderings.py` evaluates all j=0,...,24 dimension-nine purification levels, followed by transduction and the least number of dimension-four levels reaching each target. Expected source calls per Choi program before dimension-four purification are 2 M_j/p(v_j). The script uses60-digit Decimal arithmetic, not certified intervals; its outputs are ideal-model expectation evaluations, not quantum trajectories or claims of global circuit optimality.

At physical contamination eta=.01 and target Choi infidelity1e-4, the best tested ordering is eight R-levels then conversion:271439 expected calls, compared with272687 for conversion then eight q-levels. At eta=.1, R-first also wins narrowly; at eta=.5, conversion-first wins among tested choices. No universal ordering advantage is claimed. Finite timeout, successful-output conditioning, PBT ports, protected memory and known-control costs remain additional.
