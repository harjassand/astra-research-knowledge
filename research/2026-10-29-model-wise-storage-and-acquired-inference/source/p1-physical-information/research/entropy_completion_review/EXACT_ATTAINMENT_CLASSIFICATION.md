# Exact finite attainment of the native entropy floor

29 October 2026. Independent continuation of root's entropy-completion
converse. This establishes a finite-record criterion alongside the closure
theorem. A comprehensive priority search for this classification is not
complete. Its ingredients are phase-type reversal, exponential tilting,
and equality in relative-entropy data processing.

## 1. The criterion

Assume the finite native port setup of the independent review: positive
port weights, fixed holding clocks, balanced irreducible port traffic,
reciprocal direct support, and finite observed event divergence J. Every
nonzero positive-duration pair density K_ij is assumed phase-type after
normalization. This holds whenever the target record comes from a finite
CTMC; the conditioning argument is given below.

**Theorem.** There exists an exact finite CTMC completion, with arbitrary
hidden parity fixing the ports, that attains intrinsic E=J if and only if
for every nonzero off-diagonal pair there are constants C_ij>0 and real
delta_ij such that

    K_ij(t)/K_ji(t)=C_ij exp(delta_ij t),  t>0.              (1)

The completion preserves all port weights, direct fluxes, endpoint flux
masses, holding rates, and total hidden mass/mean. Its hidden state count
and rates are finite but otherwise unconstrained. The reverse constants
are C_ji=1/C_ij and delta_ji=-delta_ij. Self-return pairs have ratio one
and need no additional condition.

This is exact attainment by one finite model. It does not classify the
infimum over models that reproduce a fixed record exactly when (1) fails.
That infimum need not be attained and can even be infinite, as in root's
one-phase/two-phase example. The weighted-L1 closure floor remains J.

## 2. Necessity

Let mu be the complete microscopic excursion-flux measure and mu^R its
parity reversal. E=D_flux(mu||mu^R) and J is its image divergence under
the endpoint-duration observation (i,j,t). Equality makes dmu/dmu^R a
measurable function of that observation.

Fix any positive-rate hidden itinerary Gamma=(i,x_1,...,x_l,j). Its
likelihood ratio has form

    C_Gamma exp{sum_r b_xr s_r},
    b_x=lambda_Theta(x)-lambda_x,

where the s_r>0 are its hidden holding durations. The conditional dwell
density on sum s_r=t is positive over the full simplex. A function only
of t therefore requires every b_xr along Gamma to be equal. The path
ratio is C_Gamma exp(delta_Gamma t).

Every finite positive-rate itinerary has positive duration density for
every t>0. Thus all itineraries with the same endpoints must give the
same exponential function. That function is K_ij/K_ji, proving (1).
A missing reverse itinerary would instead make E infinite. Direct atoms
are separate and do not affect this argument.

## 3. Reversing one phase-type channel

Write a forward pair density as

    K_ij(t)=a alpha exp(Tt) r,
    alpha 1=1,  r=-T1>=0,

where T is a finite transient subgenerator and a=F_ij>0. Trim unused
phases so each remaining phase has positive occupation. Its occupation
row vector under excursion flux a is

    z=a alpha(-T)^-1 >0.

Let D_z=diag(z). The reversed-path phase-type representation is

    T_left=D_z^-1 T^T D_z,
    (beta_left)_x=z_x r_x/a,
    r_left=a alpha^T elementwise-divided-by z.

Here beta_left is a row vector. Its components sum to one because z r=a.
The identity z T=-a alpha gives T_left 1=-r_left, so this is a valid
transient phase-type channel. Its duration density equals the forward
density after normalization. More strongly, its microscopic path measure
is the time reversal of the original channel's path measure.

For the final CTMC, the forward entrance rates from port i are
a alpha_x/w_i, the internal rates are T_xy, and absorption at j has
rate r_x. Its stationary hidden weights are z.

## 4. Tilting the reversed channel to the required reverse density

Assume (1), write C=C_ij and delta=delta_ij, and let b=F_ji. The required
reverse excursion measure is the reversed forward measure multiplied by

    exp(-delta t)/C.

Its total mass is b. Define

    h=(-T_left+delta I)^-1 r_left,
    Z=beta_left h=b C/a.

All h_x are finite and strictly positive. Finiteness follows from the
finite exponential moment Z and reachability of every retained phase in
the reversed channel. Equivalently, T_left-delta I is transient on this
trimmed phase space. Now perform the standard positive h-transform:

    T_minus=D_h^-1(T_left-delta I)D_h,
    r_minus=D_h^-1 r_left,
    beta_minus=beta_left D_h/Z.

