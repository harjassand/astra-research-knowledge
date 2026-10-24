# Shorted quarter-wave shunt-filter comparison

Bounded finite-circuit check, 24 October 2026. This is a lossless single-TEM
network calculation, not a fabricated-device or phonon-interface result.

## Exact finite model

The source and load are real 50 ohm resistors. For each (N=1,2,3,4), the
network has (N) short-circuited 50 ohm quarter-wave shunt stubs and (N-1)
50 ohm quarter-wave links between adjacent stubs. The port reference planes are
at the first and last shunt nodes; no uncounted feed sections are included.
The stub admittance is

\[
Y_s(\omega)=-\frac{i}{50\,\Omega}\cot(\omega\tau),\qquad
\tau=\frac{1}{4(6\,\mathrm{GHz})}=41.6666667\,\mathrm{ps}.
\]

Every line and stub is retained as a distributed TEM section. Its integrated
resources are (C=\tau/Z=0.833333333\,\mathrm{pF}) and
(L=Z\tau=2.083333333\,\mathrm{nH}) per quarter-wave segment. The
vacuum-velocity length is 12.49135 mm per segment. The calculation cascades
the exact line and shunt ABCD matrices, uses the equal-real-port formula

\[
S_{21}=\frac{2}{A+B/50+50C+D},
\]

and checks \(|S_{11}|^2+|S_{21}|^2=1\). Power-balance error on the integration
grid is below (1.7\times10^{-15}).

## Results

The Bose-weighted integral is

\[
J=\int_0^\infty (u/\sinh u)^2 |S_{21}(u)|^2\,du,
\qquad u=f/(2k_BT/h),\quad T=100\,\mathrm{mK}.
\]

It was integrated by Simpson quadrature on 640,001 points over (0\le u\le15).
This includes the line/stub harmonic passbands throughout that range; the
remaining one-channel tail is at most (4.5011\times10^{-11}), using only
(|S_{21}|^2\le1).

| Stubs (N) | (J) | Minimum (|S_{21}|^2), 5.9–6.1 GHz | Total C (pF) | Total L (nH) | Main delay (ps) | Fits supplied aggregate C/L/main-delay caps? |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 1.074039 | 0.999828604 | 0.833333 | 2.083333 | 0 | yes |
| 2 | 0.794262 | 0.999998943 | 2.500000 | 6.250000 | 41.6667 | yes |
| 3 | 0.701008 | 0.999830711 | 4.166667 | 10.416667 | 83.3333 | yes |
| 4 | 0.674364 | 0.999995797 | 5.833333 | 14.583333 | 125.000 | no: exceeds C by 0.09552 pF and main delay by 29.37 ps |

The supplied caps are C ≤ 5.73781 pF, L ≤ 33.8362 nH, and main delay ≤
95.6302 ps. Within this small sweep, adding stubs lowers the all-frequency
integral while preserving the target pass window. The first three cases fit
the aggregate caps; the fourth gives the lowest (J), but violates the C and
main-delay caps. This is a finite set of candidates, not an optimization over
all passive networks.

For reproducibility, the endpoint complex transmissions are:

| (N) | (S_{21}(5.9\,\mathrm{GHz})) | (S_{21}(6\,\mathrm{GHz})) | (S_{21}(6.1\,\mathrm{GHz})) |
|---:|---|---|---|
| 1 | 0.999828604 + 0.013090717i | 1 | 0.999828604 − 0.013090717i |
| 2 | 0.052353841 − 0.998628068i | −i | −0.052353841 − 0.998628068i |
| 3 | −0.995720011 − 0.091500657i | −1 | −0.995720011 + 0.091500657i |
| 4 | −0.130561321 + 0.991438116i | i | 0.130561321 + 0.991438116i |

The open-stub finite-port design from the prior comparison has the same
aggregate C, essentially the full allowed main delay, and much less aggregate
L: C = 5.737809192 pF, L = 4.877137813 nH, main delay = 95.6301532 ps. Its
integral is lower, (J=0.473522549), but it misses the requested pass window:
\(|S_{21}|^2=0.049232918) at 6 GHz and ranges from 0.0470162 to 0.0515559
over 5.9–6.1 GHz. Thus it is not a passband solution for this requirement.

The (N=1) member is the direct one-resonator quarter-wave pass filter
baseline. A separate “weakly loaded” design would require specifying its
coupling network or loaded bandwidth; that choice is not fixed by the uniform
50 ohm short-stub family, so no extra tuned circuit was added to this bounded
comparison.

## Resource and scope notes

The summed physical lengths use a common vacuum phase velocity; in another TEM
medium the lengths scale with its phase velocity while the integrated C/L
values are unchanged at fixed impedance and delay. The cap comparison is
aggregate, not a per-cell footprint constraint. The ideal ABCD cascade omits
finite tee-junction discontinuities, conductor/dielectric loss, packaging,
parasitic modes, and contact calibration. Those can only be assessed with a
specified geometry and measured or independently validated multiport model.

Files: `shorted_quarterwave_comparison.py` is the NumPy-only replay;
`shorted_quarterwave_results.json` records its full numerical output.
