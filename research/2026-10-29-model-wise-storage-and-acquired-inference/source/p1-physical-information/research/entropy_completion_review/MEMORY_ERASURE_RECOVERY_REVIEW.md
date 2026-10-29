# Independent appendix review: memory erasure and sustained-rate recovery

29 October 2026. Reviewed the new Section 9 of
`../ORIENTATION_MEMORY_AND_SUSTAINED_ENTROPY.md`. Its formula and scope
are correct. The result needs a quantitative supplied contraction bound,
not merely finite irreducibility. No previous entropy result was re-audited.

## 1. Checked proof

Let L be a finite irreducible generator with positive stationary rho.
Let Theta be an involution and R=Theta L* Theta. Its stationary law is
rhoTheta, and its escape rate at x equals lambda_Theta(x). Write sigma
for the intrinsic stationary physical-reversal divergence rate of L.
If sigma is infinite, the requested lower bound is automatic; otherwise
the necessary path supports agree.

The path KL with both processes started from the same rho is exactly

    D(P_L^rho[0,t] || P_R^rho[0,t])=t sigma.

Indeed, the initial density cancels. Relative to the direct parity-rate
formula, the rates of R add the gradient
log(rhoTheta_x)-log(rhoTheta_y). Its mean under stationary L traffic is
zero. The escape-rate contribution is unchanged. The R process in this
comparison need not be stationary.

Suppose the Dobrushin coefficient of exp(tR) is at most a supplied
beta<1, for a specified t>0. Endpoint contraction of KL and Pinsker give

    TV(rho,rho exp(tR))<=sqrt(t sigma/2).

Since rhoTheta exp(tR)=rhoTheta, putting d=TV(rho,rhoTheta) gives

    d<=sqrt(t sigma/2)+beta d,
    d<=sqrt(t sigma/2)/(1-beta).

For a window T, compare P_L^rho with P_R^rho, and then change the latter
initial distribution to rhoTheta. The first path-TV difference is at
most sqrt(T sigma/2). The second is at most d by contraction under the
common R path kernel; for complete microscopic paths including time zero
it actually equals d. P_R^(rhoTheta) is the physical reversal of the
stationary L law. Therefore, for an equivariant observed reversal,

    Delta_T<=sqrt(sigma/2)[sqrt(T)+sqrt(t)/(1-beta)],

and hence

    sigma>=2 Delta_T^2/[sqrt(T)+sqrt(t)/(1-beta)]^2.

The written root proof correctly specializes to an even readout. Without
that condition, Delta_T must include the physically prescribed parity
action on observed labels. Ordinary time reversal of an arbitrary odd
readout would not justify the bound.

## 2. Bounded-score normalization

For a reversal-odd statistic f with |f|<=M, the reversed mean is minus
the forward mean. Its expectation difference is therefore 2|E f| and
its range is at most 2M. Consequently

    Delta_T>=|E f|/M.

For M=1 this is exactly the root's stated normalization. Alternatively,
if a general bounded statistic of range L has a certified forward/reverse
mean gap gamma, use Delta_T>=gamma/L. Confidence bounds and any witness
selection must be validated under the actual preparation/sampling
contract. Irregular grids require the reflected grid, as stated.

## 3. Forward hidden contraction is also sufficient

The same conclusion holds if a supplied Dobrushin bound is available for
exp(tL) instead. The physical reverse of R is L, and their intrinsic
rates coincide. One way to verify the latter is that physical path
reversal is an involution: the two stationary path KLs are equal, as are
their initial parity-divergence terms.

Apply the same-initial comparison with stationary R started from
rhoTheta and L started from rhoTheta. Endpoint Pinsker gives
TV(rhoTheta,rhoTheta exp(tL))<=sqrt(t sigma/2). Contraction toward rho
then bounds the same d and yields the identical observed-rate inequality.
This optional variant does not make a hidden contraction bound observable
from a few forward correlation measurements.

## 4. Scope

Finite irreducibility implies a contraction coefficient below one at
positive times for each individual finite model. The recovery claim
requires a supplied numerical bound at a supplied time that holds across
the admissible explanations. Mere existence of a model-dependent bound
does not exclude the orientation-memory sequence.

In that sequence the orientation process has decay rate kappa, so both
forward and reversed hidden Dobrushin coefficients are at least
exp(-kappa t). A uniform beta<1 at fixed t excludes its slow-orientation
limit. State count and maximum escape rate do not provide such a bound.

The lemma restores a lower bound from observed physical time asymmetry.
It is not a complete characterization of hidden dissipation, does not
recover the stronger all-even tree class when arbitrary parity is still
admitted, and does not acquire a reverse control or contraction estimate.
Its ingredients are standard KL perturbation, Pinsker and Dobrushin
contraction, exactly as the root states.
