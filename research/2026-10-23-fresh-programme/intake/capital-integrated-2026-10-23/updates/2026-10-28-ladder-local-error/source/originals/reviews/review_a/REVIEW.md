# Independent mathematical and physical review

**Verdicts, at the requested spectral scope:** S41 **ACCEPT**; S83 **ACCEPT**;
S29 **ACCEPT**; S62 **ACCEPT**. Each endpoint establishes
`0 < rho_(1/5)(Ep) < infinity` for the normalized dressed even pair and the
physical perturbation `V=n_L-n_R`. These are four separately checked
derivations, not four votes. Their mutual agreement is not my proof.

No endpoint establishes a resonance pole, an exponential survival law, a
finite-detuning lifetime, or a gate-error estimate. Each correctly identifies
that boundary. The decimal response is ordinary quadrature, not an interval
enclosure. No historical priority or physical implementation is certified.

## Reconstruction of the load-bearing argument

I reconstructed the physical model from the local ladder, independently of
candidate code. Write `k_+=2g^2`, `k_-=g^2`, and let `m_sigma(z)` use the
`(h_sigma-z)^(-1)` convention. The half-line Schur recursion gives one atom
and one absolutely continuous band for each endpoint measure. The exterior
Schur signs exclude other atoms; the endpoint vectors are cyclic for `g>0`.
Both densities are positive inside their bands and have square-root edges.

In normalized memory Fock coordinates,
`q_e=(|++>+|-->)/sqrt(2)`, `p=(|++>-|-->)/sqrt(2)`, and
`q_o=|+->=(|LL>-|RR>)/sqrt(2)`. Thus the even and odd hard-core constraints
remove one direction in their respective harmonic sectors. With
`D=L_+'(E)+L_-'(E)` and `L_+(E)+L_-(E)=0`, the actual unit pair is
`psi=(R_++|++>+R_--|-->)/sqrt(D)`. Its bare-pair weight is
`2 L_+(E)^2/D`. Applying the physical number difference gives exactly

```
C = sqrt(2/D),
f(x,y) = C [m_+(E-x)+m_-(E-y)],
integral f d(mu_+ x mu_-) = 0.
```

The factor `sqrt(2)` is required by bosonic normalization. The identity
`V|LR>=0` rules out a bare-pair replacement. For `dnu=dmu_+ dmu_-`, define
`K=int dnu/(x+y-z)`, `J=int f dnu/(x+y-z)`, and
`A=int f^2 dnu/(x+y-z)`. The exact odd compression gives `A-J^2/K`.
The analytic square is essential. Its imaginary part is the positive
Poisson integral of `|f-J/K|^2`, with all four atom/band combinations retained.

The atom-band channels miss `E`. The weighted band-band energy densities are
locally Hölder because the one-body densities have square-root edges and the
source is smooth on each compact support component. The elementary scalar
Plemelj/Poisson boundary theorem therefore applies. Away from an atom-atom
coincidence, `Im K(E+i0)>0`; at coincidence, the common pole cancels exactly
and `J/K` tends to the source value at that atom. I checked that cancellation
algebraically as well. There is consequently a finite scalar boundary value;
no unproved many-body operator limiting-absorption theorem is needed.

The response is the integral of
`r_+(x) r_-(E-x) |C[m_+(E-x)+m_-(x)]-J/K|^2`
over `max(4,E-2)<x<min(6,E)`. This interval has positive length and positive
weight. On a connected real analytic half-line containing the shell, the
unscaled source has the expansion

```
m_+(E-x)+m_-(x)
 = (E-6)/x^2 + (E^2-6E+k_+-k_-)/x^3 + O(x^-4).
```

A constant source would have to vanish at infinity. Its first coefficient
would require `E=6`, and then its second would require `k_+=k_-`, contrary to
`g=1/5`. No complex scalar screening constant can remove this nonconstant
source on a positive interval. This is an analytic strict-sign certificate,
independent of decimal quadrature.

## Case-specific findings

### S41 — ACCEPT

`PROOF.md` sections 1–5 supply all required steps: complete measures, normalized
pair, physical detuning source, exact odd compression, scalar boundary limit,
and moment-based strict positivity. The coincident atom is handled explicitly,
so the conclusion does not depend on a numerical connected shift. The
`0<g<=0.4` extension is supported by its argument and the governing gap bounds.

The continuum and physical Fock scripts replay successfully. The maximum Fock
complex-resolvent discrepancy is `1.63e-15`. The finest replay gives
`rho=2.12750672152351e-8`. Compared with the arbitrary-precision diagnostic
below, the last few shown digits have about `4.3e-10` relative error; tightening
the continuum quadrature alone does not remove floating-point atom/root
sensitivity. This is a numerical precision limitation, explicitly outside its
analytic classification, rather than a target-closing proof gap. No
load-bearing coding defect was found. The lifetime discussion is correctly
conditional.

### S83 — ACCEPT

`RESULT.md` gives a complete self-contained proof. In addition to reconstructing
the common projection/source argument, I checked its distinct pole-based
nonconstancy argument: at distinct atom locations one residue is nonzero; at
coincidence the residue is `w_+-w_-`. Its weight inequality is valid because
`d/sqrt((2+d)^2-1)` has derivative
`(2d+3)/((2+d)^2-1)^(3/2)>0`, while `d` increases with coupling square. Thus
the coincident poles cannot cancel when `k_+>k_-`. The identity-theorem argument
is sound on the connected slit domain containing the shell and these poles.
The wider range remains conditional on the packet's declared gap bounds, as
the endpoint states.

