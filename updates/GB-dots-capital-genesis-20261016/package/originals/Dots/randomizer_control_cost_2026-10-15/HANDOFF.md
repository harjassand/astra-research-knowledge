# Paying for randomizer control

## Strongest result
Under a qualified common Hamiltonian dilation with local, private-parent coherent residuals, the actual global-character subset effects obey

E(all selected parent characters nonzero) ≤ p^|S| I,
p=min{1,(√q_ref+b_RMS)²}.

Here q_ref=min{1,a_ref²,mB(J,γ,t)} is the proved private-randomizer reference budget, with the exact telegraph factor B specified in the included reference contract, and b_RMS² bounds the second moment of the FULL joint residual action per parent. No exact ideal CP branch is needed. To turn this character bound into a memory-support statement, the actual residual must also transform covariantly under its initial private frame, with detection/locality proved on its complete affected support. A zero character alone is not a correctness certificate without that condition.

For c fixed initial/final control slots plus N~Poisson(μ), μ=mγt, and a qualified residual action u per slot,
b_RMS≤u√[(c+μ)²+μ].
The variance term and final inverse are charged. An independently proved actual total action can tighten the budget to min{1,a_actual²,(√q_ref+b_RMS)²}; the old reference action cannot be substituted for a_actual without proof.

## Finite deterministic alternative
For M fixed cells of lengths δ_l covering t, independent fair frame values give
B_det=½[∏_l cosh(2Jδ_l)−1].
For equal cells,
B_det≤½[exp(2(Jt)²/M)−1],
q_det=min{1,a_ref²,mB_det}.

There are at most K=m(M−1) internal binary updates, with N~Binomial(K,½). Therefore
b_RMS≤u√[(c+K/2)²+K/4],
p_coherent,det≤min{1,(√q_det+b_RMS)²}.
This removes unbounded Poisson update counts and arbitrarily close update times. Finite-width ramps still need an actual qualified waveform, privacy and support model; a sufficient serial spacing condition is mδ<t/M with reserved endpoint margins.

## When the paid bound improves
With the SAME full reservation and geometry, a sufficient coherent improvement over the old certified a_old² is
√q_ref+b_RMS<a_old.

For a_ref=a_old=Jt>0, any integer M>2a_old²/log[1+a_old²/(2m)] makes the exponential q_det bound smaller than a_old²/4. Then
u√[(c+K/2)²+K/4]<a_old/2
is sufficient. This is a symbolic existence regime, not a device estimate.

If supports or total duration change, compare the full budgets instead:
d0_new+μ_new p_new<d0_old+μ_old a_old²,
with requalified support/coloring constants where needed. Lowering p alone does not establish a better memory regime.

## Alternative stochastic interface
An exact full-process decomposition R=(1−ε)R0+εR1, with normalized CPTP branches, exact private reference R0 and input/history-independent scalar weight, gives p_CP=min{1,q_ref+f_control}. For Poisson updates,
f_control=1−(1−ε)^c exp(−με).
For deterministic cells,
f_det=1−(1−ε)^c(1−ε/2)^K.

This is a stricter alternative, not a conversion of ordinary infidelity into a fault probability. Even an arbitrarily small nontrivial coherent unitary error has no nonzero exact-identity CP branch. Mixed weak/control subset effects need the whole-process independence conditions proved in the audits.

## Evidence, prior work and remaining gate
The packet includes both independent proof audits, explicit obstructions and two offline replay suites. The control-cost suite checks scalar moments/counts, coherent and CP joint effects, exact-ideal-branch failures, private-frame leakage and dimensionless budget inequalities. The reference suite checks global Fourier effects and virtual-seed equivalence. Numerical inputs are synthetic algebra checks.

Closest prior work: He Wang, Continuous-Process Randomized Compilation v2, treats finite-width mismatch, Poisson control counts, boundary controls and global operational tradeoffs. Those mechanisms are established; the conditional local subset/covariance interfaces are the distinctions examined here. No novelty claim is made.

Still missing is one actual complete gadget Hamiltonian/dilation: all initial/internal/final controls, joint residual norm/action bounds, initial-frame covariance, private-record access, full support/detection, and fixed-duration scheduling. Ordinary gate infidelity cannot certify those inputs. No measured hardware advantage, generic noisy-controller qualification or new autonomous-memory threshold is established. NEXT_GATE.md states the exact stopping boundary and next test.
