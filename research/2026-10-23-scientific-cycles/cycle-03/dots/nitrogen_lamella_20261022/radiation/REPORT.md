# Thermal gas radiation audit for the DOTS nitrogen lamella

## Result

The sources establish a large shortfall for ordinary thermal NO radiation **against a specified 110-microsecond rapid-export challenge**. They do not establish either a viable complete-cycle photon heat-export path or a rigorous, complete all-gas upper bound. In particular, the transient below-1700 K window is not a complete-reset deadline.

Using the parent's generous total retained NOx inventory, 1.924149395 mol/kg fresh (1.01 × 1.905098411), the relaxed low-radical reset certificate requires at least 53.995 kJ/kg fresh of export. It does **not** establish that all this export must occur within 110 microseconds. The parent's transient all-gas-below-1700 K window is approximately 51–111 microseconds and still has O declining from about 0.345 to 0.226 mol/kg, whereas the relaxed certificate requires O <= 0.003 mol/kg. These are distinct predicates. Heat transfer can continue downstream in the original 0.14-second packet cooler, whose eventual target is 300 K.

The calculations below test favorable available power over specified intervals, including 110 microseconds and 1 millisecond. They assume every assigned emitter is continuously available at 1700 K, every emitted photon escapes, and no incoming 300 K radiation is absorbed. They are not an actual temperature/composition history and do not establish when the reset certificate becomes applicable.

- Published NO Planck-mean estimate: 15.00 J/kg fresh in 110 microseconds; 136.37 J/kg in 1 millisecond; 6.82 J/kg in 50 microseconds.
- Published NO2 fit extrapolated to 1700 K, with **all** NOx assigned to NO2: 129.96 J/kg in 110 microseconds; 1,181.44 J/kg in 1 millisecond; 59.07 J/kg in 50 microseconds. This is not an upper bound because the underlying spectroscopy is temperature-incomplete.
- Very generous NO-only catalogue envelope: 724.83 J/kg in 110 microseconds; 6,589.32 J/kg in 1 millisecond. Its conditional NO-only minimum time for 53.995 kJ/kg is 8.194 milliseconds. This is a mathematical inequality within the represented ground-state model, not a measurement-certified universal bound, and the archived lifetime assignments have a consistency issue described below.

For the specified 110-microsecond challenge, the first estimate misses the energy target by about 3,600-fold and the extrapolative all-NO2 estimate by about 415-fold. This comparison does not exclude slower downstream radiation. Reabsorption cannot improve these idealized escape estimates. Dilution increases the number of collisions/thermal reservoir but does not create more NOx emitters per kg fresh.

## 1. Spectroscopic estimate, without guessed emissivity

DeBoskey, Geipel and Bojko (2026), Table 3, provide pressure-normalized Planck coefficients from HITEMP line-by-line calculations. The source is a newly posted primary preprint, not an independently verified upper-bound theorem. At 1700 K its fits yield:

| Species | a_P, m^-1 atm^-1 | Gross LTE power, W/mol | Energy at 110 microseconds | Energy at 1 millisecond |
|---|---:|---:|---:|---:|
| NO | 0.26818556 | 70,871.12 | 15.00 J/kg fresh | 136.37 J/kg fresh |
| NO2 | 2.32347781 | 614,005.75 | 129.96 J/kg fresh | 1,181.44 J/kg fresh |

Each row assigns the entire allowed NOx inventory to that species at fixed 1700 K. The NO heat-to-power quotient for 53.995 kJ/kg is 0.39595 seconds. This is a fixed-temperature model estimate, not the duration of the actual cooler or a measured relaxation time. The corresponding extrapolated NO2 quotient is 0.04570 seconds and inherits the serious completeness limitation below.

The conversion is derived here:

q_vol = 4 sigma T^4 a_P p_atm;
p_atm = (n/V) R T / 101325;
P_molar = 4 sigma T^4 a_P R T / 101325.

Thus this is integrated spontaneous LTE emission, not blackbody surface power with an invented gas emissivity. Ignoring the incident field gives an upper limit on **net loss for the same emission model**, but does not fix missing transitions in that model.

Primary source: https://arxiv.org/html/2610.19196v1 (Eqs. 1–7; Table 3; posted October 13, 2026).

### Critical NO2 qualification

The original HITEMP2019 authors explicitly state that NO2's NDSD-1000 input suggests a maximum applicable temperature of 1000 K, possibly lower for completeness, due to maximum rotational-level restrictions and missing polyads. They caution near that limit. The 2026 preprint's 5000 K tabulation does not demonstrate that these missing lines were supplied. Therefore its 1700 K NO2 value cannot be called a rigorous ceiling. This is a specific spectral-completeness gap, not an unspecified emissivity uncertainty.

Hargreaves et al., JQSRT 232 (2019), 35–53, section 5, pp. 50–51:
https://www.homepages.ucl.ac.uk/~ucapsy0/pdf/19HaGoRo.pdf
Alternative primary preprint: https://arxiv.org/abs/1904.02636

## 2. A deliberately loose NO-only mathematical envelope

For excitation energy E_i above the lowest state and total spontaneous rate Gamma_i = sum_j A_ij = 1/tau_i,

P_i = sum_j A_ij (E_i - E_j) <= Gamma_i E_i <= Gamma_max E_i.

Thermally averaging gives P_molar(T) <= Gamma_max U_internal(T). Canonical internal energy is nondecreasing in temperature because dU/dT = Var(E)/(k_B T^2). Consequently a cap at 1700 K bounds the same model at all lower temperatures, without assuming that individual line powers are monotone.

From the archived Wong et al. (2017) catalogue, containing 21,688 ground-electronic-state levels:

