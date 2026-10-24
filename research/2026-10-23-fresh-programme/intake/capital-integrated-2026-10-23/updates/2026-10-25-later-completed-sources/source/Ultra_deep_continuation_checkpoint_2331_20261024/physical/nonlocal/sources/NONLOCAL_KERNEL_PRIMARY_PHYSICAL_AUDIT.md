# Primary-source audit: nonlocal spring kernels and realized rods

Scope: compare the ideal positive nonlocal point-mass kernel in
`thermal/NONLOCAL_KERNEL_CONSTRUCTION.md` with the named primary sources and
one fabricated rod-routing realization. This is a source and model-boundary
check, not a novelty or priority determination.

## What the cited sources actually instantiate

**Kazemi et al., PRL 131, 176101 (2023), arXiv:2302.00591.** The paper's
single-band model is an infinite monoatomic chain of identical point masses
with linear springs to neighbours at each range (n=1,ldots,N):

`m ü_j = sum_n k_n (u_(j+n) - 2u_j + u_(j-n))`.

Its dispersion is the corresponding cosine series; Eqs. (4)–(5) obtain
spring coefficients by Fourier inversion of a target `Omega(q)^2`. The
assumptions are passive, free-standing (no grounded springs), reciprocal,
stable, and finite static stiffness. The general inverse design does not
require each `k_n` to be positive; positivity has to be checked for the
specific target. The triangular kernel here does satisfy it explicitly.
Their calculations use 10–25 spring types for designed examples, and finite
chain wave-packet simulations with 5000 sites for selected critical points.
The article reports no manufactured sample, connector geometry, thermal
conductivity, or thermal-current measurement. Its “diffusion” discussion is
wave-packet-envelope spreading from dispersion curvature, not diffusive heat
transport. [Primary full text](https://arxiv.org/html/2302.00591v1).

**Chen, Kadic & Wegener, Nature Communications 12, 3278 (2021).** Their 1D
toy model again treats point masses and Hooke springs, but their 3D proposal
replaces these by finite geometry in one polymer-like constituent: cubes as
effective masses, thin vertical rods for nearest-neighbour links, and pairs
of thick oblique rods plus an auxiliary frame to route the third-neighbour
link. The paper gives `a_z=100 µm`, `a_xy=2a_z=200 µm`, cube side
`t1=0.40a_z=40 µm`, frame height `t2=0.60a_z=60 µm`, and rod radii
`r1=0.08a_z=8 µm` and `r2=0.12a_z=12 µm`. Its representative elastic
parameters are `E=4.2 GPa`, `ν=0.4`, and `ρ=1140 kg/m^3`; the paper says
these serve as an example and can be rescaled. This is a continuum numerical
design, not the fabricated sample. The authors explicitly note that rods and
frames add substantial mass, and that the longer beams' resonances fall as
length increases. The higher gray bands in their Fig. 4 partly arise from
local resonances of those long connecting beams. The point-mass toy chain
therefore does not model the extra connector degrees of freedom. [Primary
article/PDF](https://www.nature.com/articles/s41467-021-23574-2.pdf).

**Iglesias Martínez et al., Science Advances 7, eabm2189 (2021).** This is
the closest physical support comparator: it fabricated the 3D nonlocal
architecture and measured driven-wave dispersion. The microscale sample is
IP-S polymer made by multiphoton 3D laser printing, with 50 axial periods
(`a_z=100 µm`) and a `2×2` transverse cross-section. Reported dimensions
include `a_xy=200 µm`, vertical-rod diameter `2r1=16.8 µm`, oblique-rod
diameter `2r2=25.2 µm`, and frame dimension `t2=60 µm`. The finite beam is
thus about 5 mm long and 0.4 mm across; the “mass cubes” and connectors are
one continuous printed polymer structure, not detached point bodies joined by
massless springs. The geometry needs support/scaffolding during printing;
the overhanging unit cell is split and written in multiple passes.

The companion macro sample is an air-channel system: 50 cells with pitch
`a_z=5 cm`, total length 2 m, made from 100 fused-deposition-printed PLA
halves, glued and screwed into a sealed channel, with microphones inserted at
the cells. It is not a thermal solid link.

In both experiments a piezo or loudspeaker drives one end at stepped
frequencies, and local displacement or pressure is measured along all 50
cells. The authors Fourier-transform spatial wave amplitude to estimate
`omega(k_z)`, with data normalized to unit total spatial power at each
frequency. The far end is deliberately fully reflecting; with finite damping
the sample contains a mixture of standing and propagating waves. Their
finite-sample simulations include phenomenological damping (5% imaginary part
of `E` for the elastic case; 2% of sound speed for air). These are strong
dispersion and wave-propagation demonstrations, but they do not measure
transmitted heat, a Landauer channel count, or a ballistic/diffusive thermal
regime. The standing-wave condition and normalized spectra also mean the
figures are not a transmission measurement. [Primary full text, author
repository PDF](https://publikationen.bibliothek.kit.edu/1000141113/136312450),
[DOI](https://doi.org/10.1126/sciadv.abm2189).

## Thermal-conduction check for the same-material rod model

For an ideal uniform axial rod of length `L` and area `A`, using Fourier
conduction and linear elasticity gives

`k_e = E A/L`, `g_e = kappa_th A/L`, hence `g_e/k_e=kappa_th/E`.

For a one-dimensional network with edge spans `n a`, the affine-strain
stiffness and the Fourier-network conductivity weight each link by `n^2`.
Consequently, if the same homogeneous rod material is used on every edge,
with perfect joints and no other heat path,
`sum_n n^2 g_n = (kappa_th/E) sum_n n^2 k_n`. In that restricted diffusive
network model, redistributing a fixed mechanical `K_eff=sum n^2 k_n` does
not lower the corresponding Fourier conductivity. This is an elementary
edge-network consequence, not a result reported in either paper.

It is not a general identity for the fabricated continuum: frames, cubes,
interfaces, parallel paths, contact resistance and cross-section-dependent
three-dimensional fields must be included in a continuum thermal solve. It
also does not determine coherent elastic-phonon Landauer transport. The
2021 experiments are coherent, externally driven wave spectroscopy with
finite damping/reflection; they do not measure either low-temperature
ballistic heat flow or the steady Fourier heat conductivity. The papers
therefore support finite-range rod routing and its additional modes, but do
not establish thermal suppression from the designed dispersion.
