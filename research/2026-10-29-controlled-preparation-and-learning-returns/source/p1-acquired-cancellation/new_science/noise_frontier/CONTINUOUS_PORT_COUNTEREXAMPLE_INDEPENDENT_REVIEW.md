# Independent review: a native continuous observed thermal port obstruction

29 October 2026. Causal-noise frontier review requested by root. Read the entire
new proof and executable. This is not a predecessor re-audit. No author source
was modified; exact review inputs are preserved under reviewed_continuous_port/.

Reviewed proof SHA256:

    23afb29c346be83f38455efccb345ff6ea1c24a91e6840e65d46554120ffac6e

Reviewed executable SHA256:

    095537aeff1dc0c2faa67492b9ed6579d9b0f3af1b346a9c2fd43bb463132c61

## Finding

The construction and nonlinear-response separation are correct at the stated
native SWITCHING-DIFFUSION scope. It supplies a stronger physical obstruction
than an abstract hidden jump network: the observed circle coordinate is directly
thermalized with known constant mobility/noise, both sources are reversible,
and the applied conjugate force is the same real potential operation. Hidden
internal states remain discrete. No claim for a purely diffusive hidden space
follows from this proof.

One wording clarification should accompany any summary: equality after static
bias refers to the ONE-TIME observed equilibrium distribution. Equality of the
complete stationary observed PATH law after every bias is not proved and is
not needed. The complete path-law equality established here is at baseline.
The original Section4 formula already makes the one-time statement explicit.

## 1. Native positivity and equilibrium

The rational matrix O is symmetric orthogonal and fixes 1. The vectors a and
Oa have positive components. With epsilon=1/10, psi_i>=3/5 and
psi_tilde_i>=19/30. Therefore both ground-state transformations are nonsingular.

Direct expansion gives

    D_i-30=epsilon(70-31a_i)cos x/(1+epsilon a_i cos x).

The maximum numerator magnitude is 54epsilon and the denominator is at least
3/5, so |D_i-30|<=9. Orthogonal conjugation preserves the operator norm of
diag(D_i-30), hence each rotated off-diagonal entry has magnitude at most9.
Since the unperturbed off-diagonal entry is -10, W_tilde,ij<=-1. This is a
uniform continuum bound, not an inference from the four sampled angles in
the executable. Both sets of jump rates are strictly positive and bounded.

H psi=0 follows by substitution. Expanding psi^-1[-H(psi f)] yields scalar
diffusion f_i''+2psi_i'/psi_i f_i' and exactly the claimed jump differences.
The same calculation applies after rotation. Smooth coefficients on a compact
circle with bounded finite-state jump rates give a conservative nonexplosive
switching diffusion. Strictly positive internal rates and elliptic coordinate
diffusion give irreducibility and the unique equilibrium described in the note.

Normalization is Z=pi(6+21epsilon^2). Diffusion reversibility follows from
b_i=partial_x log(psi_i^2), and jump flux symmetry is

    psi_i^2 q_ij=-W_ij psi_i psi_j=psi_j^2 q_ji.

The energy U_i=-2log psi_i and symmetric prefactor -W_ij give the ordinary
single-temperature local-detailed-balance interpretation. Their x dependence
does not invalidate this switching-diffusion construction.

## 2. Equality of all baseline observed paths

The ground-state similarity changes the stationary observed correlation into
the displayed matrix Schrödinger-semigroup inner product. A scalar multiplication
M_f commutes with the CONSTANT O, as does the scalar differential part. Inserting
O^2 between factors and replacing psi by Opsi proves equality for every finite
collection of bounded observed functions and times. Orthogonality gives the
same observed density pointwise and the same Z.

Finite-dimensional distributions determine the measure on continuous circle
paths, so equality is genuinely complete at baseline. This does not presume
the internal rotation to be a positive state relabeling; native positivity was
established independently in Section1. Independent multiple baseline records
and common randomized processing preserve this equality.

## 3. The common actuation is physically specified

Adding external energy -alpha cos x to every internal state adds force
-alpha sin x to the same directly thermalized coordinate. It leaves every
internal energy DIFFERENCE at fixed x unchanged. Holding the symmetric kinetic
prefactors fixed, or shifting each transition barrier by the same external
potential, indeed leaves internal jump rates unchanged. Consequently the actual
generator is L+alpha D, D=v'(x)partial_x, in BOTH sources.

