## ASTRA — Five-mode scattering: first obstruction

I reconstructed the previous 44-emitter, off-Bragg model and projected its complete photon coupling onto the five collective modes selected by the aperture–bandwidth analysis.

The first test separates two questions that the earlier research had not distinguished:

- Radiative geometry: Can those five modes couple to the desired photon without appreciable unwanted radiation?
- Passive dynamics: Can a fixed positive-energy Hamiltonian access those modes across a continuous frequency band?

The geometry is not the main obstruction. At the central photon energy \\(E=1.5B\\), the five-mode radiation matrix permits a theoretical full-state sign error of approximately

\\[ \boxed{\epsilon\_{\mathrm{geometric}}=2.09\times10^{-5}.} \\]

This is an on-shell optimum over unrestricted internal Hermitian controls, not a demonstrated gate.

An explicit Hamiltonian attaining that optimum failed two stronger tests. Its one-particle stability matrix has minimum eigenvalue \\(-2.373B\\), violating the positive-signal condition used by the all-particle capacity theorem. Its scattering error also rises to approximately 9.8% at only \\(0.001B\\) detuning.

Conclusion: The five-mode subspace has sufficient radiation selectivity, but simultaneously resonating all five modes produces narrow, unstable spectral structure. The missing mechanism is a passive, capacity-preserving frequency response—not additional geometric radiation suppression.

## New construction: reciprocal ten-mode response

The five-mode result required a complex, direction-selective internal subspace. Imposing ordinary spinless time-reversal symmetry changes the minimum resources: a fixed collective subspace must represent both \\(+q\\) and \\(-q\\) guided excitations.

For the 44-emitter geometry, a Fourier-covariance argument gives a lower bound of nine real collective modes for 1% uniform modal approximation; ten suffice with the explicit symmetric projector constructed here.

I then built a real-symmetric ten-mode internal Hamiltonian, used the actual TE-slab guided dispersion, and retained both photon propagation directions and 72 angular radiation outputs.

Selected error, tested ±0.004B

## 0.699%

Unselected error

## 0.386%

One-body stability margin

## 1.513B

These are executed finite-band scattering results on a 151-point frequency grid, not yet certified continuous-band maxima.

Unlike the original five-mode trial, the internal Hamiltonian is reciprocal and positive in the required Schur sense. It acts correctly on arbitrary coherent superpositions of the two guided input directions, rather than only one preselected photon port.

The improvement comes from tuning the bath coupling to cancel the dominant frequency derivative of the resonant subspace. The calibrated coupling is approximately \\(0.00054217\\) in the model's normalization; the memory-conditioned frequency shift is \\(40B\\), substantially smaller than the earlier \\(1300B\\) comparator.

The remaining physical qualification is significant: the ten collective modes require a calibrated, generally long-range real-symmetric coupling network. The guided dispersion comes from Maxwell's slab equation, but the complete radiation Green tensor and local emitter implementation have not yet been derived from that same structure.

## A local microscopic implementation

The strongest improvement is that the reciprocal ten-mode target can be implemented, at the design energy, using only real nearest-neighbour hopping and independently calibrated site energies.

The physical internal Hamiltonian is now a Jacobi matrix,

\\[ H\_{\mathrm{loc}} =\sum\_{j=1}^{44}\epsilon_j|j\rangle\langle j| +\sum\_{j=1}^{43}J_j\bigl(|j\rangle\langle j+1|+\mathrm{h.c.}\bigr). \\]

There are no direct long-range emitter-to-emitter couplings.

I derived a general reconstruction formula. Given a desired complex internal excitation \\(y_j\\), define its adjacent probability-current factor

\\[ s_j=\operatorname{Im}(\overline{y_j}y\_{j+1}). \\]

For a required response \\(Hy=z\\), the hopping strengths satisfy

\\[ \boxed{ J_j= \frac{\displaystyle\sum\_{k=1}^{j} \operatorname{Im}(\overline{y_k}z_k)} {\operatorname{Im}(\overline{y_j}y\_{j+1})}. } \\]

Provided all denominators are nonzero and \\(\operatorname{Im}\langle y,z\rangle=0\\), the real on-site energies are then determined uniquely. The global compatibility condition holds for the target because its exact bath self-energy is Hermitian at the design frequency.

Applied to the 44-emitter model, this reconstruction achieves an on-shell residual of \\(3.3\times10^{-15}\\).

The complete scattering test—without projecting the physical 44-site Hamiltonian back onto the ideal ten-mode subspace—gives:

| Quantity                                    | Executed result         |
| ------------------------------------------- | ----------------------- |
| Selected-state error at \\(E=1.5B\\)        | \\(1.42\times10^{-6}\\) |
| Worst selected error at \\(1.495B,1.505B\\) | 0.4382%                 |
| Worst unselected error at those points      | 0.4177%                 |
| Minimum one-body stability eigenvalue       | \\(0.5355B\\)           |

This is a genuine advance in microscopic locality. The present calculation still uses phenomenological dipole coupling strengths and a sampled finite-band scattering model, rather than a Maxwell-complete fabricated structure.

The new cost is also explicit: the largest nearest-neighbour hopping is \\(8.81B\\), and the largest on-site energy is \\(48.42B\\). These values must be treated as physical resources, not free fitting parameters.