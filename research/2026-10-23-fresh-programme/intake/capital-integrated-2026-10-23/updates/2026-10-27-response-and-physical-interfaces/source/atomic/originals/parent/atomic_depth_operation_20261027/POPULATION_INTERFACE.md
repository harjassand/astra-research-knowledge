# What the CrSBr population fit does and does not acquire

**Completed mathematical/source check, not an acquired physical layer model.**
The experiment demonstrates retained column-level Cr redistribution. Neither its
mean-population fit nor this check identifies a layer-specific move probability.
The SI maps intensity to populations by global min-max normalization; a
state-resolved intensity-to-count calibration is another required assumption,
particularly when hidden defect depths alter electron channelling.

Sources: [Nature article](https://www.nature.com/articles/s41586-026-10431-9),
public SI PDF pp39–41, and the authors' [pinned notebooks](https://github.com/KleinAtomLab/Mesoscale-atomic-engineering/tree/6844cc568271d448704a0eb6ee55ddfd5246d242).
The main article body was not acquired. Local source hashes and executed checks
are in `POPULATION_RESULTS.json`; code is `population_interface.py`.

## Normalization and an explicit ambiguity

Write a=Gamma02 and b=Gamma20. For N independent three-state atoms with
native-to-each-interstitial rate a and reverse rate b, expected fractions satisfy
exactly the SI equations: p0'=b(p++p-)-2a p0 and p±'=a p0-b p±.
N cancels upon division of counts by N. Under this interpretation a,b already
are per-atom rates. The all-native column's first-event rate is 2Na, a different
observable. Dividing the fitted rate by N requires a different model/statistic.

Divide N=16 into independent blocks of size k, each moving together with
per-branch rate a and reverse rate b. Expected fractions obey the same equations
for every k in {1,2,4,8,16}, but first-change rate is 2Na/k. Code checks exact
rational generator identities in all 222 aggregate count states. For even k an
alternative block moves in equal +/- halves at total rate 2a and returns at b.
It also respects p±<=1/2 on every trajectory and has the same symmetric mean
law and first-change ambiguity; 19 states are checked separately. These are
identifiability countermodels, not proposed microscopic mechanisms.

At SI a=.992/s,b=.089/s, every model has expected native fraction .0580810 at
2s. No-first-change probability ranges from 2.676e-28 for independent atoms to
.0189112 for one synchronized block; native-fraction variance differs sixteenfold.
Resolved event sizes or correlations could distinguish these models. A mean
curve alone cannot. Deposited traces have not been calibrated as such event-size
measurements. A useful acquisition target is jointly calibrated contrast, event
size/covariance, timing and dose, rather than another mean exponential fit.

## Source versions and arithmetic

At stated fluxes 1.9e24 and 2.4e24 e/cm²/s, the SI fit yields exactly
248/475=.522105 and 89/2400=.0370833 barn. The pinned notebook uses a=.779/s,
b=.1128/s, giving .410 and .047 barn, the printed values. Swapping SI flux
denominators also approximately reproduces those values. We do not know which
version/conversion explains the difference. Neither pair is a corrected physical
cross section. The deposited 200-keV sample clock is separately unresolved by
a factor of four.

## Dose dimensions: a separate interface

`Dose_rate_profile.ipynb` multiplies exp(-r²/(2sigma²)) by total electrons/s.
This Gaussian has area 2pi sigma²; it is not normalized as an areal density.
The notebook then sums over y points without dy and labels the sum e/Å²/s.
Holding beam parameters fixed, its central numeric value is 1.21981e8 at
dy=.1Å, 2.43963e8 at .05Å, and 4.87925e8 at .025Å. Physical areal dose cannot
depend on this plotting-grid choice. Multiplication by dy would make a line
integral, not an areal density. The cross-section notebook uses stated fluxes
as hard-coded inputs; its separate peak diagnostic is not time-averaged dose.

For a *conditional* normalized circular Gaussian, FWHM .8Å,total current20pA,
uniformly sinusoidal across ±2.385Å, central areal flux is 1.97725e7 e/Å²/s.
This analytic-profile/numerical-quadrature value is not a measured probe or
replacement calibration, and need not equal real channelled atomic flux.
Finite source time sampling and uniform-phase average are recorded separately.

These gates concern mean-law granularity, clock/version consistency, and dose
normalization. They do not invalidate the observed stable defect pattern. They
prevent treating printed effective cross sections as acquired independent layer
damage laws. Run `python3 population_interface.py`: about .07s, standard library,
no physical experiment or external write. No new method, physical no-go,
historical priority, or capability advantage is claimed.