- Q(1700 K) = 10,096.22923.
- U_internal(1700 K), relative to the lowest level = 20,785.22165 J/mol.
- The smallest tabulated lifetime is 0.0060695 s, so the catalogue-wide rate maximum is 164.7582173 s^-1.
- P_molar <= 3.424536 MW/mol.
- Multiplying the generous inventory and 110 microseconds gives <= 0.724825 kJ/kg fresh, about 74.5-fold below 53.995 kJ/kg.
- At 1 millisecond, the same favorable envelope is <= 6.589319 kJ/kg fresh.
- If NO alone must export 53.995 kJ/kg while its temperature never exceeds 1700 K and its inventory never exceeds the stated cap, t >= heat / (inventory × power envelope) = 0.00819432 s. This 8.194-millisecond minimum has the same catalogue/model qualifications as the power envelope.

This assigns the fastest tabulated radiative rate to **all** thermal internal energy, including rotational energy, irrespective of actual selection rules and photon energies. It is about 48 times more favorable than the detailed NO Planck-mean estimate.

The minimum is shorter than the original 0.14-second cooler interval, so this loose envelope cannot exclude an NO-only downstream path on duration grounds. Nor does it demonstrate such a path. Any actual-cycle conclusion requires integrating emission along the temperature, chemical inventory, density, optical-depth and residence-time history, including the later approach to 300 K. The 110-microsecond result cannot substitute for that integration.

Primary paper: https://doi.org/10.1093/mnras/stx1211
Primary archived catalogue: https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/470/882/s_14n16o.dat.gz
Catalogue documentation: https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/MNRAS/470/882?format=html&tex=true

### Do not promote this to a universal physical bound

The inequality is exact; the empirical/model inputs are not universally certified. It bounds the represented radiative channels using a finite spectral model. Unrepresented channels and spectroscopic uncertainties require a separate allowance. The 2017 model excludes transitions above 40,000 cm^-1. Only about 6.1e-14 of its 1700 K population is above that energy, but population smallness alone is not a complete upper bound on unrepresented rates.

There is also a data-integrity caution: the archived CDS file assigns some very short lifetimes to v=0 levels, whereas the paper's Fig. 11 plots v=0 lifetimes of tens of seconds or longer in that energy range. For example, archived ID 6256 is labelled v=0, E=1708.491173 cm^-1, tau=0.0063359 s. I do not infer the reason or use any lifetime-energy pairing. The global maximum remains invariant under a permutation of the lifetimes, but that is a conditional argument, not proof that the archive issue is only a permutation. The CDS documentation also labels tau with inverse-second units; the publication and its figure establish seconds.

Current ExoMol's NOname and XABC state files were attempted as a verification route, but local downloads returned HTTP 503/timeouts. Their full transition files were not downloaded. The current XABC web page advertises a small cooling-function file, but it also could not be fetched. No permission denial was bypassed, no login was attempted, and no external action beyond reading occurred.

## 3. What remains unbounded

The result is not a bound on the complete N2/O2/NO/NO2 mixture. In particular:

- N2/O2 magnetic-dipole, electric-quadrupole and collision-induced emission have not been integrated at 1700 K.
- HITRAN2024's CIA documentation lists the relevant N2–N2 and O2 pair datasets predominantly near atmospheric temperatures, not 1700 K. Extrapolating those data would require justification. CIA also depends on pair densities and therefore cannot be folded into a pressure-independent per-molecule rate without specifying the density history.
- Atomic O/N emission and radiative association/recombination are not included in this numerical envelope. The initial O inventory cannot be called a coolant merely by assuming fast electronic emission. Likewise, kinetic recombination heat is not automatically photon export.
- Electronic pumping, plasma excitation, added emitters and solid radiation are outside the stated ground-state gas task.

Primary CIA documentation: https://hitran.org/data/CIA/CIA_Readme_2024.pdf
Primary database description and data index: https://www.hitran.org/cia/

## 4. Precise missing quantity and rapid-export challenge threshold

For the **specified rapid-export challenge** of closing the 53.995 kJ/kg gap in 110 microseconds at the most favorable stated inventory, NOx's time-averaged gross escaping power would need to be at least:

255.107 MW per mol NOx = 4.236e-16 W per molecule.

If treated as constant-temperature optically thin LTE at 1700 K, that corresponds to a pressure-normalized Planck coefficient of at least 965.36 m^-1 atm^-1 for the effective emitter. The NO2 extrapolation is 2.3235 m^-1 atm^-1. Therefore the precise NO2 research obligation is a thermally complete 1700 K emission sum (or a defensible upper bound on its omitted contribution) that can be compared to that threshold. To claim an all-gas exclusion, the analogous time-integrated contributions of N2/O2 pair and forbidden transitions and any permitted atomic channels must be added.

The 110-microsecond challenge is 490.864 MW/kg fresh. With the supplied 4.7e-5 kg/m^2 fresh column, this is 2.5378 J/m^2 total export, or 23.07 kW/m^2 averaged over the interval. These area numbers do not assume the gas is a black surface and do not establish a complete-reset deadline.

Bottom line: ordinary NO radiation is quantitatively far too slow for the specified 110-microsecond rapid-export challenge in the supported models. The favorable NO2 extrapolation does not meet that challenge either. Neither result excludes longer downstream heat transfer, and the present evidence supports neither a demonstrated complete-cycle photon heat path nor a rigorous all-gas radiative no-go. The remaining obligations are complete high-temperature emission data and an actual coupled thermal/chemical residence-time integral, not an invented favorable emissivity or an assumed reset deadline.

## Reproducibility

Run `python calculate_radiation.py`. Numerical output is `radiation_results.json`. The script uses only the 411 kB archived state file and the published fit coefficients; no multi-million-line transition download is needed. Source PDFs and rendered Fig. 11 are preserved alongside this report for audit.