Detailed balance alone would not force a unique barrier response, but the note
explicitly supplies the common barrier/kinetic operation. It does not claim that
operation was inferred from observed equilibrium trajectories.

The biased equilibrium is proportional to psi_i^2 exp(alpha v). Summing over
internal states proves identical one-time observed equilibrium distributions
for every alpha. The response experiment instead starts in each source's own
baseline equilibrium, with the same observed initial distribution and the stated
native hidden equilibrium preparations.

## 4. Third-time-derivative calculation

For every smooth vector g, reversibility and the diffusion Dirichlet form give

    E[Dg]=-E[v Lg].

The internal jump part makes no contribution because v is identical across
internal states at each x. Stationarity kills every term with a leftmost L in
the expansion of E[(L+alpha D)^k f]. Through k=2, all remaining terms match
because they are baseline observed correlations or scalar functions integrated
against the common observed density.

At k=3 the surviving terms are exactly

    alpha E[D L^2 f]
      +alpha^2(E[D L Df]+E[D^2 Lf])+alpha^3 E[D^3 f].

The first, second-order DLDf, and cubic terms match by the same observed
correlation identity. Since Lf=f''+b_i f', direct differentiation gives

    D^2 Lf=(v')^2(f''''+b_i''f'+2b_i'f''+b_i f''')
                 +v'v''(f'''+b_i'f'+b_i f'').

The conditional b and b' averages are invariant under O; the ONLY surviving
difference is (v')^2 f' times the conditional b'' difference. Multiplying
b_i'' by psi_i^2 gives

    2(psi_i psi_i'''-3psi_i'psi_i''+2psi_i'^3/psi_i),

so the two invariant inner products cancel and the difference is precisely
-4epsilon^3 sin^3 x DeltaS(epsilon cos x)/Z. For v=f=cos x the extra f'=-sin x
makes the response integrand positive, sin^6 x DeltaS.

The exact numerator identity for DeltaS, positivity of all six denominator
factors, numerator minimum116/45 and denominator maximum479864/140625 are
correct. The numerator minimum occurs at t=-1/10 because its derivative is
positive throughout the interval. Dividing gives DeltaS>=90625/119966.
Since integral_0^(2pi) sin^6 x dx=5pi/8, the final coefficient obeys

    C >= C_lo=90625/297995544 >0.

Thus the third derivative gap is alpha^2 C, while lower time derivatives agree.
The claim that the distinction begins at quadratic RESPONSE order is correct;
its leading short-time appearance is cubic in elapsed time.

## 5. Ordinary remainder and a precise existence bound

For fixed alpha, all coefficients are smooth on the compact hybrid space.
The bounded smooth test f lies in the domain of (L+alpha D)^4 and of its tilded
counterpart. Repeated Dynkin expansion, with Markov sup-norm contraction, bounds
the combined fourth-order remainder by B4 t^4/24, where

    B4=||(L+alpha D)^4 f||_infinity
                     +||(L_tilde+alpha D)^4 f||_infinity < infinity.

Hence, whenever 0<t<=2alpha^2 C_lo/B4 (with the zero-B4 case handled directly),

    F_alpha(t)-F_tilde_alpha(t)>=alpha^2 C_lo t^3/12,
    TV(endpoint observed laws)>=alpha^2 C_lo t^3/24.

This gives an ordinary positive-time separation without appealing only to a
formal Taylor series. B4 has not been numerically instantiated; the executable
does not report a calibrated numerical time window or measured gap.

## 6. Executable check and its actual scope

Ran an UNMODIFIED COPY of check_reversible_continuous_port.py beside the copied
proof, so the original receipt and source were not overwritten. Exit code0,
status PASS. The printed rational coefficient was 90625/297995544, decimal
0.0003041152856970237.

The program correctly checks O's algebra, moment identities, the full rational
DeltaS numerator, continuum-bound constants, and generator flux identities at
four rational trigonometric points. It does not numerically establish global
positivity, semigroup equivalence, the derivative expansion, or a physical
experiment. Those are supplied by the ordinary arguments reviewed above.

The review copies, fresh executable output and input hashes are in
reviewed_continuous_port/. No mathematical correction to the author's proof
or executable was necessary. The static-equilibrium wording clarification is
recorded here rather than changing the preserved source.