All three scripts replay successfully. The maximum physical-Fock relative
response error is `2.98e-14`; the arbitrary-precision response is
`2.12750672061584377235962562955e-8`. Its normalization is consistent despite
using an unscaled source and placing `2/D` outside the resolvent. No concrete
proof or coding gap blocks the spectral target. Its cited rank-one resonance
paper is background, explicitly not applied to the full perturbation.

### S29 — ACCEPT

`PROOF.md` sections 1–5 verify the target directly at fixed coupling. I checked
the radical atom values in its equation (4) against the exact Schur polynomial
and checked the moment expansion (15). The Plemelj hypotheses are actually
verified, including the off-shell atom-band contributions, rather than merely
asserted. Equation (14) correctly removes a possible coincident atom pole.
The variance argument certifies the sign analytically; the displayed decimal
variance is not itself treated as an interval lower bound.

Continuum, arbitrary-precision, and direct connected-rail Fock scripts all
replay successfully. The maximum Fock resolvent discrepancy is `1.86e-15`;
the high-precision root and density match the independent target formulas.
The endpoint distinguishes the exact source from `|LR>` and retains the
large odd scattering correction. No target-closing proof or coding gap was
found. Its proposed analytic continuation/resonance extension remains unproved
and is labeled accordingly.

### S62 — ACCEPT

`PROOF.md` supplies the same exact physical reduction at fixed coupling and a
valid scalar boundary/sign proof. The normalization, complete spectral
measures, analytic square in the rank-one term, and atom-coincidence treatment
are correct. The large-energy moments exclude constant screening. I checked
the proof against both numerical implementations, rather than accepting the
nested principal-value calculation as an existence proof.

The nested-PV continuum replay, direct Fock check, compressed-matrix check,
and high-precision replay all succeed. Direct Fock resolvent error is
`1.91e-15`. The ordinary continuum replay gives `2.1275067206107768e-8`;
the independent high-precision script gives the value above. One minor
implementation limitation is that `--eps` controls the response integrals but
the `L`/normalization helper uses its default quadrature tolerance; a sweep of
`--eps` therefore is not a uniform accuracy refinement of the entire
calculation. The analytic proof and high-precision check make this nonblocking.
No unconditional lifetime result is claimed.

## Independent executed evidence

`independent_checks.py` imports no candidate code. It constructs the connected
rail one-body operator, builds the two-body Hamiltonian using a symmetric
tensor isometry, removes `LL,RR`, resolves parity, and applies the actual
physical number difference. At bath lengths 3, 5, 7, separately chosen
regulators `.17,.023,.0017` give:

- reconstructed dressed-pair vector error at most `1.4e-14`;
- source-norm discrepancy at most `2.8e-15`;
- direct odd versus rank-one resolvent error at most `4.5e-15`;
- exact zero parity commutator at floating precision.

Its continuum calculation uses Gauss–Legendre integration of the complete
measures, direct double integrals for the pair root/normalization, and fixed
nodes with explicit threshold splits. At 64–1024 nodes per piece it finds
`E=5.978579315166579`, `D=485.98830594766`,
`||Vpsi||^2=0.0370447906242`, and `rho≈2.1275067215e-8`. This independent
double-precision value has the same root/atom sensitivity noted above. Endpoint
second moments are `9.08,9.04`; both complete masses are one to roundoff. The
uncorrected shell value is only `1.42621721824e-11`, and the source's weighted
variance is `1.50513922228e-12`. These decimals corroborate the algebra; they
are not its sign proof.

`boundary_diagnostic.py` independently evaluates the regulated scalar
`A-J^2/K`, integrating one coordinate analytically and evaluating the source
cross term with a resolvent divided difference. At 512 threshold-piece nodes,
the regularized densities for epsilon `1e-5,1e-6,1e-7,1e-8` are respectively
`6.79796e-8,2.59455e-8,2.17421e-8,2.13218e-8`, approaching the shell value.
This is a continuum regulator diagnostic, not a finite-chain extrapolation or
a replacement for the scalar proof.

`additional_controls.json` checks `g=.1,.4` and an equal-coupling reflection
control. In that control, `m_+(6-x)+m_-(x)` vanishes to floating roundoff,
as it should: the unequal-second-moment step is a substantive condition.

The three arbitrary-precision endpoint replays give the common diagnostic
`rho=2.12750672061584377235962562955e-8`. No interval error bound is claimed.
Formal coefficients `pi*rho` and `2*pi*rho` have the stated amplitude/HWHM
and population/FWHM conventions, respectively, **only if** a suitable separate
resonance theorem is established. Local continuation/reduced-resolvent control,
resonance remainders, and a time range for any survival approximation are still
required for dynamics.

See `SOURCE_EXPOSURE.md` for exposure and `replay_summary.json`, replay logs,
`independent_checks.json`, `boundary_diagnostic.json`, and
`additional_controls.json` for reproducible evidence. All writes are inside
`review_a`; SHA-256 verification found no changes in 46 frozen packet and
endpoint files.
