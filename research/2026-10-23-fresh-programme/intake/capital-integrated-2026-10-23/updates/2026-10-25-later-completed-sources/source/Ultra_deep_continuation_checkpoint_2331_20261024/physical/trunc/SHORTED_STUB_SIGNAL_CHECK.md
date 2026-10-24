# Shorted quarter-wave stub signal check

## Contract and circuit

This is an ordinary lossless one-TEM transmission-line network between real
50-ohm matched ports. The signal contract is the full complex passband
transfer over `5.9--6.1 GHz` for a 6-GHz carrier. The chosen coherent
waveform metric allows exactly one constant phase and one constant delay:

```text
epsilon = sup_band | exp(i*(omega-omega0)*tau) S21(omega) - exp(i*phi0) |.
```

For every square-integrable incident spectral amplitude supported in this
band, the through-port spectral error from the corresponding delayed,
phase-shifted ideal waveform is at most `epsilon` times the input norm. This
is a classical linear transfer-function statement; it is not a quantum
channel-fidelity or added-noise claim.

The network has a 50-ohm feed line of the inherited `tau_main=95.6302 ps`,
split equally before and after the filter, `N=1,2,3` identical short-circuited
60-ohm shunt stubs, and a 50-ohm quarter-wave section between each adjacent
pair of stubs. All quarter waves are tuned to 6 GHz, so
`tau_q=1/(4 f0)=41.6666667 ps`. The one-stub case has no inter-stub section.
Each junction is treated as an ideal shunt node. Loss, T-junction fringing,
finite short inductance, and port-launch parasitics are outside this 1D model.

For a lossless line of impedance `Z` and delay `tau`, distributed resources
are `C=tau/Z` and `L=Z*tau`. Thus, charging the whole feed path, every
interconnect, and every stub gives

| Stubs | Total C (pF) | Total L (nH) | Main-path delay (ps) | Sum of all line-segment delays (ps) |
|---:|---:|---:|---:|---:|
| 1 | 2.607048 | 7.281510 | 95.630200 | 137.296867 |
| 2 | 4.134826 | 11.864843 | 137.296867 | 220.630200 |
| 3 | 5.662604 | 16.448177 | 178.963533 | 303.963533 |

All three satisfy the old `C<=5.73781 pF` and `L<=33.8362 nH` limits. The
three-stub design is close to the capacitance limit, with 0.075206 pF spare.
The extra path and stub lengths are explicit: no line capacitance, inductance,
or delay is treated as free. In vacuum, each quarter-wave section is 12.491
mm long; a dielectric changes physical lengths, not the delay-based C/L
accounting in this nondispersive model.

The delay column distinguishes two interpretations of the 95.6302-ps number.
The table retains it as the baseline feed-line delay and adds each required
quarter-wave interconnect. If instead 95.6302 ps is a hard limit on total
main-path propagation, the main feed must be shortened. If it is a hard limit
on the *fitted signal group delay*, the reactive stubs also count; that case
is quantified below.

## Exact complex transfer and coherent bound

Use the `e^(+i omega t)` convention. A line has ABCD matrix

```text
[[cos(omega*tau), i Z sin(omega*tau)],
 [i sin(omega*tau)/Z, cos(omega*tau)]],
```

and a short-circuited shunt stub has input admittance
`Y=-i*cot(omega*tau_q)/Zs`, represented by the shunt ABCD matrix with
`C=Y`. For equal real reference impedances `Zp=50 ohm`,
`S21=2/(A+B/Zp+C*Zp+D)`. The executable script multiplies these matrices
and independently checks the closed forms below.

Let `q=Zp/Zs=5/6`, `delta=(pi/2)*(f-f0)/f0`, and `t=tan(delta)`. After
removing the inherited feed-line phase `exp(-i omega tau_main)`, the
denominators for `N=1,2,3` are

```text
D1 = 2 + i q t,
D2 = cos(delta) * [-2(1+q)t + i(2-q(q+2)t^2)],
D3 = -[(1+i(1+q)t)(2-q(q+3)t^2+i(q+2)t)]/(1+t^2),
S21,N = exp(-i omega tau_main) * 2/DN.
```

At the carrier, the constant phase is
`phi0=-omega0*tau_main-(N-1)*pi/2`. The phase tangent at the carrier has
delay

```text
tau_fit = tau_main + tau_q * {q/2, 1+q, (4+3q)/2}  for N={1,2,3}.
```

This gives `112.991311 ps`, `172.019089 ps`, and `231.046867 ps` for the
retained 95.6302-ps feed. These are actual fitted/tangent delays, including
the stubs' reactive group delay. The values are not the physical line-delay
column above.

With `P=|S21|^2`, direct simplification gives

```text
P1 = 1/[1+q^2*t^2/4],
P2 = 1/[1+q^2(q+2)^2*t^4/(4(1+t^2))],
P3 = 1/[1+q^2*t^2(1-(q+1)(q+3)t^2)^2/(4(1+t^2)^2)].
```

On this band, `|delta|<=pi/120`, `|t|<=0.026185922`, and these expressions
give the following all-frequency lower bounds; no frequency grid is needed
for the power claim:

| Stubs | Lower bound on `|S21|^2` |
|---:|---:|
| 1 | 0.9998809686 |
| 2 | 0.9999993446 |
| 3 | 0.9998809686 |

For the waveform metric, use the one common carrier phase and the center
group-delay tangent above. The phase residuals are

```text
R1 = -atan(q*t/2) + (q/2)*delta,
R2 = -atan((1+q)t/[1-q(q+2)t^2/2]) + (1+q)*delta,
R3 = -atan((1+q)t)
     -atan(((q+2)t/2)/[1-q(q+3)t^2/2]) + (4+3q)*delta/2.
```

Applying `|atan(u)-u|<=|u|^3/3` and bounding `tan(delta)-delta` on the stated
interval yields the following conservative continuous-band bounds:

| Stubs | `sup |R_N|` bound | Complex waveform error `epsilon` bound |
|---:|---:|---:|
| 1 | 2.926e-6 | 6.245e-5 |
| 2 | 8.684e-5 | 8.717e-5 |
| 3 | 1.141e-4 | 1.736e-4 |

Here the complex bound is `1-|S21| + |R_N|`; use
`1-(1+u)^(-1/2)<=u/2` for the amplitude deficit. Thus all three meet the
chosen `epsilon<=1e-3` passband contract and exceed the requested 0.9 power
transmission by a wide margin. The script also samples 20,001 points and
checks the exact ABCD response against the closed forms.

If 95.6302 ps is a hard *total fitted-delay* ceiling, retaining the original
feed violates it. Shortening the feed makes `N=1` and `N=2` feasible in this
model: the center-tangent feed delays would be 78.2691 ps and 19.2413 ps,
respectively, to bring `tau_fit` to 95.6302 ps. The N=3 stub/interconnect
network alone contributes 135.4167 ps at the carrier, so it cannot meet that
ceiling for these 60-ohm stubs. The shortened N=1 design uses 2.259826 pF and
6.413454 nH; shortened N=2 uses 2.607048 pF and 8.045399 nH. Both remain
inside the old C/L limits.

This is a conventional narrow-window signal compatibility result, not
evidence of a unique-band filter or thermal advantage. Identical quarter-wave
stubs and spacers repeat their responses at odd harmonics; real junction,
short, conductor, and dielectric parasitics can change the stopband, heat
current, and passband. The analytic inequalities certify the idealized
single-TEM circuit transfer only.