The row identity (T_left-delta I)h=-r_left makes this a valid finite
transient subgenerator with exit vector r_minus. Its initial law sums to
one. Give it entrance flux b beta_minus from port j and absorption at i.
The entrance flux also has the useful component expression

    b(beta_minus)_x=z_x r_x h_x/C.

Its duration density is exactly

    b beta_minus exp(T_minus t) r_minus
       =K_ij(t)exp(-delta t)/C=K_ji(t).

The stationary reverse hidden weights must be computed as

    z_minus=b beta_minus(-T_minus)^-1.

They are generally NOT z elementwise-times h/C. That tempting expression
fails the balance equations when delta is nonzero.

Pair each forward phase x with the corresponding reverse phase x under
Theta. Their escape rates differ by the common amount delta:

    lambda_minus,x=lambda_plus,x+delta.

The entrance, internal and exit jump ratios telescope. Including the
native port-weight factor, a complete forward microscopic path has
likelihood ratio precisely C exp(delta t). Thus its reversal likelihood
is already measurable from endpoint and total duration. Data processing
is an equality, and the pair contributes exactly its observed J.

Both channels are finite, and every positive transition has its required
parity-reversed partner. Their occupation masses equal the exact forward
and reverse duration means. No limiting clocks, histogram approximation,
or stationary parity symmetry is needed.

## 5. Assemble the complete record

Use the preceding paired channels independently for each unordered
nonzero off-diagonal endpoint pair. For a self-return density K_ii,
construct a phase-type channel and its reversed-path copy, each with half
the flux, both returning to i. Swap these copies under Theta. Their sum
preserves K_ii exactly and has zero intrinsic reversal divergence.

Keep direct rates d_ij/w_i. Native flux balance makes all port stationarity
equations hold. Each hidden channel carries its own exact occupation
weights. The total hidden mass is the target sum of all first moments,
and the retained port clocks are their prescribed rho_i/w_i. The native
port graph ensures irreducibility of the assembled model after trimming
unused phases. Its microscopic excursion ratio is the native ratio in
every channel, so E=J globally. This proves sufficiency.

## 6. Why finite CTMC pair laws are phase-type

Suppose the target kernel has representation A_i exp(Tt) b_j, with T the
killed hidden generator. Let h_j=(-T)^-1 b_j, the probability of eventual
exit at j from each hidden state. Restrict to phases with h_j>0 reachable
from the entrance. Conditioning on exit at j gives

    T_j=D_hj^-1 T D_hj,
    r_j=D_hj^-1 b_j,
    alpha_j=A_i D_hj/F_ij.

Then T_j 1=-r_j, alpha_j 1=1, and the conditional duration density is
alpha_j exp(T_j t)r_j. Thus each nonzero endpoint-conditioned law is
phase-type. The theorem covers all records supplied by finite CTMCs,
including ones whose original hidden phases were shared across pairs.
The construction may duplicate those phases; no minimal state claim is
made.

## 7. Nontrivial exact rational example

Take forward mass a=3 and

    alpha=(1/3,2/3),
    T=[[-3,1],[1/2,-2]],     r=(2,3/2),
    z=(6/11,14/11).

Choose delta=1/2 and C=76/99, making reverse mass b=3. The reverse channel
constructed above has

    beta_minus=(7/19,12/19),
    T_minus=[[-7/2,8/7],[7/16,-5/2]],
    r_minus=(33/14,33/16),
    z_minus=(91/209,200/209).

With port weights (1,2), this is a six-state irreducible completion. Its
port rates are (3,3/2), and its exact native ratio is

    K_12(t)/K_21(t)=(76/99)exp(t/2).

The forward and reverse duration flux means are 20/11 and 291/209.
Their equal total fluxes cancel the constant log C term, giving

    E=J=(1/2)(20/11-291/209)=89/418.

The stationary mean jump log-ratio contribution vanishes here. The entire
intrinsic entropy comes from the paired escape-rate differences. Thus
the example also checks the holding term that disappears in root's
equal-clock Erlang approximation but must be retained in the general
definition.

## 8. Executable check and limits

The companion `check_entropy_completion.py` constructs this example from
the forward PH data, rather than only substituting the displayed reverse
constants. It computes z, the reversed generator, h, C, the tilted
generator and its actual stationary occupation weights with Fraction.
It verifies stationarity, native port clocks, five shifted-Laplace
identities, and the exact holding contribution 89/418. High-precision
Decimal evaluation of the full rate formula checks cancellation of the
jump terms against the separately proved exact identity. The combined
checker reports PASS in `ENTROPY_COMPLETION_CHECKS.json` and generates
no source observations.
