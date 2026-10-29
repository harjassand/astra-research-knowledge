# Acquiring new predictive directions without copying a hidden state

29 October 2026. Root continuation of FINITE_PULSE_CAUSAL_CLOSURE.md.
All rate, equilibrium, and canonical-actuation premises remain.

## 1. Passive feature expansion can fail permanently

Let e_B=(0,0,0,1), labels A={1,2,3}, B={4}, v=(-2,0,1,1), and

    Q=16(J/4-I)+(1/4) v v^T.

This is a symmetric strictly positive off-diagonal generator, stationary uniform.
V=span{1_A,1_B,1_A v} has dimension3 and is invariant under Q and both label
projections. Hence EVERY baseline visible future test lies in V. More baseline
observations cannot provide a fourth direction. The finite bias h=(1,1,1,2)
changes hidden escape activity. Multiplying 1_A v by Q1_B has a nonzero
component along (1,-3,2,0), outside V; the bias does not preserve V.

The exact rational executable builds V from bounded physical tests
1_A,1_B,1_A R_16 1_B, where R_16 is a baseline exponential-clock resolvent.
It verifies zero passive pulse defect and strictly positive finite-bias defect.
Adding 1_A S_h f_j for a detected column raises rank to4 and closes the example.
An independent spectator makes eight microscopic states with the same
four-coordinate controlled record. No physical acquisition was executed.

## 2. Observable weighted adjoint words

Allow a future test to be a fixed word O in visible projections E_a and available
forward resolvents S_h. Its conditional expectation is f=O1, with 0<=f<=1.
Execute the word chronologically; report a product of visible indicator tests.
It may include actual controlled pulses. Such a feature need not be a baseline
future function, so an ordinary reversed baseline past is insufficient.

Detailed balance supplies the correct operation:

    S_h*=H_h^2 S_h H_h^(-2) in L2(pi),       E_a*=E_a.       (1)

For example, O=S_h E_a S_g E_b has
O*=E_b H_g^2 S_g H_g^(-2) E_a H_h^2 S_h H_h^(-2).
Every factor is a forward physical pulse or a known function of a currently
observed label. Therefore

    <f_i,T f_j>_pi=<1,O_i* T O_j1>_pi                       (2)

is acquired in ONE chronological experiment from baseline pi: implement the
adjoint word by forward operations and multiply its observed endpoint weights.
No microscopic reversal, copy, bath-noise playback, or hidden-state restoration
is used. A central H_h^2 acquires the weighted moments of the main theorem.
This obtains G_h,K_h,D_h for controlled future features as well as passive ones.

The identity is numerical reweighting of an actual experiment, not a claim
that the device physically executes an adjoint transition or prepares pi h^2.
Actual intervention data supply the new information. Reversing or stitching
stored passive paths alone cannot create it.

## 3. Weight, preparation, and clock costs

Normalize acquisition h so 1<=h<=R_*. Each adjoint pulse has weight
h(Y_before)^2/h(Y_after)^2<=R_*^2. A left feature containing l pulse stages
therefore has weight range <=R_*^(2l), or <=R_*^(2l+2) including a central
h^2. For h=1+1_b, R_*=2. Some words telescope, but the universal bound is
exponential in depth. The feature f itself remains in[0,1]; a small retained
record does not pay for acquiring its weighted inner products.

Every experiment needs the forward pulses in O_i* and O_j, zero/one/two
central stages, label readings, independent calibrated clocks, and a genuinely
stationary initial preparation. Successive windows on one device are not
automatically iid. Warrant repeated preparation or supply a dependence analysis.
Calibration followed by deployment on the same source also needs the actual
joint history/state law; no reset is inferred from observed equilibration.

## 4. Constructive representation expansion

Start from label indicators. Keep features label-local E_a f, which makes label
invariance exact and keeps constant1 known. Acquire each menu pulse defect.
If R_h is nonzero, positivity implies some diagonal (R_h)_jj>0. Then S_h f_j
lies outside V. Append all label-local E_a S_h f_j; at least one increases
the span. These are actual controlled future words, so (2) acquires the new
Gram entries. Repeat, retaining an independent label-local subset.

Every exact positive defect increases dimension. An n-state source terminates
after at most n-k dimension increases, without n being an input to the final
zero certificate. A countably infinite source may have no finite closed space.
This is not a universal low-rank or efficient-identification theorem.

Finite data do not certify generic exact dependence or zero. Keep a certified
Gram floor; use residual upper bounds for sufficient prediction accuracy and
lower bounds for justified expansion. Ambiguous cases require more data or a
weaker consequence. Pilot selection followed by fresh validation, or a declared
simultaneous confidence allocation, handles adaptive dictionary selection.

## 5. Reach of the principle

The representation is enlarged by actual intervention leakage, and every new
direction has an observation/preparation protocol. Ordinary observable-operator,
residual-DMD and reduced-solver machinery can use the resulting matrices. The
candidate addition is acquiring hidden conditional inner products without
microscopic batched continuations, then completing the specified physical
family. Reweighting, projection residuals and spectral inversion are credited
as existing ingredients. Favorable depth, conditioning and practical costs
remain questions to be answered, not assumptions of the theorem.
